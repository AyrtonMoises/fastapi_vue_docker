from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session, aliased

from models.burgers import Burger, Ingrediente, Opcional, Status
from schemas import schemas


class BurgerCRUD():

    def __init__(self, db: Session):
        self.db = db

    def criar(self, burger: schemas.BurgerIn):
        db_burger = Burger(
            nome=burger.nome,
            carne_id=burger.carne,
            pao_id=burger.pao,
            preco=burger.preco,
            status_id=burger.status
        )

        # checa se opcional existe
        if burger.opcionais:
            if (opcionais := self.db.query(Opcional).filter(
                    Opcional.id.in_(burger.opcionais))
                ).count() == len(burger.opcionais):
                db_burger.opcionais.extend(opcionais)
            else:
                raise HTTPException(status_code=404, detail="opcional não encontrado")

        self.db.add(db_burger)
        self.db.commit()

        self.db.refresh(db_burger)
        return db_burger

    def listar(self):

        t1, t2 = aliased(Ingrediente), aliased(Ingrediente) # alias porque tem 2 fk na mesma tabela
        result_burgers = self.db.query(
            Burger.id,
            Burger.nome,
            Burger.preco,
            t1.descricao.label('carne'),
            t2.descricao.label('pao'),
            Status.descricao.label('status'),
        ).join(Status, Burger.status).join(
            t1, t1.id == Burger.carne_id).join(
            t2, t2.id == Burger.pao_id).order_by(Burger.id).all()

        # adicionar key com dados m2m
        burgers = []
        for burger in result_burgers:
            burger_id = burger.id
            burger = jsonable_encoder(burger)
            lista = self.db.query(Opcional).join(Burger.opcionais).filter(
                Burger.id==burger_id
            ).all()
            burger['opcionais'] = [i.descricao for i in lista ]
            burgers.append(burger)

        return burgers

    def obter(self, burger_id: int):
        stmt = select(Burger).filter_by(id=burger_id)
        burger = self.db.execute(stmt).first()[0]

        return burger

    def remover(self, burger_id: int):
        burger = self.db.query(Burger).filter(Burger.id==burger_id)

        if burger.one_or_none() is None:
            raise HTTPException(status_code=404, detail="burger não encontrado")

        burger.delete()
        self.db.commit()

    def atualizar(self, burger_id: int, burger_data: schemas.BurgerIn):
        burger = self.db.query(Burger).filter(Burger.id==burger_id).one_or_none()

        if burger is None:
            raise HTTPException(status_code=404, detail="burger não encontrado")

        burger.nome = burger_data.nome
        burger.carne_id = burger_data.carne
        burger.pao_id = burger_data.pao
        burger.preco = burger_data.preco
        burger.status_id = burger_data.status

        # checa se opcional existe
        if burger_data.opcionais:
            if (opcionais := self.db.query(Opcional).filter(
                    Opcional.id.in_(burger_data.opcionais))
                ).count() == len(burger_data.opcionais):
                burger.opcionais = []
                burger.opcionais.extend(opcionais)
            else:
                raise HTTPException(status_code=404, detail="opcional não encontrado")
        else:
            burger.opcionais.clear()

        self.db.commit()
        self.db.refresh(burger)
        return burger

    def atualizar_parcial(self, burger_id: int, burger_data: schemas.BurgerParcial):
        burger = self.db.query(Burger).filter(Burger.id==burger_id).one_or_none()

        if burger is None:
            raise HTTPException(status_code=404, detail="burger não encontrado")

        burger_data_dict = burger_data.dict(exclude_unset=True) # dicionario com keys diferente de None
        burger_data_opcionais = burger_data_dict.pop('opcionais', None)
        for key, value in burger_data_dict.items():
            setattr(burger, key, value)

        # checa se opcional existe
        if burger_data_opcionais:
            if (opcionais := self.db.query(Opcional).filter(
                    Opcional.id.in_(burger_data.opcionais))
                ).count() == len(burger_data.opcionais):
                burger.opcionais = []
                burger.opcionais.extend(opcionais)
            else:
                raise HTTPException(status_code=404, detail="opcional não encontrado")

        elif burger_data_opcionais == []:
            burger.opcionais.clear()

        self.db.commit()
        self.db.refresh(burger)
        return burger

class OpcionalCRUD():

    def __init__(self, db: Session):
        self.db = db

    def criar(self, opcional: schemas.Opcional):
        db_opcional = Opcional(
            descricao=opcional.descricao
        )
        self.db.add(db_opcional)
        self.db.commit()
        self.db.refresh(db_opcional)

        return db_opcional

    def listar(self):
        opcionais = self.db.query(Opcional).all()
        return opcionais

    def obter(self, opcional_id: int):
        stmt = select(Opcional).filter_by(id=opcional_id)
        opcional = self.db.execute(stmt).one()

        return opcional

    def remover(self, opcional_id: int):
        opcional = self.db.query(Opcional).filter(Opcional.id==opcional_id)

        if opcional.one_or_none() is None:
            raise HTTPException(status_code=404, detail="opcional não encontrado")

        opcional.delete()
        self.db.commit()


class IngredienteCRUD():

    def __init__(self, db: Session):
        self.db = db

    def criar(self, ingrediente: schemas.IngredienteIn):
        db_ingrediente = Ingrediente(
            descricao=ingrediente.descricao,
            tipo=ingrediente.tipo
        )
        self.db.add(db_ingrediente)
        self.db.commit()
        self.db.refresh(db_ingrediente)

        return db_ingrediente

    def listar(self, tipo_ingrediente: str = None):
        query = self.db.query(Ingrediente)
        if tipo_ingrediente:
            query = query.filter_by(tipo=tipo_ingrediente)
        ingredientes = query.all()
        return ingredientes

    def obter(self, ingrediente_id: int):
        stmt = select(Ingrediente).filter_by(id=ingrediente_id)
        ingrediente = self.db.execute(stmt).one()

        return ingrediente

    def remover(self, ingrediente_id: int):
        ingrediente = self.db.query(Ingrediente).filter(Ingrediente.id==ingrediente_id)

        if ingrediente.one_or_none() is None:
            raise HTTPException(status_code=404, detail="ingrediente não encontrado")

        ingrediente.delete()
        self.db.commit()


class StatusCRUD():

    def __init__(self, db: Session):
        self.db = db

    def criar(self, status: schemas.Status):
        db_status = Status(
            descricao=status.descricao,
        )
        self.db.add(db_status)
        self.db.commit()
        self.db.refresh(db_status)

        return db_status

    def listar(self):
        status = self.db.query(Status).all()
        return status

    def obter(self, status_id: int):
        stmt = select(Status).filter_by(id=status_id)
        status = self.db.execute(stmt).one()

        return status

    def remover(self, status_id: int):
        status = self.db.query(Status).filter(Status.id==status_id)

        if status.one_or_none() is None:
            raise HTTPException(status_code=404, detail="status não encontrado")

        status.delete()
        self.db.commit()