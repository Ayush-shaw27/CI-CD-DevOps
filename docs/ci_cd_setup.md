# CI/CD Pipeline Setup Guide

## 1. Overview
This pipeline automates:
- Unit testing
- Security scanning (GitLeaks, Checkov, Trivy)
- Artifact upload to AWS S3
- Auto-deployment to EC2 (Medical Records backend)

## 2. Prerequisites
- AWS account with S3 + EC2 access
- IAM user with `AmazonS3FullAccess`, `AmazonEC2FullAccess`
- GitHub Secrets:
  - AWS_ACCESS_KEY_ID
  - AWS_SECRET_ACCESS_KEY
  - AWS_REGION
  - EC2_IP

## 3. Trigger
The workflow runs on every push or pull request to the `main` branch.

## 4. Outputs
- Reports in `reports/` directory
- Uploaded reports in `S3://devsecops-scan-reports`
- Automatic backend restart on EC2
