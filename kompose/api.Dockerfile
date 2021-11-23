FROM golang:1.15-alpine AS base
RUN apk update \
    && apk add --no-cache git ca-certificates && update-ca-certificates \
    && apk --no-cache add tzdata \
    && apk --no-cache add curl \
    && apk --no-cache add make
# Fetch dependencies.
WORKDIR /app
COPY ./api/go.* ./
RUN go mod download
COPY ./api ./

FROM base AS build
ENV APP_ENV $APP_ENV
ENV USER=appuser
ENV UID=10001
# See https://stackoverflow.com/a/55757473/12429735RUN 
RUN adduser \    
    --disabled-password \    
    --gecos "" \    
    --home "/nonexistent" \    
    --shell "/sbin/nologin" \    
    --no-create-home \    
    --uid "${UID}" \    
    "${USER}"

FROM build AS postinstall
RUN export CGO_ENABLED=0 \
    && GOOS=linux GOARCH=amd64 go build -ldflags="-w -s" -o /go/bin/rest-api

FROM scratch AS production
VOLUME /tmp/uploads/images
# Import the user and group files from the builder.
COPY --from=postinstall /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=postinstall /etc/passwd /etc/passwd
COPY --from=postinstall /etc/group /etc/group
# Copy our static executable.
COPY --from=postinstall /go/bin/rest-api /go/bin/rest-api
USER ${USER}:${USER}
# Run the rest-api binary.
CMD ["/go/bin/rest-api"]