# Workshop Exercise - Check the Prerequisites

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table of Contents

* [Objective](#objective)
* [Guide](#guide)
* [Your Lab Environment](#your-lab-environment)
* [Step 1 - Access the Environment](#step-1---access-the-environment)
* [Step 2 - Working the Labs](#step-2---working-the-labs)
* [Step 3 - Challenge Labs](#step-3---challenge-labs)

# Objective

- Understand the lab topology and how to access the environment.
- Understand how to work the workshop exercises
- Understand challenge labs

# Guide

## Your Lab Environment

In this lab you work in a pre-configured lab environment. You will have access to the following hosts:

| Role                 | Inventory name |
| ---------------------| ---------------|
| Ansible Control Host | ansible        |
| Managed Host 1       | node1          |
| Managed Host 2       | node2          |
| Managed Host 3       | node3          |

## Step 1 - Access the Environment

Login to your control host via SSH:

> **Warning**
>
> Replace **11.22.33.44** by your **IP** provided to you, and the **X** in student**X** by the student number provided to you.

    ssh studentX@11.22.33.44

> **Tip**
>
> The password will be provided by your instructor

Then become root:

    [student<X>@ansible ~]$ sudo -i

Most prerequisite tasks have already been done for you:

  - Ansible software is installed

  - SSH connection and keys are configured

  - `sudo` has been configured on the managed hosts to run commands that require root privileges.

Check Ansible has been installed correctly

    [root@ansible ~]# ansible --version
    ansible 2.7.0
    [...]

> **Note**
>
> Ansible is keeping configuration management simple. Ansible requires no database or running daemons and can run easily on a laptop. On the managed hosts it needs no running agent.

Log out of the root account again:

    [root@ansible ~]# exit
    logout

> **Note**
>
> In all subsequent exercises you should work as the student\<X\> user on the control node if not explicitly told differently.

## Step 2 - Working the Labs

You might have guessed by now this lab is pretty commandline-centric…​ :-)

  - Don’t type everything manually, use copy & paste from the browser when appropriate. But stop to think and understand.

  - All labs were prepared using **Vim**, but we understand not everybody loves it. Feel free to use alternative editors. In the lab environment we provide **Midnight Commander** (just run **mc**, function keys can be reached via Esc-\<n\> or simply clicked with the mouse) or **Nano** (run **nano**). Here is a short [editor intro](../0.0-support-docs/editor_intro.md).

> **Tip**
>
> In the lab guide commands you are supposed to run are shown with or without the expected output, whatever makes more sense in the context.

## Step 3 - Challenge Labs

You will soon discover that many chapters in this lab guide come with a "Challenge Lab" section. These labs are meant to give you a small task to solve using what you have learned so far. The solution of the task is shown underneath a warning sign.

----
**Navigation**
<br>
[Next Exercise](../1.2-adhoc)
<br><br>
[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md)
