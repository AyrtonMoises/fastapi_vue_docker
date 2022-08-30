# FastAPI + Vue.js + Nginx no Docker


## Variaveis de ambiente
Na pasta .envs definir variaveis utilizadas como nos exemplos .sample e nos arquivos docker como desejar

#### Desenvolvimento
.fastapi.dev
.vue.dev

#### Produção
.fastapi.prod
.db.prod

## Desenvolvimento
```
sudo docker-compose -f docker-compose-dev.yml build
sudo docker-compose -f docker-compose-dev.yml up
sudo docker-compose -f docker-compose-dev.yml down
```

## Produção
```
sudo docker-compose build
sudo docker-compose up
sudo docker-compose down
```