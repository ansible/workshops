# Exercice 1.2 - Exécution du premier playbook Check Point

**Lisez ceci dans d'autres langues**: <br>
[![uk](../../../images/uk.png) English](README.md),  [![japan](../../../images/japan.png) 日本語](README.ja.md), [![france](../../../images/fr.png) Français](README.fr.md).<br>

## Étape 2.1 - Pare-feu Check Point

Pour montrer comment automatiser un pare-feu dans un environnement de sécurité, ce laboratoire contient le pare-feu Check Point (NGFW).

Le NGFW n'est généralement pas géré directement, mais via un serveur central de gestion de sécurité (MGMT). Le MGMT est un outil central pour gérer plusieurs NGFW ou autres outils de sécurité en un seul endroit.

Il existe plusieurs façons d'interagir avec le MGMT. Dans notre laboratoire, deux façons sont importantes:

- API: Ansible fonctionne principalement avec l'API
- Client Windows: l'interaction utilisateur a lieu dans un client Windows.

Dans ce laboratoire, les playbooks que nous écrivons interagiront avec l'API. Toutes les actions seront vérifiées dans l'interface utilisateur du client Windows.

## Étape 2.2 - Accès au serveur Check Point MGMT via un poste de travail Windows

Étant donné que l'accès au serveur MGMT nécessite un client Windows et que nous ne pouvons pas être sûrs que chaque étudiant a accès à un environnement Windows, nous avons provisionné un poste de travail Windows dans le cadre de cet atelier.

Le poste de travail Windows est accessible via le protocole RDP (Remote Desktop Protocol). Nous vous recommandons d'utiliser un client RDP natif si possible. Sinon, le poste de travail est équipé d'un client HTML RDP qui permet aux participants du laboratoire d'accéder au poste de travail via un navigateur.

Testez l'accès au serveur MGMT maintenant en pointant votre client RDP vers l'IP `windows-ws` dans votre inventaire.

Si vous n'avez pas de client RDP disponible ou souhaitez tester le client HTML RDP, veuillez ouvrir l'URL suivante dans votre navigateur: `http://<windows-wsIP>/myrtille`. Assurez-vous de remplacer «<windows-wsIP>» par l'IP du poste de travail Windows de votre inventaire. Dans le champ de connexion, ne fournissez que le nom d'utilisateur et le mot de passe: Le nom d'utilisateur est **Administrator**, le mot de passe est **Ansible+Red*Hat19!20** sauf indication contraire. Laissez les autres champs vides et cliquez sur **Connect**.

Vous accédez maintenant à un poste de travail Windows par défaut avec un navigateur Google Chrome installé.

> **Remarque**
>
> Juste après la connexion, une large barre bleue peut apparaître sur le côté droit de l'écran, à propos des configurations réseau. Vous pouvez ignorer cela en toute sécurité, la question se cache si vous cliquez n'importe où sur l'écran.

## Étape 2.3 - Accéder à l'interface utilisateur de SmartConsole

Lancez Check Point SmartConsole via l'icône du bureau. Dans la fenêtre suivante, comme nom d'utilisateur, utilisez `admin` et comme mot de passe `admin123`. L'adresse IP à saisir est celle de l'entrée **checkpoint** de votre inventaire.

![SmartConsole login window](images/smartconsole-login-window.png)

Appuyez sur le bouton **Login**. Ensuite, vous devez vérifier l'empreinte numerique du serveur en cliquant sur le bouton **PROCEED**.

> **Remarque**
>
> Dans un environnement de production, vous devez être certain que l'empreinte numérique affichée est identique à celle du serveur. Dans notre configuration de démonstration avec les instances de courte durée, nous pouvons supposer que les empreintes numeriques sont bonnes.

Vous affichez maintenant l'interface de gestion Check Point SmartConsole. Un avertissement Internet Explorer peut être visible au démarrage. Cela peut être fermé en toute sécurité et est dû à des limitations dans la façon dont IE fonctionne.

![SmartConsole main window](images/smartconsole-main-window.png)

Ensuite, sur le côté gauche, cliquez sur **SECURITY POLICIES** et notez qu'il n'y a actuellement qu'une seule règle installée: pour supprimer tout le trafic. Vous avez maintenant une première idée de l'apparence de Check Point en termes d'interface de gestion. Nous interagirons plus avec elle - mais nous revenons d'abord à la ligne de commande pour apprendre à écrire des playbooks Ansible en interagissant avec Check Point.

