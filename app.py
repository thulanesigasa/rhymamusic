from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key' # Optional if no sessions used

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_bronze_key')

# Database Configuration
# Database Configuration
uri = os.environ.get('DATABASE_URL') or os.environ.get('POSTGRES_URL')
if uri:
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
else:
    # On Vercel, the root is read-only. We move the SQLite DB to /tmp/ if no DB is provided.
    if os.environ.get('VERCEL'):
        uri = 'sqlite:////tmp/site.db'
    else:
        uri = 'sqlite:///site.db'

app.config['SQLALCHEMY_DATABASE_URI'] = uri

# Configure where to save images
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'static/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the folder exists
try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
except OSError:
    pass # Ignore error on read-only file systems (like Vercel)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)

class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    audio_url = db.Column(db.String(200)) # Link to mp3
    is_new_release = db.Column(db.Boolean, default=False)

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def home():
    latest_single = None
    try:
        latest_single = Track.query.filter_by(is_new_release=True).first()
    except Exception as e:
        print(f"Error querying latest single: {e}")

    latest_video = None
    try:
        settings = Settings.query.first()
        if not settings or not settings.latest_youtube_id:
            sync_youtube_video()
            settings = Settings.query.first()

        if settings and settings.latest_youtube_id:
            latest_video = {
                'youtube_id': settings.latest_youtube_id,
                'title': settings.latest_youtube_title or 'New Release Video'
            }
    except Exception as e:
        print(f"Error fetching YouTube settings: {e}")

    return render_template('home.html', title="Home", latest_single=latest_single, latest_video=latest_video)

@app.route('/music')
def music():
    return render_template('music.html', title="Music")

@app.route('/merch')
def merch():
    products = Product.query.all()
    return render_template('merch.html', title="Merch", products=products)

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        # In production, use check_password_hash(user.password, request.form['password'])
        if user and user.password == request.form['password']: 
            login_user(user)
            return redirect(url_for('admin'))
        else:
            print("Login Failed")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/admin', methods=['GET', 'POST'])
@login_required # Add login required
def admin():
    products = Product.query.all()
    settings = Settings.query.first()
    return render_template('admin.html', products=products, settings=settings)

@app.route('/admin/add-merch', methods=['POST'])
@login_required
def add_merch():
    name = request.form.get('name')
    price = request.form.get('price')
    file = request.files.get('image')

    image_path = None
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_path = f'uploads/{filename}'
        
    new_product = Product(name=name, price=price, image_url=image_path)
    db.session.add(new_product)
    db.session.commit()
    
    return redirect(url_for('admin')) # Redirect to admin dashboard

@app.route('/delete-merch/<int:id>', methods=['POST'])
@login_required
def delete_merch(id):
    item = Product.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('admin'))

# --- Spotify Integration ---
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask import jsonify

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(100), nullable=True)
    youtube_channel_id = db.Column(db.String(100), nullable=True)
    latest_youtube_id = db.Column(db.String(100), nullable=True)
    latest_youtube_title = db.Column(db.String(200), nullable=True)

import urllib.request
import xml.etree.ElementTree as ET
import re

def get_channel_id_from_handle(handle="rhymangn"):
    clean_handle = handle if handle.startswith('@') else '@' + handle
    url = f"https://www.youtube.com/{clean_handle}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            match = re.search(r'youtube\.com/channel/(UC[\w-]+)', html)
            if match:
                return match.group(1)
            match = re.search(r'channel_id=([\w-]+)', html)
            if match:
                return match.group(1)
            match = re.search(r'"channelId":"(UC[\w-]+)"', html)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"Error fetching channel page: {e}")
    return None

def sync_youtube_video():
    try:
        settings = Settings.query.first()
        if not settings:
            settings = Settings()
            db.session.add(settings)
            db.session.commit()

        channel_id = settings.youtube_channel_id or os.environ.get('YOUTUBE_CHANNEL_ID')
        if not channel_id:
            channel_id = get_channel_id_from_handle("rhymangn")
            if channel_id:
                settings.youtube_channel_id = channel_id
                db.session.commit()

        if not channel_id:
            return False, "Could not find YouTube Channel ID."

        rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        req = urllib.request.Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            ns = {
                'atom': 'http://www.w3.org/2005/Atom',
                'yt': 'http://www.youtube.com/xml/schemas/2015'
            }
            entry = root.find('atom:entry', ns)
            if entry is not None:
                video_id_elem = entry.find('yt:videoId', ns)
                title_elem = entry.find('atom:title', ns)
                video_id = video_id_elem.text if video_id_elem is not None else None
                title = title_elem.text if title_elem is not None else None

                if video_id:
                    settings.latest_youtube_id = video_id
                    settings.latest_youtube_title = title
                    db.session.commit()
                    return True, f"Synced YouTube Video: '{title}' ({video_id})"
        return False, "No video entries found in YouTube RSS feed."
    except Exception as e:
        return False, str(e)


