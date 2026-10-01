# Rhymamusic

![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![Flask Framework](https://img.shields.io/badge/Framework-Flask_3.1-black?logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red?logo=sqlalchemy&logoColor=white)
![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20PostgreSQL-336791?logo=postgresql&logoColor=white)
![Spotify API](https://img.shields.io/badge/Integration-Spotify_Web_API-1DB954?logo=spotify&logoColor=white)
![Deployment](https://img.shields.io/badge/Deployment-Docker%20%7C%20Vercel-000000?logo=vercel&logoColor=white)
![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen)

High-end, minimalist music website and artist portal built with Python Flask, SQLAlchemy, and Server-Side Rendering (SSR).

---

## Architecture Overview

Rhymamusic is structured as a modular Flask web application providing server-rendered dynamic views, database persistence, external service synchronization, and administration controls:

```
[ Client Browser ] <-------------> [ Flask Application (app.py) ]
                                             |
                   +-------------------------+-------------------------+
                   |                         |                         |
         [ Jinja2 Templates ]      [ SQLAlchemy ORM ]         [ Spotify Web API ]
         (SSR HTML + Static)       (SQLite / PostgreSQL)      (Track & Release Sync)
```

- **Core Application Layer (`app.py`)**: Handles HTTP routing, user session state with `Flask-Login`, form handling, file upload validation, and scheduled synchronization endpoints.
- **Serverless Adapter (`index.py`)**: Exports WSGI application instance compatible with Vercel serverless runtimes.
- **Data Persistence Layer (`instance/site.db`)**: Manages relational records for tracks, releases, scheduled drops, admin credentials, and booking inquiries.
- **Third-Party Integrations**: Spotify Web API integration (`spotipy`) for syncing track data and discography.
- **Mobile Companion (`mobile/`)**: React Native / Expo application targeting mobile client experiences.

---

## Features

- **Server-Side Rendering (SSR)**: High-speed initial load and SEO optimization using Jinja2 templates.
- **Dynamic Discography & Music Hub**: Interactive showcase featuring top tracks, latest album drops, and release countdown timers.
- **Automated Spotify Sync**: Background endpoint (`/cron/sync`) protected with cron authorization tokens for syncing artist releases from Spotify.
- **Booking & Inquiry Pipeline**: Booking request form collecting prospective client details, dates, and event specifications.
- **Secure Admin Portal**: Protected management routes with `Flask-Login` authentication for content updates and inquiry reviews.
- **Containerized & Serverless Ready**: Full deployment compatibility for Docker (`Dockerfile`, `docker-compose.yml`) and Vercel (`vercel.json`).

---

## Directory Structure

```
rhymamusic/
├── .dockerignore              # Docker build exclusions
├── .gitignore                # Version control exclusions
├── Dockerfile                # Container image definition
├── README.md                 # Project architecture and documentation
├── app.py                    # Primary Flask application entry point
├── docker-compose.yml        # Multi-container orchestration configuration
├── index.py                  # WSGI entry point for Vercel serverless deployment
├── instance/                 # Local instance storage
│   └── site.db               # SQLite database file
├── mobile/                   # React Native / Expo mobile application
│   ├── App.js                # Mobile app root component
│   ├── app.json              # Expo application manifest
│   ├── eas.json              # EAS build profile configuration
│   ├── package.json          # Node dependencies and scripts
│   └── src/                  # Mobile source code
├── requirements.txt          # Python package dependencies
├── static/                   # Static assets
│   ├── css/                  # Custom CSS stylesheets
│   ├── images/               # Image assets
│   ├── js/                   # Client-side JavaScript
│   ├── manifest.json         # Web app manifest
│   └── uploads/              # Uploaded media assets (.gitkeep preserved)
├── templates/                # Jinja2 HTML templates
│   ├── about.html            # About artist page
│   ├── admin.html            # Administration dashboard
│   ├── base.html             # Base layout template
│   ├── bookings.html         # Booking inquiries form
│   ├── contact.html          # Contact form
│   ├── home.html             # Homepage landing view
│   ├── login.html            # Admin login view
│   ├── merch.html            # Merchandise store view
│   ├── music.html            # Discography and release list view
│   ├── privacy.html          # Privacy policy
│   └── terms.html            # Terms of service
└── vercel.json               # Vercel deployment routing and cron specs
```

---

## Setup and Installation

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Create Virtual Environment

Create an isolated Python virtual environment to manage dependencies locally:

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

*(If script execution is restricted on Windows, enable it for the current process: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`)*

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables (Optional)
Create a `.env` file or export environment variables as needed:

```bash
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///site.db
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:5000/callback
CRON_SECRET=your_cron_authorization_token
```

### 5. Run the Application
Start the Flask development server:

```bash
python app.py
```

Open your browser and navigate to:
```
http://localhost:5000
```

---

## Docker Execution

To build and run the application container with Docker:

```bash
docker compose up --build
```

The service will bind to port `5000` on your host machine.
