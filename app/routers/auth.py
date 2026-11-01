from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.deps import get_db

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/register")
def registrar_usuario(datos: dict, db: Session = Depends(get_db)):
    # SQL puro para registrar un cliente en la BD
    query = text("""
        INSERT INTO usuarios (id_rol_fk, id_domicilio_fk, dni, nombre, apellido, email)
        VALUES (:rol, :domicilio, :dni, :nombre, :apellido, :email)
    """)
    # Ejecuta el INSERT en TiDB Cloud
    db.execute(query, datos)
    db.commit()
    return {"mensaje": "Usuario registrado exitosamente"}