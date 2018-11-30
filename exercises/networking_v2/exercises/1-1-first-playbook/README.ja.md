# Exercise 1.1 - Writing your first playbook

Now that you have a fundamental grasp of the inventory file and the group/host variables, this section will walk you through building a playbook.

> This section will help you understand the components of a playbook while giving you an immediate baseline for using it within your own production environment!

#### Step 1:

Using your favorite text editor (`vim` and `nano` are available on the control host) create a new file called `gather_ios_data.yml`.

>Alternately, you can create it using sublimetext or any GUI editor on your laptop and scp it over)


>Ansible playbooks are **YAML** files. YAML is a structured encoding format that is also extremely human readable (unlike it's subset - the JSON format)

#### Step 2:
```
[student1@ansible networking-workshop]$ vim gather_ios_data.yml
```

Enter the following play definition into `gather_ios_data.yml`:

>Press the letter "i" to enter insert mode*

``` yaml
---
- name: GATHER INFORMATION FROM ROUTERS
  hosts: cisco
  connection: network_cli
  gather_facts: no
```

`---` indicates that this is a YAML file. We are running this playbook against the group `cisco`, that was defined earlier in the inventory file. Playbooks related to network devices should use the connection plugin called `network_cli`. Ansible has different connection plugins that handle different connection interfaces. The `network_cli` plugin is written specifically for network equipment and handles things like ensuring a persistent SSH connection across multiple tasks.


#### Step 3

Next, add the first `task`. This task will use the `ios_facts` module to gather facts about each device in the group `cisco`.


``` yaml
---
- name: GATHER INFORMATION FROM ROUTERS
  hosts: cisco
  connection: network_cli
  gather_facts: no

  tasks:
    - name: GATHER ROUTER FACTS
      ios_facts:
```

>A play is a list of tasks. Modules are pre-written code that perform the task.



#### Step 4

Run the playbook - exit back into the command line of the control host and execute the following:

>Use the write/quit method in vim to save your playbook, i.e. Esc :wq!


```
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts gather_ios_data.yml

```

The output should look as follows.

```
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts gather_ios_data.yml

PLAY [GATHER INFORMATION FROM ROUTERS] ******************************************************************

TASK [GATHER ROUTER FACTS] ******************************************************************************
ok: [rtr1]
ok: [rtr4]
ok: [rtr3]
ok: [rtr2]

PLAY RECAP **********************************************************************************************
rtr1                       : ok=1    changed=0    unreachable=0    failed=0   
rtr2                       : ok=1    changed=0    unreachable=0    failed=0   
rtr3                       : ok=1    changed=0    unreachable=0    failed=0   
rtr4                       : ok=1    changed=0    unreachable=0    failed=0   

[student1@ansible networking-workshop]$


```


#### Step 5


The play ran successfully and executed against the 4 routers. But where is the output?! Re-run the playbook using the `-v` flag.

> Note: Ansible has increasing level of verbosity. You can use up to 4 "v's", -vvvv.


```
student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts gather_ios_data.yml  -v
Using /home/student1/.ansible.cfg as config file

PLAY [GATHER INFORMATION FROM ROUTERS] ******************************************************************

TASK [GATHER ROUTER FACTS] ******************************************************************************
ok: [rtr3] => {"ansible_facts": {"ansible_net_all_ipv4_addresses": ["10.100.100.3", "192.168.3.103", "172.16.235.46", "192.168.35.101", "10.3.3.103"], "ansible_net_all_ipv6_addresses": [], "ansible_net_filesystems": ["bootflash:"], "ansible_net_gather_subset": ["hardware", "default", "interfaces"], "ansible_net_hostname": "rtr3", "ansible_net_image": "boot:packages.conf", "ansible_net_interfaces": {"GigabitEthernet1": {"bandwidth": 1000000, "description": null, "duplex": "Full", "ipv4": [{"address": "172.16.235.46", "subnet": "16"}], "lineprotocol": "up ", "macaddress": "0e93.7710.e63c", "mediatype": "Virtual", "mtu": 1500, "operstatus": "up", "type": "CSR vNIC"}, "Loopback0": {"bandwidth": 8000000, "description": null, "duplex": null, "ipv4": [{"address": "192.168.3.103", "subnet": "24"}], "lineprotocol": "up ", "macaddress": "192.168.3.103/24", "mediatype": null, "mtu": 1514, "operstatus": "up", "type": null}, "Loopback1": {"bandwidth": 8000000, "description": null, "duplex": null, "ipv4": [{"address": "10.3.3.103", "subnet": "24"}], "lineprotocol": "up ", "macaddress": "10.3.3.103/24", "mediatype": null, "mtu": 1514, "operstatus": "up", "type": null}, "Tunnel0": {"bandwidth": 100, "description": null, "duplex": null, "ipv4": [{"address": "10.100.100.3", "subnet": "24"}]

.
.
.
.
.
<output truncated for readability>
```


> Note: The output returns key-value pairs that can then be used within the playbook for subsequent tasks. Also note that all variables that start with **ansible_** are automatically available for subsequent tasks within the play.


#### Step 6

Ansible allows you to limit the playbook execution to a subset of the devices declared in the group, against which the play is running against. This can be done using the `--limit` flag. Rerun the above task, limiting it first to `rtr1` and then to both `rtr1` and `rtr3`


```
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts gather_ios_data.yml  -v --limit rtr1
```


```
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts gather_ios_data.yml  -v --limit rtr1,rtr3

```





#### Step 7

Running a playbook in verbose mode is a good option to validate the output from a task. To work with the variables within a playbook you can use the `debug` module.

Write 2 tasks that display the routers' OS version and serial number.

``` yaml
{%raw%}
---
- name: GATHER INFORMATION FROM ROUTERS
  hosts: cisco
  connection: network_cli
  gather_facts: no

  tasks:
    - name: GATHER ROUTER FACTS
      ios_facts:

    - name: DISPLAY VERSION
      debug:
        msg: "The IOS version is: {{ ansible_net_version }}"

    - name: DISPLAY SERIAL NUMBER
      debug:
        msg: "The serial number is:{{ ansible_net_serialnum }}"
{%endraw%}        
```


#### Step 8

Now re-run the playbook but this time do not use the `verbose` flag and run it against all hosts.

```

[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts gather_ios_data.yml

PLAY [GATHER INFORMATION FROM ROUTERS] ******************************************************************

TASK [GATHER ROUTER FACTS] ******************************************************************************
ok: [rtr4]
ok: [rtr1]
ok: [rtr2]
ok: [rtr3]

TASK [DISPLAY VERSION] **********************************************************************************
ok: [rtr4] => {
    "msg": "The IOS version is: 16.08.01a"
}
ok: [rtr1] => {
    "msg": "The IOS version is: 16.08.01a"
}
ok: [rtr2] => {
    "msg": "The IOS version is: 16.08.01a"
}
ok: [rtr3] => {
    "msg": "The IOS version is: 16.08.01a"
}

TASK [DISPLAY SERIAL NUMBER] ****************************************************************************
ok: [rtr1] => {
    "msg": "The serial number is:96F0LYYKYUZ"
}
ok: [rtr4] => {
    "msg": "The serial number is:94KZZ28ZT1Y"
}
ok: [rtr2] => {
    "msg": "The serial number is:9VBX7BSSLGS"
}
ok: [rtr3] => {
    "msg": "The serial number is:9OLKU6JWXRP"
}

PLAY RECAP **********************************************************************************************
rtr1                       : ok=3    changed=0    unreachable=0    failed=0   
rtr2                       : ok=3    changed=0    unreachable=0    failed=0   
rtr3                       : ok=3    changed=0    unreachable=0    failed=0   
rtr4                       : ok=3    changed=0    unreachable=0    failed=0   

[student1@ansible networking-workshop]$

```


Using less than 20 lines of "code" you have just automated version and serial number collection. Imagine if you were running this against your production network! You have actionable data in hand that does not go out of date.

# Complete

You have completed lab exercise 1.1

---
[Click Here to return to the Ansible Linklight - Networking Workshop](../../README.md)
