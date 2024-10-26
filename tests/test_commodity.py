import unittest
from app.factory import create_app, db
from app.models import Commodity
from base64 import b64encode

class CommodityTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Set up the test app and database before all tests """
        cls.app = create_app()
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Sukla%40123@localhost/farmer_warehouse_db'
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()  # Create all tables

    # Helper function to generate basic authentication headers
    def get_auth_headers(self, username, password):
        credentials = f"{username}:{password}"
        auth_header = {
            "Authorization": "Basic " + b64encode(credentials.encode()).decode("utf-8")
        }
        return auth_header

    def test_commodity_creation(self):
        """ Test the creation of a new commodity """
        auth_headers = self.get_auth_headers("admin", "password123")

        response = self.client.post('/commodity', json={
            'id': 107,
            'commodity_name': 'Wheat2',
            'quantity': 500
        }, headers=auth_headers)

        self.assertEqual(response.status_code, 201)
        self.assertIn('Commodity created successfully', response.json['message'])

    def test_commodity_creation_duplicate_id(self):
        """ Test that creating a commodity with duplicate ID fails """
        auth_headers = self.get_auth_headers("admin", "password123")

        # First request to create a commodity
        self.client.post('/commodity', json={
            'id': 108,
            'commodity_name': 'Rice2',
            'quantity': 300
        }, headers=auth_headers)

        # Second request to create another commodity with the same ID
        response = self.client.post('/commodity', json={
            'id': 108,
            'commodity_name': 'Corn2',
            'quantity': 200
        }, headers=auth_headers)

        self.assertEqual(response.status_code, 400)
        self.assertIn('Commodity with this ID already exists', response.json['message'])

    
if __name__ == '__main__':
    unittest.main()
