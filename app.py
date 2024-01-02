from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app, resources={"/cars/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE"], "allow_headers": ["Content-Type"]}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
db = SQLAlchemy(app)

# Define the Car model
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)

# Define routes
@app.route('/cars', methods=['GET', 'POST'])
def cars():
    if request.method == 'GET':
        cars_list = Car.query.all()
        cars = [{'id': car.id, 'make': car.make, 'model': car.model, 'year': car.year} for car in cars_list]
        return jsonify(cars)
    elif request.method == 'POST':
        data = request.json
        new_car = Car(make=data['make'], model=data['model'], year=data['year'])
        db.session.add(new_car)
        db.session.commit()
        return jsonify({'message': 'Car added successfully!'})

@app.route('/cars/<int:car_id>', methods=['GET', 'PUT', 'DELETE'])
def car_detail(car_id):
    car = Car.query.get_or_404(car_id)

    if request.method == 'GET':
        return jsonify({'id': car.id, 'make': car.make, 'model': car.model, 'year': car.year})
    elif request.method == 'PUT':
        data = request.json
        car.make = data['make']
        car.model = data['model']
        car.year = data['year']
        db.session.commit()
        return jsonify({'message': 'Car updated successfully!'})
    elif request.method == 'DELETE':
        db.session.delete(car)
        db.session.commit()
        return jsonify({'message': 'Car deleted successfully!'})

# Run the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=8000, debug=True)