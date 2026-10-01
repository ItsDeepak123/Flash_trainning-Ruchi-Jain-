from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/Library_Management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy
db = SQLAlchemy(app)

# Secret key for login session
app.secret_key = "library123"

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    username = db.Column(db.String(80), unique=True, nullable=True)
    password = db.Column(db.String(80), nullable=True)

class Book(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(50), default="Available")

@app.route('/registration', methods=['GET', 'POST'])
def registration():

    if request.method == 'POST':

        name = request.form['name']
        username = request.form['username']
        password = request.form['password']

        user = User(
            name=name,
            username=username,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('registration.html')




@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(
            username=username,
            password=password
        ).first()

        if user:

            session['user_id'] = user.id
            session['username'] = user.username

            return redirect(url_for('home'))

        return "Invalid Username or Password"

    return render_template('login.html')



@app.route('/home')
def home():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    books = Book.query.all()

    return render_template(
        'home.html',
        books=books
    )


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        name = request.form['name']
        category = request.form['category']
        quantity = int(request.form['quantity'])

        book = Book(
            name=name,
            category=category,
            quantity=quantity,
            status="Available"
        )

        db.session.add(book)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add_book.html')



@app.route('/book_details/<int:id>')
def book_details(id):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    book = Book.query.get(id)

    return render_template(
        'book_details.html',
        book=book
    )



@app.route('/issue/<int:id>')
def issue(id):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    book = Book.query.get(id)

    if book.quantity > 0:

        book.quantity = book.quantity - 1

        if book.quantity == 0:
            book.status = "Issued"

        db.session.commit()

    return redirect(url_for('home'))




@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    book = Book.query.get(id)

    if request.method == 'POST':

        book.name = request.form['name']
        book.category = request.form['category']
        book.quantity = request.form['quantity']

        if int(book.quantity) > 0:
            book.status = "Available"
        else:
            book.status = "Issued"

        db.session.commit()

        return redirect(url_for('home'))

    return render_template(
        'update_book.html',
        book=book
    )



@app.route('/delete/<int:id>')
def delete(id):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    book = Book.query.get(id)

    db.session.delete(book)
    db.session.commit()

    return redirect(url_for('home'))




@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('login'))




with app.app_context():

    db.create_all()




if __name__ == '__main__':

    app.run(debug=True)