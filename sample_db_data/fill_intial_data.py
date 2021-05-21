import json

from app import db
from messages.models import MessageModel

db.create_all()

messages_to_delete = MessageModel.query.all()
for m in messages_to_delete:
    db.session.delete(m)
    db.session.commit()

with open('sample_messages.json', 'r') as f:
    sample_messages = json.load(f)

for m in sample_messages:
    message = MessageModel(**m)
    db.session.add(message)
    db.session.commit()
