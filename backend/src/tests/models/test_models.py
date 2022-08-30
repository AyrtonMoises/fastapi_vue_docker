from models.burgers import Ingrediente, Opcional, Status, Burger 
from models.auth import User
from utils.passlib_crypt import get_password_hash


def test_create_ingrediente():
    """ Teste cria Ingrediente """
    ingrediente = Ingrediente(
        descricao='Patinho',
        tipo='C'
    )

    assert ingrediente.descricao == 'Patinho'
    assert ingrediente.tipo == 'C'


def test_create_opcional():
    """ Teste cria Opcional """
    opcional = Opcional(descricao='Bacon')
    assert opcional.descricao == 'Bacon'


def test_create_status():
    """ Teste cria Ingrediente """
    status = Status(descricao='Observação')
    assert status.descricao == 'Observação'


def test_create_burger():
    """ Teste cria Burger """
    carne = Ingrediente(descricao="Maminha",tipo="C")
    pao = Ingrediente(descricao="Italiano",tipo="P")
    status = Status(descricao="Pendente")
    opcional_1 = Opcional(descricao="Barbecue")
    opcional_2 = Opcional(descricao="Mostarda")

    burger = Burger(
        nome='João',
        carne=carne,
        pao=pao,
        preco=29.99,
        status=status,
        opcionais=[opcional_1, opcional_2]
    )

    assert burger.nome == 'João'
    assert burger.carne == carne
    assert burger.pao == pao
    assert burger.status == status
    assert burger.opcionais == [opcional_1, opcional_2]


def test_create_user():
    """ Teste cria user """
    user = User(
        username='usuario',
        password='senha',
        full_name='usuario sobrenome',
        disabled=False
    )
    password_hash = get_password_hash(user.password)
    user.password = password_hash

    assert user.username == 'usuario'
    assert user.password == password_hash
    assert user.full_name == 'usuario sobrenome'
    assert user.disabled == False

