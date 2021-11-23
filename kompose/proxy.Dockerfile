FROM nginx:alpine
COPY ./proxy/nginx-prod.conf /etc/nginx/conf.d/default.conf
CMD ["nginx", "-g", "daemon off;"]