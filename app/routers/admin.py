from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.deps import get_db
from app.schemas.product import ProductoCreate, ProductoResponse

router = APIRouter(prefix="/admin", tags=["Administración"])

class CategoriaCreate(BaseModel):
    nombre_categoria: str = Field(min_length=1, max_length=30)
    descripcion: str | None = None

class MarcaCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=30)
    pais_origen: str = Field(min_length=1, max_length=30)

class UsuarioAdminCreate(BaseModel):
    id_rol_fk: int
    dni: str = Field(min_length=1, max_length=20)
    nombre: str = Field(min_length=1, max_length=30)
    apellido: str = Field(min_length=1, max_length=30)
    email: EmailStr
    tel_movil: str | None = None
    ciudad: str = Field(min_length=1, max_length=30)
    provincia: str = Field(min_length=1, max_length=30)
    codigo_postal: str = Field(min_length=1, max_length=15)
    calle: str = Field(min_length=1, max_length=50)
    numero: str = Field(min_length=1, max_length=10)

class UsuarioUpdate(BaseModel):
    id_rol_fk: int
    nombre: str = Field(min_length=1, max_length=30)
    apellido: str = Field(min_length=1, max_length=30)
    email: EmailStr
    tel_movil: str | None = None

@router.get("/productos")
def listar_productos(db: Session = Depends(get_db)):
    query = text("""
        SELECT p.id_producto, p.nombre, p.descripcion, p.precio, p.stock,
               p.abv, p.volumen_ml, p.id_categoria_fk, p.id_marca_fk,
               p.id_proveedor_fk, c.nombre_categoria AS categoria, m.nombre AS marca
        FROM productos p
        JOIN categorias c ON p.id_categoria_fk = c.id_categoria
        JOIN marcas m ON p.id_marca_fk = m.id_marca
        ORDER BY p.id_producto DESC
    """)
    return [dict(row._mapping) for row in db.execute(query)]


@router.get("/opciones")
def opciones_admin(db: Session = Depends(get_db)):
    categorias = db.execute(text(
        "SELECT id_categoria, nombre_categoria, descripcion FROM categorias ORDER BY nombre_categoria"
    ))
    marcas = db.execute(text(
        "SELECT id_marca, nombre, pais_origen FROM marcas ORDER BY nombre"
    ))
    admins = db.execute(text("""
        SELECT u.id_usuario, u.nombre, u.apellido, u.email, u.id_rol_fk, r.nombre AS rol
        FROM usuarios u JOIN roles r ON r.id_rol = u.id_rol_fk
        WHERE LOWER(r.nombre) = 'admin' ORDER BY u.apellido, u.nombre
    """))
    clientes = db.execute(text("""
        SELECT u.id_usuario, u.nombre, u.apellido, u.email, u.id_rol_fk, r.nombre AS rol
        FROM usuarios u JOIN roles r ON r.id_rol = u.id_rol_fk
        WHERE LOWER(r.nombre) = 'cliente' ORDER BY u.apellido, u.nombre
    """))
    return {
        "categorias": [dict(row._mapping) for row in categorias],
        "marcas": [dict(row._mapping) for row in marcas],
        "admins": [dict(row._mapping) for row in admins],
        "clientes": [dict(row._mapping) for row in clientes],
    }


