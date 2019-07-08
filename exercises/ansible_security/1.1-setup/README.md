# Exercise 1 - Check the Prerequisites

## Your Lab Environment

In this lab you work in a pre-configured lab environment. You will have access to the following hosts:

| Role                         | Inventory name |
| -----------------------------| ---------------|
| Ansible Control Host         | |
| Splunk Enterprise Security   | |
| Snort                        | |
| Ceck Point Management Server | |
| Ceck Point Gateway           | |

## Step 1.1 - Access the Environment

Login to your control host via SSH:

> **Warning**
> 
> Replace **11.22.33.44** by your **IP** provided to you, and the **X** in student**X** by the student number provided to you.

    ssh studentX@11.22.33.44

> **Tip**
> 
> The password is **ansible** if not otherwise noted.

Then become root:

    [student<X>@ansible ~]$ sudo -i

Most prerequisite tasks have already been done for you:

  - Ansible software is installed

  - SSH connection and keys are configured

  - `sudo` has been configured on the managed hosts to run commands that require root privileges.

Check Ansible has been installed correctly

    [root@ansible ~]# ansible --version
    ansible 2.8.1
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

## Step 1.2 - Working the Labs

You might have guessed by now this lab is pretty commandline-centric.

  - Don’t type everything manually, use copy & paste from the browser when appropriate. But don’t stop to think and understand.

> **Tip**
> 
> In the lab guide commands you are supposed to run are shown with or without the expected output, whatever makes more sense in the context.

----

[Click Here to return to the Ansible Security Automation Workshop](../README.md)
