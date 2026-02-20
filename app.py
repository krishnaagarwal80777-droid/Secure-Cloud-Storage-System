from flask import Flask, request, redirect, url_for, render_template_string, session
import boto3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change in production

# S3 Client (Uses IAM Role on EC2)
s3 = boto3.client('s3')

PRIMARY_BUCKET = "krishna-primary-storage"
BACKUP_BUCKET = "krishna-backup-storage"

# Temporary in-memory user storage (for demo)
users = {}

# ================= HOME PAGE =================

@app.route("/")
def home():
    return render_template_string("""
    <h1>🔐 Secure Cloud Storage System</h1>

    <h2>Register</h2>
    <form method="post" action="/register">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Register">
    </form>

    <h2>Login</h2>
    <form method="post" action="/login">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>

    <h2>Upload File</h2>
    <form method="post" action="/upload" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>

    <h2>List Files</h2>
    <a href="/files">View Files</a>
    """)

# ================= REGISTER =================

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]

    if username in users:
        return "User already exists!"

    users[username] = password
    return "Registered Successfully! <a href='/'>Go Back</a>"

# ================= LOGIN =================

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if username in users and users[username] == password:
        session["user"] = username
        return "Login Successful! <a href='/'>Go Back</a>"

    return "Invalid Credentials! <a href='/'>Go Back</a>"

# ================= UPLOAD =================

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file part"

    file = request.files["file"]

    if file.filename == "":
        return "No selected file"

    filename = secure_filename(file.filename)

    try:
        # Upload to Primary Bucket
        s3.upload_fileobj(file, PRIMARY_BUCKET, filename)

        # Reset file pointer before backup upload
        file.seek(0)

        # Upload to Backup Bucket
        s3.upload_fileobj(file, BACKUP_BUCKET, filename)

        return "<h2>File Uploaded & Backed Up Successfully</h2><a href='/'>Go Back</a>"

    except Exception as e:
        return f"Upload Failed: {str(e)}"

# ================= LIST FILES =================

@app.route("/files")
def list_files():
    try:
        response = s3.list_objects_v2(Bucket=PRIMARY_BUCKET)

        if "Contents" not in response:
            return "No files found."

        file_list = "<h2>Files in Primary Bucket:</h2><ul>"

        for obj in response["Contents"]:
            file_list += f"<li>{obj['Key']}</li>"

        file_list += "</ul><a href='/'>Go Back</a>"

        return file_list

    except Exception as e:
        return f"Error listing files: {str(e)}"

# ================= RUN APP =================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)