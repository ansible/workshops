# Atelier - Rédaction de votre premier Playbook

**Lisez ceci dans d'autres langues**:

<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).


## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
  - [Étape 1 - Principes de base d'un Playbook](#Étape-1---Principes-de-base-d-un-Playbook)
  - [Étape 2 - Création d'une structure pour votre Playbook](#Étape-2---Création-d-une-structure-pour-votre-Playbook)
  - [Étape 3 - Exécution du Playbook](#Étape-3---Exécution-du-Playbook)
  - [Étape 4 - Ajout de tache: Démarrage et activation de Apache](#Étape-4---Ajout-de-tache-Démarrage-et-activation-de-Apache)
  - [Étape 5 - Ajout de tache: Création de fichier html](#Étape-5---Ajout-de-tache-Création-de-fichier-html)
  - [Étape 6 - Application à plusieurs hôtes](#Étape-6---Application-à-plusieurs-hôtes)

# Objectif

Cet exercice couvre l'utilisation d'Ansible pour créer deux serveurs Web Apache sur Red Hat Enterprise Linux. Cet exercice couvre les principes de base d'Ansible suivants:

- Comprendre les paramètres du module Ansible
- Comprendre et utiliser les modules suivants
   - [module yum](https://docs.ansible.com/ansible/latest/modules/yum_module.html)
   - [module de service](https://docs.ansible.com/ansible/latest/modules/service_module.html)
   - [module de copie](https://docs.ansible.com/ansible/latest/modules/copy_module.html)
- Comprendre [Idempotence](https://en.wikipedia.org/wiki/Idempotence) et comment les modules Ansible peuvent être idempotents

# Guide

Bien que les commandes Ad-hoc Ansible soient utiles pour des opérations simples, elles ne conviennent pas aux scénarios de gestion de configuration ou d'orchestration complexes. Pour de tels cas d'utilisation, les *playbooks* sont la solution.

Les playbooks sont des fichiers qui décrivent les configurations ou étapes souhaitées à implémenter sur les hôtes gérés. Les playbooks peuvent transformer des tâches administratives longues et complexes en routines facilement reproductibles avec des résultats prévisibles et réussis.

Un playbook est l'endroit où vous pouvez prendre certaines de ces commandes Ad-hoc que vous venez d'exécuter et les mettre dans un ensemble répétable de *plays* et *taches*.

Un playbook peut avoir plusieurs "plays" et un "play" peut avoir une ou plusieurs taches. Dans une tâche, un *module* est appelé, comme les modules du chapitre précédent. Le but d'un *play* est de cartographier un groupe d'hôtes. Le but d'une *tâche* est d'implémenter des modules sur ces hôtes.

> **Astuce**
>
> Voici une belle analogie: lorsque les modules Ansible sont les outils de votre atelier, l'inventaire est le matériel et les Playbooks les instructions.

## Étape 1 - Principes de base d un Playbook

Les playbooks sont des fichiers texte écrits au format YAML et nécessitent donc:

   - de commencer par trois tirets (`---`)

   - une indentation appropriée en utilisant des espaces et **surtout pas** de tabulation \!

Il existe quelques concepts importants:

   - **hosts**: les hôtes sur lesquels seront effectués les tâches

   - **tasks**: les opérations à effectuer en appelant les modules Ansible et en leur passant les options nécessaires.

   - **become**: élévation de privilèges dans les playbooks, identique à l'utilisation de `-b` dans la commande Ad-hoc.

> **Avertissement**
>
> L'ordre des contenus dans un Playbook est important, car Ansible exécute les play et les tâches dans l'ordre où ils sont présentés.

Un Playbook doit être **idempotent**, donc si un Playbook est exécuté une fois pour mettre les hôtes dans l'état correct, il devrait être sûr de l'exécuter une deuxième fois et il ne devrait plus apporter de modifications aux hôtes.

> **Astuce**
>
> La plupart des modules Ansible sont idempotents, il est donc relativement facile de s'assurer que cela est vrai.

## Étape 2 - Création d'une structure pour votre Playbook

Assez de théorie, il est temps de créer votre premier Playbook Ansible. Dans ce laboratoire, vous créez un playbook pour configurer un serveur Web Apache en trois étapes:

  1. Installez le package httpd

  2. Activer/démarrer le service httpd

  3. Copiez un fichier web.html sur chaque hôte Web

Ce Playbook s'assure que le paquet contenant le serveur Web Apache est installé sur `node1`.

Il existe un guide des [meilleures pratiques](http://docs.ansible.com/ansible/playbooks_best_practices.html) sur les structures de répertoires a utilisé pour les playbooks. Nous vous encourageons fortement à lire et à comprendre ces pratiques lorsque vous développez vos compétences de maitre ninja Ansible. Cela dit, notre playbook d'aujourd'hui est très basique et créer une structure complexe ne fera que confondre les choses.

Au lieu de cela, nous allons créer une structure de répertoire très simple pour notre playbook et y ajouter seulement quelques fichiers.

Sur votre hôte de contrôle **ansible**, créez un répertoire appelé `ansible-files` dans votre répertoire personnel, et rentrez dedans.

```bash
[student<X>@ansible ~]$ mkdir ansible-files
[student<X>@ansible ~]$ cd ansible-files/
```

Ajoutez un fichier appelé `apache.yml` avec le contenu suivant. Comme expliqué dans les exercices précédents, utilisez à nouveau `vi`/`vim` ou, si vous débutez avec les éditeurs sur la ligne de commande, consultez à nouveau [intro de l'éditeur](../0.0-support-docs/editor_intro.md) .

```yaml
---
- name: Apache server installed
  hosts: node1
  become: yes
```

Cela montre l'une des forces d'Ansible: la syntaxe Playbook est facile à lire et à comprendre. Dans ce Playbook:

   - Un nom est donné pour le play via `name:`.

   - L'hôte sur lequel sera exécuter le playbook est défini via `hosts:`.

   - Nous activons l'escalade de privilèges utilisateur avec `become:`.

> **Astuce**
>
> Vous devez évidemment utiliser une élévation de privilèges pour installer un package ou exécuter toute autre tâche nécessitant des autorisations root. Cela se fait dans le Playbook par "become: yes".

Maintenant que nous avons défini le play, ajoutons une tâche pour faire quelque chose. Nous ajouterons une tâche dans laquelle yum s'assurera que le package Apache est installé dans la dernière version. Modifiez le fichier pour qu'il ressemble à la liste suivante:

```yaml
---
- name: Apache server installed
  hosts: node1
  become: yes
  tasks:
  - name: latest Apache version installed
    yum:
      name: httpd
      state: latest
```
> **Astuce**
>
> Les playbooks étant écrits en YAML, l'alignement des lignes et des mots-clés est crucial. Assurez-vous d'aligner verticalement le *t* dans `tâche` avec le *b* dans `become`. Une fois que vous vous serez familiarisé avec Ansible, assurez-vous de prendre un peu de temps et d'étudier un peu la [Syntaxe YAML](http://docs.ansible.com/ansible/YAMLSyntax.html).

Dans les lignes ajoutées:

  - Nous avons commencé la partie tâches avec le mot clé `tasks:`.

  - Une tâche est nommée et le module de la tâche est référencé. Ici, il utilise le module `yum`.

  - Des paramètres pour le module sont ajoutés:

    - `name:` pour identifier le nom du paquet
    - `state:` pour définir l'état souhaité du paquet

> **Astuce**
>
> Les paramètres du module sont individuels pour chaque module. En cas de doute, recherchez-les à nouveau avec `ansible-doc`.

Enregistrez votre playbook et quittez votre éditeur.

## Étape 3 - Exécution du Playbook

Les Playbooks Ansible sont exécutés à l'aide de la commande `ansible-playbook` sur le nœud de contrôle. Avant d'exécuter un nouveau Playbook, il est judicieux de vérifier les erreurs de syntaxe:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook --syntax-check apache.yml
```

Vous devriez maintenant être prêt à exécuter votre playbook:

```
[student<X>@ansible ansible-files]$ ansible-playbook apache.yml
```

La sortie ne doit pas signaler d'erreurs mais fournir un aperçu des tâches exécutées et un récapitulatif du pay résumant ce qui a été fait. Il y a aussi une tâche appelée "Gathering Facts" qui y est répertoriée: il s'agit d'une tâche intégrée qui s'exécute automatiquement au début de chaque jeu. Il collecte des informations sur les nœuds gérés. Des exercices plus tard couvriront cela plus en détail.

Connectez-vous à `node1` via SSH pour vous assurer qu'Apache a été installé:

```
[student<X>@ansible ansible-files]$ ssh node1
Last login: Wed May 15 14:03:45 2019 from 44.55.66.77
Managed by Ansible
```

Utilisez la commande `rpm -qe httpd` pour vérifié que httpd est bien installé :

```
[student<X>@node1 ~]$ rpm -qi httpd
Name        : httpd
Version     : 2.4.6
[...]
```

Déconnectez-vous de `node1` avec la commande `exit` pour revenir sur l'hôte de contrôle et vérifiez que le package installé via une commande Ad-hoc Ansible.

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m command -a 'rpm -qi httpd'
```

Exécutez le Playbook une deuxième fois et comparez la sortie: la sortie est passée de «changed» à «ok» et la couleur est passée du jaune au vert. De plus, le "PLAY RECAP" est différent maintenant. Cela permet de repérer facilement ce qu'Ansible a réellement fait.

## Étape 4 - Ajout de tache: Démarrage et activation de Apache

La partie suivante du Playbook Ansible s'assure que l'application Apache est activée et démarrée sur `node1`.

Sur l'hôte de contrôle, en tant qu'utilisateur student, modifiez le fichier `~/ansible-files/apache.yml` pour ajouter une deuxième tâche à l'aide du module `service`. Le Playbook devrait maintenant ressembler à ceci:

```yaml
---
- name: Apache server installed
  hosts: node1
  become: yes
  tasks:
  - name: latest Apache version installed
    yum:
      name: httpd
      state: latest
  - name: Apache enabled and running
    service:
      name: httpd
      enabled: true
      state: started
```

Encore une fois: ce que font ces lignes est facile à comprendre:

   - une deuxième tâche est créée et nommée

   - un module est spécifié (`service`)

   - les paramètres du module sont fournis

Ainsi, avec la deuxième tâche, nous nous assurons que le serveur Apache fonctionne bien sur la machine cible. Exécutez votre Playbook étendu:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook apache.yml
```

Notez maintenant la sortie: Certaines tâches sont affichées comme "ok" en vert et une est indiquée comme "modified" en jaune.

   - Utilisez à nouveau une commande Ad-hoc Ansible pour vous assurer qu'Apache a été activé et démarré, par exemple avec: `systemctl status httpd`.

   - Exécutez le Playbook une deuxième fois pour vous habituer au changement de sortie.

## Étape 5 - Ajout de tache: Création de fichier html

Vérifiez que les tâches ont été exécutées correctement et qu'Apache accepte les connexions: effectuez une demande HTTP à l'aide du module uri d'Ansible dans une commande Ad-hoc du nœud de contrôle. Assurez-vous de remplacer le **\<IP\>** par l'IP du nœud de l'inventaire.

> **Avertissement**
>
> **Attendez-vous à beaucoup de lignes rouges et un statut 403 \!**

```bash
[student<X>@ansible ansible-files]$ ansible localhost -m uri -a "url=http://<IP>"
```

Il y a beaucoup de lignes rouges et une erreur: tant qu'il n'y a pas le fichier `web.html` devant être servi par Apache, il affichera un vilain état ""HTTP Error 403: Forbidden"" et Ansible signalera une erreur.

Alors pourquoi ne pas utiliser Ansible pour déployer un simple fichier `web.html`?
Sur l'hôte de contrôle ansible, en tant qu'utilisateur `student <X>`, créez le répertoire `files` pour contenir les ressources de fichiers dans `~/ ansible-files/`:

```bash
[student<X>@ansible ansible-files]$ mkdir files
```

Créez ensuite le fichier `~/ansible-files/files/web.html` sur le nœud de contrôle:

```html
<body>
<h1>Apache is running fine</h1>
</body>
```

Vous avez déjà utilisé le module de copie d'Ansible pour écrire le texte fourni sur la ligne de commande dans un fichier. Vous allez maintenant utiliser le module de votre Playbook pour copier un fichier:

Sur le nœud de contrôle, en tant qu'utilisateur étudiant, modifiez le fichier `~/ansible-files/apache.yml` et ajoutez une nouvelle tâche en utilisant le module `copy`. Cela devrait maintenant ressembler à ceci:


```yaml
---
- name: Apache server installed
  hosts: node1
  become: yes
  tasks:
  - name: latest Apache version installed
    yum:
      name: httpd
      state: latest
  - name: Apache enabled and running
    service:
      name: httpd
      enabled: true
      state: started
  - name: copy web.html
    copy:
      src: web.html
      dest: /var/www/html/index.html
```

Vous vous habituez à la syntaxe Playbook, alors que se passe-t-il? La nouvelle tâche utilise le module `copy` et définit les options source et destination pour l'opération de copie en tant que paramètres.

Exécutez votre Playbook étendu:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook apache.yml
```

- Regardez bien la sortie

- Exécutez à nouveau la commande Ad-hoc à l'aide du module "uri" ci-dessus pour tester Apache: La commande devrait maintenant renvoyer une ligne verte "status: 200" entre autres informations.

## Étape 6 - Application à plusieurs hôtes

C'était bien, mais le vrai pouvoir d'Ansible est d'appliquer le même ensemble de tâches de manière fiable à de nombreux hôtes.

   - Alors, qu'en est-il de changer le Playbook apache.yml pour qu'il fonctionne sur `node1` **et** `node2` **et** `node3`?


Comme vous vous en souvenez peut-être, l'inventaire répertorie tous les nœuds en tant que membres du groupe `web`:

```ini
[web]
node1 ansible_host=11.22.33.44
node2 ansible_host=22.33.44.55
node3 ansible_host=33.44.55.66
```

> **Astuce**
>
> Les adresses IP présentées ici ne sont que des exemples, vos nœuds auront des adresses IP différentes.

Modifiez le Playbook pour pointer vers le groupe "web":

```yaml
---
- name: Apache server installed
  hosts: web
  become: yes
  tasks:
  - name: latest Apache version installed
    yum:
      name: httpd
      state: latest
  - name: Apache enabled and running
    service:
      name: httpd
      enabled: true
      state: started
  - name: copy web.html
    copy:
      src: web.html
      dest: /var/www/html/index.html
```

Maintenant, lancez le Playbook:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook apache.yml
```

Enfin, vérifiez si Apache fonctionne maintenant sur les deux serveurs. Identifiez d'abord les adresses IP des nœuds de votre inventaire, puis utilisez-les chacune dans la commande Ad-hoc avec le module uri comme nous l'avons déjà fait avec le `node1` ci-dessus. Toute sortie doit être verte.

> **Astuce**
>
> Une autre façon de vérifier qu'Apache fonctionne sur les deux serveurs est d'utiliser la commande `ansible node2,node3 -m uri -a "url=http://localhost/"`.


----
**Navigation**
<br>
[Exercise précédent](../1.2-adhoc/README.fr.md) - [Exercise suivant](../1.4-variables/README.fr.md)

[Cliquez ici pour revenir à l'atelier Ansible pour Red Hat Enterprise Linux](../README.fr.md)
