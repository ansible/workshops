# Exercise 1.2 - Module documentation, Registering output & tags

前のセクションでは、`ios_facts` と `debug` の使い方を学びました。  
`debug` モジュールの使い方では、 `msg` と呼ばれるパラメータを設定しましたが、`ios_facts`モジュールについては特にそのようなものを設定しませんでした。  
これらのモジュールに設定できるパラメータについて知りたいと思った場合、どうすれば良いでしょうか？

解決するためには、2つのオプションがあります。

- 1.  https://docs.ansible.com へアクセスし、Network Moduleについてのドキュメントを確認することができます。

- 2. コマンドラインから、`ansible-doc <module-name>`コマンドを実行し、ドキュメントを確認することができます。


#### Step 1
コントロールホスト上で、ドキュメントを確認してみましょう。  
この演習で確認するドキュメントは、`debug`モジュールと `ios_facts`モジュールです。


```
[student1@ansible networking-workshop]$ ansible-doc debug

```

`debug`モジュールを、何もオプションを指定せずに実行した場合に何が起こるかをドキュメント上で確認してみてください。

```
[student1@ansible networking-workshop]$ ansible-doc ios_facts

```

factsの取得を制限したい場合、どうすれば良いでしょうか？
ドキュメント上で確認してみてください。


#### Step 2
前のセクションでは、`ios_facts`モジュールを用いてデバイスの詳細を取得する方法を学習しました。  
`ios_facts`モジュールでは取得ができない情報があった場合、`ios_command`モジュールを利用することで、手動オペレーションと同様`show`コマンドの結果から取得することができます。  

この演習を進めることで、_show_ コマンドの実行結果から、**hostname**と`show ip interface brief`の出力結果を自動収集する方法を学びましょう。


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


    - name: COLLECT OUTPUT OF SHOW COMMANDS
      ios_command:
        commands:
          - show run | i hostname
          - show ip interface brief
{%endraw%}
```

> Note: **commands** is a parameter required by the **ios_module**. The input to this parameter is a "list" of IOS commands.



#### Step 3

Before running the playbook, add a `tag` to the last task. Name it "show"

> Tags can be added to tasks, plays or roles within a playbook. You can assign one or more tags to any given task/play/role. Tags allow you to selectively run parts of the playbook.





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


    - name: COLLECT OUTPUT OF SHOW COMMANDS
      ios_command:
        commands:
          - show run | i hostname
          - show ip interface brief
      tags: show

{%endraw%}
```


#### Step 4

Selectively run the last task within the playbook using the `--tags` option:

```
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts gather_ios_data.yml --tags=show

PLAY [GATHER INFORMATION FROM ROUTERS] **************************************************************************

TASK [COLLECT OUTPUT OF SHOW COMMANDS] **************************************************************************
ok: [rtr2]
ok: [rtr3]
ok: [rtr1]
ok: [rtr4]

PLAY RECAP ******************************************************************************************************
rtr1                       : ok=1    changed=0    unreachable=0    failed=0   
rtr2                       : ok=1    changed=0    unreachable=0    failed=0   
rtr3                       : ok=1    changed=0    unreachable=0    failed=0   
rtr4                       : ok=1    changed=0    unreachable=0    failed=0   

[student1@ansible networking-workshop]$

```

Note 2 important points here.

1. Only a single task was executed during the playbook run (You no longer can see the serial number and IOS version being displayed)

2. The output of the show commands is not being displayed.


#### Step 5

Re-run the playbook using the `-v` verbose flag to see the output coming back from the routers.

```
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts gather_ios_data.yml --tags=show -v

```

#### Step 6

With the `ios_facts` module, the output was automatically assigned to the `ansible_*` variables. For any of the ad-hoc commands we run against remote devices, the output has to be "registered" to a variable in order to use it within the playbook. Go ahead and add the `register` directive to collect the output of the show commands into a variable called `show_output`:


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

    - name: COLLECT OUTPUT OF SHOW COMMANDS
      ios_command:
        commands:
          - show run | i hostname
          - show ip interface brief
      tags: show
      register: show_output
{%endraw%}

```

#### Step 7


Add a task to use the `debug` module to display the content's of the `show_output` variable. Tag this task as "show" as well.



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

    - name: COLLECT OUTPUT OF SHOW COMMANDS
      ios_command:
        commands:
          - show run | i hostname
          - show ip interface brief
      tags: show
      register: show_output

    - name: DISPLAY THE COMMAND OUTPUT
      debug:
        var: show_output
      tags: show
{%endraw%}
```

