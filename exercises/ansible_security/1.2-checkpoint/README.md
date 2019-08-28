# Exercise 1.2 - Executing the first Check Point playbook

## Step 2.1 - Check Point Next Generation Firewall

To showcase how to automate the firewall in a security environment, this lab contains a Check Point Next Generaion Firewall (NGFW).

The NGFW is usually not managed directly, but via a central security management server (MGMT). The MGMT is a central tool to manage multiple NGFWs or other security tools in one spot.

There are multiple ways to interact with the MGMT. In our lab, two ways are important:

- API: Ansible mostly works with the API
- Windows client: the user interaction takes place in a Windows client.

In this lab the playbooks we write will be interacting with the API in the background. All actions will be verified in the Windows client UI.

## Step 2.2 - Accessing the Check Point MGMT server via a Windows workstation

Since access to the MGMT server requires a Windows client and we cannot be sure that each and every lab student has access to a Windows environment, we have provisioned a Windows workstation as part of this lab.

The Windows workstation can be reached via Remote Desktop Protocol (RDP). We recommend to use a native RDP client if available. If not, the Workstation is equipped with an HTML RDP client which enables lab participants to access the workstation via browser.

Test the access to the MGMT server now by pointing your RDP client to the `windows-ws` IP in your inventory.

If you do not have a RDP client available or want to test the HTML RDP client, please open the following URL in your browser: `https://<windows-wsIP>/myrtille`. Be sure to replace `<windows-wsIP>` with the IP for the Windows workstation from your inventory. In the login field, only provide the user name and the password: The user name is **Adminimstrator**, the password is **RedHat19!** if not provided otherwise.

## Step 2.3 - Install SmartConsole

SmartConsole should already be installed on your system. Please check your desktop for an icon to launch SmartConsole and launch it. If this works, the following tasks are not necessary and you can proceed to **Step 2.4**.

If for any reason SmartConsole was not installed properly during the deployment of the lab, it is simple to do that yourself:

- Inside your Windows workstation, open the Chrome browser
- Point the browser to `https://<checkpointIP>`, where `<checkpointIP>` is the IP for the checkpoint entry in your inventory
- A warning page will open since Check Point MGMT server is by default installed with a self signed certificate. Accept the certificate by clicking on **Advanced** and afterwards by clicking on the link named **Proceed to 11.22.33.44 (unsafe)**, with your `checkpoint` IP instead of **11.22.33.44** 
- Login with user name `admin` and password `admin123`
- Accept the message of the day with a click on the **Ok** button
- On top of the page, click on the green **Download Now!** button
- The download starts immediately, the file is downloaded to the **Downloads** folder of the administrator
- Find the file and launch the installer via double click
- Accept all default values and finish the installation

## Step 2.4 - Access the SmartConsole UI

Launch the Check Point SmartConsole via the desktop icon. In the following window, as username use `admin` and as password `admin123` if not instructed otherwise. The IP address to enter is the one from the **checkpoint** entry of your inventory.

![SmartConsole login window](images/smartconsole-login-window.png)

Press the **Login** button. Afterwards you need to verify the server fingerprint by clicking the **PROCEED** button.

> **Note**
>
> In a productive nevironment, you would first figure out the fingerprint of the server and would only proceed after you confirmed that the fiungerprint shown is identical with the one from the server. In our demo setup with the short lived instances we can assume that the fingerprints are good.

You are now viewing the Check Point SmartConsole management interface.

![SmartConsole main window](images/smartconsole-main-window.png)

## Step 2.5 - First example playbook

In Ansible, automation is described in playbooks. Playbooks are files which describe the desired configurations or steps to implement on managed hosts. Playbooks can change lengthy, complex administrative tasks into easily repeatable routines with predictable and successful outcomes.

A playbook is where you can take some of those ad-hoc commands you just ran and put them into a repeatable set of *plays* and *tasks*.

A playbook can have multiple plays and a play can have one or multiple tasks. In a task a *module* is called, like the modules in the previous chapter. The goal of a *play* is to map a group of hosts.  The goal of a *task* is to implement modules against those hosts.

> **Tip**
>
> Here is a nice analogy: When Ansible modules are the tools in your workshop, the inventory is the materials and the playbooks are the instructions.

