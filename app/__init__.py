from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_httpauth import HTTPBasicAuth
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the app, database, API, and authentication
db = SQLAlchemy()
auth = HTTPBasicAuth()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    db.init_app(app)

    api = Api(app)

    # Import and add resources
    from app.resources import FarmerResource, WarehouseResource, CommodityResource, FarmerWarehouseCommodityResource
    api.add_resource(FarmerResource, '/farmer')
    api.add_resource(WarehouseResource, '/warehouse')
    api.add_resource(CommodityResource, '/commodity')
    api.add_resource(FarmerWarehouseCommodityResource, '/farmer_warehouse_commodity')

    return app
