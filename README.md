# LocalStack Security Lab 🔐

![AWS](https://img.shields.io/badge/AWS-LocalStack-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Security](https://img.shields.io/badge/Security-Testing-red?style=for-the-badge&logo=security&logoColor=white)

## 📋 Project Overview

A comprehensive cloud security testing environment built with LocalStack to simulate AWS infrastructure and practice cloud security configurations, penetration testing methodologies, and security monitoring. This project demonstrates hands-on experience with AWS services, security best practices, and infrastructure-as-code principles.

## 🎯 Learning Objectives

- **Cloud Security Fundamentals**: Understanding AWS IAM, security groups, and access controls
- **Security Misconfiguration Detection**: Identifying and exploiting common cloud misconfigurations
- **Logging & Monitoring**: Implementing CloudTrail, CloudWatch, and security event analysis
- **Infrastructure as Code**: Automating security configurations using AWS CLI and scripts
- **Incident Response**: Analyzing logs and detecting suspicious activities

## 🛠️ Technologies Used

- **LocalStack**: AWS cloud service emulator for local development
- **AWS CLI**: Command-line interface for AWS services
- **Docker**: Container platform for running LocalStack
- **Python**: Scripting and automation
- **Git/GitHub**: Version control and documentation
- **CloudTrail**: AWS API logging and monitoring
- **IAM**: Identity and Access Management testing
- **S3**: Object storage and bucket policy testing

## 🏗️ Architecture

```text
┌─────────────────────────────────────────┐
│         LocalStack Container            │
│  ┌───────────────────────────────────┐  │
│  │   AWS Services (Emulated)         │  │
│  │  • S3                             │  │
│  │  • IAM                            │  │
│  │  • CloudTrail                     │  │
│  │  • CloudWatch Logs                │  │
│  │  • Lambda                         │  │
│  │  • DynamoDB                       │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
           ↕ (API Calls)
┌─────────────────────────────────────────┐
│         AWS CLI / Scripts               │
└─────────────────────────────────────────┘
```

## 🚀 Getting Started

### Prerequisites

- Windows 10/11, macOS, or Linux
- Docker Desktop installed and running
- Python 3.x installed
- AWS CLI v2 installed
- Git installed

### Installation

Detailed setup instructions can be found in [`setup/installation-guide.md`](setup/installation-guide.md)

**Quick Start:**

```bash
# Install LocalStack
pip install localstack

# Start LocalStack
localstack start

# Configure AWS CLI (use dummy credentials)
aws configure
# Access Key: test
# Secret Key: test
# Region: us-east-1
# Output: json
```

## 📚 Project Structure

```text
localstack-security-lab/
├── README.md                          # Project documentation
├── setup/                             # Installation and setup guides
│   ├── installation-guide.md
│   └── localstack-setup.md
├── scripts/                           # Automation scripts
│   ├── create-s3-bucket.sh
│   ├── setup-cloudtrail.sh
│   ├── iam-misconfigurations.sh
│   └── security-tests.sh
├── configurations/                    # Configuration files
│   ├── iam-policies/
│   ├── bucket-policies/
│   └── cloudtrail-config/
├── docs/                             # Additional documentation
│   ├── architecture.md
│   ├── security-scenarios.md
│   └── testing-results.md
└── screenshots/                      # Visual documentation
```

## 🔐 Security Scenarios Covered

### 1. IAM Security Testing

- ✅ Overly permissive IAM policies
- ✅ Privilege escalation scenarios
- ✅ Cross-account access misconfigurations
- ✅ Role assumption testing

### 2. S3 Security

- ✅ Public bucket detection
- ✅ Bucket policy misconfigurations
- ✅ Encryption testing
- ✅ Access logging validation

### 3. Logging & Monitoring

- ✅ CloudTrail implementation
- ✅ Log analysis and threat detection
- ✅ CloudWatch integration
- ✅ Security event correlation

### 4. Configuration Auditing

- ✅ Security group analysis
- ✅ Resource tagging compliance
- ✅ Least privilege validation

## 📊 Key Skills Demonstrated

- **Cloud Security**: AWS security best practices and common vulnerabilities
- **Infrastructure as Code**: Automating cloud resource deployment
- **Security Testing**: Identifying and exploiting misconfigurations
- **Log Analysis**: Using CloudTrail for security monitoring
- **Scripting**: Bash/Python automation for security tasks
- **Documentation**: Technical writing and project documentation

## 🧪 Testing Examples

```bash
# Create an intentionally misconfigured S3 bucket
aws --endpoint-url=http://localhost:4566 s3 mb s3://vulnerable-bucket
aws --endpoint-url=http://localhost:4566 s3api put-bucket-acl \
    --bucket vulnerable-bucket --acl public-read

# Enable CloudTrail logging
aws --endpoint-url=http://localhost:4566 cloudtrail create-trail \
    --name security-audit-trail --s3-bucket-name audit-logs

# Test IAM policy for privilege escalation
aws --endpoint-url=http://localhost:4566 iam create-user --user-name test-user
aws --endpoint-url=http://localhost:4566 iam attach-user-policy \
    --user-name test-user --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
```

## 📈 Project Roadmap

- [x] Initial LocalStack setup
- [x] S3 bucket creation and testing
- [x] CloudTrail logging implementation
- [ ] IAM security scenario creation
- [ ] Security misconfiguration testing
- [ ] Automated security scanning scripts
- [ ] Datadog integration for monitoring
- [ ] Comprehensive documentation
- [ ] Video walkthrough/demo

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

### Clayton Demps

- GitHub: [@CMDemps](https://github.com/CMDemps)
- LinkedIn: [in/claytondemps](https://linkedin.com/in/claytondemps)
- Email: clayton.demps@outlook.com

## 🙏 Acknowledgments

- LocalStack team for providing an excellent AWS emulation platform
- AWS documentation for security best practices
- Cloud security community for shared knowledge

---

## 📖 Additional Resources

- [LocalStack Documentation](https://docs.localstack.cloud/)
- [AWS Security Best Practices](https://docs.aws.amazon.com/security/)
- [AWS CLI Command Reference](https://docs.aws.amazon.com/cli/)
