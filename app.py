from flask import Flask, request, render_template_string, session, redirect
import boto3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change in real production

# Initialize S3 client (Uses IAM Role automatically)
s3 = boto3.client('s3')

PRIMARY_BUCKET = "krishna-primary-storage"
BACKUP_BUCKET = "krishna-backup-storage"

# In-memory user store (for demo)
users = {}

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Secure Cloud Storage</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="container mt-5">

<h2 class="text-center mb-4">Secure Cloud Storage System</h2>

{% if 'user' not in session %}

<div class="row">
    <div class="col-md-6">
        <h4>Register</h4>
        <form method="POST" action="/register">
            <input class="form-control mb-2" name="username" placeholder="Username" required>
            <input class="form-control mb-2" type="password" name="password" placeholder="Password" required>
            <button class="btn btn-primary w-100">Register</button>
        </form>
    </div>

    <div class="col-md-6">
        <h4>Login</h4>
        <form method="POST" action="/login">
            <input class="form-control mb-2" name="username" placeholder="Username" required>
            <input class="form-control mb-2" type="password" name="password" placeholder="Password" required>
            <button class="btn btn-success w-100">Login</button>
        </form>
    </div>
</div>

{% else %}

<p>Welcome, <b>{{ session['user'] }}</b> |
<a href="/logout">Logout</a></p>

<h4>Upload File</h4>
<form method="POST" action="/upload" enctype="multipart/form-data">
    <input class="form-control mb-2" type="file" name="file" required>
    <button class="btn btn-dark w-100">Upload</button>
</form>

<h4 class="mt-4">List Files</h4>
<a href="/files" class="btn btn-outline-primary">View Files</a>

{% endif %}

<p class="text-danger mt-3">{{ message }}</p>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML, message="")

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    if username in users:
        return render_template_string(HTML, message="User already exists!")

    users[username] = generate_password_hash(password)
    return render_template_string(HTML, message="Registration successful!")

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and check_password_hash(users[username], password):
        session['user'] = username
        return redirect('/')

    return render_template_string(HTML, message="Invalid credentials!")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/upload', methods=['POST'])
def upload():
    if 'user' not in session:
        return redirect('/')

    file = request.files['file']

    if file:
        filename = session['user'] + "/" + file.filename

        # Upload to primary bucket
        s3.put_object(Bucket=PRIMARY_BUCKET, Key=filename, Body=file)

        # Backup copy
        s3.copy_object(
            Bucket=BACKUP_BUCKET,
            CopySource={'Bucket': PRIMARY_BUCKET, 'Key': filename},
            Key=filename
        )

        return render_template_string(HTML, message="File uploaded & backed up successfully!")

    return render_template_string(HTML, message="No file selected!")

@app.route('/files')
def list_files():
    if 'user' not in session:
        return redirect('/')

    response = s3.list_objects_v2(Bucket=PRIMARY_BUCKET, Prefix=session['user'] + "/")
    files = []

    if 'Contents' in response:
        for obj in response['Contents']:
            files.append(obj['Key'])

    return "<br>".join(files) if files else "No files found."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)