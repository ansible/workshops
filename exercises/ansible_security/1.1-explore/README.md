# Exercise 1.1 - Exploring the lab environment

## Step 1.1 - Objective

Explore and understand the lab environment. This exercise will cover

- The general setup and idea of the lab
- What nodes and services are part of your environment.
- How you access the control node.
- What your inventory is and where you can find it.
- How to edit files.

## Step 1.2 - General Setup of the lab

The focus of this lab is to show how automation can help with various security challenges in the day-to-days business of security practitioners. For this we have set up a typical set of security related tools:

- a Firewall, in this case [CheckPoint Next Generation Firewall](https://www.checkpoint.com/products/next-generation-firewall/)
- a Security Information and Event Management (SIEM), here [https://www.splunk.com/en_us/software/enterprise-security.html](Splunk Enterprise Security)
- a Intrusion Detection & Prevention System, here [Snort](https://www.snort.org)

The exercises of the first section of this lab guide you through each individual solution mentioned above. You will learn how to access them, what is basically possible with them and how to interact with them using Ansible.

The exercises of the second section of this lab are focused on typical security operations use cases: situations in which a certain challenge has to be met, usually by interacting not only with one of the mentioned solutions above, but with a mix of them. After setting forth the challenge and explaining what tasks need to be done manually to solve the situation, the lab walks through the steps to automate the tasks with Ansible.

## Step 1.3 - Nodes and Services

In this lab you work in a pre-configured lab environment. You will have access to the following hosts and services:

| Role                         | Inventory name |
| -----------------------------| ---------------|
| Ansible Control Host         | ansible        |
| Splunk Enterprise Security   | splunk         |
| Snort                        | snort          |
| Ceck Point Management Server | checkpoint     |
| Ceck Point Gateway           | -              |
| Windows Workstation          | windows-ws     |

## Step 1.4 - Access the Ansible Environment

Login to your control host via SSH. Open a terminal and type the following command:

> **Warning**
> 
> Replace **11.22.33.44** by your **IP** provided to you, and the **X** in student**X** by the student number provided to you in the following example and in all other cases were examples contain IP addresses.

```bash
ssh studentX@11.22.33.44
```

The password is **ansible** if not otherwise noted.

Then become root:

```bash
[student<X>@ansible ~]$ sudo -i
```

Most prerequisite tasks have already been done for you:

  - Ansible software is installed

  - SSH connection and keys are configured

  - `sudo` has been configured on the managed hosts to run commands that require root privileges.

Log out of the root account again:

```bash
    [root@ansible ~]# exit
    logout
```

Check Ansible has been installed correctly

```bash
    [student<X>@ansible ~]$ ansible --version
    ansible 2.8.2
    [...]
```

In all subsequent exercises you should work as the student\<X\> user on the control node if not explicitly told differently.

> **Note**
> 
> Ansible is keeping configuration management simple. Ansible requires no database or running daemons and can run easily on a laptop. On the managed hosts it needs no running agent.

## Step 1.5 - Your inventory

The inventory of your environment will be provided in a static, ini-type file. It can be found at `/home/student<X>/lab_inventory/hosts` and looks like the following listing. Please note that the IP addresses provided here are just an example and will be different in your lab environment:

```ini
[all:vars]
ansible_user=student1
ansible_ssh_pass=ansible
ansible_port=22

[siem]
splunk ansible_host=11.22.33.44 ansible_user=admin private_ip=192.168.1.2 ansible_ssh_pass=admin

[control]
ansible ansible_host=22.33.44.55 ansible_user=ec2-user private_ip=192.168.2.3

[ids]
snort ansible_host=33.44.55.66 ansible_user=ec2-user private_ip=192.168.3.4

[firewall]
checkpoint ansible_host=44.55.66.77 ansible_user=admin private_ip=192.168.4.5 ansible_network_os=checkpoint ansible_connection=httpapi ansible_httpapi_use_ssl=yes ansible_httpapi_validate_certs=no

[windows]
windows-ws ansible_host=55.66.77.88 ansible_user=Administrator ansible_pass=RedHat19! ansible_port=5986 ansible_connection=winrm ansible_winrm_server_cert_validation=ignore private_ip=192.168.5.6
```

Ansible is already configured to use the inventory specific to your environment. As shown in the example above, the inventory carries more than just the host names and IP addresses. Especially in the case of the Windows workstation, several more parameters are set.

> **Note**
> 
> Not all hosts in your lab can be reached vis SSH. During the exercises, each node type will be explained in detail and the means how to access the resources will be shown step by step.

## Step 1.6 - Working the Labs

You might have guessed by now this lab is pretty commandline-centric…​ :-)

  - Don’t type everything manually, use copy & paste from the browser when appropriate. But stop to think and understand.

  - All labs were prepared using **Vim**, but we understand not everybody loves it. Feel free to use alternative editors. In the lab environment we provide **Midnight Commander** (just run **mc**, function keys can be reached via Esc-\<n\> or simply clicked with the mouse) or **Nano** (run **nano**). Here is a short [editor intro](../0.0-support-docs/editor_intro.md).

> **Tip**
>
> In the lab guide commands you are supposed to run are shown with or without the expected output, whatever makes more sense in the context.

----

[Click Here to return to the Ansible Security Automation Workshop](../README.md)