## Étape 2.4 - Premier exemple de playbook

Dans Ansible, l'automatisation est décrite dans les playbooks. Les playbooks sont des fichiers qui décrivent les configurations ou étapes souhaitées à implémenter sur les hôtes gérés. Les playbooks peuvent transformer des tâches administratives longues et complexes en routines facilement reproductibles avec des résultats prévisibles et réussis.

Un playbook est un ensemble répétable de *Plays* et *tâches*.

Un playbook peut avoir plusieurs play et un play peut avoir une ou plusieurs tâches. Une tâche est composée d'un ou plusieurs *modules*, les modules sont les composants qui effectuent une action.

Le but d'un *play* est de cartographier un groupe d'hôtes. Le but d'une *tâche* est d'implémenter des modules sur ces hôtes.

Si vous n'êtes pas très familier avec Ansible, consultez l'exemple suivant d'un playbook:

```yaml
---
- name: install and start apache
  hosts: web
  become: yes
  vars:
    http_port: 80

  tasks:
    - name: httpd package is present
      yum:
        name: httpd
        state: latest

    - name: latest index.html file is present
      template:
        src: files/index.html
        dest: /var/www/html/

    - name: httpd is started
      service:
        name: httpd
        state: started
```

> **Astuce**
>
> Voici une belle analogie: lorsque les modules Ansible sont les outils de votre atelier, l'inventaire est le matériel et les playbooks sont les instructions.

Nous allons maintenant écrire un playbook pour changer la configuration de la configuration de Check Point. Nous commencerons par un exemple simple où nous ajouterons une entrée whiltelist dans la configuration du pare-feu pour autoriser le trafic d'une certaine machine à une autre. Dans notre exemple, nous autoriserons la machine appelée **attaquant** à envoyer du trafic vers notre machine **snort**.

Le playbook sera écrit et exécuté sur l'hôte de contrôle Ansible. La langue dans laquelle le playbook est écrit est [YAML] (https://en.wikipedia.org/wiki/YAML). Dans votre navigateur, accédez à l'éditeur en ligne VS Code. Dans la barre de menu, cliquez sur **Fichier** -> **Nouveau fichier**. Un nouveau fichier vide s'ouvre. Avant de continuer, enregistrons-le. Encore une fois dans la barre de menu, cliquez sur **Fichier** -> **Enregistrer sous ...**. Le menu déroulant s'ouvre, suggérant le nom de fichier **Untitled-1** dans le répertoire **lab_inventory**. Remplacez-le par «whitelist_attacker.yml» et supprimez le répertoire **lab_inventory** pour que le nom de fichier complet soit: «/home/student<X>/whitelist_attacker.yml» où «<X>» est l'ID étudiant qui vous est attribué .

> **Remarque**
>
> Assurez-vous que le fichier et toutes les opérations futures sont toujours effectués dans le répertoire personnel, **/home/student<X>**. Ceci est crucial pour la bonne exécution des exercices.

Une fois que nous avons enregistré le fichier au bon endroit, nous pouvons ajouter notre code playbook. Tout d'abord, un playbook a besoin d'un nom et les hôtes sur lesquels il doit être exécuté. Ajoutons donc ceux-ci:

```yaml
---
- name: Whitelist Attacker
  hosts: checkpoint
```

Au cas où vous vous poseriez la question: les trois tirets en haut, `---`, indiquent le début d'un fichier YAML.

> **Remarque**
>
> Il est recommandé de rendre les playbooks plus réutilisables en les pointant vers `hosts: all` et de limiter l'exécution plus tard sur la ligne de commande ou via Tower. Mais pour l'instant, nous simplifions le processus en nommant directement les hôtes dans le playbook.

Comme mentionné, dans cet exemple simple, nous ajouterons une entrée dans la liste d'autorisation. Une entrée se compose d'une adresse IP source, d'une adresse IP de destination et de la règle permettant l'accès entre celles-ci.

Pour cela, nous ajoutons les IP source et de destination en tant que variables au playbook. Étant donné qu'Ansible connaît toutes les machines de l'inventaire et que les adresses IP sont répertoriées dans l'inventaire, nous pouvons simplement référencer ces informations comme
[variables](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html) des hôtes correspondants:

<!-- {% raw %} -->
```yaml
---
- name: Whitelist Attacker
  hosts: checkpoint

  vars:
    source_ip: "{{ hostvars['attacker']['private_ip2'] }}"
    destination_ip: "{{ hostvars['snort']['private_ip2'] }}"
```
<!-- {% endraw %} -->

