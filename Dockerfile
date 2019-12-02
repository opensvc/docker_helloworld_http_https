FROM python:3-slim

COPY helloworld-http-https.py /

ENV LISTEN_IP=${LISTEN_IP:-"0.0.0.0"}
ENV HTTP_PORT=${HTTP_PORT:-8080}
ENV HTTPS_PORT=${HTTPS_PORT:-8443}
ENV SSL_CERT_PATH=${SSL_CERT_PATH:-"/etc/ssl/server.cert"}
ENV SSL_CERT_KEY=${SSL_CERT_KEY:-"/etc/ssl/server.key"}

ENTRYPOINT ["/helloworld-http-https.py" ]
