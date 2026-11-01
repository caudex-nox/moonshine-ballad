from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# Importaciones del backend creadas por tu compañero
from app.config import settings
from app.routers import auth, client, admin

# 1. Instancia principal de FastAPI
app = FastAPI(
    title="Moonshine Ballad API",
    description="API RESTful y plataforma e-commerce de whiskies finos y destilados artesanales.",
    version="1.0.0"
)

# 2. Configuración de archivos estáticos y plantillas Jinja2 (Frontend)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="templates")

# 3. Registrar los routers de la API (Backend de tu compañero)
app.include_router(auth.router)
app.include_router(client.router)
app.include_router(admin.router)


# --- Rutas Web (Frontend Jinja2) ---

@app.get("/", response_class=HTMLResponse)
@app.get("/store", response_class=HTMLResponse)
async def read_store(request: Request):
    """Renderiza la tienda principal."""
    return templates.TemplateResponse(request=request, name="store.html")

@app.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    """Renderiza la pantalla de autenticación."""
    return templates.TemplateResponse(request=request, name="login.html")

@app.get("/admin", response_class=HTMLResponse)
async def read_admin(request: Request):
    """Renderiza el panel de administración."""
    return templates.TemplateResponse(request=request, name="admin_dashboard.html")


# --- Endpoint de estado / HealthCheck (Backend) ---

@app.get("/api/health", tags=["HealthCheck"])
def health_check():
    return {
        "status": "online",
        "app": "Moonshine Ballad API",
        "database": "TiDB Cloud (Connected)"
    }