Comme vous le voyez, les variables sont marquées par des accolades. Notez que nous utilisons la deuxième IP privée - celles-ci appartiennent à un réseau qui est spécifiquement routé via le FW pour le trafic d'application. La première IP privée appartient au réseau de gestion. Les variables sont utilisées pour définir une autre variable (plus courte), qui sera utilisée tout au long du playbook. Il s'agit d'un moyen courant de dissocier les données de l'exécution.

> **Remarque**
>
> Assurez-vous que les espaces et l'indentation sont exactement comme indiqué: YAML est très pointilleux à ce sujet, et de nombreuses erreurs dans l'exécution des playbooks sont dues à une indentation incorrecte.

Ensuite, nous devons ajouter les tâches. La section des tâches est l'endroit où les modifications réelles sur les machines cibles sont effectuées. Dans ce cas, cela se produit en trois étapes:

- nous créons d'abord un objet source
- puis un objet de destination
- enfin la règle d'accès entre ces deux objets

Commençons par une tâche pour définir l'objet source:

<!-- {% raw %} -->
```yaml
---
- name: Whitelist attacker
  hosts: checkpoint

  vars:
    source_ip: "{{ hostvars['attacker']['private_ip2'] }}"
    destination_ip: "{{ hostvars['snort']['private_ip2'] }}"

  tasks:
    - name: Create source IP host object
      checkpoint_host:
        name: "asa-{{ source_ip }}"
        ip_address: "{{ source_ip }}"
```
<!-- {% endraw %} -->

Comme vous pouvez le voir, la tâche elle-même a un nom - tout comme le play - et fait référence à un module, ici `checkpoint_hosts`. Le module est la partie d'Ansible qui "fait" - le module dans ce cas crée ou modifie des entrées d'objet dans Check Point. Le module a des paramètres, ici `name` et `ip_address`. Chaque module a des paramètres individuels, souvent certains d'entre eux sont requis tandis que d'autres sont facultatifs. Pour obtenir plus d'informations sur un module, vous pouvez ouvrir un terminal dans votre éditeur en ligne VS Code et appeler l'aide. Par exemple, dans la barre de menus, cliquez sur **Terminal** > **Nouveau terminal** et exécutez la commande suivante. Il affichera l'aide pour le module `checkpoint_host`:

```bash
[student<X>@ansible ~]$ ansible-doc checkpoint_host
```

> **Astuce**
>
> Dans `ansible-doc`, vous pouvez utiliser les flèches `haut` / `bas` pour faire défiler le contenu et `q` pour quitter.

De la même manière que nous avons défini l'IP source, nous allons maintenant ajouter l'IP de destination:

<!-- {% raw %} -->
```yaml
---
- name: Whitelist attacker
  hosts: checkpoint

  vars:
    source_ip: "{{ hostvars['attacker']['private_ip2'] }}"
    destination_ip: "{{ hostvars['snort']['private_ip2'] }}"

  tasks:
    - name: Create source IP host object
      checkpoint_host:
        name: "asa-{{ source_ip }}"
        ip_address: "{{ source_ip }}"

    - name: Create destination IP host object
      checkpoint_host:
        name: "asa-{{ destination_ip }}"
        ip_address: "{{ destination_ip }}"
```
<!-- {% endraw %} -->

Enfin, nous définissons la règle d'accès entre ces deux serveurs. Les règles doivent encore être appliquées, et cela peut se faire de deux manières: soit par les tâches definis précédemment, via le paramètre du module `auto_install_policy: yes`, soit en tant que tâche finale dédiée avec le module `cp_mgmt_install_policy`. Les deux sont présentés dans ce manuel pour souligner la flexibilité que nous avons avec l'approche modulaire. Dans le cas où cependant le module a déjà commencé un processus d'application, le dernier module de politique d'installation peut échouer, nous ajoutons donc un indicateur spécial pour ignorer les erreurs possibles, `failed_when: false`:

