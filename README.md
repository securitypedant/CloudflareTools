# Simple Python Flask application for managing Cloudflare features on your local home network

- Dynamic DNS updates
- Maintain a Zero Trust list of public IPs

## TODO

- Build ability to keep a [Zero Trust list](https://developers.cloudflare.com/api/operations/zero-trust-lists-update-zero-trust-list) updated with our internet IP
- Keep IP address in [Proxy Endpoint](https://developers.cloudflare.com/api/operations/zero-trust-gateway-proxy-endpoints-update-proxy-endpoint)
- Include some version numbering in the UX up to date.
- Document what API token to create
- Tidy up GitHub and DockerHub entries so people understand how to use this

## To build the docker image

docker buildx build --push --platform linux/amd64,linux/arm64 -t simonsecuritypedant/cloudflaretools:latest .