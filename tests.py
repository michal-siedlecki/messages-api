import json
import unittest

from app import app
from models import MessageModel
from config import API_URL, TOKEN


class BasicTestCase(unittest.TestCase):


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

    # ::::::::::: DETAIL VIEW TESTS :::::::::::::::

    def test_detail_view(self):
        message = MessageModel.query.first()
        tester = app.test_client(self)
        response = tester.get(f'/{API_URL}/{message.id}')
        message_in_response = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(message_in_response.get('id'), message.id)
        self.assertEqual(message_in_response.get('content'), message.content)
        self.assertEqual(message_in_response.get('views'), message.views)


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

    def test_unauthorized_create(self):
        data = {
            'content': 'Created content',
            'password': ''
        }
        tester = app.test_client(self)
        response = tester.post(
            f'/{API_URL}',
            data=json.dumps(data),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 403)
        self.assertIn(b'Unauthorized', response.data)

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
        self.assertTrue(updated_message.get('views') == 1) # Get request after update adds view.

    def test_unauthorized_update_view(self):
        message_to_update = MessageModel.query.first()
        data = {
            'content': 'Updated content',
            'password': ''
        }
        tester = app.test_client(self)
        response = tester.patch(
            f'/{API_URL}/{message_to_update.id}',
            data=json.dumps(data),
            content_type='application/json',
        )
        updated_message = response.get_json()
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(updated_message, message_to_update)
        self.assertTrue(b'Unauthorized' in response.data)

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

    def test_unauthorized_delete_view(self):
        message_to_delete = MessageModel.query.first()
        messages_count_before = len(MessageModel.query.all())
        data = {
            'password': ''
        }
        tester = app.test_client(self)
        response = tester.delete(
            f'/{API_URL}/{message_to_delete.id}',
            data=json.dumps(data),
            content_type='application/json',
        )

        messages_count_after = len(MessageModel.query.all())
        self.assertEqual(response.status_code, 403)
        self.assertEqual(messages_count_before, messages_count_after)
        self.assertTrue(b'Unauthorized' in response.data)


if __name__ == '__main__':
    unittest.main()
