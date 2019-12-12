from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask('__name__', template_folder='templates')

base_dir = os.path.abspath(os.path.dirname('__file__'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
mars_mallow = Marshmallow(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    price = db.Column(db.Integer)

    def __int__(self, name, price):
        self.name = name
        self.price = price


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))

    def __int__(self, username, password):
        self.username = username
        self.password = password


class ProductSchema(mars_mallow.Schema):
    class Meta:
        fields = ('id', 'name', 'price')


class UserSchema(mars_mallow.Schema):
    class Meta:
        fields = ('id', 'username', 'password')


# product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
user_schema = UserSchema(many=True)


@app.route('/products', methods=['POST'])
def add_product():
    name = request.json['name']
    price = request.json['price']

    new_product = Product(name=name, price=price)
    db.session.add(new_product)
    db.session.commit()

    return products_schema.jsonify(new_product)


@app.route('/products', methods=['GET'])
def get_all_products():
    all_products = Product.query.all()
    # result = products_schema.dump(all_products)

    return products_schema.jsonify(all_products)


@app.route('/products/<product_id>', methods=['GET'])
def get_single_product(product_id):
    product = Product.query.get(product_id)
    return products_schema.jsonify(product)


@app.route('/users', methods=['GET'])
def get_all_users():
    # username = request.json['username']
    # password = request.json['password']
    users = User.query.all()
    users = user_schema.dump(users)
    print("users are : ", jsonify(users))
    for user in users:
        print(user)
    return jsonify(users)


@app.route('/users', methods=['POST'])
def create_new_user():
    if request.method == "POST":
        # take argument as query
        # username = request.args.get('username')
        # password = request.args.get('password')
        username = request.form.get('username')
        password = request.form.get('password')
        print(username, password)
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return "new user created"
    else:
        return None


@app.route('/delete/user/<slug>', methods=['DELETE'])
def delete_a_user(slug):
    user = User.query.get(slug)
    print(user)
    db.session.delete(user)
    db.session.commit()
    return f'{user} is deleted'


if __name__ == '__main__':
    app.run(debug=True)


