from app.factory import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask, jsonify, request
# from flask_restful import Api, Resource, reqparse
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.exc import SQLAlchemyError
# from datetime import datetime, timezone
# from flask_httpauth import HTTPBasicAuth
# from werkzeug.security import generate_password_hash, check_password_hash
# import re

# app = Flask(__name__)
# api = Api(app)
# auth = HTTPBasicAuth()

# users = {
#     "admin": generate_password_hash("password123"),
# }

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Sukla%40123@localhost/farmer_warehouse_db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
#     'pool_size': 10,              
#     'max_overflow': 20,           
#     'pool_timeout': 30,           
#     'pool_recycle': 1800,         
# }

# db = SQLAlchemy(app)

# class Farmer(db.Model):
#     __tablename__ = 'farmer'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     contact = db.Column(db.String(50), nullable=False)
#     country = db.Column(db.String(100), nullable=False)
#     state = db.Column(db.String(100), nullable=False)
#     district = db.Column(db.String(100), nullable=False)
#     village = db.Column(db.String(100), nullable=False)
#     created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

# class Warehouse(db.Model):
#     __tablename__ = 'warehouse'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     country = db.Column(db.String(100), nullable=False)
#     state = db.Column(db.String(100), nullable=False)
#     district = db.Column(db.String(100), nullable=False)
#     village = db.Column(db.String(100), nullable=False)
#     capacity = db.Column(db.Integer, nullable=False)
#     created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

# class Commodity(db.Model):
#     __tablename__ = 'commodity'
#     id = db.Column(db.Integer, primary_key=True)
#     commodity_name = db.Column(db.String(100), nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

# class FarmerWarehouseCommodity(db.Model):
#     __tablename__ = 'farmer_warehouse_commodity'
#     id = db.Column(db.Integer, primary_key=True)
#     farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.id'), nullable=False)
#     warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)
#     commodity_id = db.Column(db.Integer, db.ForeignKey('commodity.id'), nullable=False)
#     farmer_warehouse_commodity_receipt = db.Column(db.String(255), nullable=False, unique=True)

#     farmer = db.relationship('Farmer', backref=db.backref('farmer_warehouse_commodity', lazy=True))
#     warehouse = db.relationship('Warehouse', backref=db.backref('farmer_warehouse_commodity', lazy=True))
#     commodity = db.relationship('Commodity', backref=db.backref('farmer_warehouse_commodity', lazy=True))

# with app.app_context():
#     db.create_all()

# def validate_receipt(receipt):
#     if not receipt or receipt.strip() == "":
#         return False, "Receipt cannot be empty."
#     if not re.match(r'^R-\d{4,}', receipt):
#         return False, "Receipt must start with 'R-' followed by at least 4 digits."
#     if FarmerWarehouseCommodity.query.filter_by(farmer_warehouse_commodity_receipt=receipt).first():
#         return False, "Receipt already exists. Please provide a unique receipt."
#     return True, None

# @auth.verify_password
# def verify_password(username, password):
#     if username in users and check_password_hash(users.get(username), password):
#         return username
#     return None

# class FarmerResource(Resource):
#     @auth.login_required  
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('id', required=True, help="ID cannot be blank!")
#         parser.add_argument('name', required=True, help="Name cannot be blank!")
#         parser.add_argument('contact', required=True, help="Contact cannot be blank!")
#         parser.add_argument('country', required=True, help="Country cannot be blank!")
#         parser.add_argument('state', required=True, help="State cannot be blank!")
#         parser.add_argument('district', required=True, help="District cannot be blank!")
#         parser.add_argument('village', required=True, help="Village cannot be blank!")
#         args = parser.parse_args()

#         try:
#             new_farmer = Farmer(
#                 id=args['id'],
#                 name=args['name'],
#                 contact=args['contact'],
#                 country=args['country'],
#                 state=args['state'],
#                 district=args['district'],
#                 village=args['village']
#             )
#             db.session.add(new_farmer)
#             db.session.commit()
#             return {'message': 'Farmer created successfully'}, 201
#         except SQLAlchemyError as e:
#             db.session.rollback()
#             return {'message': 'Database error', 'data': str(e)}, 500
#         finally:
#             db.session.close()  

