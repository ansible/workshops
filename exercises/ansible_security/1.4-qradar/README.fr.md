# Exercice 1.4 - Exécution du premier playbook IBM QRadar

**Lisez ceci dans d'autres langues**: <br>
[![uk](../../../images/uk.png) English](README.md),  [![japan](../../../images/japan.png) 日本語](README.ja.md), [![france](../../../images/fr.png) Français](README.fr.md).<br>

## Étape 4.1 - IBM QRadar

Pour montrer comment automatiser un SIEM dans un environnement de sécurité, nous allons utiliser [IBM QRadar, community edition](https://developer.ibm.com/qradar/ce/).

Le SIEM est accessible via l'interface utilisateur Web et via l'API REST. Dans cet atelier, les playbooks que nous écrirons interagiront avec l'API. Toutes les actions seront vérifiées dans l'interface utilisateur Web.

## Étape 4.2 - Accéder à l'interface utilisateur Web

Jetez un premier coup d'œil au SIEM et vérifiez qu'il fonctionne réellement. Pointez votre navigateur Web vers `https://<qradar-IP>`, où `<qradar-IP>` est l'adresse IP de l'entrée `qradar` dans votre section `siem` de votre inventaire. Ensuite, vous serez confronté à un avertissement indiquant que le certificat n'est pas sécurisé car il est auto-signé. Veuillez l'accepter et continuer.

> **Remarque**
>
> Dans un environnement productif, l'acceptation d'un certificat non sécurisé ne serait pas une option. Étant donné que la configuration de l'atelier n'est que de courte durée et sert uniquement à une démonstration, nous acceptons le risque.

Dans le champ de connexion, indiquez le nom d'utilisateur **admin** et le mot de passe **Ansible1!**. Puis appuyez sur le bouton **Login**.

Vous êtes maintenant connecté à l'interface Web principale d'IBM QRadar.

![QRadar main window](images/qradar-main-window.png)

Pour avoir une idée de QRadar et des concepts de base, jetons un coup d'œil à l'interface: dans la partie supérieure, il y a une barre de navigation avec plusieurs points d'entrée dans les principales parties de QRadar.

- **Dashboard**, offrant une vue d'ensemble centrale
- **Offenses**, messages ou événements générés par une condition surveillée
- **Log Activity**, montrant les événements collectés à partir des journaux
- **Network Activity**, communication du trafic réseau entre certains hôtes
- **Assets**, profils automatiquement créés des périphériques réseau et des hôtes dans votre environnement
- **Reports**, rapports personnalisés ou standard pour, signaler ce qui se passe dans votre environnement

Aux fins de la démo, nous verrons de plus près les **Offenses**: cliquez sur l'élément de menu. Dans la nouvelle fenêtre, vous verrez une barre de navigation sur le côté gauche pour filtrer les infractions.

![QRadar offense window](images/qradar-offense-window.png)

> **Remarque**
>
> Comme il s'agit d'un environnement de démonstration, il est probable que la liste des infractions soit actuellement vide.

Les infractions sont des messages ou des événements générés en fonction des résultats des messages de journal ou du trafic réseau, comme une ligne de journal malveillante. QRadar déclenche des infractions basées sur des règles: les règles décrivent des conditions et lorsqu'une condition est remplie il crée une infraction.

Pour le dire avec les mots de la documentation officielle:

> *Des règles, parfois appelées règles de corrélation, sont appliquées aux événements, flux ou infractions pour rechercher ou détecter des anomalies. Si toutes les conditions d'un test sont remplies, la règle génère une réponse. [Documentation QRadar](https://www.ibm.com/support/knowledgecenter/en/SS42VS_7.3.2/com.ibm.qradar.doc/c_qradar_rul_mgt.html)*

Dans un environnement productif, il est courant de créer de plus en plus de règles personnalisées au fil du temps. Mais pour l'instant, regardons les règles qui sont déjà installées sur le système: dans la fenêtre **Offenses**, à gauche dans la barre de navigation, cliquez sur **Rules**. Une longue liste de règles s'affiche. Dans la barre de recherche en haut de cette liste, entrez le terme de recherche suivant: `DDoS` Appuyez sur Entrée après pour filtrer la liste.

La liste est filtrée et n'affiche que quelques règles liées à DDOS.

![QRadar, filtered rules list](images/qradar-offenses-rules.png)

Cliquez sur celui appelé  **"Potential DDoS Against Single Host (TCP)"**, notez qu'il est activé. Cela sera pertinent plus tard dans cet exercice.

Maintenant que vous avez eu un premier aperçu de QRadar, il est temps de voir comment il peut être automatisé par Ansible.

## Étape 4.3 - Modules QRadar et collections Ansible

Au niveau le plus élémentaire, l'automatisation Ansible effectue des tâches. Ces tâches exécutent des modules, qui fonctionnent généralement sur les cibles correspondantes, comme un point de terminaison API d'un périphérique ou d'un programme spécial.

Ansible est livré avec de nombreux modules inclus. Mais au moment de l'écriture, Ansible ne livre pas les modules QRadar prêts à l'emploi. Au lieu de cela, ces modules sont fournis en tant que [collections Ansible](https://docs.ansible.com/ansible/devel/dev_guide/collections_tech_preview.html):

> *Les collections sont un format de distribution pour le contenu Ansible. Ils peuvent être utilisés pour empaqueter et distribuer des playbooks, des rôles, des modules et des plugins. Vous pouvez publier et utiliser des collections via Ansible Galaxy.*

Les collections suivent une structure de répertoire simple pour fournir du contenu Ansible. Si cela vous rappele Les rôles Ansible, c'est normal: les collections sont construites sur l'idée des rôles, mais étendent le concept à la gestion générale du contenu Ansible. La collection pour IBM QRadar se trouve dans le [projet de sécurité ansible](https://github.com/ansible-security/ibm_qradar).

Comme les rôles, les collections doivent également être installées avant de pouvoir être utilisées. Ils sont installés sur la machine exécutant Ansible, dans le cas du laboratoire c'est l'hôte de contrôle.

Installons la collection de modules QRadar sur votre hôte de contrôle. Dans votre éditeur en ligne VS Code, ouvrez un nouveau terminal. Exécutez la commande `ansible-galaxy collection --help` pour vérifier que la fonction collections fonctionne correctement:

```bash
[student<X>@ansible ~]$ ansible-galaxy collection --help
usage: ansible-galaxy collection [-h] COLLECTION_ACTION ...

positional arguments:
  COLLECTION_ACTION
    init             Initialize new collection with the base structure of a
                     collection.
    build            Build an Ansible collection artifact that can be publish
                     to Ansible Galaxy.
    publish          Publish a collection artifact to Ansible Galaxy.
    install          Install collection(s) from file(s), URL(s) or Ansible
                     Galaxy

optional arguments:
  -h, --help         show this help message and exit
```

Nous pouvons maintenant installer la collection `ibm.qradar`:

```bash
[student<X>@ansible ~]$ ansible-galaxy collection install ibm.qradar
Process install dependency map
Starting collection install process
Installing 'ibm.qradar:0.0.1' to '/home/student<X>/.ansible/collections/ansible_collections/ibm/qradar'
```

Vérifiez que la collection a été installée correctement:

```bash
[student<X>@ansible ~]$ ls -1 ~/.ansible/collections/ansible_collections/ibm/qradar
docs
LICENSE
plugins
README.md
tests
```

Tous les fichiers requis sont là - en particulier le répertoire `plugins/modules` qui contient les modules réels.

Avec la collection en place, nous pouvons maintenant commencer à écrire notre playbook.

> **Remarque**
>
> Si vous voulez l'essayer chez vous: veuillez noter que cette ccollection nécessite au moins la version 2.9 d'Ansible!

## Étape 4.4 - Premier exemple de playbook

Dans notre premier exemple d'utilisation de QRadar, nous allons activer / désactiver une règle. C'est un changement assez petit mais commun et montre comment Ansible et QRadar interagissent. Nous allons le faire en deux étapes: d'abord nous trouvons la règle que nous voulons changer, ensuite nous appliquons le changement.

Dans votre éditeur en ligne VS Code, créez un nouveau fichier, `find_qradar_rule.yml` dans le répertoire personnel de votre utilisateur. Ajoutez le nom et les hôtes cibles, ici `qradar`.

```yaml
---
- name: Find QRadar rule state
  hosts: qradar
```

Nous allons utiliser la collection que nous venons d'ajouter. Une collection peut être référencée à plusieurs endroits, par exemple au niveau de la tâche ou au niveau du jeu. Nous la référencerons au niveau du jeu pour pouvoir écrire plusieurs tâches qui l'appelera.

```yaml
---
- name: Find QRadar rule state
  hosts: qradar
  collections:
    - ibm.qradar
```

Ensuite, nous apportons les tâches réelles. L'API REST de QRadar est conçue de telle sorte que nous devons d'abord rechercher une règle appropriée pour trouver son ID, puis désactiver la règle en référençant l'ID donné. Dans la dernière section, nous avons déjà examiné les règles QRadar via **Offenses** > **Rules**, et les avons filtrées pour le terme **DDoS**. Dans la liste filtrée, notez la première règle qui y est affichée, **"Potential DDoS Against Single Host (TCP)"**. Nous utiliserons cette chaîne pour rechercher le rôle en utilisant le module `qradar_rule_info`:

```yaml
---
- name: Find QRadar rule state
  hosts: qradar
  collections:
    - ibm.qradar

  tasks:
    - name: get info about qradar rule
      qradar_rule_info:
        name: "DDoS Attack Detected"
```

Ce module renvoie de nombreuses informations, parmi lesquelles l'ID dont nous avons besoin pour désactiver le rôle. Enregistrons les informations retournées dans une variable à l'aide du mot-clé `register`. Il est directement utilisé avec le module lui-même. Cela nous permet d'utiliser le contenu de la variable dans la tâche suivante.

```yaml
---
- name: Find QRadar rule state
  hosts: qradar
  collections:
    - ibm.qradar

  tasks:
    - name: get info about qradar rule
      qradar_rule_info:
        name: "DDoS Attack Detected"
      register: rule_info
```

À quoi ressemblent donc les informations renvoyées par le module? Et si nous affichions juste la variable `rule_info`? Pour cela, ajoutez une tâche de `debug` qui peut être utilisée pour afficher des variables pendant une exécution de playbook:

```yaml
---
- name: Find QRadar rule state
  hosts: qradar
  collections:
    - ibm.qradar

  tasks:
    - name: get info about qradar rule
      qradar_rule_info:
        name: "Potential DDoS Against Single Host (TCP)"
      register: rule_info

    - name: output returned rule_info
      debug:
        var: rule_info
```

> **Remarque**
>
> Le paramètre "var" du module de débogage attend déjà un nom de variable - pour cette raison, les accolades et les guillemets ne sont pas nécessaires comme d'habitude lorsque vous référencez une variable.

Les deux tâches collectent et produisent uniquement des données, elles ne changent rien. Exécutons rapidement le playbook pour regarder les données retournées:


```bash
[student<X>@ansible ansible-files]$ ansible-playbook find_qradar_rule.yml

PLAY [Find QRadar rule state] ***************************************************

TASK [Gathering Facts] ************************************************************
ok: [qradar]

TASK [get info about qradar rule] *************************************************
ok: [qradar]

TASK [output returned rule_info] **************************************************
ok: [qradar] => {
    "rule_info": {
        "changed": false,
        "failed": false,
        "rules": [
            {
                "average_capacity": 0,
                "base_capacity": 0,
                "base_host_id": 0,
                "capacity_timestamp": 0,
                "creation_date": 1278524200032,
                "enabled": true,
                "id": 100065,
                "identifier": "SYSTEM-1520",
                "linked_rule_identifier": null,
                "modification_date": 1566928030130,
                "name": "Potential DDoS Against Single Host (TCP)",
                "origin": "SYSTEM",
                "owner": "admin",
                "type": "FLOW"
            }
        ]
    }
}

PLAY RECAP ************************************************************************
qradar  : ok=3  changed=0  unreachable=0  failed=0  skipped=0  rescued=0  ignored=0
```

Comme vous le voyez, la tâche de débogage  `output returned rule_info`` montre le contenu de la variable, et donc le contenu qui a été retourné par le module `qradar_rule_info`. Notez parmi ces données de retour la clé `id`, dans cet exemple avec la valeur `100065`. C'est la clé dont nous avons besoin.

> **Remarque**
>
> L'identifiant de la clé peut être différent dans votre cas.

Comment obtient-on la clé lorsqu'elle se trouve dans cette structure? Tout d'abord, c'est dans le segment `rules` de la variable, auquel nous pouvons accéder via `rule_info.rules`. A l'intérieur de `rules`, il y a en fait une liste (notez les accolades), mais avec une seule entrée - nous y accédons donc avec `rule_info.rules[0]`. Et à partir de l'entrée de la liste, nous pouvons accéder à chaque clé individuellement via son nom: `rule_info.rules[0]['id']`.

Écrivons donc un nouveau playbook où nous fournissons ceci comme valeur au module qui peut désactiver la règle, `qradar_rule`.

Dans votre éditeur en ligne VS Code, créez un nouveau fichier, `change_qradar_rule.yml` dans le répertoire personnel `/home/student<X>/`. Ajoutez le nom et les hôtes cibles, ici `qradar`.

<!-- {% raw %} -->
```yaml
---
- name: Change QRadar rule state
  hosts: qradar
  collections:
    - ibm.qradar

  tasks:
    - name: get info about qradar rule
      qradar_rule_info:
        name: "Potential DDoS Against Single Host (TCP)"
      register: rule_info

    - name: disable rule by id
      qradar_rule:
        state: disabled
        id: "{{ rule_info.rules[0]['id'] }}"
```
<!-- {% endraw %} -->

Le playbook est maintenant terminé: il interroge QRadar pour récupérer la liste des règles, et désactive celle que nous recherchons.

## Étape 4.5 - Exécutez le playbook

Après avoir terminé le playbook, exécutons-le:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook change_qradar_rule.yml

PLAY [Change QRadar rule state] ***************************************************

TASK [Gathering Facts] ************************************************************
ok: [qradar]

TASK [get info about qradar rule] *************************************************
ok: [qradar]

TASK [disable rule by id] *********************************************************
changed: [qradar]

PLAY RECAP ************************************************************************
qradar  : ok=3  changed=1  unreachable=0  failed=0  skipped=0  rescued=0  ignored=0
```

Comme vous pouvez le voir, le playbook dénote un changement: la règle a été modifiée. Exécutez à nouveau le playbook - il ne signale plus de changement, car la règle est maintenant déjà désactivée.

## Étape 4.6 - Modifications correctes de l'interface utilisateur

Pour vérifier qu'Ansible a effectivement changé quelque chose, nous revenons à l'interface utilisateur de QRadar. Connectez vous à l'IP de QRadar via votre navigateur Web. Cliquez sur l'onglet **Offenses**, puis à gauche sur **Rules**. La longue liste de règles s'affiche. Dans la barre de recherche en haut de cette liste, entrez le terme de recherche suivant: `DDoS`
Appuyez sur Entrée après pour filtrer la liste, de sorte qu'elle n'affiche que les règles liées au mot clé `DDOS`. Enfin, notez la règle concernant les attaques DDOS et vérifiez l'état dans la colonne **Enabled**: il doit être réglé à **False**!

![QRadar, filtered rules list showing disabled rule](images/qradar-rules-disabled.png)

Vous avez terminé les premières étapes de l'automatisation de QRadar avec Ansible. Revenez à l'aperçu de l'exercice et passez à l'exercice suivant.

----

[Cliquez ici pour revenir à l'atelier Ansible pour la sécurité](../README.fr.md)
