from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Sukla%40123@localhost/farmer_warehouse_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Farmer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class Commodity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)
    commodity_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_stored = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(50), default="stored")



@app.route('/')
def home():
    return "Welcome to the Farmer Warehouse API"

@app.before_request
def create_tables():
    db.create_all()

@app.route('/farmer', methods=['POST'])
def create_farmer():
    data = request.get_json()
    new_farmer = Farmer(id=data['id'],name=data['name'], contact=data['contact'], location=data['location'])
    db.session.add(new_farmer)
    db.session.commit()
    return jsonify({'message': 'Farmer created successfully'}), 201

@app.route('/warehouse', methods=['POST'])
def create_warehouse():
    data = request.get_json()
    new_warehouse = Warehouse(id=data['id'],name=data['name'], location=data['location'], capacity=data['capacity'])
    db.session.add(new_warehouse)
    db.session.commit()
    return jsonify({'message': 'Warehouse created successfully'}), 201

@app.route('/commodity', methods=['POST'])
def store_commodity():
    data = request.get_json()
    new_commodity = Commodity(
        id=data['id'],farmer_id=data['farmer_id'], warehouse_id=data['warehouse_id'],
        commodity_name=data['commodity_name'], quantity=data['quantity']
    )
    db.session.add(new_commodity)
    db.session.commit()
    return jsonify({'message': 'Commodity stored successfully'}), 201

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