# class WarehouseResource(Resource):
#     @auth.login_required  
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('id', required=True, help="ID cannot be blank!")
#         parser.add_argument('name', required=True, help="Name cannot be blank!")
#         parser.add_argument('country', required=True, help="Country cannot be blank!")
#         parser.add_argument('state', required=True, help="State cannot be blank!")
#         parser.add_argument('district', required=True, help="District cannot be blank!")
#         parser.add_argument('village', required=True, help="Village cannot be blank!")
#         parser.add_argument('capacity', required=True, help="Capacity cannot be blank!")
#         args = parser.parse_args()

#         try:
#             new_warehouse = Warehouse(
#                 id=args['id'],
#                 name=args['name'],
#                 country=args['country'],
#                 state=args['state'],
#                 district=args['district'],
#                 village=args['village'],
#                 capacity=args['capacity']
#             )
#             db.session.add(new_warehouse)
#             db.session.commit()
#             return {'message': 'Warehouse created successfully'}, 201
#         except SQLAlchemyError as e:
#             db.session.rollback()
#             return {'message': 'Database error', 'data': str(e)}, 500
#         finally:
#             db.session.close()  

# class CommodityResource(Resource):
#     @auth.login_required  
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('id', required=True, help="ID cannot be blank!")
#         parser.add_argument('commodity_name', required=True, help="Commodity name cannot be blank!")
#         parser.add_argument('quantity', required=True, help="Quantity cannot be blank!")
#         args = parser.parse_args()

#         try:
#             new_commodity = Commodity(
#                 id=args['id'],
#                 commodity_name=args['commodity_name'],
#                 quantity=args['quantity']
#             )
#             db.session.add(new_commodity)
#             db.session.commit()
#             return {'message': 'Commodity created successfully'}, 201
#         except SQLAlchemyError as e:
#             db.session.rollback()
#             return {'message': 'Database error', 'data': str(e)}, 500
#         finally:
#             db.session.close()  

# class FarmerWarehouseCommodityResource(Resource):
#     @auth.login_required  
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('id', required=True, help="ID cannot be blank!")
#         parser.add_argument('farmer_id', required=True, help="Farmer ID cannot be blank!")
#         parser.add_argument('warehouse_id', required=True, help="Warehouse ID cannot be blank!")
#         parser.add_argument('commodity_id', required=True, help="Commodity ID cannot be blank!")
#         parser.add_argument('farmer_warehouse_commodity_receipt', required=True, help="Receipt cannot be blank!")
#         args = parser.parse_args()

#         receipt = args['farmer_warehouse_commodity_receipt']
#         is_valid, error_message = validate_receipt(receipt)
#         if not is_valid:
#             return {'message': error_message}, 400

#         try:
#             new_record = FarmerWarehouseCommodity(
#                 id=args['id'],
#                 farmer_id=args['farmer_id'],
#                 warehouse_id=args['warehouse_id'],
#                 commodity_id=args['commodity_id'],
#                 farmer_warehouse_commodity_receipt=receipt
#             )
#             db.session.add(new_record)
#             db.session.commit()
#             return {'message': 'Farmer-Warehouse-Commodity record created successfully'}, 201

#         except SQLAlchemyError as e:
#             db.session.rollback()  
#             return {'message': 'Database error', 'data': str(e)}, 500
#         finally:
#             db.session.close()  

# api.add_resource(FarmerResource, '/farmer')
# api.add_resource(WarehouseResource, '/warehouse')
# api.add_resource(CommodityResource, '/commodity')
# api.add_resource(FarmerWarehouseCommodityResource, '/farmer_warehouse_commodity')

# if __name__ == '__main__':
#     app.run(debug=True)
