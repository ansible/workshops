# Atelier - Exécution de commandes Ad-hoc

**Lisez ceci dans d'autres langues**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).


## Table des matières

* [Objectif](#objectif)
* [Guide](#guide)
* [Étape 1 - Travailler avec votre inventaire](#Étape-1---travailler-avec-votre-inventaire)
* [Étape 2 - Les fichiers de configuration Ansible](#Étape-2---les-fichiers-de-configuration-ansible)
* [Étape 3 - Ping d'un hôte](#Étape-3---ping-d-un-hôte)
* [Étape 4 - Liste des modules et obtention d'aide](#Étape-4---liste-des-modules-et-obtention-d-aide)
* [Étape 5 - Utilissation du module commande](#Étape-5---utilisation-du-module-commande)
* [Étape 6 - Le module de copie et les autorisations](#Étape-6---le-module-de-copie-et-les-autorisations)
* [Défi: Les modules](#défi-les-modules)

# Objectif

Pour notre premier exercice, nous allons exécuter quelques commandes Ad-hoc pour vous aider à comprendre comment fonctionne Ansible. Les commandes Ad-Hoc Ansible vous permettent d'effectuer des tâches sur des nœuds distants sans avoir à écrire un playbook. Ils sont très utiles lorsque vous devez simplement faire une ou deux choses rapidement et souvent, sur de nombreux nœuds distants.

Cet exercice couvrira
- Localisation et compréhension du fichier de configuration Ansible (`ansible.cfg`)
- Localisation et compréhension d'un fichier d'inventaire au format "ini"
- Exécution de commandes ad hoc

# Guide

## Étape 1 - Travailler avec votre inventaire

Pour utiliser Ansible, vous devez fournir un fichier d'inventaire qui définit une liste d'hôtes à gérer. Dans cet atelier, l'inventaire est fourni par votre instructeur. L'inventaire est un fichier au format ini répertoriant vos hôtes, trié en groupes, fournissant en outre certaines variables.
Par exemple:

```bash
[web]
node1 ansible_host=<X.X.X.X>
node2 ansible_host=<Y.Y.Y.Y>
node3 ansible_host=<Z.Z.Z.Z>

[control]
ansible ansible_host=44.55.66.77
```

Ansible est déjà configuré pour utiliser l'inventaire spécifique à votre environnement. Nous vous montrerons à l'étape suivante comment procéder. Pour l'instant, nous allons exécuter quelques commandes simples pour comprendre l'inventaire.

Pour référencer les hôtes d'inventaire, vous fournissez un modèle d'hôte à la commande ansible. Ansible a une option `--list-hosts` qui peut être utile pour clarifier quels hôtes gérés sont référencés par le modèle d'hôte dans une commande ansible.

Le modèle d'hôte le plus basique est le nom d'un seul hôte géré répertorié dans le fichier d'inventaire. Cela spécifie que l'hôte sera le seul dans le fichier d'inventaire qui sera traité par la commande ansible.
Executez:

```bash
[student<X@>ansible ~]$ ansible node1 --list-hosts
  hosts (1):
    node1
```

Un fichier d'inventaire peut contenir beaucoup plus d'informations, il peut organiser vos hôtes en groupes ou définir des variables. Dans notre exemple, l'inventaire actuel a les groupes «web» et «control». Exécutez Ansible avec ces modèles d'hôte et observez la sortie:

```bash
[student<X@>ansible ~]$ ansible web  --list-hosts
[student<X@>ansible ~]$ ansible web,ansible --list-hosts
[student<X@>ansible ~]$ ansible 'node*' --list-hosts
[student<X@>ansible ~]$ ansible all --list-hosts
```

Comme vous le voyez, il est correct de placer les systèmes dans plusieurs groupes. Par exemple, un serveur peut être à la fois un serveur Web et un serveur de base de données. Notez que dans Ansible, les groupes ne sont pas nécessairement hiérarchiques.

> **Astuce**
>
> L'inventaire peut contenir plus de données. Par exemple. si vous avez des hôtes qui s'exécutent sur des ports SSH non standard, vous pouvez mettre le numéro de port après le nom d'hôte avec deux points. Ou vous pouvez définir des noms spécifiques à Ansible et les faire pointer vers la "vraie" IP ou le nom d'hôte.

## Étape 2 - Les fichiers de configuration Ansible

Le comportement d'Ansible peut être personnalisé en modifiant les paramètres du fichier de configuration d'Ansible (format ini). Ansible sélectionnera son fichier de configuration à partir de plusieurs emplacements possibles sur le nœud de contrôle, veuillez vous référer à la [documentation](https://docs.ansible.com/ansible/latest/reference_appendices/config.html).

> **Astuce**
>
> La pratique recommandée est de créer un fichier `ansible.cfg` dans le répertoire à partir duquel vous exécutez les commandes Ansible. Ce répertoire contiendrait également tous les fichiers utilisés par votre projet Ansible, tels que l'inventaire et les playbooks. Une autre pratique recommandée est de créer un fichier `.ansible.cfg` dans votre répertoire personnel.

Dans l'environnement de laboratoire qui vous est fourni, un fichier `.ansible.cfg` a déjà été créé et rempli avec les détails nécessaires dans le répertoire personnel de votre `student<X>` sur le nœud de contrôle:

```bash
[student<X>@ansible ~]$ ls -la .ansible.cfg
-rw-r--r--. 1 student<X> student<X> 231 14. Mai 17:17 .ansible.cfg
```

Affichez le fichier de configuration:

```bash
[student<X>@ansible ~]$ cat .ansible.cfg
[defaults]
stdout_callback = community.general.yaml
connection = smart
timeout = 60
deprecation_warnings = False
host_key_checking = False
retry_files_enabled = False
inventory = /home/student<X>/lab_inventory/hosts
```

Plusieurs options de configuration sont fournis. La plupart d'entre eux ne sont pas intéressantes ici, mais assurez-vous de noter la dernière ligne: l'emplacement de l'inventaire est indiqué. C'est ainsi qu'Ansible savait dans les commandes précédentes à quelles machines se connecter.

Affichez le fichier d'inventaire

```bash
[student<X>@ansible ~]$ cat /home/student<X>/lab_inventory/hosts
[web]
node1 ansible_host=11.22.33.44
node2 ansible_host=22.33.44.55
node3 ansible_host=33.44.55.66

[control]
ansible ansible_host=44.55.66.77
```

> **Astuce**
>
> Notez que chaque étudiant a un environnement de laboratoire individuel. Les adresses IP indiquées ci-dessus ne sont qu'un exemple et les adresses IP de vos environnements individuels sont différentes. Comme pour les autres cas, remplacez **\<X\>** par votre numéro d'étudiant réel.

## Étape 3 - Ping d un hôte

> **Avertissement**
>
> **N'oubliez pas d'exécuter les commandes depuis le répertoire personnel de votre utilisateur étudiant, `/home/student<X>`. C'est là que se trouve votre fichier `.ansible.cfg`, sans quoi Ansible ne saura pas quel inventaire utiliser.**

Commençons par quelque chose de vraiment basique - pinger un hôte. Pour ce faire, nous utilisons le module Ansible `ping`. Le module `ping` s'assure que nos hôtes cibles sont accessible. Fondamentalement, il se connecte à l'hôte géré, y exécute un petit script et collecte les résultats. Cela garantit que l'hôte géré est accessible et qu'Ansible est capable d'exécuter correctement les commandes sur celui-ci.

> **Astuce**
>
> Considérez un module comme un outil conçu pour accomplir une tâche spécifique.

Ansible doit savoir qu'il doit utiliser le module `ping`: L'option `-m` définit le module Ansible à utiliser. Les options peuvent être passées au module spécifié en utilisant l'option `-a`.

```bash
[student<X>@ansible ~]$ ansible web -m ping
node2 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
[...]
```

Comme vous le voyez, chaque nœud donne un resultat positif - ici "pong".

## Étape 4 - Liste des modules et obtention d aide

Ansible est livré avec de nombreux modules par défaut. Pour répertorier tous les modules exécutés:

```bash
[student<X>@ansible ~]$ ansible-doc -l
```

> **Astuce**
>
> Dans `ansible-doc` quittez en appuyant sur le bouton `q`. Utilisez les flèches `haut`/`bas` pour faire défiler le contenu.

Pour trouver un module, essayez par exemple:


```bash
[student<X>@ansible ~]$ ansible-doc -l | grep -i user
```

Obtenez de l'aide pour un module spécifique, y compris des exemples d'utilisation:

```bash
[student<X>@ansible ~]$ ansible-doc user
```

> **Astuce**
>
> Les options obligatoires sont marquées d'un "=" dans `ansible-doc`.

## Étape 5 - Utilisation du module commande:

Voyons maintenant comment exécuter une bonne commande Linux à l'ancienne à l'aide du module `command`.
Celui lui ci exécute simplement la commande spécifiée sur un hôte géré:

```bash
[student<X>@ansible ~]$ ansible node1 -m command -a "id"
node1 | CHANGED | rc=0 >>
uid=1001(student1) gid=1001(student1) Gruppen=1001(student1) Kontext=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
```
Dans ce cas, le module est appelé «commande» et l'option passée avec "-a" est la commande réelle à exécuter. Essayez d'exécuter cette commande Ad-hoc sur tous les hôtes gérés en utilisant le modèle d'hôte `all`.

Un autre exemple: jetez un œil aux versions du noyau que vos hôtes:

```bash
[student<X>@ansible ~]$ ansible all -m command -a 'uname -r'
```

Parfois, il est souhaitable d'avoir la sortie d'un hôte sur une seule ligne:

```bash
[student<X>@ansible ~]$ ansible all -m command -a 'uname -r' -o
```

> **Astuce**
>
> Comme de nombreuses commandes Linux, `ansible` permet des options de forme longue aussi bien que de forme courte. Par exemple, `ansible web --module-name ping` est identique à l'exécution de` ansible web -m ping`. Nous allons utiliser les options abrégées tout au long de cet atelier.

## Étape 6 - Le module de copie et les autorisations

En utilisant le module `copy`, exécutez une commande Ad-hoc sur `node1` pour changer le contenu du fichier `/etc/motd`. **Le contenu est remis au module via une option dans ce cas**.

Exécutez ce qui suit, mais **attendez-vous à une erreur**:

```bash
[student<X>@ansible ~]$ ansible node1 -m copy -a 'content="Managed by Ansible\n" dest=/etc/motd'
```

Comme mentionné, cela produit une **erreur**:

```bash
    node1 | FAILED! => {
        "changed": false,
        "checksum": "a314620457effe3a1db7e02eacd2b3fe8a8badca",
        "failed": true,
        "msg": "Destination /etc not writable"
    }
```

La sortie de la commande Ad-hoc vous crie **FAILED** en rouge. Pourquoi? Parce que l'utilisateur **student\<X\>** n'est pas autorisé à écrire le fichier motd.

Maintenant, c'est un cas pour l'escalade de privilèges et la raison pour laquelle `sudo` doit être configuré correctement. Nous devons demander à Ansible d'utiliser `sudo` pour exécuter la commande en tant que root en utilisant le paramètre` -b` (pensez "become").

> **Astuce**
>
> Ansible se connectera aux machines en utilisant votre nom d'utilisateur actuel (student\<X\> dans ce cas), tout comme SSH le ferait. Pour remplacer le nom d'utilisateur distant, vous pouvez utiliser le paramètre `-u`.

Pour nous, il est normal de se connecter en tant que **student<\X\>** car `sudo` est configuré. Modifiez la commande pour utiliser le paramètre `-b` et exécutez à nouveau:

```bash
[student<X>@ansible ~]$ ansible node1 -m copy -a 'content="Managed by Ansible\n" dest=/etc/motd' -b
```

Cette fois, la commande est un succès:

```
node1 | CHANGED => {
    "changed": true,
    "checksum": "4458b979ede3c332f8f2128385df4ba305e58c27",
    "dest": "/etc/motd",
    "gid": 0,
    "group": "root",
    "md5sum": "65a4290ee5559756ad04e558b0e0c4e3",
    "mode": "0644",
    "owner": "root",
    "secontext": "system_u:object_r:etc_t:s0",
    "size": 19,
    "src": "/home/student1/.ansible/tmp/ansible-tmp-1557857641.21-120920996103312/source",
    "state": "file",
    "uid": 0
```

Utilisez Ansible avec le module générique `command` pour vérifier le contenu du fichier motd:

```bash
[student<X>@ansible ~]$ ansible node1 -m command -a 'cat /etc/motd'
node1 | CHANGED | rc=0 >>
Managed by Ansible
```


Exécutez à nouveau la commande `ansible node1 -m copy…`. Notez:

   - La couleur de sortie différente (configuration de terminal appropriée fournie).
   - Le changement de `"changed": true,` à `" changed": false,`.
   - La première ligne indique `SUCCESS` au lieu de `CHANGED`.  

> **Astuce**
>
> Cela permet de repérer plus facilement les changements et ce qu'Ansible a réellement fait.

## Défi: Les modules

   - Utilisation de `ansible-doc`

       - Trouvez un module qui utilise Yum pour gérer les packages logiciels.

       - Recherchez les exemples d'aide du module pour savoir comment installer un package dans la dernière version.

   - Exécutez une commande Ad-hoc Ansible pour installer le package "squid" dans la dernière version sur `node1`.

> **Astuce**
>
> Utilisez la commande copier Ad-hoc ci-dessus comme modèle et modifiez le module et les options.

> **Avertissement**
>
> **Solution ci-dessous \!**

```
[student<X>@ansible ~]$ ansible-doc -l | grep -i yum
[student<X>@ansible ~]$ ansible-doc yum
[student<X>@ansible ~]$ ansible node1 -m yum -a 'name=squid state=latest' -b
```

----
**Navigation**
<br>
[Exercise précédent](../1.1-setup/README.fr.md) - [Exercise suivant](../1.3-playbook/README.fr.md)

[Cliquez ici pour revenir à l'atelier Ansible pour Red Hat Enterprise Linux](../README.fr.md)
