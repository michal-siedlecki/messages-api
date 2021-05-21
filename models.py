from app import db


class MessageModel(db.Model):
    __tablename__ = "message_model"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(160))
    views = db.Column(db.Integer, default=1)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'content': self.content,
            'views': self.views
        }
