from app import db, ma


class MessageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(160))
    views = db.Column(db.Integer, default=1)


class MessageModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MessageModel
        fields = ['id', 'content', 'views']


message_schema = MessageModelSchema()
messages_schema = MessageModelSchema(many=True)