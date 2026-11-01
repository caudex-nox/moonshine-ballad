from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.deps import get_db

router = APIRouter(prefix="/catalogo", tags=["Catálogo Cliente"])

@router.get("/whiskies")
def obtener_whiskies(db: Session = Depends(get_db)):
    # Consulta SQL con JOINs para mostrar el catálogo completo
    query = text("""
        SELECT p.id_producto, p.nombre, p.precio, p.stock, c.nombre_categoria, m.nombre AS marca
        FROM productos p
        JOIN categorias c ON p.id_categoria_fk = c.id_categoria
        JOIN marcas m ON p.id_marca_fk = m.id_marca;
    """)
    result = db.execute(query)
    return [dict(row._mapping) for row in result]