from pydantic import BaseModel, Field
from typing import Optional, List, Union, Literal


class Opcional(BaseModel):
    descricao: str

    class Config:
        orm_mode = True

class OpcionalOut(BaseModel):
    id: int
    descricao: str

    class Config:
        orm_mode = True


class IngredienteIn(BaseModel):
    descricao: str
    tipo: Literal["C", "P"]= Field(description="(P) Pão ou (C) - Carne")

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "descricao": "Picanha",
                "tipo": "C",
            }
        }


class IngredienteOut(BaseModel):
    id: int
    descricao: str

    class Config:
        orm_mode = True


class Status(BaseModel):
    descricao: str

    class Config:
        orm_mode = True


class StatusOut(BaseModel):
    id: int
    descricao: str

    class Config:
        orm_mode = True


class BurgerIn(BaseModel):
    nome: str
    carne: int
    pao: int
    preco: float = Field(gt=0, le=100, title="O valor deve ser maior que zero e menor que 100")
    opcionais: Optional[List[int]]
    status: int

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "nome": "João",
                "carne": 2,
                "pao": 1,
                "preco": 18.99,
                "opcionais": [1, 2],
                "status": 1
            }
        }


class BurgerOut(BaseModel):
    id: int
    nome: str
    carne: IngredienteOut
    pao: IngredienteOut
    preco: float
    opcionais: Optional[List[Opcional]]
    status: Status
    carne: IngredienteOut

    class Config:
        orm_mode = True

class BurgerParcial(BaseModel):
    nome: str = None
    carne_id: int = None
    pao_id: int = None
    preco: float = Field(default=None, gt=0, le=100, title="O valor deve ser maior que zero e menor que 100")
    opcionais: Optional[List[int]] = None
    status_id: int = None


class BurgerOutList(BaseModel):
    id: int
    nome: str
    carne: str
    pao: str
    preco: float
    status: str
    opcionais: Optional[List[str]]


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    full_name: Union[str, None]
    disabled: Union[bool, None]

    class Config:
        orm_mode = True
        

class UserChangePassword(BaseModel):
    old_password: str
    new_password: str


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class RefreshToken(BaseModel):
    refresh_token: str


class AccessRefreshToken(AccessToken, RefreshToken):
    username: str


class TokenData(BaseModel):
    username: Union[str, None] = None



