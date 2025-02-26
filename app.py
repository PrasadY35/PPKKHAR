from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
import smtplib
import random
import os

app = Flask(__name__, static_folder='')

users = {}  # In-memory storage for user details
otps = {}  # In-memory storage for OTPs
user_counter = 1  # Counter for generating user IDs

# Configure SMTP
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'prasadyammi2@gmail.com'
EMAIL_PASSWORD = 'jgkd udby yfrb dwbv'  # Use your app password

def send_otp(email, otp):
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            message = f'Subject: Your OTP Code\n\nYour OTP code is {otp}'
            server.sendmail(EMAIL_ADDRESS, email, message)
        print(f"OTP sent to {email}: {otp}")  # Debugging statement
    except Exception as e:
        print(f"Error sending OTP to {email}: {str(e)}")  # Debugging statement
        raise

def generate_user_id(name, location):
    global user_counter
    user_id = f"NIR{name[:3].upper()}{location[:3].upper()}{user_counter:03d}"
    user_counter += 1
    return user_id

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/login')
def login():
    return send_from_directory('', 'login.html')

@app.route('/signup')
def signup():
    return send_from_directory('', 'signup.html')

@app.route('/payment')
def payment():
    return send_from_directory('', 'payment.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory('', 'dashboard.html')

@app.route('/admin')
def admin():
    return send_from_directory('', 'admin.html')

@app.route('/send-otp', methods=['POST'])
def send_otp_route():
    data = request.get_json()
    email = data['email']
    otp = str(random.randint(100000, 999999))  # Generate 6-digit OTP

    # Store OTP
    otps[email] = otp

    # Send OTP email
    try:
        print(f"Attempting to send OTP to {email}")  # Debugging statement
        send_otp(email, otp)
        return jsonify({'message': 'OTP sent successfully'}), 200
    except Exception as e:
        print(f"Error sending OTP to {email}: {str(e)}")  # Debugging statement
        return jsonify({'message': 'Error sending OTP', 'error': str(e)}), 500

@app.route('/verify-otp', methods=['POST'])
def verify_otp_route():
    data = request.get_json()
    email = data['email']
    otp = data['otp']

    if otps.get(email) == otp:
        del otps[email]  # Remove OTP after verification
        return jsonify({'message': 'OTP verified successfully'}), 200
    else:
        return jsonify({'message': 'Invalid OTP'}), 400

@app.route('/register', methods=['POST'])
def register_route():
    data = request.get_json()
    email = data['email']
    name = data['name']
    location = data['location']
    password = data['password']

    if email in users:
        return jsonify({'message': 'User already registered'}), 400

    user_id = generate_user_id(name, location)
    users[email] = {
        'user_id': user_id,
        'name': name,
        'location': location,
        'password': password
    }

    print(f"User registered: {users[email]}")  # Debugging statement

    return jsonify({'message': 'User registered successfully', 'userId': user_id}), 200

@app.route('/login', methods=['POST'])
def login_route():
    data = request.get_json()
    user_id = data['userId']
    password = data['password']

    # Check for admin credentials
    if user_id == 'ADMINPRASAD' and password == 'Admipra@2010':
        return jsonify({'message': 'Admin login successful', 'redirect': 'admin.html'}), 200

    for email, user in users.items():
        if user['user_id'] == user_id and user['password'] == password:
            print(f"User logged in: {user}")  # Debugging statement
            return jsonify({'message': 'Login successful'}), 200

    print(f"Invalid login attempt: {user_id}, {password}")  # Debugging statement
    return jsonify({'message': 'Invalid User ID or Password'}), 400

@app.route('/admin-login', methods=['POST'])
def admin_login_route():
    data = request.get_json()
    admin_username = data['username']
    admin_password = data['password']

    print(f"Admin login attempt: {admin_username}, {admin_password}")  # Debugging statement

    # Replace with your actual admin credentials
    if admin_username == 'ADMINPRASAD' and admin_password == 'Admipra@2010':
        print("Admin login successful")  # Debugging statement
        return jsonify({'message': 'Admin login successful'}), 200
    else:
        print("Invalid Admin Credentials")  # Debugging statement
        return jsonify({'message': 'Invalid Admin Credentials'}), 400

@app.route('/get-users', methods=['GET'])
def get_users_route():
    return jsonify(users), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)