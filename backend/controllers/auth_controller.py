import os
import time
from fastapi import Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from config.db import get_db

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend')

def signup(username: str = Form(None), email: str = Form(None), password: str = Form(None)):
    if not username or not email or not password:
        return HTMLResponse('Error: All fields are required')

    # Validation - require reasonable length
    if len(username) < 3 or len(username) > 20:
        return HTMLResponse('Error: Username must be 3-20 characters')

    if len(password) < 8 or len(password) > 50:
        return HTMLResponse('Error: Password must be 8-50 characters')

    if '@' not in email or len(email) < 5:
        return HTMLResponse('Error: Invalid email format')

    # Vuln #1: SQL Injection - raw string concatenation (despite validation)
    # Attacker must craft proper SQL to exploit
    query = ("INSERT INTO users (username, email, password) VALUES ('"
             + str(username) + "', '" + str(email) + "', '" + str(password) + "')")
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
    if not username or not password:
        return HTMLResponse('Error: Invalid credentials. <a href="/login">Try again</a>')

    if len(username) < 3 or len(password) < 8:
        return HTMLResponse('Error: Invalid credentials. <a href="/login">Try again</a>')

    # Generic error - no user enumeration
    error_msg = 'Error: Invalid credentials. <a href="/login">Try again</a>'

    # Vuln #1: SQL Injection - raw string concatenation requires proper password match
    # Attacker needs to bypass BOTH username AND password check
    query = ("SELECT * FROM users WHERE username = '"
             + str(username) + "' AND password = '" + str(password) + "'")
    try:
        conn = get_db()
        user = conn.execute(query).fetchone()
        conn.close()
    except Exception as e:
        return HTMLResponse(error_msg)

    if user:
        # Vuln #3: Session management - stores username in plaintext in session
        # Vuln #3: Session secret is hardcoded and weak
        request.session['user_id'] = user['id']
        request.session['username'] = user['username']
        request.session['email'] = user['email']

        # Vuln #2: Stored XSS - username injected unescaped into HTML
        with open(os.path.join(FRONTEND_DIR, 'welcome.html'), 'r', encoding='utf-8') as f:
            html = f.read()
        # VULNERABLE: No HTML escaping - XSS happens here
        html = html.replace('{{username}}', user['username'])
        # Vuln #6: Information disclosure - email and timestamp in comments
        html = html + '\n<!-- User email: ' + user['email'] + ' | Login time: ' + str(time.time()) + ' -->'

        response = RedirectResponse('/dashboard', status_code=302)
        return response
    else:
        return HTMLResponse(error_msg)
