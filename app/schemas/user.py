from typing import Optional
from pydantic import BaseModel, EmailStr

# --- DOMICILIO SCHEMAS ---
class DomicilioBase(BaseModel):
    cod_postal_fk: str
    calle: str
    numero: str
    piso: Optional[str] = None
    dpto: Optional[str] = None

class DomicilioCreate(DomicilioBase):
    pass

class DomicilioResponse(DomicilioBase):
    id_domicilio: int

    class Config:
        from_attributes = True

# --- USUARIO SCHEMAS ---
class UsuarioBase(BaseModel):
    dni: str
    nombre: str
    apellido: str
    email: EmailStr
    tel_fijo: Optional[str] = None
    tel_movil: Optional[str] = None
    legajo: Optional[str] = None
    cargo: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    id_rol_fk: int
    domicilio: DomicilioCreate  # Permite crear el domicilio junto con el usuario

class UsuarioResponse(UsuarioBase):
    id_usuario: int
    id_rol_fk: int
    id_domicilio_fk: int

    class Config:
        from_attributes = True