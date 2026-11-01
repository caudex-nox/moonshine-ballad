from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id_categoria = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_categoria = Column(String(30), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)

    productos = relationship("Producto", back_populates="categoria")


class Marca(Base):
    __tablename__ = "marcas"

    id_marca = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(30), unique=True, nullable=False)
    pais_origen = Column(String(30), nullable=False)

    productos = relationship("Producto", back_populates="marca")


class Proveedor(Base):
    __tablename__ = "proveedores"

    id_proveedor = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_domicilio_fk = Column(Integer, ForeignKey("domicilios.id_domicilio"), nullable=True)
    razon_social = Column(String(30), nullable=False)
    cuit = Column(String(20), unique=True, nullable=False)
    email = Column(String(40), nullable=False)
    tel_fijo = Column(String(20), nullable=True)
    tel_movil = Column(String(20), nullable=True)

    domicilio = relationship("Domicilio", back_populates="proveedores")
    productos = relationship("Producto", back_populates="proveedor")


class Producto(Base):
    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_categoria_fk = Column(Integer, ForeignKey("categorias.id_categoria"), nullable=False)
    id_marca_fk = Column(Integer, ForeignKey("marcas.id_marca"), nullable=False)
    id_proveedor_fk = Column(Integer, ForeignKey("proveedores.id_proveedor"), nullable=True)
    nombre = Column(String(30), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    abv = Column(Numeric(4, 1), nullable=False)
    volumen_ml = Column(Integer, nullable=False)

    categoria = relationship("Categoria", back_populates="productos")
    marca = relationship("Marca", back_populates="productos")
    proveedor = relationship("Proveedor", back_populates="productos")
    detalles_venta = relationship("DetalleVenta", back_populates="producto")


class Venta(Base):
    __tablename__ = "ventas"

    id_venta = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_cliente_fk = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_empleado_fk = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)
    id_domicilio_envio_fk = Column(Integer, ForeignKey("domicilios.id_domicilio"), nullable=False)
    fecha_venta = Column(DateTime, server_default=func.now(), nullable=False)
    metodo_pago = Column(String(30), nullable=False)
    estado = Column(String(20), default="Pendiente", nullable=False)

    cliente = relationship("Usuario", foreign_keys=[id_cliente_fk], back_populates="ventas_cliente")
    empleado = relationship("Usuario", foreign_keys=[id_empleado_fk], back_populates="ventas_empleado")
    domicilio_envio = relationship("Domicilio", back_populates="ventas_envio")
    detalles = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")


class DetalleVenta(Base):
    __tablename__ = "detalle_ventas"

    id_detalle = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_venta_fk = Column(Integer, ForeignKey("ventas.id_venta", ondelete="CASCADE"), nullable=False)
    id_producto_fk = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    cantidad = Column(Integer, nullable=False)

    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_venta")