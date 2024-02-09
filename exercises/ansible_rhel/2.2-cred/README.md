# Workshop Exercise: Inventories and Credentials in Ansible Automation Controller

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),![japan](../../../images/japan.png)[日本語](README.ja.md),![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Objective
This workshop is designed to provide a practical understanding of how to manage inventories and credentials within the Ansible Automation Controller. You'll learn how to navigate a preloaded inventory, understand its structure, and explore the setup and use of machine credentials for accessing managed hosts.

## Table of Contents
1. [Introduction to Inventories](#1-introduction-to-inventories)
2. [Exploring the 'Workshop Inventory'](#2-exploring-the-workshop-inventory)
3. [Understanding Machine Credentials](#3-understanding-machine-credentials)
4. [Additional Credential Types](#4-additional-credential-types)
5. [Conclusion](#5-conclusion)

### 1. Introduction to Inventories
Inventories in the Ansible Automation Controller are crucial for defining and organizing the hosts your playbooks will run against. They can be static, with a fixed list of hosts, or dynamic, pulling host lists from external sources.

### 2. Exploring the 'Workshop Inventory'
The 'Workshop Inventory' is preloaded into your lab environment, representing a typical static inventory:

- **Accessing the Inventory:** Navigate to `Resources → Inventories` in the web UI, and select 'Workshop Inventory'.
- **Viewing Hosts:** Click the 'Hosts' button to reveal the preloaded host configurations, similar to what you might find in a traditional Ansible inventory file, such as:



```yaml
[web_servers]
web1 ansible_host=22.33.44.55
web2 ansible_host=33.44.55.66
...
```


### 3. Understanding Machine Credentials
Machine credentials are essential for establishing SSH connections to your managed hosts:

- **Accessing Credentials:** From the main menu, choose `Resources → Credentials` and select 'Workshop Credential'.
- **Credential Details:** The 'Workshop Credential' is pre-set with parameters like:
- **Credential Type:** Machine, for SSH access.
- **Username:** A predefined user, e.g., `ec2-user`.
- **SSH Private Key:** Encrypted, providing secure access to your hosts.

### 4. Additional Credential Types
The Ansible Automation Controller supports various credential types for different automation scenarios:

- **Network Credentials:** For managing network devices.
- *Source Control Credentials:** For source control management access.
- **Amazon Web Services Credentials:** For integration with Amazon AWS.

Each type is tailored to specific requirements, enhancing your automation's flexibility and security.

### 5. Conclusion
This workshop introduces the foundational concepts of inventories and credentials within the Ansible Automation Controller. Understanding these components is crucial for efficiently managing your automation tasks and securing access to your infrastructure.

---
**Navigation**
<br>
[Previous Exercise](../2.1-intro) - [Next Exercise](../2.3-projects)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-2---ansible-tower-exercises)


