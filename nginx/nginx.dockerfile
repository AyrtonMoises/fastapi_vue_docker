FROM nginx:stable-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/
EXPOSE 8181
ENTRYPOINT ["nginx"]

CMD ["-g", "daemon off;"]


