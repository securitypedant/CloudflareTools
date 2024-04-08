# Simple Python Flask application for managing Cloudflare features on your local home network

- Dynamic DNS updates

## TODO

- Build ability to keep a Zero Trust list updated with our internet IP

## To build the docker image

docker buildx build --push --platform linux/amd64,linux/arm64 -t simonsecuritypedant/cloudflaretools:latest .