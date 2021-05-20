import json
import unittest
from app import create_app

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


from models import MessageModel


class BasicTestCase(unittest.TestCase):

    app = create_app('testing')
    db = SQLAlchemy(app)
    ma = Marshmallow(app)

    db.init_app(app)
    db.init_app(app)
    db.create_all()

# it is needed to create test database manually - write script


    with open('utils/sample_messages.json', 'r') as f:
        messages = json.load(f)

    for m in messages:
        message = MessageModel(**m)
        db.session.add(message)
        db.session.commit()

    def test_home(self):
            tester = self.app.test_client(self)
            response = tester.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Messages API', response.data)
    #
    def test_list_view(self):
            tester = self.app.test_client(self)
            response = tester.get('/api/v1/messages')
            self.assertEqual(response.status_code, 200)
            # self.assertIn(response.data, 'Russia’s Foreign Intelligence Service (SVR)')

    # def test_other(self):
    #         tester = self.app.test_client(self)
    #         response = tester.get('a', content_type='html/text')
    #         self.assertEqual(response.status_code, 404)
    #         self.assertTrue(b'does not exist' in response.data)

if __name__ == '__main__':
    unittest.main()