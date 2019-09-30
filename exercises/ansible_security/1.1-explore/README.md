# Exercise 1.1 - Exploring the lab environment

## Step 1.1 - Objective

The objective of this lab is to provide you a deeper understanding and hands on experience how to automate security tools used by security operators. For that we will tackle three security use cases rather typical for the day-to-day challenges of security operatos. While all of them will interact with roughly the same toolset, each use case shows a different perspective (security analyst, firewall operator, IDS specialist) and thus a different point of view on the available tools.

We have set up a common set of security related tools:

- a Firewall, in this case [Check Point Next Generation Firewall](https://www.checkpoint.com/products/next-generation-firewall/)
- a Security Information and Event Management (SIEM), here [QRadar](https://www.ibm.com/security/security-intelligence/qradar)
- a Intrusion Detection & Prevention System, here [Snort](https://www.snort.org)

The exercises of the first section of this lab guide you through each individual solution mentioned above. You will learn how to access them, what they are used for and how to interact with them using Ansible.

The exercises of the second section of this lab are focused on the actual security operations use cases: situations in which a certain challenge has to be met, usually by interacting not only with one of the mentioned solutions above, but with a mix of them. After setting forth the challenge and explaining what tasks need to be done manually to solve the situation, the lab walks through the steps to automate the tasks with Ansible.

## Step 1.3 - Architecture of the lab, Nodes and Services

In this lab you work in a pre-configured lab environment. You will have access to the following hosts and services:

| Role                         | Inventory name |
| -----------------------------| ---------------|
| Ansible Control Host         | ansible        |
| IBM QRadar                   | qradar         |
| Attacker                     | attacker       |
| Snort                        | snort          |
| Ceck Point Management Server | checkpoint     |
| Ceck Point Gateway           | -              |
| Windows Workstation          | windows-ws     |

The lab is set up individually for you. You have your own environment, own services, own virtual machines.

All interactions with the environment are either done via SSH, or via web browser. All SSH connections should be to your control host, from which the Ansible playbooks are executed. The web browser connections are explained in the  later exercises since they are very specific to the corresponding solutions.

```
      +-------------+
      |             |
      |  Lab        |
      |  computer   +-----------------^------------------->
      |             |                 |                   |
      +-----+-------+                 | RDP/HTTP          | HTTP
            |                         |                   |
        SSH |                         |            +------+------+
            |                         |            |             |
      +-----v-------+          +------+------+     | QRadar      |
  SSH | Ansible     |  REST    | Windows     |     |             |
+-----+ Control     +----+---->+ Workstation |     +--+---+------+
|     | Host        |    |     +------+------+        ^   ^
|     +-------------+    |            |               |   |
|                        +------------o---------------+   |
|                                     |                   |
|                              +------+------+            |
|                              |             |    Syslog  |
|     +-------------+          | Check Point +------------^
|     |             |          | MGMT        |            |
| SSH | Attacker    |  HTTP    |             |            |
+-----+             +------+   +------+------+            |
|     |             |      |          |                   |
|     +-------------+      |          |                   |
|                          |          |                   |
|                          |   +------+------+            |
|                          +---+             |            |
|                              | Check Point |            |
|     +-------------+      +---+ Firewall    |            |
| SSH |             |      |   |             |            |
+-----+ IDS Snort   +------+   +-------------+            |
      |             |  HTTP                               |
      +------+------+                                     |
             |                    Syslog                  |
             +--------------------------------------------+
```

## Step 1.4 - Access the Ansible Environment

For a start, log into your Ansible control host via SSH. Open a terminal and type the following command:

> **Warning**
> 
> In the next examples, replace **11.22.33.44** by the **IP** of your control host, provided to you by the instructor. Also, replace the **X** in student**X** by the student number provided to you. In all following examples and in all other cases were examples contain IP addresses, always replace them with the **IP** addresses from your individual setup

Open a terminal and type the following command to connect to your control host via SSH:

```bash
ssh studentX@11.22.33.44
```

The password is **ansible** if not otherwise noted.

Most prerequisite tasks have already been done for you:

  - Ansible software is installed

  - SSH connection and keys are configured

  - `sudo` has been configured on the managed hosts to run commands that require root privileges.

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

[attack]
attacker ansible_host=99.88.77.66 ansible_user=ec2-user private_ip=172.16.99.66 private_ip2=172.17.44.66

[control]
ansible ansible_host=22.33.44.55 ansible_user=ec2-user private_ip=192.168.2.3

[siem]
qradar ansible_host=22.44.55.77 ansible_user=admin private_ip=172.16.3.44 ansible_httpapi_pass="Ansible1!" ansible_connection=httpapi ansible_httpapi_use_ssl=yes ansible_httpapi_validate_certs=False ansible_network_os=ibm.qradar.qradar

[ids]
snort ansible_host=33.44.55.66 ansible_user=ec2-user private_ip=192.168.3.4 private_ip2=172.17.33.77

[firewall]
checkpoint ansible_host=44.55.66.77 ansible_user=admin private_ip=192.168.4.5 ansible_network_os=checkpoint ansible_connection=httpapi ansible_httpapi_use_ssl=yes ansible_httpapi_validate_certs=no

[windows]
windows-ws ansible_host=55.66.77.88 ansible_user=Administrator ansible_pass=RedHat19! ansible_port=5986 ansible_connection=winrm ansible_winrm_server_cert_validation=ignore private_ip=192.168.5.6
```

On your control host, have a look at the inventory by executing the command `cat ~/lab_inventory/hosts`. All the IP addresses are specific to your environment. Whenever the exercises ask you to access a certain machine, you can always look up the IP in the inventory on the control host.

Ansible is already configured to use the inventory specific to your environment. As shown in the example above, the inventory carries more than just the host names and IP addresses. Especially in the case of the Windows workstation, several more parameters are set.

> **Note**
> 
> Not all hosts in your lab can be reached vis SSH. During the exercises, each node type will be explained in detail and the means how to access the resources will be shown step by step.

## Step 1.6 - Victim machine

For the exercises of section 2 we need to have security incidents. Those should happen on a **victim** machine - that is Snort server. It is basically a RHEL installation with Snort installed and running a simplified web server to run attacks against.

## Step 1.7 - Working the Labs

You might have guessed by now this lab is pretty commandline-centric…​ :-)

  - Don’t type everything manually, use copy & paste from the browser when appropriate. But stop to think and understand.

  - All labs were prepared using **Vim**, but we understand not everybody loves it. Feel free to use alternative editors. In the lab environment we provide **Midnight Commander** (just run **mc**, function keys can be reached via Esc-\<n\> or simply clicked with the mouse) or **Nano** (run **nano**). Here is a short [editor intro](../0.0-support-docs/editor_intro.md).

----

[Click Here to return to the Ansible Security Automation Workshop](../README.md#section-1---introduction-to-ansible-security-automation-basics)
