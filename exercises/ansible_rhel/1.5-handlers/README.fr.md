# Exercice de l'Atelier - Conditionnels, Gestionnaires et Boucles

**Lisez ceci dans d'autres langues** :
<br>![uk](../../../images/uk.png) [Anglais](README.md), ![japan](../../../images/japan.png) [日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugais du Brésil](README.pt-br.md), ![france](../../../images/fr.png) [Français](README.fr.md), ![Español](../../../images/col.png) [Espagnol](README.es.md).

# Exercices de l'Atelier - Utilisation des Conditionnels, Gestionnaires et Boucles

## Table des Matières

- [Objectif](#objectif)
- [Guide](#guide)
  - [Étape 1 - Comprendre les Conditionnels, Gestionnaires et Boucles](#étape-1---comprendre-les-conditionnels-gestionnaires-et-boucles)
  - [Étape 2 - Conditionnels](#étape-2---conditionnels)
  - [Étape 3 - Gestionnaires](#étape-3---gestionnaires)
  - [Étape 4 - Boucles](#étape-4---boucles)

## Objectif

En élargissant l'exercice 1.4, cet exercice introduit l'application des conditionnels, gestionnaires et boucles dans les playbooks Ansible. Vous apprendrez à contrôler l'exécution des tâches avec des conditionnels, à gérer les réponses des services avec des gestionnaires et à gérer efficacement les tâches répétitives à l'aide de boucles.

## Guide

Les conditionnels, gestionnaires et boucles sont des fonctionnalités avancées dans Ansible qui améliorent le contrôle, l'efficacité et la flexibilité dans vos playbooks d'automatisation.

### Étape 1 - Comprendre les Conditionnels, Gestionnaires et Boucles

- **Conditionnels** : Permettent l'exécution des tâches basée sur des conditions spécifiques.
- **Gestionnaires** : Tâches spéciales déclenchées par une directive `notify`, généralement utilisées pour redémarrer les services après des modifications.
- **Boucles** : Utilisées pour répéter une tâche plusieurs fois, particulièrement utile lorsque la tâche est similaire mais doit être appliquée à différents éléments.

### Étape 2 - Conditionnels

Les conditionnels dans Ansible contrôlent si une tâche doit être exécutée en fonction de certaines conditions.
Ajoutons à notre playbook system_setup.yml la capacité d'installer le Serveur HTTP Apache (`httpd`) uniquement sur les hôtes qui appartiennent au groupe `web` dans notre inventaire.

> REMARQUE : Les exemples précédents avaient des hôtes définis sur node1 mais maintenant il est défini sur all. Cela signifie que lorsque vous exécutez ce playbook Ansible mis à jour, vous remarquerez des mises à jour pour les nouveaux systèmes automatisés, l'utilisateur Roger créé sur tous les nouveaux systèmes et le paquet du serveur web Apache httpd installé sur tous les hôtes du groupe web.

<!-- {% raw %} -->

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
      ansible.builtin.dnf:
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
      ansible.builtin.dnf:
        name: "{{ package_name }}"
        state: present
      when: inventory_hostname in groups['web']
```

<!-- {% raw %} -->

Dans cet exemple, `inventory_hostname in groups['web']` est la déclaration conditionnelle. `inventory_hostname` fait référence au nom de l'hôte actuel sur lequel Ansible travaille dans le playbook. La condition vérifie si cet hôte fait partie du groupe web défini dans votre fichier d'inventaire. Si c'est vrai, la tâche s'exécutera et installera Apache sur cet hôte.

### Étape 3 - Gestionnaires

Les gestionnaires sont utilisés pour les tâches qui ne doivent s'exécuter que lorsqu'elles sont notifiées par une autre tâche. Typiquement, ils sont utilisés pour redémarrer les services après un changement de configuration.

Disons que nous voulons nous assurer que le pare-feu est correctement configuré sur tous les serveurs web, puis recharger le service pare-feu pour appliquer les nouveaux paramètres. Nous définirons un gestionnaire qui recharge le service pare-feu et est notifié par une tâche qui assure que les règles de pare-feu souhaitées sont en place :

<!-- {% raw %} -->

```yaml
---
- name: Configuration Système de Base
  hosts: all
  become: true
  .
  .
  .
    - name: Installer firewalld
      ansible.builtin.dnf:
        name: firewalld
        state: present

    - name: S'assurer que firewalld est en cours d'exécution
      ansible.builtin.service:
        name: firewalld
        state: started
        enabled: true

    - name: Autoriser le trafic HTTPS sur les serveurs web
      ansible.posix.firewalld:
        service: https
        permanent: true
        state: enabled
      when: inventory_hostname in groups['web']
      notify: Recharger le Pare-feu

  handlers:
    - name: Recharger le Pare-feu
      ansible.builtin.service:
        name: firewalld
        state: reloaded

```

<!-- {% raw %} -->

Le gestionnaire Recharger le Pare-feu est déclenché uniquement si la tâche "Autoriser le trafic HTTPS sur les serveurs web" effectue des modifications.

> REMARQUE : Remarquez comment le nom du gestionnaire est utilisé dans la section notify de la tâche de configuration "Recharger le Pare-feu". Cela garantit que le bon gestionnaire est exécuté car il peut y avoir plusieurs gestionnaires dans un playbook Ansible.

```
PLAY [Configuration Système de Base] ******************************************************

TASK [Collecte des Faits] *********************************************************
ok: [node1]
ok: [node2]
ok: [ansible-1]
ok: [node3]

TASK [Mettre à jour tous les paquets liés à la sécurité] ************************************
ok: [node2]
ok: [node1]
ok: [ansible-1]
ok: [node3]

TASK [Créer un nouvel utilisateur] *******************************************************
ok: [node1]
ok: [node2]
ok: [ansible-1]
ok: [node3]

TASK [Installer Apache sur les serveurs web] *******************************************
skipping: [ansible-1]
ok: [node2]
ok: [node1]
ok: [node3]

TASK [Installer firewalld] *******************************************************
changed: [ansible-1]
changed: [node2]
changed: [node1]
changed: [node3]

TASK [S'assurer que firewalld est en cours d'exécution] *********************************************
changed: [node3]
changed: [ansible-1]
changed: [node2]
changed: [node1]

TASK [Autoriser le trafic HTTPS sur les serveurs web] **************************************
skipping: [ansible-1]
changed: [node2]
changed: [node1]
changed: [node3]

GESTIONNAIRE EN COURS [Recharger le Pare-feu] **********************************************
changed: [node2]
changed: [node1]
changed: [node3]

COMPTE RENDU DU JEU *********************************************************************
ansible-1                  : ok=5    changed=2    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
node1                      : ok=8    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node2                      : ok=8    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node3                      : ok=8    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

```

### Étape 4 - Boucles

Les boucles dans Ansible vous permettent d'effectuer une tâche plusieurs fois avec différentes valeurs. Cette fonctionnalité est particulièrement utile pour des tâches comme la création de plusieurs comptes utilisateurs dans notre exemple donné.
Dans le playbook system_setup.yml original de l'exercice 1.4, nous avions une tâche pour créer un seul utilisateur :

<!-- {% raw %} -->

```yaml
- name: Créer un nouvel utilisateur
  ansible.builtin.user:
    name: "{{ user_name }}"
    state: present
    create_home: true

```
<!-- {% raw %} -->

Maintenant, modifions cette tâche pour créer plusieurs utilisateurs à l'aide d'une boucle :

<!-- {% raw %} -->

```yaml
- name: Créer un nouvel utilisateur
  ansible.builtin.user:
    name: "{{ item }}"
    state: present
    create_home: true
  loop:
    - alice
    - bob
    - carol
```

<!-- {% raw %} -->

<!-- {% raw %} -->

Qu'est-ce qui a changé ?

1. Directive de Boucle : Le mot-clé loop est utilisé pour itérer sur une liste d'éléments. Dans ce cas, la liste contient les noms des utilisateurs que nous souhaitons créer : alice, bob et carol.

2. Création d'Utilisateurs avec Boucle : Au lieu de créer un seul utilisateur, la tâche modifiée itère maintenant sur chaque élément de la liste de boucle. Le placeholder `{{ item }}` est dynamiquement remplacé par chaque nom d'utilisateur dans la liste, de sorte que le module ansible.builtin.user crée chaque utilisateur à son tour.
<!-- {% raw %} -->

Lorsque vous exécutez le playbook mis à jour, cette tâche est exécutée trois fois, une fois pour chaque utilisateur spécifié dans la boucle. C'est une manière efficace de gérer les tâches répétitives avec des données d'entrée variables.

Extrait de la sortie pour la création d'un nouvel utilisateur sur tous les nœuds.

```bash
[student@ansible-1 ~lab_inventory]$ ansible-navigator run system_setup.yml -m stdout

PLAY [Configuration Système de Base] ******************************************************

.
.
.

TASK [Créer un nouvel utilisateur] *******************************************************
changed: [node2] => (item=alice)
changed: [ansible-1] => (item=alice)
changed: [node1] => (item=alice)
changed: [node3] => (item=alice)
changed: [node1] => (item=bob)
changed: [ansible-1] => (item=bob)
changed: [node3] => (item=bob)
changed: [node2] => (item=bob)
changed: [node1] => (item=carol)
changed: [node3] => (item=carol)
changed: [ansible-1] => (item=carol)
changed: [node2] => (item=carol)

.
.
.


COMPTE RENDU DU JEU *********************************************************************
ansible-1                  : ok=5    changed=1    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
node1                      : ok=7    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node2                      : ok=7    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node3                      : ok=7    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```



----
**Navigation**
<br>
[Exercise précédent](../1.4-variables/README.fr.md) - [Exercise suivant](../1.6-templates/README.fr.md)

[Cliquez ici pour revenir à l'atelier Ansible pour Red Hat Enterprise Linux](../README.fr.md)


