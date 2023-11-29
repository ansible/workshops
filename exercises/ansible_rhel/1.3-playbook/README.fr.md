# Exercice - Rédaction de votre premier Playbook

**Lisez ceci dans d'autres langues:**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Français](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table des matières

- [Exercice - Rédaction de votre premier Playbook](#exercice---rédaction-de-votre-premier-playbook)
  - [Table des matières](#table-des-matières)
  - [Objectif](#objectif)
  - [Guide](#guide)
    - [Etape 1 - Principes de base d'un Playbook](#Etape-1---Principes-de-base-d'un-Playbook)
    - [Etape 2 - Création d'une structure pour votre Playbook](#Etape-2---Création-d-une-structure-pour-votre-Playbook)
    - [Etape 3 - Exécution du Playbook](#Etape-3---Exécution-du-Playbook)
    - [Etape 4 - Ajout de tache: Démarrage et activation de Apache](#Etape-4---Ajout-de-tache-Démarrage-et-activation-de-Apache)
    - [Etape 5 - Ajout de tache: Création de fichier html](#Etape-5---Ajout-de-tache-Création-de-fichier-html)
    - [Etape 6 - Application à plusieurs hôtes](#Etape-6---Application-à-plusieurs-hôtes)

## Objectif

Cet exercice couvre l'utilisation d'Ansible pour créer deux serveurs Web Apache sur Red Hat Enterprise Linux. Cet exercice couvre les principes de base d'Ansible suivants:

* Comprendre les paramètres du module Ansible
* Comprendre et utiliser les modules suivants
  * [module dnf](https://docs.ansible.com/ansible/latest/modules/dnf_module.html)
  * [module service](https://docs.ansible.com/ansible/latest/modules/service_module.html)
  * [module copy](https://docs.ansible.com/ansible/latest/modules/copy_module.html)
* Comprendre l'[idempotence](https://en.wikipedia.org/wiki/Idempotence) et comment les modules Ansible peuvent être idempotents

## Guide

Les Playbooks sont des fichiers qui décrivent les configurations souhaitées ou les étapes pour les implémenter sur les hôtes gérés. Les Playbooks peuvent transformer des tâches longues et complexes d'un point de vue administratif en routines facilement reproductibles avec des résultats prévisibles et réussis.

Un playbook peut avoir plusieurs "plays" et un "play" peut avoir une ou plusieurs tâches. Dans une tâche, un module est appelé, comme les modules du chapitre précédent. Le but d'un play est de cartographier un groupe d'hôtes. Le but d'une tâche est d'implémenter des modules sur ces hôtes.

> **Astuce**
>
> Voici une belle analogie: lorsque les modules Ansible sont les outils de votre atelier, l'inventaire est le matériel et les Playbooks les instructions.

### Etape 1 - Principes de base d'un Playbook

Les playbooks sont des fichiers texte écrits au format YAML et nécessitent donc:

  * de commencer par trois tirets (`---`)
  * une indentation appropriée en utilisant des espaces et **surtout pas** de tabulation \!

Il existe quelques concepts importants:

 *  **hosts**: les hôtes sur lesquels seront effectués les tâches
 *  **tasks**: les opérations à effectuer en appelant les modules Ansible et en leur passant les options nécessaires.
 *  **become**: élévation de privilèges dans les playbooks, identique à l'utilisation de `-b` dans la commande Ad-hoc.

> **Avertissement**
>
> L'ordre des contenus dans un Playbook est important, car Ansible exécute les play et les tâches dans l'ordre où ils sont présentés.

Un Playbook doit être **idempotent**, donc si un Playbook est exécuté une fois pour mettre les hôtes dans l'état correct, il devrait être sûr de l'exécuter une deuxième fois et il ne devrait plus apporter de modifications aux hôtes.

> **Astuce**
>
> La plupart des modules Ansible sont idempotents, il est donc relativement facile de s'assurer que cela est vrai.

### Etape 2 - Création d'une structure pour votre Playbook

Assez de théorie, il est temps de créer votre premier Playbook Ansible. Dans ce laboratoire, vous créez un playbook pour configurer un serveur Web Apache en trois étapes:
  1. Installez le package httpd
  2. Activer/démarrer le service httpd
  3. Copiez un fichier web.html sur chaque hôte Web

Ce Playbook s'assure que le paquet contenant le serveur Web Apache est installé sur `node1`.

Il existe un guide des [bonnes pratiques](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html) sur les structures de répertoires à utiliser pour les Playbooks. Nous vous encourageons fortement à lire et à comprendre ces pratiques lorsque vous développez vos compétences de maitre ninja Ansible. Cela dit, notre Playbook d'aujourd'hui est très basique et créer une structure complexe ne fera que rendre les choses confuses.

Au lieu de cela, nous allons créer une structure de répertoire très simple pour notre playbook et y ajouter seulement quelques fichiers.

Sur votre hôte de contrôle **ansible**, créez un répertoire appelé `ansible-files` dans votre répertoire personnel, et rentrez dedans.

```bash
[student@ansible-1 ~]$ mkdir ansible-files
[student@ansible-1 ~]$ cd ansible-files/
```

Ajoutez un fichier appelé `apache.yml` avec le contenu suivant. Comme expliqué dans les exercices précédents, utilisez à nouveau `vi`/`vim` ou, si vous débutez avec les éditeurs sur la ligne de commande, consultez à nouveau [introduction à l'éditeur](../0.0-support-docs/editor_intro.md).

```yaml
---
- name: Apache server installed
  hosts: node1
  become: yes
```

Cela montre l'une des forces d'Ansible: la syntaxe Playbook est facile à lire et à comprendre. Dans ce Playbook:
* Un nom est donné pour le play via `name:`.
* L'hôte sur lequel sera exécuter le playbook est défini via `hosts:`.
* Nous activons l'escalade de privilèges utilisateur avec `become:`.

> **Astuce**
>
> Vous devez évidemment utiliser une élévation de privilèges pour installer un package ou exécuter toute autre tâche nécessitant des autorisations root. Cela se fait dans le Playbook par `become: yes`.

Maintenant que nous avons défini le play, ajoutons une tâche pour faire quelque chose. Nous ajouterons une tâche dans laquelle dnf s'assurera que le package Apache est installé dans la dernière version. Modifiez le fichier pour qu'il ressemble à la liste suivante:

```yaml
---
- name: Apache server installed
  hosts: node1
  become: yes
  tasks:

    - name: Install Apache
      ansible.builtin.dnf:
        name: httpd
```

> **Astuce**
>
> Les playbooks étant écrits en YAML, l'alignement des lignes et des mots-clés est crucial. Assurez-vous d'aligner verticalement le *t* dans `tâche` avec le *b* dans `become`. Une fois que vous vous serez familiarisé avec Ansible, assurez-vous de prendre un peu de temps et d'étudier un peu la [Syntaxe YAML](http://docs.ansible.com/ansible/YAMLSyntax.html).

Dans les lignes ajoutées:
* Nous avons commencé la partie tâches avec le mot clé `tasks:`.
* Une tâche est nommée et le module de la tâche est référencé. Ici, il utilise le module `dnf`.
* Des paramètres pour le module sont ajoutés:
  * `name:` pour identifier le nom du paquet
  * `state:` pour définir l'état souhaité du paquet

> **Astuce**
>
> Les paramètres du module sont individuels pour chaque module. En cas de doute, recherchez-les à nouveau avec la documentation dans `ansible-navigator`.

Enregistrez votre playbook et quittez votre éditeur.

### Etape 3 - Exécution du Playbook

Depuis Ansible Automation Platform 2, un certain nombre de nouveaux composants sont introduits dans le cadre de l'expérience développeur. Les Environnements d'Execution ont été introduits pour fournir un environnement prévisible lors de l'exécution de l'automatisation. Toutes les dépendances en terme de collections sont contenues dans l'EE pour garantir que l'automatisation créée dans l'environnement de développement est exécutée à l'identique dans les environnements de production.

Que trouve-t-on dans un Environnement d'Execution?
* RHEL UBI 8
* Ansible 2.9 ou Ansible Core 2.11
* Python 3.8
* Des collections
* Des dépendances Python ou binaires pour les collections

Pourquoi utiliser des Environnements d'Execution ?

Ils fournissent un moyen standardisé de définir, construire et distribuer les environnements dans lesquels l'automatisation tourne. En résumé, les EE sont des images de conteneurs qui permettent une administration facilitée de Ansible par l'administrateur de la plateforme.

En considérant le déplacement vers l'exécution conteneurisée de l'automatisation, le processus et l'outillage de développement de l'automatisation qui existait avant Ansible Automation Platform 2 ont du être réminaginés. En résumé, `ansible-navigator` remplace `ansible-playbook` et les autres commandes utilitaires en ligne de commande `ansible-*`.

Avec ce changement, les Playbooks Ansible sont exécutés à l'aide de la commande `ansible-navigator` sur le noeud de contrôle.

Les prérequis et bonnes pratiques pour l'utilisation de `ansible-navigator` ont été traités pour vous dans ce lab.

Cela inclut:
* L'installation du package `ansible-navigator`
* La création de paramètres par défaut dans `/home/student/.ansible-navigator.yml` pour tous vos projets (optionnel)
* Tous les logs des EE sont stockés dans `/home/student/.ansible-navigator/logs/ansible-navigator.log`
* Les artéfacts de Playbooks sont sauvegardés dans `/tmp/artifact.json`

Pour plus d'informations sur les [paramètres de Ansible navigator](https://github.com/ansible/ansible-navigator/blob/main/docs/settings.rst)

> **Astuce**
>
> Le sparamètres de `ansible-navigator` peuvent être modifiés pour votre environnement spécifique. Les paramètres actuels utilisent un `ansible-navigator.yml` par défaut pour tous les projets, mais un `ansible-navigator.yml` spécifique peut être créé pour chaque projet, et c'est la pratique recommandée.

Pour lancer votre Playbook, utilisez la commande `ansible-navigator run <playbook>` comme suit:

```bash
[student@ansible-1 ansible-files]$ ansible-navigator run apache.yml
```

> **Astuce**
>
> Le fichier `ansible-navigator.yml` existant fournit l'emplacement de votre fichier d'inventaire. Si ce n'était pas renseigné dans votre fichier `ansible-navigator.yml`, alors la commande pour lancer le Playboko serait: `ansible-navigator run apache.yml -i /home/student/lab_inventory/hosts`

Pendant l'exécution du playbook, vous aurez une interface en mode texte (TUI) qui affiche le nom du Play, et d'autres informations sur le playbook en cours.

```bash
  PLAY NAME                        OK  CHANGED    UNREACHABLE      FAILED    SKIPPED    IGNORED    IN PROGRESS     TASK COUNT          PROGRESS
0│Apache server installed           2        1              0           0          0          0              0              2          COMPLETE
```

Si vous remarquez, avant le nom du Play `Apache server installed`, vous verrez un `0`. EN pressant la touche `0` sur votre clavier, vous obtiendrez une nouvelle fenêtre qui affiche les différentes tâches qui ont tourné pour ce Playbook. Dnas cet exemple, ces tâches incluent  "Gathering Facts" et "Install Apache". La tâche "Gathering Facts" est intégrée et tourne automatiquement au début de chaque Play. Elle collecte des informations sur les noeuds gérés. Les exercices ultérieurs couvriront ce concept plus en détail. La tâche "Install Apache" est la tâche créée dans le fichier `apache.yml` qui installe `httpd`.

Le résultat devrait ressembler à ceci:

```bash
  RESULT      HOST	NUMBER      CHANGED       TASK                                                   TASK ACTION           DURATION
0│OK          node1          0        False       Gathering Facts                                        gather_facts                1s
1│OK          node1          1         True       Install Apache                        dnf                         4s
```

En regardant de plus près, vous rmarquerez que chaque tâche est associée à un numéro. La tâche 1, "Install Apache", marque un changemenet et a utilisé le module `dnf`. Dans ce cas le changement est l'installation de Aache (paquet `httpd`) sur l'hôte `node1`.

En pressant `0` ou `1` sur votre clavier, vous pouvez voir plus de détails sur les tâches exécutées. Si vous souhaitez un affichage plus traditionnel, tapez `:st` dans l'interface texte.

Une fois terminé, vous pouvez quitter la TUI avec la touche Echap de votre clavier.

> **Astuce**
>
> La touche Echap vous ramène simplement à l'écran précédent. Une fois sur l'écran principal, appuyer sur Echap vous ramène au terminal.

Une fois le playbook complété, connectez vous à `node1` via SSH pour vous assurer que Apache a été installé:

```bash
[student@ansible-1 ansible-files]$ ssh node1
Last login: Wed May 15 14:03:45 2019 from 44.55.66.77
Managed by Ansible
```

Utilisez la commande `rpm -qi httpd` pour vérifier que httpd est installé:

```bash
[ec2-user@node1 ~]$ rpm -qi httpd
Name        : httpd
Version     : 2.4.37
[...]
```

Déconnectez-vous de `node1` avec la commande `exit` pour revenir sur l'hôte de contrôle et vérifier le paquet installé avec un Playbook Ansible intitulé `package.yml`

{% raw %}
```yaml
---
- name: Check packages
  hosts: node1
  become: true
  vars:
    package: "httpd"

  tasks:
    - name: Gather the package facts
      ansible.builtin.package_facts:
        manager: auto

    - name: Check whether a {{ package }}  is installed
      ansible.builtin.debug:
        msg: "{{ package }} {{ ansible_facts.packages[ package ][0].version }} is installed!"
      when: "package in ansible_facts.packages"

```
{% endraw %}


```bash
[student@ansible-1 ~]$ ansible-navigator run package.yml -m stdout
```

```bash

PLAY [Check packages] **********************************************************

TASK [Gathering Facts] *********************************************************
ok: [ansible]

TASK [Gather the package facts] ************************************************
ok: [ansible]

TASK [Check whether a httpd  is installed] *************************************
ok: [ansible] => {
    "msg": "httpd 2.4.37 is installed!"
}

PLAY RECAP *********************************************************************
ansible                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

Lancez le Playbook `ansible-navigator run apache.yml` une seconde fois, et comparez le résultat. Le compteur "CHANGED" montre à présent `0` au lieu de `1` et la couleur est passée de jaune à vert. Cela rend plus facile le repérage des changements lors des lancements de Playbooks Ansible.

### Etape 4 - Ajout de tache: Démarrage et activation de Apache

La partie suivante du Playbook Ansible s'assure que l'application Apache est activée et démarrée sur `node1`.

Sur l'hôte de contrôle, en tant qu'utilisateur student, modifiez le fichier `~/ansible-files/apache.yml` pour ajouter une deuxième tâche à l'aide du module `service`. Le Playbook devrait maintenant ressembler à ceci:

```yaml
---
- name: Apache server installed
  hosts: node1
  become: true
  tasks:

    - name: Install Apache
      ansible.builtin.dnf:
        name: httpd

    - name: Apache enabled and running
      ansible.builtin.service:
        name: httpd
        enabled: true
        state: started
```

Quels changements avons-nous faits ?
* une deuxième tâche est créée et nommée
* un module est spécifié (`service`)
* Le module `service` prend le nom du service (`httpd`), renseigne son activation (`enabled`), et son état actuel (`started`)

Ainsi, avec la seconde tâche on s'assure que le serveur Apache est bien en route sur la machine cible. Lancez votre Playbook étendu:

```bash
[student@ansible-1 ~]$ ansible-navigator run apache.yml
```

Notez dans le résultat, on voir que le Play avait `1` élément "CHANGED" affiché en jaune et si on presse `0` pour entrer dans la sortie du Play, on peut voir que la tâche 2, "Apache enabled and running", éait la tâche qui incorporait les derniers changements grâce à la valeur de "CHANGED" passée à True et colorée en jaune.

* Lancez le Playbook une seconde fois en utilisant `ansible-navigator` pour vous habituer aux changements dans le résultat.
  
* Utilisez un Playbook Ansible institulé `service_state.yml` pour vous assurer que le service Apache (httpd) est lancé sur `node1`, c'est-à-dire avec: `systemctl status httpd`.

{% raw %}
```yaml
---
- name: Check Status
  hosts: node1
  become: true
  vars:
    package: "httpd"

  tasks:
    - name: Check status of {{ package }} service
      ansible.builtin.service_facts:
      register: service_state

    - ansible.builtin.debug:
        var: service_state.ansible_facts.services["{{ package }}.service"].state
```

```bash
{% endraw %}

[student@ansible-1 ~]$ ansible-navigator run service_state.yml
```

### Etape 5 - Ajout de tache: Création de fichier html

Vérifiez que les tâches ont été exécutées correctement et qu'Apache accepte les connexions: effectuez une requête HTTP à l'aide du module `uri` d'Ansible dans un Playbook intitulé `check_httpd.yml` depuis le noeud de contrôle vers `node1`.

{% raw %}
```yaml
---
- name: Check URL
  hosts: control
  vars:
    node: "node1"

  tasks:
    - name: Check that you can connect (GET) to a page and it returns a status 200
      ansible.builtin.uri:
        url: "http://{{ node }}"

```
{% endraw %}

> **Avertissement**
>
> **Attendez-vous à beaucoup de lignes rouges et un statut 403 \!**

```bash
[student@ansible-1 ~]$ ansible-navigator run check_httpd.yml -m stdout
```

Il y a beaucoup de lignes rouges et une erreur: tant qu'il n'y a pas le fichier `web.html` servi par Apache, il affichera un vilain statut ""HTTP Error 403: Forbidden"" et Ansible signalera une erreur.

Alors pourquoi ne pas utiliser Ansible pour déployer un simple fichier `web.html`? Sur l'hôte de contrôle ansible, en tant qu'utilisateur `student`, créez le répertoire `files` pour contenir les fichiers ressources dans `~/ ansible-files/`:

```bash
[student@ansible-1 ansible-files]$ mkdir files
```

Créez ensuite le fichier `~/ansible-files/files/web.html` sur le nœud de contrôle:

```html
<body>
<h1>Apache is running fine</h1>
</body>
```

Vous avez déjà utilisé le module `copy` d'Ansible pour écrire le texte fourni sur la ligne de commande dans un fichier. Vous allez maintenant utiliser le module de votre Playbook pour copier un fichier.

Sur le nœud de contrôle, en tant qu'utilisateur `student`, modifiez le fichier `~/ansible-files/apache.yml` et ajoutez une nouvelle tâche en utilisant le module `copy`. Il devrait maintenant ressembler à ceci:

```yaml
---
- name: Apache server installed
  hosts: node1
  become: true
  tasks:

    - name: Install Apache
      ansible.builtin.dnf:
        name: httpd

    - name: Apache enabled and running
      ansible.builtin.service:
        name: httpd
        enabled: true
        state: started

    - name: Copy index.html
      ansible.builtin.copy:
        src: web.html
        dest: /var/www/html/index.html
        mode: '644'
```

Que fait cette nouvelle tâche de copie ? La nouvelle tâche utilise le module `copy` et définit la source et la destination pour l'opération de copie en tant que paramètres.

Exécutez votre Playbook étendu:

```bash
[student@ansible-1 ansible-files]$ ansible-navigator run apache.yml -m stdout
```

* Regardez bien la sortie, notez les changements "CHANGED" et les tâches associées à ces changements.

* Exécutez à nouveau le Playbook `check_httpd.yml` avec le module `uri` employé ci-dessus pour tester Apache. La commande devrait maintenant renvoyer une ligne verte "status: 200" entre autres informations.

### Etape 6 - Application à plusieurs hôtes

Bien que les manipulations précédentes montrent la simplicité d'appliquer des changements sur un hôte particulier, qu'en est-il de propager des changements à de nombreux hôtes ? C'est maintenant qu'on constate le vrai pouvoir de Ansible, alors qu'il applique les mêmes jeux de tâches de manière fiable sur de nombreux hôtes.

* Alors, qu'en est-il de changer le Playbook apache.yml pour qu'il fonctionne sur `node1` **et** `node2` **et** `node3`?

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

Modifiez le paramètre `hosts` du Playbook pour pointer vers le groupe `web` au lieu de `node1`:

```yaml
---
- name: Apache server installed
  hosts: web
  become: true
  tasks:

    - name: Install Apache
      ansible.builtin.dnf:
        name: httpd

    - name: Apache enabled and running
      ansible.builtin.service:
        name: httpd
        enabled: true
        state: started

    - name: Copy index.html
      ansible.builtin.copy:
        src: web.html
        dest: /var/www/html/index.html
        mode: '644'

```

Maintenant, lancez le Playbook:

```bash
[student@ansible-1 ansible-files]$ ansible-navigator run apache.yml -m stdout
```

Enfin, vérifiez si Apache fonctionne maintenant sur tous les serveurs web (node1, node2, node3). Toute sortie doit être verte.

---
**Navigation**
<br>

{% if page.url contains 'ansible_rhel_90' %}
[Exercise précédent](../2-thebasics/README.fr.md) - [Exercise suivant](../4-variables/README.fr.md)
{% else %}
[Exercise précédent](../1.2-thebasics/README.fr.md) - [Exercise suivant](../1.4-variables/README.fr.md)
{% endif %}
<br><br>
