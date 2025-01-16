from flask import Blueprint, jsonify, render_template, request, session
from datetime import datetime
from .models import Clients, Conversation, Message
from . import db

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

#PROFILE PAGE
@auth.route('/')
def conversation_list():
    user_id = session.get('client_id')
    if not user_id:
        return("Please log in to view your history.", "warning")
    
    # Fetch all conversations for the user
    all_conversations = Conversation.query.filter_by(user_id=user_id).order_by(Conversation.conversation_date.desc()).all()

    # Group conversations
    today = datetime.now().date()
    this_month = today.replace(day=1)
    history = {
        "Today": [],
        "This Month": [],
        "Previous Months": {},
        "Years": {}
    }

    for conversation in all_conversations:
        created_date = conversation.conversation_date

        if created_date == today:
            history["Today"].append(conversation)
        elif created_date >= this_month:
            history["This Month"].append(conversation)
        elif created_date.year == today.year:
            month_name = created_date.strftime("%B")
            if month_name not in history["Previous Months"]:
                history["Previous Months"][month_name] = []
            history["Previous Months"][month_name].append(conversation)
        else:
            year = created_date.year
            if year not in history["Years"]:
                history["Years"][year] = []
            history["Years"][year].append(conversation)

    return render_template('index.html', history=history)

@auth.route('/conversations/<int:conversation_id>')
def conversation_detail(conversation_id):
    # Ensure the user is logged in
    user_id = session.get('client_id')
    if not user_id:
        return "Please log in to view your conversations.", 403

    # Fetch the conversation and its messages
    conversation = Conversation.query.filter_by(id=conversation_id, user_id=user_id).first_or_404()
    messages = Message.query.filter_by(conversation_id=conversation.id).order_by(Message.timestamp.asc()).all()

    return render_template('conversation_detail.html', conversation=conversation, messages=messages)

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

    session['client_id'] = client.id
    print(session.get('client_id'))

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