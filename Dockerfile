# Multi-stage Dockerfile for Let's Encrypt SSL with Nginx
FROM nginx:alpine AS base

# Install certbot and dependencies
RUN apk add --no-cache \
    certbot \
    certbot-nginx \
    python3 \
    py3-pip \
    openssl \
    curl \
    bash

# Create directories for SSL certificates and nginx config
RUN mkdir -p /etc/letsencrypt/live \
    && mkdir -p /etc/letsencrypt/archive \
    && mkdir -p /var/www/certbot \
    && mkdir -p /etc/nginx/conf.d \
    && mkdir -p /var/log/letsencrypt \
    && chown -R nginx:nginx /etc/letsencrypt \
    && chown -R nginx:nginx /var/www/certbot \
    && chown -R nginx:nginx /var/log/letsencrypt

# Copy SSL generation script
COPY ssl-setup.sh /usr/local/bin/ssl-setup.sh
RUN chmod +x /usr/local/bin/ssl-setup.sh

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx-ssl.conf /etc/nginx/conf.d/default.conf

# Copy application files
COPY src/ /usr/share/nginx/html/
COPY index.html /usr/share/nginx/html/
COPY public/ /usr/share/nginx/html/public/

# Generate self-signed certificate for initial setup
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/certs/nginx-selfsigned.key \
    -out /etc/ssl/certs/nginx-selfsigned.crt \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Create startup script
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Expose ports
EXPOSE 80 443

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Use custom entrypoint
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
