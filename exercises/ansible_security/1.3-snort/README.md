# Exercise 1.3 - Executing the first Snort playbook

**Read this in other languages**: <br>
[![uk](../../../images/uk.png) English](README.md),  [![japan](../../../images/japan.png) 日本語](README.ja.md), [![france](../../../images/fr.png) Français](README.fr.md).<br>

<div id="section_title">
  <a data-toggle="collapse" href="#collapse2">
    <h3>Workshop access</h3>
  </a>
</div>
<div id="collapse2" class="panel-collapse collapse">
  <table>
    <thead>
      <tr>
        <th>Role</th>
        <th>Inventory name</th>
        <th>Hostname</th>
        <th>Username</th>
        <th>Password</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Ansible Control Host</td>
        <td>ansible</td>
        <td>ansible-1</td>
        <td>-</td>
        <td>-</td>
      </tr>
      <tr>
        <td>IBM QRadar</td>
        <td>qradar</td>
        <td>qradar</td>
        <td>admin</td>
        <td>Ansible1!</td>
      </tr>
      <tr>
        <td>Attacker</td>
        <td>attacker</td>
        <td>attacker</td>
        <td>-</td>
        <td>-</td>
      </tr>
      <tr>
        <td>Snort</td>
        <td>snort</td>
        <td>snort</td>
        <td>-</td>
        <td>-</td>
      </tr>
      <tr>
        <td>Check Point Management Server</td>
        <td>checkpoint</td>
        <td>checkpoint_mgmt</td>
        <td>admin</td>
        <td>admin123</td>
      </tr>
      <tr>
        <td>Check Point Gateway</td>
        <td>-</td>
        <td>checkpoint_gw</td>
        <td>-</td>
        <td>-</td>
      </tr>
      <tr>
        <td>Windows Workstation</td>
        <td>windows-ws</td>
        <td>windows_ws</td>
        <td>administrator</td>
        <td><em>Provided by Instructor</em></td>
      </tr>
    </tbody>
  </table>
  <blockquote>
    <p><strong>Note</strong></p>
    <p>
    The workshop includes preconfigured SSH keys to log into Red Hat Enterprise Linux hosts and don't need a username and password to log in.</p>
  </blockquote>
</div>

## Step 3.1 - Snort

To showcase how to automate a network intrusion detection and intrusion prevention system in a security environment, this lab will take you through managing a Snort IDS instance. Snort analyzes network traffic and compares it against some given rule set.
In this lab, Snort is installed on a Red Hat Enterprise Linux machine and Ansible interacts with it by accessing the RHEL node over SSH.

## Step 3.2 - Accessing the Snort server

In order to connect to the Snort installation, we need to to find the IP address of the machine it is installed on. You can then get the IP address of the Snort machine by looking up the information on the inventory file `~/lab_inventory/hosts`. In your VS Code online editor, in the menu bar click on **File** > **Open File...** and open the file `/home/student<X>/lab_inventory/hosts`. Search and find the entry for snort which looks like this:

```bash
snort ansible_host=22.333.44.5 ansible_user=ec2-user private_ip=172.16.1.2
```

> **NOTE**
>
> The IP addresses here are for demo purposes and will be different in your case. You have your own dedicated Snort setup in your individual lab environment.

The connection tp the Snort server uses a SSH key pre-installed on the control host, the user for the Snort server is `ec2-user`. In your VS Code online editor, open a terminal and access the snort server via:

```bash
[student<X>@ansible-1 ~]$ ssh ec2-user@snort
Warning: Permanently added '22.333.44.5' (ECDSA) to the list of known hosts.
Last login: Mon Aug 26 12:17:48 2019 from h-213.61.244.2.host.de.colt.net
[ec2-user@snort ~]$
```

To verify snort is installed and configured properly, you can call it via sudo and ask for the version:

