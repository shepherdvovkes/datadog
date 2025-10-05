#!/bin/bash

# SSL Certificate Setup Script for Let's Encrypt
# This script handles SSL certificate generation and renewal

set -e

# Environment variables
DOMAIN=${DOMAIN:-"your-domain.com"}
EMAIL=${EMAIL:-"admin@your-domain.com"}
STAGING=${STAGING:-"false"}
NGINX_CONF="/etc/nginx/conf.d/default.conf"
CERT_PATH="/etc/letsencrypt/live/$DOMAIN"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

# Function to check if domain is accessible
check_domain() {
    log "Checking if domain $DOMAIN is accessible..."
    
    # Wait for nginx to start
    sleep 5
    
    # Check if domain resolves and is accessible
    if curl -f -s "http://$DOMAIN" > /dev/null; then
        log "Domain $DOMAIN is accessible"
        return 0
    else
        error "Domain $DOMAIN is not accessible. Please ensure:"
        error "1. Domain DNS points to this server"
        error "2. Port 80 is open"
        error "3. No firewall blocking the connection"
        return 1
    fi
}

# Function to generate initial self-signed certificate
generate_self_signed() {
    log "Generating self-signed certificate for initial setup..."
    
    mkdir -p "$(dirname "$CERT_PATH")"
    
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout "$CERT_PATH/privkey.pem" \
        -out "$CERT_PATH/fullchain.pem" \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=$DOMAIN" \
        -addext "subjectAltName=DNS:$DOMAIN"
    
    # Create symlinks for nginx
    ln -sf "$CERT_PATH/privkey.pem" /etc/letsencrypt/live/$DOMAIN/privkey.pem
    ln -sf "$CERT_PATH/fullchain.pem" /etc/letsencrypt/live/$DOMAIN/fullchain.pem
    
    log "Self-signed certificate generated"
}

# Function to obtain Let's Encrypt certificate
obtain_letsencrypt_cert() {
    log "Obtaining Let's Encrypt certificate for $DOMAIN..."
    
    # Prepare certbot command
    CERTBOT_CMD="certbot certonly --webroot -w /var/www/certbot"
    CERTBOT_CMD="$CERTBOT_CMD --email $EMAIL --agree-tos --no-eff-email"
    CERTBOT_CMD="$CERTBOT_CMD --domains $DOMAIN"
    
    # Add staging flag if enabled
    if [ "$STAGING" = "true" ]; then
        CERTBOT_CMD="$CERTBOT_CMD --staging"
        warn "Using Let's Encrypt staging environment"
    fi
    
    # Force renewal if requested
    if [ "$FORCE_RENEWAL" = "true" ]; then
        CERTBOT_CMD="$CERTBOT_CMD --force-renewal"
    fi
    
    # Run certbot
    if $CERTBOT_CMD; then
        log "Let's Encrypt certificate obtained successfully"
        return 0
    else
        error "Failed to obtain Let's Encrypt certificate"
        return 1
    fi
}

# Function to update nginx configuration for SSL
update_nginx_ssl() {
    log "Updating nginx configuration for SSL..."
    
    # Check if certificates exist
    if [ -f "$CERT_PATH/privkey.pem" ] && [ -f "$CERT_PATH/fullchain.pem" ]; then
        log "SSL certificates found, enabling HTTPS"
        
        # Create SSL nginx configuration
        cat > "$NGINX_CONF" << EOF
server {
    listen 80;
    server_name $DOMAIN;
    
    # Redirect all HTTP traffic to HTTPS
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $DOMAIN;
    
    # SSL Configuration
    ssl_certificate $CERT_PATH/fullchain.pem;
    ssl_certificate_key $CERT_PATH/privkey.pem;
    
    # SSL Security Settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Root directory
    root /usr/share/nginx/html;
    index index.html;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
    
    # Main location block
    location / {
        try_files \$uri \$uri/ /index.html;
    }
    
    # Static files caching
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Security.txt
    location /.well-known/security.txt {
        alias /usr/share/nginx/html/security.txt;
    }
    
    # Robots.txt
    location /robots.txt {
        alias /usr/share/nginx/html/robots.txt;
    }
    
    # Let's Encrypt challenge
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
}
EOF
        
        log "Nginx SSL configuration updated"
    else
        error "SSL certificates not found at $CERT_PATH"
        return 1
    fi
}

# Function to setup SSL certificates
setup_ssl() {
    log "Starting SSL setup for domain: $DOMAIN"
    
    # Check if domain is accessible
    if ! check_domain; then
        warn "Domain not accessible, generating self-signed certificate"
        generate_self_signed
        update_nginx_ssl
        return 0
    fi
    
    # Try to obtain Let's Encrypt certificate
    if obtain_letsencrypt_cert; then
        log "Let's Encrypt certificate obtained successfully"
    else
        warn "Failed to obtain Let's Encrypt certificate, using self-signed"
        generate_self_signed
    fi
    
    # Update nginx configuration
    update_nginx_ssl
    
    log "SSL setup completed"
}

# Function to renew certificates
renew_certificates() {
    log "Renewing SSL certificates..."
    
    if certbot renew --quiet; then
        log "Certificates renewed successfully"
        # Reload nginx to use new certificates
        nginx -s reload
    else
        error "Certificate renewal failed"
        return 1
    fi
}

# Main execution
case "${1:-setup}" in
    "setup")
        setup_ssl
        ;;
    "renew")
        renew_certificates
        ;;
    "check")
        check_domain
        ;;
    *)
        echo "Usage: $0 {setup|renew|check}"
        exit 1
        ;;
esac
