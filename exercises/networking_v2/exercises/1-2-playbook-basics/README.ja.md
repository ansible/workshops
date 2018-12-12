# Exercise 1.2 - Moduleのドキュメントの確認方法、 出力結果の登録方法、 tagの使い方

前のセクションでは、`ios_facts` と `debug` の使い方を学びました。
`debug` モジュールの使い方では、 `msg` と呼ばれるパラメータを設定しましたが、`ios_facts`モジュールについては特にそのようなものを設定しませんでした。
これらのモジュールに設定できるパラメータについて知りたいと思った場合、どうすれば良いでしょうか？

解決するためには、2つのオプションがあります。

1.  https://docs.ansible.com へアクセスし、Network Moduleについてのドキュメントを確認することができます。
1. コマンドラインから、`ansible-doc <module-name>`コマンドを実行し、ドキュメントを確認することができます。


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

factsの取得を制限したい場合、どうすれば良いでしょうか？答えはドキュメント上で確認してみてください。


#### Step 2
前のセクションでは、`ios_facts`モジュールを用いてデバイスの詳細を取得する方法を学習しました。
`ios_facts`モジュールでは取得ができない情報があった場合、`ios_command`モジュールを利用することで、手動オペレーションと同様`show`コマンドの結果から取得することができます。

この演習を進めて、_show_ コマンドの実行結果から、**hostname**と`show ip interface brief`の出力結果を自動収集する方法を学びましょう。

```
[student1@ansible networking-workshop]$ vim gather_ios_data.yml
```

{%raw%}
``` yaml
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
```
{%endraw%}

> Note: **commands** 以下は、**ios_module**が必要とするパラメータを入力します。
パラメータとして入力する値は、"list"形式で記述されるIOS コマンドとなります。


#### Step 3

playbookを実行する前に、最後のtaskへ`tag`を追加しましょう。
ここでは`show`と名前をつけます。

> Tagは、playbookの中でタスク、play、rolesに対して追加することができます。
> 1つもしくは複数のtagをtask/play/roleへ追加することができます。
> tagを指定してplaybookの一部だけを選択して実行することができるようになります。


{%raw%}
``` yaml
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
```
{%endraw%}


#### Step 4

部分的な実行を試してみましょう。
この機能を利用するには、`--tags`オプションをつけてplaybookを実行します。

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

2つの重要なポイントを記します。

1. playbookの実行中には、1つのタスクだけが実行されたはずです。(シリアル番号と、IOS Versionが表示されなくなったはずです。)

1. show commandの実行結果が、表示されていないはずです。


#### Step 5

playbookを `-v`オプション(vervose mode)をつけて再実行してみましょう。ルータに実行されたコマンドの出力結果が確認できます。

```
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts gather_ios_data.yml --tags=show -v
```

#### Step 6

`ios_facts`モジュールでは、取得された情報は自動的に`ansible_*`変数へ割り当てされていました。
それとは対照的にアドホックなコマンドを実行した際には出力結果が自動的になにがしかの変数に割当たることがないため、playbook内で利用するには任意の変数に登録(register)する必要があります。
先ほど作成したplaybookの中へ、`show_output`と定義した変数を追加し、showコマンドの出力結果を登録`register`する構文を追加してみましょう。

{%raw%}
``` yaml
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
```
{%endraw%}

#### Step 7

`debug` モジュールを用いて、先ほど作成した`show_output`変数の内容を表示するタスクを追加してください。
また、このtaskにも"show"というtagを付与してください。


{%raw%}
``` yaml
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
```
{%endraw%}

>  debugモジュールにおける、**var** と **msg** の使い方に注意してください。



#### Step 8

playbookを再実行して、タグ付けしたタスクのみを実行します。
今回は、`-v`フラグを付けずにplaybookを実行します。


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

みなさんが作成し定義した`show_output` 変数は、`python dictionary`(辞書)と同じように構文解析を行うことができます。
それらは、通常 "key" と呼ばれる `stdout`(標準出力)を含みます。
`stdout`は、リスト型のオブジェクトで、`ios_command`タスクの`command`パラメータへの入力と同じだけの数の構成数になります。

つまり、
- `show_output.stdout[0]`は`show running | i hostname`コマンドの結果が格納され、
- `show_output.stdout[1]`は、 `show ip interface brief`の結果が格納される、
ということです。

debug コマンドを用いて hostname だけを表示する新しいtaskを追記してみましょう。


{%raw%}
``` yaml
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
```
{%endraw%}

#### Step 10

playbookを再実行してみましょう。


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

```

# Complete

お疲れ様でした。
以上でlab exercise 1.2 は終了です。

---
[ここをクリックすると Ansible Linklight - Networking Workshop へ戻ります](../../README.ja.md)
