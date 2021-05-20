import json
import unittest

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import MessageModel as Base
from config import API_URL, TOKEN

app = create_app('testing')
db = SQLAlchemy(app)
ma = Marshmallow(app)



class MessageModel(db.Model, Base):
    pass


class BasicTestCase(unittest.TestCase):

    db.create_all()

    messages_to_delete = MessageModel.query.all()
    for m in messages_to_delete:
        db.session.delete(m)
        db.session.commit()

    with open('utils/sample_messages.json', 'r') as f:
        sample_messages = json.load(f)

    for m in sample_messages:
        message = MessageModel(**m)
        db.session.add(message)
        db.session.commit()

    # ::::::::::: INFO VIEW TESTS ::::::::::::::::

    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Messages API', response.data)

    # ::::::::::: LIST VIEW TESTS :::::::::::::::

    def test_list_view(self):
        messages_count = len(MessageModel.query.all())
        tester = app.test_client(self)
        response = tester.get(f'/{API_URL}')
        response_messages_count = len(response.get_json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(messages_count, response_messages_count)

    # ::::::::::: CREATE VIEW TESTS :::::::::::::::

    def test_create_view(self):
        data = {
            'content': 'Created content',
            'password': TOKEN
        }
        tester = app.test_client(self)
        response = tester.post(
            f'/{API_URL}',
            data=json.dumps(data),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Created content', response.data)


    # ::::::::::: UPDATE VIEW TESTS :::::::::::::::

    def test_update_view(self):
        message_to_update = MessageModel.query.first()
        data = {
            'content': 'Updated content',
            'password': TOKEN
        }
        tester = app.test_client(self)
        response = tester.patch(
            f'/{API_URL}/{message_to_update.id}',
            data=json.dumps(data),
            content_type='application/json',
        )
        updated_message = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Updated content' in response.data)
        self.assertTrue(updated_message.get('views') == 1)

    # ::::::::::: DELETE VIEW TESTS :::::::::::::::

    def test_delete_view(self):
        message_to_delete = MessageModel.query.first()
        data = {
            'password': TOKEN
        }
        tester = app.test_client(self)
        response = tester.delete(
            f'/{API_URL}/{message_to_delete.id}',
            data=json.dumps(data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
    unittest.main()