We will now write a playbook to change the configuration of the Check Point setup. We will start with a simple example where we will add a blacklist entry in the firewall configuration.

The playbook will be written and run on the Ansible control host. Use SSH to access your control host. On there, open an editor of your choice and create a file with the name `fw_blacklist_ip.yml`.

First, a playbook needs a name and the hosts it should be executed on. So let's add those:

```yaml
---
- name: Blacklist IP
  hosts: checkpoint
```

> **Note**
>
> It is a good practice to make playbooks more reusable by pointing them at `hosts: all` and limit the execution later on the command line or via Tower. But for now we simplify the process by naming hosts in the playbook directly.

As mentioned, in this a simple example we will add a blacklist entry. A simple blacklist entry consists of a source IP address, a destination IP address and the rule to prevent access between those.

For this, we add the source and destination IP as variables to the playbook.

```yaml
---
- name: Blacklist IP
  hosts: checkpoint

  vars:
    source_ip: 192.168.0.10
    destination_ip: 192.168.0.11
```

Next, we need to add the tasks where the actual changes on the target machines are done. This happens in three steps: first we create a source object, than a destination object, and finally the access rule between those two.

Let's start with a task to define the source object:

```yaml
---
- name: Blacklist IP
  hosts: checkpoint

  vars:
    source_ip: 192.168.0.10
    destination_ip: 192.168.0.11

  tasks:
    - name: Create source IP host object
      checkpoint_host:
        name: "asa-{{ source_ip }}"
        ip_address: "{{ source_ip }}"
```

As you can see, the task itself has a name - just like the play itself - and references a module, here `checkpoint_hosts`. The module has parameters, here `name` and `ip_address`. Each module has individual parameters, often some of them are required while others are optional. To get more information about a module, you can call the help:

```bash
[student<X>@ansible ~]$ ansible-doc checkpoint_host
```

> **Tip**
>
> In `ansible-doc` leave by pressing the button `q`. Use the `up`/`down` arrows to scroll through the content.

In the same way we defined the source IP host object, we will now add the destination IP host object:

```yaml
---
- name: Blacklist IP
  hosts: checkpoint

  vars:
    source_ip: 192.168.0.10
    destination_ip: 192.168.0.11

  tasks:
    - name: Create source IP host object
      checkpoint_host:
        name: "asa-{{ source_ip }}"
        ip_address: "{{ source_ip }}"

    - name: Create destination IP host object
      checkpoint_host:
        name: "asa-{{ destination_ip }}"
        ip_address: "{{ destination_ip }}"
```

Last, we are defining the actual access rule between those two host objects:

```yaml
---
- name: Blacklist IP
  hosts: checkpoint

  vars:
    source_ip: 192.168.0.10
    destination_ip: 192.168.0.11

  tasks:
    - name: Create source IP host object
      checkpoint_host:
        name: "asa-{{ source_ip }}"
        ip_address: "{{ source_ip }}"

    - name: Create destination IP host object
      checkpoint_host:
        name: "asa-{{ destination_ip }}"
        ip_address: "{{ destination_ip }}"

    - name: Create access rule to deny access from source to destination
      checkpoint_access_rule:
        layer: Network
        position: top
        name: "asa-drop-{{ source_ip }}-to-{{ destination_ip }}"
        source: "asa-{{ source_ip }}"
        destination: "asa-{{ destination_ip }}"
        action: drop
```

## Step 2.6 - Run the playbook

Playbooks are executed using the `ansible-playbook` command on the control node. Before you run a new playbook it’s a good idea to check for syntax errors:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook --syntax-check fw_blacklist_ip.yml
```

Now you should be ready to run your playbook:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook fw_blacklist_ip.yml

PLAY [Blacklist IP] *******************************************************************

TASK [Gathering Facts] ****************************************************************
ok: [checkpoint]

TASK [Create source IP host object] ***************************************************
changed: [checkpoint]

TASK [Create destination IP host object] **********************************************
changed: [checkpoint]

TASK [Create access rule to deny access from source todestination] ********************
changed: [checkpoint]

PLAY RECAP ****************************************************************************
checkpoint  : ok=4  changed=1  unreachable=0  failed=0  skipped=0  rescued=0  ignored=0
```

## Step 2.7 - Verfiy changes in UI