@router.get("/usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT u.id_usuario, u.id_rol_fk, r.nombre AS rol, u.dni,
               u.nombre, u.apellido, u.email, u.tel_movil
        FROM usuarios u JOIN roles r ON r.id_rol = u.id_rol_fk
        ORDER BY u.apellido, u.nombre
    """))
    return [dict(row._mapping) for row in result]


@router.get("/categorias")
def listar_categorias(db: Session = Depends(get_db)):
    result = db.execute(text(
        "SELECT id_categoria, nombre_categoria, descripcion FROM categorias ORDER BY nombre_categoria"
    ))
    return [dict(row._mapping) for row in result]


@router.get("/marcas")
def listar_marcas(db: Session = Depends(get_db)):
    result = db.execute(text(
        "SELECT id_marca, nombre, pais_origen FROM marcas ORDER BY nombre"
    ))
    return [dict(row._mapping) for row in result]


@router.post("/categorias", status_code=201)
def agregar_categoria(datos: CategoriaCreate, db: Session = Depends(get_db)):
    db.execute(text("""
        INSERT INTO categorias (nombre_categoria, descripcion)
        VALUES (:nombre_categoria, :descripcion)
    """), datos.model_dump())
    db.commit()
    return {"mensaje": "Categoría creada correctamente"}


@router.post("/marcas", status_code=201)
def agregar_marca(datos: MarcaCreate, db: Session = Depends(get_db)):
    db.execute(text("""
        INSERT INTO marcas (nombre, pais_origen)
        VALUES (:nombre, :pais_origen)
    """), datos.model_dump())
    db.commit()
    return {"mensaje": "Marca creada correctamente"}


@router.post("/usuarios", status_code=201)
def agregar_usuario(datos: UsuarioAdminCreate, db: Session = Depends(get_db)):
    values = datos.model_dump()
    db.execute(text("""
        INSERT INTO codigos_postales (codigo_postal, ciudad, provincia)
        VALUES (:codigo_postal, :ciudad, :provincia)
        ON DUPLICATE KEY UPDATE ciudad = VALUES(ciudad), provincia = VALUES(provincia)
    """), values)
    address = db.execute(text("""
        INSERT INTO domicilios (cod_postal_fk, calle, numero)
        VALUES (:codigo_postal, :calle, :numero)
    """), values)
    values["id_domicilio_fk"] = address.lastrowid
    db.execute(text("""
        INSERT INTO usuarios
          (id_rol_fk, id_domicilio_fk, dni, nombre, apellido, email, tel_movil)
        VALUES
          (:id_rol_fk, :id_domicilio_fk, :dni, :nombre, :apellido, :email, :tel_movil)
    """), values)
    db.commit()
    return {"mensaje": "Usuario creado correctamente"}


@router.put("/usuarios/{usuario_id}")
def actualizar_usuario(usuario_id: int, datos: UsuarioUpdate, db: Session = Depends(get_db)):
    values = datos.model_dump()
    values["usuario_id"] = usuario_id
    if db.execute(text("SELECT 1 FROM usuarios WHERE id_usuario = :id"), {"id": usuario_id}).first() is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.execute(text("""
        UPDATE usuarios
        SET id_rol_fk = :id_rol_fk, nombre = :nombre, apellido = :apellido,
            email = :email, tel_movil = :tel_movil
        WHERE id_usuario = :usuario_id
    """), values)
    db.commit()
    return {"mensaje": "Usuario actualizado correctamente"}


@router.put("/categorias/{categoria_id}")
def actualizar_categoria(categoria_id: int, datos: CategoriaCreate, db: Session = Depends(get_db)):
    values = datos.model_dump()
    values["categoria_id"] = categoria_id
    if db.execute(text("SELECT 1 FROM categorias WHERE id_categoria = :id"), {"id": categoria_id}).first() is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.execute(text("""
        UPDATE categorias
        SET nombre_categoria = :nombre_categoria, descripcion = :descripcion
        WHERE id_categoria = :categoria_id
    """), values)
    db.commit()
    return {"mensaje": "Categoría actualizada correctamente"}


@router.put("/marcas/{marca_id}")
def actualizar_marca(marca_id: int, datos: MarcaCreate, db: Session = Depends(get_db)):
    values = datos.model_dump()
    values["marca_id"] = marca_id
    if db.execute(text("SELECT 1 FROM marcas WHERE id_marca = :id"), {"id": marca_id}).first() is None:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    db.execute(text("""
        UPDATE marcas
        SET nombre = :nombre, pais_origen = :pais_origen
        WHERE id_marca = :marca_id
    """), values)
    db.commit()
    return {"mensaje": "Marca actualizada correctamente"}


@router.post("/productos", response_model=ProductoResponse, status_code=201)
def agregar_producto(datos: ProductoCreate, db: Session = Depends(get_db)):
    query = text("""
        INSERT INTO productos
          (id_categoria_fk, id_marca_fk, id_proveedor_fk, nombre, descripcion,
           precio, stock, abv, volumen_ml)
        VALUES
          (:id_categoria_fk, :id_marca_fk, :id_proveedor_fk, :nombre, :descripcion,
           :precio, :stock, :abv, :volumen_ml)
    """)
    result = db.execute(query, datos.model_dump())
    db.commit()
    product_id = result.lastrowid
    product = db.execute(
        text("SELECT * FROM productos WHERE id_producto = :id"),
        {"id": product_id},
    ).mappings().one()
    return dict(product)


@router.put("/productos/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(
    producto_id: int,
    datos: ProductoCreate,
    db: Session = Depends(get_db),
):
    values = datos.model_dump()
    values["producto_id"] = producto_id
    exists = db.execute(
        text("SELECT 1 FROM productos WHERE id_producto = :id"),
        {"id": producto_id},
    ).first()
    if exists is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.execute(text("""
        UPDATE productos
        SET id_categoria_fk = :id_categoria_fk, id_marca_fk = :id_marca_fk,
            id_proveedor_fk = :id_proveedor_fk, nombre = :nombre,
            descripcion = :descripcion, precio = :precio, stock = :stock,
            abv = :abv, volumen_ml = :volumen_ml
        WHERE id_producto = :producto_id
    """), values)
    db.commit()
    product = db.execute(
        text("SELECT * FROM productos WHERE id_producto = :id"),
        {"id": producto_id},
    ).mappings().one()
    return dict(product)