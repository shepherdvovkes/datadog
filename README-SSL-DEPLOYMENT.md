# DATAGOD SSL Deployment Guide

This guide explains how to deploy the DATAGOD application with Let's Encrypt SSL certificates on Google Cloud Platform (GCP).

## Overview

The deployment includes:
- **Domain**: `https://datagod.s0me.uk`
- **SSL**: Let's Encrypt certificates with automatic renewal
- **Container**: Docker-based deployment with Nginx
- **Platform**: Google Cloud Run with custom domain

## Prerequisites

1. **Google Cloud SDK** installed and authenticated
2. **Docker** installed locally
3. **Domain DNS** pointing to your GCP resources
4. **GCP Project** with billing enabled

## Quick Start

### 1. Set Environment Variables

```bash
export GCP_PROJECT_ID="your-project-id"
export GCP_REGION="us-central1"
```

### 2. Deploy to GCP

```bash
# Make deployment script executable
chmod +x deploy-gcp.sh

# Run deployment
./deploy-gcp.sh
```

### 3. Update DNS Records

After deployment, update your DNS records to point to the provided load balancer IP.

## Manual Deployment Steps

### Step 1: Build and Push Docker Image

```bash
# Build the image
docker build -t gcr.io/$PROJECT_ID/datagod-ssl:latest .

# Configure Docker authentication
gcloud auth configure-docker

# Push the image
docker push gcr.io/$PROJECT_ID/datagod-ssl:latest
```

### Step 2: Deploy to Cloud Run

```bash
gcloud run deploy datagod-ssl \
  --image gcr.io/$PROJECT_ID/datagod-ssl:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --port 80 \
  --port 443 \
  --set-env-vars "DOMAIN=datagod.s0me.uk,EMAIL=admin@datagod.s0me.uk,STAGING=false" \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10
```

### Step 3: Set Up Custom Domain

```bash
# Map domain to Cloud Run service
gcloud run domain-mappings create \
  --service datagod-ssl \
  --domain datagod.s0me.uk \
  --region us-central1
```

### Step 4: Create SSL Certificate

```bash
# Create managed SSL certificate
gcloud compute ssl-certificates create datagod-ssl-cert \
  --domains=datagod.s0me.uk \
  --global
```

## Local Development with SSL

### Using Docker Compose

```bash
# Start the application with SSL
docker-compose up -d

# Check logs
docker-compose logs -f datagod-ssl

# Stop the application
docker-compose down
```

### Environment Variables

Create a `.env` file with:

```env
DOMAIN=datagod.s0me.uk
EMAIL=admin@datagod.s0me.uk
STAGING=true
FORCE_RENEWAL=false
```

## SSL Certificate Management

### Automatic Renewal

The container includes automatic certificate renewal:
- Certificates are checked twice daily
- Automatic renewal 30 days before expiration
- Nginx reloads with new certificates

### Manual Renewal

```bash
# Renew certificates manually
docker exec datagod-ssl /usr/local/bin/ssl-setup.sh renew

# Check certificate status
docker exec datagod-ssl /usr/local/bin/ssl-setup.sh check
```

## Monitoring and Logs

### View Logs

```bash
# Cloud Run logs
gcloud logging read "resource.type=cloud_run_revision" --limit 50

# Container logs
docker-compose logs -f datagod-ssl
```

### Health Checks

The deployment includes health checks:
- HTTP endpoint: `http://datagod.s0me.uk/`
- HTTPS endpoint: `https://datagod.s0me.uk/`
- Health check endpoint: `https://datagod.s0me.uk/.well-known/security.txt`

## Security Features

- **SSL/TLS**: TLS 1.2 and 1.3 support
- **Security Headers**: HSTS, X-Frame-Options, X-Content-Type-Options
- **Rate Limiting**: Protection against abuse
- **Gzip Compression**: Optimized content delivery
- **Static File Caching**: Efficient resource delivery

## Troubleshooting

### Common Issues

1. **Domain not accessible**
   - Check DNS records
   - Verify firewall rules
   - Ensure port 80/443 are open

2. **SSL certificate issues**
   - Check domain ownership
   - Verify email address
   - Use staging environment for testing

3. **Container startup issues**
   - Check environment variables
   - Verify nginx configuration
   - Review container logs

### Debug Commands

```bash
# Test nginx configuration
docker exec datagod-ssl nginx -t

# Check SSL certificate
openssl s_client -connect datagod.s0me.uk:443 -servername datagod.s0me.uk

# Test domain resolution
nslookup datagod.s0me.uk
```

## File Structure

```
DATADOG/
├── Dockerfile                 # Multi-stage Docker build
├── docker-compose.yml         # Local development
├── nginx.conf                 # Nginx main configuration
├── nginx-ssl.conf            # SSL configuration template
├── ssl-setup.sh              # SSL certificate management
├── docker-entrypoint.sh      # Container startup script
├── deploy-gcp.sh             # GCP deployment script
├── cloudbuild.yaml           # Cloud Build configuration
├── .dockerignore             # Docker ignore file
└── env.main                  # Environment variables
```

## Support

For issues or questions:
1. Check the logs first
2. Verify DNS configuration
3. Test SSL certificate status
4. Review GCP resource status

## License

This deployment configuration is part of the DATAGOD project.
