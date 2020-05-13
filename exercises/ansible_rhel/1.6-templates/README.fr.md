# Atelier - Les templates

**Lisez ceci dans d'autres langues**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table des matières

* [Objectif](#objectif)
* [Guide](#guide)
* [Étape 1 - Utilisation des templates](#Étape-1---utilisation-des-templates)
* [Étape 2 - Défi: Les templates](#Étape-2---défi-les-templates)

# Objectif

Cet exercice couvre les templates. Ansible utilise les templates Jinja2 pour modifier les fichiers avant qu'ils ne soient distribués aux hôtes gérés. Jinja2 est l'un des moteurs de modèles les plus utilisés pour Python (<http://jinja.pocoo.org/>).

# Guide

## Étape 1 - Utilisation des templates

Lorsqu'un template de fichier a été créé, il peut être déployé sur les hôtes gérés à l'aide du module `template`, qui prend en charge le transfert d'un fichier local du nœud de contrôle vers les hôtes gérés.

Comme exemple d'utilisation d'un template, vous allez modifier le fichier motd pour qu'il contienne des données spécifiques à l'hôte.

Créez d'abord le répertoire `templates` pour contenir les ressources de template dans `~/ansible-files/`:
```bash
[student<X>@ansible ansible-files]$ mkdir templates
```

Ensuite, dans le répertoire `~/ansible-files/templates/` créez le template `motd-facts.j2`:

<!-- {% raw %} -->
```html+jinja
Welcome to {{ ansible_hostname }}.
{{ ansible_distribution }} {{ ansible_distribution_version}}
deployed on {{ ansible_architecture }} architecture.
```
<!-- {% endraw %} -->

Le template contient le texte de base qui sera ensuite recopié. Il contient également des variables qui seront remplacées individuellement sur les machines cibles.

Ensuite, nous avons besoin d'un playbook pour utiliser ce modèle. Dans le répertoire `~/ansible-files/` créez le Playbook `motd-facts.yml`:
```yaml
---
- name: Fill motd file with host data
  hosts: node1
  become: true
  tasks:
    - template:
        src: motd-facts.j2
        dest: /etc/motd
        owner: root
        group: root
        mode: 0644
```

Vous l'avez déjà fait plusieurs fois:

   - Comprenez ce que fait le Playbook.

   - Exécutez le Playbook `motd-facts.yml`.

   - Connectez-vous à `node1` via SSH et vérifiez le contenu du message du jour.

   - Déconnectez-vous de `node1`.

Vous devriez voir comment Ansible remplace les variables par les faits qu'il a découverts dans le système.

## Étape 2 - Défi: Les templates

Ajoutez une ligne au template pour afficher le noyau utilisé du nœud géré.

   - Trouvez un fait qui contient la version du noyau en utilisant les commandes que vous avez apprises dans le chapitre sur les "faits".

> **Astuce**
>
> Faites un `grep -i` pour le noyau

   - Modifiez le modèle pour utiliser le fait que vous avez trouvé.

   - Exécutez à nouveau le Playbook.

   - Vérifiez motd en vous connectant à node1

> **Avertissement**
>
> **Solution ci-dessous \!**


  - Trouvez le fait:
```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup|grep -i kernel
       "ansible_kernel": "3.10.0-693.el7.x86_64",
```

  - Modifiez le template  `motd-facts.j2`:
<!-- {% raw %} -->
```html+jinja
Welcome to {{ ansible_hostname }}.
{{ ansible_distribution }} {{ ansible_distribution_version}}
deployed on {{ ansible_architecture }} architecture
running kernel {{ ansible_kernel }}.
```
<!-- {% endraw %} -->

  - Executez le playbook.
```
[student1@ansible ~]$ ansible-playbook motd-facts.yml
```

  - Vérifiez le nouveau message via la connexion SSH pour `node1`.
```
[student1@ansible ~]$ ssh node1
Welcome to node1.
RedHat 8.1
deployed on x86_64 architecture
running kernel 4.18.0-147.8.1.el8_1.x86_64.
```

----
**Navigation**
<br>
[Exercise précédent](../1.5-handlers/README.fr.md) - [Exercise suivant](../1.7-role/README.fr.md)

[Cliquez ici pour revenir à l'atelier Ansible pour Red Hat Enterprise Linux](../README.fr.md)