Now it's time to check if the changes really did take place, if the actual Check Point MGMT server configuration was really altered.

Access the Windows workstation and open the SmartConsole interface. On the right side, underneath **Object Categories**, click on **Network Objects**, then pick **Hosts**. It should list both new host entries.

![SmartConsole Hosts list](images/smartconsole-hosts-list.png)

Next, on the left side, click on **SECURITY POLICIES** and note the additional access control policy entry in the middle of the field

![SmartConsole Policiy Entries](images/smartconsole-policy-entry.png)

## Step 2.8 - Realizing the same task with pre-defined roles

While it is possible to write a playbook in one file as we did above throughout this workshop, eventually you’ll want to reuse files and start to organize things.

Ansible Roles are the way we do this. When you create a role, you deconstruct your playbook into parts and those parts sit in a directory structure.

There are multiple advantages in using roles to write your automation code. The most notable are that the complexity and intelligence behind a set of playbooks is hidden away. Also the roles are usually easy to re-use by others.

In case of the security automation we created a role which contains the code mentioned above already - together with some more tasks to make sure that the execution runs in no problems in case objects already exist. You can check out the code in the [Github repository acl_manger](https://github.com/ansible-security/acl_manager). The playbook you are familiar with already is in the file (´[tasks/providers/checkpoint/blacklist_ip.yaml](https://github.com/ansible-security/acl_manager/blob/master/tasks/providers/checkpoint/blacklist_ip.yaml).

If you have a closer look at how the entire role is set up you soon will realize that it is made in a way to support firewall solutions from multiple vendors. That way users of the role do not have to worry where are the differences are between different firewall vendors - that is hidden away in the role.

In the more advanced steps in the lab we will sometimes re-use the roles. So let's have a look at how our playbook can be rewritten to use the roles directly. For this first we have to get the role onto our control machine. There are different ways how this can be achieved, but a very convenient way is to use the command line tool `ansible-galaxy`. It can install roles directly from archives, Git URLs - and it can also install roles from [Ansible Galaxy](https://galaxy.ansible.com). Ansible Galaxy is a community hub for finding and sharing Ansible content. It provides features like rating, quality testing, proper searching and so on. For example, the role mentioned above can be found in Ansible Galaxy at [ansible_security/acl_manager](https://galaxy.ansible.com/ansible_security/acl_manager).

On your control host, use the `ansible-galaxy` tool to download and install the above mentioned role with a single command:

```bash
[student<X>@ansible ~]$ ansible-galaxy install ansible_security.acl_manager
- downloading role 'acl_manager', owned by ansible_security
- downloading role from https://github.com/ansible-security/acl_manager/archive/master.tar.gz
- extracting ansible_security.acl_manager to /home/student<X>/.ansible/roles/ansible_security.acl_manager
- ansible_security.acl_manager (master) was installed successfully
```

As you see the role was installed to the roles default path, `~/.ansible/roles/`. It was prefixed by `ansible_security` which is the project writing the security roles used for example in this workshop.

As we now have the role installed on our control host, let's use it. Open your editor to create a new file, `role-blacklist.yml`, and add the name and target hosts. Also, we immediately add the variables needed to tell the tasks what we are going to do.

```yaml
---
- name: Blacklist IP
  hosts: checkpoint

  vars:
    source_ip: 192.168.0.10
    destination_ip: 192.168.0.11
```

Next, add the tasks. Instead of tasks directly interacting with target machines we just reference the role and what tasks of the role we want to be used:

```yaml
---
- name: Blacklist IP
  hosts: checkpoint

  vars:
    source_ip: 192.168.0.10
    destination_ip: 192.168.0.11

  tasks: 
    - include_role:
        name: ansible_security.acl_manager
        tasks_from: blacklist_ip
```

That's it already - the playbook is much shorter than the previous one because a lot of the code already exists in the role!

Now we can execute the role:

```bash
[student<X>@ansible ~]$ ansible-playbook role_blacklist.yml
```

The output should look fairly familiar to you - some of the tasks executed are just the ones we had in our playbook. Others are new - those are tasks ensuring that everything works fine even if certain objects already exist.

You are done with the first steps of automating Check Point with Ansible. Head back to the exercise overview and continue with the next step.

----

[Click Here to return to the Ansible Security Automation Workshop](../README.md)
