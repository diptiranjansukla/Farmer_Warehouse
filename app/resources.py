from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from app.models import Farmer, Warehouse, Commodity, FarmerWarehouseCommodity
from app import db, auth
from app.utils import validate_receipt

class FarmerResource(Resource):
    @auth.login_required  
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, help="ID cannot be blank!")
        parser.add_argument('name', required=True, help="Name cannot be blank!")
        parser.add_argument('contact', required=True, help="Contact cannot be blank!")
        parser.add_argument('country', required=True, help="Country cannot be blank!")
        parser.add_argument('state', required=True, help="State cannot be blank!")
        parser.add_argument('district', required=True, help="District cannot be blank!")
        parser.add_argument('village', required=True, help="Village cannot be blank!")
        args = parser.parse_args()

        try:
            new_farmer = Farmer(
                id=args['id'],
                name=args['name'],
                contact=args['contact'],
                country=args['country'],
                state=args['state'],
                district=args['district'],
                village=args['village']
            )
            db.session.add(new_farmer)
            db.session.commit()
            return {'message': 'Farmer created successfully'}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'Database error', 'data': str(e)}, 500
        finally:
            db.session.close()  

class WarehouseResource(Resource):
    @auth.login_required  
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, help="ID cannot be blank!")
        parser.add_argument('name', required=True, help="Name cannot be blank!")
        parser.add_argument('country', required=True, help="Country cannot be blank!")
        parser.add_argument('state', required=True, help="State cannot be blank!")
        parser.add_argument('district', required=True, help="District cannot be blank!")
        parser.add_argument('village', required=True, help="Village cannot be blank!")
        parser.add_argument('capacity', required=True, help="Capacity cannot be blank!")
        args = parser.parse_args()

        try:
            new_warehouse = Warehouse(
                id=args['id'],
                name=args['name'],
                country=args['country'],
                state=args['state'],
                district=args['district'],
                village=args['village'],
                capacity=args['capacity']
            )
            db.session.add(new_warehouse)
            db.session.commit()
            return {'message': 'Warehouse created successfully'}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'Database error', 'data': str(e)}, 500
        finally:
            db.session.close()  

class CommodityResource(Resource):
    @auth.login_required  
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, help="ID cannot be blank!")
        parser.add_argument('commodity_name', required=True, help="Commodity name cannot be blank!")
        parser.add_argument('quantity', required=True, help="Quantity cannot be blank!")
        args = parser.parse_args()

        try:
            new_commodity = Commodity(
                id=args['id'],
                commodity_name=args['commodity_name'],
                quantity=args['quantity']
            )
            db.session.add(new_commodity)
            db.session.commit()
            return {'message': 'Commodity created successfully'}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'Database error', 'data': str(e)}, 500
        finally:
            db.session.close()  

class FarmerWarehouseCommodityResource(Resource):
    @auth.login_required  
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, help="ID cannot be blank!")
        parser.add_argument('farmer_id', required=True, help="Farmer ID cannot be blank!")
        parser.add_argument('warehouse_id', required=True, help="Warehouse ID cannot be blank!")
        parser.add_argument('commodity_id', required=True, help="Commodity ID cannot be blank!")
        parser.add_argument('farmer_warehouse_commodity_receipt', required=True, help="Receipt cannot be blank!")
        args = parser.parse_args()

        receipt = args['farmer_warehouse_commodity_receipt']
        is_valid, error_message = validate_receipt(receipt)
        if not is_valid:
            return {'message': error_message}, 400

        try:
            new_record = FarmerWarehouseCommodity(
                id=args['id'],
                farmer_id=args['farmer_id'],
                warehouse_id=args['warehouse_id'],
                commodity_id=args['commodity_id'],
                farmer_warehouse_commodity_receipt=receipt
            )
            db.session.add(new_record)
            db.session.commit()
            return {'message': 'Farmer-Warehouse-Commodity record created successfully'}, 201

        except SQLAlchemyError as e:
            db.session.rollback()  
            return {'message': 'Database error', 'data': str(e)}, 500
        finally:
            db.session.close()  



