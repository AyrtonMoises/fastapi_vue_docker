import pytest

from models.burgers import Burger, Ingrediente, Opcional, Status 
from models.auth import User
from utils.passlib_crypt import get_password_hash


@pytest.fixture(scope="session")
def ingredientes(db_session):
    data = [
        Ingrediente(descricao="Maminha", tipo="C"),
        Ingrediente(descricao="Italiano", tipo="P"),
        Ingrediente(descricao="Patinho", tipo="C"),
        Ingrediente(descricao="3 Queijos", tipo="P"),
    ]
    db_session.bulk_save_objects(data)
    db_session.commit()
    return db_session.query(Ingrediente).all()


@pytest.fixture(scope="session")
def opcionais(db_session):
    data = [
        Opcional(descricao="Barbecue"),
        Opcional(descricao="Mostarda"),
        Opcional(descricao="Ovo"),
    ]
    db_session.bulk_save_objects(data)
    db_session.commit()
    return db_session.query(Opcional).all()


@pytest.fixture(scope="session")
def status(db_session):
    data = [
        Status(descricao="Pendente"),
        Status(descricao="Produção"),
        Status(descricao="Finalizado"),
    ]
    db_session.bulk_save_objects(data)
    db_session.commit()
    return db_session.query(Status).all()


@pytest.fixture(scope="session")
def users(db_session):
    data = [
        User(
            username='usuario1',
            password=get_password_hash('senha'),
            full_name='usuario1 sobrenome',
            disabled=False
        ),
        User(
            username='usuario2',
            password=get_password_hash('senha'),
            full_name='usuario2 sobrenome',
            disabled=True
        )
    ]
    db_session.bulk_save_objects(data)
    db_session.commit()
    return db_session.query(User).all()



@pytest.fixture(scope="session")
def burgers(db_session, ingredientes, status, opcionais):
    carne = db_session.query(Ingrediente).filter_by(tipo='C').all()[0]
    pao = db_session.query(Ingrediente).filter_by(tipo='P').all()[0]
    status = db_session.query(Status).filter_by(id=1).one_or_none()
    opcional_1 = db_session.query(Opcional).filter_by(id=1).one_or_none()
    opcional_2 = db_session.query(Opcional).filter_by(id=2).one_or_none()

    data = [
        Burger(
            nome='João',
            carne=carne,
            pao=pao,
            preco=29.99,
            status=status,
            opcionais=[opcional_1, opcional_2]
        ),
        Burger(
            nome='Maria',
            carne=carne,
            pao=pao,
            preco=15.00,
            status=status
        )
    ]

    db_session.bulk_save_objects(data)
    db_session.commit()

    return db_session.query(Burger).all()
