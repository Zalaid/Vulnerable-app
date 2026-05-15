# Vulnerable App

An intentionally vulnerable web application designed to teach common security vulnerabilities through hands-on exploitation. Rather than studying vulnerabilities in theory, you'll exploit them in a working application to understand how real attacks work.

**Warning:** This application is deliberately insecure. It is designed for educational use only and should never be deployed to production or used on systems you don't own.


## Overview

This project consists of a simple authentication system with 6 intentional security flaws:

1. **SQL Injection** - Database queries vulnerable to input manipulation
2. **Stored XSS** - Persistent JavaScript injection stored in the database
3. **Reflected XSS** - JavaScript injection through URL parameters
4. **Session Hijacking** - Weak session management allowing credential theft
5. **Plaintext Passwords** - Passwords stored without encryption
6. **No Rate Limiting** - Unlimited login attempts enabling brute force attacks

The application is built with FastAPI and SQLite, making it simple enough to understand but realistic enough to demonstrate actual attack techniques.

## Getting Started

### Prerequisites

- Python 3.9 or later
- Git (optional, for cloning the repository)

### Installation

Clone the repository:
```bash
git clone <repository-url>
cd "Vulnerable app"
```

Navigate to the backend directory:
```bash
cd backend
```

Install the project manager:
```bash
pip install uv
```

Create and activate the virtual environment with dependencies:
```bash
uv sync
```

**On Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
.venv\Scripts\activate.bat
```

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

### Running the Application

```bash
python app.py
```

The application will start on `http://localhost:3001`. Open this URL in your browser to access the login page.

## Learning Path

**Read the exploitation guide first:** Open `EXPLOITS.md` in the root directory. This document walks through each vulnerability with step-by-step instructions for exploiting it. No prior security knowledge is required.

**Then explore the code:** After exploiting a vulnerability, examine the relevant source files to understand why it was vulnerable. The main logic is in `backend/controllers/auth_controller.py` and `backend/routes/auth_routes.py`.

**Finally, fix it:** The most valuable exercise is to modify the code to patch each vulnerability. Use secure coding practices like parameterized queries, output escaping, password hashing, and input validation.

## Project Structure

```
backend/
├── app.py                    FastAPI application entry point
├── pyproject.toml            Project configuration and dependencies
├── config/
│   └── db.py                 Database connection and initialization
├── routes/
│   └── auth_routes.py         HTTP route handlers (includes protected /welcome route)
└── controllers/
    └── auth_controller.py     Business logic for authentication

frontend/
├── signup.html
├── login.html
├── welcome.html              Protected page (requires valid session)
├── images/
│   ├── brand.svg             Logo displayed on top right
│   └── datasciene-logo.jpg   Logo displayed on top left
└── css/
    └── styles.css            Modern styling with gradient design
```

## Useful Commands

Install or update dependencies:
```bash
uv sync
```

Check the SQLite database:
```bash
sqlite3 vulnerable_app.db
sqlite> SELECT * FROM users;
sqlite> .exit
```

Test the application is running:
```bash
curl http://localhost:3001
```

Deactivate the virtual environment:
```bash
deactivate
```

## Technology Stack

- **Backend Framework:** FastAPI
- **Application Server:** Uvicorn
- **Database:** SQLite3
- **Frontend:** HTML/CSS
- **Python Version:** 3.9+

## Educational Context

These vulnerabilities are relevant to:

- **OWASP Top 10** - The industry standard list of critical web vulnerabilities
- **Security certifications** including CompTIA Security+, CEH, and eJPT
- **Real-world security** - These same vulnerabilities are found in production applications and exploited by attackers
- **Bug bounty programs** - Understanding these basics is essential for vulnerability research

## Troubleshooting

**"python command not found"**
- Install Python 3.9+ from https://www.python.org/downloads/

**"uv command not found"**
- Run `pip install uv`

**"Port 3001 already in use"**
- Edit `backend/app.py` and change the PORT value on line 11

**"Database file not found"**
- The database is created automatically when you run the application for the first time

**"Virtual environment won't activate"**
- Ensure you are in the `backend/` directory before running the activation command
- On Windows, you may need to adjust PowerShell execution policy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

## Legal Notice

This application is provided strictly for educational purposes. Unauthorized access to computer systems is illegal. Ensure you have explicit permission before testing security vulnerabilities on any system you do not own. The authors are not responsible for misuse of this project.

## License

Educational use only.
