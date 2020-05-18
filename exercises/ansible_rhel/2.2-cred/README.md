# Workshop Exercise - Inventories, credentials and ad hoc commands

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table of Contents

* [Objective](#objective)
* [Guide](#guide)
* [Examine an Inventory](#examine-an-inventory)
* [Machine Credentials](#machine-credentials)
* [Configure Machine Credentials](#examine-machine-credentials)
* [Run Ad Hoc Commands](#run-ad-hoc-commands)
* [Challenge Lab: Ad Hoc Commands](#challenge-lab-ad-hoc-commands)

# Objective

Explore and understand the lab environment.  This exercise will cover
- Locating and understanding:
  - Ansible Tower [**Inventory**](https://docs.ansible.com/ansible-tower/latest/html/userguide/inventories.html)
  - Ansible Tower [**Credentials**](https://docs.ansible.com/ansible-tower/latest/html/userguide/credentials.html)
- Running ad hoc commands via the Ansible Tower web UI

# Guide

## Examine an Inventory

The first thing we need is an inventory of your managed hosts. This is the equivalent of an inventory file in Ansible Engine. There is a lot more to it (like dynamic inventories) but let’s start with the basics.

  - You should already have the web UI open, if not: Point your browser to the URL you were given, similar to **https://student\<X\>.workshopname.rhdemo.io** (replace "\<X\>" with your student number and "workshopname" with the name of your current workshop) and log in as `admin`. The password will be provided by the instructor.

There will be one inventory, the **Workshop Inventory**. Click the **Workshop Inventory** then click the **Hosts** button

The inventory information at `~/lab_inventory/hosts` was pre-loaded into the Ansible Tower Inventory as part of the provisioning process.

```bash
$ cat ~/lab_inventory/hosts
[all:vars]
ansible_user=student<X>
ansible_ssh_pass=PASSWORD
ansible_port=22

[web]
node1 ansible_host=22.33.44.55
node2 ansible_host=33.44.55.66
node3 ansible_host=44.55.66.77

[control]
ansible ansible_host=11.22.33.44
```
> **Warning**
>
> In your inventory the IP addresses will be different.

## Examine Machine Credentials

Now we will examine the credentials to access our managed hosts from Tower.  As part of the provisioning process for this Ansible Workshop the **Workshop Credential** has already been setup.

In the **RESOURCES** menu choose **Credentials**. Now click on the **Workshop Credential**.

Note the following information:

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

## Run Ad Hoc commands

It is possible to run run ad hoc commands from Ansible Tower as well.

  - In the web UI go to **RESOURCES → Inventories → Workshop Inventory**

  - Click the **HOSTS** button to change into the hosts view and select the three hosts by ticking the boxes to the left of the host entries.

  - Click **RUN COMMANDS**. In the next screen you have to specify the ad hoc command:

  <table>
    <tr>
      <th>Parameter</th>
      <th>Value</th>
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

The simple **ping** module doesn’t need options. For other modules you need to supply the command to run as an argument. Try the **command** module to find the userid of the executing user using an ad hoc command.

  <table>
    <tr>
      <th>Parameter</th>
      <th>Value</th>
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

> **Tip**
>
> After choosing the module to run, Tower will provide a link to the docs page for the module when clicking the question mark next to "Arguments". This is handy, give it a try.

<hr>

How about trying to get some secret information from the system? Try to print out */etc/shadow*.

<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
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


> **Warning**
>
> **Expect an error\!**

Oops, the last one didn’t went well, all red.

Re-run the last ad hoc command but this time tick the **ENABLE PRIVILEGE ESCALATION** box.

As you see, this time it worked. For tasks that have to run as root you need to escalate the privileges. This is the same as the **become: yes** used in your Ansible Playbooks.

## Challenge Lab: Ad Hoc Commands

Okay, a small challenge: Run an ad hoc to make sure the package "tmux" is installed on all hosts. If unsure, consult the documentation either via the web UI as shown above or by running `[ansible@tower ~]$ ansible-doc yum` on your Tower control host.

> **Warning**
>
> **Solution below\!**

<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
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
    <td>ENABLE PRIVILEGE ESCALATION</td>
    <td>✓</td>
  </tr>
</table>

> **Tip**
>
> The yellow output of the command indicates Ansible has actually done something (here it needed to install the package). If you run the ad hoc command a second time, the output will be green and inform you that the package was already installed. So yellow in Ansible doesn’t mean "be careful"…​ ;-).

----
**Navigation**
<br>
[Previous Exercise](../2.1-intro) - [Next Exercise](../2.3-projects)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-2---ansible-tower-exercises)
