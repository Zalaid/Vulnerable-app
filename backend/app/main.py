"""
main.py
Application entry point. Configures the FastAPI instance, registers session
middleware, mounts static file directories, and starts the Uvicorn server.
"""
import sys
import os

# Ensure the backend directory is on the path so app.* packages are importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from app.db.session import init_db
from app.api.routes.auth import router

PORT = int(os.environ.get('PORT', 3001))

_HERE = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(_HERE)
PROJECT_DIR = os.path.dirname(BACKEND_DIR)
FRONTEND_DIR = os.path.join(PROJECT_DIR, 'frontend')

SECRET_KEY = "super-secret-key-12345"

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.include_router(router)
app.mount('/static/css', StaticFiles(directory=os.path.join(FRONTEND_DIR, 'static', 'css')), name='css')
app.mount('/static/images', StaticFiles(directory=os.path.join(FRONTEND_DIR, 'static', 'images')), name='images')

if __name__ == '__main__':
    import uvicorn
    init_db()
    uvicorn.run('app.main:app', host='0.0.0.0', port=PORT, reload=False)
