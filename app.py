from flask import Flask, render_template, request
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required

app = Flask(__name__)

from werkzeug.security import generate_password_hash, check_password_hash

# Update your Login Route
@app.route('/login', methods=['GET', 'POST'])
def admin_dashboard():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        # check_password_hash compares the typed password with the stored hash
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('admin'))
        else:
            print("Login Failed") # You can add a flash message here later
    return render_template('login.html')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_bronze_key'
db = SQLAlchemy(app)

# Database Model for Merch
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200))

@app.route('/delete-merch/<int:id>', methods=['POST'])
@login_required
def delete_merch(id):
    item = Product.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

# Run this once in python console to create: db.create_all()

@app.route('/admin', methods=['GET', 'POST'])
# @login_required  <-- Add this once you set up a login page
def admin():
    if request.method == 'POST':
        # Get data from the form
        new_name = request.form.get('name')
        new_price = request.form.get('price')
        
        # Save to database
        new_product = Product(name=new_name, price=new_price)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('merch'))
        
    return render_template('admin.html')

# Models for Music and Announcements
class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    audio_url = db.Column(db.String(200)) # Link to mp3
    is_new_release = db.Column(db.Boolean, default=False)

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=db.func.current_timestamp())

# User Model for Admin Login
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']: # Use hashing in production!
            login_user(user)
            return redirect(url_for('admin'))
    return render_template('login.html')



@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# Routes
@app.route('/')
def home():
    return render_template('home.html', title="Home")

@app.route('/music')
def music():
    return render_template('music.html', title="Music")

@app.route('/merch')
def merch():
    return render_template('merch.html', title="Merch")


@app.route('/about')
def about():
    return render_template('about.html', title="About")

@app.route('/bookings', methods=['GET', 'POST'])
def bookings():
    if request.method == 'POST':
        # Handle form submission logic here (e.g., email or database)
        pass
    return render_template('bookings.html', title="Bookings")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle form submission logic here
        pass
    return render_template('contact.html', title="Contact")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
