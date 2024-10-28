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

            # # Adding initial data for Farmer, Warehouse, and Commodity to use in tests
            # farmer = Farmer(id=1, name='Test Farmer', contact='1234567890', country='Country A', state='State A', district='District A', village='Village A')
            # warehouse = Warehouse(id=1, name='Test Warehouse', country='Country A', state='State A', district='District A', village='Village A', capacity=1000)
            # commodity = Commodity(id=1, commodity_name='Test Commodity', quantity=100)

            # db.session.add(farmer)
            # db.session.add(warehouse)
            # db.session.add(commodity)
            # db.session.commit()

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
            'id': 6,
            'farmer_id': 1,
            'warehouse_id': 101,
            'commodity_id': 101,
            'farmer_warehouse_commodity_receipt': 'R-0001'
        }, headers=auth_headers)

        self.assertEqual(response.status_code, 201)
        self.assertIn('Farmer-Warehouse-Commodity record created successfully', response.json['message'])

    def test_farmer_warehouse_commodity_creation_duplicate_id(self):
        """ Test that creating a Farmer-Warehouse-Commodity record with a duplicate ID fails """
        auth_headers = self.get_auth_headers("admin", "password123")

        # First request to create a Farmer-Warehouse-Commodity record
        self.client.post('/farmer_warehouse_commodity', json={
            'id': 7,
            'farmer_id': 10,
            'warehouse_id': 102,
            'commodity_id': 102,
            'farmer_warehouse_commodity_receipt': 'R-0002'
        }, headers=auth_headers)

        # Second request with the same ID (should fail)
        response = self.client.post('/farmer_warehouse_commodity', json={
            'id': 7,
            'farmer_id': 7,
            'warehouse_id': 105,
            'commodity_id': 107,
            'farmer_warehouse_commodity_receipt': 'R-0003'
        }, headers=auth_headers)

        self.assertEqual(response.status_code, 400)
        self.assertIn('Record with this ID already exists', response.json['message'])

    # def test_farmer_warehouse_commodity_creation_invalid_receipt(self):
    #     """ Test that creating a Farmer-Warehouse-Commodity record with an invalid receipt fails """
    #     auth_headers = self.get_auth_headers("admin", "password123")
    #     # Attempt to create a record with an invalid receipt
    #     response = self.client.post('/farmer_warehouse_commodity', json={
    #         'id': 3,
    #         'farmer_id': 1,
    #         'warehouse_id': 1,
    #         'commodity_id': 1,
    #         'farmer_warehouse_commodity_receipt': 'InvalidReceipt'
    #     }, headers=auth_headers)

    #     self.assertEqual(response.status_code, 400)
    #     self.assertIn('Receipt must start with \'R-\' followed by at least 4 digits.', response.json['message'])

if __name__ == '__main__':
    unittest.main()
