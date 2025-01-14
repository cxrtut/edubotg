from flask import Blueprint, render_template, request, jsonify
from .models import Clients
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

auth = Blueprint('auth', __name__)

# SIGN IN SIDE
@auth.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@auth.route('/validate_email', methods=['POST'])
def validate_email():
    data = request.json
    email = data.get('email')

    # Check if email exists in the database
    client = Clients.query.filter_by(email=email).first()
    if not client:  
        return jsonify({"status": "error", "message": "Email does not exist"}), 400

    return jsonify({"status": "ok", "message": "Email is valid"}), 200

@auth.route('/validate_password', methods=['POST'])
def validate_password():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Check if the email exists in the database
    client = Clients.query.filter_by(email=email).first()
    if not client:
        return jsonify({"message": "Email not found."}), 400

    # Check if the password matches the stored password
    if password != client.password:  
        return jsonify({"message": "Invalid password."}), 400

    return jsonify({"message": "Password is correct."}), 200

#SIGN UP SIDE
@auth.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@auth.route('/check_email_not_exists', methods=['POST'])
def check_email_not_exists():
    data = request.get_json()
    email = data.get('email')
    
    # Check if the email exists in the database
    existing_user = Clients.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "Email already exists."}), 400

    return jsonify({"message": "Email is available."}), 200

@auth.route('/store_user', methods=['POST'])
def store_user():
    data = request.json
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    # Validate the password length
    if len(password) < 8:
        return jsonify({"status": "error", "message": "Password must be at least 8 characters long"}), 400

    # Check if the email already exists
    if Clients.query.filter_by(email=email).first():
        return jsonify({"status": "error", "message": "Email already exists"}), 400

    # Store the user in the database
    new_user = Clients(email=email, username=username, password=password)
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"status": "ok", "message": "User registered successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////




@main.route('/practise')
def practise():
    return render_template('practise.html')