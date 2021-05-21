from app import db

class MessageModel(db.Model):
    __tablename__ = "message_model"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(160))
    views = db.Column(db.Integer, default=1)

