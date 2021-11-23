FROM node:14.14.0-alpine AS base
WORKDIR /app
COPY ./proxy/nginx.conf /etc/nginx/conf.d/default.conf
COPY ./web/package.json .
RUN npm install -g @vue/cli

FROM base as postinstall
WORKDIR /app
COPY ./web .
# --only=production
RUN npm install --silent --no-optional && npm cache clean --force \
    && npm run build
ENV PATH /app/node_modules/.bin:$PATH

FROM nginx:alpine AS production
# Remove default nginx config and replace
RUN rm /etc/nginx/conf.d/default.conf
COPY --from=postinstall /app/dist /usr/share/nginx/html
COPY --from=postinstall /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf
CMD ["nginx", "-g", "daemon off;"]