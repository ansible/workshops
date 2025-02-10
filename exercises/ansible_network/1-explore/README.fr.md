# Exercice 1 - Exploration de l'environnement de laboratoire

**Lisez ceci dans d'autres langues** : ![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English](README.md), ![japan](https://github.com/ansible/workshops/raw/devel/images/japan.png) [日本語](README.ja.md), ![Español](https://github.com/ansible/workshops/raw/devel/images/es.png) [Español](README.es.md), ![Français](https://github.com/ansible/workshops/raw/devel/images/fr.png) [Français](README.fr.md).

## Table des matières

- [Exercice 1 - Exploration de l'environnement de laboratoire](#exercice-1---exploration-de-lenvironnement-de-laboratoire)
  - [Table des matières](#table-des-matières)
  - [Objectif](#objectif)
  - [Diagramme](#diagramme)
  - [Guide](#guide)
    - [Étape 1 - Connexion via VS Code](#étape-1---connexion-via-vs-code)
    - [Étape 2 - Utilisation du terminal](#étape-2---utilisation-du-terminal)
    - [Étape 3 - Examen des environnements d'exécution](#étape-3---examen-des-environnements-dexécution)
    - [Étape 4 - Examen de la configuration d'ansible-navigator](#étape-4---examen-de-la-configuration-dansible-navigator)
    - [Étape 5 - Examen de l'inventaire](#étape-5---examen-de-linventaire)
    - [Étape 6 - Compréhension de l'inventaire](#étape-6---compréhension-de-linventaire)
    - [Étape 7 - Utilisation d'ansible-navigator pour explorer l'inventaire](#étape-7---utilisation-dansible-navigator-pour-explorer-linventaire)
    - [Étape 8 - Connexion aux périphériques réseau](#étape-8---connexion-aux-périphériques-réseau)
  - [Conclusion](#conclusion)

## Objectif

Explorer et comprendre l'environnement de laboratoire.

Les premiers exercices de ce laboratoire permettront d'explorer les utilitaires en ligne de commande de la plateforme d'automatisation Ansible. Cela inclut :

- [ansible-navigator](https://github.com/ansible/ansible-navigator) - un utilitaire en ligne de commande et une interface utilisateur textuelle (TUI) pour exécuter et développer du contenu d'automatisation Ansible.
- [ansible-core](https://docs.ansible.com/core.html) - l'exécutable de base qui fournit le cadre, le langage et les fonctions soutenant la plateforme d'automatisation Ansible. Il inclut également divers outils CLI tels que `ansible`, `ansible-playbook` et `ansible-doc`. Ansible Core fait le lien entre la communauté open source et l'offre d'automatisation d'entreprise de Red Hat.
- [Environnements d'exécution](https://docs.ansible.com/automation-controller/latest/html/userguide/execution_environments.html) - non spécifiquement couverts dans cet atelier car les environnements intégrés incluent déjà toutes les collections prises en charge par Red Hat utilisées ici. Les environnements d'exécution sont des images de conteneurs utilisées pour exécuter Ansible.
- [ansible-builder](https://github.com/ansible/ansible-builder) - également non couvert ici, c'est un utilitaire CLI pour automatiser la création d'environnements d'exécution.

Pour plus d'informations sur les nouveaux composants de la plateforme d'automatisation Ansible, vous pouvez consulter cette page [https://red.ht/AAP-20](https://red.ht/AAP-20).

> Rejoignez notre forum communautaire !
>
> Avant de commencer, rejoignez-nous sur <a target="_new" href="https://forum.ansible.com/">https://forum.ansible.com/</a>. Cela vous permettra d'obtenir de l'aide après les ateliers.

## Diagramme

![Red Hat Ansible Automation](https://github.com/ansible/workshops/raw/devel/images/ansible_network_diagram.png)

## Guide

### Étape 1 - Connexion via VS Code

<table>
<thead>
  <tr>
    <th>Il est fortement recommandé d'utiliser Visual Studio Code pour réaliser les exercices de l'atelier. Visual Studio Code offre :
    <ul>
    <li>Un explorateur de fichiers</li>
    <li>Un éditeur de texte avec mise en surbrillance de la syntaxe</li>
    <li>Un terminal intégré</li>
    </ul>
    Un accès SSH direct est disponible en solution de secours, ou si Visual Studio Code ne convient pas. Une courte vidéo YouTube est disponible pour plus de clarté : <a href="https://youtu.be/Y_Gx4ZBfcuk">Ansible Workshops - Accéder à votre environnement de travail</a>.
</th>
  </tr>
</thead>
</table>

- Connectez-vous à Visual Studio Code depuis la page de lancement de l'atelier (fournie par votre instructeur). Le mot de passe est indiqué sous le lien WebUI.

  ![page de lancement](images/launch_page.png)

- Entrez le mot de passe fourni pour vous connecter.

  ![connexion vs code](images/vscode_login.png)

- Ouvrez le répertoire `network-workshop` dans Visual Studio Code :

  ![explorateur de fichiers](images/vscode-networkworkshop.png)

- Cliquez sur `playbook.yml` pour voir le contenu.

  ![playbook](images/vscode-playbook.png)

### Étape 2 - Utilisation du terminal

- Ouvrez un terminal dans Visual Studio Code :

  ![nouveau terminal](images/vscode-new-terminal.png)

Naviguez jusqu'au répertoire `network-workshop` sur le terminal du noeud de contrôle Ansible.

```bash
[student@ansible-1 ~]$ cd ~/network-workshop/
[student@ansible-1 network-workshop]$ pwd
/home/student/network-workshop
[student@ansible-1 network-workshop]$
```

* `~` - le tilde dans ce contexte est un raccourci pour le répertoire personnel, c'est-à-dire `/home/student`
* `cd` - commande Linux pour changer de répertoire
* `pwd` - commande Linux pour afficher le répertoire de travail actuel

### Étape 3 - Examen des environnements d'exécution

Exécutez la commande `ansible-navigator` avec l'argument `images` pour examiner les environnements d'exécution configurés sur le noeud de contrôle :

```bash
$ ansible-navigator images
```

![ansible-navigator images](images/navigator-images.png)

> Note
>
> La sortie que vous voyez peut différer de celle ci-dessus.

Cette commande vous donne des informations sur tous les environnements d'exécution actuellement installés (ou EEs pour "Execution Environments"). Examinez un EE en appuyant sur le numéro correspondant. Par exemple, en appuyant sur **0** dans l'exemple ci-dessus, vous ouvrirez l'environnement d'exécution `network-ee` :

![menu principal ee](images/navigator-ee-menu.png)

La sélection de `2` pour `Version et collections Ansible` affichera toutes les collections Ansible installées sur cet EE particulier, ainsi que la version de `ansible-core` :

![info ee](images/navigator-ee-collections.png)

### Étape 4 - Examen de la configuration d'ansible-navigator

Utilisez Visual Studio Code pour ouvrir ou utilisez la commande `cat` pour afficher le contenu du fichier `ansible-navigator.yml`. Le fichier est situé dans le répertoire personnel :

```bash
$ cat ~/.ansible-navigator.yml
---
ansible-navigator:
  ansible:
    inventory:
      entries:
      - /home/student/lab_inventory/hosts

  execution-environment:
    image: quay.io/acme_corp/network-ee:latest
    enabled: true
    container-engine: podman
    pull:
      policy: missing
    volume-mounts:
    - src: "/etc/ansible/"
      dest: "/etc/ansible/"
```

Notez les paramètres suivants dans le fichier `ansible-navigator.yml` :

* `inventories` : montre l'emplacement de l'inventaire Ansible utilisé
* `execution-environment` : où l'environnement d'exécution par défaut est défini

Pour une liste complète de toutes les options configurables, consultez la [documentation](https://ansible-navigator.readthedocs.io/en/latest/settings/).

### Étape 5 - Examen de l'inventaire

La portée d'un `play` dans un `playbook` est limitée aux groupes d'hôtes déclarés dans un **inventaire** Ansible. Ansible prend en charge plusieurs [types d'inventaire](http://docs.ansible.com/ansible/latest/intro_inventory.html). Un inventaire peut être un simple fichier plat contenant une collection d'hôtes ou un script dynamique (interrogeant potentiellement une base de données CMDB) générant une liste de dispositifs pour exécuter le playbook.

Dans ce laboratoire, vous travaillerez avec un inventaire basé sur fichier au format **ini**. Utilisez Visual Studio Code pour ouvrir ou utilisez la commande `cat` pour afficher le contenu du fichier `~/lab_inventory/hosts`.

```bash
$ cat ~/lab_inventory/hosts
```

```bash
[all:vars]
ansible_ssh_private_key_file=~/.ssh/aws-private.pem

[routers:children]
cisco
juniper
arista

[cisco]
rtr1 ansible_host=18.222.121.247 private_ip=172.16.129.86
[arista]
rtr2 ansible_host=18.188.194.126 private_ip=172.17.158.197
rtr4 ansible_host=18.221.5.35 private_ip=172.17.8.111
[juniper]
rtr3 ansible_host=3.14.132.20 private_ip=172.16.73.175

[cisco:vars]
ansible_user=ec2-user
ansible_network_os=ios
ansible_connection=network_cli

[juniper:vars]
ansible_user=ec2-user
ansible_network_os=junos
ansible_connection=netconf

[arista:vars]
ansible_user=ec2-user
ansible_network_os=eos
ansible_connection=network_cli
ansible_become=true
ansible_become_method=enable

[dc1]
rtr1
rtr3

[dc2]
rtr2
rtr4

[control]
ansible ansible_host=13.58.149.157 ansible_user=student private_ip=172.16.240.184
```

### Étape 6 - Compréhension de l'inventaire

Dans la sortie ci-dessus, chaque `[ ]` définit un groupe. Par exemple, `[dc1]` est un groupe qui contient les hôtes `rtr1` et `rtr3`. Les groupes peuvent également être _imbriqués_. Le groupe `[routers]` est un groupe parent du groupe `[cisco]`.

Les groupes parents sont déclarés à l'aide de la directive `children`. L'imbrication des groupes permet d'attribuer des valeurs plus spécifiques aux variables.

Nous pouvons associer des variables à des groupes et à des hôtes.

> Note :
>
> Un groupe appelé **all** existe toujours et contient tous les groupes et hôtes définis dans un inventaire.

Les variables des hôtes peuvent être définies sur la même ligne que les hôtes eux-mêmes. Par exemple, pour l'hôte `rtr1` :

```sh
rtr1 ansible_host=18.222.121.247 private_ip=172.16.129.86
```

* `rtr1` - Le nom qu'Ansible utilisera. Cela peut, mais ne doit pas, reposer sur le DNS.
* `ansible_host` - L'adresse IP qu'Ansible utilisera. Si elle n'est pas configurée, elle utilisera par défaut le DNS.
* `private_ip` - Cette valeur n'est pas réservée par Ansible, elle sera donc considérée comme une [variable d'hôte](http://docs.ansible.com/ansible/latest/intro_inventory.html#host-variables). Cette variable peut être utilisée par les playbooks ou ignorée.

Les variables de groupe sont déclarées à l'aide de la directive `vars`. Les groupes permettent d'attribuer des variables communes à plusieurs hôtes. Plusieurs variables de groupe peuvent être définies sous la section `[group_name:vars]`. Par exemple, regardez le groupe `cisco` :

```sh
[cisco:vars]
ansible_user=ec2-user
ansible_network_os=ios
ansible_connection=network_cli
```

* `ansible_user` - L'utilisateur qu'Ansible utilisera pour se connecter à cet hôte. Si elle n'est pas configurée, elle utilisera par défaut l'utilisateur avec lequel le playbook est exécuté.
* `ansible_network_os` - Cette variable est nécessaire lors de l'utilisation du type de connexion `network_cli` dans une définition de play.
* `ansible_connection` - Cette variable définit le [plugin de connexion](https://docs.ansible.com/ansible/latest/plugins/connection.html) pour ce groupe. Elle peut être configurée avec des valeurs telles que `netconf`, `httpapi` et `network_cli` en fonction des compatibilités de la plateforme réseau.

### Étape 7 - Utilisation d'ansible-navigator pour explorer l'inventaire

Nous pouvons également utiliser l'interface utilisateur textuelle (TUI) `ansible-navigator` pour explorer l'inventaire.

Exécutez la commande `ansible-navigator inventory` pour afficher l'inventaire dans la TUI :

![ansible-navigator tui](images/ansible-navigator.png)

Appuyer sur **0** ou **1** sur votre clavier ouvrira respectivement les groupes ou les hôtes.

![groupes ansible-navigator](images/ansible-navigator-groups.png)

Appuyez sur la touche **Esc** pour remonter d'un niveau, ou vous pouvez zoomer sur un hôte individuel :

![ansible-navigator hôte](images/ansible-navigator-rtr-1.png)

### Étape 8 - Connexion aux périphériques réseau

Il y a quatre routeurs, nommés rtr1, rtr2, rtr3 et rtr4. Le diagramme réseau est toujours disponible dans la [table des matières de l'atelier d'automatisation réseau](../README.fr.md). Le fichier de configuration SSH (`~/.ssh/config`) est déjà configuré sur le nœud de contrôle. Cela signifie que vous pouvez vous connecter en SSH à n'importe quel routeur depuis le nœud de contrôle sans identifiants supplémentaires :

Par exemple, pour se connecter à rtr1 depuis le nœud de contrôle Ansible, tapez :

```bash
$ ssh rtr1
```

Par exemple :
```
$ ssh rtr1
Warning: Permanently added 'rtr1,35.175.115.246' (RSA) to the list of known hosts.
```

et utilisez la commande `show version` pour vérifier la version de Cisco IOS :

```
rtr1#show ver
Cisco IOS XE Software, Version 17.14.01a
Cisco IOS Software [IOSXE], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 17.14.1a, RELEASE SOFTWARE (fc1)
```

> **Note**
>
> Les ateliers ont récemment été mis à niveau vers Red Hat Enterprise Linux 9, qui utilise une [politique cryptographique système plus sécurisée](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/security_hardening/using-the-system-wide-cryptographic-policies_security-hardening). Si vous rencontrez l'erreur `no mutual signature supported` pour un périphérique réseau Cisco, exécutez la commande `sudo update-crypto-policies --set LEGACY`, puis quittez/réouvrez votre terminal pour que la politique prenne effet. Ce problème sera corrigé dans une future version de l'atelier. Veuillez signaler les problèmes sur https://github.com/ansible/workshops

## Conclusion

Vous avez terminé l'exercice 1 !

Vous comprenez maintenant :

* Comment se connecter à l'environnement de laboratoire avec Visual Studio Code
* Comment explorer les **environnements d'exécution** avec `ansible-navigator`
* Où se trouve la configuration Ansible Navigator (`ansible-navigator.yml`)
* Où est stocké l'inventaire pour les exercices en ligne de commande
* Comment utiliser l'interface utilisateur textuelle (TUI) d'ansible-navigator

---
[Exercice suivant](../2-first-playbook/README.fr.md)

[Retour à l'atelier d'automatisation réseau Ansible](../README.fr.md)



