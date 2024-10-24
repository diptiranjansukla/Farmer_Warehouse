import unittest
from app.factory import create_app, db
from app.models import Warehouse
from base64 import b64encode

class WarehouseTest(unittest.TestCase):

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

    def test_warehouse_creation(self):
        """ Test the creation of a new warehouse """
        auth_headers = self.get_auth_headers("admin", "password123")  # Adjust if necessary

        response = self.client.post('/warehouse', json={
            'id': 111,
            'name': 'Warehouse AA1',
            'country': 'Country A',
            'state': 'State A',
            'district': 'District A',
            'village': 'Village A',
            'capacity': 500
        }, headers=auth_headers)  # Pass auth headers with the request
        self.assertEqual(response.status_code, 201)
        self.assertIn('Warehouse created successfully', response.json['message'])

    def test_warehouse_creation_duplicate_id(self):
        """ Test that creating a warehouse with duplicate ID fails """
        auth_headers = self.get_auth_headers("admin", "password123")  # Ensure credentials are correct

        # First request to create a warehouse
        self.client.post('/warehouse', json={
            'id': 113,
            'name': 'Warehouse BB1',
            'country': 'Country B',
            'state': 'State B',
            'district': 'District B',
            'village': 'Village B',
            'capacity': 1000
        }, headers=auth_headers)

        # Second request to create another warehouse with the same ID (this should fail)
        response = self.client.post('/warehouse', json={
            'id': 113,
            'name': 'Warehouse CC1',
            'country': 'Country C',
            'state': 'State C',
            'district': 'District C',
            'village': 'Village C',
            'capacity': 800
        }, headers=auth_headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Warehouse with this ID already exists', response.json['message'])

if __name__ == '__main__':
    unittest.main()
