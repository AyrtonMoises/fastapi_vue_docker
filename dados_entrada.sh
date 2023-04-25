
# usuario
curl -X 'POST' \
  'http://localhost:5000/api/users' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "meu_usuario",
  "full_name": "nome completo",
  "disabled": false,
  "password": "minha_senha"
}'

# ingredientes

## pães

curl -X 'POST' \
  'http://localhost:5000/api/ingrediente' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '
  {
    "descricao": "Francês",
    "tipo": "P"
  }
'

curl -X 'POST' \
  'http://localhost:5000/api/ingrediente' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '
  {
    "descricao": "Gergelim",
    "tipo": "P"
  }
'

## carne

curl -X 'POST' \
  'http://localhost:5000/api/ingrediente' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '
  {
    "descricao": "Picanha",
    "tipo": "C"
  }
'

curl -X 'POST' \
  'http://localhost:5000/api/ingrediente' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '
  {
    "descricao": "Maminha",
    "tipo": "C"
  }
'

# opcionais
curl -X 'POST' \
  'http://localhost:5000/api/opcional' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "descricao": "ketchup"
}'

curl -X 'POST' \
  'http://localhost:5000/api/opcional' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "descricao": "mostarda"
}'

# status
curl -X 'POST' \
  'http://localhost:5000/api/status' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "descricao": "pendente"
}'

curl -X 'POST' \
  'http://localhost:5000/api/status' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "descricao": "fazendo"
}'

curl -X 'POST' \
  'http://localhost:5000/api/status' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "descricao": "finalizado"
}'


