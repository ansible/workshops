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

If you notice, prior to the play name `Apache server installed`, you'll see a `0`. By pressing the `0` key on your keyboard, you will be provided a new window view displaying the different tasks that ran for the playbook completion. In this example, those tasks included the "Gathering Facts" and "Install Apache". The "Gathering Facts" is a built-in task that runs automatically at the beginning of each play. It collects information about the managed nodes. Exercises later on will cover this in more detail. The "Install Apache" was the task created within the `apache.yml` file that installed `httpd`.

The display should look something like this:

```bash
  RESULT      HOST	NUMBER      CHANGED       TASK                                                   TASK ACTION           DURATION
0│OK          node1          0        False       Gathering Facts                                        gather_facts                1s
1│OK          node1          1         True       Install Apache                        dnf                         4s
```

Taking a closer look, you'll notice that each task is associated with a number. Task 1, "Install Apache", had a change and used the `dnf` module. In this case, the change is the installation of Apache (`httpd` package) on the host `node1`.

By pressing `0` or `1` on your keyboard, you can see further details of the task being run. If a more traditional output view is desired, type `:st` within the text user interface.

Once you've completed, reviewing your Ansible playbook, you can exit out of the TUI via the Esc key on your keyboard.

> **Tip**
>
> The Esc key only takes you back to the previous screen. Once at the main overview screen an additional Esc key will take you back to the terminal window.


Once the playbook has completed, connect to `node1` via SSH to make sure Apache has been installed:

```bash
[student@ansible-1 ansible-files]$ ssh node1
Last login: Wed May 15 14:03:45 2019 from 44.55.66.77
Managed by Ansible
```

Use the command `rpm -qi httpd` to verify httpd is installed:

```bash
[ec2-user@node1 ~]$ rpm -qi httpd
Name        : httpd
Version     : 2.4.37
[...]
```

Log out of `node1` with the command `exit` so that you are back on the control host and verify the installed package with an Ansible playbook labeled `package.yml`

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

Run the the `ansible-navigator run apache.yml` playbook for a second time, and compare the output. The output "CHANGED" now shows `0` instead of `1` and the color changed from yellow to green. This makes it easier to spot when changes have occured when running the Ansible playbook.

### Etape 4 - Extend your Playbook: Start & Enable Apache

The next part of the Ansible playbook makes sure the Apache application is enabled and started on `node1`.

On the control host, as your student user, edit the file `~/ansible-files/apache.yml` to add a second task using the `service` module. The Playbook should now look like this:

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

What exactly did we do?

* a second task named "Apache enabled and running" is created
* a module is specified (`service`)
* The module `service` takes the name of the service (`httpd`), if it should be permanently set (`enabled`), and its current state (`started`)


Thus with the second task we make sure the Apache server is indeed running on the target machine. Run your extended Playbook:

```bash
[student@ansible-1 ~]$ ansible-navigator run apache.yml
```

Notice in the output, we see the play had `1` "CHANGED" shown in yellow and if we press `0` to enter the play output, you can see that task 2, "Apache enabled and running", was the task that incorporated the latest change by the "CHANGED" value being set to True and highlighted in yellow.


* Run the playbook a second time using `ansible-navigator` to get used to the change in the output.

* Use an Ansible playbook labeled service_state.yml to make sure the Apache (httpd) service is running on `node1`, e.g. with: `systemctl status httpd`.

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

### Etape 5 - Extend your Playbook: Create an web.html

Check that the tasks were executed correctly and Apache is accepting connections: Make an HTTP request using Ansible’s `uri` module in a playbook named check_httpd.yml from the control node to `node1`.

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

> **Warning**
>
> **Expect a lot of red lines and a 403 status\!**

```bash
[student@ansible-1 ~]$ ansible-navigator run check_httpd.yml -m stdout
```

There are a lot of red lines and an error: As long as there is not at least an `web.html` file to be served by Apache, it will throw an ugly "HTTP Error 403: Forbidden" status and Ansible will report an error.

So why not use Ansible to deploy a simple `web.html` file? On the ansible control host, as the `student` user, create the directory `files` to hold file resources in `~/ansible-files/`:

```bash
[student@ansible-1 ansible-files]$ mkdir files
```

Then create the file `~/ansible-files/files/web.html` on the control node:

```html
<body>
<h1>Apache is running fine</h1>
</body>
```

In a previous example, you used Ansible’s `copy` module to write text supplied on the command line into a file. Now you’ll use the module in your playbook to copy a file.

On the control node as your student user edit the file `~/ansible-files/apache.yml` and add a new task utilizing the `copy` module. It should now look like this:

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

What does this new copy task do? The new task uses the `copy` module and defines the source and destination options for the copy operation as parameters.

Run your extended Playbook:

```bash
[student@ansible-1 ansible-files]$ ansible-navigator run apache.yml -m stdout
```

* Have a good look at the output, notice the changes of "CHANGED" and the tasks associated with that change.

* Run the Ansible playbook check_httpd.yml using the "uri" module from above again to test Apache. The command should now return a friendly green "status: 200" line, amongst other information.

### Etape 6 - Practice: Apply to Multiple Host

While the above, shows the simplicity of applying changes to a particular host. What about if you want to set changes to many hosts? This is where you'll notice the real power of Ansible as it applies the same set of tasks reliably to many hosts.

* So what about changing the apache.yml Playbook to run on `node1` **and** `node2` **and** `node3`?

As you might remember, the inventory lists all nodes as members of the group `web`:

```ini
[web]
node1 ansible_host=11.22.33.44
node2 ansible_host=22.33.44.55
node3 ansible_host=33.44.55.66
```

> **Tip**
>
> The IP addresses shown here are just examples, your nodes will have different IP addresses.

Change the playbook `hosts` parameter to point to `web` instead of `node1`:

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

Now run the playbook:

```bash
[student@ansible-1 ansible-files]$ ansible-navigator run apache.yml -m stdout
```

Verify if Apache is now running on all web servers (node1, node2, node3). All output should be green.

---
**Navigation**
<br>

{% if page.url contains 'ansible_rhel_90' %}
[Previous Exercise](../2-thebasics) - [Next Exercise](../4-variables)
{% else %}
[Previous Exercise](../1.2-thebasics) - [Next Exercise](../1.4-variables)
{% endif %}
<br><br>
