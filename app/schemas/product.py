from typing import Optional
from decimal import Decimal
from pydantic import BaseModel

# --- CATEGORIA ---
class CategoriaBase(BaseModel):
    nombre_categoria: str
    descripcion: Optional[str] = None

class CategoriaResponse(CategoriaBase):
    id_categoria: int

    class Config:
        from_attributes = True

# --- MARCA ---
class MarcaBase(BaseModel):
    nombre: str
    pais_origen: str

class MarcaResponse(MarcaBase):
    id_marca: int

    class Config:
        from_attributes = True

# --- PRODUCTO ---
class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: Decimal
    stock: int = 0
    abv: Decimal
    volumen_ml: int

class ProductoCreate(ProductoBase):
    id_categoria_fk: int
    id_marca_fk: int
    id_proveedor_fk: Optional[int] = None

class ProductoResponse(ProductoBase):
    id_producto: int
    id_categoria_fk: int
    id_marca_fk: int
    id_proveedor_fk: Optional[int]

    class Config:
        from_attributes = True