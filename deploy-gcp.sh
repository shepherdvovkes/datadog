#!/bin/bash

# GCP Deployment Script for DATAGOD with Let's Encrypt SSL
# This script deploys the containerized application to Google Cloud Platform

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

# Configuration
PROJECT_ID=${GCP_PROJECT_ID:-"datagod-project"}
REGION=${GCP_REGION:-"us-central1"}
ZONE=${GCP_ZONE:-"us-central1-a"}
DOMAIN="datagod.s0me.uk"
EMAIL="admin@datagod.s0me.uk"
SERVICE_NAME="datagod-ssl"

# Function to check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check if gcloud is installed
    if ! command -v gcloud &> /dev/null; then
        error "gcloud CLI is not installed. Please install it first."
        exit 1
    fi
    
    # Check if docker is installed
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Please install it first."
        exit 1
    fi
    
    # Check if user is authenticated
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        error "Not authenticated with gcloud. Please run 'gcloud auth login'"
        exit 1
    fi
    
    log "Prerequisites check passed"
}

# Function to set up GCP project
setup_project() {
    log "Setting up GCP project: $PROJECT_ID"
    
    # Set the project
    gcloud config set project $PROJECT_ID
    
    # Enable required APIs
    log "Enabling required APIs..."
    gcloud services enable cloudbuild.googleapis.com
    gcloud services enable run.googleapis.com
    gcloud services enable containerregistry.googleapis.com
    gcloud services enable compute.googleapis.com
    
    log "GCP project setup completed"
}

# Function to build and push Docker image
build_and_push() {
    log "Building and pushing Docker image..."
    
    # Build the image
    docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME:latest .
    
    # Configure Docker to use gcloud as a credential helper
    gcloud auth configure-docker
    
    # Push the image
    docker push gcr.io/$PROJECT_ID/$SERVICE_NAME:latest
    
    log "Docker image built and pushed successfully"
}

# Function to deploy to Cloud Run
deploy_to_cloud_run() {
    log "Deploying to Cloud Run..."
    
    # Deploy the service
    gcloud run deploy $SERVICE_NAME \
        --image gcr.io/$PROJECT_ID/$SERVICE_NAME:latest \
        --region $REGION \
        --platform managed \
        --allow-unauthenticated \
        --port 80 \
        --port 443 \
        --set-env-vars "DOMAIN=$DOMAIN,EMAIL=$EMAIL,STAGING=false" \
        --memory 1Gi \
        --cpu 1 \
        --max-instances 10 \
        --timeout 300 \
        --concurrency 1000
    
    log "Cloud Run deployment completed"
}

# Function to set up custom domain
setup_custom_domain() {
    log "Setting up custom domain: $DOMAIN"
    
    # Map the domain to the Cloud Run service
    gcloud run domain-mappings create \
        --service $SERVICE_NAME \
        --domain $DOMAIN \
        --region $REGION
    
    log "Custom domain mapping created"
    warn "You need to update your DNS records to point to the provided CNAME target"
}

# Function to set up SSL certificate
setup_ssl_certificate() {
    log "Setting up SSL certificate for $DOMAIN"
    
    # Create managed SSL certificate
    gcloud compute ssl-certificates create datagod-ssl-cert \
        --domains=$DOMAIN \
        --global
    
    log "SSL certificate creation initiated"
    warn "SSL certificate provisioning may take up to 10 minutes"
}

# Function to create load balancer with SSL
create_load_balancer() {
    log "Creating load balancer with SSL..."
    
    # Create backend service
    gcloud compute backend-services create datagod-backend \
        --global \
        --protocol HTTP \
        --port-name http \
        --health-checks datagod-health-check
    
    # Create health check
    gcloud compute health-checks create http datagod-health-check \
        --port 80 \
        --request-path / \
        --check-interval 30s \
        --timeout 10s \
        --healthy-threshold 2 \
        --unhealthy-threshold 3
    
    # Create URL map
    gcloud compute url-maps create datagod-url-map \
        --default-service datagod-backend
    
    # Create HTTPS proxy
    gcloud compute target-https-proxies create datagod-https-proxy \
        --url-map datagod-url-map \
        --ssl-certificates datagod-ssl-cert
    
    # Create HTTP proxy (for redirect)
    gcloud compute target-http-proxies create datagod-http-proxy \
        --url-map datagod-url-map
    
    # Create global forwarding rule for HTTPS
    gcloud compute forwarding-rules create datagod-https-rule \
        --global \
        --target-https-proxy datagod-https-proxy \
        --ports 443
    
    # Create global forwarding rule for HTTP (redirect)
    gcloud compute forwarding-rules create datagod-http-rule \
        --global \
        --target-http-proxy datagod-http-proxy \
        --ports 80
    
    log "Load balancer with SSL created"
}

# Function to display deployment information
display_info() {
    log "Deployment completed successfully!"
    echo ""
    info "Service URL: https://$DOMAIN"
    info "Cloud Run Service: $SERVICE_NAME"
    info "Region: $REGION"
    info "Project: $PROJECT_ID"
    echo ""
    warn "Next steps:"
    warn "1. Update your DNS records to point to the load balancer IP"
    warn "2. Wait for SSL certificate to be provisioned (up to 10 minutes)"
    warn "3. Test your site at https://$DOMAIN"
}

# Main execution
main() {
    log "Starting GCP deployment for DATAGOD with SSL..."
    
    check_prerequisites
    setup_project
    build_and_push
    deploy_to_cloud_run
    setup_custom_domain
    setup_ssl_certificate
    create_load_balancer
    display_info
    
    log "Deployment completed!"
}

# Run main function
main "$@"
