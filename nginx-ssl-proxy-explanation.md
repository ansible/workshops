# nginx SSL Proxy Setup for Ansible Automation Platform

## Table of Contents

1. [Overview](#overview)
2. [Architecture Explanation](#architecture-explanation)
3. [How the Setup Works](#how-the-setup-works)
4. [Port Configuration Discovery](#port-configuration-discovery)
5. [The nginx Proxy Solution](#the-nginx-proxy-solution)
6. [Traffic Flow](#traffic-flow)
7. [Why This Approach](#why-this-approach)
8. [Key Configuration Files](#key-configuration-files)

## Overview

This document explains how the `issue_cert` role implements SSL certificates for Ansible Automation Platform (AAP) workshops **without modifying AAP itself**. Instead of reconfiguring AAP's SSL certificates (which would require re-running the entire installer), this solution installs a **separate nginx instance** that acts as an SSL-terminating reverse proxy.

## Architecture Explanation

**Important**: This setup does **NOT** modify AAP's configuration or install nginx "into" AAP. Instead, it:

1. **Installs a standalone nginx service** on the same host as AAP
2. **Configures nginx as a reverse proxy** with SSL termination
3. **Leaves AAP completely unchanged** - AAP continues running on its original port with its original configuration

## How the Setup Works

### AAP Installation (Pre-built in AMI)
- AAP is installed during the Packer AMI build process
- The `extra_vars.yml` file specifies `aap_port: 8501`
- AAP's envoy gateway is configured to listen on port 8501 instead of the default 443
- AAP runs with its own self-signed certificates on port 8501

### SSL Certificate Solution (During Workshop Provisioning)
- The `issue_cert` role installs a **separate nginx instance**
- nginx obtains proper SSL certificates from Let's Encrypt
- nginx is configured to listen on port 443 (the standard HTTPS port)
- nginx proxies all traffic to AAP running on localhost:8501

## Port Configuration Discovery

The mystery of port 8501 is solved by examining the Packer build configuration:

**File: `/provisioner/packer/extra_vars.yml`**
```yaml
aap_port: 8501
```

This variable is used during AMI creation, causing AAP to be installed with:
```yaml
envoy_https_port: 8501  # Instead of default 443
```

## The nginx Proxy Solution

### nginx Installation and Configuration

The `issue_cert` role performs these steps:

1. **Installs nginx** (separate from AAP)
```yaml
- name: Make sure nginx and certbot are installed
  ansible.builtin.dnf:
    name:
      - nginx
      - certbot
```

2. **Obtains SSL certificates** from Let's Encrypt
```yaml
- name: Issue SSL cert
  ansible.builtin.shell: certbot certonly --standalone -d {{ dns_name }}
```

3. **Configures nginx as SSL proxy**
```nginx
# HTTPS server block
server {
    listen 443 ssl;
    server_name {{ dns_name }};

    # SSL certificates from Let's Encrypt
    ssl_certificate /etc/nginx/ssl/aap.crt;
    ssl_certificate_key /etc/nginx/ssl/aap.key;

    # Proxy all traffic to AAP
    location / {
        proxy_pass https://127.0.0.1:8501;
        proxy_ssl_verify off;
        # ... additional proxy headers
    }
}
```

## Traffic Flow

```
Internet Request (HTTPS:443)
    ↓
nginx (Port 443) - SSL Termination with Let's Encrypt Certs
    ↓
Proxy Pass to AAP (localhost:8501) - Original AAP with Self-Signed Certs
    ↓
AAP Response back through nginx
    ↓
Encrypted Response to Client
```

## Why This Approach

### Advantages:
1. **No AAP Modification**: AAP installation remains completely untouched
2. **No Installer Re-run**: Avoids the time and complexity of reconfiguring AAP
3. **Proper SSL Certificates**: Uses Let's Encrypt for trusted certificates
4. **Clean Separation**: nginx handles SSL, AAP handles application logic
5. **Easy Maintenance**: SSL certificate renewal happens independently of AAP

### Alternative Approaches (Not Used):
- **Modifying AAP SSL**: Would require re-running the AAP installer with new certificate paths
- **Direct Certificate Replacement**: Would require stopping AAP services and complex certificate management

## Key Configuration Files

### 1. Packer Build Configuration
**File**: `provisioner/packer/extra_vars.yml`
```yaml
aap_port: 8501  # Forces AAP to use port 8501 during AMI build
```

### 2. AAP Installation Template
**File**: `roles/control_node/templates/controller_install.j2`
```ini
envoy_https_port={{ aap_port | default('443') | int }}
```

### 3. nginx Configuration Template
**File**: `roles/issue_cert/templates/nginx.conf.j2`
```nginx
server {
    listen 443 ssl;
    location / {
        proxy_pass https://127.0.0.1:8501;  # Proxy to AAP
    }
}
```

### 4. Security Group Rules
**File**: `provisioner/group_vars/all/vpc_rules.yml`
```yaml
- proto: tcp
  to_port: 8501
  from_port: 8501
  cidr_ip: 0.0.0.0/0
  rule_desc: receptor  # AAP internal port
```

---

**Summary**: This is an elegant solution that provides proper SSL certificates for workshop participants without the complexity and time required to modify AAP's native SSL configuration. The separate nginx proxy handles all SSL concerns while AAP continues running unchanged on its internal port.
