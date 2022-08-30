# compilação
FROM node:lts-alpine as build-stage
WORKDIR /app

# deixa disponivel variavel de ambiente na compilacao
ARG VUE_APP_BACKEND_URL                       
ENV VUE_APP_API=$VUE_APP_BACKEND_URL 

COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# produção
FROM nginx:stable-alpine as production-stage
COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]