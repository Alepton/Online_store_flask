from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/user')
def user():
    return render_template("user.html")


@app.route('/users/<string:name>/<int:id>')
def users(name, id):
    return "User page " + name + " - " + str(id)


if __name__ == "__main__":
    app.run(debug=True)
