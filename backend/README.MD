# Burgueria API

## Criando ambiente e instalando pacotes
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Roda servidor backend
```
cd src
uvicorn server:app --reload
```

## Testes
```
cd src
pytest
```

### Comandos úteis do Alembic
```
alembic init nome_app # iniciar alembic
alembic.ini # nesse arquivo adicionar a sua url_db ou no env.py(recomendado) usar config.set_main_option('sqlalchemy.url', SQLALCHEMY_DATABASE_URL)

alembic revision --autogenerate -m "campo email adicionado ao usuario" # gera migracao automatico do model sqlalchemy(tem q importar as models no arquivo env.py do alembic como referencia para o Base.metadata do arquivo database.py) depois basta migrar
alembic revision -m "primeira" # (FORMA MANUAL não recomendado!)
alembic upgrade head # executa migrações
alembic downgrade -1 # voltar migracao anterior
alembic upgrade +1 # proxima migracao
alembic upgrade +1 --sql # proxima migracao exibindo sql
alembic history -i # migracao atual

### SQLacodegen para busca tabelas do db e cria models do sqlalchemy
sqlacodegen url_db > models_encontradas.py

```