```bash
[ec2-user@snort ~]$ sudo snort --version

   ,,_     -*> Snort! <*-
  o"  )~   Version 2.9.13 GRE (Build 15013)
   ''''    By Martin Roesch & The Snort Team: http://www.snort.org/contact#team
           Copyright (C) 2014-2019 Cisco and/or its affiliates. All rights reserved.
           Copyright (C) 1998-2013 Sourcefire, Inc., et al.
           Using libpcap version 1.5.3
           Using PCRE version: 8.32 2012-11-30
           Using ZLIB version: 1.2.7
```

Also, check if the service is actively running via `sudo systemctl`:

```bash
[ec2-user@snort ~]$ sudo systemctl status snort
● snort.service - Snort service
   Loaded: loaded (/etc/systemd/system/snort.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2019-08-26 17:06:10 UTC; 1s ago
 Main PID: 17217 (snort)
   CGroup: /system.slice/snort.service
           └─17217 /usr/sbin/snort -u root -g root -c /etc/snort/snort.conf -i eth0 -p -R 1 --pid-path=/var/run/snort --no-interface-pidfile --nolock-pidfile
[...]
```

> **NOTE**
>
> It might happen that the snort service is not running. In this demo environment this is not a problem, if that is the case, restart it with `systemctl restart snort` and check the status again. It should be running.

Exit the Snort server now by pressing `CTRL` and `D`, or by typing `exit` on the command line. All further interaction will be done via Ansible from the Ansible control host.

## Step 3.3 - Simple Snort rules

In the most basic capacity, Snort works by reading some rules and acting according to them. In this lab, we will be working with some simple examples of Snort in order to show how to automate this configuration with Ansible. This session is not designed to dive into the specifics of Snort rules and the complexity involved in large setups, however, it is helpful to understand the basic structure of a simple rule so that you are aware of what you are automating.

A rule consists of a rule header and rule options and is saved in files.

The Snort rule header breaks down into:

- an action
- the protocol to look for like TCP
- source information like IP and port
- destination information like IP and port

The Snort rule options are keywords separated by `;` and can be:

- messages to output when a rule matches
- SID, a unique identifier of the rule
- content to search for in the packet payload, for example a suspicious string
- or byte tests to check for binary data
- a revision of the rule
- the severity of the attack, called "priority"
- a pre-defined attack type called "classtype" to better group the rule with other rules
- and others.

Not all options are mandatory, some also only override existing default values.

A Snort rule's outline is as follows:

```
[action][protocol][sourceIP][sourceport] -> [destIP][destport] ( [Rule options] )
```

