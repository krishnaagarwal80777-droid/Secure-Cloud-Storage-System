# Secure Cloud Storage System

## Overview

This project implements a secure cloud-based file storage system using Amazon Web Services (AWS). The application is deployed on an EC2 instance and integrates Amazon S3 for scalable object storage. 

The system allows users to register, log in, upload files, and store them in a primary S3 bucket with versioning enabled. Every uploaded file is also automatically backed up to a secondary S3 bucket to ensure redundancy and fault tolerance.

---

## Features

- User Registration and Login
- File Upload via Web Interface
- Storage in Amazon S3
- S3 Bucket Versioning Enabled
- Automatic Backup to Secondary Bucket
- Public Deployment on EC2 (Port 80)

---

## Architecture

User → Flask Web Application (EC2) → Primary S3 Bucket (Versioning Enabled)  
                                             ↓  
                                     Backup S3 Bucket  

---

## Technologies Used

- Python (Flask)
- AWS EC2 (Infrastructure as a Service)
- Amazon S3 (Object Storage)
- Boto3 (AWS SDK for Python)

---

## How It Works

1. The Flask application runs on an EC2 instance.
2. Users interact with the system through a web interface.
3. When a file is uploaded:
   - It is stored in the Primary S3 bucket.
   - Versioning automatically maintains file history.
   - A backup copy is stored in the Secondary S3 bucket.
4. Files can be listed from the primary bucket.

---

## Deployment Details

- Hosted on Amazon EC2 (Amazon Linux)
- Security Group configured to allow:
  - SSH (Port 22)
  - HTTP (Port 80)
- S3 Versioning enabled on Primary bucket
- Manual backup logic implemented using Boto3

---

## Setup Instructions
1. Launch an EC2 instance.
2. Attach an IAM role with S3 access permissions.
3. Install Python and required dependencies:
 4. Update bucket names inside `app.py`.
5. Run the application:
6.  Access via:  
---

## Security Notes

- AWS credentials are not hardcoded.
- The application uses IAM role-based authentication for S3 access.
- Sensitive files such as `.aws/credentials` and `.pem` keys are excluded via `.gitignore`.

---

## Author

Krishna Agarwal
1. Launch an EC2 instance.
2. Attach an IAM role with S3 access permissions.
3. Install Python and required dependencies:
