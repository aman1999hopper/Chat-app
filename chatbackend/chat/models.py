from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class ChatMessage(Document):
    username = StringField(required=True)
    message = StringField(required=True)
    timestamp = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'chat_messages'  # optional name for MongoDB collection
    }
