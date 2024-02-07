# Exercice d'Atelier - Les Fondamentaux d'Ansible

**Lisez ceci dans d'autres langues** :
<br>![uk](../../../images/uk.png) [Anglais](README.md), ![japan](../../../images/japan.png) [日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugais du Brésil](README.pt-br.md), ![france](../../../images/fr.png) [Français](README.fr.md), ![Español](../../../images/col.png) [Espagnol](README.es.md).

## Table des Matières <!-- omettre dans toc -->

- [Objectif](#objectif)
- [Guide](#guide)
  - [Les Bases du Fichier d'Inventaire](#les-bases-du-fichier-dinventaire)
  - [Découverte de Modules](#découverte-de-modules)
  - [Accès à la Documentation des Modules](#accès-à-la-documentation-des-modules)

## Objectif

Dans cet exercice, nous allons explorer le dernier utilitaire de ligne de commande d'Ansible `ansible-navigator` pour apprendre à travailler avec des fichiers d'inventaire et la liste des modules lorsqu'une assistance est nécessaire. L'objectif est de vous familiariser avec le fonctionnement d'`ansible-navigator` et comment il peut être utilisé pour enrichir votre expérience avec Ansible.

## Guide

### Les Bases du Fichier d'Inventaire

Un fichier d'inventaire est un fichier texte qui spécifie les nœuds qui seront gérés par la machine de contrôle. Les nœuds à gérer peuvent inclure une liste de noms d'hôtes ou d'adresses IP de ces nœuds. Le fichier d'inventaire permet d'organiser les nœuds en groupes en déclarant un nom de groupe d'hôtes entre crochets ([]).

### Explorer l'Inventaire

Pour utiliser la commande `ansible-navigator` pour la gestion des hôtes, vous devez fournir un fichier d'inventaire qui définit une liste d'hôtes à gérer depuis le nœud de contrôle. Dans ce laboratoire, l'inventaire est fourni par votre instructeur. Le fichier d'inventaire est un fichier formaté `ini` listant vos hôtes, triés par groupes, fournissant également certaines variables. Un exemple peut ressembler à ce qui suit :

```bash
[web]
node1 ansible_host=<X.X.X.X>
node2 ansible_host=<Y.Y.Y.Y>
node3 ansible_host=<Z.Z.Z.Z>

[control]
ansible-1 ansible_host=44.55.66.77
```

Pour voir votre inventaire avec ansible-navigator, utilisez la commande `ansible-navigator inventory --list -m stdout`. Cette commande affiche tous les nœuds et leurs groupes respectifs.

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

NOTE : `-m` est l'abréviation de `--mode` qui permet de passer au mode de sortie standard au lieu d'utiliser l'interface utilisateur basée sur le texte (TUI).

Pour une vue moins détaillée, `ansible-navigator inventory --graph -m stdout` offre une représentation visuelle des groupements.

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

Nous pouvons clairement voir que les nœuds : `node1`, `node2`, `node3` font partie du groupe `web`, tandis que `ansible-1` fait partie du groupe `control`.

Un fichier d'inventaire peut organiser vos hôtes en groupes ou définir des variables. Dans notre exemple, l'inventaire actuel a les groupes `web` et `control`. Exécutez `ansible-navigator` avec ces modèles d'hôtes et observez la sortie :

En utilisant la commande `ansible-navigator inventory`, vous pouvez exécuter des commandes qui fournissent des informations uniquement pour un hôte ou un groupe. Par exemple, exécutez les commandes suivantes et observez leurs différentes sorties.

```bash
[student@ansible-1 ~]$ ansible-navigator inventory --graph web -m stdout
[student@ansible-1 ~]$ ansible-navigator inventory --graph control -m stdout
[student@ansible-1 ~]$ ansible-navigator inventory --host node1 -m stdout
```

> **Conseil**
>
> L'inventaire peut contenir plus de données. Par exemple, si vous avez des hôtes qui fonctionnent sur des ports SSH non standard, vous pouvez mettre le numéro de port après le nom d'hôte avec deux points. On peut également définir des noms spécifiques à Ansible et les faire pointer vers l'IP ou le nom d'hôte.

### Découverte de Modules

La Plateforme d'Automatisation Ansible est livrée avec plusieurs Environnements d'Exécution (EE) pris en charge. Ces EE sont livrés avec des collections prises en charge groupées contenant du contenu pris en charge, y compris des modules.

> **Conseil**
>
> Dans `ansible-navigator`, sortez en appuyant sur le bouton `ESC`.

Pour parcourir vos modules disponibles, entrez d'abord en mode interactif :

```bash
$ ansible-navigator
```

![image d'ansible-navigator](images/interactive-mode.png)

Parcourez une collection en tapant `:collections`

```bash
:collections
```

![image d'ansible-navigator](images/interactive-collections.png)

### Accès à la Documentation des Modules

Pour explorer les modules d'une collection spécifique, entrez le numéro à côté du nom de la collection.

Par exemple, dans la capture d'écran ci-dessus, le numéro `0` correspond à la collection `amazon.aws`. Pour zoomer sur la collection, tapez le numéro `0`.

```bash
0
```

![image d'ansible-navigator](images/interactive-aws.png)

Accédez directement à la documentation détaillée de n'importe quel module en spécifiant son numéro correspondant. Par exemple, le module `ec2_tag` correspond à `24`.

```bash
:24
```

En faisant défiler vers le bas à l'aide des touches fléchées ou de page en haut et page en bas, nous pouvons voir la documentation et les exemples.

![image d'ansible-navigator](images/interactive-ec2-tag.png)

Vous pouvez accéder directement à un module particulier en tapant simplement `:doc namespace.collection.module-name`. Par exemple, taper `:doc amazon.aws.ec2_tag` vous amènerait directement à la page finale montrée ci-dessus.

> **Conseil**
>
> Différents environnements d'exécution peuvent avoir accès à différentes collections et à différentes versions de ces collections. En utilisant la documentation intégrée, vous savez qu'elle sera précise pour cette version particulière de la collection.


---
**Navigation**
{% if page.url contains 'ansible_rhel_90' %}
[Exercice précédent](../1-setup/README.fr.md) - [Exercice suivant](../3-playbook/README.fr.md)
{% else %}
[Exercice précédent](../1.1-setup/README.fr.md) - [Exercice suivant](../1.3-playbook/README.fr.md)
{% endif %}
<br><br>

