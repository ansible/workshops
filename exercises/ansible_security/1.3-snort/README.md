# Exercise 1.3 - Executing the first Snort playbook

## Step 3.1 - Snort

To showcase how to automate a network intrusion detection and intrusion prevention system in a security environment, this lab contains a Snort installation. Used as an intrusion detection system, Snort can analyze network traffic and compare it against given rule sets.

In this lab, Snort is installed on a Red Hat Enterprise Linux machine. Ansible interacts with Snort via accessing the Linux node via SSH and interacting with the Snort installation on the machine.

## Step 3.2 - Accessing the Snort server

The Snort software is installed on a typical Red Hat Enterprise Linux system. Thus access to the server is performed via SSH. On you control host `ansible`, open your inventory again and find the IP address of you Snort server. This can also be done in one go with a single command:

```bash
[student<X>@ansible ~]$ grep snort ~/lab_inventory/hosts 
snort ansible_host=22.333.44.5 ansible_user=ec2-user private_ip=172.16.1.2
```

> **NOTE**
>
> The IP addresses here are just an example and will be different in your case since you have a dedicated Snort setup in your individual lab environment.

Knowing this IP address, you can now access the Snort server. Note that the user for the Snort server is `ec2-user`!

```bash
[student<X>@ansible ~]$ ssh ec2-user@22.333.44.5
Warning: Permanently added '22.333.44.5' (ECDSA) to the list of known hosts.
Last login: Mon Aug 26 12:17:48 2019 from h-213.61.244.2.host.de.colt.net
[ec2-user@ip-172-16-1-2 ~]$ 
```

Verify that snort is installed and configured properly by calling it via sudo and let it output the version:

```bash
[ec2-user@ip-172-16-1-2 ~]$ sudo snort --version

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
[ec2-user@ip-172-16-1-2 ~]$ sudo systemctl status snort
● snort.service - Snort service
   Loaded: loaded (/etc/systemd/system/snort.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2019-08-26 17:06:10 UTC; 1s ago
 Main PID: 17217 (snort)
   CGroup: /system.slice/snort.service
           └─17217 /usr/sbin/snort -u root -g root -c /etc/snort/snort.conf -i eth0 -p -R 1 --pid-path=/var/run/snort --no-interface-pidfile --nolock-pidfile
[...]
```

Exit the Snort server now by pressing `CTRL` and `D`, or by typing `exit` on the command line. All further interaction will be done via Ansible from the Ansible control host.

## Step 3.3 - Simple Snort rules

On the most simple level, Snort works by reading rules and acting according to them. We will work with very simple examples of Snort in this lab to highlight how to automate Snort configuration with Ansible. This lab is not meant to dive into the specifics of Snort rules and what can be done with them in complex setups. But it helps if you understand the basic structure of a simple Snort rule to better follow how to automate those.

Basically, a rule consists of a rule header and rule options and is saved in files.

The Snort rule header breaks down into:

- an action
- the protocol to look for like TCP
- source information like IP and port
- destination information like IP and port

The Snort rule options are keywords separated by `;` and can be:

- messages to output when a rule matches
- SID, a unique identifier of the rule
- content to search for in the packet payload, for example a suspicious string
- or also byte tests to check for binary data
- a revision of the rule
- the severity of the attack, called "priority"
- a pre-defined attack type called "classtype" to better group the rule with other rules
- and others.

Not all options are mandatory, some also only override existing default values.

Together a Snort rule outline is:

```
[action][protocol][sourceIP][sourceport] -> [destIP][destport] ( [Rule options] )
```

