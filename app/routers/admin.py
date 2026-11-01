from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.deps import get_db

router = APIRouter(prefix="/admin", tags=["Administración"])

@router.post("/productos")
def agregar_producto(datos: dict, db: Session = Depends(get_db)):
    query = text("""
        INSERT INTO productos (id_categoria_fk, id_marca_fk, nombre, precio, stock, abv, volumen_ml)
        VALUES (:id_categoria, :id_marca, :nombre, :precio, :stock, :abv, :volumen)
    """)
    db.execute(query, datos)
    db.commit()
    return {"mensaje": "Producto agregado al catálogo"}