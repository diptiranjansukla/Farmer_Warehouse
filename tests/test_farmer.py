import unittest
from app import create_app, db
from app.models import Farmer

class FarmerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Set up the test app and database before all tests """
        cls.app = create_app()
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB for testing
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()  # Create all tables

    @classmethod
    def tearDownClass(cls):
        """ Clean up the database after all tests """
        with cls.app.app_context():
            db.drop_all()

    def test_farmer_creation(self):
        """ Test the creation of a new farmer """
        response = self.client.post('/farmer', json={
            'id': 1,
            'name': 'John Doe',
            'contact': '1234567890',
            'country': 'Country A',
            'state': 'State A',
            'district': 'District A',
            'village': 'Village A'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Farmer created successfully', response.json['message'])

    def test_farmer_creation_duplicate_id(self):
        """ Test that creating a farmer with duplicate ID fails """
        self.client.post('/farmer', json={
            'id': 2,
            'name': 'Jane Doe',
            'contact': '0987654321',
            'country': 'Country B',
            'state': 'State B',
            'district': 'District B',
            'village': 'Village B'
        })

        response = self.client.post('/farmer', json={
            'id': 2,
            'name': 'Another Farmer',
            'contact': '1122334455',
            'country': 'Country C',
            'state': 'State C',
            'district': 'District C',
            'village': 'Village C'
        })
        self.assertEqual(response.status_code, 500)
        self.assertIn('Database error', response.json['message'])

if __name__ == '__main__':
    unittest.main()
