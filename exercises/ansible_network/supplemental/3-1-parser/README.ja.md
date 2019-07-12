# Exercise 3.1 - コマンドパーザーを使って動的なドキュメントを生成する

CLIベースのネットワーク装置でほとんどで `show` コマンドがサポートされています。その出力結果は実にさまざまな種類があります。人間が読みやすい綺麗な形式で表示されます。自動化ツールでは、その表示結果をマシン(コード)が処理しやすいようにデータ変換しなければなりません。コマンド結果を「構造化データ」に変換する必要があります。言い換えればコードやマシンが処理できるようにデータ形式を指示する必要があります。また、マシンにはリスト型、辞書型、配列型などの形式があります。

Ansible の [network-engine](https://github.com/ansible-network/network-engine) は、`command_parser` と `textfsm_parser` の2つトランスレーターをサポートする [role](https://docs.ansible.com/ansible/2.5/user_guide/playbooks_reuse_roles.html) です。`network-engine` ロールで、これら生のテキスト入力(さまざまな形式で表現されたもの）と入力データとして取り、構造化データへ変換してくれます。次の各セクションで、これらをそれぞれ使用してダイナミックレポートを生成します。

# ネットワーク装置からの非構造なコマンド出力

こちらは Cisco IOS 上で実行された `show interfaces` コマンドの出力です。

``` shell
rtr2#show interfaces
GigabitEthernet1 is up, line protocol is up
  Hardware is CSR vNIC, address is 0e56.1bf5.5ee2 (bia 0e56.1bf5.5ee2)
  Internet address is 172.17.16.140/16
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive set (10 sec)
  Full Duplex, 1000Mbps, link type is auto, media type is Virtual
  output flow-control is unsupported, input flow-control is unsupported
  ARP type: ARPA, ARP Timeout 04:00:00
  Last input 00:00:00, output 00:00:00, output hang never
  Last clearing of "show interface" counters never
  Input queue: 0/375/0/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: fifo
  Output queue: 0/40 (size/max)
  5 minute input rate 1000 bits/sec, 1 packets/sec
  5 minute output rate 1000 bits/sec, 1 packets/sec
     208488 packets input, 22368304 bytes, 0 no buffer
     Received 0 broadcasts (0 IP multicasts)
     0 runts, 0 giants, 0 throttles
     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
     0 watchdog, 0 multicast, 0 pause input
     250975 packets output, 40333671 bytes, 0 underruns
     0 output errors, 0 collisions, 1 interface resets
     0 unknown protocol drops
     0 babbles, 0 late collision, 0 deferred
     0 lost carrier, 0 no carrier, 0 pause output
     0 output buffer failures, 0 output buffers swapped out
Loopback0 is up, line protocol is up
  Hardware is Loopback
  Internet address is 192.168.2.102/24
  MTU 1514 bytes, BW 8000000 Kbit/sec, DLY 5000 usec,
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation LOOPBACK, loopback not set
  Keepalive set (10 sec)

.
.
.
.
.
<output omitted for brevity>
```

実行したタスクで、インターフェースの状態が **up** 、MTU値の設定、また、インターフェースのタイプと説明が把握できます。ぞれぞれのネットワーク装置にログインし、上記のコマンドを実行して各種情報を収集することができます。あなたが管理するネットワーク上の150台のネットワーク装置に対して上記の作業を繰り返さなければならない状態を想像してみてください。それは退屈なタスクで多くの工数を消費することでしょう。

このラボでは、このシナリオを自動化するための方法を Ansible を使って学習します。

#### Step 1

新規に `interface_report.yml` というファイル名の Playbook を作成して始めていきましょう。まずは Playbook に次の行を加えてください。

{% raw %}
``` yaml
---
- name: GENERATE INTERFACE REPORT
  hosts: cisco
  gather_facts: no
  connection: network_cli

```
{% endraw %}


#### Step 2

次に Playbook に `ansible-network.network-engine` ロールを加えてみます。ロールは何も行いませんが、より高いレベルで Playbook の抽象化を行います。繰り返し書かれた特定のタスクを扱うために部品化された Playbook と考えてください。

最初にロールをインストールする必要があります。control node 上で次のコマンドを実行してロールをインストールします。

``` bash
[student1@ansible networking-workshop]$ ansible-galaxy install ansible-network.network-engine

```

`ansible-network.network-engine` ロールは、特に `command_parser` モジュールのために用意されています。これを自身の Playbook 中に記述することで後続のタスクの中で使うことができます。

{% raw %}
``` yaml
---
- name: GENERATE INTERFACE REPORT
  hosts: cisco
  gather_facts: no
  connection: network_cli

  roles:
    - ansible-network.network-engine

```
{% endraw %}


#### Step 3

これでタスクが追加できるようなりました。最初のタスクに追加して、次にすべてのルーターに対して `show interfaces` を実行し、その出力結果を変数に格納します。

{% raw %}
``` yaml
---
- name: GENERATE INTERFACE REPORT
  hosts: cisco
  gather_facts: no
  connection: network_cli

  roles:
    - ansible-network.network-engine

  tasks:
    - name: CAPTURE SHOW INTERFACES
      ios_command:
        commands:
          - show interfaces
      register: output

```
{% endraw %}

> この Playbook を実行する際に `-v` オプションをつけて実行すると、実際にネットワーク装置から出力されたコマンド結果を見ることができます。


#### Step 4

次のタスクは直前のタスクでネットワーク装置から得た生データを `command_parser` モジュールに渡します。このモジュールは生データと一緒にパーザーファイルを入力パラメータとして受け取ります。

> 注記: パーザーファイルは YAML ファイルです。Ansible Playbookと同様の構造で記述されています。

Playbook を次のように追記してください。

{% raw %}
``` yaml
---
- name: GENERATE INTERFACE REPORT
  hosts: cisco
  gather_facts: no
  connection: network_cli

  roles:
    - ansible-network.network-engine

  tasks:
    - name: CAPTURE SHOW INTERFACES
      ios_command:
        commands:
          - show interfaces
      register: output

    - name: PARSE THE RAW OUTPUT
      command_parser:
        file: "parsers/show_interfaces.yaml"
        content: "{{ output.stdout[0] }}"

```
{% endraw %}

このタスクについて、もう少し深く理解しましょう。`command_parser` は `parsers` ディレクトリの中にある `show_interfaces.yaml` と呼ばれるファイルを参照して処理します。このラボでは、パーザーファイルは受講者の環境に事前設置済みです。パーサーは、さまざまなネットワークプラットフォーム上の標準的な show コマンドの出力を処理するために書かれています。

> 多くのパーザーは Public Domain ライセンスの元に利用可能になっており、特定のユースケースが処理されていない場合にのみビルドする必要があります。

パーザーファイルの中身を見てみましょう。正規表現を使用して `show` コマンドの結果から関連するデータを収録し、それを `interface_facts` と呼ばれる変数に格納していることが分かるでしょう。

#### Step 5

`command_parser` によって返された内容を新しいタスクの中で使ってみます。

{% raw %}
``` yaml
---
- name: GENERATE INTERFACE REPORT
  hosts: cisco
  gather_facts: no
  connection: network_cli

  roles:
    - ansible-network.network-engine

  tasks:
    - name: CAPTURE SHOW INTERFACES
      ios_command:
        commands:
          - show interfaces
      register: output

    - name: PARSE THE RAW OUTPUT
      command_parser:
        file: "parsers/show_interfaces.yaml"
        content: "{{ output.stdout[0] }}"

    - name: DISPLAY THE PARSED DATA
      debug:
        var: interface_facts

```
{%endraw%}

#### Step 6

この Playbook を実行してください。今回の目的は、モジュールから返されたデータを見るだけなので、Playbook の実行対象を1台のルーターに制限します。

``` shell
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts interface_report.yml --limit rtr1

PLAY [GENERATE INTERFACE REPORT] ************************************************************************************************************************************************************

TASK [CAPTURE SHOW INTERFACES] **************************************************************************************************************************************************************
ok: [rtr1]

TASK [PARSE THE RAW OUTPUT] *****************************************************************************************************************************************************************
ok: [rtr1]

TASK [DISPLAY THE PARSED DATA] **************************************************************************************************************************************************************
ok: [rtr1] => {
    "interface_facts": [
        {
            "GigabitEthernet1": {
                "config": {
                    "description": null,
                    "mtu": 1500,
                    "name": "GigabitEthernet1",
                    "type": "CSR"
                }
            }
        },
        {
            "Loopback0": {
                "config": {
                    "description": null,
                    "mtu": 1514,
                    "name": "Loopback0",
                    "type": "Loopback"
                }
            }
        },
        {
            "Loopback1": {
                "config": {
                    "description": null,
                    "mtu": 1514,
                    "name": "Loopback1",
                    "type": "Loopback"
                }
            }
        },
        {
            "Tunnel0": {
                "config": {
                    "description": null,
                    "mtu": 9976,
                    "name": "Tunnel0",
                    "type": "Tunnel"
                }
            }
        },
        {
            "Tunnel1": {
                "config": {
                    "description": null,
                    "mtu": 9976,
                    "name": "Tunnel1",
                    "type": "Tunnel"
                }
            }
        },
        {
            "VirtualPortGroup0": {
                "config": {
                    "description": null,
                    "mtu": 1500,
                    "name": "VirtualPortGroup0",
                    "type": "Virtual"
                }
            }
        }
    ]
}

PLAY RECAP **********************************************************************************************************************************************************************************
rtr1                       : ok=3    changed=0    unreachable=0    failed=0   

[student1@ansible networking-workshop]$

```

なんと素晴らしい事でしょう！実行した Playbook の中で実行されたコマンドの生のテキスト出力が構造化データになっていますね。あなたがレポートを作るために必要な要素が辞書型のリストになっているのが分かると思います。


#### Step 7

次にデバイスごとのレポートのためにディレクトリを作成します。

``` shell
[student1@ansible networking-workshop]$ mkdir intf_reports

```

#### Step 8
次の Step では template モジュールを使って上記のデータからレポートを生成してみます。前のラボで学習した同じテクニックを使用してネットワーク装置ごとのレポートを生成し、assemble モジュールを使用してレポートを結合します。

{% raw %}
``` yaml
---
- name: GENERATE INTERFACE REPORT
  hosts: cisco
  gather_facts: no
  connection: network_cli

  roles:
    - ansible-network.network-engine

  tasks:
    - name: CAPTURE SHOW INTERFACES
      ios_command:
        commands:
          - show interfaces
      register: output

    - name: PARSE THE RAW OUTPUT
      command_parser:
        file: "parsers/show_interfaces.yaml"
        content: "{{ output.stdout[0] }}"

    #- name: DISPLAY THE PARSED DATA
    #  debug:
    #    var: interface_facts

    - name: GENERATE REPORT FRAGMENTS
      template:
        src: interface_facts.j2
        dest: intf_reports/{{inventory_hostname}}_intf_report.md

    - name: GENERATE A CONSOLIDATED REPORT
      assemble:
        src: intf_reports/
        dest: interfaces_report.md
      delegate_to: localhost
      run_once: yes

```
{% endraw %}

> 注記: このラボでは Jinja2 テンプレートが受講者の環境に事前設置済みです。**templates** ディレクトリ の中にある **interface_facts.j2** がテンプレートです。

> 注記: debug タスクがコメントアウトされ、表示が簡潔になりました。

#### Step 9

Playbook の実行結果は以下のとおりです。

``` shell
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts interface_report.yml

PLAY [GENERATE INTERFACE REPORT] ************************************************************************************************************************************************************

TASK [CAPTURE SHOW INTERFACES] **************************************************************************************************************************************************************
ok: [rtr1]
ok: [rtr3]
ok: [rtr4]
ok: [rtr2]

TASK [PARSE THE RAW OUTPUT] *****************************************************************************************************************************************************************
ok: [rtr3]
ok: [rtr2]
ok: [rtr1]
ok: [rtr4]

TASK [GENERATE REPORT FRAGMENTS] ************************************************************************************************************************************************************
changed: [rtr4]
changed: [rtr2]
changed: [rtr3]
changed: [rtr1]

TASK [GENERATE A CONSOLIDATED REPORT] *******************************************************************************************************************************************************
changed: [rtr3]
ok: [rtr1]
ok: [rtr4]
ok: [rtr2]

PLAY RECAP **********************************************************************************************************************************************************************************
rtr1                       : ok=4    changed=1    unreachable=0    failed=0   
rtr2                       : ok=4    changed=1    unreachable=0    failed=0   
rtr3                       : ok=4    changed=2    unreachable=0    failed=0   
rtr4                       : ok=4    changed=1    unreachable=0    failed=0   

```

#### Step 10

`cat` コマンドを使って最終的に作成されたレポートファイルを確認してみましょう。

``` shell
[student1@ansible networking-workshop]$ cat interfaces_report.md
RTR1
----
GigabitEthernet1:
  Description:
  Name: GigabitEthernet1
  MTU: 1500

Loopback0:
  Description:
  Name: Loopback0
  MTU: 1514

Loopback1:
  Description:
  Name: Loopback1
  MTU: 1514

Tunnel0:
  Description:
  Name: Tunnel0
  MTU: 9976

Tunnel1:
  Description:
  Name: Tunnel1
  MTU: 9976

VirtualPortGroup0:
  Description:
  Name: VirtualPortGroup0
  MTU: 1500

RTR2
----
GigabitEthernet1:
  Description:
  Name: GigabitEthernet1
  MTU: 1500

Loopback0:
  Description:
  Name: Loopback0
  MTU: 1514

Loopback1:
  Description:
  Name: Loopback1
  MTU: 1514
.
.
.
.
.
<output omitted for brevity>
```

# Complete

ラボの Exercise 3.1 は、これで完了です。

---
[Ansible Linklight - Networking Workshop に戻るにはクリックしてください](../../README.ja.md)
