from models.burgers import Opcional

    
def test_get_opcionais(client, opcionais):
    """ Teste exibindo todos os opcionais """
    response = client.get("/api/opcional")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "descricao": "Barbecue" },
        {"id": 2, "descricao": "Mostarda"},
        {"id": 3, "descricao": "Ovo"}
    ]

def test_post_opcional(client):
    """ Teste incluir opcional """
    dados = {"descricao": "Bacon"}
    response = client.post("/api/opcional", json=dados)
    assert response.status_code == 201

    dados_opcional = response.json()
    assert dados["descricao"] == dados_opcional["descricao"] 


def test_delete_opcional(client, db_session):
    """ Teste deletando opcional """
    total = db_session.query(Opcional).count()
    opcional = db_session.query(Opcional).all()[0]
    response = client.delete(f"/api/opcional/{opcional.id}")
    assert response.status_code == 200
    total_new = db_session.query(Opcional).count()
    assert total-1 == total_new


