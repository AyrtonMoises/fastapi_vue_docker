# FastAPI + Vue.js + Nginx no Docker
Sistema simples de pedidos de uma hamburgueria


## Variaveis de ambiente
Na pasta .envs definir variaveis utilizadas como nos exemplos .sample e nos arquivos docker-compose como desejar

#### Desenvolvimento
.fastapi.dev
.vue.dev

#### Produção
.fastapi.prod
.db.prod

## Desenvolvimento
```
sudo docker-compose -f docker-compose-dev.yml up -d --build
sudo docker-compose -f docker-compose-dev.yml down -v
```

## Produção
```
sudo docker-compose up -d --build
sudo docker-compose down -v
```

## Criar dados de exemplo para ambiente de desenvolvimento
```
bash dados_entrada.sh
```

WEB:
http://localhost:8080/

API:
http://localhost:5000/docs

