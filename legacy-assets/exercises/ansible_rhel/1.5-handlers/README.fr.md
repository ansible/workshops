# Atelier - Les conditions, Handlers et boucles

**Lisez ceci dans d'autres langues**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).


## Table des matières

* [Objectif](#objectif)
* [Guide](#guide)
* [Étape 1 - Les Conditions](#Étape-1---les-conditions)
* [Étape 2 - Les handlers](#Étape-2---les-handlers)
* [Étape 3 - Les boucles simples](#Étape-3---les-boucles-simples)
* [Étape 4 - Les Boucles complexes](#Étape-4---les-boucles-complexes)

# Objectif

Les trois fonctionnalités fondamentales d'Ansible sont les suivantes:
- [Conditions](https://docs.ansible.com/ansible/latest/user_guide/playbooks_conditionals.html)
- [Gestionnaires](https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html#handlers-running-operations-on-change)
- [Boucles](https://docs.ansible.com/ansible/latest/user_guide/playbooks_loops.html)

# Guide

## Étape 1 - Les conditions

Ansible peut utiliser des conditions pour exécuter des tâches ou des plays lorsque certaines conditions sont remplies.

Pour implémenter un conditionnel, l'instruction `when` doit être utilisée, suivie de la condition à tester. La condition est exprimée en utilisant l'un des opérateurs disponibles ci-dessous:

|      |                                                              |
| ---- | ------------------------------------------------------------ |
| \ == | Compare deux objets pour l'égalité.                          |
| \! = | Compare deux objets pour l'inégalité.                        |
| \>   | true si le côté gauche est supérieur au côté droit.          |
| \> = | true si le côté gauche est supérieur ou égal au côté droit.  |
| \<   | true si le côté gauche est plus bas que le côté droit.       |
| \< = | true si le côté gauche est inférieur ou égal au côté droit.  |

Pour plus d'informations à ce sujet, veuillez vous référer à la documentation: <http://jinja.pocoo.org/docs/2.10/templates/>

À titre d'exemple, nous allons installé un serveur FTP, mais uniquement sur les hôtes qui se trouvent dans le groupe d'inventaire "ftpserver".

Pour ce faire, modifiez d'abord l'inventaire pour ajouter un autre groupe et placez `node2` dedans. Assurez-vous que l'adresse IP de `node2` est toujours la même lorsque `node2` est répertorié. Modifiez l'inventaire `~/lab_inventory/hosts` pour qu'il ressemble à la liste suivante:

```ini
[all:vars]
ansible_user=student1
ansible_ssh_pass=ansible
ansible_port=22

[web]
node1 ansible_host=11.22.33.44
node2 ansible_host=22.33.44.55
node3 ansible_host=33.44.55.66

[ftpserver]
node2 ansible_host=22.33.44.55

[control]
ansible ansible_host=44.55.66.77
```

Créez ensuite le fichier `ftpserver.yml` sur votre hôte de contrôle dans le répertoire `~/ansible-files/`:

```yaml
---
- name: Install vsftpd on ftpservers
  hosts: all
  become: yes
  tasks:
    - name: Install FTP server when host in ftpserver group
      yum:
        name: vsftpd
        state: latest
      when: inventory_hostname in groups["ftpserver"]
```

> **Astuce**
>
> À présent, vous devez savoir comment exécuter les Playbooks Ansible, nous allons commencer à être moins verbeux dans ce guide.

Exécutez-le et examinez la sortie. Résultat attendu: la tâche est ignorée sur node1, node3 et l'hôte ansible (votre hôte de contrôle) car ils ne font pas partie du groupe ftpserver dans votre fichier d'inventaire.

```bash
TASK [Install FTP server when host in ftpserver group] *******************************************
skipping: [ansible]
skipping: [node1]
skipping: [node3]
changed: [node2]
```

## Étape 2 - Les handlers

Parfois, lorsqu'une tâche apporte une modification au système, une ou plusieurs tâches supplémentaires peuvent devoir être exécutées. Par exemple, une modification du fichier de configuration d'un service peut alors nécessiter le redémarrage du service pour que la configuration modifiée prenne effet.

Ici, les handlers d'Ansible entrent en jeu. Les handlers peuvent être considérés comme des tâches inactives qui ne sont déclenchées que lorsqu'elles sont explicitement invoquées à l'aide de l'instruction "notify". En savoir plus à leur sujet dans la documentation [Ansible Handlers](http://docs.ansible.com/ansible/latest/playbooks_intro.html#handlers-running-operations-on-change).

À titre d'exemple, écrivons un Playbook qui:

   - gère le fichier de configuration d'Apache `/etc/httpd/conf/httpd.conf` sur tous les hôtes du groupe `web`

   - redémarre Apache lorsque le fichier a changé

Nous avons d'abord besoin du fichier qu'Ansible déploiera, prenons simplement celui de node1. N'oubliez pas de remplacer l'adresse IP indiquée dans la liste ci-dessous par l'adresse IP de votre `node1` personnel.

```
[student<X>@ansible ansible-files]$ scp 11.22.33.44:/etc/httpd/conf/httpd.conf ~/ansible-files/files/.
student<X>@11.22.33.44's password:
httpd.conf             
```

Ensuite, créez le Playbook `httpd_conf.yml`. Assurez-vous que vous êtes dans le répertoire `~/ansible-files`.

```yaml
---
- name: manage httpd.conf
  hosts: web
  become: yes
  tasks:
  - name: Copy Apache configuration file
    copy:
      src: httpd.conf
      dest: /etc/httpd/conf/
    notify:
        - restart_apache
  handlers:
    - name: restart_apache
      service:
        name: httpd
        state: restarted
```

Alors quoi de neuf ici?

   - La section "notifier" n'appelle le handler que lorsque la tâche de copie modifie réellement le fichier. De cette façon, le service est redémarré uniquement si nécessaire - et non à chaque exécution du playbook.

   - La section "handlers" définit une tâche qui n'est exécutée que sur notification.
<hr>

Exécutez le Playbook. Nous n'avons encore rien modifié dans le fichier, donc il ne devrait pas y avoir de lignes "modifies" dans la sortie et bien sûr le handler n'a pas dû se déclencher.

   - Maintenant, changez la ligne `Listen 80` dans `/etc/httpd/conf/httpd.conf` en:

```ini
Listen 8080
```

- Exécutez à nouveau le Playbook. Maintenant, la sortie d'Ansible devrait être beaucoup plus intéressante:

       - httpd.conf a dû être copié

       - Le handler a dû redémarrer Apache

Apache devrait maintenant écouter sur le port 8080. Assez facile à vérifier:

```bash
[student1@ansible ansible-files]$ curl http://22.33.44.55
curl: (7) Failed connect to 22.33.44.55:80; Connection refused
[student1@ansible ansible-files]$ curl http://22.33.44.55:8080
<body>
<h1>This is a production webserver, take care!</h1>
</body>
```
N'hésitez pas à modifier à nouveau le fichier httpd.conf et à exécuter le playbook.

## Étape 3 - Les boucles simples

Les boucles nous permettent de répéter la même tâche encore et encore. Par exemple, supposons que vous souhaitiez créer plusieurs utilisateurs. En utilisant une boucle Ansible, vous pouvez le faire en une seule tâche. Les boucles peuvent également parcourir plus que les listes de base. Par exemple, si vous avez une liste d'utilisateurs avec leur groupe correspondant, la boucle peut également les parcourir. En savoir plus sur les boucles dans la documentation [Ansible Loops](https://docs.ansible.com/ansible/latest/user_guide/playbooks_loops.html).

Pour montrer la fonction des boucles, nous allons générer trois nouveaux utilisateurs sur `node1`. Pour cela, créez le fichier `loop_users.yml` dans `~/ansible-files` sur votre nœud de contrôle en tant qu'utilisateur student. Nous utiliserons le module `utilisateur` pour générer les comptes utilisateurs.


<!-- {% raw %} -->
```yaml
---
- name: Ensure users
  hosts: node1
  become: yes

  tasks:
    - name: Ensure three users are present
      user:
        name: "{{ item }}"
        state: present
      loop:
         - dev_user
         - qa_user
         - prod_user
```
<!-- {% endraw %} -->

Comprendre le playbook et la sortie:

<!-- {% raw%} -->
   - Les noms ne sont pas fournis directement au module utilisateur. Au lieu de cela, il n'y a qu'une variable appelée `{{item}}` pour le paramètre `name`.

   - Le mot clé `loop` répertorie les noms d'utilisateur réels. Ceux-ci remplacent le `{{item}}` pendant l'exécution réelle du playbook.

   - Pendant l'exécution, la tâche n'est répertoriée qu'une seule fois, mais trois modifications sont répertoriées en dessous.
<!-- {% endraw%} -->

## Étape 4 - Les boucles complexes

Comme mentionné, les boucles peuvent également se trouver sur des listes de hachages. Imaginez que les utilisateurs doivent être affectés à différents groupes supplémentaires:

```yaml
- username: dev_user
  groups: ftp
- username: qa_user
  groups: ftp
- username: prod_user
  groups: apache
```

Le module `user` a le paramètre optionnel `groups` pour l'assigner à un groupe. Pour référencer des éléments dans un hachage, le mot clé `{{item}}` doit référencer la sous-clé: `{{item.groups}}` par exemple.

Réécrivons le playbook pour créer les utilisateurs avec des droits d'utilisateur supplémentaires:

<!-- {% raw %} -->
```yaml
---
- name: Ensure users
  hosts: node1
  become: yes

  tasks:
    - name: Ensure three users are present
      user:
        name: "{{ item.username }}"
        state: present
        groups: "{{ item.groups }}"
      loop:
        - { username: 'dev_user', groups: 'ftp' }
        - { username: 'qa_user', groups: 'ftp' }
        - { username: 'prod_user', groups: 'apache' }

```
<!-- {% endraw %} -->

Vérifiez la sortie:

   - Encore une fois, la tâche est répertoriée une fois, mais trois modifications sont répertoriées. Chaque boucle avec son contenu est affichée.

Vérifiez que l'utilisateur `dev_user` a bien été créé sur `node1`:

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m command -a "id dev_user"
node1 | CHANGED | rc=0 >>
uid=1002(dev_user) gid=1002(dev_user) Gruppen=1002(dev_user),50(ftp)
```

----
**Navigation**
<br>
[Exercise précédent](../1.4-variables/README.fr.md) - [Exercise suivant](../1.6-templates/README.fr.md)

[Cliquez ici pour revenir à l'atelier Ansible pour Red Hat Enterprise Linux](../README.fr.md)
