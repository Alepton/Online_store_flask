from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout



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
    items = Item.query.order_by(Item.price).all()
    return render_template("index.html", data=items)

@app.route('/buy/<int:id>') # создаем динамический параметр ссылки int - числовой ; id - имя которое передадим в функцию item_by(id)
def item_by(id):
    item = Item.query.get(id) # получаем из базы данных объект по id нажатой кнопки

    # вставляем код из официальной документации
    api = Api(merchant_id=1396424,  # id нашей компании, который выдается при регистрации на сайте
              secret_key='test')    # secret_key - секретный ключ который так же выдается при регистрации, пока будем использовать тестовый
    checkout = Checkout(api=api)    # создается страничка оплаты
    data = {                        # данные которые мы передаем для оплаты
        "currency": "BYN",
        "amount": str(item.price) + "00"  # у объекта item считываем price, преобразуем его в строку и прибывам 00 копеек
    }
    url = checkout.url(data).get('checkout_url')
    #return url посмотрим url ссылку при переходи на которую мы сможем выполнить оплату товара
    #return str(id) # просто выведим id на страницу для проверки работы
    return redirect(url) # выполняем переадресацию на url оплаты

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
