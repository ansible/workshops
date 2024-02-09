# Exercice de l'Atelier - Rôles : Rendre vos playbooks réutilisables

**Lire ceci dans d'autres langues** :
<br>![uk](../../../images/uk.png) [Anglais](README.md), ![japan](../../../images/japan.png) [Japonais](README.ja.md), ![brazil](../../../images/brazil.png) [Portugais du Brésil](README.pt-br.md), ![france](../../../images/fr.png) [Français](README.fr.md), ![Español](../../../images/col.png) [Espagnol](README.es.md).

## Table des Matières

- [Objectif](#objectif)
- [Guide](#guide)
  - [Étape 1 - Bases des Rôles](#étape-1---bases-des-rôles)
  - [Étape 2 - Nettoyage de l'Environnement](#étape-2---nettoyage-de-lenvironnement)
  - [Étape 3 - Construction du Rôle Apache](#étape-3---construction-du-rôle-apache)
  - [Étape 4 - Intégration du Rôle dans un Playbook](#étape-4---intégration-du-rôle-dans-un-playbook)
  - [Étape 5 - Exécution et Validation du Rôle](#étape-5---exécution-et-validation-du-rôle)
  - [Étape 6 - Vérification du Fonctionnement d'Apache](#étape-6---vérification-du-fonctionnement-dapache)

## Objectif

Cet exercice s'appuie sur les exercices précédents et approfondit vos compétences en Ansible en vous guidant à travers la création d'un rôle qui configure Apache (httpd). Vous utiliserez les connaissances acquises pour intégrer des variables, des gestionnaires et un modèle pour un index.html personnalisé. Ce rôle montre comment encapsuler des tâches, des variables, des modèles et des gestionnaires dans une structure réutilisable pour une automatisation efficace.

## Guide

### Étape 1 - Bases des Rôles

Les rôles dans Ansible organisent des tâches d'automatisation et des ressources connexes, telles que des variables, des modèles et des gestionnaires, dans un répertoire structuré. Cet exercice se concentre sur la création d'un rôle de configuration Apache, en mettant l'accent sur la réutilisabilité et la modularité.

### Étape 2 - Nettoyage de l'Environnement

En nous appuyant sur notre travail précédent avec la configuration d'Apache, créons un playbook Ansible dédié au nettoyage de notre environnement. Cette étape ouvre la voie à l'introduction d'un nouveau rôle Apache, offrant une vision claire des ajustements effectués. Grâce à ce processus, nous approfondirons notre compréhension de la polyvalence et de la réutilisabilité offertes par les Rôles Ansible.

Exécutez le playbook Ansible suivant pour nettoyer l'environnement :

```yaml
---
- name: Cleanup Environment
  hosts: all
  become: true
  vars:
    package_name: httpd
  tasks:
    - name: Remove Apache from web servers
      ansible.builtin.dnf:
        name: "{{ package_name }}"
        state: absent
      when: inventory_hostname in groups['web']

    - name: Remove firewalld
      ansible.builtin.dnf:
        name: firewalld
        state: absent

    - name: Delete created users
      ansible.builtin.user:
        name: "{{ item }}"
        state: absent
        remove: true  # Use 'remove: true’ to delete home directories
      loop:
        - alice
        - bob
        - carol
        - Roger

    - name: Reset MOTD to an empty message
      ansible.builtin.copy:
        dest: /etc/motd
        content: ''
```

### Étape 3 - Construction du Rôle Apache

Nous allons développer un rôle nommé `apache` pour installer, configurer et gérer Apache.

1. Générer la Structure du Rôle :

Créez le rôle à l'aide d'ansible-galaxy, en spécifiant le répertoire des rôles pour la sortie.

```bash
[student@ansible-1 lab_inventory]$ mkdir roles
[student@ansible-1 lab_inventory]$ ansible-galaxy init --offline roles/apache
```

2. Définir les Variables du Rôle :

Remplissez `/home/student/lab_inventory/roles/apache/vars/main.yml` avec des variables spécifiques à Apache :

```yaml
---
# vars file for roles/apache
apache_package_name: httpd
apache_service_name: httpd
```

3. Configurer les Tâches du Rôle :

Ajustez `/home/student/lab_inventory/roles/apache/tasks/main.yml` pour inclure des tâches pour l'installation d'Apache et la gestion des services :

```yaml
---
# tasks file for ansible-files/roles/apache
- name: Install Apache web server
  ansible.builtin.package:
    name: "{{ apache_package_name }}"
    state: present

- name: Ensure Apache is running and enabled
  ansible.builtin.service:
    name: "{{ apache_service_name }}"
    state: started
    enabled: true

- name: Install firewalld
  ansible.builtin.dnf:
    name: firewalld
    state: present

- name: Ensure firewalld is running
  ansible.builtin.service:
    name: firewalld
    state: started
    enabled: true

- name: Allow HTTPS traffic on web servers
  ansible.posix.firewalld:
    service: https
    permanent: true
    state: enabled
  when: inventory_hostname in groups['web']
  notify: Reload Firewall
```

4. Implémenter les Gestionnaires :

Dans `/home/student/lab_inventory/roles/apache/handlers/main.yml`, créez un gestionnaire pour redémarrer firewalld si sa configuration change :

```yaml
---
# handlers file for ansible-files/roles/apache
- name: Reload Firewall
  ansible.builtin.service:
    name: firewalld
    state: reloaded
```

5. Créer et Déployer le Modèle :

Utilisez un modèle Jinja2 pour un `index.html` personnalisé. Stockez le modèle dans `templates/index.html.j2` :

```html
<html>
<head>
<title>Welcome to {{ ansible_hostname }}</title>
</head>
<body>
 <h1>Hello from {{ ansible_hostname }}</h1>
</body>
</html>
```

6. Mettre à jour `tasks/main.yml` pour déployer ce modèle `index.html` :

```yaml
- name: Deploy custom index.html
  ansible.builtin.template:
    src: index.html.j2
    dest: /var/www/html/index.html
```

### Étape 4 - Intégration du Rôle dans un Playbook

Intégrez le rôle `apache` dans un playbook nommé `deploy_apache.yml` situé dans `/home/student/lab_inventory` pour l'appliquer à vos hôtes du groupe 'web' (node1, node2, node3).

```yaml
- name: Setup Apache Web Servers
  hosts: web
  become: true
  roles:
    - apache
```

### Étape 5 - Exécution et Validation du Rôle

Lancez votre playbook pour configurer Apache sur les serveurs web désignés :

```bash
ansible-navigator run deploy_apache.yml -m stdout
```

#### Sortie :

```plaintext
PLAY [Setup Apache Web Servers] ************************************************

TASK [Gathering Facts] *********************************************************
ok: [node2]
ok: [node1]
ok: [node3]

TASK [apache : Install Apache web server] **************************************
changed: [node1]
changed: [node2]
changed: [node3]

TASK [apache : Ensure Apache is running and enabled] ***************************
changed: [node2]
changed: [node1]
changed: [node3]

TASK [apache : Deploy custom index.html] ***************************************
changed: [node1]
changed: [node2]
changed: [node3]

RUNNING HANDLER [apache : Reload Firewall] *************************************
ok: [node2]
ok: [node1]
ok: [node3]

PLAY RECAP *********************************************************************
node1                      : ok=5    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node2                      : ok=5    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node3                      : ok=5    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

### Étape 6 - Vérification du Fonctionnement d'Apache

Une fois le playbook terminé, vérifiez que `httpd` fonctionne bien sur tous les nœuds web.

```bash
[rhel@control ~]$ ssh node1 "systemctl status httpd"
● httpd.service - The Apache HTTP Server
   Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2024-01-29 16:49:13 UTC; 3min 46s ago
```

```bash
[rhel@control ~]$ ssh node2 "systemctl status httpd"
● httpd.service - The Apache HTTP Server
   Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2024-01-29 16:49:13 UTC; 3min 58s ago
```

Une fois que `httpd` a été vérifié comme étant en fonctionnement, vérifiez si le serveur web Apache sert bien le fichier `index.html` approprié :

```bash
[student@ansible-1 lab_inventory]$ curl http://node1
<html>
<head>
<title>Welcome to node1</title>
</head>
<body>
 <h1>Hello from node1</h1>
</body>
</html>
```


---
**Navigation**
<br>
[Exercice précédent](../1.6-templates/README.fr.md) - [Exercice suivant](../1.8-troubleshoot/README.fr.md)

[Cliquez ici pour revenir à l'atelier Ansible pour Red Hat Enterprise Linux](../README.md#section-1---ansible-engine-exercises)

