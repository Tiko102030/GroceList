from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

def init_db():
    with app.app_context():
        db.create_all()

@app.route('/')
def home():
    products = Product.query.all()
    return render_template('dashboard.html', products=products)

@app.route('/add', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(name=data['name'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added!', 'id': new_product.id})

@app.route('/remove/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product removed!'})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
