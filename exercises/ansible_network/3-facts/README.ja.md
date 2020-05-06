# Exercise 3: Ansible Facts の利用

**別の言語で読む**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
- [Takeaways](#takeaways)
- [Solution](#solution)

# Objective

ネットワーク機器に対する Ansible facts の利用を説明します。

Ansible facts はリモートのネットワーク構成要素から取得される情報です。Ansible facts は利用が容易な構造化(JSON)されたデータを返します。例えば、Ansible Facts と Template 機能を使うと迅速にMarkdownやHTML形式の監査レポートを作成することが可能です。

この演習は以下を含みます。:
- Playbookをスクラッチから作成します。
- [ansible-doc](https://docs.ansible.com/ansible/latest/cli/ansible-doc.html) の利用
- [ios_facts モジュール](https://docs.ansible.com/ansible/latest/modules/ios_facts_module.html) の利用
- [debug モジュール](https://docs.ansible.com/ansible/latest/modules/debug_module.html) の利用。

#### Step 1

コントローラーノード上で `ios_facts` モジュールと `debug` モジュールのドキュメントを確認します。

```bash
[student1@ansible network-workshop]$ ansible-doc debug
```

`debug` を任意のパラメーター無しで利用するとどうなるか確認してください。

```bash
[student1@ansible network-workshop]$ ansible-doc ios_facts
```

収集する Facts 情報に制限を書ける方法を確認してください。


#### Step 2:

Playbooks は [**YAML**](https://yaml.org/) 形式です。YAML は構造化されたフォーマットで可読性に優れます（JSON と違って）

好きなエディタを使って新しいファイル `facts.yml` を作成してください (`vim` と `nano` がコントローラーホストで利用可能です) :

```
[student1@ansible network-workshop]$ vim facts.yml
```

`facts.yml` に以下の Play 定義を入力します:

```yaml
---
- name: gather information from routers
  hosts: cisco
  gather_facts: no
```

各行の意味:
- 1行目の `---` は、これが YAML ファイルであることを示します。
- `- name:` キーはこのPlaybookの説明を記述しています。
- `hosts:` キーは、このPlaybookがインベントリーファイル内の `cisco` グループを対象することを意味します。
- `gather_facts: no` は Ansible 2.8 か以前のバージョンから必要となります。自動で Fact を収集する機能ですが、この機能は Linux ホストのみで利用可能で、ネットワーク環境では利用できません。ネットワーク環境では別の方法で Facts の収集を行います。


#### Step 3

次に最初の `task` を追加します。このタスクでは `cisco` グループ内の各デバイスから `ios_facts` モジュールを使って Facts を収集します。


```yaml
---
- name: gather information from routers
  hosts: cisco
  gather_facts: no

  tasks:
    - name: gather router facts
      ios_facts:
```

>play は task のリストです。モジュールは事前に準備されたプログラムでタスクから実行されます。

#### Step 4

この Playbook を実行します:

```
[student1@ansible network-workshop]$ ansible-playbook facts.yml
```

出力は以下のようになるはずです。

```bash
[student1@ansible network-workshop]$ ansible-playbook facts.yml

PLAY [gather information from routers] *****************************************

TASK [gather router facts] *****************************************************
ok: [rtr1]

PLAY RECAP ******************************************************************************************************************
rtr1                       : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```


#### Step 5

この play は Cisco ルーターに対して実行されて成功したはずです。しかし、出力はどこへ行ったのでしょうか？この playbook を冗長出力モードの `-v` オプションをつけて再実行してください。


```
[student1@ansible network-workshop]$ ansible-playbook facts.yml -v
Using /home/student1/.ansible.cfg as config file

PLAY [gather information from routers] *****************************************

TASK [gather router facts] *****************************************************
ok: [rtr1] => changed=false
  ansible_facts:
    ansible_net_all_ipv4_addresses:
    - 192.168.35.101
    - 172.16.129.86
    - 192.168.1.101
    - 10.1.1.101
    - 10.200.200.1
    - 10.100.100.1
.
.
 <output truncated for readability>
.
.
    ansible_net_iostype: IOS-XE
    ansible_net_memfree_mb: 1853993
    ansible_net_memtotal_mb: 2180495
    ansible_net_neighbors: {}
    ansible_net_python_version: 2.7.5
    ansible_net_serialnum: 91Y8URJWFPU
    ansible_net_system: ios
    ansible_net_version: 16.09.02
    discovered_interpreter_python: /usr/bin/python

PLAY RECAP *********************************************************************
rtr1                       : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```


> Note: 出力は後続のタスクで使用できる key-value のペアで返されます。ここで取得された **ansible_** で始まる全ての変数は、同じ play 内の後続のタスクで自動的に利用可能になります。

#### Step 6

Playbook を冗長モードで実行するのは変数を確認するのに便利です。変数をPlaybookで利用するには `debug` モジュールが利用できます。

2つのタスクを追加し、ルーターのOSバージョンとシリアルナンバーを表示します。

<!-- {% raw %} -->
``` yaml
---
- name: gather information from routers
  hosts: cisco
  gather_facts: no

  tasks:
    - name: gather router facts
      ios_facts:

    - name: display version
      debug:
        msg: "The IOS version is: {{ ansible_net_version }}"

    - name: display serial number
      debug:
        msg: "The serial number is:{{ ansible_net_serialnum }}"
```
<!-- {% endraw %} -->


#### Step 8

では `冗長出力モード` オプションを利用せずに、再度Playbookを実行します:

```
[student1@ansible network-workshop]$ ansible-playbook facts.yml

PLAY [gather information from routers] **************************************************************************************

TASK [gather router facts] **************************************************************************************************
ok: [rtr1]

TASK [display version] ******************************************************************************************************
ok: [rtr1] =>
  msg: 'The IOS version is: 16.09.02'

TASK [display serial number] ************************************************************************************************
ok: [rtr1] =>
  msg: The serial number is:91Y8URJWFPU

PLAY RECAP ******************************************************************************************************************
rtr1                       : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```


20行以下の "code" を使ってバージョンとシリアルナンバーの収集を自動化しました。このPlaybookを本番ネットワークに対して実行することを想像してください。古くなったデータではなく、最新の利用可能なデータを入手することができます。

# Takeaways

- [ansible-doc](https://docs.ansible.com/ansible/latest/cli/ansible-doc.html) コマンドはインターネット接続なしにドキュメントを確認できます。このドキュメントはコントローラーノードのAnsibleバージョンと同じです。
- [ios_facts モジュール](https://docs.ansible.com/ansible/latest/modules/ios_config_module.html) は Cisco IOS から構造化されたデータを収集します。それぞれのネットワークプラットフォームごとに関連するモジュールがあります。例えば、 `junos_fact` は Juniper Junos のためのモジュールで、`eos_fact` は Arista EOS用です。
- [debug モジュール](https://docs.ansible.com/ansible/latest/modules/debug_module.html) はPlaybookから端末に値を表示することができます。


# Solution

完成したPlaybookはここから参照できます: [facts.yml](facts.yml).

---

# Complete

以上で exercise 3 は終了です。

[Click here to return to the Ansible Network Automation Workshop](../README.ja.md)
