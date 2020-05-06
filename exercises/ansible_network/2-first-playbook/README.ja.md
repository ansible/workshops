# Exercise 2 - 最初のPlaybook

**別の言語で読む**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
- [Takeaways](#takeaways)
- [Solution](#solution)

# Objective

ルーター設定の更新にAnsibleを利用します。この演習ではPlaybookは作成せずに、準備されたものを利用します。

この演習は以下を含みます。
- 既存のPlaybookを確認します。
- Playbook を `ansible-playbook` コマンドを使って実行します。
- check mode (`--check` オプション)
- verbose mode (`--verbose` or `-v` オプション)

# Guide

#### Step 1

`network-workshop` ディレクトリを移動してください（別のディレクトリにいる場合）

```bash
[student1@ansible ~]$ cd ~/network-workshop/
[student1@ansible network-workshop]$
[student1@ansible network-workshop]$ pwd
/home/student1/network-workshop
```

演習用に提供される `playbook.yml`を確認します。好きなエディタでこのファイルを開いてください。以下の例では `cat` コマンドを利用しています。

```
[student1@ansible network-workshop]$ cat playbook.yml
---
- name: snmp ro/rw string configuration
  hosts: cisco
  gather_facts: no

  tasks:

    - name: ensure that the desired snmp strings are present
      ios_config:
        commands:
          - snmp-server community ansible-public RO
          - snmp-server community ansible-private RW
```

 - `cat` - ファイルの内容を確認するコマンド
 - `playbook.yml` - 演習で提供されるPlaybook

次の演習でPlaybookの詳細については確認します。ここではこのPlaybookで2つのCisco IOS-XEコマンドが実行されることが確認できれば十分です。

```
snmp-server community ansible-public RO
snmp-server community ansible-private RW
```

#### Step 3

`ansible-playbook` コマンドを使ってこのPlaybookを実行します:

```bash
[student1@ansible network-workshop]$ ansible-playbook playbook.yml

PLAY [snmp ro/rw string configuration] *****************************************

TASK [ensure that the desired snmp strings are present] ************************
changed: [rtr1]

PLAY RECAP *********************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

#### Step 4

このPlaybookの動きを確認します。`rtr1`へログインし、Cisco IOS-XE上で実行中のコンフィグを確認します。

```bash
[student1@ansible network-workshop]$ ssh rtr1

rtr1#show run | i snmp
snmp-server community ansible-public RO
snmp-server community ansible-private RW
```


#### Step 5

`ios_config` モジュールは冪等性を持ちます。つまり、コンフィグの変更がエンドホストに存在しない場合にだけ、コンフィグがデバイスにプッシュされることを意味します。

>Ansible Automation の用語（冪等性のような単語）の説明が必要な場合は [glossary](https://docs.ansible.com/ansible/latest/reference_appendices/glossary.html) で確認することができます。

冪等性を確認するには、Playbookを再実行します:

```bash
[student1@ansible network-workshop]$  ansible-playbook playbook.yml

PLAY [snmp ro/rw string configuration] **************************************************************************************

TASK [ensure that the desired snmp strings are present] *********************************************************************
ok: [rtr1]

PLAY RECAP ******************************************************************************************************************
rtr1                       : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[student1@ansible network-workshop]$
```

> Note: **PLAY RECAP** の中の **changed** パラメーターが changed=0 であることを確認してください。

このPlaybookを複数回実行しても、結果は **ok=1** **change=0** と毎回同じになります。別のオペレーターやプロセスが rtr1 の設定を削除、変更をしない限り、このPlaybookはネットワークデバイス上で正しく設定が投入されていることを示す **ok=1** を通知し続けます。


#### Step 6

ここで `ansible-test` というコミュニティ名を追加するようにタスクを更新します。

```
snmp-server community ansible-test RO
```

好きなテキストエディタで `playbook.yml` を開いて、コマンドを追加します:

```bash
[student1@ansible network-workshop]$ nano playbook.yml
```

Playbookは以下のようになります:

``` yaml
---
- name: snmp ro/rw string configuration
  hosts: cisco
  gather_facts: no

  tasks:

    - name: ensure that the desired snmp strings are present
      ios_config:
        commands:
          - snmp-server community ansible-public RO
          - snmp-server community ansible-private RW
          - snmp-server community ansible-test RO
```

#### Step 7

ここでは、このPlaybookを実行してデバイスのコンフィグを更新する代わりに、`--check` オプションと `-v(--verbose)` の冗長出力モードを組み合わせて実行します。


```bash
[student1@ansible network-workshop]$ ansible-playbook playbook.yml --verbose --check
Using /home/student1/.ansible.cfg as config file

PLAY [snmp ro/rw string configuration] *****************************************

TASK [ensure that the desired snmp strings are present] ************************
changed: [rtr1] => changed=true
  ansible_facts:
    discovered_interpreter_python: /usr/bin/python
  banners: {}
  commands:
  - snmp-server community ansible-test RO
  updates:
  - snmp-server community ansible-test RO

PLAY RECAP *********************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

`--check` と `--verbose` を組み合わせると、実際にデバイス対して更新を行うことなく、どのような変更が行われるのかを確認することができます。これは、実際に更新を行う前に、変更内容を検証するのに最適な方法です。

#### Step 8

`ansible-test` コミュニティが作成されていないことを確認します。`rtr1` へログインして、コンフィグ内容を確認してください。

```bash
[student1@ansible network-workshop]$ ssh rtr1

rtr1#show run | i snmp
snmp-server community ansible-public RO
snmp-server community ansible-private RW
```


#### Step 9

最後に、このPlaybookを `-v` `--check` オプションなしで再実行して、更新をプッシュします。

```bash
[student1@ansible network-workshop]$ ansible-playbook playbook.yml

PLAY [snmp ro/rw string configuration] *****************************************

TASK [ensure that the desired snmp strings are present] ************************
changed: [rtr1]

PLAY RECAP ******************************************************************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

#### Step 10

Playbookが設定した `ansible-test` コミュニティを確認します。`rtr1` へログインして、コンフィグ内容を確認してください。

```bash
[student1@ansible network-workshop]$ ssh rtr1

rtr1#sh run | i snmp
snmp-server community ansible-public RO
snmp-server community ansible-private RW
snmp-server community ansible-test RO
```

# Takeaways

- ***os_config** (例えば ios_config) モジュールは冪等性を持ち、ステートフルです。
- **check mode** はリモートシステムを変更せずにPlaybookを確認できる。
- **verbose mode** は端末に多くの情報を表示し、そこにはどのようなコマンドが適用されるかが含まれている。
- Playbook は設定を強制するために **Red Hat Ansible Tower** からスケジュールすることが可能です。例えば、特定のネットワークに1日1回Playbookを実行するなどです。また **check mode** と組み合わせ利用すると、ネットワークの設定が変更されたり削除された場合に、それを確認したりレポートすることも可能になります。

# Solution

完成したPlaybookはここから参照できます: [playbook.yml](../playbook.yml).

---

# Complete

以上で exercise 2 は終了です。

[Click here to return to the Ansible Network Automation Workshop](../README.ja.md)
