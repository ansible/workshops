# Exercice de l'Atelier - Modèles

**Lisez ceci dans d'autres langues** :
<br>![uk](../../../images/uk.png) [Anglais](README.md), ![japan](../../../images/japan.png) [Japonais](README.ja.md), ![brazil](../../../images/brazil.png) [Portugais du Brésil](README.pt-br.md), ![france](../../../images/fr.png) [Français](README.fr.md), ![Español](../../../images/col.png) [Espagnol](README.es.md).

## Table des Matières

- [Exercice de l'Atelier - Modèles](#exercice-de-latelier---modèles)
  - [Table des Matières](#table-des-matières)
  - [Objectif](#objectif)
  - [Guide](#guide)
    - [Étape 1 - Introduction à la Templatisation Jinja2](#étape-1---introduction-à-la-templatisation-jinja2)
    - [Étape 2 - Création de Votre Premier Modèle](#étape-2---création-de-votre-premier-modèle)
      - [Configuration du Répertoire des Modèles :](#configuration-du-répertoire-des-modèles-)
      - [Développement du Modèle MOTD :](#développement-du-modèle-motd-)
    - [Étape 3 - Déploiement du Modèle avec un Playbook](#étape-3---déploiement-du-modèle-avec-un-playbook)
    - [Étape 4 - Exécution du Playbook](#étape-4---exécution-du-playbook)

## Objectif

L'Exercice 1.5 introduit la templatisation Jinja2 au sein d'Ansible, une fonctionnalité puissante pour générer des fichiers dynamiques à partir de modèles. Vous apprendrez à créer des modèles qui intègrent des données spécifiques à l'hôte, permettant la création de fichiers de configuration sur mesure pour chaque hôte géré.

## Guide

### Étape 1 - Introduction à la Templatisation Jinja2

Ansible utilise Jinja2, un langage de templatisation largement utilisé pour Python, permettant la génération de contenu dynamique dans les fichiers. Cette capacité est particulièrement utile pour configurer des fichiers qui doivent différer d'un hôte à l'autre.

### Étape 2 - Création de Votre Premier Modèle

<!-- {% raw %} -->
Les modèles se terminent par une extension `.j2` et mélangent du contenu statique avec des espaces réservés dynamiques entourés de `{{ }}`.
<!-- {% endraw %} -->

Dans l'exemple suivant, créons un modèle pour le Message du Jour (MOTD) qui inclut des informations dynamiques sur l'hôte.

#### Configuration du Répertoire des Modèles :

Assurez-vous qu'un répertoire de modèles existe dans votre répertoire lab_inventory pour organiser vos modèles.

```bash
mkdir -p ~/lab_inventory/templates
```

#### Développement du Modèle MOTD :

Créez un fichier nommé `motd.j2` dans le répertoire des modèles avec le contenu suivant :

<!-- {% raw %} -->

```jinja
Bienvenue sur {{ ansible_hostname }}.
OS : {{ ansible_distribution }} {{ ansible_distribution_version }}
Architecture : {{ ansible_architecture }}
```

<!-- {% endraw %} -->

Ce modèle affiche dynamiquement le nom d'hôte, la distribution de l'OS, la version et l'architecture de chaque hôte géré.

### Étape 3 - Déploiement du Modèle avec un Playbook

Utilisez le module `ansible.builtin.template` dans un playbook pour distribuer et rendre le modèle sur vos hôtes gérés.

Modifiez le playbook `system_setup.yml` avec le contenu suivant :

```yaml
---
- name: Configuration Système de Base
  hosts: all
  become: true
  vars:
    user_name: 'Roger'
    package_name: httpd
  tasks:
    - name: Mettre à jour tous les paquets liés à la sécurité
      ansible.builtin.package:
        name: '*'
        state: latest
        security: true
        update_only: true
    - name: Créer un nouvel utilisateur
      ansible.builtin.user:
        name: "{{ user_name }}"
        state: present
        create_home: true
    - name: Installer Apache sur les serveurs web
      ansible.builtin.package:
        name: "{{ package_name }}"
        state: present
      when: inventory_hostname in groups['web']
    - name: Installer firewalld
      ansible.builtin.package:
        name: firewalld
        state: present
      when: inventory_hostname in groups['web']
    - name: S'assurer que firewalld est en cours d'exécution
      ansible.builtin.service:
        name: firewalld
        state: started
        enabled: true
      when: inventory_hostname in groups['web']
    - name: Autoriser le trafic HTTP sur les serveurs web
      ansible.posix.firewalld:
        service: http
        permanent: true
        state: enabled
      when: inventory_hostname in groups['web']
      notify: Recharger le Pare-feu
    - name: Mettre à jour MOTD depuis le modèle Jinja2
      ansible.builtin.template:
        src: templates/motd.j2
        dest: /etc/motd
  handlers:
    - name: Recharger le Pare-feu
      ansible.builtin.service:
        name: firewalld
        state: reloaded
```

Le module `ansible.builtin.template` prend le modèle `motd.j2` et génère un fichier `/etc/motd` sur chaque hôte, en remplissant les espaces réservés du modèle avec les faits réels de l'hôte.

### Étape 4 - Exécution du Playbook

Exécutez le playbook pour appliquer votre MOTD personnalisé sur tous les hôtes gérés :

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_setup.yml -m stdout
```

```plaintext
PLAY [Configuration Système de Base] *******************************************
.
.
.

TASK [Mise à jour de MOTD à partir du modèle Jinja2] ***************************
changed: [node1]
changed: [node2]
changed: [node3]
changed: [ansible-1]

RECAP *************************************************************************
ansible-1                  : ok=6    changed=1    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
node1                      : ok=8    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node2                      : ok=8    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node3                      : ok=8    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Vérifiez les changements en vous connectant au nœud via SSH, et vous devriez voir le message du jour:

```plaintext
[rhel@control ~]$ ssh node1

Welcome to node1.
OS: RedHat 8.7
Architecture: x86_64
Register this system with Red Hat Insights: insights-client --register
Create an account or view all your systems at https://red.ht/insights-dashboard
Last login: Mon Jan 29 16:30:31 2024 from 10.5.1.29
```

Quittez la session SSH pour retourner à votre nœud de contrôle avant de continuer vers l'exercice suivant :

```plaintext
[rhel@node1 ~]$ exit
logout
Connection to node1 closed.
[rhel@control ~]$
```

----
**Navigation**
<br>
[Exercise précédent](../1.5-handlers/README.fr.md) - [Exercise suivant](../1.7-role/README.fr.md)

[Cliquez ici pour revenir à l'atelier Ansible pour Red Hat Enterprise Linux](../README.fr.md)
