from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the app and extensions
db = SQLAlchemy()
auth = HTTPBasicAuth()

# Define users and their hashed passwords
users = {
    "admin": generate_password_hash("password123"),  # Make sure this matches your test credentials
}

# Verify the username and password
@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    return None

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Sukla%40123@localhost/farmer_warehouse_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    db.init_app(app)

    # Initialize the API
    api = Api(app)

    # Import and register resources (ensure these routes require authentication)
    from app.resources import FarmerResource, WarehouseResource, CommodityResource, FarmerWarehouseCommodityResource
    api.add_resource(FarmerResource, '/farmer')
    api.add_resource(WarehouseResource, '/warehouse')
    api.add_resource(CommodityResource, '/commodity')
    api.add_resource(FarmerWarehouseCommodityResource, '/farmer_warehouse_commodity')

    return app
