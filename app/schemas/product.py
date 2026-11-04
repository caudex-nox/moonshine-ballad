from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field

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
    nombre: str = Field(min_length=1, max_length=30)
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = Field(default=None, max_length=500)
    precio: Decimal = Field(ge=0)
    stock: int = Field(default=0, ge=0)
    abv: Decimal = Field(ge=0, le=100)
    volumen_ml: int = Field(gt=0)

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