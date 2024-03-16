# #!/usr/bin/env python3


# from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from models import db, Restaurant, Pizza, RestaurantPizza


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# db.init_app(app)
# migrate = Migrate(app, db)


# @app.route('/')
# def home():
#     return 'Welcome to the Pizza App!'

# @app.route('/restaurants')
# def get_restaurants():
#     restaurants = Restaurant.query.all()
#     return jsonify([restaurant.to_dict(fields=('id', 'name', 'address')) for restaurant in restaurants]), 200


# @app.route('/restaurants/<int:id>')
# def get_restaurant(id):
#     restaurant = Restaurant.query.get(id)
#     if restaurant:
#         return jsonify(restaurant.to_dict(included=['restaurant_pizzas'])), 200
#     else:
#         return jsonify({'error': 'Restaurant not found'}), 404


# @app.route('/restaurants/<int:id>', methods=['DELETE'])
# def delete_restaurant(id):
#     restaurant = Restaurant.query.get(id)
#     if restaurant:
#         db.session.delete(restaurant)
#         db.session.commit()
#         return '', 204
#     else:
#         return jsonify({'error': 'Restaurant not found'}), 404


# @app.route('/pizzas')
# def get_pizzas():
#     pizzas = Pizza.query.all()
#     return jsonify([pizza.to_dict() for pizza in pizzas]), 200


# @app.route('/restaurant_pizzas', methods=['POST'])
# def create_restaurant_pizza():
#     data = request.get_json()
#     new_restaurant_pizza = RestaurantPizza(price=data['price'], pizza_id=data['pizza_id'], restaurant_id=data['restaurant_id'])
#     db.session.add(new_restaurant_pizza)
#     try:
#         db.session.commit()
#         return jsonify(new_restaurant_pizza.to_dict(included=['pizza', 'restaurant'])), 201
#     except AssertionError as e:
#         db.session.rollback()
#         return jsonify({'errors': [str(e)]}), 400


# if __name__ == '__main__':
#     app.run(port=5555, debug=True)


# phase-4-code-challenge-pizzas-KevinKiseli/server/app.py

from flask import Flask, request, jsonify
from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return 'Welcome to the Pizza App!'

# GET /restaurants
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = db.session.query(Restaurant).all()
    return jsonify([restaurant.to_dict() for restaurant in restaurants]), 200

# GET /restaurants/<int:id>
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant_by_id(id):
    restaurant = db.session.query(Restaurant).get(id)
    if restaurant:
        return jsonify(restaurant.to_dict(include_pizzas=True)), 200
    else:
        return jsonify({"error": "Restaurant not found"}), 404

# DELETE /restaurants/<int:id>
@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = db.session.query(Restaurant).get(id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    else:
        return jsonify({"error": "Restaurant not found"}), 404

# GET /pizzas
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = db.session.query(Pizza).all()
    return jsonify([pizza.to_dict() for pizza in pizzas]), 200

# POST /restaurant_pizzas
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.json
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    if not all([price, pizza_id, restaurant_id]):
        return jsonify({"errors": ["validation errors"]}), 400

    if not (1 <= price <= 30):
        return jsonify({"errors": ["validation errors"]}), 400

    pizza = db.session.query(Pizza).get(pizza_id)
    restaurant = db.session.query(Restaurant).get(restaurant_id)

    if not (pizza and restaurant):
        return jsonify({"errors": ["Pizza or Restaurant not found"]}), 404

    try:
        new_restaurant_pizza = RestaurantPizza(
            price=price,
            pizza_id=pizza_id,
            restaurant_id=restaurant_id
        )
        db.session.add(new_restaurant_pizza)
        db.session.commit()

        return jsonify(new_restaurant_pizza.to_dict()), 201
    except ValueError as e:
        return jsonify({"errors": [str(e)]}), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)
