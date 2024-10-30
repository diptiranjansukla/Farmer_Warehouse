import unittest
from app.factory import create_app, db
from app.models import Farmer, Warehouse, Commodity, FarmerWarehouseCommodity
from base64 import b64encode

class FarmerWarehouseCommodityTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Set up the test app and database before all tests """
        cls.app = create_app()
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Sukla%40123@localhost/farmer_warehouse_db'
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()  # Create all tables

            # Adding initial data for Farmer, Warehouse, and Commodity to use in tests
            farmer = Farmer(id=71, name='John Smith3', contact='1234567899', country='Country X1', state='State Y1', district='District Z1', village='Village Q1')
            warehouse = Warehouse(id=200, name='Warehouse A', country='Country X', state='State Y', district='District Z', village='Village Q', capacity=5000)
            commodity = Commodity(id=300, commodity_name='Corn', quantity=100)

            db.session.add_all([farmer, warehouse, commodity])
            db.session.commit()

    # Helper function to generate basic authentication headers
    def get_auth_headers(self, username, password):
        credentials = f"{username}:{password}"
        auth_header = {
            "Authorization": "Basic " + b64encode(credentials.encode()).decode("utf-8")
        }
        return auth_header

    def test_farmer_warehouse_commodity_creation(self):
        """ Test the creation of a new Farmer-Warehouse-Commodity relationship """
        auth_headers = self.get_auth_headers("admin", "password123")

        response = self.client.post('/farmer_warehouse_commodity', json={
            'id': 1001,
            'farmer_id': 71,
            'warehouse_id': 200,
            'commodity_id': 300,
            'farmer_warehouse_commodity_receipt': 'R-10001'
        }, headers=auth_headers)
        
        print(response.json)

        self.assertEqual(response.status_code, 201)
        self.assertIn('Farmer-Warehouse-Commodity record created successfully', response.json['message'])

    def test_farmer_warehouse_commodity_creation_duplicate_id(self):
        """ Test that creating a Farmer-Warehouse-Commodity record with a duplicate ID fails """
        auth_headers = self.get_auth_headers("admin", "password123")

        # First request to create a Farmer-Warehouse-Commodity record
        self.client.post('/farmer_warehouse_commodity', json={
            'id': 1002,
            'farmer_id': 71,
            'warehouse_id': 200,
            'commodity_id': 300,
            'farmer_warehouse_commodity_receipt': 'R-10002'
        }, headers=auth_headers)

        # Second request with the same ID (should fail)
        response = self.client.post('/farmer_warehouse_commodity', json={
            'id': 1002,  # Duplicate ID
            'farmer_id': 71,
            'warehouse_id': 200,
            'commodity_id': 300,
            'farmer_warehouse_commodity_receipt': 'R-10003'
        }, headers=auth_headers)

        self.assertEqual(response.status_code, 400)
        self.assertIn('Record with this ID already exists', response.json['message'])


if __name__ == '__main__':
    unittest.main()
