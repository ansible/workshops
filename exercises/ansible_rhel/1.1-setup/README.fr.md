# Atelier - Vérifier les prérequis

**Lisez ceci dans d'autres langues**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Français](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table des matières

- [Atelier - Vérifier les prérequis](#atelier---vérifier-les-prérequis)
  - [Table des matières](#table-des-matières)
  - [Objectif](#objectif)
  - [Guide](#guide)
    - [Votre Environment](#votre-environnement)
    - [Etape 1 - Accéder à l'environnement](#etape-1---accéder-à-l'environnement)
    - [Etape 2 - Utiliser le terminal](#etape-2---utiliser-le-terminal)
    - [Etape 3 - Examiner les Environnements d'Execution](#etape-3---examiner-les-environnements-d'execution)
    - [Etape 4 - Examiner la configuration de ansible-navigator](#etape-4---examiner-la-configuration-de-ansible-navigator)
    - [Etape 5 - Défis](#etape-5---défis)

## Objectif

* Comprendre la topologie du lab et comment accéder à l'environnement
* Comprendre comment les exercices de l'atelier fonctionnent
* Comprendre les défis

Ces premiers exercices explorent les utilitaires en ligne de commande (CLI) de Ansible Automation Platform. 

- [ansible-navigator](https://github.com/ansible/ansible-navigator) - un utilitaire en ligne de commande et une interface utilisateur en mode texte (TUI) pour exécuter et développer du contenu d'automatisation Ansible.
- [ansible-core](https://docs.ansible.com/core.html) - l'exécutable de base qui fournit le framework, le langage et les fonctions qui soutiennent Ansible Automation Platform. Il comprend également les divers outils CLI comme `ansible`, `ansible-playbook` et `ansible-doc`. Ansible Core agit comme un pont entre la communauté upstream et la version gratuite de Ansible et avec la version downstream d'automatisation d'entreprise offerte par Red Hat : Ansible Automation Platform.
- [Environnement d'Execution](https://docs.ansible.com/automation-controller/latest/html/userguide/execution_environments.html) - ne seront pas couvert particulièrement dans cet atelier car la version intégrée dans Ansible des Environnement d'Execution fournit déjà toutes les collections supportées par Red Hat, ce qui inclut les collections utilisées dans cet atelier. Les Environnements d'Execution sont des images de conteneur qui peuvent être utilisées pour exécuter de l'automatisation Ansible.
- [ansible-builder](https://github.com/ansible/ansible-builder) - ne sera pas particulièrement couvert dans cet atelier, `ansible-builder` est un utilitaire en ligne de commande pour automatiser le processuss de construction des Environnements d'Execution.

S'il vous faut davatange d'informations sur les nouveaux composants de Ansible Automation Platform, ajoutez en favori cette page [https://red.ht/AAP-20](https://red.ht/AAP-20)

## Guide

### Votre Environnement

Dans ce lab, vous travaillez avec un environement préconfiguré. Vous aurez accès aux hôtes suivants:

| Role                 | Inventory name |
| ---------------------| ---------------|
| Ansible Control Host | ansible-1      |
| Managed Host 1       | node1          |
| Managed Host 2       | node2          |
| Managed Host 3       | node3          |

### Etape 1 - Accéder à l'environnement

<table>
<thead>
  <tr>
    <th>Il est fortement recommandé d'utiliser Visual Studio Code pour faire les exercices de l'atelier. Visual Studio Code fournit:
    <ul>
    <li>Un navigateur de fichiers</li>
    <li>Un éditeur de texte avec coloration syntaxique</li>
    <li>Un terminal intégré au navigateur</li>
    </ul>
    L'accès SSH direct est disponible en secours, ou si un Visual Studio Code n'est pas suffisant. Cette vidéo Youtube apporte plus de clarification si nécessaire: <a href="https://youtu.be/Y_Gx4ZBfcuk">Ansible Workshops - Accessing your workbench environment</a>.
</th>
</tr>
</thead>
</table>

- Connectez-vous à Visual Studio Code depuis la page de l'atelier (fournie par votre instructeur). Le mot de passe est fourni sous le lien WebUI.

  ![launch page](images/launch_page.png)

- Entrez votre mot de passe pour vous connecter.

  ![login vs code](images/vscode_login.png)

  - Ouvrez le répertoire `rhel-workshop` dans Visual Studio Code:

### Etape 2 - Utiliser le terminal

- Ouvrez un terminal dans Visual Studio Code:

  ![picture of new terminal](images/vscode-new-terminal.png)

Naviguer vers le répertoire `rhel-workshop` sur le terminal du noeud de contrôle Ansible.

```bash
[student@ansible-1 ~]$ cd ~/rhel-workshop/
[student@ansible-1 rhel-workshop]$ pwd
/home/student/rhel-workshop
[student@ansible-1 rhel-workshop]$
```

* `~` - le tilde dans ce contexte est un raccourci pour le répertoire home, ici `/home/student`
* `cd` - commande Linux pour changer de répertoire
* `pwd` - commande Linux pour afficher le répertoire de travail courant. Le chemin complet du répertoire courant sera affiché.

### Etape 3 - Examiner les Environnements d'Execution

Exécuter la commande `ansible-navigator` avec l'argument `images` pour lister les Environnements d'Execution configurés sur le noeud de contrôle Ansible:

```bash
$ ansible-navigator images
```

![ansible-navigator images](images/navigator-images.png)


> Note: Le résultat obtenu peut différer légèrement du résultat ci-dessus.

Cette commande vous donne des informations sur les Environnements d'Execution (EE) actuellement installés. Renseignez-vous sur un EE en tapant le numéro correspondant. Par exemple taper **2** dans l'exemple ci-dessus ouvre l'environnement d'exécution `ee-supported-rhel8`:

![ee main menu](images/navigator-ee-menu.png)

Sélectionner `2` pour `Ansible version and collections` affiche les collections Ansible installées sur cet EE, et la version de `ansible-core`:

![ee info](images/navigator-ee-collections.png)

### Etape 4 - Examiner la configuration de ansible-navigator

Au choix, utilisez Visual Studio Code ou la commande `cat` pour voir le contenu du fichier `ansible-navigator.yml`. Le fichier est situé dnas le répertoire home:

```bash
$ cat ~/.ansible-navigator.yml
---
ansible-navigator:
  ansible:
    inventory:
      entries:
      - /home/student/lab_inventory/hosts

  execution-environment:
    image: registry.redhat.io/ansible-automation-platform-20-early-access/ee-supported-rhel8:2.0.0
    enabled: true
    container-engine: podman
    pull:
      policy: missing
    volume-mounts:
    - src: "/etc/ansible/"
      dest: "/etc/ansible/"
```

Notez les paramètres suivants dans le fichier `ansible-navigator.yml`:

* `inventories`: donne l'emplacement de l'inventaire Ansible utilisé
* `execution-environment`: donne l'emplacement de l'environnement d'exécution par défaut

Pour une liste complète des éléments configurables, consultez la [documentation](https://ansible.readthedocs.io/projects/navigator/settings/)

### Etape 5 - Défis

Certains chapitres de cet atelier comportent une section "Défi". Ces labs sont pensés pour vous donner une taĉhe à compléter en utilisant ce que vous avez appris jusque là. La solution est donnée en dessous du signe warning.

---
**Navigation**

<br>

{% if page.url contains 'ansible_rhel_90' %}
[Next Exercise](../2-thebasics/README.fr.md)
{% else %}
[Next Exercise](../1.2-thebasics/README.fr.md)
{% endif %}
<br><br>

[Cliquez ici pour revenir à l'atelier Ansible pour Red Hat Enterprise Linux](../README.fr.md#section-1---ansible-engine-exercises)
