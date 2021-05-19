import unittest

import json
from app import create_app, db


class MessagesTestCase(unittest.TestCase):
    """This class represents the messages test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.content = {'content': 'This is testing content'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_messages_creation(self):
        """Test API can create a message (POST request)"""
        res = self.client().post('/messages/', data=self.content)
        self.assertEqual(res.status_code, 201)
        self.assertIn('This is testing content', str(res.data))

    def test_api_can_get_all_messages(self):
        """Test API can get a messages (GET request)."""
        res = self.client().post('/messages/', data=self.content)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/messages/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('This is testing content', str(res.data))

    def test_api_can_get_message_by_id(self):
        """Test API can get a single message by using it's id."""
        rv = self.client().post('/messages/', data=self.content)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/bucketlists/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go to Borabora', str(result.data))

    def test_bucketlist_can_be_edited(self):
        """Test API can edit an existing bucketlist. (PUT request)"""
        rv = self.client().post(
            '/bucketlists/',
            data={'name': 'Eat, pray and love'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/bucketlists/1',
            data={
                "name": "Dont just eat, but also pray and love :-)"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/bucketlists/1')
        self.assertIn('Dont just eat', str(results.data))

    def test_bucketlist_deletion(self):
        """Test API can delete an existing bucketlist. (DELETE request)."""
        rv = self.client().post(
            '/bucketlists/',
            data={'name': 'Eat, pray and love'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/bucketlists/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/bucketlists/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()