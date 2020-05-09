# 演習 2.2 - モジュールの組み合わせを使用して適切なロールバックを実行する

**Read this in other languages**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

## 目次

- [目的](#目的)
- [解説](#解説)
- [Playbook の出力](#Playbookの出力)
- [解答](#解答)

# 目的

BIG-IPで設定のロールバックを実行するためのさまざまなモジュールの使用方法を説明します。

# 解説

## Step 1

テキストエディアで新しいファイル `bigip-error-handling.yml` を作成します。

{% raw %}
```
[student1@ansible ~]$ nano bigip-error-handling.yml
```
{% endraw %}

>`vim` と`nano` がコントールノードで利用できます。もしくは RDP で接続して Visual Studio と Atom を利用することも可能です。

## Step 2

以下の play 定義を `bigip-error-handling.yml` に追加してください:

{% raw %}
``` yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: no

```
{% endraw %}

- ファイルの先頭の `---` はこのファイルが YAML であることを示します。
- `hosts: lb` はこのプレイブックが lb グループのみで実行されることを示しています。 本演習では、BIG-IP機器は１つだけですが、もし複数台が設定されている場合には同時に設定されます。
- `connection: local` は Playbook がローカル実行されることを示します。
- `gather_facts: no` Fact 情報の収集を無効にします。この演習では Playbook の中で Fact 情報を利用しません。

## Step 3

プロバイダ値を設定するために `set_fact` を含む tasks を追加します。

{% raw %}
```
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: no

  tasks:
  - name: Setup provider
    set_fact:
      provider:
        server: "{{private_ip}}"
        user: "{{ansible_user}}"
        password: "{{ansible_ssh_pass}}"
        server_port: "8443"
        validate_certs: "no"
```
{% endraw %}

## Step 4

次に、`block` 句とタスクを追加します。タスク[演習 1.2 - F5 BIG-IPへノードを追加](../1.2-add-node/README.ja.md) で実行した `bigip_node` です。

{% raw %}
``` yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: no

  tasks:
  - name: Setup provider
    set_fact:
      provider:
        server: "{{private_ip}}"
        user: "{{ansible_user}}"
        password: "{{ansible_ssh_pass}}"
        server_port: "8443"
        validate_certs: "no"

  - name: Setup and graceful rollback BIG-IP configuration
    block:
      - name: CREATE NODES
        bigip_node:
          provider: "{{provider}}"
          host: "{{hostvars[item].ansible_host}}"
          name: "{{hostvars[item].inventory_hostname}}"
        loop: "{{ groups['web'] }}"
```

{% endraw %}

## Step 5

次に、 [演習 1.3 - プールの追加](../1.3-add-pool/README.ja.md) で利用された`bigip_pool` のタスクを追加します。

{% raw %}
```yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: no

  tasks:
  - name: Setup provider
    set_fact:
      provider:
        server: "{{private_ip}}"
        user: "{{ansible_user}}"
        password: "{{ansible_ssh_pass}}"
        server_port: "8443"
        validate_certs: "no"

  - name: Setup and graceful rollback BIG-IP configuration
    block:
      - name: CREATE NODES
        bigip_node:
          provider: "{{provider}}"
          host: "{{hostvars[item].ansible_host}}"
          name: "{{hostvars[item].inventory_hostname}}"
        loop: "{{ groups['web'] }}"

      - name: CREATE POOL
        bigip_pool:
          provider: "{{provider}}"
          name: "http_pool"
          lb_method: "round-robin"
          monitors: "/Common/http"
          monitor_type: "and_list"
```
{% endraw %}

## Step 6

次タスクでは [演習 1.4 - メンバーをプールへ追加](../1.4-add-pool-members/README.ja.md) で説明した `bigip_pool_member` を使用します。

{% raw %}
```yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: no

  tasks:
  - name: Setup provider
    set_fact:
      provider:
        server: "{{private_ip}}"
        user: "{{ansible_user}}"
        password: "{{ansible_ssh_pass}}"
        server_port: "8443"
        validate_certs: "no"

  - name: Setup and graceful rollback BIG-IP configuration
    block:
      - name: CREATE NODES
        bigip_node:
          provider: "{{provider}}"
          host: "{{hostvars[item].ansible_host}}"
          name: "{{hostvars[item].inventory_hostname}}"
        loop: "{{ groups['web'] }}"

      - name: CREATE POOL
        bigip_pool:
          provider: "{{provider}}"
          name: "http_pool"
          lb_method: "round-robin"
          monitors: "/Common/http"
          monitor_type: "and_list"

      - name: ADD POOL MEMBERS
        bigip_pool_member:
          provider: "{{provider}}"
          state: "present"
          name: "{{hostvars[item].inventory_hostname}}"
          host: "{{hostvars[item].ansible_host}}"
          port: "80"
          pool: "http_pool"
        loop: "{{ groups['web'] }}"
```
{% endraw %}

## Step 7

次に[演習 1.5 - Virtual Server の追加](../1.5-add-virtual-server/README.ja.md)で使用した `bigip_virtual_server` タスクを追加します。

{% raw %}
```yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: no

  tasks:
  - name: Setup provider
    set_fact:
      provider:
        server: "{{private_ip}}"
        user: "{{ansible_user}}"
        password: "{{ansible_ssh_pass}}"
        server_port: "8443"
        validate_certs: "no"

  - name: Setup and graceful rollback BIG-IP configuration
    block:
      - name: CREATE NODES
        bigip_node:
          provider: "{{provider}}"
          host: "{{hostvars[item].ansible_host}}"
          name: "{{hostvars[item].inventory_hostname}}"
        loop: "{{ groups['web'] }}"

      - name: CREATE POOL
        bigip_pool:
          provider: "{{provider}}"
          name: "http_pool"
          lb_method: "round-robin"
          monitors: "/Common/http"
          monitor_type: "and_list"

      - name: ADD POOL MEMBERS
        bigip_pool_member:
          provider: "{{provider}}"
          state: "present"
          name: "{{hostvars[item].inventory_hostname}}"
          host: "{{hostvars[item].ansible_host}}"
          port: "80"
          pool: "http_pool"
        loop: "{{ groups['web'] }}"

      - name: ADD VIRTUAL SERVER
        bigip_virtual_server:
          provider: "{{provider}}"
          name: "vip"
          destination: "{{private_ip}}"
          port: "443"
          enabled_vlans: "all"
          all_profiles: ['http','clientssl','oneconnect']
          pool: "http_pool"
          snat: "Automap1"
```
{% endraw %}

## Step 7

次に、**rescue** 句を追加します。`rescue` 句に配置されるタスクは、 [演習 2.1 - コンフィグの削除](../2.1-delete-configuration/README.ja.md) と同じです。ノードとプールを削除するとすべての構成が削除されるため、`bigip_pool_member` タスクを再入力する必要はありません。**block** 内のいずれかのタスクが失敗すると、**rescue** が順番に実行されます。VIP、プール、およびノードは適切に削除されます。

{% raw %}
```yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: no

  tasks:
  - name: Setup provider
    set_fact:
      provider:
        server: "{{private_ip}}"
        user: "{{ansible_user}}"
        password: "{{ansible_ssh_pass}}"
        server_port: "8443"
        validate_certs: "no"

  - name: Setup and graceful rollback BIG-IP configuration
    block:
      - name: CREATE NODES
        bigip_node:
          provider: "{{provider}}"
          host: "{{hostvars[item].ansible_host}}"
          name: "{{hostvars[item].inventory_hostname}}"
        loop: "{{ groups['web'] }}"

      - name: CREATE POOL
        bigip_pool:
          provider: "{{provider}}"
          name: "http_pool"
          lb_method: "round-robin"
          monitors: "/Common/http"
          monitor_type: "and_list"

      - name: ADD POOL MEMBERS
        bigip_pool_member:
          provider: "{{provider}}"
          state: "present"
          name: "{{hostvars[item].inventory_hostname}}"
          host: "{{hostvars[item].ansible_host}}"
          port: "80"
          pool: "http_pool"
        loop: "{{ groups['web'] }}"

      - name: ADD VIRTUAL SERVER
        bigip_virtual_server:
          provider: "{{provider}}"
          name: "vip"
          destination: "{{private_ip}}"
          port: "443"
          enabled_vlans: "all"
          all_profiles: ['http','clientssl','oneconnect']
          pool: "http_pool"
          snat: "Automap1"

    rescue:
      - name: DELETE VIRTUAL SERVER
        bigip_virtual_server:
          provider: "{{provider}}"
          name: "vip"
          state: absent

      - name: DELETE POOL
        bigip_pool:
          provider: "{{provider}}"
          name: "http_pool"
          state: absent

      - name: DELETE NODES
        bigip_node:
          provider: "{{provider}}"
          name: "{{hostvars[item].inventory_hostname}}"
          state: absent
        loop: "{{ groups['web'] }}"
```
{% endraw %}

## Step 8

最後に **always** を追加してrunning config を保存します。

{% raw %}
```yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: no

  tasks:
  - name: Setup provider
    set_fact:
      provider:
        server: "{{private_ip}}"
        user: "{{ansible_user}}"
        password: "{{ansible_ssh_pass}}"
        server_port: "8443"
        validate_certs: "no"

  - name: Setup and graceful rollback BIG-IP configuration
    block:
      - name: CREATE NODES
        bigip_node:
          provider: "{{provider}}"
          host: "{{hostvars[item].ansible_host}}"
          name: "{{hostvars[item].inventory_hostname}}"
        loop: "{{ groups['web'] }}"

      - name: CREATE POOL
        bigip_pool:
          provider: "{{provider}}"
          name: "http_pool"
          lb_method: "round-robin"
          monitors: "/Common/http"
          monitor_type: "and_list"

      - name: ADD POOL MEMBERS
        bigip_pool_member:
          provider: "{{provider}}"
          state: "present"
          name: "{{hostvars[item].inventory_hostname}}"
          host: "{{hostvars[item].ansible_host}}"
          port: "80"
          pool: "http_pool"
        loop: "{{ groups['web'] }}"

      - name: ADD VIRTUAL SERVER
        bigip_virtual_server:
          provider: "{{provider}}"
          name: "vip"
          destination: "{{private_ip}}"
          port: "443"
          enabled_vlans: "all"
          all_profiles: ['http','clientssl','oneconnect']
          pool: "http_pool"
          snat: "Automap1"

    rescue:
      - name: DELETE VIRTUAL SERVER
        bigip_virtual_server:
          provider: "{{provider}}"
          name: "vip"
          state: absent

      - name: DELETE POOL
        bigip_pool:
          provider: "{{provider}}"
          name: "http_pool"
          state: absent

      - name: DELETE NODES
        bigip_node:
          provider: "{{provider}}"
          name: "{{hostvars[item].inventory_hostname}}"
          state: absent
        loop: "{{ groups['web'] }}"

    always:
      - name: SAVE RUNNING CONFIGURATION
        bigip_config:
          provider: "{{provider}}"
          save: yes
```
{% endraw %}

上記の Playbook では、仮想サーバー、プール、ノードの構成を試みますが、snat値が `Automap1` として提供されているため、仮想サーバーの追加は失敗し、`rescue` が実行されます。

## Step 9

Playbook の実行 - コマンドラインへ戻ったら以下のコマンドでPlaybookを実行してください:

{% raw %}
```
[student1@ansible ~]$ ansible-playbook bigip-error-handling.yml
```
{% endraw %}

# Playbookの出力

{% raw %}
```
[student1@ansible ~]$ ansible-playbook bigip-error-handling.yml

[student1@ansible ~]$ ansible-playbook bigip-error-handling.yml

PLAY [BIG-IP SETUP] ****************************************************************************************************

TASK [Setup provider] **************************************************************************************************
ok: [f5]

TASK [CREATE NODES] *****************************************************************************************************
changed: [f5] => (item=node1)
changed: [f5] => (item=node2)

TASK [CREATE POOL] *******************************************************************************************************
changed: [f5]

TASK [ADD POOL MEMBERS] **************************************************************************************************************************
changed: [f5] => (item=node1)
changed: [f5] => (item=node2)

TASK [ADD VIRTUAL SERVER] ***************************************************************************************************************************
fatal: [f5]: FAILED! => {"changed": false, "msg": "0107163f:3: Pool (/Common/Automap1) of type (snatpool) doesn't exist."}

TASK [DELETE VIRTUAL SERVER] **************************************************************************************************************************
ok: [f5]

TASK [DELETE POOL] **************************************************************************************************************************
changed: [f5]

TASK [DELETE NODES] **************************************************************************************************************************
changed: [f5] => (item=node1)
changed: [f5] => (item=node2)

TASK [SAVE RUNNING CONFIGURATION] ***************************************************************************************************************************
changed: [f5]

PLAY RECAP *****************************************************************************************************************
f5                         : ok=8    changed=6    unreachable=0    failed=1

```
{% endraw %}
# 解答

完成したPlaybookのサンプルは [bigip-error-handling.yml](./bigip-error-handling.yml) から参照できます。

本演習は終了です。 [Click here to return to the lab guide](../README.ja.md)
