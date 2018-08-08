# Lab 4: Using Ansible to collect and report router information


In this lab you will learn how to use the `template` module to pass collected data from devices to a Jinja2 template. The template module then renders the output as a `markdown` file.



#### Step 1

Create a new playbook called `router_report.yml` and add the following play definition to it:


``` yaml
---
- name: GENERATE OS REPORT FROM ROUTERS
  hosts: cisco
  connection: network_cli
  gather_facts: no
```


#### Step 2

Add a task that collects the facts using the `ios_facts` module. Recollect that we used this module in an earlier lab.


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

> Recall that the **facts** modules automatically populate the **ansible_net_version** and **ansible_net_serial_number** variables within the play. You can validate this by running the playbook in verbose mode.




#### Step 3

Rather than using debug or verbose mode to display the output on the screen, go ahead and add a new task using the template module as follows:


``` yaml
---
- name: GATHER INFORMATION FROM ROUTERS
  hosts: cisco
  connection: network_cli
  gather_facts: no

  tasks:
    - name: GATHER ROUTER FACTS
      ios_facts:

    - name: RENDER FACTS AS A REPORT
      template:
        src: os_report.j2
        dest: reports/{{ inventory_hostname }}.md
```


Let's break this task down a bit. The `template` module has a `src` parameter that has a value of `os_report.j2`. In the next few steps, we will create this file. This will be the Jinja2 template,  used to generate the desired report. The `dest` parameter specifies the destination file name to render the report into.


#### Step 4
In the previous step we are rendering the generated report into a directory called `reports`. Go ahead and create this directory.



``` shell
[student1@ip-172-16-208-140 networking-workshop]$ mkdir reports
[student1@ip-172-16-208-140 networking-workshop]$
```



#### Step 5


The next step is to create a Jinja2 template. Ansible will look for the template file in the current working directory and within a directory called `templates` automatically. Convention/best-practice is to create the template file within the template directory.

Using `vi`, `nano` or another text editor, go ahead and create a new file called `os_report.j2` under the `templates` directory. Add the following into the template file:


{%raw%}
``` python


{{ inventory_hostname.upper() }}
---
{{ ansible_net_serialnum }} : {{ ansible_net_version }}



```
{%endraw%}  
This file simply contains some of the variables we have been using in our playbooks until now.

> Note: Python inbuilt methods for datatypes are available natively in Jinja2 making it very easy to manipulate the formatting etc.


#### Step 6

With this in place, go ahead and run the playbook:

``` shell
[student1@ip-172-16-208-140 networking-workshop]$ ansible-playbook -i lab_inventory/hosts router_report.yml

PLAY [GATHER INFORMATION FROM ROUTERS] ******************************************************************************************************************************************************

TASK [GATHER ROUTER FACTS] ******************************************************************************************************************************************************************
ok: [rtr4]
ok: [rtr3]
ok: [rtr2]
ok: [rtr1]

TASK [RENDER FACTS AS A REPORT] *************************************************************************************************************************************************************
changed: [rtr4]
changed: [rtr2]
changed: [rtr3]
changed: [rtr1]

PLAY RECAP **********************************************************************************************************************************************************************************
rtr1                       : ok=2    changed=1    unreachable=0    failed=0   
rtr2                       : ok=2    changed=1    unreachable=0    failed=0   
rtr3                       : ok=2    changed=1    unreachable=0    failed=0   
rtr4                       : ok=2    changed=1    unreachable=0    failed=0   

[student1@ip-172-16-208-140 networking-workshop]$

```


#### Step 7

After the playbook run, you should see the following files appear in the reports directory:


``` shell
reports/
├── rtr1.md
├── rtr2.md
├── rtr3.md
└── rtr4.md

0 directories, 4 files

```

The contents of one of them for example:

``` shell
[student1@ip-172-16-208-140 networking-workshop]$ cat reports/rtr4.md


RTR4
---
9TCM27U9TQG : 16.08.01a

[student1@ip-172-16-208-140 networking-workshop]$
```


#### Step 8


While it is nice to have the data, it would be even better to consolidate all these individual router reports into a single document. Let's add a new task to do that



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

    - name: RENDER FACTS AS A REPORT
      template:
        src: os_report.j2
        dest: reports/{{ inventory_hostname }}.md

    - name: CONSOLIDATE THE IOS DATA
      assemble:
        src: reports/
        dest: network_os_report.md
      delegate_to: localhost
      run_once: yes
{%endraw%}
```


Here we are using the `assemble` module. The `src` parameter specifies the directory that contain file fragments that need to be consolidated and the `dest` parameter provides the file to render the fragments into.

> Note: The **delegate_to** can be used to specify tasks that need to be executed locally. The **run_once** directive will ensure that the given task is executed only once.




#### Step 9

Go ahead and run the playbook.

``` shell
[student1@ip-172-16-208-140 networking-workshop]$ ansible-playbook -i lab_inventory/hosts router_report.yml

PLAY [GATHER INFORMATION FROM ROUTERS] ******************************************************************************************************************************************************

TASK [GATHER ROUTER FACTS] ******************************************************************************************************************************************************************
ok: [rtr2]
ok: [rtr4]
ok: [rtr1]
ok: [rtr3]

TASK [RENDER FACTS AS A REPORT] *************************************************************************************************************************************************************
ok: [rtr3]
ok: [rtr2]
ok: [rtr1]
ok: [rtr4]

TASK [CONSOLIDATE THE IOS DATA] *************************************************************************************************************************************************************
changed: [rtr1 -> localhost]

PLAY RECAP **********************************************************************************************************************************************************************************
rtr1                       : ok=3    changed=1    unreachable=0    failed=0   
rtr2                       : ok=2    changed=0    unreachable=0    failed=0   
rtr3                       : ok=2    changed=0    unreachable=0    failed=0   
rtr4                       : ok=2    changed=0    unreachable=0    failed=0   

[student1@ip-172-16-208-140 networking-workshop]$

```



#### Step 10

A new file called `network_os_report.md` will now be available in the playbook root. Use the `cat` command to view it's contents:


``` shell
[student1@ip-172-16-208-140 networking-workshop]$ cat network_os_report.md


RTR1
---
9YJXS2VD3Q7 : 16.08.01a



RTR2
---
9QHUCH0VZI9 : 16.08.01a



RTR3
---
9ZGJ5B1DL14 : 16.08.01a



RTR4
---
9TCM27U9TQG : 16.08.01a

[student1@ip-172-16-208-140 networking-workshop]$

```

> Note: Markdown files can be rendered visually as HTML

At this point, with 3 small tasks, you have an OS report on all the IOS devices in your network. This is a simple example but the principle remains as you expand upon the capabilities.  For example, you can build status reports and dashboards that rely on the output of device show commands.

Ansible provides the tools and methods to extend network automation beyond configuration management to more robust capabilities, such as, generating documentation and or reports.
