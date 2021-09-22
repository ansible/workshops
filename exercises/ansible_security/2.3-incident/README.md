# Exercise 2.3 - Incident response

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

## Step 3.1 - Background

In this exercise we will focus on threat detection and response capabilities. As usual, security operators need a set of tools in enterprise IT to perform this task.

You are a security operator in charge of the corporate IDS. The IDS of our choice is Snort.

## Step 3.2 - Preparations

We will start this exercise with an operator looking at logs in Snort. So first we need to set up a snort rule to actually generate log entries. In your VS Code online editor, create the playbook `incident_snort_rule.yml`:

<!-- {% raw %} -->
```yaml
---
- name: Add ids signature for sql injection simulation
  hosts: ids
  become: yes

  vars:
    ids_provider: snort
    protocol: tcp
    source_port: any
    source_ip: any
    dest_port: any
    dest_ip: any

  tasks:
    - name: Add snort sql injection rule
      include_role:
        name: "ansible_security.ids_rule"
      vars:
        ids_rule: 'alert {{protocol}} {{source_ip}} {{source_port}} -> {{dest_ip}} {{dest_port}}  (msg:"Attempted SQL Injection"; uricontent:"/sql_injection_simulation"; classtype:attempted-admin; sid:99000030; priority:1; rev:1;)'
        ids_rules_file: '/etc/snort/rules/local.rules'
        ids_rule_state: present
```
<!-- {% endraw %} -->

To be able to execute the playbook we will use the prepared role `ids_rule` to modify IDS rules, which is included in the `security_ee` execution environment. The same is true for the role `ids.config`.

Run the playbook with:

```bash
[student<X>@ansible-1 ~]$ ansible-navigator run incident_snort_rule.yml --mode stdout
```

To have those rules generate logs, we need suspicious traffic - an attack. Again we have a playbook which simulates a simple access every few seconds on which the other components in this exercise will later on react to. In your VS Code online editor, create the playbook `sql_injection_simulation.yml` with the following content:

<!-- {% raw %} -->
```yml
---
- name: start sql injection simulation
  hosts: attacker
  become: yes
  gather_facts: no

  tasks:
    - name: simulate sql injection attack every 5 seconds
      shell: "/sbin/daemonize /usr/bin/watch -n 5 curl -m 2 -s http://{{ hostvars['snort']['private_ip2'] }}/sql_injection_simulation"
```
<!-- {% endraw %} -->

Run it with:

```bash
[student<X>@ansible-1 ~]$ ansible-navigator run sql_injection_simulation.yml --mode stdout
```

For this exercise to work properly, we'll need to make sure a few steps in the previous [Check Point exercises](../1.2-checkpoint/README.md) have been completed:

1. The `whitelist_attacker.yml` playbook must have been run at least once. 
2. Also, the logging for the attacker whitelist policy must have been activated in the Check Point SmartConsole.

Both were done in the [Check Point exercises](../1.2-checkpoint/README.md). If you missed the steps, go back there, execute the playbook, follow the steps to activate the logging and come back here.

## Step 3.3 - Identify incident

As the security operator in charge of the corporate IDS, you routinely check the logs. From the terminal of your VS Code online editor, SSH to your snort node as the user `ec2-user` and view the logs:

```bash
[student<X>@ansible-1 ~]$ ssh ec2-user@snort
```
```bash
[ec2-user@snort ~]$ journalctl -u snort -f
-- Logs begin at Sun 2019-09-22 14:24:07 UTC. --
Sep 22 21:03:03 ip-172-16-115-120.ec2.internal snort[22192]: [1:99000030:1] Attempted SQL Injection [Classification: Attempted Administrator Privilege Gain] [Priority: 1] {TCP} 172.17.78.163:53376 -> 172.17.23.180:80
Sep 22 21:03:08 ip-172-16-115-120.ec2.internal snort[22192]: [1:99000030:1] Attempted SQL Injection [Classification: Attempted Administrator Privilege Gain] [Priority: 1] {TCP} 172.17.78.163:53378 -> 172.17.23.180:80
Sep 22 21:03:13 ip-172-16-115-120.ec2.internal snort[22192]: [1:99000030:1] Attempted SQL Injection [Classification: Attempted Administrator Privilege Gain] [Priority: 1] {TCP} 172.17.78.163:53380 -> 172.17.23.180:80
```

