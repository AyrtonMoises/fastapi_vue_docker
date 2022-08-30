from typing import List, Literal
from fastapi import APIRouter, status, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.schemas import (
    BurgerIn, BurgerOut, Opcional, IngredienteIn,
    Status, BurgerOutList, IngredienteOut, BurgerParcial, User, OpcionalOut, StatusOut
)
from crud.burger import (
    BurgerCRUD, OpcionalCRUD, IngredienteCRUD, StatusCRUD
)
from routers.auth_router import get_current_active_user



router = APIRouter()


@router.post('/burger', status_code=status.HTTP_201_CREATED, response_model=BurgerOut, tags=["burger"])
def criar_burger(burger: BurgerIn, db: Session = Depends(get_db)):
    burger_criado = BurgerCRUD(db).criar(burger)
    return burger_criado

@router.put("/burger/{burger_id}", response_model=BurgerOut, tags=["burger"],)
async def atualizar_burger(burger_id: int, burger: BurgerIn, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    burger = BurgerCRUD(db).atualizar(burger_id, burger)
    return burger

@router.patch("/burger/{burger_id}", response_model=BurgerOut, tags=["burger"],)
async def atualizar_parcial_burger(burger_id: int, burger: BurgerParcial, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    burger = BurgerCRUD(db).atualizar_parcial(burger_id, burger)
    return burger

@router.get('/burger', response_model=List[BurgerOutList], tags=["burger"])
def listar_burgers(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, current_user: User = Depends(get_current_active_user)):
    burgers = BurgerCRUD(db).listar()
    return burgers[skip : limit]


@router.get('/burger/{burger_id}', response_model=BurgerOut, tags=["burger"],)
def obter_burger(burger_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    try:
        burger = BurgerCRUD(db).obter(burger_id)
        return burger
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Não existe um burger com id={burger_id}'
        )

@router.delete('/burger/{burger_id}', tags=["burger"])
def remover_burger(burger_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    BurgerCRUD(db).remover(burger_id)
    return {"msg": "Removido com sucesso"}


@router.post('/opcional', status_code=status.HTTP_201_CREATED, tags=["opcional"])
def criar_opcional(opcional: Opcional, db: Session = Depends(get_db)):
    opcional_criado = OpcionalCRUD(db).criar(opcional)
    return opcional_criado


@router.get('/opcional', response_model=List[OpcionalOut], tags=["opcional"])
def listar_opcionals(db: Session = Depends(get_db)):
    return OpcionalCRUD(db).listar()


@router.delete('/opcional/{opcional_id}', tags=["opcional"])
def remover_opcional(opcional_id: int, db: Session = Depends(get_db)):
    OpcionalCRUD(db).remover(opcional_id)
    return {"msg": "Removido com sucesso"}


@router.post('/ingrediente', status_code=status.HTTP_201_CREATED, tags=["ingrediente"])
def criar_ingrediente(ingrediente: IngredienteIn, db: Session = Depends(get_db)):
    ingrediente_criado = IngredienteCRUD(db).criar(ingrediente)
    return ingrediente_criado


@router.get('/ingrediente', response_model=List[IngredienteOut], tags=["ingrediente"])
def listar_ingrediente(tipo_ingrediente: Literal["C", "P"] = Query(
        default=None,
        title="Tipo",
        description="(C) Carne, (P) Pão",
    ), db: Session = Depends(get_db)):
    return IngredienteCRUD(db).listar(tipo_ingrediente)


@router.delete('/ingrediente/{ingrediente_id}', tags=["ingrediente"])
def remover_ingrediente(ingrediente_id: int, db: Session = Depends(get_db)):
    IngredienteCRUD(db).remover(ingrediente_id)
    return {"msg": "Removido com sucesso"}


@router.post('/status', status_code=status.HTTP_201_CREATED, tags=["status"])
def criar_status(status: Status, db: Session = Depends(get_db)):
    status_criado = StatusCRUD(db).criar(status)
    return status_criado


@router.get('/status', response_model=List[StatusOut], tags=["status"])
def listar_status(db: Session = Depends(get_db)):
    return StatusCRUD(db).listar()


@router.delete('/status/{status_id}', tags=["status"])
def remover_status(status_id: int, db: Session = Depends(get_db)):
    StatusCRUD(db).remover(status_id)
    return {"msg": "Removido com sucesso"}

