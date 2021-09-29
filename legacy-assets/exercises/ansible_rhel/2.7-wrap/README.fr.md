# Atelier - Conclusion

**Lisez ceci dans d'autres langues**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

## Table des matières

* [Objectif](#objectif)
* [Guide](#guide)
  * [Préparons le terrain](#Préparons-le-terrain)
  * [Le référentiel Git](#Le-référentiel-Git)
  * [Préparer l'inventaire](#Préparer-l-inventaire)
  * [Créer le modèle](#Créer-le-modèle)
  * [Vérifiez les résultats](#Vérifiez-les-résultats)
  * [Ajouter un questionnaire](#Ajouter-un-questionnaire)
  * [Solution](#solution)
* [La fin](#la-fin)

# Objectif

C'est le dernier défi où nous essayons de rassembler la plupart de ce que vous avez appris.

# Guide

## Préparons le terrain

Votre équipe d'exploitation et votre équipe de développement d'applications aiment ce qu'ils voient dans Ansible Tower. Pour vraiment l'utiliser dans leur environnement, ils ont mis en place ces exigences:

- Tous les serveurs Web (`node1`, `node2` et `node3`) doivent aller dans un seul groupe

- Étant donné que les serveurs Web peuvent être utilisés à des fins de développement ou de production, il doit y avoir un moyen de les signaler en conséquence comme "stage dev" ou "stage prod".

    - Actuellement, `node1` et` node3` sont utilisés comme système de développement et `node2` est en cours de production.

- Bien sûr, le contenu de l'application de renommée mondiale "index.html" sera différent entre les étapes de développement et de production.

    - Il devrait y avoir un titre sur la page indiquant l'environnement

    - Il devrait y avoir un champ de contenu

- Le rédacteur de contenu `wweb` devrait avoir accès à une enquête pour modifier le contenu des serveurs de développement et de production.

## Le référentiel Git

Tout le code est déjà en place - c'est un Atelier pour Tower apres tout. Consultez le **Workshop Project** à **https: //github.com/ansible/workshop-examples**. Vous y trouverez le playbook `webcontent.yml`, qui appelle le rôle` role_webcontent`.

Par rapport au précédent rôle d'installation d'Apache, il y a une différence majeure: il existe maintenant deux versions d'un modèle `index.html` et une tâche de déploiement du fichier modèle qui a une variable dans le nom du fichier source:

`dev_index.html.j2`

<!-- {% raw %} -->
```html
<body>
<h1>This is a development webserver, have fun!</h1>
{{ dev_content }}
</body>
```
<!-- {% endraw %} -->

`prod_index.html.j2`

<!-- {% raw %} -->
```html
<body>
<h1>This is a production webserver, take care!</h1>
{{ prod_content }}
</body>
```
<!-- {% endraw %} -->

`main.yml`

<!-- {% raw %} -->
```yaml
[...]
- name: Deploy index.html from template
  template:
    src: "{{ stage }}_index.html.j2"
    dest: /var/www/html/index.html
  notify: apache-restart
```
<!-- {% endraw %} -->

## Préparer l'inventaire

Il y a bien sûr plus d'une façon d'y parvenir, mais voici ce que vous devez faire:

- Assurez-vous que tous les hôtes sont dans le groupe d'inventaire `Webserver`.

- Définissez une variable `stage` avec la valeur `dev` pour l'inventaire `Webserver`:

    - Ajoutez `stage: dev` à l'inventaire `Webserver` en le plaçant dans le champ **VARIABLES** sous les trois tirets start-yaml.

- De la même manière, ajoutez une variable `stage: prod` mais cette fois uniquement pour `node2` (en cliquant sur le nom d'hôte) afin qu'elle écrase la variable d'inventaire.

> **Astuce**
>
> Assurez-vous de garder les trois tirets qui marquent le début de YAML et la ligne `ansible_host` en place \!

## Créer le modèle

- Créez un nouveau **modèle de tâche** nommé "Créer un contenu Web" qui

    - cible l'inventaire `Webserver`

    - utilise le Playbook `rhel/apache/webcontent.yml` du projet **Workshop Project**

    - Définit deux variables: `dev_content: contenu dev par défaut` et `prod_content: contenu prod par défaut` dans le **CHAMP EXTRA VARIABLES**

    - Utilise les "Workshop Credential" et avec une élévation de privilèges

- Enregistrez et exécutez le modèle

## Vérifiez les résultats

Cette fois, nous utilisons la puissance d'Ansible pour vérifier les résultats: exécutez curl pour obtenir le contenu Web de chaque nœud, orchestré par une commande Ad-hoc sur la ligne de commande de votre hôte de contrôle Tower:

> **Astuce**
>
> Nous utilisons la variable `ansible_host` dans l'URL pour accéder à tous les nœuds du groupe d'inventaire.

<!-- {% raw %} -->
```bash
[student<X>@ansible ~]$ ansible web -m command -a "curl -s http://{{ ansible_host }}"
 [WARNING]: Consider using the get_url or uri module rather than running 'curl'.  If you need to use command because get_url or uri is insufficient you can add 'warn: false' to this command task or set 'command_warnings=False' in ansible.cfg to get rid of this message.

node2 | CHANGED | rc=0 >>
<body>
<h1>This is a production webserver, take care!</h1>
prod wweb
</body>

node1 | CHANGED | rc=0 >>
<body>
<h1>This is a development webserver, have fun!</h1>
dev wweb
</body>

node3 | CHANGED | rc=0 >>
<body>
<h1>This is a development webserver, have fun!</h1>
dev wweb
</body>
```
<!-- {% endraw %} -->

Notez l'avertissement de la première ligne de ne pas utiliser `curl` via le module `command` car il existe de meilleurs modules directement dans Ansible. Nous y reviendrons dans la prochaine partie.

## Ajouter un questionnaire

- Ajouter un questionnaire au modèle pour permettre de changer les variables `dev_content` et `prod_content`

- Ajoutez des autorisations au contenu Web de l'équipe afin que le modèle **Créer du contenu Web** puisse être exécuté par `wweb`.

- Exécutez le questionnaire en tant qu'utilisateur `wweb`

Vérifiez à nouveau les résultats. La dernière fois nous avons reçu un avertissement en utilisant `curl` via le module `command`, cette fois nous ferons mieux les chose et utiliserons le module `uri` dédié. Comme arguments, il a besoin de l'URL et d'un indicateur pour afficher le corps dans les résultats.

<!-- {% raw %} -->
```bash
[student<X>ansible ~]$ ansible web -m uri -a "url=http://{{ ansible_host }}/ return_content=yes"
node3 | SUCCESS => {
    "accept_ranges": "bytes",
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "connection": "close",
    "content": "<body>\n<h1>This is a development webserver, have fun!</h1>\nwerners dev content\n</body>\n",                                                                                         
    "content_length": "87",
    "content_type": "text/html; charset=UTF-8",
    "cookies": {},
    "cookies_string": "",
    "date": "Tue, 29 Oct 2019 11:14:24 GMT",
    "elapsed": 0,
    "etag": "\"57-5960ab74fc401\"",
    "last_modified": "Tue, 29 Oct 2019 11:14:12 GMT",
    "msg": "OK (87 bytes)",
    "redirected": false,
    "server": "Apache/2.4.6 (Red Hat Enterprise Linux)",
    "status": 200,
    "url": "http://18.205.236.208"
}
[...]
```
<!-- {% endraw %} -->

## Solution

> **Avertissement**
>
> **Solution pas en dessous**

Vous avez déjà effectué toutes les étapes de configuration requises dans le laboratoire. En cas de doute, reportez-vous simplement aux chapitres respectifs.

# La fin

Félicitations, vous avez terminé tous vos ateliers \! Nous espérons que vous avez apprécié votre première rencontre avec Ansible Tower autant que nous avons nous même apprécié la création des ateliers.

----
**Navigation**
<br>
[Exercise précédent](../2.6-workflows/README.fr.md)

[Cliquez ici pour revenir à l'atelier Ansible pour Red Hat Enterprise Linux](../README.fr.md)
