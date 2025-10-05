# Cloudflare SSL Configuration for datadog.s0me.uk

**Date:** October 5, 2025  
**Status:** ⚠️ HTTPS Error 525 - Configuration Needed  

---

## 🔴 Current Issue:

**HTTPS Error 525:** SSL Handshake Failed

```
HTTP: ✅ Working (http://datadog.s0me.uk)
HTTPS: ❌ Error 525 (https://datadog.s0me.uk)
```

**Cause:** Cloudflare SSL/TLS mode is set to "Full" or "Full (Strict)", but Google Cloud Load Balancer only has HTTP (port 80) configured.

---

## ✅ Solution: Configure Cloudflare SSL Mode

### Go to Cloudflare Dashboard:

1. **Login to Cloudflare:** https://dash.cloudflare.com
2. **Select domain:** s0me.uk
3. **Navigate to:** SSL/TLS → Overview

### Change SSL/TLS Encryption Mode:

**Current Mode (causing error):** Full or Full (Strict)  
**Required Mode:** **Flexible** ⭐

#### Option 1: Flexible SSL (Recommended for Current Setup)
```
┌─────────────────────────────────────────────────────────────┐
│  Encryption Mode: Flexible                                  │
│                                                             │
│  User → Cloudflare: HTTPS (encrypted)                       │
│  Cloudflare → Origin: HTTP (unencrypted)                    │
│                                                             │
│  ✅ Works with your current setup (HTTP only)               │
│  ✅ Free SSL for users                                      │
│  ⚠️  Backend connection not encrypted                       │
└─────────────────────────────────────────────────────────────┘
```

**To Set:**
- Go to: SSL/TLS → Overview
- Select: **Flexible**
- Wait: 1-5 minutes for changes to apply

---

## 🔧 Architecture with Flexible SSL:

```
User Browser
    ↓ HTTPS (encrypted) ✅
Cloudflare
    ↓ HTTP (not encrypted) ⚠️
Google Cloud Load Balancer (34.149.13.177:80)
    ↓ HTTP
Cloud Storage Bucket (datadog-s0me-uk)
```

---

## 🔒 Alternative: Full SSL (More Secure)

If you want end-to-end encryption:

### Configure Google Cloud HTTPS Backend:

1. Create self-signed SSL certificate for backend
2. Configure HTTPS on port 443
3. Set Cloudflare to "Full" mode

**Commands:**
```bash
# Create backend with HTTPS
gsutil -m rsync -r gs://datadog-s0me-uk/ gs://datadog-s0me-uk-https/

# Configure Cloud CDN with HTTPS origin
# (More complex setup, not needed for static content)
```

**Trade-off:** More complex, higher cost, minimal security benefit for static site.

---

## ⚙️ Additional Cloudflare Settings:

### After Setting Flexible SSL:

1. **Always Use HTTPS** (Recommended)
   - Path: SSL/TLS → Edge Certificates
   - Setting: **ON**
   - Effect: Auto-redirect HTTP → HTTPS

2. **Automatic HTTPS Rewrites**
   - Path: SSL/TLS → Edge Certificates
   - Setting: **ON**
   - Effect: Rewrites HTTP links to HTTPS

3. **Minimum TLS Version**
   - Path: SSL/TLS → Edge Certificates
   - Setting: **TLS 1.2**
   - Effect: Blocks old, insecure TLS versions

4. **TLS 1.3**
   - Path: SSL/TLS → Edge Certificates
   - Setting: **ON**
   - Effect: Use latest, most secure TLS

---

## 📊 Current Configuration:

### DNS:
```
Type: A
Name: datadog
IP: 34.149.13.177 (via Cloudflare proxy)
Proxy: ✅ Enabled (Orange cloud)
Cloudflare IPs: 104.21.12.4, 172.67.150.231
```

### Google Cloud:
```
Load Balancer: HTTP only (port 80)
Backend: Cloud Storage bucket
CDN: Enabled
HTTPS: Not configured (using Cloudflare SSL)
```

### Cloudflare:
```
Proxy: ✅ Enabled
SSL Mode: ⚠️ Needs to be set to Flexible
HTTPS: ❌ Not working (Error 525)
HTTP: ✅ Working
```

---

## 🎯 Step-by-Step Fix:

### Step 1: Set Cloudflare SSL Mode
1. Login to Cloudflare
2. Select s0me.uk domain
3. Go to SSL/TLS → Overview
4. Change to **Flexible**
5. Wait 2-5 minutes

### Step 2: Enable Always Use HTTPS
1. Go to SSL/TLS → Edge Certificates
2. Find "Always Use HTTPS"
3. Toggle **ON**

### Step 3: Test
```bash
# Test HTTPS
curl -I https://datadog.s0me.uk

# Should return: HTTP/2 200 OK
```

---

## ✅ Expected Results After Configuration:

```
✅ http://datadog.s0me.uk → Redirects to HTTPS
✅ https://datadog.s0me.uk → HTTP 200 OK
✅ User connection encrypted (Cloudflare SSL)
✅ Free SSL certificate from Cloudflare
✅ CDN and caching enabled
✅ DDoS protection enabled
```

---

## 🔍 Verification Commands:

```bash
# Test HTTP
curl -I http://datadog.s0me.uk

# Test HTTPS
curl -I https://datadog.s0me.uk

# Check SSL certificate
openssl s_client -connect datadog.s0me.uk:443 -servername datadog.s0me.uk | grep -A5 "Certificate chain"

# Test from different location
curl -I https://datadog.s0me.uk --resolve datadog.s0me.uk:443:104.21.12.4
```

---

## 📝 Summary:

**Current Setup:**
- ✅ Cloudflare proxy active (correct!)
- ✅ HTTP working
- ❌ HTTPS not working (525 error)

**Required Action:**
- Change Cloudflare SSL/TLS mode to **Flexible**
- Enable **Always Use HTTPS**
- Wait 2-5 minutes

**Result:**
- ✅ Full HTTPS support
- ✅ Free SSL certificate
- ✅ Secure user connections
- ✅ Fast global delivery

---

## 💡 Why Flexible SSL is OK for Static Sites:

1. **User data is protected** - HTTPS between user and Cloudflare
2. **Static content only** - No sensitive data in transit to origin
3. **Public website** - Content is not confidential
4. **Simpler setup** - No certificate management on origin
5. **Free** - No additional costs

For sites with user logins, payments, or private data, use Full (Strict) SSL with proper origin certificates.

---

**Next Steps:**
1. Set Cloudflare SSL to Flexible
2. Test HTTPS
3. Report back results

---

Slava Ukraini! 🇺🇦
