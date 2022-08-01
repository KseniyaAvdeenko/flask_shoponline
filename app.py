from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# models
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    # image = db.Column(db.LargeBinary, default='img/default.jpg')
    isActive = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Item %r>' % self.id



# routes
@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        category = request.form['category']

        item = Item(title=title, price=price, category=category)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')

        except:
            return "Error!"

    else:
        return render_template('create.html')


if __name__ == "__main__":
    app.run(debug=True)