<!-- {% raw %} -->
```yaml
---
- name: Whitelist attacker
  hosts: checkpoint

  vars:
    source_ip: "{{ hostvars['attacker']['private_ip2'] }}"
    destination_ip: "{{ hostvars['snort']['private_ip2'] }}"

  tasks:
    - name: Create source IP host object
      checkpoint_host:
        name: "asa-{{ source_ip }}"
        ip_address: "{{ source_ip }}"

    - name: Create destination IP host object
      checkpoint_host:
        name: "asa-{{ destination_ip }}"
        ip_address: "{{ destination_ip }}"

    - name: Create access rule to allow access from source to destination
      checkpoint_access_rule:
        auto_install_policy: yes
        auto_publish_session: yes
        layer: Network
        position: top
        name: "asa-accept-{{ source_ip }}-to-{{ destination_ip }}"
        source: "asa-{{ source_ip }}"
        destination: "asa-{{ destination_ip }}"
        action: accept

    - name: Install policy
      cp_mgmt_install_policy:
        policy_package: standard
        install_on_all_cluster_members_or_fail: yes
      failed_when: false
```
<!-- {% endraw %} -->

## Étape 2.5 - Exécutez le playbook

Les playbooks sont exécutés à l'aide de la commande `ansible-playbook` sur le nœud de contrôle. Avant d'exécuter un nouveau playbook, il est judicieux de vérifier les erreurs de syntaxe. Dans votre éditeur en ligne VS Code, dans la barre de menu, cliquez sur **Terminal** -> **Nouveau terminal**. Dans le terminal, exécutez la commande suivante:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook --syntax-check whitelist_attacker.yml
```

La vérification de la syntaxe ne doit signaler aucune erreur. S'il signale une erreur, vérifiez la sortie et essayez de résoudre le problème dans le code du playbook.

Vous devriez maintenant être prêt à exécuter votre playbook:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook whitelist_attacker.yml

PLAY [Whitelist attacker] *********************************************************

TASK [Gathering Facts] ************************************************************
ok: [checkpoint]

TASK [Create source IP host object] ***********************************************************************************
changed: [checkpoint]

TASK [Create destination IP host object] ***********************************************************************************
changed: [checkpoint]

TASK [Create access rule to allow access from source to destination] ***********************************************************************************
changed: [checkpoint]

PLAY RECAP ************************************************************************
checkpoint  : ok=4 changed=3 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0
```

## Étape 2.6 - Vérifier les modifications de l'interface utilisateur

Il est maintenant temps de vérifier si les changements ont réellement eu lieu et la configuration du serveur Check Point MGMT a été modifiée.

Accédez au poste de travail Windows et ouvrez l'interface SmartConsole. Sur le côté droit, sous **Object Categories**, cliquez sur **Network Objects**, puis choisissez **Hosts**. Il doit répertorier les deux nouvelles entrées d'hôte.

![SmartConsole Hosts list](images/smartconsole-hosts-list.png)

Ensuite, sur le côté gauche, cliquez sur **SECURITY POLICIES**. Remarquez l'entrée de politique de contrôle d'accès supplémentaire, comparez la configuration avec lorsque nous l'avons examiné plus tôt. Puisque le trafic est autorisé maintenant, l'entrée dans la colonne **Action** est modifiée et a une couleur différente.

![SmartConsole Policy Entries](images/smartconsole-policy-entry.png)

Notez également dans le coin inférieur gauche qu'il y a une barre verte indiquant que les modifications ont été appliquées à l'ensemble du système.

## Étape 2.7 - Activez la journalisation pour la nouvelle stratégie

Pour voir comment les modifications sont normalement effectuées dans une interaction manuelle typique avec Check Point, faisons une petite modification qui sera utile plus tard. Par défaut, Check Point n'active pas la journalisation pour les nouvelles règles. Activons la journalisation pour notre nouvelle politique. Sur le côté gauche de la fenêtre principale, cliquez sur **SECURITY POLICIES**. Les deux règles sont répertoriées. Dans la colonne **Track**, passez la souris sur l'entrée **None** de notre règle nouvellement créée. Faites un clic droit dessus et dans la case qui apparaît, choisissez **Log**.

![SmartConsole, change logging](images/smartconsole-change-logging.png)

Ensuite, cliquez sur le bouton **Install Policy** en haut de la liste des politiques, confirmez la boîte de dialogue qui s'ouvre avec **Publish & Install** et dans la dernière boîte de dialogue, cliquez sur **Install**.

Par conséquent, dans le coin gauche, une petite fenêtre apparaît pour vous informer de la progression du déploiement de la modification.

Comme vous pouvez le voir, même un petit changement dans la configuration nécessite plusieurs clics de la part de l'utilisateur - plus ces étapes peuvent être automatisées, mieux c'est.

----

[Cliquez ici pour revenir à l'atelier Ansible pour la sécurité](../README.fr.md)
