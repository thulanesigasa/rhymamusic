from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import re
import urllib.request

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
    audio_url = db.Column(db.String(200)) # Link to mp3 or Spotify URL
    is_new_release = db.Column(db.Boolean, default=False)
    release_type = db.Column(db.String(20), default='single') # 'single' or 'ep'
    release_date = db.Column(db.String(20), nullable=True)

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def home():
    latest_single = Track.query.filter_by(is_new_release=True).first()
    settings = Settings.query.first()
    latest_video_id = settings.latest_video_id if (settings and settings.latest_video_id) else 'puw1cc7-2ZY'
    return render_template('home.html', title="Home", latest_single=latest_single, latest_video_id=latest_video_id)

@app.template_filter('spotify_embed')
def spotify_embed_filter(url):
    if not url:
        return ""
    if '/embed/' in url:
        return url
    converted = url.replace('https://open.spotify.com/', 'https://open.spotify.com/embed/')
    if '?' not in converted:
        converted += '?utm_source=generator'
    return converted

@app.route('/music')
def music():
    try:
        eps = Track.query.filter_by(release_type='ep').order_by(Track.id.desc()).limit(5).all()
        singles = Track.query.filter_by(release_type='single').order_by(Track.id.desc()).limit(5).all()
    except Exception:
        eps, singles = [], []

    default_eps = [
        {"title": "AFRO NOIR", "audio_url": "https://open.spotify.com/album/6AvJoL5LSVDf2Jtm7NjgO8"},
        {"title": "VIBES ON VIBES", "audio_url": "https://open.spotify.com/album/4zdanK4qRRjCe0N4XXToBt"},
        {"title": "STAND OUT", "audio_url": "https://open.spotify.com/album/11G7xf6VQHjhSSCtW6FRdt"},
        {"title": "STAMINA", "audio_url": "https://open.spotify.com/album/3YUXPunrRpyRj2zv3ufbEQ"},
        {"title": "I'm Callin'", "audio_url": "https://open.spotify.com/album/0u14DjLpxYnzJzHdnV1Ez1"}
    ]

    default_singles = [
        {"title": "Medusa", "audio_url": "https://open.spotify.com/track/2tYZv2w593ANPrz1HZhp55"},
        {"title": "Stamina", "audio_url": "https://open.spotify.com/track/3b3VmMwvuKGPDNcUdYmLBh"},
        {"title": "I'm Callin'", "audio_url": "https://open.spotify.com/album/0u14DjLpxYnzJzHdnV1Ez1"},
        {"title": "Midnight Gold", "audio_url": "https://open.spotify.com/track/0shpPfrxAqZgu2bpeKo86E"},
        {"title": "Velvet Dreams", "audio_url": "https://open.spotify.com/track/58P64V8UDPqOOmlXJpYLfn"}
    ]

    display_eps = eps if eps and len(eps) >= 1 else default_eps
    display_singles = singles if singles and len(singles) >= 1 else default_singles

    return render_template('music.html', title="Music", eps=display_eps, singles=display_singles)

@app.route('/gallery')
def gallery():
    gallery_dir = os.path.join(app.root_path, 'static', 'images', 'gallery')
    images = []
    if os.path.exists(gallery_dir):
        images = [f for f in sorted(os.listdir(gallery_dir)) if f.lower().endswith(('.jpeg', '.jpg', '.png', '.webp'))]
    if not images:
        images = [
            'WhatsApp_Image_2026-10-30_at_07_48_37.jpeg',
            'WhatsApp_Image_2026-10-30_at_07_48_38.jpeg',
            'WhatsApp_Image_2026-10-30_at_07_48_38__1_.jpeg',
            'WhatsApp_Image_2026-10-30_at_07_48_39.jpeg',
            'WhatsApp_Image_2026-10-30_at_07_48_39__1_.jpeg',
            'WhatsApp_Image_2026-10-30_at_07_48_39__2_.jpeg',
            'WhatsApp_Image_2026-10-30_at_07_48_39__3_.jpeg',
            'WhatsApp_Image_2026-10-30_at_07_48_39__4_.jpeg'
        ]
    return render_template('gallery.html', title="Gallery", images=images)

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
    # Admin dashboard logic (combining both admin logic)
    if request.method == 'POST':
        # Default admin post logic - not sure specifically what this form does based on snippet, 
        # but kept from HEAD lines 48-57 which handled adding products without image?
        # Leaving as is but maybe redirect to add-merch
        pass
        
    return render_template('admin.html')

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
    latest_video_id = db.Column(db.String(50), nullable=True, default='puw1cc7-2ZY')
    

