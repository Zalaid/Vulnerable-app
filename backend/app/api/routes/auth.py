"""
auth.py
HTTP route handlers for all application endpoints.
Handles authentication pages, form submissions, the user search endpoint,
the protected dashboard, and the database download route.
"""
import os
from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse
from app.services.auth_service import signup as do_signup, login as do_login
from app.db.session import get_db

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(_HERE))))
TEMPLATES_DIR = os.path.join(_PROJECT_ROOT, 'frontend', 'templates')

router = APIRouter()


@router.get('/')
def index():
    """Redirect the root URL to the signup page."""
    return RedirectResponse('/signup', status_code=302)


@router.get('/signup')
def signup_page():
    """Serve the user registration form."""
    return FileResponse(os.path.join(TEMPLATES_DIR, 'signup.html'))


@router.post('/signup')
def signup_post(username: str = Form(None), email: str = Form(None), password: str = Form(None)):
    """Process the registration form submission."""
    return do_signup(username, email, password)


@router.get('/login')
def login_page():
    """Serve the login form."""
    return FileResponse(os.path.join(TEMPLATES_DIR, 'login.html'))


@router.post('/login')
def login_post(request: Request, username: str = Form(None), password: str = Form(None)):
    """Process the login form submission."""
    return do_login(request, username, password)


@router.get('/download/db')
def download_db():
    """Serve the SQLite database file as a downloadable attachment."""
    db_path = os.path.join(_PROJECT_ROOT, 'vulnerable_app.db')
    return FileResponse(path=db_path, filename='vulnerable_app.db')


@router.get('/search')
def search_user(q: str = None):
    """Search users by username or email and return results as an HTML page."""
    if not q:
        return HTMLResponse('Error: Query parameter required')

    query = ("SELECT username, email FROM users WHERE username LIKE '%"
             + str(q) + "%' OR email LIKE '%" + str(q) + "%'")
    try:
        conn = get_db()
        results = conn.execute(query).fetchall()
        conn.close()

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
        return HTMLResponse(f"<h2>Error</h2><p>{str(e)}</p>")


@router.get('/welcome')
def welcome_page(request: Request):
    """Serve the dashboard; redirects to login if the session is not active."""
    if 'user_id' not in request.session:
        return RedirectResponse('/login', status_code=302)

    username = request.session.get('username', 'Unknown')
    with open(os.path.join(TEMPLATES_DIR, 'dashboard.html'), 'r', encoding='utf-8') as f:
        html = f.read()
    html = html.replace('{{username}}', username)
    return HTMLResponse(html)


@router.get('/logout')
def logout(request: Request):
    """Clear the user session and redirect to the login page."""
    request.session.clear()
    return RedirectResponse('/login', status_code=302)
