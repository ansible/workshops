# Workshop Exercise - Your Lab Environment

## Table of Contents

- [Workshop Exercise - Your Lab Environment](#workshop-exercise---your-lab-environment)
  - [Table of Contents](#table-of-contents)
  - [Objectives](#objectives)
  - [Guide](#guide)
    - [Your Lab Environment](#your-lab-environment)
    - [Step 1 - Access the Environment](#step-1---access-the-environment)
    - [Step 2 - Open a Terminal Session](#step-2---open-a-terminal-session)
    - [Step 3 - Access the AAP Web UI](#step-3---access-the-aap-web-ui)
    - [Step 4 - Access the RHEL Web Console](#step-4---access-the-rhel-web-console)
    - [Step 5 - Challenge Labs](#step-5---challenge-labs)
  - [Conclusion](#conclusion)

## Objectives

* Understand the lab topology and how to access the environment
* Understand how to perform the workshop exercises
* Understand challenge labs

## Guide

### Your Lab Environment

The workshop is provisioned with a pre-configured lab environment. You will have access to a host deployed with Ansible Automation Platform (AAP) which you will use to control the playbook and workflow jobs that automation the RHEL in-place upgrade workflow steps. You will also have access to some "pet" application hosts, two with RHEL7 and another two with RHEL8. These are the hosts where we will be upgrading the RHEL operating system (OS).

| Role                 | Inventory name |
| ---------------------| ---------------|
| AAP Control Host     | ansible-1      |
| RHEL7 pet app host 1 | tidy-bengal    |
| RHEL7 pet app host 2 | strong-hyena   |
| RHEL8 pet app host 1 | more-calf      |
| RHEL8 pet app host 2 | upward-moray   |

> **Note**
>
> The inventory names of the pet app hosts will be random pet names different from the example above. <!-- FIXME: The workshop launch page provided by your instructor will list the names actually provisioned with your workshop instance. --> We'll dive deeper into why we are using random names in a later exercise.

### Step 1 - Access the Environment

We will use Visual Studio Code (VS Code) as it provides a convenient and intuitive way to use a web browser to edit files and access terminal sessions. If you are a command line hero, direct SSH access is available if VS Code is not to your liking. There is a short YouTube video to explain if you need additional clarity: <a href="https://youtu.be/Y_Gx4ZBfcuk">Ansible Workshops - Accessing your workbench environment</a>.

- You can open VS Code in your web browser using the "WebUI" link under "VS Code access" on the workshop launch page provided by your instructor. The password is given below the link. For example:

  ![Example link to VS Code WebUI](images/vscode_link.png)

- After opening the link, type in the provided password to access your instance of VS Code.

> **Note**
>
> A welcome wizard may appear to guide you through configuring your VS Code user experience. This is optional as the default settings will work fine for this workshop. Feel free to step though the wizard to explore the VS code bells and whistles or you may just skip it.

### Step 2 - Open a Terminal Session

Terminal sessions provide access to the RHEL commands and utilities that will help us understand what's going on "behind the curtain" when the RHEL in-place upgrade automation is doing its thing.

- Use VS Code to open a terminal session. For example:

  ![Example of how to open a terminal session in VS Code](images/new_term.svg)

- This terminal session will be running on the AAP control host `ansible-1`. Use the `cat /etc/hosts` command to see the hostnames of your pet app hosts. Next, use the `ssh` command to login to one of your pet app hosts. Finally, use the highlighted commands confirm the RHEL OS version and kernel version installed.

  For example:

  ![Example ssh login to pet app host](images/ssh_login.svg)

- In the example above, the command `ssh tidy-bengal` connects us to a new session on the named pet app host. Then the commands `cat /etc/redhat-release` and `uname -r` are used to output the OS release information `Red Hat Enterprise Linux Server release 7.9 (Maipo)` and kernel version `3.10.0-1160.88.1.el7.x86_64` from that host.

### Step 3 - Access the AAP Web UI

The AAP Web UI is where we will go to submit and check the status of the Ansible playbook jobs we will use to automate the RHEL in-place upgrade workflow.

- Let's open the AAP Web UI in a new web browser tab using the "WebUI" link under "Automation controller" on the workshop launch page. For example:

  ![Example link to AAP Web UI](images/aap_link.png)

- Enter the username `admin` and the password provided. This will bring you to your AAP Web UI dashboard like the example below:

  ![Example AAP Web UI dashboard](images/aap_console_example.svg)

- We will learn more about how to use the AAP Web UI in the next exercise.

### Step 4 - Access the RHEL Web Console

We will use the RHEL Web Console to review the results of the Leapp pre-upgrade reports we generate for our pet app servers.

- Open a new web browser tab using the link under "RHEL Web Console" on the workshop launch page. For example:

  ![Example link to RHEL Web Console](images/cockpit_link.png)

- Enter the username `student` and the password provided. This will bring you to a RHEL Web Console Overview page like the example below:

  ![Example RHEL Web Console](images/cockpit_example.svg)

- We will revisit the RHEL Web Console when we are ready to review our pre-upgrade reports in an upcoming exercise.

### Step 5 - Challenge Labs

You will soon discover that many exercises in the workshop come with a "Challenge Lab" step. These labs are meant to give you a small task to solve using what you have learned so far. The solution of the task is shown underneath a warning sign.

## Conclusion

In this exercise, we learned about the lab environment we will be using to continue through the workshop exercises. We verified that we are able to use VS Code in our web browser and from there we can open terminal sessions. We also made sure we are able to access the AAP Web UI which will be the "self-service portal" we use to perform the next steps of the RHEL in-place upgrade automation workflow. Finally, we connected to the RHEL Web Console where we will soon be reviewing pre-upgrade reports.

Use the link below to move on the the next exercise.

---

**Navigation**

[Next Exercise](../1.2-preupg/README.md)

[Home](../README.md)
