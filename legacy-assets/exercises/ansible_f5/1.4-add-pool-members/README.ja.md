# 演習 1.4 - メンバーをプールへ追加

**Read this in other languages**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

## 目次

- [目的](#目的)
- [解説](#解説)
- [Playbook の出力](#Playbookの出力)
- [出力のパース](#出力のパース)
- [解答](#解答)
- [確認](#確認)

# 目的

本演習では、[BIG-IP pool member module](https://docs.ansible.com/ansible/latest/modules/bigip_pool_member_module.html) を使って、演習 1.3 で作成したプール `http_pool` にWebサーバーを追加します。

# 解説

## Step 1:

テキストエディタを使って、`bigip-pool-members.yml` というファイルを新規作成します。

```
[student1@ansible ~]$ nano bigip-pool-members.yml
```

>`vim` と `nano` はコントロールノード上で利用可能です。RDP経由でのVisual Studio と Atom も同様です。

## Step 2:

`bigip-pool-members.yml` へ、以下のプレイブック定義を記述します :

``` yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false
```

- このファイルの最初の `---` は、このファイルがYAMLであることを示します。
- `hosts: lb` はこのプレイブックが lb グループのみで実行されることを示しています。 本演習では、BIG-IP機器は１つだけですが、もし複数台が設定されている場合には同時に設定されます。
- `connection: local` で、このプレイブックが（自分自身にSSH接続をするのではなく）ローカル実行されることを指示しています。
- `gather_facts: false` で、FACTの収集を無効化します。このプレイブックではFACT変数を使用しません。  

まだエディタを閉じないでください。

## Step 3

次に、タスクを追加します。このタスクは、`bigip_pool_member` モジュールを使用して、BIG-IP上に、２つの RHEL （Webサーバー）をプールメンバーとして設定します。

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


- `name: ADD POOL MEMBERS` ：　ユーザーが定義する説明文です。これは実行時に端末に表示されることになります。
- `bigip_pool_member:` ：　使用するモジュールを宣言しています。
- `provider:` ：　BIG-IP の詳細な接続情報のオブジェクト。
- `server: "{{private_ip}}"` ：　接続先となるBIG-IPのIPアドレスを指定します。これはインベントリ内で `private_ip` として登録されているものです。
- `user: "{{ansible_user}}"` ：　BIG-IP へログインするユーザー名を指定します。
- `password: "{{ansible_password}}"` ：　BIG-IPへログインする際のパスワードを指定します。
- `server_port: 8443` ：　BIG-IPへ接続する際のポート番号を指定します。
- `validate_certs: false` ： （あくまで演習用ラボなので）SSL証明書の検証を行わないように設定します。
- `state: "present"` ： プールメンバーを（削除ではなく）追加するように指定します。
- `name: "{{hostvars[item].inventory_hostname}}"` ： `inventory_hostname` をホスト名（node1、node2 となります）として使うことを指示します。
- `host: "{{hostvars[item].ansible_host}}"` ：　モジュールへインベントリに登録済みのWebサーバーのIPアドレスを追加します。
- `port`: プールメンバーポートを指定します。
- `pool: "http_pool"` ： Webサーバーを追加するプールとして、http_pool を指定します。
最後に、（モジュール・パラメータではなく）タスクレベルのパラメータである、loop パラメータの指定です。
- `loop:` ：　与えられた一覧に対してタスクをループ実行することを指定します。この演習では、二つのRHELホストを含む web グループが一覧となります。

ファイルを保存して、エディタを終了してください。

## Step 4

プレイブックの実行 - コントロールホストのコマンドラインで以下を実行します。

```
[student1@ansible ~]$ ansible-playbook bigip-pool-members.yml
```

# Playbook の出力

出力は以下のようになります。

```yaml
[student1@ansible ~]$ ansible-playbook bigip-pool-members.yml

PLAY [BIG-IP SETUP] ************************************************************

TASK [ADD POOL MEMBERS] ********************************************************
changed: [f5] => (item=node1)
changed: [f5] => (item=node2)

PLAY RECAP *********************************************************************
f5                         : ok=1    changed=1    unreachable=0    failed=0
```
# 出力のパース

bigip_device_facts モジュールを使って、BIG-IPに設定されたプールメンバー情報を確認してみましょう。 [JSON query](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#json-query-filter) は強力なフィルタリングツールです。演習を進める前に確認してみましょう。

{% raw %}
```
[student1@ansible ~]$ nano display-pool-members.yml
```

以下を記述します:
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
      loop: "{{bigip_device_facts.ltm_pools | json_query(query_string)}}"
      vars:
        query_string: "[?name=='http_pool'].members[*].name[]"
```
{% endraw %}

- `vars:` ： モジュール内部で利用されるクエリ文字列を定義しています。
- `query_String` ： 'http_pool' というプールに含まれる全てのプールメンバーの名前を取得します。query_string を設定することで JSON の可読性が向上します。

プレイブックの実行
```
[student1@ansible ~]$ ansible-playbook display-pool-members.yml
```

出力

```yaml
[student1@ansible ~]$ ansible-playbook display-pool-members.yml

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
f5                         : ok=3    changed=0    unreachable=0    failed=0
```

# 解答
完成形のAnsible Playbook はこちらから参照可能です。 [bigip-pool-members.yml](./bigip-pool-members.yml).

# 確認

ブラウザでBIG-IPへログインして設定されたものを確認してみましょう。lab_inventory/hosts ファイルからBIG-IPのIPアドレスを確認して、https://X.X.X.X:8443/ のようにアクセスします。

BIG-IP へのログイン情報:
- username: admin
- password: **講師から指示されます** (default is admin)

プールに二つのメンバー（node1とnode2）が含まれていることを確認します。**Local Traffic** -> **Pools** とクリックします。そして、http_pool をクリックすることでより詳細な情報を確認します。Members タブをクリックすることで全てのプールメンバーが表示されます。
![f5members](poolmembers.png)


これで本演習は終わりです。[演習ガイドへ戻る](../README.ja.md)
