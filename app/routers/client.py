from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.core.deps import get_db

router = APIRouter(prefix="/catalogo", tags=["Catálogo Cliente"])

class VentaItem(BaseModel):
    id_producto: int
    cantidad: int = Field(gt=0)

class VentaCreate(BaseModel):
    id_cliente: int
    items: list[VentaItem] = Field(min_length=1)
    metodo_pago: str = "Demo"

@router.get("/whiskies")
def obtener_whiskies(
    categoria: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = text("""
        SELECT p.id_producto, p.nombre, p.descripcion, p.imagen_url, p.precio, p.stock,
               p.abv, p.volumen_ml, p.id_categoria_fk, p.id_marca_fk,
               p.id_proveedor_fk, c.nombre_categoria AS categoria, m.nombre AS marca
        FROM productos p
        JOIN categorias c ON p.id_categoria_fk = c.id_categoria
        JOIN marcas m ON p.id_marca_fk = m.id_marca;
    """)
    if categoria:
        query = text(str(query).replace(";", "") + " WHERE c.nombre_categoria = :categoria")
        result = db.execute(query, {"categoria": categoria})
    else:
        result = db.execute(query)
    return [dict(row._mapping) for row in result]


@router.get("/usuarios")
def obtener_usuarios(
    rol: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = text("""
        SELECT u.id_usuario, u.nombre, u.apellido, u.email, u.id_rol_fk,
               r.nombre AS rol
        FROM usuarios u
        JOIN roles r ON r.id_rol = u.id_rol_fk
        WHERE (:rol IS NULL OR LOWER(r.nombre) = LOWER(:rol))
        ORDER BY u.apellido, u.nombre
    """)
    return [dict(row._mapping) for row in db.execute(query, {"rol": rol})]


@router.post("/ventas", status_code=201)
def crear_venta(datos: VentaCreate, db: Session = Depends(get_db)):
    customer = db.execute(text("""
        SELECT u.id_usuario, u.id_domicilio_fk
        FROM usuarios u
        JOIN roles r ON r.id_rol = u.id_rol_fk
        WHERE u.id_usuario = :id_cliente AND LOWER(r.nombre) = 'cliente'
    """), {"id_cliente": datos.id_cliente}).mappings().first()
    if customer is None:
        raise HTTPException(status_code=400, detail="El cliente seleccionado no es válido")

    quantities: dict[int, int] = {}
    for item in datos.items:
        quantities[item.id_producto] = quantities.get(item.id_producto, 0) + item.cantidad

    try:
        for product_id, quantity in quantities.items():
            product = db.execute(text("""
                SELECT id_producto, stock
                FROM productos
                WHERE id_producto = :id_producto
                FOR UPDATE
            """), {"id_producto": product_id}).mappings().first()
            if product is None:
                raise HTTPException(status_code=404, detail=f"Producto {product_id} no encontrado")
            if product["stock"] < quantity:
                raise HTTPException(
                    status_code=409,
                    detail=f"Stock insuficiente para el producto {product_id}",
                )

        sale = db.execute(text("""
            INSERT INTO ventas
              (id_cliente_fk, id_domicilio_envio_fk, metodo_pago, estado)
            VALUES
              (:id_cliente, :id_domicilio, :metodo_pago, 'Pendiente')
        """), {
            "id_cliente": datos.id_cliente,
            "id_domicilio": customer["id_domicilio_fk"],
            "metodo_pago": datos.metodo_pago,
        })
        sale_id = sale.lastrowid

        for product_id, quantity in quantities.items():
            db.execute(text("""
                INSERT INTO detalle_ventas (id_venta_fk, id_producto_fk, cantidad)
                VALUES (:id_venta, :id_producto, :cantidad)
            """), {
                "id_venta": sale_id,
                "id_producto": product_id,
                "cantidad": quantity,
            })
            db.execute(text("""
                UPDATE productos
                SET stock = stock - :cantidad
                WHERE id_producto = :id_producto
            """), {"cantidad": quantity, "id_producto": product_id})

        db.commit()
        return {"id_venta": sale_id, "mensaje": "Venta registrada correctamente"}
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="No se pudo registrar la venta")