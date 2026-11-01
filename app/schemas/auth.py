from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    dni: str  # O la credencial que definas para autenticar

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: str | None = None