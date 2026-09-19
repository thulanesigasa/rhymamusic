from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import urllib.request
import xml.etree.ElementTree as ET
import re

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
        if should_sync_youtube(settings):
            sync_youtube_video()
            settings = Settings.query.first()

        if settings and settings.latest_youtube_id:
            latest_video = {
                'youtube_id': settings.latest_youtube_id,
                'title': settings.latest_youtube_title or 'Rhyma - 24/7 (Visualizer)'
            }
        else:
            latest_video = {
                'youtube_id': 'puw1cc7-2ZY',
                'title': 'Rhyma - 24/7 (Visualizer)'
            }
    except Exception as e:
        print(f"Error fetching YouTube settings: {e}")
        latest_video = {
            'youtube_id': 'puw1cc7-2ZY',
            'title': 'Rhyma - 24/7 (Visualizer)'
        }

    return render_template('home.html', title="Home", latest_single=latest_single, latest_video=latest_video)

@app.route('/music')
def music():
    tracks = []
    try:
        tracks = Track.query.order_by(Track.id.desc()).all()
    except Exception as e:
        print(f"Error fetching music tracks from DB: {e}")

    default_tracks = [
        {'title': 'AFRO NOIR', 'audio_url': 'https://open.spotify.com/album/6AvJoL5LSVDf2Jtm7NjgO8'},
        {'title': 'Stand Out', 'audio_url': 'https://open.spotify.com/album/11G7xf6VQHjhSSCtW6FRdt'},
        {'title': 'Stamina', 'audio_url': 'https://open.spotify.com/track/3b3VmMwvuKGPDNcUdYmLBh'},
        {'title': 'Medusa', 'audio_url': 'https://open.spotify.com/track/2tYZv2w593ANPrz1HZhp55'},
        {'title': 'I\'m Callin\'', 'audio_url': 'https://open.spotify.com/album/0u14DjLpxYnzJzHdnV1Ez1'}
    ]

    latest_tracks = []
    if tracks:
        for t in tracks:
            latest_tracks.append({
                'title': t.title,
                'audio_url': t.audio_url
            })

    if len(latest_tracks) < 5:
        for dt in default_tracks:
            if len(latest_tracks) >= 5:
                break
            if not any(t['audio_url'] == dt['audio_url'] for t in latest_tracks):
                latest_tracks.append(dt)

    return render_template('music.html', title="Music", latest_tracks=latest_tracks[:5])

def get_gallery_data():
    return [
        {'id': 1, 'url': url_for('static', filename='images/gallery/rhyma_gallery_1.jpg'), 'title': 'Rhyma Studio Shoot'},
        {'id': 2, 'url': url_for('static', filename='images/gallery/rhyma_gallery_2.jpg'), 'title': 'Writing Session'},
        {'id': 3, 'url': url_for('static', filename='images/gallery/rhyma_gallery_3.jpg'), 'title': 'Creative Process'},
        {'id': 4, 'url': url_for('static', filename='images/gallery/rhyma_gallery_4.jpg'), 'title': 'Lounge Session'},
        {'id': 5, 'url': url_for('static', filename='images/gallery/rhyma_gallery_5.jpg'), 'title': 'Luxury Portrait'},
        {'id': 6, 'url': url_for('static', filename='images/gallery/rhyma_gallery_6.jpg'), 'title': 'Afro Noir Shoot'},
        {'id': 8, 'url': url_for('static', filename='images/gallery/rhyma_gallery_8.jpg'), 'title': 'Khaki Vest Pose'},
        {'id': 9, 'url': url_for('static', filename='images/gallery/rhyma_gallery_9.jpg'), 'title': 'Archway Studio Shoot'},
        {'id': 10, 'url': url_for('static', filename='images/gallery/rhyma_gallery_10.jpg'), 'title': 'Focus Session'}
    ]

@app.route('/gallery')
def gallery():
    return render_template('gallery.html', title="Gallery", images=get_gallery_data())

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
    last_youtube_sync = db.Column(db.DateTime, nullable=True)

DEFAULT_YOUTUBE_CHANNEL_ID = "UCDew3CMxwN0A7VRLHOwXLBw"

def should_sync_youtube(settings):
    if not settings or not settings.latest_youtube_id or not settings.last_youtube_sync:
        return True
    try:
        time_diff = (datetime.utcnow() - settings.last_youtube_sync).total_seconds()
        return time_diff > 900 # Re-check YouTube RSS feed every 15 minutes
    except Exception:
        return True

def get_channel_id_from_handle(handle="rhymangn"):
    clean_handle = handle if handle.startswith('@') else '@' + handle
    url = f"https://www.youtube.com/{clean_handle}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
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
    return DEFAULT_YOUTUBE_CHANNEL_ID

