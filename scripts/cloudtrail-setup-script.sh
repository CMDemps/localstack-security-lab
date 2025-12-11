#!/bin/bash
# CloudTrail Setup Script for LocalStack Security Lab
# This script sets up CloudTrail logging for security monitoring and auditing
# Author: Clayton Demps
# Date: December 2025

echo "=========================================="
echo "LocalStack CloudTrail Setup"
echo "=========================================="
echo ""

# Check if LocalStack is running
echo "[1/5] Checking if LocalStack is running..."
if ! awslocal s3 ls &> /dev/null; then
    echo "❌ Error: LocalStack is not running or not accessible"
    echo "Please start LocalStack with: localstack start -d"
    exit 1
fi
echo "✅ LocalStack is running"
echo ""

# Create S3 bucket for CloudTrail logs
echo "[2/5] Creating S3 bucket for CloudTrail logs..."
if awslocal s3 mb s3://cloudtrail-logs-bucket 2>/dev/null; then
    echo "✅ Created bucket: cloudtrail-logs-bucket"
else
    echo "ℹ️  Bucket already exists: cloudtrail-logs-bucket"
fi
echo ""

# Create CloudTrail trail
echo "[3/5] Creating CloudTrail trail..."
if awslocal cloudtrail create-trail \
    --name security-audit-trail \
    --s3-bucket-name cloudtrail-logs-bucket 2>/dev/null; then
    echo "✅ Created trail: security-audit-trail"
else
    echo "ℹ️  Trail already exists: security-audit-trail"
fi
echo ""

# Start CloudTrail logging
echo "[4/5] Starting CloudTrail logging..."
awslocal cloudtrail start-logging --name security-audit-trail
echo "✅ CloudTrail logging started"
echo ""

# Verify CloudTrail status
echo "[5/5] Verifying CloudTrail status..."
STATUS=$(awslocal cloudtrail get-trail-status --name security-audit-trail)
echo "$STATUS"
echo ""

echo "=========================================="
echo "✅ CloudTrail Setup Complete!"
echo "=========================================="
echo ""
echo "CloudTrail is now logging all API calls"
echo "View recent events with:"
echo " awslocal cloudtrail lookup-events --max-results 10"
echo ""
echo "Check log bucket contents with:"
echo " awslocal s3 ls s3://cloudtrail-logs-bucket/AWSLogs/ --recursive"
echo ""
