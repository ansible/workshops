# Workshop Exercise - Check the Prerequisites

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table of Contents

- [Workshop Exercise - Check the Prerequisites](#workshop-exercise---check-the-prerequisites)
  - [Table of Contents](#table-of-contents)
  - [Objective](#objective)
  - [Guide](#guide)
    - [Your Lab Environment](#your-lab-environment)
    - [Step 1 - Access the Environment](#step-1---access-the-environment)
    - [Step 2 - Using the Terminal](#step-2---using-the-terminal)
    - [Step 3 - Examining Execution Environments](#step-3---examining-execution-environments)
    - [Step 4 - Examining the ansible-navigator configuration](#step-4---examining-the-ansible-navigator-configuration)
    - [Step 5 - Challenge Labs](#step-5---challenge-labs)

## Objective

* Understand Lab Topology: Familiarize yourself with the lab environment and access methods.
* Master Workshop Exercises: Gain proficiency in navigating and executing workshop tasks.
* Embrace Challenge Labs: Learn to apply your knowledge in practical challenge scenarios.

## Guide

This workshop's initial phase focuses on the command-line utilities of the Ansible Automation Platform, such as:


- [ansible-navigator](https://github.com/ansible/ansible-navigator) - a Text-based User Interface (TUI) for running and developing Ansible content.
- [ansible-core](https://docs.ansible.com/core.html) - the base executable that provides the framework, language and functions that underpin the Ansible Automation Platform, including CLI tools like `ansible`, `ansible-playbook` and `ansible-doc`.
- [Execution Environments](https://docs.ansible.com/automation-controller/latest/html/userguide/execution_environments.html) - Pre-built container images with Red Hat supported collections. 
- [ansible-builder](https://github.com/ansible/ansible-builder) - automates the  process of building Execution Environments. Not a primary focus in this workshop.

If you need more information on new Ansible Automation Platform components bookmark this landing page [https://red.ht/AAP-20](https://red.ht/AAP-20)


### Your Lab Environment

You'll work in a pre-configured environment with the following hosts:


| Role                 | Inventory name |
| ---------------------| ---------------|
| Ansible Control Host | ansible-1      |
| Managed Host 1       | node1          |
| Managed Host 2       | node2          |
| Managed Host 3       | node3          |

### Step 1 - Access the Environment

We recommend using Visual Studio Code for this workshop for its integrated file browser, syntax-highlighting editor, and in-browser terminal. Direct SSH access is also available. Check out this YouTube tutorial on accessing your workbench environment.

NOTE: There is a short YouTube video provided if you need additional clarity:
[Ansible Workshops - Accessing your workbench environment](https://youtu.be/Y_Gx4ZBfcuk)


1. Connect to Visual Studio Code via the Workshop launch page.

  ![launch page](images/launch_page.png)

2. Enter the provided password to login. 

  ![login vs code](images/vscode_login.png)


### Step 2 - Using the Terminal

1. Open a terminal in Visual Studio Code:

  ![picture of new terminal](images/vscode-new-terminal.png)

2. Navigate to the `rhel-workshop` directory on the Ansible control node terminal.

```bash
[student@ansible-1 ~]$ cd ~/rhel-workshop/
[student@ansible-1 rhel-workshop]$ pwd
/home/student/rhel-workshop
```

* `~`: shortcut for the home directory `/home/student`
* `cd`: command to change directories
* `pwd`: prints the current working directory's full path.

### Step 3 - Examining Execution Environments

1. Run `ansible-navigator images` to view configured Execution Environments.
2. Use the corresponding number to investigate an EE, e.g. pressing 2 to open `ee-supported-rhel8`

```bash
$ ansible-navigator images
```

![ansible-navigator images](images/navigator-images.png)


> Note: The output  you see might differ from the above output


![ee main menu](images/navigator-ee-menu.png)

Selecting `2` for `Ansible version and collections` will show us all Ansible Collections installed on that particular EE, and the version of `ansible-core`:

![ee info](images/navigator-ee-collections.png)

### Step 4 - Examining the ansible-navigator configuration

1. View the contents of `~/.ansible-navigator.yml` using Visual Studio Code or the `cat` command.

```bash
$ cat ~/.ansible-navigator.yml
---
ansible-navigator:
  ansible:
    inventory:
      entries:
      - /home/student/lab_inventory/hosts

  execution-environment:
    image: registry.redhat.io/ansible-automation-platform-20-early-access/ee-supported-rhel8:2.0.0
    enabled: true
    container-engine: podman
    pull:
      policy: missing
    volume-mounts:
    - src: "/etc/ansible/"
      dest: "/etc/ansible/"
```

2. Note the following parameters within the `ansible-navigator.yml` file:

* `inventories`: shows the location of the ansible inventory being used
* `execution-environment`: where the default execution environment is set

For a full listing of every configurable knob checkout the [documentation](https://ansible.readthedocs.io/projects/navigator/settings/)

### Step 5 - Challenge Labs

Each chapter comes with a Challenge Lab. These tasks test your understanding and application of the learned concepts. Solutions are provided under a warning sign for reference.

---
**Navigation**

<br>

{% if page.url contains 'ansible_rhel_90' %}
[Next Exercise](../2-thebasics)
{% else %}
[Next Exercise](../1.2-thebasics)
{% endif %}
<br><br>
[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md)
