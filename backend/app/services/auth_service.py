"""
auth_service.py
Business logic for user registration and authentication.
Validates input, constructs database queries, manages session state on login,
and returns appropriate HTTP responses.
"""
import os
from fastapi import Form, Request
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from app.db.session import get_db
from app.core.security import hash_password

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
TEMPLATES_DIR = os.path.join(_PROJECT_ROOT, 'frontend', 'templates')


def signup(username: str = Form(None), email: str = Form(None), password: str = Form(None)):
    """Register a new user by inserting hashed credentials into the database."""
    if not username or not email or not password:
        return HTMLResponse('Error: All fields are required')

    hashed = hash_password(str(password))

    query = ("INSERT INTO users (username, email, password) VALUES ('"
             + str(username) + "', '" + str(email) + "', '" + hashed + "')")
    try:
        conn = get_db()
        conn.execute(query)
        conn.commit()
        conn.close()
    except Exception as e:
        if 'UNIQUE' in str(e) or 'duplicate' in str(e).lower():
            return HTMLResponse('Error: Username already exists')
        return HTMLResponse('Error: Registration failed')

    return RedirectResponse('/login', status_code=302)


def login(request: Request, username: str = Form(None), password: str = Form(None)):
    """Authenticate a user and establish a session on success.

    Returns a 401 JSON response on failure so the frontend can display
    the error message inline without a full page reload.
    """
    if not username or not password:
        return JSONResponse({'error': 'Invalid credentials.'}, status_code=401)

    hashed = hash_password(str(password))

    query = ("SELECT * FROM users WHERE username = '"
             + str(username) + "' AND password = '" + hashed + "'")
    try:
        conn = get_db()
        user = conn.execute(query).fetchone()
        conn.close()
    except Exception:
        return JSONResponse({'error': 'Invalid credentials.'}, status_code=401)

    if user:
        request.session['user_id'] = user['id']
        request.session['username'] = user['username']
        request.session['email'] = user['email']
        return RedirectResponse('/welcome', status_code=302)

    return JSONResponse({'error': 'Invalid credentials.'}, status_code=401)