> Note the use of **var** vs **msg** for the debug module.




#### Step 8

Re-run the playbook to execute only the tasks that have been tagged. This time run the playbook without the `-v` flag.


```
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts gather_ios_data.yml --tags=show

PLAY [GATHER INFORMATION FROM ROUTERS] **************************************************************************

TASK [COLLECT OUTPUT OF SHOW COMMANDS] **************************************************************************
ok: [rtr4]
ok: [rtr1]
ok: [rtr3]
ok: [rtr2]

TASK [DISPLAY THE COMMAND OUTPUT] *******************************************************************************
ok: [rtr4] => {
    "show_output": {
        "changed": false,
        "failed": false,
        "stdout": [
            "hostname rtr4",
            "Interface              IP-Address      OK? Method Status                Protocol\nGigabitEthernet1       172.17.231.181  YES DHCP   up                    up      \nLoopback0              192.168.4.104   YES manual up                    up      \nLoopback1              10.4.4.104      YES manual up                    up      \nTunnel0                10.101.101.4    YES manual up                    up      \nVirtualPortGroup0      192.168.35.101  YES TFTP   up                    up"
        ],
        "stdout_lines": [
            [
                "hostname rtr4"
            ],
            [
                "Interface              IP-Address      OK? Method Status                Protocol",
                "GigabitEthernet1       172.17.231.181  YES DHCP   up                    up      ",
                "Loopback0              192.168.4.104   YES manual up                    up      ",
                "Loopback1              10.4.4.104      YES manual up                    up      ",
                "Tunnel0                10.101.101.4    YES manual up                    up      ",
                "VirtualPortGroup0      192.168.35.101  YES TFTP   up                    up"
            ]
        ]
    }
}
ok: [rtr1] => {
    "show_output": {
        "changed": false,
.
.
.
.
.
<output omitted for brevity>
```
#### Step 9

The `show_output` variable can now be parsed just like a `Python` dictionary. It contains a "key" called `stdout`. `stdout` is a list object, and will contain exactly as many elements as were in the input to the `commands` parameter of the `ios_command` task. This means `show_output.stdout[0]` will contain the output of the `show running | i hostname` command and `show_output.stdout[1]` will contain the output of `show ip interface brief`.

Write a new task to display only the hostname using a debug command:



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

    - name: COLLECT OUTPUT OF SHOW COMMANDS
      ios_command:
        commands:
          - show run | i hostname
          - show ip interface brief
      tags: show
      register: show_output

    - name: DISPLAY THE COMMAND OUTPUT
      debug:
        var: show_output
      tags: show

    - name: DISPLAY THE HOSTNAME
      debug:
        msg: "The hostname is {{ show_output.stdout[0] }}"
      tags: show
{%endraw%}
```

#### Step 10

Re-run the playbook.


``` yaml
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts gather_ios_data.yml --tags=show

PLAY [GATHER INFORMATION FROM ROUTERS] **************************************************************************

TASK [COLLECT OUTPUT OF SHOW COMMANDS] **************************************************************************
ok: [rtr2]
ok: [rtr4]
ok: [rtr1]
ok: [rtr3]

TASK [DISPLAY THE COMMAND OUTPUT] *******************************************************************************
ok: [rtr2] => {
    "show_output": {
        "changed": false,
        "failed": false,
        "stdout": [
.
.
.
.
.
<output omitted for brevity>
.
.
.
TASK [DISPLAY THE HOSTNAME] *************************************************************************************
ok: [rtr2] => {
    "msg": "The hostname is hostname rtr2"
}
ok: [rtr1] => {
    "msg": "The hostname is hostname rtr1"
}
ok: [rtr3] => {
    "msg": "The hostname is hostname rtr3"
}
ok: [rtr4] => {
    "msg": "The hostname is hostname rtr4"
}

PLAY RECAP ******************************************************************************************************
rtr1                       : ok=3    changed=0    unreachable=0    failed=0   
rtr2                       : ok=3    changed=0    unreachable=0    failed=0   
rtr3                       : ok=3    changed=0    unreachable=0    failed=0   
rtr4                       : ok=3    changed=0    unreachable=0    failed=0   

[student1@ansible networking-workshop]$


```

# Complete

You have completed lab exercise 1.2

---
[Click Here to return to the Ansible Linklight - Networking Workshop](../../README.md)
