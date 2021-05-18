from config import db, ma


class MessageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(160))
    views = db.Column(db.Integer, default=1)

    def add_view(self):
        self.views += 1
        db.commit()

    def reset_views(self):
        self.views = 0
        db.commit()


class MessageModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MessageModel
        fields = ['id', 'content', 'views']


message_schema = MessageModelSchema()
messages_schema = MessageModelSchema(many=True)