from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key' # Optional if no sessions used

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# Models removed for static client-side version


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

@app.route('/privacy')
def privacy():
    return render_template('privacy.html', title="Privacy Policy")

@app.route('/terms')
def terms():
    return render_template('terms.html', title="Terms of Service")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
