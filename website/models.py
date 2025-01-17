from . import db
from datetime import datetime
from flask_login import UserMixin

class Clients(db.Model, UserMixin ):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)  
    conversation_date = db.Column(db.Date, default=datetime.utcnow)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  
    messages = db.relationship('Message', backref='conversation', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    sender = db.Column(db.String(255), nullable=False)  
    message_content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)