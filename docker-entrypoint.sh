#!/bin/bash

# Docker entrypoint script for SSL-enabled nginx container
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"
}

# Function to wait for nginx to be ready
wait_for_nginx() {
    local max_attempts=30
    local attempt=1
    
    log "Waiting for nginx to be ready..."
    
    while [ $attempt -le $max_attempts ]; do
        if nginx -t > /dev/null 2>&1; then
            log "Nginx configuration is valid"
            return 0
        fi
        
        warn "Attempt $attempt/$max_attempts: Nginx not ready yet..."
        sleep 2
        ((attempt++))
    done
    
    error "Nginx failed to become ready after $max_attempts attempts"
    return 1
}

# Function to start nginx in background
start_nginx() {
    log "Starting nginx in background..."
    nginx -g "daemon on;"
    
    # Wait for nginx to be ready
    if wait_for_nginx; then
        log "Nginx started successfully"
    else
        error "Failed to start nginx"
        exit 1
    fi
}

# Function to setup SSL certificates
setup_ssl_certificates() {
    log "Setting up SSL certificates..."
    
    # Run SSL setup script
    if /usr/local/bin/ssl-setup.sh setup; then
        log "SSL setup completed successfully"
    else
        warn "SSL setup failed, continuing with HTTP only"
    fi
}

# Function to setup certificate renewal cron job
setup_cert_renewal() {
    log "Setting up certificate renewal..."
    
    # Create renewal script
    cat > /usr/local/bin/renew-certs.sh << 'EOF'
#!/bin/bash
/usr/local/bin/ssl-setup.sh renew
EOF
    
    chmod +x /usr/local/bin/renew-certs.sh
    
    # Add to crontab (run twice daily)
    echo "0 2,14 * * * /usr/local/bin/renew-certs.sh >> /var/log/cert-renewal.log 2>&1" | crontab -
    
    log "Certificate renewal cron job configured"
}

# Function to handle graceful shutdown
graceful_shutdown() {
    log "Received shutdown signal, gracefully stopping nginx..."
    nginx -s quit
    
    # Wait for nginx to stop
    while pgrep nginx > /dev/null; do
        sleep 1
    done
    
    log "Nginx stopped gracefully"
    exit 0
}

# Set up signal handlers
trap graceful_shutdown SIGTERM SIGINT

# Main execution
main() {
    log "Starting DATAGOD SSL-enabled container..."
    
    # Display environment information
    info "Domain: ${DOMAIN:-'not set'}"
    info "Email: ${EMAIL:-'not set'}"
    info "Staging: ${STAGING:-'false'}"
    
    # Validate required environment variables
    if [ -z "$DOMAIN" ]; then
        error "DOMAIN environment variable is required"
        exit 1
    fi
    
    if [ -z "$EMAIL" ]; then
        error "EMAIL environment variable is required"
        exit 1
    fi
    
    # Start nginx in background first
    start_nginx
    
    # Setup SSL certificates
    setup_ssl_certificates
    
    # Setup certificate renewal
    setup_cert_renewal
    
    # Test nginx configuration
    if nginx -t; then
        log "Nginx configuration is valid"
    else
        error "Nginx configuration is invalid"
        exit 1
    fi
    
    # Reload nginx with new configuration
    nginx -s reload
    
    log "Container is ready and serving traffic"
    log "HTTP: http://$DOMAIN"
    log "HTTPS: https://$DOMAIN"
    
    # Keep container running and monitor nginx
    while true; do
        if ! pgrep nginx > /dev/null; then
            error "Nginx process died, exiting..."
            exit 1
        fi
        sleep 30
    done
}

# Run main function
main "$@"
