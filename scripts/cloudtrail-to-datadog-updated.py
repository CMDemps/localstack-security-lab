#!/usr/bin/env python3
"""
CloudTrail to Datadog Log Forwarder
Fetches CloudTrail events from LocalStack and sends them to Datadog as structured logs
Author: Clayton Demps
Date: December 2025
"""

import boto3
import json
import requests
import time
import os
from datetime import datetime, timedelta, timezone

# Configuration
LOCALSTACK_ENDPOINT = "http://localhost:4566"
DATADOG_API_KEY = os.environ.get('DD_API_KEY')
DATADOG_SITE = os.environ.get('DD_SITE', 'us5.datadoghq.com')
DATADOG_LOG_ENDPOINT = f"https://http-intake.logs.{DATADOG_SITE}/api/v2/logs"

# Track processed event IDs to avoid duplicates
processed_event_ids = set()

# CloudTrail client
cloudtrail = boto3.client(
    'cloudtrail',
    endpoint_url=LOCALSTACK_ENDPOINT,
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

def fetch_cloudtrail_events(start_time=None, max_results=50):
    """Fetch CloudTrail events from LocalStack"""
    try:
        params = {'MaxResults': max_results}
        
        if start_time:
            params['StartTime'] = start_time
        
        response = cloudtrail.lookup_events(**params)
        return response.get('Events', [])
    except Exception as e:
        print(f"Error fetching CloudTrail events: {e}")
        return []

def format_event_for_datadog(event):
    """Format CloudTrail event for Datadog ingestion"""
    try:
        # Parse the CloudTrail event
        cloud_trail_event = json.loads(event.get('CloudTrailEvent', '{}'))
        
        # Create Datadog log entry with CloudTrail attributes
        datadog_log = {
            "ddsource": "aws.cloudtrail",
            "ddtags": "env:dev,project:security-lab,service:localstack-security-lab",
            "hostname": "localstack-wsl",
            "service": "localstack-security-lab",
            "message": f"{cloud_trail_event.get('eventName', 'Unknown')} by {cloud_trail_event.get('userIdentity', {}).get('principalId', 'Unknown')}",
            
            # CloudTrail specific attributes
            "evt": {
                "name": event.get('EventName'),
                "id": event.get('EventId'),
                "time": event.get('EventTime').isoformat() if event.get('EventTime') else None,
                "source": event.get('EventSource'),
                "type": cloud_trail_event.get('eventType'),
                "version": cloud_trail_event.get('eventVersion')
            },
            
            # User identity
            "usr": {
                "name": event.get('Username'),
                "id": cloud_trail_event.get('userIdentity', {}).get('principalId'),
                "type": cloud_trail_event.get('userIdentity', {}).get('type'),
                "arn": cloud_trail_event.get('userIdentity', {}).get('arn'),
                "account_id": cloud_trail_event.get('userIdentity', {}).get('accountId')
            },
            
            # AWS specific
            "aws": {
                "region": cloud_trail_event.get('awsRegion'),
                "service": event.get('EventSource'),
                "account_id": cloud_trail_event.get('recipientAccountId')
            },
            
            # Network
            "network": {
                "client": {
                    "ip": cloud_trail_event.get('sourceIPAddress')
                }
            },
            
            # HTTP
            "http": {
                "useragent": cloud_trail_event.get('userAgent'),
                "url": event.get('EventSource')
            },
            
            # Resources
            "resources": event.get('Resources', []),
            
            # Request/Response
            "request_parameters": cloud_trail_event.get('requestParameters'),
            "response_elements": cloud_trail_event.get('responseElements'),
            "error_code": cloud_trail_event.get('errorCode'),
            "error_message": cloud_trail_event.get('errorMessage'),
            
            # Full CloudTrail event for reference
            "cloudtrail_event": cloud_trail_event
        }
        
        return datadog_log
    except Exception as e:
        print(f"Error formatting event: {e}")
        return None

def send_to_datadog(logs):
    """Send logs to Datadog"""
    if not logs:
        return
    
    if not DATADOG_API_KEY:
        print("ERROR: DD_API_KEY environment variable not set!")
        return
    
    headers = {
        'DD-API-KEY': DATADOG_API_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(
            DATADOG_LOG_ENDPOINT,
            headers=headers,
            json=logs
        )
        
        if response.status_code == 202:
            print(f"✅ Successfully sent {len(logs)} events to Datadog")
        else:
            print(f"❌ Error sending to Datadog: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception sending to Datadog: {e}")

def main():
    """Main function - fetch and forward CloudTrail events"""
    print("=" * 60)
    print("CloudTrail to Datadog Log Forwarder")
    print("=" * 60)
    print(f"LocalStack Endpoint: {LOCALSTACK_ENDPOINT}")
    print(f"Datadog Site: {DATADOG_SITE}")
    print(f"Datadog API Key: {'Set ✅' if DATADOG_API_KEY else 'Not Set ❌'}")
    print("=" * 60)
    print()
    
    if not DATADOG_API_KEY:
        print("ERROR: Please set DD_API_KEY environment variable!")
        print("Export it with: export DD_API_KEY='your-api-key'")
        return
    
    # Track last processed event time
    last_event_time = datetime.now(timezone.utc) - timedelta(hours=1)
    
    # Track if waiting message has been shown
    waiting_message_shown = False
    
    print("Starting to monitor CloudTrail events...")
    print("Press Ctrl+C to stop")
    print()
    
    try:
        while True:
            # Fetch events
            events = fetch_cloudtrail_events(start_time=last_event_time, max_results=50)
            
            if events:
                print(f"📊 Found {len(events)} new CloudTrail events")
                waiting_message_shown = False  # Reset
                
                # Format for Datadog
                datadog_logs = []
                for event in events:
                    event_id = event.get('EventId')
                    
                    # Skip if already processed
                    if event_id in processed_event_ids:
                        continue
                    
                    # Skip LookupEvents (the script's own monitoring activity)
                    event_name = event.get('EventName')
                    if event_name == 'LookupEvents':
                        processed_event_ids.add(event_id)
                        continue
                    
                    formatted_event = format_event_for_datadog(event)
                    if formatted_event:
                        datadog_logs.append(formatted_event)
                        processed_event_ids.add(event_id)  # Mark as processed
                        
                        # Update last event time
                        event_time = event.get('EventTime')
                        if event_time and event_time > last_event_time:
                            last_event_time = event_time
                
                # Send to Datadog
                if datadog_logs:
                    send_to_datadog(datadog_logs)
                    print(f"   Events: {', '.join([e['evt']['name'] for e in datadog_logs[:5]])}")
                    if len(datadog_logs) > 5:
                        print(f"   ... and {len(datadog_logs) - 5} more")
                print()
            else:
                if not waiting_message_shown:
                    print("⏳ No new events, waiting...")
                    waiting_message_shown = True
            
            # Wait before next check
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping CloudTrail forwarder...")
        print("Goodbye!")

if __name__ == "__main__":
    main()
