from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Rol(Base):
    __tablename__ = "roles"

    id_rol = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(30), unique=True, nullable=False)

    usuarios = relationship("Usuario", back_populates="rol")


class CodigoPostal(Base):
    __tablename__ = "codigos_postales"

    codigo_postal = Column(String(15), primary_key=True, index=True)
    ciudad = Column(String(30), nullable=False)
    provincia = Column(String(30), nullable=False)

    domicilios = relationship("Domicilio", back_populates="codigo_postal_rel")


class Domicilio(Base):
    __tablename__ = "domicilios"

    id_domicilio = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cod_postal_fk = Column(String(15), ForeignKey("codigos_postales.codigo_postal"), nullable=False)
    calle = Column(String(50), nullable=False)
    numero = Column(String(10), nullable=False)
    piso = Column(String(10), nullable=True)
    dpto = Column(String(10), nullable=True)

    codigo_postal_rel = relationship("CodigoPostal", back_populates="domicilios")
    usuarios = relationship("Usuario", back_populates="domicilio")
    proveedores = relationship("Proveedor", back_populates="domicilio")
    ventas_envio = relationship("Venta", back_populates="domicilio_envio")


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_rol_fk = Column(Integer, ForeignKey("roles.id_rol"), nullable=False)
    id_domicilio_fk = Column(Integer, ForeignKey("domicilios.id_domicilio"), nullable=False)
    dni = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(30), nullable=False)
    apellido = Column(String(30), nullable=False)
    email = Column(String(40), unique=True, nullable=False)
    tel_fijo = Column(String(20), nullable=True)
    tel_movil = Column(String(20), nullable=True)
    legajo = Column(String(20), unique=True, nullable=True)
    cargo = Column(String(30), nullable=True)

    rol = relationship("Rol", back_populates="usuarios")
    domicilio = relationship("Domicilio", back_populates="usuarios")
    ventas_cliente = relationship("Venta", foreign_keys="[Venta.id_cliente_fk]", back_populates="cliente")
    ventas_empleado = relationship("Venta", foreign_keys="[Venta.id_empleado_fk]", back_populates="empleado")