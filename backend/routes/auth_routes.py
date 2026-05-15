import os
from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse, FileResponse, JSONResponse, HTMLResponse
from controllers.auth_controller import signup as do_signup, login as do_login
from config.db import get_db

# Get absolute path to frontend directory
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BACKEND_DIR)
FRONTEND_DIR = os.path.join(PROJECT_DIR, 'frontend')
router = APIRouter()

@router.get('/')
def index():
    return RedirectResponse('/signup', status_code=302)

@router.get('/signup')
def signup_page():
    return FileResponse(os.path.join(FRONTEND_DIR, 'signup.html'))

@router.post('/signup')
def signup_post(username: str = Form(None), email: str = Form(None), password: str = Form(None)):
    return do_signup(username, email, password)

@router.get('/login')
def login_page():
    return FileResponse(os.path.join(FRONTEND_DIR, 'login.html'))

@router.post('/login')
def login_post(request: Request, username: str = Form(None), password: str = Form(None)):
    return do_login(request, username, password)

# Vuln: Database download endpoint (simulates server misconfiguration)
# In real apps: backup files, database exports, git repos, etc. can be accidentally exposed
@router.get('/download/db')
def download_db():
    """
    Vuln: Exposed database download
    In real scenarios this happens via:
    - Misconfigured web server (serving /backups, /.git, etc.)
    - Exposed S3 buckets
    - Server info disclosure
    - Directory traversal vulnerabilities
    """
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'vulnerable_app.db')
    return FileResponse(path=db_path, filename='vulnerable_app.db')

# Vuln: Search endpoint vulnerable to Reflected XSS and SQL Injection
@router.get('/search')
def search_user(q: str = None):
    """Vuln: Reflected XSS - search query displayed without escaping"""
    if not q:
        return HTMLResponse('Error: Query parameter required')

    # Vuln #1: Raw string concatenation in LIKE clause (SQL Injection)
    query = "SELECT username, email FROM users WHERE username LIKE '%" + str(q) + "%' OR email LIKE '%" + str(q) + "%'"

    try:
        conn = get_db()
        cursor = conn.execute(query)
        results = cursor.fetchall()
        conn.close()

        # Vuln: Reflected XSS - user input reflected directly in HTML without escaping
        html = f"<h2>Search Results for: {q}</h2>"

        if results:
            html += "<ul>"
            for row in results:
                html += f"<li>{row[0]} ({row[1]})</li>"
            html += "</ul>"
        else:
            html += "<p>No users found matching your search.</p>"

        return HTMLResponse(html)
    except Exception as e:
        # Vuln #6: Error messages reveal SQL structure
        return HTMLResponse(f"<h2>Error</h2><p>{str(e)}</p>")

@router.get('/welcome')
def welcome_page(request: Request):
    """Protected welcome page - requires session"""
    if 'user_id' not in request.session:
        return RedirectResponse('/login', status_code=302)

    username = request.session.get('username', 'Unknown')

    with open(os.path.join(FRONTEND_DIR, 'welcome.html'), 'r', encoding='utf-8') as f:
        html = f.read()
    html = html.replace('{{username}}', username)
    return HTMLResponse(html)

@router.get('/logout')
def logout(request: Request):
    """Logout and clear session"""
    request.session.clear()
    return RedirectResponse('/login', status_code=302)
