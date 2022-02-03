# 演習 1.4: F5 でのプールへのメンバーの追加

**他の言語でもお読みいただけます** :![uk](../../../images/uk.png) [English](README.md)、![japan](../../../images/japan.png) [日本語](README.ja.md).

## 目次

- [目的](#objective)  - [ガイド](#guide)  - [Playbook の出力](#playbook-output)  -
[出力の解釈](#output-parsing)  - [ソリューション](#solution)  -
[ソリューションの確認](#verifying-the-solution)

# 目的

[BIG-IP プールメンバーモジュール](https://docs.ansible.com/ansible/latest/modules/bigip_pool_module.html) を使用して、Web サーバーノードを前の演習で作成したロードバランシングプール `http_pool` に結びつける方法を説明します。  

# ガイド

## ステップ 1:

VSCode を使用して、左側のペインの新規ファイルアイコンをクリックして、`bigip-pool-members.yml`
という名前の新しいファイルを作成します。

![picture of create file
icon](../1.1-get-facts/images/vscode-openfile_icon.png)

## ステップ 2:

次のプレイ定義を `bigip-pool-members.yml` に入力します。

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

まだエディターを終了しないでください。

## ステップ 3

次に、最初の `task` を上記の Playbook に追加します。このタスクは、`bigip_pool_member` モジュールを使用して 2
つの RHEL Web サーバーを BIG-IP F5 ロードバランサー上のノードとして設定します。

{% raw %}
``` yaml
  tasks:
    - name: ADD POOL MEMBERS
      f5networks.f5_modules.bigip_pool_member:
        provider:
          server: "{{private_ip}}"
          user: "{{ansible_user}}"
          password: "{{ansible_password}}"
          server_port: 8443
          validate_certs: false
        state: "present"
        name: "{{hostvars[item].inventory_hostname}}"
        host: "{{hostvars[item].ansible_host}}"
        port: "80"
        pool: "http_pool"
      loop: "{{ groups['web'] }}"
```
{% endraw %}

タスク内の各行の説明: - `name: ADD POOL MEMBERS` は、ターミナル出力に表示されるユーザー定義の説明です。  -
`bigip_pool_member:` は、使用するモジュールをタスクに指示します。

次に、モジュールパラメータが来ます - `server: "{{private_ip}}"` パラメーターは、F5 BIG-IP IP
アドレスに接続するようにモジュールに指示します。このアドレスは、インベントリーの変数 `private_ip` として保存されます -
`provider:` パラメーターは、BIG-IP の接続詳細のグループです。  - `user: "{{ansible_user}}"`
パラメーターは、F5 BIG-IP デバイスにログインするためのユーザー名をモジュールに指示します - `password:
"{{ansible_password}}"` パラメーターは、F5 BIG-IP デバイスにログインするためのパスワードをモジュールに指示します -
`server_port: 8443` パラメーターは、F5 BIG-IP デバイスに接続するためのポートをモジュールに指示します - `state:
"present"` パラメーターは、これを削除するのではなく追加することをモジュールに指示します。  - `name:
"{{hostvars[item].inventory_hostname}}"` パラメーターは、名前に `inventory_hostname`
(node1 および node2) を使用するようにモジュールに指示します。  - `host:
"{{hostvars[item].ansible_host}}"` パラメーターは、すでにインベントリーに定義されている Web サーバーの IP
アドレスを追加するようにモジュールに指示します。  - `port` パラメーターは、プールメンバーのポートを指示します。  - `pool:
"http_pool"` パラメーターは、このノードを http_pool という名前のプールに配置するようにモジュールに指示します -
`validate_certs: "no"` パラメーターは、SSL
証明書を検証しないようにモジュールに指示します。これはラボなので、デモ目的のためにのみ使用されます。最後に、タスクレベルの loop
パラメーターが来ます (モジュールパラメーターではなく、タスクレベルのパラメーターです)。 - `loop:`
は、指定されたリストをループオーバーするようにタスクに指示します。ここでは、リストは 2 つの RHEL ホストが含まれるグループ Web です。

ファイルを保存して、エディターを終了します。

## ステップ 4

Playbook を実行します。VS Code サーバーのターミナルに戻り、以下を実行します。

```
[student1@ansible ~]$ ansible-navigator run bigip-pool-members.yml --mode stdout
```

# Playbook の出力

出力は次のようになります。

```yaml
[student1@ansible ~]$ ansible-navigator run bigip-pool-members.yml --mode stdout

PLAY [BIG-IP SETUP] ************************************************************

TASK [ADD POOL MEMBERS] ********************************************************
changed: [f5] => (item=node1)
changed: [f5] => (item=node2)

PLAY RECAP *********************************************************************
f5                         : ok=1    changed=1    unreachable=0    failed=0
```
# 出力の解釈

bigip_device_info を使用して BIG-IP 上のプールメンバーを収集してみましょう。[JSON
クエリー](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#json-query-filter)
は、使用できる強力なフィルターです。先に進む前に確認してください。

{% raw %}
```
[student1@ansible ~]$ nano display-pool-members.yml
```

以下の設定を入力します。
```yaml
---
- name: "List pool members"
  hosts: lb
  gather_facts: false
  connection: local

  tasks:
    - name: Query BIG-IP facts
      f5networks.f5_modules.bigip_device_info:
        provider:
          server: "{{private_ip}}"
          user: "{{ansible_user}}"
          password: "{{ansible_password}}"
          server_port: 8443
          validate_certs: false
        gather_subset:
          - ltm-pools
      register: bigip_device_facts

    - name: "View complete output"
      debug: "msg={{bigip_device_facts}}"

    - name: "Show members belonging to pool"
      debug: "msg={{item}}"
      loop: "{{bigip_device_facts.ltm_pools | community.general.json_query(query_string)}}"
      vars:
        query_string: "[?name=='http_pool'].members[*].name[]"
```
{% endraw %}

- モジュールの `vars:` は、モジュール自体で使用される変数 query_string を定義します。
- `query_String` は、プール名 'http_pool' からのすべてのメンバーの名前を持ちます。json 文字列全体の読み取りを容易にするために、query_string が定義されます

VS Code ターミナルでの Playbook の実行
```
[student1@ansible ~]$ ansible-navigator run display-pool-members.yml --mode stdout
```

出力

``` yaml
[student1@ansible 1.4-add-pool-members]$ ansible-navigator run display-pool-members.yml --mode stdout

PLAY [List pool members] ******************************************************

TASK [Query BIG-IP facts] *****************************************************
changed: [f5]

TASK [View complete output] ***************************************************
ok: [f5] =>
  msg:
    changed: true
    ltm_pools:
    - allow_nat: 'yes'
      allow_snat: 'yes'
      client_ip_tos: pass-through
      client_link_qos: pass-through
      full_path: /Common/http_pool
      ignore_persisted_weight: 'no'
      lb_method: round-robin
      members:
      - address: 54.191.xx.xx
        connection_limit: 0
        dynamic_ratio: 1
        ephemeral: 'no'
        fqdn_autopopulate: 'no'
        full_path: /Common/node1:80
        inherit_profile: 'yes'
        logging: 'no'
        monitors: []
        name: node1:80
        partition: Common
        priority_group: 0
        rate_limit: 'no'
        ratio: 1
        state: disabled
      - address: 54.200.xx.xx
        connection_limit: 0
        dynamic_ratio: 1
        ephemeral: 'no'
        fqdn_autopopulate: 'no'
        full_path: /Common/node2:80
        inherit_profile: 'yes'
        logging: 'no'
        monitors: []
        name: node2:80
        partition: Common
        priority_group: 0
        rate_limit: 'no'
        ratio: 1
        state: disabled
      minimum_active_members: 0
      minimum_up_members: 0
      minimum_up_members_action: failover
      minimum_up_members_checking: 'no'
      monitors:
      - /Common/http
      name: http_pool
      priority_group_activation: 0
      queue_depth_limit: 0
      queue_on_connection_limit: 'no'
      queue_time_limit: 0
      reselect_tries: 0
      server_ip_tos: pass-through
      server_link_qos: pass-through
      service_down_action: none
      slow_ramp_time: 10

TASK [Show members belonging to pool] *****************************************
ok: [f5] => (item=node1:80) =>
  msg: node1:80
ok: [f5] => (item=node2:80) =>
  msg: node2:80

PLAY RECAP ********************************************************************
f5                         : ok=3    changed=1    unreachable=0    failed=0

```

# ソリューション
完成した Ansible Playbook
が、回答キーとしてここで提供されています。[bigip-pool-members.yml](https://github.com/network-automation/linklight/blob/master/exercises/ansible_f5/1.4-add-pool-members/bigip-pool-members.yml)
を表示するには、ここをクリックしてください。

# ソリューションの確認

Web ブラウザーで F5 にログインし、設定された内容を確認します。lab_inventory/hosts ファイルから F5 ロードバランサーの
IP 情報を取得し、https://X.X.X.X:8443/ のように入力します。

BIG-IP のログイン情報: - ユーザー名: admin - パスワード: **インストラクターから提供**、デフォルトは ansible

プールには 2 つのメンバー（node1 および node2）が表示されるようになります。Local Traffic をクリックし、続いて Pools をクリックします。http_pool をクリックして、より詳細な情報を取得します。中央の Members タブをクリックし、すべてのメンバーを一覧表示します。
![f5members](poolmembers.png)

You have finished this exercise.  [Click here to return to the lab
guide](../README.md)