If you want to learn more about Snort rules, check out the [Snort Rule Infographic](https://www.snort.org/documents/snort-rule-infographic) or dive into the [Snort Users Manual (PDF)](https://www.snort.org/documents/snort-users-manual). If you want to have a look at some real Snort rules you can also access the Snort installation in your lab and look at the content of the `/etc/snort/rules` directory.

## Step 3.4 - Example playbook

 As discussed earlier, Ansible automation is described in playbooks. Playbooks consist of tasks. Each task uses a module and the module's corresponding parameters to describe the change that needs to be done or the state that is desired.

Ansible releases are shipped with a set of modules, however, in Ansible Core 2.11 there are no modules to interact with Snort yet. For this reason we wrote a set of modules for managing Snort, which has been included in the `security_ee` execution environment. Using execution environments, we are able to update our modules faster. This is especially important in the early life of a newly developed module.

These Snort modules are shipped as part of a "role". To better describe a role, think about how you wrote your playbook in the last section. While it is possible to write a playbook in one file as we did earlier, often writing all automation pieces in one place results in creating long, complicated playbooks. At some point you will want to reuse the automation content you wrote in your playbooks already. Therefore, you will need to organize things in a way to get multiple smaller playbooks to work together. Ansible roles are the way we achieve this. When you create a role, you deconstruct your playbook into parts and those parts sit in a directory structure.

There are multiple advantages in using roles to write your automation. The most notable is that the complexity and playbook intelligence is hidden from the user. The other important advantage is that roles can be easily shared and re-used.

Back to the Snort use case: as mentioned, the Snort modules are shipped as part of a role. This role is called [ids_rule](https://github.com/ansible-security/ids_rule). Open the Github repository link in the web browser, click on the [library](https://github.com/ansible-security/ids_rule/tree/master/library) path. You will find the module `snort_rule.py` there. This module shipped as a part of the `ids_rule` role, can create and change snort rules.

If you take a closer look at the role you'll see that it comes with a re-usable playbook at [tasks/snort.yml](https://github.com/ansible-security/ids_rule/blob/master/tasks/snort.yml).

Let's have a look at how this playbook can be re-written to use the roles directly. As mentioned previously, the `ids_rule` role is bundled in the `security_ee` execution environment.

In order to use the role, create a new file called `add_snort_rule.yml` in your online editor. Save it in the home directory of your user, and add the name `Add Snort rule` and target hosts, here `snort`. Since we need root rights to make any changes on Snort, add the `become` flag so that Ansible would take care of privilege escalation.

```yaml
---
- name: Add Snort rule
  hosts: snort
  become: true
```

Next we need to add the variables required by our playbook. The role we are using is written in a way that can work with multiple IDS providers, all the user needs to provide is the name of the IDS and the role will take care of the rest. Since we are managing a Snort IDS, we need to set the value of `ids_provider` variable to `snort`.

```yaml
---
- name: Add Snort rule
  hosts: snort
  become: true

  vars:
    ids_provider: snort
```

Next, we need to add the tasks. Tasks are the components which make the actual changes on the target machines. Since we are using a role, we can simply use a single step in our tasks, `include_role`, to add it to our playbook. 

>Note
>
> The Ansible `include_role` module dynamically loads and executes a specified role as a task. Please have a look at the [include_role documentation](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/include_role_module.html) for more information.


In our case, we will use the `include_role` module to use the `ids_rule` role.

In order to make the role suitable for our use case, we add the following task-specific variables:

- the actual rule
- the Snort rules file
- the state of the rule, present or absent

```yaml
---
- name: Add Snort rule
  hosts: snort
  become: true

  vars:
    ids_provider: snort

  tasks:
    - name: Add snort password attack rule
      include_role:
        name: "ansible_security.ids_rule"
      vars:
        ids_rule: 'alert tcp any any -> any any (msg:"Attempted /etc/passwd Attack"; uricontent:"/etc/passwd"; classtype:attempted-user; sid:99000004; priority:1; rev:1;)'
        ids_rules_file: '/etc/snort/rules/local.rules'
        ids_rule_state: present
```

Let's have a quick look at what is happening here. the rule header is `alert tcp any any -> any any`, so we create an alert for tcp traffic from any source to any destination.
The rule options define the human readable Snort message if and when the rule finds a match. `uricontent` which is a specialized version of `content` making it easier to analyze URIs. The `classtype` is set to `attempted-user` which is the default class for "attempted user privilege gain". SID is set to a value high enough for user defined rules. The priority is `1` and finally since this is the first version of this rule we set the revision to `1`.

The other variables, `ids_rules_file` and  `ids_rule_state` provide the user defined location for the rules file and state that the rule should be created if it does not exist already (`present`).

## Step 3.5 - Run the playbook

It is now time to execute the playbook. In your VS Code online editor. In the terminal, execute the following command:

```bash
[student1@ansible-1 ~]$ ansible-navigator run add_snort_rule.yml --mode stdout

PLAY [Add Snort rule] *****************************************************************

TASK [Gathering Facts] ****************************************************************
ok: [snort]

TASK [Add snort password attack rule] *************************************************

TASK [ansible_security.ids_rule : verify required variable ids_provider is defined] ***
skipping: [snort]

TASK [ansible_security.ids_rule : ensure ids_provider is valid] ***********************
skipping: [snort]

TASK [ansible_security.ids_rule : verify required variable ids_rule is defined] *******
skipping: [snort]

TASK [ansible_security.ids_rule : verify required variable ids_rule_state is defined] *
skipping: [snort]

TASK [ansible_security.ids_rule : include ids_provider tasks] *************************
included: /home/student1/.ansible/roles/ansible_security.ids_rule/tasks/snort.yml for
snort

TASK [ansible_security.ids_rule : snort_rule] *****************************************
changed: [snort]

RUNNING HANDLER [ansible_security.ids_rule : restart snort] ***************************
changed: [snort]

PLAY RECAP ****************************************************************************
snort  : ok=4  changed=2  unreachable=0  failed=0  skipped=4  rescued=0  ignored=0
```

As you can see when you run this playbook, there are many tasks executed in addition to adding the rules. For instance, the role reloads the Snort service after the rule is added. Other tasks ensure that the variables are defined and verified.

This yet again highlights the value of using roles. By taking advantage of roles, you are not only making your content re-usable but you can also add verification tasks and other important steps and keep them neatly hidden inside the role. The users of the role do not need to know the specifics of how Snort works in order to use this role as part of their security automation.

## Step 3.6 - Verify changes

A quick way to check if the rules were written correctly is to SSH to the Snort server and look for the content of the `/etc/snort/rules/local.rules` file.

Another way is to use Ansible on our control host. To do this we use a different role to verify if a Snort rule is in place. This role searches and finds existing rules in Snort and is called [ids_rule_facts](http://github.com/ansible-security/ids_rule_facts). This role is included in the `security_ee` execution environment.

In our VS Code online editor, we create a playbook, `verify_attack_rule.yml` to use it. Set the name of the playbook to something like "Verify Snort rule". The values for hosts, the IDS provider variable and the `become` flag can be set to the same as in our previous playbook.

```yaml
---
- name: Verify Snort rule
  hosts: snort
  become: yes

  vars:
    ids_provider: snort
```

Next, we import the role `ids_rule_facts`. We also need to provide a search string to identify the rule we are looking for. In our example, considering the rule we have created, it makes sense to use the `uricontent` rule option for this purpose.

```yaml
---
- name: Verify Snort rule
  hosts: snort
  become: yes

  vars:
    ids_provider: snort

  tasks:
    - name: import ids_rule_facts
      import_role:
        name: 'ansible_security.ids_rule_facts'
      vars:
        ids_rule_facts_filter: 'uricontent:"/etc/passwd"'
```
>Note
>
> The Ansible `import_role` task loads a role and allows you to control when the role tasks run in between other tasks of the play. Please have a look at the [import_role documentation](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/import_role_module.html) for more information.

And most importantly, we want to be able to see what is actually found. The `ids_rule_facts` stores the data it collects as Ansible facts. Ansible facts are information specific to each individual host which can be used in further tasks. Therefore, we add another task to output these facts.

```yaml
---
- name: Verify Snort rule
  hosts: snort
  become: yes

  vars:
    ids_provider: snort

  tasks:
    - name: import ids_rule_facts
      import_role:
        name: 'ansible_security.ids_rule_facts'
      vars:
        ids_rule_facts_filter: 'uricontent:"/etc/passwd"'

    - name: output rules facts
      debug:
        var: ansible_facts.ids_rules
```

Now let's execute the playbook to verify that our rule is part of the Snort installation:

```bash
[student<X>@ansible-1 ~]$ ansible-navigator run verify_attack_rule.yml --mode stdout

PLAY [Verify Snort rule] **************************************************************

TASK [Gathering Facts] ****************************************************************
ok: [snort]

TASK [ansible_security.ids_rule_facts : collect snort facts] **************************
ok: [snort]

TASK [debugoutput rules facts] ********************************************************
ok: [snort] =>
  ansible_facts.ids_rules:
  - alert tcp and any -> any any (msg:"Attempted /etc/passwd Attack";
  uricontent:"/etc/passwd"; classtype:attempted-user; sid:99000004; priority:1; rev:1;)

PLAY RECAP ****************************************************************************
snort  : ok=3  changed=0  unreachable=0  failed=0  skipped=0  rescued=0  ignored=0
```

The last task outputs the rule which was found by the role. As you can see, it is the rule we previously added.

Congratulations! You have completed the first steps of automating Snort with Ansible. Head back to the exercise overview and continue with the next step.

----

**Navigation**
<br><br>
[Previous Exercise](../1.2-checkpoint/README.md) | [Next Exercise](../1.4-qradar/README.md) 
<br><br>
[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md)
