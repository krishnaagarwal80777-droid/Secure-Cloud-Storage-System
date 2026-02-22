Secure Cloud Storage System
Overview

This project is a secure cloud-based file storage system built using AWS EC2, Amazon S3, and Flask. The application allows users to register, log in, upload files securely, and store them in Amazon S3 with backup redundancy.

The system demonstrates secure authentication, IAM role-based access control, and cloud storage best practices.

Architecture

Client (Browser)
→ Flask Application (EC2 Instance)
→ IAM Role (Instance Profile)
→ Amazon S3 Primary Bucket
→ Amazon S3 Backup Bucket

Features

User registration and login

Password hashing using Werkzeug

Session-based authentication

Secure file upload to S3

User-specific folder isolation in S3

Automatic backup to secondary S3 bucket

IAM role-based authentication (no hardcoded AWS credentials)

Clean Bootstrap-based UI

Runs securely on port 80 without root credential conflict

Technologies Used

Python 3

Flask

boto3 (AWS SDK for Python)

Amazon EC2

Amazon S3

IAM Role (Instance Profile)

Bootstrap 5

Security Implementation
1. IAM Role-Based Access

The EC2 instance uses an attached IAM role to access Amazon S3.
No AWS access keys are stored in the application.

boto3 automatically retrieves temporary credentials from the Instance Metadata Service.

2. Password Hashing

User passwords are stored using hashed values via:

werkzeug.security.generate_password_hash
3. Session-Based Authentication

After login, a Flask session is created.
Protected routes such as file upload verify the session before granting access.

4. User-Based File Isolation

Files are stored in S3 using the structure:

username/filename

This ensures logical separation between users.

5. Backup Redundancy

Each uploaded file is:

Uploaded to the primary bucket

Automatically copied to the backup bucket

Bucket Configuration

Primary Bucket: krishna-primary-storage

Backup Bucket: krishna-backup-storage

Versioning enabled (recommended)

Setup Instructions
1. Launch EC2 Instance

Use Amazon Linux 2023

Attach IAM role with S3 access permissions

2. Install Dependencies
sudo dnf install python3 -y
pip3 install flask boto3 werkzeug
3. Allow Port 80

Add inbound rule in Security Group:

Type: HTTP

Port: 80

Source: 0.0.0.0/0

4. Allow Python to Bind to Port 80
sudo setcap 'cap_net_bind_service=+ep' /usr/bin/python3.9
5. Run Application
python3 app.py

Access in browser:

http://PUBLIC-IP
How Authentication Works

User registers.

Password is hashed and stored.

On login, session variable is created.

Upload route checks for active session.

If not authenticated, access is denied.

Key Improvements Made During Development

Removed hardcoded AWS credentials.

Switched to IAM role-based authentication.

Resolved ExpiredToken errors caused by root credentials.

Eliminated sudo-related permission conflicts.

Implemented proper session-based access control.

Added automatic backup bucket replication.

Future Enhancements

Persistent database (RDS or DynamoDB)

HTTPS using SSL/TLS

Role-based access control (Admin/User)

File download feature

Object lifecycle policies

CloudFront integration

Learning Outcomes

Understanding IAM roles and temporary credentials

Debugging AWS ExpiredToken issues

Managing Linux port binding permissions

Implementing session-based authentication

Designing secure cloud-native architecture

Author

Krishna Agarwal
B.E. Electronics Engineering
Cloud Computing Lab Project
