from flask import Flask, render_template, request
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key' # Change this to a random secret key

# Database Configuration (PostgreSQL for Vercel, SQLite for Local)
import os
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Database Model for Merch
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200))

class ArtistSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    upcoming_drop = db.Column(db.String(100), nullable=True) # e.g. "2023-12-25"
    spotify_artist_id = db.Column(db.String(100), nullable=True)
    spotify_client_id = db.Column(db.String(100), nullable=True)
    spotify_client_secret = db.Column(db.String(100), nullable=True)
    
    # Cached Data
    latest_release_id = db.Column(db.String(100), nullable=True)
    latest_release_name = db.Column(db.String(200), nullable=True)
    latest_release_image = db.Column(db.String(500), nullable=True)
    # Store top tracks as a JSON string for simplicity
    top_tracks_json = db.Column(db.Text, nullable=True) 

# Spotify Helper
def get_spotify_client(client_id, client_secret):
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    try:
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(auth_manager=auth_manager)
        return sp
    except Exception as e:
        print(f"Spotify Auth Error: {e}")
        return None

# Run this once in python console to create: db.create_all()

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    settings = ArtistSettings.query.first()
    if not settings:
        settings = ArtistSettings()
        db.session.add(settings)
        db.session.commit()

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update_settings':
            settings.upcoming_drop = request.form.get('upcoming_drop')
            settings.spotify_artist_id = request.form.get('spotify_artist_id')
            settings.spotify_client_id = request.form.get('spotify_client_id')
            settings.spotify_client_secret = request.form.get('spotify_client_secret')
            db.session.commit()
            return redirect(url_for('admin'))
            
        elif action == 'sync_spotify':
             if settings.spotify_client_id and settings.spotify_client_secret and settings.spotify_artist_id:
                sp = get_spotify_client(settings.spotify_client_id, settings.spotify_client_secret)
                if sp:
                    try:
                        # Fetch Latest Release
                        results = sp.artist_albums(settings.spotify_artist_id, album_type='album,single', limit=1)
                        if results['items']:
                            latest = results['items'][0]
                            settings.latest_release_id = latest['id']
                            settings.latest_release_name = latest['name']
                            settings.latest_release_image = latest['images'][0]['url'] if latest['images'] else None
                        
                        # Fetch Top Tracks
                        top_tracks = sp.artist_top_tracks(settings.spotify_artist_id)
                        import json
                        tracks_data = []
                        for track in top_tracks['tracks'][:5]:
                             tracks_data.append({
                                 'name': track['name'],
                                 'id': track['id'],
                                 'duration_ms': track['duration_ms']
                             })
                        settings.top_tracks_json = json.dumps(tracks_data)
                        
                        db.session.commit()
                    except Exception as e:
                        print(f"Sync Error: {e}")
             return redirect(url_for('admin'))

        # Legacy Merch Logic (kept for compatibility, UI removed)
        # elif action == 'add_product':
        #     new_name = request.form.get('name')
        #     new_price = request.form.get('price')
        #     new_product = Product(name=new_name, price=new_price)
        #     db.session.add(new_product)
        #     db.session.commit()
        #     return redirect(url_for('merch'))
        
    return render_template('admin.html', settings=settings)

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# Routes
@app.route('/')
def home():
    settings = ArtistSettings.query.first()
    return render_template('home.html', title="Home", settings=settings)

@app.route('/music')
def music():
    settings = ArtistSettings.query.first()
    top_tracks = []
    if settings and settings.top_tracks_json:
        import json
        try:
            top_tracks = json.loads(settings.top_tracks_json)
        except:
            pass
    return render_template('music.html', title="Music", settings=settings, top_tracks=top_tracks)

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
