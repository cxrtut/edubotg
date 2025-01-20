import sys
import os

# Add the root directory (SMARTSPHERE) to the sys.path so Python can find the 'app' package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from website import create_app, db  # Now Python can find the 'app' module
from website.models import Conversation, Message  # Import your models
from datetime import datetime, timedelta

# Create the app context
app = create_app()  # Create app using the factory function

with app.app_context():  # Ensure we're within the Flask app context
    # Helper function to add messages with real content
    def add_messages(conversation_id, sender, message_count=6):
        message_texts = [
            "Hey, how's it going?",
            "I'm doing well, thanks for asking! How about you?",
            "I'm good too, just been really busy with work lately.",
            "Same here, work has been exhausting, but it's been productive.",
            "That's great to hear! Are you doing anything fun this weekend?",
            "Not sure yet, maybe catch up on some rest. You?",
        ]
        
        messages = [
            Message(conversation_id=conversation_id, sender=sender, message_content=message_texts[i], timestamp=datetime.utcnow() + timedelta(minutes=i))
            for i in range(message_count)
        ]
        db.session.add_all(messages)
        db.session.commit()

    def add_conversations():
        today = datetime.utcnow().date()
        for i in range(2):
            conversation = Conversation(user_id=1, title=f"Conversation {i+1}", conversation_date=today, created_at=datetime.utcnow())
            db.session.add(conversation)
            db.session.commit()
            add_messages(conversation.id, "User 1")

        date_1201 = datetime(2025, 1, 12).date()
        for i in range(2):
            conversation = Conversation(user_id=1, title=f"Conversation {i+3}", conversation_date=date_1201, created_at=datetime.utcnow())
            db.session.add(conversation)
            db.session.commit()
            add_messages(conversation.id, "User 1")

        date_1212 = datetime(2024, 12, 12).date()
        for i in range(2):
            conversation = Conversation(user_id=1, title=f"Conversation {i+5}", conversation_date=date_1212, created_at=datetime.utcnow())
            db.session.add(conversation)
            db.session.commit()
            add_messages(conversation.id, "User 1")

        db.session.commit()

    add_conversations()
    print("Data has been populated!")
