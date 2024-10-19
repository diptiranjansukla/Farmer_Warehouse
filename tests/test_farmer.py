import unittest
from app.factory import create_app, db
from app.models import Farmer
from base64 import b64encode

class FarmerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Set up the test app and database before all tests """
        cls.app = create_app()

        # Use SQLite in-memory database for testing instead of MySQL
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

    def test_farmer_creation(self):
        """ Test the creation of a new farmer """
        # Ensure that the username and password match those defined in the Flask app
        auth_headers = self.get_auth_headers("admin", "password123")  # Adjust if necessary

        response = self.client.post('/farmer', json={
            'id': 256,
            'name': 'ramesh das',
            'contact': '1234567880',
            'country': 'Country A',
            'state': 'State A',
            'district': 'District A',
            'village': 'Village A'
        }, headers=auth_headers)  # Pass auth headers with the request
        print(response.json)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Farmer created successfully', response.json['message'])

    def test_farmer_creation_duplicate_id(self):
        """ Test that creating a farmer with duplicate ID fails """
        auth_headers = self.get_auth_headers("admin", "password123")  # Ensure credentials are correct

        # First request to create a farmer
        response = self.client.post('/farmer', json={
            'id': 342,
            'name': 'asu sahoo',
            'contact': '9987654321',
            'country': 'Country B',
            'state': 'State B',
            'district': 'District B',
            'village': 'Village B',
        }, headers=auth_headers)

        print(response.json)  # Debug: Print the response to see the result of the first request

        # Second request to create another farmer with the same ID (this should fail)
        response = self.client.post('/farmer', json={
            'id': 342,
            'name': 'Another Farmer2',
            'contact': '1122334455',
            'country': 'Country C',
            'state': 'State C',
            'district': 'District C',
            'village': 'Village C',
        }, headers=auth_headers)

        print(response.json)  # Debug: Print the response to see the result of the second request
        
        # Expect a 400 status code for duplicate entry
        self.assertEqual(response.status_code, 400)
        
        # Update to match the actual message returned by the API
        self.assertIn('Farmer with this ID already exists', response.json['message'])

if __name__ == '__main__':
    unittest.main()
