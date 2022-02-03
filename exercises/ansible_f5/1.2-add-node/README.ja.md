# 演習 1.2 - F5 BIG-IP へのノードの追加

**他の言語でもお読みいただけます** :![uk](../../../images/uk.png) [English](README.md)、![japan](../../../images/japan.png) [日本語](README.ja.md).

## 目次

- [目的](#objective)  - [ガイド](#guide)  - [Playbook の出力](#playbook-output)  -
[ソリューション](#solution)  - [ソリューションの確認](#verifying-the-solution)

# 目的

[BIG-IP
ノードモジュール](https://docs.ansible.com/ansible/latest/modules/bigip_node_module.html)
を使用して、2 つの RHEL (Red Hat Enterprise Linux) Web サーバーを BIG-IP
ロードバランサーのノードとして追加する方法を説明します。

# ガイド

## ステップ 1:

VSCode を使用して、左側のペインの新規ファイルアイコンをクリックして、`bigip-node.yml` という名前の新しいファイルを作成します。

![picture of create file
icon](../1.1-get-facts/images/vscode-openfile_icon.png)


## ステップ 2:

次のプレイ定義を `bigip-node.yml` に入力します。

``` yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false
```

- ファイル上部の `---` は、これが YAML ファイルであることを示しています。  - `hosts: lb` は、プレイが lb
グループでのみ実行されることを示します。技術的には、F5 デバイスは 1 つだけしか存在しませんが、複数あれば、それぞれが同時に設定されます。  -
`connection: local` は、（自身に SSH 接続するのではなく）ローカルで実行するように Playbook に指示します  -
`gather_facts: false` はファクト収集を無効にします。この Playbook では、ファクト変数を使用しません。

まだエディターを閉じないでください。

## ステップ 3

次に、最初の `task` を上記の Playbook に追加します。このタスクは、`bigip_node` モジュールを使用して 2 つの RHEL
Web サーバーを BIG-IP F5 ロードバランサー上のノードとして設定します。

<!-- {% raw %} -->
``` yaml
  tasks:
    - name: CREATE NODES
      f5networks.f5_modules.bigip_node:
        provider:
          server: "{{private_ip}}"
          user: "{{ansible_user}}"
          password: "{{ansible_password}}"
          server_port: 8443
          validate_certs: false
        host: "{{hostvars[item].ansible_host}}"
        name: "{{hostvars[item].inventory_hostname}}"
      loop: "{{ groups['web'] }}"
```
<!-- {% endraw %} -->

>[loop](https://docs.ansible.com/ansible/latest/user_guide/playbooks_loops.html) は、タスクに指定したリストのタスクを繰り返します。この場合は、2 つの Web サーバーのそれぞれに対して 1 回ずつ、合計 2 回ループします。

- `name: CREATE NODES` は、ターミナル出力に表示されるユーザー定義の説明です。  - `bigip_node:`
は、使用するモジュールをタスクに指示します。`loop` 以外は、すべてモジュールのドキュメントページで定義されるモジュールパラメーターです。  -
`server: "{{private_ip}}"` パラメーターは、F5 BIG-IP IP
アドレスに接続するようにモジュールに指示します。このアドレスは、インベントリーの変数 `private_ip` として保存されます -
`provider:` パラメーターは、BIG-IP の接続詳細のグループです。  - `user: "{{ansible_user}}"`
パラメーターは、F5 BIG-IP デバイスにログインするためのユーザー名をモジュールに指示します - `password:
"{{ansible_password}}"` パラメーターは、F5 BIG-IP デバイスにログインするためのパスワードをモジュールに指示します -
`server_port: 8443` パラメーターは、F5 BIG-IP デバイスに接続するためのポートをモジュールに指示します - `host:
"{{hostvars[item].ansible_host}}"` パラメーターは、すでにインベントリーに定義されている Web サーバーの IP
アドレスを追加するようにモジュールに指示します。  - `name: "{{hostvars[item].inventory_hostname}}"`
パラメーターは、名前に `inventory_hostname` (node1 および node2) を使用するようにモジュールに指示します。  -
`validate_certs: false` パラメーターは、SSL
証明書を検証しないようにモジュールに指示します。これはラボなので、デモ目的のためにのみ使用されます。  - `loop:`
は、指定したリストをループするようにタスクに指示します。ここでのリストは、2 つの RHEL ホストが含まれるグループ Web です。

ファイルを保存して、エディターを終了します。

## ステップ 4

Playbook を実行します。コントロールホストの VS Code サーバーのターミナルに戻り、以下を実行します。

```
[student1@ansible ~]$ ansible-navigator run bigip-node.yml --mode stdout
```

# Playbook の出力

出力は次のようになります。

```yaml
[student1@ansible]$ ansible-navigator run bigip-node.yml --mode stdout

PLAY [BIG-IP SETUP] ************************************************************

TASK [CREATE NODES] ************************************************************
changed: [f5] => (item=node1)
changed: [f5] => (item=node2)

PLAY RECAP *********************************************************************
f5                         : ok=1    changed=1    unreachable=0    failed=0
```

# ソリューション

完成した Ansible Playbook
が、回答キーとしてここで提供されています。[bigip-node.yml](https://github.com/network-automation/linklight/blob/master/exercises/ansible_f5/1.2-add-node/bigip-node.yml)
を表示するには、ここをクリックしてください。

# ソリューションの確認

Web ブラウザーで F5 にログインし、設定された内容を確認します。lab_inventory/hosts ファイルから F5 ロードバランサーの
IP 情報を取得し、https://X.X.X.X:8443/ のように入力します。

BIG-IP のログイン情報: - ユーザー名: admin - パスワード: **インストラクターから提供、デフォルトは ansible**

ノードのリストは、左側のメニューからナビゲーションして探すことができます。Local Traffic をクリックし、続いて Nodes をクリックします。
![f5web](nodes.png)

You have finished this exercise.  [Click here to return to the lab
guide](../README.md)
