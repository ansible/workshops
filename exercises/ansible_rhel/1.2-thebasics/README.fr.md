# Exercice - Les Bases d'Ansible <!-- omit in toc -->

**Lisez ceci dans d'autres langues**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Français](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table des matières <!-- omit in toc -->

- [Objectif](#objectif)
- [Guide](#guide)
  - [Étape 1 - Travailler avec votre inventaire](#Étape-1---travailler-avec-votre-inventaire)
  - [Étape 2 - Liste des modules et obtention d'aide](#Étape-4---liste-des-modules-et-obtention-d-aide)

## Objectif

Dans cet exercice, nous allons explorer le dernier utilitaire en ligne de commande `ansible-navigator` pour apprendre comment travailler avec les fichiers d'inventaire et obtenir la liste des modules en cas de besoin. Le but est de vous familiariser avec le fcontionnement de `ansible-navigator` et la façon dont il peut être utilisé pour enrichir votre expérience Ansible.

Cet exercice couvrira
* L'utilisation de fichiers d'inventaire
* La localisation et la compréhension d'un fichier d'inventaire au format `ini`
* L'obtention de la liste des modules et d'aide pour les utiliser

## Guide

### Étape 1 - Travailler avec votre inventaire

Un fichier d'inventaire est un fichier texte qui spécifie les noeuds qui seront gérés par la machine de contrôle. Les noeuds à gérer peuvent inclure une liste de hostnames ou les adresses IP de ces hôtes. Le fichier d'inventaire permet d'organiser les noeuds dans des groupes en déclarant un nom de groupe d'hôtes entre des crochets ([]).

Pour gérer les hôtes avec la commande `ansible-navigator`, vous devez fournir un fichier d'inventaire qui définit une liste d'hôtes à gérer depuis le noeud de contrôle. Dans ce lab, l'inventaire est déjà fourni. Le ficher d'inventaire est un fichier au format `ini` qui liste les hôtes, rangés par groupes, avec des varaiables additionnelles. Il ressemble à ceci :

```bash
[web]
node1 ansible_host=<X.X.X.X>
node2 ansible_host=<Y.Y.Y.Y>
node3 ansible_host=<Z.Z.Z.Z>

[control]
ansible-1 ansible_host=44.55.66.77
```

Ansible est déjà configuré pour utiliser l'inventaire propre à votre environnement. Nous allons vous montrer dans la prochaine étape comment c'est réalisé. Pour le moment, nous allons exécuter des commandes simples pour travailler avec l'inventaire.

Pour employer tous les hôtes de l'inventaire, vous fournissez un pattern à la commande `ansible-navigator`. La commande `ansible-navigator inventory` a une option `--list` qui peut être utile pour afficher tous les hôtes qui sont dans un fichier d'inventaire, en incluant les groupes auxquels ils sont associés.

```bash
[student@ansible-1 rhel_workshop]$ cd /home/student
[student@ansible-1 ~]$ ansible-navigator inventory --list -m stdout
{
    "_meta": {
        "hostvars": {
            "ansible-1": {
                "ansible_host": "3.236.186.92"            },
            "node1": {
                "ansible_host": "3.239.234.187"
            },
            "node2": {
                "ansible_host": "75.101.228.151"
            },
            "node3": {
                "ansible_host": "100.27.38.142"
            }
        }
    },
    "all": {
        "children": [
            "control",
            "ungrouped",
            "web"
        ]
    },
    "control": {
        "hosts": [
            "ansible-1"
        ]
    },
    "web": {
        "hosts": [
            "node1",
            "node2",
            "node3"
        ]
    }
}

```

NOTE: `-m` est le raccourci de `--mode` qui permet de changer le mode en output standard au lieu d'utiliser l'interface en mode texte (TUI).

Si `--list` est trop verbeux, l'option `--graph` peut être utilisée pour fournir une version plus compacte de `--list`.

```bash
[student@ansible-1 ~]$ ansible-navigator inventory --graph -m stdout
@all:
  |--@control:
  |  |--ansible-1
  |--@ungrouped:
  |--@web:
  |  |--node1
  |  |--node2
  |  |--node3

```

On peut bien voir que les noeuds: `node1`, `node2`, `node3` sont dans le groupe `web` group, tandis que `ansible-1` est dans le groupe `control`.

Un fichier d'inventaire peut contenir bien plus d'informations, il peut organiser les hôtes dans des groupes ou définir des variables. Dans notre exemple, l'inventaire courant a les groupes `web` et `control`. Lancez Ansible avec ces patterns d'hôtes et observez le résultat.

En utilisant la commande `ansible-navigator inventory`, on peut aussi lancer des commandes qui fournissent des informations uniquement sur un hôte ou un groupe. Par exemple, essayez la commande suivante pour observer son résultat:

```bash
[student@ansible-1 ~]$ ansible-navigator inventory --graph web -m stdout
[student@ansible-1 ~]$ ansible-navigator inventory --graph control -m stdout
[student@ansible-1 ~]$ ansible-navigator inventory --host node1 -m stdout
```

> **Astuce**
>
> L'inventaire contient plus de données. Par exemple, si vous avez des hôtes qui exposent un port SSH non standard, vous pouvez renseigner le numéro de port après le nom d'hôte à l'aide des deux-points (:). Ou encore, vous pouvez renseignez dess noms propres à Ansible et les faire pointer vers les adresse IP ou nom d'hôtes réels.

### Etape 2 - Liste des modules et obtention d aide

Ansible Automation Platform est livré avec plusieurs Environnements d'Execution (EE) supportés. Ces EE sont fournis avec des collections supportées qui contiennent du contenu supporté, comme des modules.

> **Astuce**
>
> Dans `ansible-navigator` quittez en pressant la touche `ESC`.

Pour consulter les modules disponibles, entrez dans le mode interactif:

```bash
$ ansible-navigator
```

![picture of ansible-navigator](images/interactive-mode.png)

Commencez par consulter une collection en tapant `:collections`

```bash
:collections
```

![picture of ansible-navigator](images/interactive-collections.png)

Pour consulter le contenu d'une collection spécifique, tapez le numéro correspondant. Par exemple, sur la capture d'écran ci-dessus, le numéro `0` correspond à la collection `amazon.aws`. Pour zoomer dans cette collection, tapez `0`.

```bash
0
```

![picture of ansible-navigator](images/interactive-aws.png)

Obtenez de l'aide pour un module spécifique et son utilisation en zoomant davantage. Par exemple, le module `ec2_tag` correspond à `24`.

```bash
:24
```

Naviguez vers le bas, en utilisant les flèches ou les boutons page-haut et page-bas, pour obtenir de la documentation et des exemples.

![picture of ansible-navigator](images/interactive-ec2-tag.png)

Vous pouvez aussi sauter directement sur un module particulier en tapant simplement `:doc namespace.collection.module-name`. Par exemple, taper `:doc amazon.aws.ec2_tag` vous amène directement sur la dernière page affichée ci-dessus.

> **Astuce**
>
> Différents EE peuvent avoir accès à différentes collections, et différentes versions de ces collections. En utilisant la documentation embarquée, vous savez qu'elle sera appropriée pour cette version particulière de cette collection.

---
**Navigation**
{% if page.url contains 'ansible_rhel_90' %}
[Exercice précédent](../1-setup/README.fr.md) - [Exercice suivant](../3-playbook/README.fr.md)
{% else %}
[Exercice précédent](../1.1-setup/README.fr.md) - [Exercice suivant](../1.3-playbook/README.fr.md)
{% endif %}
<br><br>

