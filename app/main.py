from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="Moonshine Ballad API",
    description="API RESTful para el e-commerce de whiskies finos y destilados artesanales.",
    version="1.0.0"
)

@app.get("/", tags=["HealthCheck"])
def read_root():
    return {
        "status": "online",
        "app": "Moonshine Ballad API",
        "database": "TiDB Cloud (Connected)"
    }