def sync_youtube_video():
    try:
        settings = Settings.query.first()
        if not settings:
            settings = Settings()
            db.session.add(settings)
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()

        channel_id = settings.youtube_channel_id or os.environ.get('YOUTUBE_CHANNEL_ID')
        if not channel_id:
            channel_id = get_channel_id_from_handle("rhymangn") or DEFAULT_YOUTUBE_CHANNEL_ID
            settings.youtube_channel_id = channel_id
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()

        if not channel_id:
            channel_id = DEFAULT_YOUTUBE_CHANNEL_ID

        rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        req = urllib.request.Request(rss_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=6) as response:
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
                    settings.last_youtube_sync = datetime.utcnow()
                    try:
                        db.session.commit()
                    except Exception:
                        db.session.rollback()
                    return True, f"Synced YouTube Video: '{title}' ({video_id})"
        return False, "No video entries found in YouTube RSS feed."
    except Exception as e:
        print(f"YouTube sync error: {e}")
        try:
            db.session.rollback()
        except Exception:
            pass
        return False, str(e)



def sync_spotify_music():
    try:
        settings = Settings.query.first()
        artist_id = settings.artist_id if (settings and settings.artist_id) else os.environ.get('SPOTIFY_ARTIST_ID')
        if not artist_id:
            return False, "Artist ID not configured in Settings or Env (SPOTIFY_ARTIST_ID)."
        auth_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(auth_manager=auth_manager)

        results = sp.artist_albums(artist_id, album_type='single,album', limit=10)
        added_count = 0
        if results and results.get('items'):
            sorted_albums = sorted(results['items'], key=lambda x: x.get('release_date', ''), reverse=True)[:5]
            
            for item in sorted_albums:
                track_title = item['name']
                audio_url = item['external_urls']['spotify']
                existing = Track.query.filter_by(title=track_title).first()
                if not existing:
                    new_track = Track(title=track_title, audio_url=audio_url, is_new_release=True)
                    db.session.add(new_track)
                    added_count += 1
                else:
                    existing.audio_url = audio_url
            db.session.commit()
            return True, f"Synced top 5 latest releases from Spotify. Added {added_count} new track(s)."
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

from sqlalchemy import inspect, text

@app.route('/api/latest-video', methods=['GET'])
def get_latest_video():
    try:
        settings = Settings.query.first()
        if should_sync_youtube(settings):
            sync_youtube_video()
            settings = Settings.query.first()

        youtube_id = (settings.latest_youtube_id if (settings and settings.latest_youtube_id) else 'puw1cc7-2ZY')
        title = (settings.latest_youtube_title if (settings and settings.latest_youtube_title) else 'Rhyma - 24/7 (Visualizer)')
        return jsonify({
            'youtube_id': youtube_id,
            'title': title,
            'embed_url': f"https://www.youtube.com/embed/{youtube_id}"
        })
    except Exception as e:
        print(f"Error in get_latest_video endpoint: {e}")
        return jsonify({
            'youtube_id': 'puw1cc7-2ZY',
            'title': 'Rhyma - 24/7 (Visualizer)',
            'embed_url': 'https://www.youtube.com/embed/puw1cc7-2ZY'
        })

@app.route('/api/gallery', methods=['GET'])
def get_gallery():
    return jsonify(get_gallery_data())

@app.route('/api/cron/sync', methods=['GET'])
def cron_sync():
    # Check for authentication (Vercel Cron Secret)
    cron_secret = os.environ.get('CRON_SECRET')
    if cron_secret:
        auth_header = request.headers.get('Authorization')
        # Vercel sends: Authorization: Bearer <CRON_SECRET>
        if not auth_header or auth_header != f"Bearer {cron_secret}":
             return jsonify({'error': 'Unauthorized'}), 401
    
    spotify_success, spotify_msg = False, "Skipped"
    try:
        spotify_success, spotify_msg = sync_spotify_music()
    except Exception as e:
        spotify_msg = str(e)

    youtube_success, youtube_msg = False, "Skipped"
    try:
        youtube_success, youtube_msg = sync_youtube_video()
    except Exception as e:
        youtube_msg = str(e)

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
            try:
                inspector = inspect(db.engine)
                if 'settings' in inspector.get_table_names():
                    columns = [c['name'] for c in inspector.get_columns('settings')]
                    with db.engine.connect() as conn:
                        trans = conn.begin()
                        try:
                            if 'youtube_channel_id' not in columns:
                                conn.execute(text("ALTER TABLE settings ADD COLUMN youtube_channel_id VARCHAR(100)"))
                            if 'latest_youtube_id' not in columns:
                                conn.execute(text("ALTER TABLE settings ADD COLUMN latest_youtube_id VARCHAR(100)"))
                            if 'latest_youtube_title' not in columns:
                                conn.execute(text("ALTER TABLE settings ADD COLUMN latest_youtube_title VARCHAR(200)"))
                            if 'last_youtube_sync' not in columns:
                                conn.execute(text("ALTER TABLE settings ADD COLUMN last_youtube_sync TIMESTAMP"))
                            trans.commit()
                        except Exception as ex:
                            trans.rollback()
                            print(f"Schema migration error: {ex}")
            except Exception as ex:
                print(f"Schema inspection error: {ex}")
    except Exception as e:
        print(f"Database initialization skipped or failed: {e}")

init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
