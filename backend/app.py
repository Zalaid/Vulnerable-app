import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from config.db import init_db
from routes.auth_routes import router

PORT = int(os.environ.get('PORT', 3001))
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend')

# Vuln #3: Weak session secret - hardcoded and predictable
# Vuln #3: No secure/httponly flags on cookies
SECRET_KEY = "super-secret-key-12345"  # Hardcoded, easy to guess

app = FastAPI()

# Vuln #3: Session middleware with weak secret
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.include_router(router)
app.mount('/css', StaticFiles(directory=os.path.join(FRONTEND_DIR, 'css')), name='css')

if __name__ == '__main__':
    import uvicorn
    init_db()
    uvicorn.run('app:app', host='0.0.0.0', port=PORT, reload=False)
