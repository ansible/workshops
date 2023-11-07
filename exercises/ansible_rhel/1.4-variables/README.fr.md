# Exercice - Utilisation des variables

**Lisez ceci dans d'autres langues**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Français](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table des matières

* [Objectif](#objectif)
* [Guide](#guide)
* [Introduction aux variables](#introduction-aux-variables)
* [Étape 1 - Création des fichiers de variables](#Étape-1---Création-des-fichiers-de-variables)
* [Étape 2 - Création des fichiers html](#Étape-2---Création-des-fichiers-html)
* [Étape 3 - Création du Playbook](#Étape-3---Création-du-playbook)
* [Étape 4 - Teste du résultat](#Étape-4---teste-du-résultat)
* [Étape 5 - Les Faits Ansible](#Étape-5---les-faits-ansible)
* [Étape 6 - Défi: Les faits](#Étape-6---défi-les-faits)
* [Étape 7 - Utilisation des faits dans un playbook](#Étape-7---utilisation-des-faits-dans-un-playbook)

# Objectif

Ansible prend en charge des variables pour stocker des valeurs pouvant être utilisées dans Playbooks. Les variables peuvent être définies à divers endroits et ont une précédence claire. Ansible remplace la variable par sa valeur lorsqu'une tâche est exécutée.

Cet exercice couvre des variables, en particulier
* Comment utiliser les délimiteurs de variables `{{` et `}}`
* Qu'est-ce que `host_vars` et `group_vars` et quand les utiliser
* Comment utiliser `ansible_facts`
* Comment utiliser le module `debug` pour imprimer des variables dans la fenêtre de la console

## Guide

### Introduction aux variables

Les variables sont référencées dans les Playbooks en plaçant le nom de la variable entre deux accolades:

<!-- {% raw %} -->

```yaml
Here comes a variable {{ variable1 }}
```

<!-- {% endraw %} -->

Les variables et leurs valeurs peuvent être définies à différents endroits: l'inventaire, les fichiers supplémentaires, sur la ligne de commande, etc.

La pratique recommandée pour fournir des variables dans l'inventaire est de les définir dans des fichiers situés dans deux répertoires nommés `host_vars` et `group_vars`:
* Pour définir des variables pour un groupe `serveurs`, utilisez un fichier YAML nommé `group_vars/servers.yml` pour la définitions des variables.
* Pour définir des variables spécifiquement pour un hôte `node1`, utilisez le fichier `host_vars/node1.yml` pour la définition des variables.

> **Astuce**
>
> Les variables hôtes ont priorité sur les variables de groupe (plus d'informations sur la priorité peuvent être trouvées dans la [documentation](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable).

### Step 1 -  Création des fichiers de variables

Pour comprendre et pratiquer, faisons un exercice. Dans le prolongement du thème "Construisons un serveur Web. Ou deux. Ou même plus ...", vous allez changer le `index.html` pour montrer l'environnement de développement (dev/prod) dans lequel un serveur est déployé.

Sur l'hôte de contrôle Ansible, en tant qu'utilisateur `student`, créez les répertoires pour contenir les définitions des variables dans `~/ansible-files/`:

```bash
[student@ansible-1 ansible-files]$ mkdir host_vars group_vars
```

Créez maintenant deux fichiers contenant des définitions de variables. Nous allons définir une variable nommée `stage` qui pointera vers différents environnements, `dev` ou `prod`:

* Créez le fichier `~/ansible-files/group_vars/web.yml` avec ce contenu:

```yaml
---
stage: dev
```

* Créez le fichier `~/ansible-files/host_vars/node2.yml` avec ce contenu:

```yaml
---
stage: prod
```

De quoi s'agit-il ?

* Pour tous les serveurs du groupe `web`, la variable `stage` avec la valeur `dev` est définie. Donc, par défaut, nous les signalons comme membres de l'environnement de développement.
* Pour le serveur `node2`, la declaration ci-dessus est remplacé et l'hôte est marqué comme serveur de production.

### Step 2 - Création des fichiers html

Créez maintenant deux fichiers dans `~/ansible-files/files/`:

L'un appelé `prod_web.html` avec le contenu suivant:

```html
<body>
<h1>This is a production webserver, take care!</h1>
</body>
```

Et l'autre appelé `dev_web.html` avec comme contenu:

```html
<body>
<h1>This is a development webserver, have fun!</h1>
</body>
```

### Step 3 - Création du Playbook

Vous avez maintenant besoin d'un Playbook qui copie le fichier prod ou dev `web.html` - selon la variable "stage".

Créez un nouveau Playbook appelé `deploy_index_html.yml` dans le répertoire `~/ansible-files/`.

> **Astuce**
>
> Notez comment la variable "stage" est utilisée dans le nom du fichier à copier.

<!-- {% raw %} -->

```yaml
---
- name: Copy web.html
  hosts: web
  become: true
  tasks:
  - name: copy web.html
    ansible.builtin.copy:
      src: "{{ stage }}_web.html"
      dest: /var/www/html/index.html
```

<!-- {% endraw %} -->

* Lancez le Playbook:

```bash
[student@ansible-1 ansible-files]$ ansible-navigator run deploy_index_html.yml
```

### Step 4 - Testez le résultat

Le Playbook Ansible copie différents fichiers index.html sur les hôtes, utilisez `curl` pour le tester. 

Pour node1:

```bash
[student@ansible-1 ansible-files]$ curl http://node1
<body>
<h1>This is a development webserver, have fun!</h1>
</body>
```

Pour node2:

```bash
[student@ansible-1 ansible-files]$ curl http://node2
<body>
<h1>This is a production webserver, take care!</h1>
</body>
```

Pour node3:

```bash
[student@ansible-1 ansible-files]$ curl http://node3
<body>
<h1>This is a development webserver, have fun!</h1>
</body>
```

> **Astuce**
>
> Si vous êtes en train de penser: il doit y avoir un moyen plus intelligent de modifier le contenu des fichiers… vous avez absolument raison. Cet exercice a été fait pour introduire les variables, vous êtes sur le point d'en apprendre davantage sur les modèles dans l'un des chapitres suivants.

### Step 5 - Les Faits Ansible

Les faits Ansible sont des variables qui sont automatiquement découvertes par Ansible sur un hôte géré. Vous souvenez-vous de la tâche "Gathering Facts" répertoriée dans la sortie de chaque exécution de `ansible-navigator`? À ce moment, les Faits sont collectés pour chaque noeud géré. Les Faits peuvent également être collectés par le module `setup`. Ils contiennent des informations utiles stockées dans des variables que les administrateurs peuvent réutiliser.

Pour avoir une idée des Faits collectés par défaut par Ansible, sur votre noeud de contrôle avec votre utilisateur `student`, lancez le Playbook suivant pour obtenir les détails de `setup` sur `node1`:

```yaml
---
- name: Capture Setup
  hosts: node1

  tasks:

    - name: Collect only facts returned by facter
      ansible.builtin.setup:
        gather_subset:
        - 'all'
      register: setup

    - ansible.builtin.debug:
        var: setup
```

```bash
[student@ansible-1 ansible-files]$ cd ~
[student@ansible-1 ~]$ ansible-navigator run setup.yml -m stdout
```

C'est peut être un peu trop d'information, vous pouvez utiliser des filtres pour limiter la sortie à certains faits, l'expression est un caractère wildcard de style shell dans votre Playbook. Créez un Playbook intitulé `setup_filter.yml` comme indiqué ci-dessous. Dans cet exemple, on filtre pour obtenir les Faits `eth0` ainsi que le détail sur la mémoire de `node1`.

```yaml
---
- name: Capture Setup
  hosts: node1

  tasks:

    - name: Collect only specific facts
      ansible.builtin.setup:
        filter:
        - 'ansible_eth0'
        - 'ansible_*_mb'
      register: setup

    - debug:
        var: setup
```

```bash
[student@ansible-1 ansible-files]$ ansible-navigator run setup_filter.yml -m stdout
```

### Step 6 - Défi: Les Faits

* Essayez de trouver et d'imprimer la distribution (Red Hat) de vos hôtes gérés en utilisant un playbook.

> **Astuce**
>
> Utilisez un caractère wildcard pour trouver le Fait dans votre filtre, puis appliquez un filtre pour imprimer uniquement ce fait.

> **Avertissement **
>
> **Solution ci-dessous \!**

```yaml
---
- name: Capture Setup
  hosts: node1

  tasks:

    - name: Collect only specific facts
      ansible.builtin.setup:
        filter:
        - '*distribution'
      register: setup

    - ansible.builtin.debug:
        var: setup
```

Avec le caractère wildcard, la sortie montre:

```bash

TASK [debug] *******************************************************************
ok: [ansible] => {
    "setup": {
        "ansible_facts": {
            "ansible_distribution": "RedHat"
        },
        "changed": false,
        "failed": false
    }
}
```

Avec ceci, on peut conclure que la variable qu'on cherche est intitulée `ansible_distribution`.

On peut maintenant mettre à jour le playbook pour être explicite dans sa recherche et changer la ligne suivante:

```yaml
filter:
- '*distribution'
```

en:

```yaml
filter:
- 'ansible_distribution'
```

```bash
[student@ansible-1 ansible-files]$ ansible-navigator run setup_filter.yml -m stdout
```

### Step 7 - Utilisation des Faits dans un Playbook

Les faits peuvent être utilisés dans un Playbook comme des variables, en utilisant le bon nom, bien sûr. Créez ce Playbook nommé `facts.yml` dans le répertoire `~/ansible-files/`:

<!-- {% raw %} -->

```yaml
---
- name: Output facts within a playbook
  hosts: all
  tasks:
  - name: Prints Ansible facts
    ansible.builtin.debug:
      msg: The default IPv4 address of {{ ansible_fqdn }} is {{ ansible_default_ipv4.address }}
```

<!-- {% endraw %} -->

> **Astuce**
>
> Le module "debug" peut être pratique pour débugger les variables ou expressions.

Exécutez-le pour voir comment les faits sont affichés:

```bash
[student@ansible-1 ansible-files]$ ansible-navigator run facts.yml
```

Dans l'interface texte (TUI), tapez  `:st` pour capturer la sortie suivante:

```bash
PLAY [Output facts within a playbook] ******************************************

TASK [Gathering Facts] *********************************************************
ok: [node3]
ok: [node2]
ok: [node1]
ok: [ansible-1]

TASK [Prints Ansible facts] ****************************************************
ok: [node1] =>
  msg: The default IPv4 address of node1 is 172.16.190.143
ok: [node2] =>
  msg: The default IPv4 address of node2 is 172.16.30.170
ok: [node3] =>
  msg: The default IPv4 address of node3 is 172.16.140.196
ok: [ansible-1] =>
  msg: The default IPv4 address of ansible is 172.16.2.10

PLAY RECAP *********************************************************************
ansible-1                  : ok=2    changed=0    unreachable=0    failed=0
node1                      : ok=2    changed=0    unreachable=0    failed=0
node2                      : ok=2    changed=0    unreachable=0    failed=0
node3                      : ok=2    changed=0    unreachable=0    failed=0
```

---
**Navigation**
<br>

{% if page.url contains 'ansible_rhel_90' %}
[Exercise précédent](../3-playbook/README.fr.md) - [Exercise suivant](../5-surveys/README.fr.md)
{% else %}
[Exercise précédent](../1.3-playbook/README.fr.md) - [Exercise suivant](../1.5-handlers/README.fr.md)
{% endif %}
<br><br>
