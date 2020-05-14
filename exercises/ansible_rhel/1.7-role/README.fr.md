# Atelier - Rôles: Rendre vos playbook réutilisables

**Lisez ceci dans d'autres langues**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table des matières

* [Objectif](#objectif)
* [Guide](#guide)
* [Étape 1 - Comprendre la structure des rôles](#étape-1---comprendre-la-structure-des-rôles)
* [Étape 2 - Création d'un rôle de base](#étape-2---création-d-un-rôle-de-base)
* [Étape 3 - Création du fichier de tâches](#étape-3---création-du-fichier-de-tâches)
* [Étape 4 - Création du handler](#étape-4---création-du-handler)
* [Étape 5 - Création des templates](#étape-5---création-des-templates)
* [Étape 6 - Teste du rôle](#étape-6---teste-du-rôle)

# Objectif

Bien qu'il soit possible d'écrire un playbook dans un fichier comme nous l'avons fait tout au long de cet atelier, vous souhaiterez éventuellement réutiliser des fichiers et commencer à organiser les choses.

Les rôles Ansible sont notre façon de procéder. Lorsque vous créez un rôle, vous déconstruisez votre playbook en parties et ces parties se trouvent dans une structure de répertoires. Ceci est expliqué plus en détail dans la [meilleure pratique](http://docs.ansible.com/ansible/playbooks_best_practices.html).

Cet exercice couvrira:
- la structure des dossiers d'un rôle Ansible
- comment construire un rôle Ansible
- création d'un playbook pour utiliser et exécuter un rôle

# Guide

## Étape 1 - Comprendre la structure des rôles

Les rôles sont des éléments réutilisables comprenant des fichiers Ansible et a pour but de simplifier la gestion des fichiers référencés.

Les rôles suivent une structure de répertoires définie; un rôle est nommé par le répertoire de niveau supérieur. Certains sous-répertoires contiennent des fichiers YAML, nommés `main.yml`. Les sous-répertoires de fichiers et de template peuvent contenir des objets utilisés par les fichiers YAML.

Un exemple de structure de projet pourrait ressembler à ceci, le nom du rôle serait "apache":

```text
apache/
├── defaults
│   └── main.yml
├── files
├── handlers
│   └── main.yml
├── meta
│   └── main.yml
├── README.md
├── tasks
│   └── main.yml
├── templates
├── tests
│   ├── inventory
│   └── test.yml
└── vars
    └── main.yml
```

Les différents fichiers `main.yml` contiennent du contenu en fonction de leur emplacement dans la structure de répertoires indiquée ci-dessus. Par exemple, `vars/main.yml` fait référence à des variables, `handlers/main.yaml` décrit les handlers, etc. Notez que contrairement aux playbooks, les fichiers `main.yml` contiennent uniquement le contenu spécifique et non des informations supplémentaires sur le playbook comme les hôtes, `become` ou d'autres mots clés.

> **Astuce**
>
> Il existe en fait deux répertoires pour les variables: `vars` et `default`: les variables par défaut ont la priorité la plus faible et contiennent généralement des valeurs par défaut définies par les auteurs du rôle et sont souvent utilisées lorsqu'il est prévu que leurs valeurs soient remplacées. Les variables peuvent être définis dans `vars/main.yml` ou `defaults/main.yml`, mais pas aux deux endroits.

L'utilisation de rôles dans un Playbook est simplement:
```yaml
---
- name: launch roles
  hosts: web
  roles:
    - role1
    - role2
```

Pour chaque rôle, les tâches, les handlers et les variables de ce rôle seront inclus dans le Playbook, dans cet ordre. Toute tâche de copie, de script, de template ou d'inclusion peuvent référencer les fichiers par leur *nom de chemin absolu ou relatif*. Ansible les recherchera respectivement dans les fichiers en fonction de leur utilisation.

## Étape 2 - Création d un rôle de base

Ansible recherche les rôles dans un sous-répertoire appelé `roles` dans le répertoire du projet. Cela peut être remplacé dans la configuration Ansible. Chaque rôle a son propre répertoire. Pour faciliter la création d'un nouveau rôle, l'outil `ansible-galaxy` peut être utilisé.

> **Astuce**
>
> Ansible Galaxy est votre hub pour trouver, réutiliser et partager le meilleur contenu Ansible. `ansible-galaxy` aide à interagir avec Ansible Galaxy. Pour l'instant, nous allons simplement l'utiliser comme aide pour construire la structure du répertoire.

Bien, commençons à construire un rôle. Nous allons créer un rôle qui installe et configure Apache pour servir un `virtual host`. Exécutez ces commandes dans votre répertoire `~/ansible-files`:

```bash
[student<X>@ansible ansible-files]$ mkdir roles
[student<X>@ansible ansible-files]$ ansible-galaxy init --offline roles/apache_vhost
```

Jetez un œil aux répertoires de rôles et à leur contenu:

```bash
[student<X>@ansible ansible-files]$ tree roles
```

## Étape 3 - Création du fichier de tâches

Le fichier `main.yml` dans le sous-répertoire `tasks` du rôle doit faire ce qui suit:

   - S'assurer que httpd est installé

   - S'assurer que httpd est démarré et activé

   - Mettre du contenu HTML dans la racine du document Apache

   - Installer le template fourni pour configurer le vhost

> **AVERTISSEMENT**
>
> ** Le `main.yml` (et d'autres fichiers éventuellement inclus par main.yml) ne peut contenir que des tâches, et non de Playbook complet!**

Accédez au répertoire `roles/apache_vhost`. Editez le fichier `tasks/main.yml`:

```yaml
---
- name: install httpd
  yum:
    name: httpd
    state: latest

- name: start and enable httpd service
  service:
    name: httpd
    state: started
    enabled: true
```

Notez qu'ici, seules les tâches ont été ajoutées. Les détails d'un playbook ne sont pas présents.

Les tâches ajoutées jusqu'ici font:

   - Installez le package httpd à l'aide du module yum

   - Utilisez le module de service pour activer et démarrer httpd

Ensuite, nous ajoutons deux tâches supplémentaires pour garantir une structure de répertoire vhost et copier le contenu html:

<!-- {% raw %} -->
```yaml
- name: ensure vhost directory is present
  file:
    path: "/var/www/vhosts/{{ ansible_hostname }}"
    state: directory

- name: deliver html content
  copy:
    src: web.html
    dest: "/var/www/vhosts/{{ ansible_hostname }}/index.html"
```
<!-- {% endraw %} -->

Notez que le répertoire vhost est créé en utilisant le module `file`.

La dernière tâche que nous ajoutons utilise le module template pour créer le fichier de configuration vhost à partir d'un modèle j2:

```yaml
- name: template vhost file
  template:
    src: vhost.conf.j2
    dest: /etc/httpd/conf.d/vhost.conf
    owner: root
    group: root
    mode: 0644
  notify:
    - restart_httpd
```
Notez qu'il utilise un handler pour redémarrer httpd après une mise à jour de configuration.

Le fichier complet `tasks/main.yml` est:

<!-- {% raw %} -->
```yaml
---
- name: install httpd
  yum:
    name: httpd
    state: latest

- name: start and enable httpd service
  service:
    name: httpd
    state: started
    enabled: true

- name: ensure vhost directory is present
  file:
    path: "/var/www/vhosts/{{ ansible_hostname }}"
    state: directory

- name: deliver html content
  copy:
    src: web.html
    dest: "/var/www/vhosts/{{ ansible_hostname }}"

- name: template vhost file
  template:
    src: vhost.conf.j2
    dest: /etc/httpd/conf.d/vhost.conf
    owner: root
    group: root
    mode: 0644
  notify:
    - restart_httpd
```
<!-- {% endraw %} -->


## Étape 4 - Création du handler

Créez le handler dans le fichier `handlers/main.yml` pour redémarrer httpd lorsqu'il est notifié par la tâche de modèle:

```yaml
---
# handlers file for roles/apache_vhost
- name: restart_httpd
  service:
    name: httpd
    state: restarted
```

## Étape 5 - Création des templates

Créez le contenu HTML qui sera servi par le serveur Web.

   - Créez un fichier web.html dans le répertoire "src" du rôle, `files`:

```bash
[student<X>@ansible ansible-files]$ echo 'simple vhost index' > ~/ansible-files/roles/apache_vhost/files/web.html
```

- Créez le fichier de modèle `vhost.conf.j2` dans le sous-répertoire `templates` du rôle.

<!-- {% raw %} -->
```
# {{ ansible_managed }}

<VirtualHost *:8080>
    ServerAdmin webmaster@{{ ansible_fqdn }}
    ServerName {{ ansible_fqdn }}
    ErrorLog logs/{{ ansible_hostname }}-error.log
    CustomLog logs/{{ ansible_hostname }}-common.log common
    DocumentRoot /var/www/vhosts/{{ ansible_hostname }}/

    <Directory /var/www/vhosts/{{ ansible_hostname }}/>
  Options +Indexes +FollowSymlinks +Includes
  Order allow,deny
  Allow from all
    </Directory>
</VirtualHost>
```
<!-- {% endraw %} -->

## Étape 6 - Teste du rôle

Vous êtes prêt à tester le rôle sur `node2`. Mais comme un rôle ne peut pas être attribué directement à un nœud, créez d'abord un playbook qui connecte le rôle et l'hôte. Créez le fichier `test_apache_role.yml` dans le répertoire `~/ansible-files`:

```yaml
---
- name: use apache_vhost role playbook
  hosts: node2
  become: yes

  pre_tasks:
    - debug:
        msg: 'Beginning web server configuration.'

  roles:
    - apache_vhost

  post_tasks:
    - debug:
        msg: 'Web server has been configured.'
```

Notez les mots clés `pre_tasks` et `post_tasks`. Normalement, les tâches des rôles s'exécutent avant les tâches d'un playbook. Pour contrôler l'ordre d'exécution, des `pre_tasks` sont effectuées avant l'application des rôles. Les `post_tasks` sont effectués une fois tous les rôles terminés. Ici, nous les utilisons simplement pour mieux mettre en évidence lorsque le rôle réel est exécuté.

Vous êtes maintenant prêt à exécuter votre playbook:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook test_apache_role.yml
```

Exécutez une commande curl contre `node2` pour confirmer que le rôle a fonctionné:

```bash
[student<X>@ansible ansible-files]$ curl -s http://node2:8080
simple vhost index
```

Tout va bien? Toutes nos félicitations! Vous avez terminé avec succès les exercices d'atelier Ansible Engine!

----
**Navigation**
<br>
[Exercise précédent](../1.6-templates/README.fr.md)

[Cliquez ici pour revenir à l'atelier Ansible pour Red Hat Enterprise Linux](../README.fr.md)
