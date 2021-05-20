import os
import json

from app import db
from models import MessageModel

# Create new database file (remove old)
if os.path.exists("db.sqlite"):
    os.remove("db.sqlite")

db.create_all()


# Import initial data
with open('sample_messages.json', 'r') as f:
    messages = json.load(f)

for m in messages:
    message = MessageModel(**m)
    db.session.add(message)
    db.session.commit()
