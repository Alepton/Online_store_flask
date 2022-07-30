from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActiv = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return self.title



@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']

        item = Item(title=title, description=description, price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/') # переадресация на главную страницу после добавления данных в базу
        except:
            return "Произошла ошибка"
    else:
        return render_template("create.html")


@app.route('/user')
def user():
    return render_template("user.html")


@app.route('/users/<string:name>/<int:id>')
def users(name, id):
    return "User page " + name + " - " + str(id)


if __name__ == "__main__":
    app.run(debug=True)