def sync_spotify_music():
    try:
        settings = Settings.query.first()
        # Use env var as default fallback if DB is empty
        artist_id = settings.artist_id if (settings and settings.artist_id) else os.environ.get('SPOTIFY_ARTIST_ID')
        if not artist_id:
            return False, "Artist ID not configured in Settings or Env (SPOTIFY_ARTIST_ID)."
        auth_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(auth_manager=auth_manager)
        # Clear existing new release flags
        for t in Track.query.filter_by(is_new_release=True).all():
            t.is_new_release = False
        db.session.commit()
        # Fetch latest releases (Singles & Albums/EPs)
        # We fetch more than 1 to ensure we can sort them by release_date properly
        results = sp.artist_albums(artist_id, album_type='single,album', limit=5)
        added_count = 0
        if results['items']:
            # Sort by release_date descending (newest first)
            sorted_albums = sorted(results['items'], key=lambda x: x['release_date'], reverse=True)
            latest_album = sorted_albums[0]
            track_title = latest_album['name']
            audio_url = latest_album['external_urls']['spotify']
            release_date = latest_album['release_date']
            # Check if this single is already in our DB
            existing = Track.query.filter_by(title=track_title).first()
            if existing:
                existing.is_new_release = True
                existing.audio_url = audio_url  # update url just in case
            else:
                new_track = Track(title=track_title, audio_url=audio_url, is_new_release=True)
                db.session.add(new_track)
                added_count += 1
            db.session.commit()
            return True, f"Found Latest: '{track_title}' ({release_date}). Synced {added_count} new track(s)."
        return False, "No releases found for this Artist ID on Spotify."
    except Exception as e:
        return False, str(e)

@app.route('/admin/sync-spotify', methods=['POST'])
@login_required
def sync_spotify_route():
    success, msg = sync_spotify_music()
    print(f"Spotify Sync: {success} - {msg}") # Logs to console
    return redirect(url_for('admin'))

@app.route('/admin/sync-youtube', methods=['POST'])
@login_required
def sync_youtube_route():
    success, msg = sync_youtube_video()
    print(f"YouTube Sync: {success} - {msg}")
    return redirect(url_for('admin'))

@app.route('/admin/settings', methods=['POST'])
@login_required
def update_settings():
    aid = request.form.get('artist_id')
    settings = Settings.query.first()
    if not settings:
        settings = Settings(artist_id=aid)
        db.session.add(settings)
    else:
        settings.artist_id = aid
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/youtube-settings', methods=['POST'])
@login_required
def update_youtube_settings():
    cid = request.form.get('youtube_channel_id')
    vid = request.form.get('latest_youtube_id')
    settings = Settings.query.first()
    if not settings:
        settings = Settings(youtube_channel_id=cid)
        db.session.add(settings)
    else:
        if cid:
            settings.youtube_channel_id = cid
        if vid:
            if 'v=' in vid:
                vid = vid.split('v=')[1].split('&')[0]
            elif 'youtu.be/' in vid:
                vid = vid.split('youtu.be/')[1].split('?')[0]
            settings.latest_youtube_id = vid
    db.session.commit()
    return redirect(url_for('admin'))

# --- API Endpoints for Mobile App ---
@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    data = [{'id': p.id, 'name': p.name, 'price': p.price, 'image_url': p.image_url} for p in products]
    return jsonify(data)

@app.route('/api/tracks', methods=['GET'])
def get_tracks():
    tracks = Track.query.all()
    data = [{'id': t.id, 'title': t.title, 'audio_url': t.audio_url, 'is_new_release': t.is_new_release} for t in tracks]
    return jsonify(data)

@app.route('/api/latest-video', methods=['GET'])
def get_latest_video():
    settings = Settings.query.first()
    if not settings or not settings.latest_youtube_id:
        sync_youtube_video()
        settings = Settings.query.first()
    return jsonify({
        'youtube_id': settings.latest_youtube_id if settings else 'prZ-ErkCkNw',
        'title': settings.latest_youtube_title if settings else 'New Release Video',
        'embed_url': f"https://www.youtube.com/embed/{settings.latest_youtube_id if settings and settings.latest_youtube_id else 'prZ-ErkCkNw'}"
    })

@app.route('/api/cron/sync', methods=['GET'])
def cron_sync():
    # Check for authentication (Vercel Cron Secret)
    cron_secret = os.environ.get('CRON_SECRET')
    if cron_secret:
        auth_header = request.headers.get('Authorization')
        # Vercel sends: Authorization: Bearer <CRON_SECRET>
        if not auth_header or auth_header != f"Bearer {cron_secret}":
             return jsonify({'error': 'Unauthorized'}), 401
    
    spotify_success, spotify_msg = sync_spotify_music()
    youtube_success, youtube_msg = sync_youtube_video()
    return jsonify({
        'spotify': {'success': spotify_success, 'message': spotify_msg},
        'youtube': {'success': youtube_success, 'message': youtube_msg}
    })


# Run this once in python console to create: db.create_all()

# Database initialization for Vercel/Production
def init_db():
    try:
        with app.app_context():
            db.create_all()
            with db.engine.connect() as conn:
                try:
                    result = conn.execute(db.text("PRAGMA table_info(settings)")).fetchall()
                    columns = [row[1] for row in result]
                    if columns:
                        if 'youtube_channel_id' not in columns:
                            conn.execute(db.text("ALTER TABLE settings ADD COLUMN youtube_channel_id VARCHAR(100)"))
                        if 'latest_youtube_id' not in columns:
                            conn.execute(db.text("ALTER TABLE settings ADD COLUMN latest_youtube_id VARCHAR(100)"))
                        if 'latest_youtube_title' not in columns:
                            conn.execute(db.text("ALTER TABLE settings ADD COLUMN latest_youtube_title VARCHAR(200)"))
                        conn.commit()
                except Exception as ex:
                    print(f"Schema migration info: {ex}")
    except Exception as e:
        print(f"Database initialization skipped or failed: {e}")

init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
