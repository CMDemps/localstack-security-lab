# CloudTrail Setup and Configuration

## Overview

CloudTrail is AWS's logging and auditing service that records all API calls made to AWS services. This is critical for security monitoring, incident response, and compliance.

## What CloudTrail Logs

CloudTrail captures:

- **Who** made the API call (user/role identity)
- **What** action was performed (API operation)
- **When** it occurred (timestamp)
- **Where** it came from (source IP address)
- **Which** resources were affected
- **What** the response was (success/failure)

## Setup Process

### Prerequisites

- LocalStack running with Pro/Student license activated
- `awslocal` CLI wrapper configured
- Auth token set as environment variable

### Automated Setup

Run the setup script:

```bash
./scripts/cloudtrail-setup-script.sh
```

### Manual Setup

If you prefer to set up CloudTrail manually:

1. **Create S3 bucket for logs:**

   ```bash
   awslocal s3 mb s3://cloudtrail-logs-bucket
   ```

2. **Create the trail:**

   ```bash
   awslocal cloudtrail create-trail \
       --name security-audit-trail \
       --s3-bucket-name cloudtrail-logs-bucket
   ```

3. **Start logging:**

   ```bash
   awslocal cloudtrail start-logging --name security-audit-trail
   ```

4. **Verify it's working:**

   ```bash
   awslocal cloudtrail get-trail-status --name security-audit-trail
   ```

## Using CloudTrail for Security Monitoring

### View Recent Events

To see the most recent API calls:

```bash
awslocal cloudtrail lookup-events --max-results 20
```

### Filter Events by User

```bash
awslocal cloudtrail lookup-events \
    --lookup-attributes AttributeKey=Username,AttributeValue=test-user
```

### Filter Events by Resource

```bash
awslocal cloudtrail lookup-events \
    --lookup-attributes AttributeKey=ResourceName,AttributeValue=my-bucket
```

### Search by Time Range

```bash
awslocal cloudtrail lookup-events \
    --start-time 2025-12-11T00:00:00Z \
    --end-time 2025-12-11T23:59:59Z
```

## Security Use Cases

### 1. Detecting Unauthorized Access

Monitor for API calls from unexpected users or IP addresses:

```bash
awslocal cloudtrail lookup-events --max-results 50 | grep "errorCode"
```

### 2. Tracking Privilege Escalation

Look for IAM policy changes or role assumptions:

```bash
awslocal cloudtrail lookup-events \
    --lookup-attributes AttributeKey=EventName,AttributeValue=AttachUserPolicy
```

### 3. Monitoring S3 Bucket Access

Track who's accessing sensitive S3 buckets:

```bash
awslocal cloudtrail lookup-events \
    --lookup-attributes AttributeKey=ResourceType,AttributeValue=AWS::S3::Bucket
```

### 4. Incident Response

During a security incident, CloudTrail logs are your first stop to understand:

- What happened?
- When did it happen?
- Who did it?
- What data was accessed?

## LocalStack-Specific Behavior

**Note:** In LocalStack, CloudTrail's S3 log file delivery may be delayed or work differently than production AWS. However, the `lookup-events` API works perfectly and provides real-time access to all logged events.

This is actually ideal for learning because:

- You get immediate feedback via `lookup-events`
- You can practice CloudTrail queries without waiting for log files
- It simulates the CloudTrail API perfectly

## Event Structure

Each CloudTrail event contains:

```json
{
    "eventVersion": "1.08",
    "userIdentity": {
        "type": "IAMUser",
        "principalId": "AIDAI...",
        "arn": "arn:aws:iam::000000000000:user/admin",
        "accountId": "000000000000",
        "userName": "admin"
    },
    "eventTime": "2025-12-11T18:30:00Z",
    "eventSource": "s3.amazonaws.com",
    "eventName": "CreateBucket",
    "awsRegion": "us-east-1",
    "sourceIPAddress": "127.0.0.1",
    "userAgent": "aws-cli/2.x",
    "requestParameters": {
        "bucketName": "my-test-bucket"
    },
    "responseElements": null,
    "requestID": "abc123...",
    "eventID": "def456...",
    "eventType": "AwsApiCall",
    "recipientAccountId": "000000000000"
}
```

## Best Practices

1. **Always enable CloudTrail** in any AWS environment
2. **Store logs in a secure bucket** with restricted access
3. **Enable log file validation** to detect tampering
4. **Set up alerts** for suspicious activities
5. **Regular log analysis** to identify patterns
6. **Retain logs** according to compliance requirements

## Troubleshooting

### CloudTrail Not Logging

Check if logging is enabled:

```bash
awslocal cloudtrail get-trail-status --name security-audit-trail
```

If not, start it:

```bash
awslocal cloudtrail start-logging --name security-audit-trail
```

### No Events Showing

Ensure you're performing actions that generate events:

```bash
awslocal s3 ls  # This generates an event
awslocal iam list-users  # This also generates an event
```

Then check again:

```bash
awslocal cloudtrail lookup-events --max-results 5
```

## Next Steps

With CloudTrail configured, you can now:

- Set up IAM users and roles with different permissions
- Create intentional security misconfigurations
- Practice detecting suspicious activities in logs
- Build automated security monitoring scripts

## Additional Resources

- [AWS CloudTrail Documentation](https://docs.aws.amazon.com/cloudtrail/)
- [LocalStack CloudTrail Coverage](https://docs.localstack.cloud/references/coverage/coverage_cloudtrail/)
- [CloudTrail Event Reference](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference.html)