def sync_latest_youtube_video():
    try:
        url = "https://www.youtube.com/playlist?list=UUDew3CMxwN0A7VRLHOwXLBw"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode('utf-8')
        vids = re.findall(r'/watch\?v=([a-zA-Z0-9_-]{11})', html)
        unique_vids = list(dict.fromkeys(vids))
        if unique_vids:
            latest_id = unique_vids[0]
            settings = Settings.query.first()
            if not settings:
                settings = Settings(artist_id='1j1fZpqk1Rov3O8bLIxvGL', latest_video_id=latest_id)
                db.session.add(settings)
            else:
                settings.latest_video_id = latest_id
            db.session.commit()
            return True, latest_id
    except Exception as e:
        db.session.rollback()
        return False, str(e)
    return False, "No videos found"

def sync_spotify_music():
    try:
        settings = Settings.query.first()
        artist_id = (settings.artist_id if settings and settings.artist_id else None) or os.environ.get('SPOTIFY_ARTIST_ID') or '1j1fZpqk1Rov3O8bLIxvGL'
        auth_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        # 1. Fetch EPs / Albums (keep latest 5, rolling off older ones)
        album_results = sp.artist_albums(artist_id, album_type='album', limit=10)
        ep_items = sorted(album_results.get('items', []), key=lambda x: x.get('release_date', ''), reverse=True)[:5]
        
        # 2. Fetch Singles (keep latest 5, rolling off older ones)
        single_results = sp.artist_albums(artist_id, album_type='single', limit=10)
        single_items = sorted(single_results.get('items', []), key=lambda x: x.get('release_date', ''), reverse=True)[:5]
        
        if not ep_items and not single_items:
            return False, "No releases found for this Artist ID on Spotify."
            
        # Update EPs: maintain strictly 5
        if ep_items:
            Track.query.filter_by(release_type='ep').delete()
            for ep in ep_items:
                t = Track(
                    title=ep['name'],
                    audio_url=ep['external_urls']['spotify'],
                    release_type='ep',
                    release_date=ep.get('release_date', ''),
                    is_new_release=False
                )
                db.session.add(t)

        # Update Singles: maintain strictly 5
        if single_items:
            Track.query.filter_by(release_type='single').delete()
            for idx, s in enumerate(single_items):
                t = Track(
                    title=s['name'],
                    audio_url=s['external_urls']['spotify'],
                    release_type='single',
                    release_date=s.get('release_date', ''),
                    is_new_release=(idx == 0) # Flag latest single for homepage
                )
                db.session.add(t)
                
        db.session.commit()
        return True, f"Successfully synced {len(ep_items)} EPs and {len(single_items)} Singles from Spotify."
    except Exception as e:
        db.session.rollback()
        return False, str(e)

@app.route('/admin/sync-spotify', methods=['POST'])
@login_required
def sync_spotify_route():
    success, msg = sync_spotify_music()
    yt_success, yt_msg = sync_latest_youtube_video()
    print(f"Spotify Sync: {success} - {msg}")
    print(f"YouTube Sync: {yt_success} - {yt_msg}")
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

@app.route('/api/cron/sync', methods=['GET'])
def cron_sync():
    # Check for authentication (Vercel Cron Secret)
    cron_secret = os.environ.get('CRON_SECRET')
    if cron_secret:
        auth_header = request.headers.get('Authorization')
        # Vercel sends: Authorization: Bearer <CRON_SECRET>
        if not auth_header or auth_header != f"Bearer {cron_secret}":
             return jsonify({'error': 'Unauthorized'}), 401
    
    success, msg = sync_spotify_music()
    yt_success, yt_msg = sync_latest_youtube_video()
    return jsonify({
        'spotify': {'success': success, 'message': msg},
        'youtube': {'success': yt_success, 'message': yt_msg}
    })


# Run this once in python console to create: db.create_all()

# Database initialization for Vercel/Production
try:
    with app.app_context():
        db.create_all()
        with db.engine.connect() as conn:
            try:
                conn.execute(db.text("ALTER TABLE track ADD COLUMN release_type VARCHAR(20) DEFAULT 'single'"))
                conn.commit()
            except Exception:
                pass
            try:
                conn.execute(db.text("ALTER TABLE track ADD COLUMN release_date VARCHAR(20)"))
                conn.commit()
            except Exception:
                pass
            try:
                conn.execute(db.text("ALTER TABLE settings ADD COLUMN latest_video_id VARCHAR(50) DEFAULT 'puw1cc7-2ZY'"))
                conn.commit()
            except Exception:
                pass
except Exception as e:
    print(f"Database initialization skipped or failed: {e}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
