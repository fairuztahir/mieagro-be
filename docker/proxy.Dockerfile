# syntax=docker/dockerfile:1
ARG APP_ENV

FROM nginx:alpine AS base
RUN apk update && apk upgrade
# RUN apk --no-cache upgrade curl libxml2

FROM base as dev-preinstall
# RUN --mount=type=cache,target=/root/.cache/proxy
COPY ./proxy/nginx-dev.conf /etc/nginx/conf.d/default.conf


FROM base as prod-preinstall
# RUN --mount=type=cache,target=/root/.cache/proxy
COPY ./proxy/nginx-prod.conf /etc/nginx/conf.d/default.conf

FROM ${APP_ENV}-preinstall as release

FROM release
CMD ["nginx", "-g", "daemon off;"]