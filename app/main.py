from fastapi import FastAPI
from app.config import settings
from app.routers import auth, client, admin

app = FastAPI(
    title="Moonshine Ballad API",
    description="API RESTful para el e-commerce de whiskies finos y destilados artesanales.",
    version="1.0.0"
)

# Registrar los routers de la aplicación
app.include_router(auth.router)
app.include_router(client.router)
app.include_router(admin.router)


@app.get("/", tags=["HealthCheck"])
def read_root():
    return {
        "status": "online",
        "app": "Moonshine Ballad API",
        "database": "TiDB Cloud (Connected)"
    }