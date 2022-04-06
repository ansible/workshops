# Atelier - Les inventaires, identifications et commandes Ad-hoc

**Lisez ceci dans d'autres langues**:
<br>![uk](../../../images/uk.png) [English](README.md),![japan](../../../images/japan.png)[日本語](README.ja.md),![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table des matières

* [Objectif](#objectif)
* [Guide](#guide)
* [Examiner un inventaire](#examiner-un-inventaire)
* [Examination des informations d'identifications](#Examination-des-informations-d-identification)
* [Exécution des commandes Ad-hoc](#exécution-des-commandes-ad-hoc)
* [Défi: Les commandes Ad-hoc](#défi-les-commandes-ad-hoc)

# Objectif

Explorez et comprenez l'environnement du laboratoire. Cet exercice couvrira
- Localisation et compréhension:
  - Tour Ansible [**Inventaire**](https://docs.ansible.com/ansible-tower/latest/html/userguide/inventories.html)
  - Tour Ansible [**Informations d'identification **](https://docs.ansible.com/ansible-tower/latest/html/userguide/credentials.html)
- Exécution de commandes ad hoc via l'interface utilisateur Web d'Ansible Tower

# Guide

## Examiner un inventaire

La première chose dont nous avons besoin est un inventaire de vos hôtes gérés. C'est l'équivalent d'un fichier d'inventaire dans Ansible Engine. Il y en a beaucoup plus (comme les inventaires dynamiques), mais commençons par les bases.

  - Vous devriez déjà avoir l'interface utilisateur Web ouverte, sinon: pointez votre navigateur sur l'URL qui vous a été donnée, similaire à **https://student\<X\>.workshopname.rhdemo.io** (remplacez "\<X\> "avec votre numéro d'étudiant et" workshopname "avec le nom de votre atelier actuel) et connectez-vous en tant qu'"admin". Le mot de passe sera fourni par l'instructeur.

Il y aura un seul inventaire, l'**inventaire de l'atelier**. Cliquez sur **Workshop Inventory** puis sur le bouton **Hôtes**

Les informations d'inventaire dans `~/lab_inventory/hosts` ont été préchargées dans l'inventaire de la tour Ansible dans le cadre du processus d'approvisionnement.

```bash
$ cat ~/lab_inventory/hosts
[web]
node1 ansible_host=22.33.44.55
node2 ansible_host=33.44.55.66
node3 ansible_host=44.55.66.77

[control]
ansible ansible_host=11.22.33.44
```
> **Avertissement**
>
> Dans votre inventaire, les adresses IP seront différentes.

## Examination des informations d identification

Nous allons maintenant examiner les informations d'identification pour accéder à nos hôtes gérés depuis Tower. Dans le cadre du processus d'approvisionnement de cet atelier Ansible, **les informations d'identification de l'atelier** ont déjà été configurées.

Dans le menu **RESSOURCES**, choisissez **INFORMATIONS D’IDENTIFICATION**. Maintenant, cliquez sur **Workshop Credential**.

Notez les informations suivantes:

<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>Credential Type</td>
    <td><code>Machine</code>- Machine credentials define ssh and user-level privilege escalation access for playbooks. They are used when submitting jobs to run playbooks on a remote host.</td>
  </tr>
  <tr>
    <td>username</td>
    <td><code>ec2-user</code> which matches our command-line Ansible inventory username for the other linux nodes</td>
  </tr>
  <tr>
    <td>SSH PRIVATE KEY</td>
    <td><code>ENCRYPTED</code> - take note that you can't actually examine the SSH private key once someone hands it over to Ansible Tower</td>
  </tr>
</table>


## Exécution des commandes Ad hoc

Il est également possible d'exécuter des commandes ad hoc à partir d'Ansible Tower.

   - Dans l'interface utilisateur Web, accédez à **RESSOURCES → Inventaires → Workshop Inventory**

   - Cliquez sur le bouton **HÔTES** pour passer à la vue des hôtes et sélectionnez les trois hôtes en cochant les cases à gauche des entrées d'hôte.

   - Cliquez sur **EXÉCUTER COMMANDE**. Dans l'écran suivant, vous devez spécifier la commande ad hoc:
  <table>
    <tr>
      <th>Parametre</th>
      <th>Valeur</th>
    </tr>
    <tr>
      <td>MODULE</td>
      <td>ping</td>
    </tr>
    <tr>
      <td>MACHINE CREDENTIAL</td>
      <td>Workshop Credentials</td>
    </tr>
  </table>

  - Click **LAUNCH**, and watch the output.

<hr>

Le module **ping** simple n'a pas besoin d'options. Pour les autres modules, vous devez fournir la commande à exécuter comme argument. Essayez le module **command** pour trouver l'ID utilisateur de l'utilisateur exécutant à l'aide d'une commande ad hoc.
  <table>
    <tr>
      <th>Parametre</th>
      <th>Valeur</th>
    </tr>
    <tr>
      <td>MODULE</td>
      <td>command</td>
    </tr>
    <tr>
      <td>ARGUMENTS</td>
      <td>id</td>
    </tr>
  </table>

> **Astuce**
>
> Après avoir choisi le module à exécuter, Tower fournira un lien vers la page de documentation du module en cliquant sur le point d'interrogation à côté de "Arguments". C'est pratique, essayez-le.

<hr>

Que diriez-vous d'essayer d'obtenir des informations secrètes du système? Essayez d'afficher le fichier */etc/shadow*.

<table>
  <tr>
    <th>Parametre</th>
    <th>Valeur</th>
  </tr>
  <tr>
    <td>MODULE</td>
    <td>command</td>
  </tr>
  <tr>
    <td>ARGUMENTS</td>
    <td>cat /etc/shadow</td>
  </tr>
</table>


> **Avertissement**
>
> **Attendez-vous à une erreur \!**

Oups, le dernier ne s'est pas bien passé, tout rouge.

Réexécutez la dernière commande Ad-hoc mais cette fois cochez la case **Activer l’élévation des privilèges**.

Comme vous le voyez, cette fois, cela a fonctionné. Pour les tâches qui doivent s'exécuter en tant que root, vous devez augmenter les privilèges. C'est la même chose que le **become: yes** utilisé dans vos Playbooks Ansible.

## Défi: Les commandes Ad hoc

D'accord, un petit défi: exécutez un ad hoc pour vous assurer que le package "tmux" est installé sur tous les hôtes. En cas de doute, consultez la documentation soit via l'interface utilisateur Web comme indiqué ci-dessus, soit en exécutant `[ansible @ tower ~] $ ansible-doc yum` sur votre hôte de contrôle Tower.

> **Avertissement**
>
> **Solution ci-dessous \!**

<table>
  <tr>
    <th>Parametre</th>
    <th>Valeur</th>
  </tr>
  <tr>
    <td>yum</td>
    <td>command</td>
  </tr>
  <tr>
    <td>ARGUMENTS</td>
    <td>name=tmux</td>
  </tr>
  <tr>
    <td>Activer l’élévation des privilèges</td>
    <td>✓</td>
  </tr>
</table>

> **Astuce**
>
> La sortie jaune de la commande indique qu'Ansible a réellement fait quelque chose (ici, il fallait installer le paquet). Si vous exécutez la commande ad hoc une deuxième fois, la sortie sera verte et vous informera que le package a déjà été installé. Donc, le jaune dans Ansible ne signifie pas "soyez prudent"… ;-).
----
**Navigation**
<br>
[Exercice précédent](../2.1-intro/README.fr.md) - [Exercice suivant](../2.3-projects/README.fr.md)

[Cliquez ici pour revenir à l'atelier Ansible pour Red Hat Enterprise Linux](../README.fr.md)
