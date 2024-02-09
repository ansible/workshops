# Exercice de l'Atelier - Rédaction de Votre Premier Playbook

**Lire ceci dans d'autres langues** :
<br>![uk](../../../images/uk.png) [Anglais](README.md), ![japan](../../../images/japan.png) [日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugais du Brésil](README.pt-br.md), ![france](../../../images/fr.png) [Français](README.fr.md), ![Español](../../../images/col.png) [Espagnol](README.es.md).

## Table des Matières

- [Exercice de l'Atelier - Rédaction de Votre Premier Playbook](#exercice-de-latelier---rédaction-de-votre-premier-playbook)
  - [Objectif](#objectif)
  - [Guide](#guide)
    - [Étape 1 - Les Bases du Playbook](#étape-1---les-bases-du-playbook)
    - [Étape 2 - Création de Votre Playbook](#étape-2---création-de-votre-playbook)
    - [Étape 3 - Exécution du Playbook](#étape-3---exécution-du-playbook)
    - [Étape 4 - Vérification du Playbook](#étape-4---vérification-du-playbook)


## Objectif

Dans cet exercice, vous utiliserez Ansible pour effectuer des tâches de configuration système de base sur un serveur Red Hat Enterprise Linux. Vous vous familiariserez avec les modules fondamentaux d'Ansible comme `dnf` et `user`, et apprendrez à créer et exécuter des playbooks.

## Guide

Les playbooks dans Ansible sont essentiellement des scripts écrits au format YAML. Ils sont utilisés pour définir les tâches et configurations qu'Ansible appliquera à vos serveurs.

### Étape 1 - Les Bases du Playbook
Tout d'abord, créez un fichier texte au format YAML pour votre playbook. Souvenez-vous :
- Commencez par trois tirets (`---`).
- Utilisez des espaces, pas des tabulations, pour l'indentation.

Concepts Clés :
- `hosts` : Spécifie les serveurs ou appareils cibles sur lesquels votre playbook s'exécutera.
- `tasks` : Les actions qu'Ansible effectuera.
- `become` : Permet l'escalade de privilèges (exécution de tâches avec des privilèges élevés).

> NOTE : Un playbook Ansible est conçu pour être idempotent, ce qui signifie que si vous l'exécutez plusieurs fois sur les mêmes hôtes, il assure l'état souhaité sans effectuer de changements redondants.

### Étape 2 - Création de Votre Playbook
Avant de créer votre premier playbook, assurez-vous d'être dans le bon répertoire en changeant pour `~/lab_inventory` :

```bash
cd ~/lab_inventory
```

Créez maintenant un playbook nommé `system_setup.yml` pour effectuer la configuration système de base :
- Mettre à jour tous les paquets liés à la sécurité.
- Créer un nouvel utilisateur nommé ‘myuser’.

La structure de base se présente comme suit :

```yaml
---
- name: Basic System Setup
  hosts: node1
  become: true
  tasks:
    - name: Update all security-related packages
      ansible.builtin.dnf:
        name: '*'
        state: latest
        security: true

    - name: Create a new user
      ansible.builtin.user:
        name: myuser
        state: present
        create_home: true
```

> NOTE : La mise à jour des paquets peut prendre quelques minutes avant la fin de l'exécution du playbook Ansible.

* À propos du module `dnf` : Ce module est utilisé pour la gestion des paquets avec DNF (YUM Dandifié) sur RHEL et d'autres systèmes basés sur Fedora.

* À propos du module `user` : Ce module est utilisé pour gérer les comptes d'utilisateurs.

### Étape 3 - Exécution du Playbook

Exécutez votre playbook en utilisant la commande `ansible-navigator` :

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_setup.yml -m stdout
```

Revoyez la sortie pour vous assurer que chaque tâche est terminée avec succès.

### Étape 4 - Vérification du Playbook
Maintenant, créons un second playbook pour les vérifications post-configuration, nommé `system_checks.yml` :

```yaml
---
- name: System Configuration Checks
  hosts: node1
  become: true
  tasks:
    - name: Check user existence
      ansible.builtin.command:
        cmd: id myuser
      register: user_check

    - name: Report user status
      ansible.builtin.debug:
        msg: "L'utilisateur 'myuser' existe."
      when: user_check.rc == 0
```

Exécutez le playbook de vérifications :

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_checks.yml -m stdout
```

Revoyez la sortie pour vous assurer que la création de l'utilisateur a été réussie.

---
**Navigation**
<br>

{% if page.url contains 'ansible_rhel_90' %}
[Exercise précédent](../2-thebasics/README.fr.md) - [Exercise suivant](../4-variables/README.fr.md)
{% else %}
[Exercise précédent](../1.2-thebasics/README.fr.md) - [Exercise suivant](../1.4-variables/README.fr.md)
{% endif %}
<br><br>
