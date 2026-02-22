# Secure Cloud Storage System

A cloud-based secure file storage application built using Flask, AWS
EC2, and Amazon S3.\
The system implements IAM role-based authentication, session-based user
authentication, and automatic backup replication.

------------------------------------------------------------------------

## Project Overview

-   Users can register and log in
-   Authenticated users can upload files
-   Files are stored securely in Amazon S3
-   Each upload is automatically backed up
-   No AWS credentials are hardcoded
-   IAM role-based authentication is used

------------------------------------------------------------------------

## Architecture

Client (Browser)\
→ Flask Application (EC2 Instance)\
→ IAM Role (Instance Profile)\
→ Amazon S3 Primary Bucket\
→ Amazon S3 Backup Bucket

------------------------------------------------------------------------

## Key Features

-   User registration and login
-   Password hashing using Werkzeug
-   Session-based authentication
-   Secure file upload to Amazon S3
-   User-specific folder isolation (username/filename)
-   Automatic backup to secondary bucket
-   IAM role-based secure access (no stored credentials)
-   Clean Bootstrap UI

------------------------------------------------------------------------

## Security Design

### IAM Role-Based Authentication

-   EC2 instance has an attached IAM role
-   boto3 retrieves temporary credentials automatically
-   No AWS access keys stored in code or configuration

### Session-Based Access Control

-   User session created after successful login
-   Protected routes verify session before allowing access
-   Unauthorized uploads are blocked

### Password Protection

-   Passwords are hashed using:
    -   generate_password_hash
    -   check_password_hash

### Data Isolation

-   Each user's files stored under: username/filename

### Backup Strategy

-   File uploaded to primary bucket
-   Automatically copied to backup bucket

------------------------------------------------------------------------

## Technologies Used

-   Python 3
-   Flask
-   boto3
-   Amazon EC2
-   Amazon S3
-   IAM Role (Instance Profile)
-   Bootstrap 5

------------------------------------------------------------------------

## Setup Instructions

1.  Launch EC2 Instance

    -   Amazon Linux 2023
    -   Attach IAM role with S3 permissions

2.  Install dependencies

    sudo dnf install python3 -y\
    pip3 install flask boto3 werkzeug

3.  Configure Security Group

    -   Allow HTTP (Port 80)
    -   Source: 0.0.0.0/0

4.  Allow Python to bind to Port 80 (without sudo)

    sudo setcap 'cap_net_bind_service=+ep' /usr/bin/python3.9

5.  Run application

    python3 app.py

Access the app via:

http://PUBLIC-IP

------------------------------------------------------------------------

## Problems Solved During Development

-   Removed expired temporary AWS credentials
-   Eliminated root credential conflicts caused by sudo
-   Implemented IAM role-based authentication
-   Secured upload route using session validation
-   Added automatic S3 backup replication

------------------------------------------------------------------------

## Learning Outcomes

-   Understanding IAM roles and temporary credentials
-   Debugging AWS ExpiredToken errors
-   Managing privileged ports securely in Linux
-   Implementing secure session-based authentication
-   Designing scalable cloud storage architecture

------------------------------------------------------------------------

## Author

Krishna Agarwal\
B.E. Electronics Engineering\
Cloud Computing Lab Project