If you want to learn more about Snort rules, check out the [Snort Rule Infographic](https://www.snort.org/documents/snort-rule-infographic) or dive into the [Snort Users Manual (PDF)](https://www.snort.org/documents/snort-users-manual). If you want to have a look at some real Snort rules you can also access your lab Snort installation and look at the content of the `/etc/snort/rules` directory.

## Step 3.4 - Example playbook

With this knowledge, now let's automate the Snort rule configuration! As described earlier, in Ansible automation is described in playbooks, which consist of multiple tasks. Each task uses a module and corresponding parameters to describe the change that needs to be done or the state that is desired.

In case of Snort, in Ansible 2.9 there are no modules to interact with Snort. So we wrote a set of modules to interact with Snort properly. That way, we can provide value already without the need to wait for a new Ansible release. Also we are able to update our modules faster which is especially important in the early times of a rather newer module. Those modules are shipped as part of a "role". But what are roles?

Think about how you wrote your playbook in the last section: while it is possible to write a playbook in one file as we did, eventually you’ll want to reuse files and start to organize things when the playbook gets longer and multiple playbooks come together.

Ansible Roles are the way we do this. When you create a role, you deconstruct your playbook into parts and those parts sit in a directory structure.

There are multiple advantages in using roles to write your automation code. The most notable are that the complexity and intelligence behind a set of playbooks is hidden away. Also the roles are usually easy to be re-used by others.

Back to the Snort use case: as mentioned, the Snort modules are shipped as part of a role to manage Snort modules. The role is called [ids_rule](https://github.com/ansible-security/ids_rule). Open the link in the web browser and in the shown Github repository, click on the [library](https://github.com/ansible-security/ids_rule/tree/master/library) path. You will find the module `snort_rule.py` there, which can create and change snort rules and is as thus part of the role.

If you take an even closer look at the role you will realize that it also comes along with a re-usable playbook at [tasks/snort.yml](https://github.com/ansible-security/ids_rule/blob/master/tasks/snort.yml).

Let's have a look at how our playbook can be rewritten to use the roles directly. For this first we have to get the role onto our control host. There are different ways how this can be achieved, but a very convenient way is to use the command line tool `ansible-galaxy`. It can install roles directly from archives, Git URLs - and it can also install roles from [Ansible Galaxy](https://galaxy.ansible.com). Ansible Galaxy is a community hub for finding and sharing Ansible content. It provides features like rating, quality testing, proper searching and so on. For example, the role mentioned above can be found in Ansible Galaxy at [ansible_security/ids_rule](https://galaxy.ansible.com/ansible_security/ids_rule).

On your control host, use the `ansible-galaxy` tool to download and install the above mentioned role with a single command:

```bash
[student<X>@ansible ~]$ ansible-galaxy install ansible_security.ids_rule
- downloading role 'ids_rule', owned by ansible_security
- downloading role from https://github.com/ansible-security/ids_rule/archive/master.tar.gz
- extracting ansible_security.ids_rule to /home/student<X>/.ansible/roles/ansible_security.ids_rule
- ansible_security.ids_rule (master) was installed successfully
```

As you see the role was installed to the roles default path, `~/.ansible/roles/`. It was prefixed by `ansible_security` which is the project writing the security roles used for example in this workshop.

As we now have the role installed on our control host, let's use it. Open your editor to create a new file, `add_snort_rule.yml`. And the name and target hosts, here `snort`. Also, since we need root rights to do changes to Snort, add the `become` flag so that Ansible will do a privilege escalation.

```yaml
---
- name: Add Snort rule
  hosts: snort
  become: yes
```

Next we add the variable needed for our rule. The role we downloaded is written in a way that it can work with multiple IDS providers, so we have to set the `ids_provider` to `snort`.

```yaml
---
- name: Add Snort rule
  hosts: snort
  become: yes

  vars:
    ids_provider: snort
```

Next, we need to add the tasks where the actual changes on the target machines are done. Since we re-use a role, this is just a single step where we include the role to which we add some task-specific variables:

- the actual rule
- the Snort rules file
- the state of the rule, present or absent

```yaml
---
- name: Add Snort rule
  hosts: snort
  become: yes

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

Let's quickly look at what is actually happening here: the rule header is `alert tcp any any -> any any`, so we create an alert for tcp traffic from any source to any destination. The rule options define the human readable Snort message when the rule matches, and `uricontent` which is a specialized version of `content` making it easier to analyze URIs. The `classtype` is set to `attempted-user` which is the default class for "attempted user privilege gain" and the SID is set to a value high enough for user defined rules. The priority is `1`. Finally since this is the first version of this rule we set the revision to `1`.

The other variables set the rules file a the user defined location and set that the rule should be created if not there (`present`).

## Step 3.5 - Run the playbook

It is now time to execute the playbook. Call `ansible-playbook` with the playbook name:

```bash
[student1@ansible ~]$ ansible-playbook add_snort_rule.yml 

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

As you see there are many more tasks executed than just the mere adding of the rules. For example the role takes care of reloading the Snort service after the rule was added. Other tasks verify that the entered variables are in fact correct.

This shows again how valuable re-usable roles can be: it is possible to not only make your content re-usable, you can also add verification tasks and other important steps which are neatly hidden inside the role. Users of the role do not need to know the specifics of how Snort works to use the role and embed it into their automation.

## Step 3.6 - Verfiy changes

A quick way to see if the rules were properly written is to check the content of the `/etc/snort/rules/local.rules` file on the Snort server.

Another way is to use Ansible for this: we created an Ansible role to find existing rules in Snort: [ids_rule_facts](https://github.com/ansible-security/ids_rule_facts). Let's use it to verify that the rule is indeed installed on the Snort server.

First, let's install the role with `ansible-galaxy`:

```bash
[student<X>@ansible ~]$ ansible-galaxy install ansible_security.ids_rule_facts
- downloading role 'ids_rule_facts', owned by ansible_security
- downloading role from https://github.com/ansible-security/ids_rule_facts/archive/master.tar.gz
- extracting ansible_security.ids_rule_facts to /home/student1/.ansible/roles/ansible_security.ids_rule_facts
- ansible_security.ids_rule_facts (master) was installed successfully
```

Now, let's create a playbook, `verify_attack_rule.yml`. The hosts, the IDS provider variable and the `become` flag can be re-used from the playbook above. Only the name needs to change.

```yaml
---
- name: Verify Snort rule
  hosts: snort
  become: yes

  vars:
    ids_provider: snort
```

Next, we import the role `ids_rule_facts` and provide a search string to identify the rule we are looking for. In our example it makes sense to use the `uricontent` rule option:

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

Last but not least we want to see what was actually found. The `ids_rule_facts` stores the data it collects about rules as Ansible facts - information individual to each host which can be used in further tasks. So we add another task outputting these facts:

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

Now let's execute the playbook to verify that our rule is indeed part of the Snort installation:

```bash
[student<X>@ansible ~]$ ansible-playbook verify_attack_rule.yml 

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

The last task outputs the actual rule which was found by the role. And in fact it is the rule we previously added.

You are done with the first steps of automating Snort with Ansible. Head back to the exercise overview and continue with the next step.

----

[Click Here to return to the Ansible Security Automation Workshop](../README.md#section-1---introduction-to-ansible-security-automation-basics)
