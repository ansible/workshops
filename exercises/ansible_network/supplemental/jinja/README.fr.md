# Supplémentaire - Configuration Réseau avec les Modèles Jinja

**Lire ceci dans d'autres langues** : ![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English](README.md),  ![japan](https://github.com/ansible/workshops/raw/devel/images/japan.png) [日本語](README.ja.md),![Español](https://github.com/ansible/workshops/raw/devel/images/es.png) [Español](README.es.md).

## Table des Matières

- [Supplémentaire - Configuration Réseau avec les Modèles Jinja](#supplémentaire---configuration-réseau-avec-les-modèles-jinja)
  - [Table des Matières](#table-des-matières)
  - [Objectif](#objectif)
  - [Guide](#guide)
    - [Étape 1 - Création des variables de groupe](#étape-1---création-des-variables-de-groupe)
    - [Étape 2 - Création d'un modèle Jinja2](#étape-2---création-dun-modèle-jinja2)
    - [Étape 3 - Exploration du modèle Jinja2](#étape-3---exploration-du-modèle-jinja2)
    - [Étape 4 - Création d'un playbook](#étape-4---création-dun-playbook)
    - [Étape 5 - Exécution du Playbook Ansible](#étape-5---exécution-du-playbook-ansible)
    - [Étape 6 - Vérification de la configuration](#étape-6---vérification-de-la-configuration)
  - [Points à retenir](#points-à-retenir)
  - [Solution](#solution)
  - [Terminer](#terminer)

## Objectif

Démonstration de la génération d'une configuration réseau et de son application sur un appareil

* Utilisation et compréhension des [variables](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html) pour stocker les adresses IP souhaitées.
* Utilisation du [plugin de recherche de modèles Jinja2](https://docs.ansible.com/ansible/latest/plugins/lookup.html)
* Démonstration de l'utilisation du [module cli_config](https://docs.ansible.com/ansible/latest/modules/cli_config_module.html) pour l'automatisation réseau.

## Guide

### Étape 1 - Création des variables de groupe

Cette étape couvre la création de variables Ansible pour un Playbook Ansible. Cet exercice utilisera le schéma d'adresse IP suivant pour les adresses loopback sur rtr1 et rtr2 :

Appareil  | Adresse IP Loopback100 |
------------ | ------------- |
rtr1  | 192.168.100.1/32 |
rtr2  | 192.168.100.2/32 |

Les informations des variables peuvent être stockées dans `host_vars` et `group_vars`. Pour cet exercice, créez un dossier nommé `group_vars` :

- Créez un nouveau dossier appelé `group_vars`. Faites un clic droit sur la barre d'outils Explorer à gauche de Visual Studio Code et sélectionnez **New Folder**

   ![nouveau dossier](images/ansible-navigator-new-folder.png)

- Créez un nouveau fichier appelé `all.yml`. Faites un clic droit sur la barre d'outils Explorer à gauche de Visual Studio Code et sélectionnez **New File** dans le répertoire `group_vars`.

   ![nouveau fichier](images/ansible-navigator-new-file.png)

Les informations sur l'interface et l'adresse IP ci-dessus doivent être stockées en tant que variables afin que le playbook Ansible puisse les utiliser. Commencez par créer un dictionnaire YAML simple qui stocke le tableau listé ci-dessus. Utilisez une variable de haut niveau (par exemple `nodes`) afin de pouvoir effectuer une recherche basée sur le `inventory_hostname` :

```yaml
nodes:
  rtr1:
    Loopback100: "192.168.100.1"
  rtr2:
    Loopback100: "192.168.100.2"
```

Copiez le dictionnaire YAML que nous avons créé ci-dessus dans le fichier `group_vars/all.yml` et enregistrez le fichier.

> Tous les appareils font partie du groupe **all** par défaut. Si nous créons un groupe nommé **cisco**, seuls les appareils réseau appartenant à ce groupe pourront accéder à ces variables.

### Étape 2 - Création d'un modèle Jinja2

Créez un nouveau fichier appelé `template.j2` dans le répertoire `network-workshop`. Faites un clic droit sur la barre d'outils Explorer à gauche de Visual Studio Code et sélectionnez **New File**. La structure du répertoire ressemblera à ceci :

```
├── group_vars
│   └── all.yml
├── template.j2
```

Copiez ce qui suit dans le fichier template.j2 :

<!-- {% raw %} -->

```yaml
{% for interface,ip in nodes[inventory_hostname].items() %}
interface {{interface}}
  ip address {{ip}} 255.255.255.255
{% endfor %}
```

<!-- {% endraw %} -->

Enregistrez le fichier.

### Étape 3 - Exploration du modèle Jinja2

Cette étape expliquera et élaborera chaque partie du fichier template.j2 nouvellement créé.

<!-- {% raw %} -->

```yaml
{% for interface,ip in nodes[inventory_hostname].items() %}
```

<!-- {% endraw %} -->

<!-- {% raw %} -->
* Les morceaux de code dans un modèle Jinja sont échappés avec `{%` et `%}`. La déclaration `interface,ip` décompose le dictionnaire en une clé nommée `interface` et une valeur nommée `ip`.
<!-- {% endraw %} -->

* Le `nodes[inventory_hostname]` effectue une recherche de dictionnaire dans le fichier `group_vars/all.yml`. La variable **inventory_hostname** est le nom de l'hôte configuré dans le fichier d'inventaire d'Ansible. Lorsque le playbook est exécuté contre `rtr1`, inventory_hostname sera `rtr1`, et pour `rtr2`, ce sera `rtr2`, etc.

> La variable inventory_hostname est considérée comme une [variable magique](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#magic-variables-and-how-to-access-information-about-other-hosts) automatiquement fournie.

* Le mot-clé `items()` retourne une liste de dictionnaires. Dans ce cas, la clé du dictionnaire est le nom de l'interface (par exemple Loopback100) et la valeur est une adresse IP (par exemple 192.168.100.1)

<!-- {% raw %} -->
```yaml
interface {{ interface }}
  ip address {{ i }} 255.255.255.255
```
<!-- {% endraw %} -->

* Les variables sont rendues avec les accolades comme ceci : `{{ variable_here }}`. Dans ce cas, les noms des variables n'existent que dans le contexte de la boucle. En dehors de la boucle, ces deux variables n'existent pas. Chaque itération réattribuera les variables à de nouvelles valeurs en fonction de ce que nous avons dans nos variables.

Enfin :

<!-- {% raw %} -->
```yaml
{% endfor %}
```
<!-- {% endraw %} -->

* En Jinja, nous devons spécifier la fin de la boucle.

### Étape 4 - Création d'un playbook

- Créez un nouveau fichier de Playbook Ansible appelé `config.yml`. Faites un clic droit sur la barre d'outils Explorer à gauche de Visual Studio Code et sélectionnez **New File**. Copiez le playbook ci-dessous ou tapez-le :

<!-- {% raw %} -->
```yaml
---
- name: configure network devices
  hosts: rtr1,rtr2
  gather_facts: false
  tasks:
    - name: configure device with config
      cli_config:
        config: "{{ lookup('template', 'template.j2') }}"
```
<!-- {% endraw %} -->

* Ce Playbook Ansible contient une tâche nommée *configure device with config*
* Le module **cli_config** est indépendant du fournisseur. Ce module fonctionnera de manière identique pour un appareil Arista, Cisco ou Juniper. Ce module fonctionne uniquement avec le plugin de connexion **network_cli**.
* Le module cli_config ne nécessite qu'un paramètre, dans ce cas **config**, qui peut pointer vers un fichier plat ou utiliser le plugin de recherche comme ici. Pour une liste complète des plugins de recherche disponibles [visitez la documentation](https://docs.ansible.com/ansible/latest/plugins/lookup.html)
* L'utilisation du plugin de recherche template nécessite deux paramètres : le type de plugin *template* et le nom du modèle correspondant *template.j2*.

### Étape 5 - Exécution du Playbook Ansible

Utilisez la commande `ansible-navigator` pour exécuter le playbook :

```
[student@ansible network-workshop]$ ansible-playbook config.yml
```

La sortie ressemblera à ceci :

```
[student@ansible-1 network-workshop]$ ansible-navigator run config.yml --mode stdout

PLAY [configure network devices] ***********************************************

TASK [configure device with config] ********************************************
changed: [rtr1]
changed: [rtr2]

PLAY RECAP *********************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
rtr2                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

### Étape 6 - Vérification de la configuration

Utilisez la commande `show ip int br` pour vérifier que les adresses IP ont été confirmées sur les appareils réseau.

```sh
[student@ansible network-workshop]$ ssh rtr1

rtr1#show ip int br | include Loopback100
Loopback100            192.168.100.1   YES manual up                    up
```

## Points à retenir

* Le [plugin de recherche de modèles Jinja2](https://docs.ansible.com/ansible/latest/plugins/lookup.html) permet de générer une configuration pour un appareil.
* Les modules `config` (par exemple `cisco.ios.config`, `arista.eos.config`) et cli_config peuvent utiliser un fichier de modèle Jinja2 et l'appliquer directement sur un appareil. Si vous souhaitez simplement générer une configuration localement sur le nœud de contrôle, utilisez le [module template](https://docs.ansible.com/ansible/latest/modules/template_module.html).
* Les variables sont le plus souvent stockées dans `group_vars` et `host_vars`. Cet exemple court n'a utilisé que group_vars.

## Solution

Le Playbook Ansible final est fourni ici comme référence : [config.yml](config.yml).

Le modèle Jinja2 fourni est disponible ici : [template.j2](template.j2).

## Terminer

Vous avez terminé cet exercice de laboratoire.

---

[Cliquez ici pour revenir au Workshop d'Automatisation de Réseaux Ansible](../../README.fr.md)