As you see this node has just registered multiple alerts to an **Attempted Administrator Privilege Gain**. Leave the log view by pressing `CTRL-C`.

If you want a closer look at the details in the snort log, check out the content of the file `/var/log/snort/merged.log` on the Snort machine:

```bash
[ec2-user@snort ~]$ sudo tail -f /var/log/snort/merged.log
Accept: */*
[...]
GET /sql_injection_simulation HTTP/1.1
User-Agent: curl/7.29.0
Host: 172.17.30.140
Accept: */*
```
Besides some weird characters you will see the actual malformed "attack" of the user in the form of the string `sql_injection_simulation`. Leave the Snort server with the command `exit` .

## Step 3.4 - Create and run a playbook to forward logs to QRadar

To better analyze this incident it is crucial to correlate the data with other sources. For this we want to feed the logs into our SIEM, QRadar.

As you know by now, due to the missing integration of various security tool with each other, as a security operator in charge of the IDS we would now have to manually contact another team or forward our logs via e-mail. Or upload them to a FTP server, carry them over on USB stick or worse. Luckily as shown in the last exercises already we can use Ansible to just configure Snort and Qradar.

In your VS Code online editor, create a playbook called `incident_snort_log.yml` like the following:

<!-- {% raw %} -->
```yaml
---
- name: Configure snort for external logging
  hosts: snort
  become: true
  vars:
    ids_provider: "snort"
    ids_config_provider: "snort"
    ids_config_remote_log: true
    ids_config_remote_log_destination: "{{ hostvars['qradar']['private_ip'] }}"
    ids_config_remote_log_procotol: udp
    ids_install_normalize_logs: false

  tasks:
    - name: import ids_config role
      include_role:
        name: "ansible_security.ids_config"

- name: Add Snort log source to QRadar
  hosts: qradar
  collections:
    - ibm.qradar

  tasks:
    - name: Add snort remote logging to QRadar
      qradar_log_source_management:
        name: "Snort rsyslog source - {{ hostvars['snort']['private_ip'] }}"
        type_name: "Snort Open Source IDS"
        state: present
        description: "Snort rsyslog source"
        identifier: "{{ hostvars['snort']['ansible_fqdn'] }}"

    - name: deploy the new log sources
      qradar_deploy:
        type: INCREMENTAL
      failed_when: false
```
<!-- {% endraw %} -->

This playbook should look familiar to you, it configures Snort to send logs to QRadar, configures QRadar to accept those and enables an offense. Run it:

```bash
[student<X>@ansible-1 ~]$ ansible-navigator run incident_snort_log.yml --mode stdout
```

## Step 3.5 - Verify new configuration in QRadar

Let's change our perspective briefly to the one of a security analyst. We mainly use the SIEM, and now logs are coming in from Snort. To verify that, access your QRadar UI, open the **Log Activity** tab and validate that events are now making it to QRadar from Snort.

