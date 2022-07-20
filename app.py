from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    discription = db.Column(db.String(150), nullable=False)
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


@app.route('/creat')
def creat():
    return render_template("creat.html")


@app.route('/user')
def user():
    return render_template("user.html")


@app.route('/users/<string:name>/<int:id>')
def users(name, id):
    return "User page " + name + " - " + str(id)


if __name__ == "__main__":
    app.run(debug=True)
