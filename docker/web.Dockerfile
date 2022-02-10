# syntax=docker/dockerfile:1
ARG APP_ENV

# Building the base image
FROM node:17-alpine AS base
# Get the latest npm version
# RUN npm i npm@latest -g
RUN apk update && apk upgrade
WORKDIR /app
COPY ./proxy/nginx.conf /etc/nginx/conf.d/default.conf
COPY ./web/package.json .
RUN --mount=type=cache,target=/root/.cache/node \
    npm install -g @vue/cli


FROM base as dev-preinstall
WORKDIR /app
COPY ./web .
RUN --mount=type=cache,target=/root/.cache/node \
    --mount=type=cache,target=/root/.cache/node-build \
    npm install --silent --no-optional && npm cache clean --force
ENV PATH /app/node_modules/.bin:$PATH


FROM base as test-preinstall
WORKDIR /app
COPY ./web .
RUN --mount=type=cache,target=/root/.cache/node \
    --mount=type=cache,target=/root/.cache/node-build \
    npm install --silent --no-optional && npm cache clean --force
ENV PATH /app/node_modules/.bin:$PATH


FROM base as prod-preinstall
WORKDIR /app
COPY ./web .
# --only=production
RUN --mount=type=cache,target=/root/.cache/node \
    --mount=type=cache,target=/root/.cache/node-build \
    npm install --silent --no-optional && npm cache clean --force \
    && npm run build
ENV PATH /app/node_modules/.bin:$PATH


FROM ${APP_ENV}-preinstall as postinstall


FROM node:17-alpine as development
RUN apk update && apk upgrade
WORKDIR /app
# RUN --mount=type=cache,target=/root/.cache/node \
#     --mount=type=cache,target=/root/.cache/node-build
COPY --from=postinstall /app .
CMD ["npm", "run", "dev"]


FROM nginx:alpine AS production
RUN apk update && apk upgrade
# RUN apk --no-cache upgrade curl libxml2
# Remove default nginx config and replace
RUN rm /etc/nginx/conf.d/default.conf
COPY --from=postinstall /app/dist /usr/share/nginx/html
COPY --from=postinstall /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf
CMD ["nginx", "-g", "daemon off;"]