![QRadar logs view, showing logs from Snort](images/qradar_incoming_snort_logs.png#centreme)

>**Note**
>
> If no logs are shown, wait a bit. It might take more than a minute to show the first entries. Also, the first logs might be identified with the "default" log source (showing **SIM Generic Log DSM-7** instead of **Snort rsyslog source**) so give it some time.

As the analyst, it's our responsibility to investigate possible security threats and, if necessary, create an incident response. In this case, the SQL Injection attack is indeed a cyber attack and we need to mitigate it as soon as possible. 

To have a clearer view of the logs, change the display to **Raw Events** at the top of the Log Activity output window. 

![QRadar logs view, attacker IP address](images/qradar_attacker_ip.png#centreme)

>**Note**
>
>Remember that it helps to add filters to the QRadar log view for more concise information.   

Looking closer at the **Raw Events** output, we can see that the Snort logs includes a ***Host*** entry with the IP address. This is vital information we'll need to remediate the cyber attack.

>**Note**
>
>Note that these logs already show an offense marker on the left hand side.

Open the **Offenses** tab on the top menu. We'll see a newly created offense similar to the below. 

![QRadar offense list](images/qradar_offense_list.png#centreme)

Double-click on the new offense and in the top right hand corner, click on the **Display** dropdown menu and select **Annotations**.

![QRadar Offense Display menu](images/qradar_offense_display_menu.png)

 In the *Annotation section, there we will see a **SQL Injection Detected** annotation indicating that our custom **Ansible Workshop SQL Injection Rule** was triggered.

![QRadar Offense Annotation](images/qradar_annotation_sql_injection.png)

## Step 3.6 - Blacklist IP

With all these information at hand, we can now create our incident response. We've realized that these attacks originate from a specific IP which we previously identified in the Snort logs in the QRadar Log Activity window. So let's stop it! We will blacklist the source IP of the attacker.

In a typical environment, performing this remediation would require yet another interaction with the security operators in charge of the firewalls. But we can launch an Ansible playbook to achieve the same goal in seconds rather than hours or days.

In your VS Code online editor, create a file called `incident_blacklist.yml`. Note that we do not enter the IP address here but again a variable, since Ansible already has the information from the inventory.

<!-- {% raw %} -->
```yaml
---
- name: Blacklist attacker
  hosts: checkpoint

  vars:
    source_ip: "{{ hostvars['attacker']['private_ip2'] }}"
    destination_ip: "{{ hostvars['snort']['private_ip2'] }}"

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
        auto_install_policy: yes
        auto_publish_session: yes
        layer: Network
        position: top
        name: "asa-accept-{{ source_ip }}-to-{{ destination_ip }}"
        source: "asa-{{ source_ip }}"
        destination: "asa-{{ destination_ip }}"
        action: drop

    - name: Install policy
      cp_mgmt_install_policy:
        policy_package: standard
        install_on_all_cluster_members_or_fail: yes
      failed_when: false
```
<!-- {% endraw %} -->

Run the playbook, to effectively blacklist the IP:

```bash
[student<X>@ansible-1 ~]$ ansible-navigator run incident_blacklist.yml --mode stdout
```

In your QRadar UI, verify in the Log Activity tab that you do not receive any more alerts from Snort. Note that, if you would have connected the firewall to QRadar, there would actually be logs coming in from there.

Also, let's quickly verify that the new rule was added to Check Point: Access the Windows workstation and open the SmartConsole interface. On the left side, click on **SECURITY POLICIES** and note that the access control policy entry changed from **Accept** to **Drop**.

![SmartConsole Blacklist Policy](images/check_point_policy_drop.png#centreme)

You have successfully identified an attack and blocked the traffic behind the attack!

## Step 3.7 - Roll back

As the final step, we can run the rollback playbook to undo the Snort configuration, reducing resource consumption and the analysis workload.

>**Note**
>
> Please ensure that you have exited out of any current ssh sessions and have your **control-node** prompt open before running the `rollback.yml` playbook.


Execute the playbook `rollback.yml` we wrote in the last exercise to roll all changes back.

```bash
[student<X>@ansible-1 ~]$ ansible-navigator run rollback.yml --mode stdout
```

Note here that the playbook runs through without problems - even though we did not configure Check Point as a log source for QRadar this time! This is possible since Ansible tasks are most often idempotent: they can be run again and again, ensuring the desired state.

Also we need to kill the process simulating the attack. In the terminal, run the `stop_attack_simulation.yml` playbook.

<!-- {% raw %} -->
```bash
[student<X>@ansible-1 ~]$ ansible-navigator run stop_attack_simulation.yml --mode stdout
```
<!-- {% endraw %} -->

You are done with this last exercise. Congratulations!

## Step 3.8 - Wrap it all up

It happens that the job of a CISO and her team is difficult even if they have in place all necessary tools, because the tools don’t integrate with each other. When there is a security breach, an analyst has to perform a triage, chasing all relevant piece of information across the entire infrastructure, taking days to understand what’s going on and ultimately perform any sort of remediation.

Ansible Security Automation is a Red Hat initiative to facilitate the integration of a wide range of security solutions through a common and open automation language: Ansible. Ansible Security Automation is designed to help security analysts investigate and remediate security incidents faster.

This is how ansible security automation can integrate three different security products, an enterprise firewall, an IDS, and a SIEM, to help security analysts and operators in investigation enrichment, threat hunting and incident response.

Ansible Security Automation allows security organizations to create pre-approved automation workflows, called playbooks, that can be maintained centrally and shared across different teams. And with the help of automation controller, we can even provide those automation workflows to other teams in a controlled, user friendly and simple to consume way.

----
**Navigation**
<br><br>
[Previous Exercise](..//2.2-threat/README.md)
<br><br>
[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md)