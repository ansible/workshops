# Atelier - Utilisation des variables

**Lisez ceci dans d'autres langues**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table des matières

* [Objectif](#objectif)
* [Guide](#guide)
* [Introduction aux variables](#introduction-aux-variables)
* [Étape 1 - Création des fichiers de variables](#Étape-1---Création-des-fichiers-de-variables)
* [Étape 2 - Création des fichiers html](#Étape-2---Création-des-fichiers-html)
* [Étape 3 - Création du Playbook](#Étape-3---Création-du-playbook)
* [Étape 4 - Teste du résultat](#Étape-4---teste-du-résultat)
* [Étape 5 - Les faits](#Étape-5---les-faits)
* [Étape 6 - Défi: Les faits](#Étape-6---défi-les-faits)
* [Étape 7 - Utilisation des faits dans un playbook](#Étape-7---utilisation-des-faits-dans-un-playbook)

# Objectif

Ansible prend en charge des variables pour stocker des valeurs pouvant être utilisées dans Playbooks. Les variables peuvent être définies à divers endroits et ont une priorité claire. Ansible remplace la variable par sa valeur lorsqu'une tâche est exécutée.

Cet exercice couvre des variables, en particulier
- Comment utiliser les délimiteurs de variables `{{` et `}}`
- Qu'est-ce que `host_vars` et `group_vars` et quand les utiliser
- Comment utiliser `ansible_facts`
- Comment utiliser le module `debug` pour imprimer des variables dans la fenêtre de la console

# Guide

## Introduction aux variables

Les variables sont référencées dans les Playbooks en plaçant le nom de la variable entre deux accolades:

<!-- {% raw %} -->
```yaml
Here comes a variable {{ variable1 }}
```
<!-- {% endraw %} -->

Les variables et leurs valeurs peuvent être définies à différents endroits: l'inventaire, les fichiers supplémentaires, sur la ligne de commande, etc.

La pratique recommandée pour fournir des variables dans l'inventaire est de les définir dans des fichiers situés dans deux répertoires nommés `host_vars` et `group_vars`:

   - Pour définir des variables pour un groupe "serveurs", utilisez un fichier YAML nommé `group_vars/servers.yml` pour la définitionsdes variables.

   - Pour définir des variables spécifiquement pour un hôte `node1`, utilisez le fichier `host_vars/node1.yml` apour la définition des variables.

> **Astuce**
>
> Les variables hôtes ont priorité sur les variables de groupe (plus d'informations sur la priorité peuvent être trouvées dans la [documentation](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable).


## Étape 1 - Création des fichiers de variables

Pour comprendre et pratiquer, faisons un laboratoire. Dans le prolongement du thème "Construisons un serveur Web. Ou deux. Ou même plus ...", vous allez changer le `index.html` pour montrer l'environnement de développement (dev/prod) dans lequel un serveur est déployé.

Sur l'hôte de contrôle ansible, en tant qu'utilisateur `student<X>`, créez les répertoires pour contenir les définitions des variables dans `~/ansible-files/`:

```bash
[student<X>@ansible ansible-files]$ mkdir host_vars group_vars
```

Créez maintenant deux fichiers contenant des définitions de variables. Nous allons définir une variable nommée `stage` qui pointera vers différents environnements, `dev` ou `prod`:

  - Créez le fichier `~/ansible-files/group_vars/web.yml` avec ce contenu:

```yaml
---
stage: dev
```
  - Créez le fichier `~/ansible-files/host_vars/node2.yml` avec ce contenu:

```yaml
---
stage: prod
```

Ca parle de quoi?

   - Pour tous les serveurs du groupe `web`, la variable `stage` avec la valeur `dev` est définie. Donc, par défaut, nous les signalons comme membres de l'environnement de développement.

   - Pour le serveur `node2`, la declaration ci-dessus est remplacé et l'hôte est marqué comme serveur de production.

## Étape 2 - Création des fichiers html

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

## Étape 3 - Création du Playbook

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
  become: yes
  tasks:
  - name: copy web.html
    copy:
      src: "{{ stage }}_web.html"
      dest: /var/www/html/index.html
```
<!-- {% endraw %} -->

  - Executez le Playbook:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook deploy_index_html.yml
```

## Étape 4 - Testez le résultat

Le Playbook doit copier différents fichiers sous forme d'index.html sur les hôtes, utilisez `curl` pour le tester. Vérifiez à nouveau l'inventaire si vous avez oublié les adresses IP de vos nœuds.

```bash
[student<X>@ansible ansible-files]$ grep node ~/lab_inventory/hosts
node1 ansible_host=11.22.33.44
node2 ansible_host=22.33.44.55
node3 ansible_host=33.44.55.66
[student<X>@ansible ansible-files]$ curl http://11.22.33.44
<body>
<h1>This is a development webserver, have fun!</h1>
</body>
[student1@ansible ansible-files]$ curl http://22.33.44.55
<body>
<h1>This is a production webserver, take care!</h1>
</body>
[student1@ansible ansible-files]$ curl http://33.44.55.66
<body>
<h1>This is a development webserver, have fun!</h1>
</body>
```

> **Astuce**
>
> Si vous y reflechissez, il doit y avoir un moyen plus intelligent de modifier le contenu des fichiers… vous avez absolument raison. Ce laboratoire a été fait pour introduire des variables, vous êtes sur le point d'en apprendre davantage sur les modèles dans l'un des chapitres suivants.

## Étape 5 - Les faits

Les faits Ansible sont des variables qui sont automatiquement découvertes par Ansible à partir d'un hôte géré. Vous vous souvenez de la tâche "Gathering Facts" répertoriée dans la sortie de chaque exécution de "ansible-playbook"? À ce moment, les faits sont rassemblés pour chaque nœud géré. Les faits peuvent également être tirés par le module `setup`. Ils contiennent des informations utiles stockées dans des variables que les administrateurs peuvent réutiliser.

Pour avoir une idée des faits collectés par défaut par Ansible, sur votre nœud de contrôle avec votre utilisateur étudiant, exécutez:

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup
```

C'est peut être un peu trop d'information, vous pouvez utiliser des filtres pour limiter la sortie à certains faits, l'expression est un caractère générique de style shell:

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup -a 'filter=ansible_eth0'
```
Ou qu'en est-il uniquement de rechercher des faits liés à la mémoire:

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup -a 'filter=ansible_*_mb'
```

## Étape 6 - Défi: Les faits

   - Essayez de trouver et d'imprimer la distribution (Red Hat) de vos hôtes gérés. Veuilliez l'afficher sur une seule ligne.

> **Astuce**
>
> Utilisez grep pour trouver le fait, puis appliquez un filtre pour imprimer uniquement ce fait.

> **Avertissement **
>
> **Solution ci-dessous \!**

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup|grep distribution
[student<X>@ansible ansible-files]$ ansible node1 -m setup -a 'filter=ansible_distribution' -o
```

## Étape 7 - Utilisation des faits dans un playbook

Les faits peuvent être utilisés dans un Playbook comme des variables, en utilisant le bon nom, bien sûr. Créez ce Playbook en tant que `facts.yml` dans le répertoire `~/ansible-files/`:

<!-- {% raw %} -->
```yaml    
---
- name: Output facts within a playbook
  hosts: all
  tasks:
  - name: Prints Ansible facts
    debug:
      msg: The default IPv4 address of {{ ansible_fqdn }} is {{ ansible_default_ipv4.address }}
```
<!-- {% endraw %} -->

> **Astuce**
>
> Le module "debug" peut être pratique pour débogager les variables ou expressions.

Exécutez-le pour voir comment les faits sont affichés:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook facts.yml

PLAY [Output facts within a playbook] ******************************************

TASK [Gathering Facts] *********************************************************
ok: [node3]
ok: [node2]
ok: [node1]
ok: [ansible]

TASK [Prints Ansible facts] ****************************************************
ok: [node1] =>
  msg: The default IPv4 address of node1 is 172.16.190.143
ok: [node2] =>
  msg: The default IPv4 address of node2 is 172.16.30.170
ok: [node3] =>
  msg: The default IPv4 address of node3 is 172.16.140.196
ok: [ansible] =>
  msg: The default IPv4 address of ansible is 172.16.2.10

PLAY RECAP *********************************************************************
ansible                    : ok=2    changed=0    unreachable=0    failed=0   
node1                      : ok=2    changed=0    unreachable=0    failed=0   
node2                      : ok=2    changed=0    unreachable=0    failed=0   
node3                      : ok=2    changed=0    unreachable=0    failed=0   
```

----
**Navigation**
<br>
[Exercise précédent](../1.3-playbook/README.fr.md) - [Exercise suivant](../1.5-handlers/README.fr.md)

[Cliquez ici pour revenir à l'atelier Ansible pour Red Hat Enterprise Linux](../README.fr.md)
