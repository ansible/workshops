# 演習 2.2: モジュールの組み合わせを使用した安全なロールバックの実行

**他の言語でもお読みいただけます** :![uk](../../../images/uk.png) [English](README.md)、![japan](../../../images/japan.png) [日本語](README.ja.md).

## 目次

- [目的](#objective)  - [ガイド](#guide)  - [Playbook の出力](#playbook-output)  -
[ソリューション](#solution)

# 目的

さまざまなモジュールを使用して BIG-IP 上で設定のロールバックを行う方法を説明します。

# ガイド

## ステップ 1

VSCode を使用して、左側のペインの新規ファイルアイコンをクリックして、`bigip-error-handling.yml`
という名前の新しいファイルを作成します。

![picture of create file
icon](../1.1-get-facts/images/vscode-openfile_icon.png)

## ステップ 2

次のプレイ定義を `bigip-error-handling.yml` に入力します。

{% raw %}
``` yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false

```
{% endraw %}

- ファイル上部の `---` は、これが YAML ファイルであることを示しています。  - `hosts: lb` は、プレイが F5 BIG-IP
デバイスでのみ実行されることを示します。  - `connection: local` は、（自身に SSH
接続するのではなく）ローカルで実行するように Playbook に指示します  - `gather_facts: false`
はファクト収集を無効にします。この Playbook では、ファクト変数を使用しません。

## ステップ 3

プロバイダー値を設定する set_fact で tasks セクションを追加します。

{% raw %}
``` yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false

  tasks:
    - name: Setup provider
      set_fact:
        provider:
          server: "{{private_ip}}"
          user: "{{ansible_user}}"
          password: "{{ansible_password}}"
          server_port: 8443
          validate_certs: false

```
{% endraw %}

## ステップ 4

次に、`block` スタンザと最初の `task` を追加します。最初のタスクは、[演習 1.2 - F5 BIG-IP
へのノードの追加](../1.2-add-node/README.md) で実行される bigip_node です。

{% raw %}
``` yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false

  tasks:
    - name: Setup provider
      set_fact:
      provider:
        server: "{{private_ip}}"
        user: "{{ansible_user}}"
        password: "{{ansible_password}}"
        server_port: "8443"
        validate_certs: "no"

    - name: SETUP AND GRACEFUL ROLLBACK BIG-IP CONFIGURATION
      block:
        - name: CREATE NODES
          f5networks.f5_modules.bigip_node:
            provider: "{{provider}}"
            host: "{{hostvars[item].ansible_host}}"
            name: "{{hostvars[item].inventory_hostname}}"
          loop: "{{ groups['web'] }}"

```

{% endraw %}

## ステップ 5

次に、[演習 1.3 - ロードバランシングプールの追加](../1.3-add-pool/README.md)
で説明されているように、bigip_pool の 2 番目のタスクを追加します。

{% raw %}
```yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false

  tasks:
    - name: Setup provider
      set_fact:
        provider:
          server: "{{private_ip}}"
          user: "{{ansible_user}}"
          password: "{{ansible_password}}"
          server_port: "8443"
          validate_certs: "no"

    - name: SETUP AND GRACEFUL ROLLBACK BIG-IP CONFIGURATION
      block:
        - name: CREATE NODES
          f5networks.f5_modules.bigip_node:
            provider: "{{provider}}"
            host: "{{hostvars[item].ansible_host}}"
            name: "{{hostvars[item].inventory_hostname}}"
          loop: "{{ groups['web'] }}"

        - name: CREATE POOL
          f5networks.f5_modules.bigip_pool:
            provider: "{{provider}}"
            name: "http_pool"
            lb_method: "round-robin"
            monitors: "/Common/http"
            monitor_type: "and_list"

```
{% endraw %}

## ステップ 6

次に 3 番目のタスクを追加します。3 番目のタスクには、[演習 1.4 -
プールへのメンバーの追加](../1.4-add-pool-members/README.md)
で説明されているように、bigip_pool_member を使用します。

{% raw %}
```yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false

  tasks:
    - name: Setup provider
      set_fact:
        provider:
          server: "{{private_ip}}"
          user: "{{ansible_user}}"
          password: "{{ansible_password}}"
          server_port: "8443"
          validate_certs: "no"

    - name: SETUP AND GRACEFUL ROLLBACK BIG-IP CONFIGURATION
      block:
        - name: CREATE NODES
          f5networks.f5_modules.bigip_node:
            provider: "{{provider}}"
            host: "{{hostvars[item].ansible_host}}"
            name: "{{hostvars[item].inventory_hostname}}"
          loop: "{{ groups['web'] }}"

        - name: CREATE POOL
          f5networks.f5_modules.bigip_pool:
            provider: "{{provider}}"
            name: "http_pool"
            lb_method: "round-robin"
            monitors: "/Common/http"
            monitor_type: "and_list"

        - name: ADD POOL MEMBERS
          f5networks.f5_modules.bigip_pool_member:
            provider: "{{provider}}"
            state: "present"
            name: "{{hostvars[item].inventory_hostname}}"
            host: "{{hostvars[item].ansible_host}}"
            port: "80"
            pool: "http_pool"
          loop: "{{ groups['web'] }}"

```
{% endraw %}

## ステップ 7

次に 4 番目のタスクを追加します。4 番目のタスクには、[演習 1.5 -
仮想サーバーの追加](../1.5-add-virtual-server/README.md)
で説明されているように、bigip_virtual_server を使用します。

{% raw %}
```yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false

  tasks:
    - name: Setup provider
      set_fact:
        provider:
          server: "{{private_ip}}"
          user: "{{ansible_user}}"
          password: "{{ansible_password}}"
          server_port: "8443"
          validate_certs: "no"

    - name: SETUP AND GRACEFUL ROLLBACK BIG-IP CONFIGURATION
      block:
        - name: CREATE NODES
          f5networks.f5_modules.bigip_node:
            provider: "{{provider}}"
            host: "{{hostvars[item].ansible_host}}"
            name: "{{hostvars[item].inventory_hostname}}"
          loop: "{{ groups['web'] }}"

        - name: CREATE POOL
          f5networks.f5_modules.bigip_pool:
            provider: "{{provider}}"
            name: "http_pool"
            lb_method: "round-robin"
            monitors: "/Common/http"
            monitor_type: "and_list"

        - name: ADD POOL MEMBERS
          f5networks.f5_modules.bigip_pool_member:
            provider: "{{provider}}"
            state: "present"
            name: "{{hostvars[item].inventory_hostname}}"
            host: "{{hostvars[item].ansible_host}}"
            port: "80"
            pool: "http_pool"
          loop: "{{ groups['web'] }}"

        - name: ADD VIRTUAL SERVER
          f5networks.f5_modules.bigip_virtual_server:
            provider: "{{provider}}"
            name: "vip"
            destination: "{{private_ip}}"
            port: "443"
            enabled_vlans: "all"
            all_profiles: ['http', 'clientssl', 'oneconnect']
            pool: "http_pool"
            snat: "Automap1"

```
{% endraw %}

## ステップ 7

次に **rescue** スタンザを追加します。`rescue` スタンザセクションのタスクは、[演習 2.1 - F5 BIG-IP
設定の削除](../2.1-delete-configuration/README.md) と同じです。bigip_pool_member
タスクでは、ノードとプールを削除することですべての設定が削除されるので、bigip_pool_member
タスクを再入力する必要はありません。**ブロック** 内のタスクが失敗すると、**rescue**
スタンザが順番に実行されます。VIP、プール、およびノードが安全に削除されます。

{% raw %}
```yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false

  tasks:
    - name: Setup provider
      set_fact:
        provider:
          server: "{{private_ip}}"
          user: "{{ansible_user}}"
          password: "{{ansible_password}}"
          server_port: "8443"
          validate_certs: "no"

    - name: SETUP AND GRACEFUL ROLLBACK BIG-IP CONFIGURATION
      block:
        - name: CREATE NODES
          f5networks.f5_modules.bigip_node:
            provider: "{{provider}}"
            host: "{{hostvars[item].ansible_host}}"
            name: "{{hostvars[item].inventory_hostname}}"
          loop: "{{ groups['web'] }}"

        - name: CREATE POOL
          f5networks.f5_modules.bigip_pool:
            provider: "{{provider}}"
            name: "http_pool"
            lb_method: "round-robin"
            monitors: "/Common/http"
            monitor_type: "and_list"

        - name: ADD POOL MEMBERS
          f5networks.f5_modules.bigip_pool_member:
            provider: "{{provider}}"
            state: "present"
            name: "{{hostvars[item].inventory_hostname}}"
            host: "{{hostvars[item].ansible_host}}"
            port: "80"
            pool: "http_pool"
          loop: "{{ groups['web'] }}"

        - name: ADD VIRTUAL SERVER
          f5networks.f5_modules.bigip_virtual_server:
            provider: "{{provider}}"
            name: "vip"
            destination: "{{private_ip}}"
            port: "443"
            enabled_vlans: "all"
            all_profiles: ['http', 'clientssl', 'oneconnect']
            pool: "http_pool"
            snat: "Automap1"

      rescue:
        - name: DELETE VIRTUAL SERVER
          f5networks.f5_modules.bigip_virtual_server:
            provider: "{{provider}}"
            name: "vip"
            state: absent

        - name: DELETE POOL
          f5networks.f5_modules.bigip_pool:
            provider: "{{provider}}"
            name: "http_pool"
            state: absent

        - name: DELETE NODES
          f5networks.f5_modules.bigip_node:
            provider: "{{provider}}"
            name: "{{hostvars[item].inventory_hostname}}"
            state: absent
          loop: "{{ groups['web'] }}"

```
{% endraw %}

## ステップ 8

最後に **always** を追加して、実行中の設定を保存します。

{% raw %}
```yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false

  tasks:
    - name: Setup provider
      set_fact:
        provider:
          server: "{{private_ip}}"
          user: "{{ansible_user}}"
          password: "{{ansible_password}}"
          server_port: "8443"
          validate_certs: "no"

    - name: SETUP AND GRACEFUL ROLLBACK BIG-IP CONFIGURATION
      block:
        - name: CREATE NODES
          f5networks.f5_modules.bigip_node:
            provider: "{{provider}}"
            host: "{{hostvars[item].ansible_host}}"
            name: "{{hostvars[item].inventory_hostname}}"
          loop: "{{ groups['web'] }}"

        - name: CREATE POOL
          f5networks.f5_modules.bigip_pool:
            provider: "{{provider}}"
            name: "http_pool"
            lb_method: "round-robin"
            monitors: "/Common/http"
            monitor_type: "and_list"

        - name: ADD POOL MEMBERS
          f5networks.f5_modules.bigip_pool_member:
            provider: "{{provider}}"
            state: "present"
            name: "{{hostvars[item].inventory_hostname}}"
            host: "{{hostvars[item].ansible_host}}"
            port: "80"
            pool: "http_pool"
          loop: "{{ groups['web'] }}"

        - name: ADD VIRTUAL SERVER
          f5networks.f5_modules.bigip_virtual_server:
            provider: "{{provider}}"
            name: "vip"
            destination: "{{private_ip}}"
            port: "443"
            enabled_vlans: "all"
            all_profiles: ['http', 'clientssl', 'oneconnect']
            pool: "http_pool"
            snat: "Automap1"

      rescue:
        - name: DELETE VIRTUAL SERVER
          f5networks.f5_modules.bigip_virtual_server:
            provider: "{{provider}}"
            name: "vip"
            state: absent

        - name: DELETE POOL
          f5networks.f5_modules.bigip_pool:
            provider: "{{provider}}"
            name: "http_pool"
            state: absent

        - name: DELETE NODES
          f5networks.f5_modules.bigip_node:
            provider: "{{provider}}"
            name: "{{hostvars[item].inventory_hostname}}"
            state: absent
          loop: "{{ groups['web'] }}"

      always:
        - name: SAVE RUNNING CONFIGURATION
          f5networks.f5_modules.bigip_config:
            provider: "{{provider}}"
            save: true
```
{% endraw %}

上記の Playbook は仮想サーバー、プール、ノードの設定を試みますが、snat
値は「Automap1」として指定されているため、仮想サーバーの追加が失敗し、'rescue' ブロックが実行されます。

ファイルを保存して、エディターを終了します。

## ステップ 9

Playbook を実行します。VS Code サーバーのターミナルに戻り、以下を実行します。

{% raw %}
```
[student1@ansible ~]$ ansible-navigator run bigip-error-handling.yml --mode stdout
```
{% endraw %}

# Playbook の出力

{% raw %}
```yaml
[student1@ansible ~]$ ansible-navigator run bigip-error-handling.yml --mode stdout

PLAY [BIG-IP SETUP] ***********************************************************

TASK [Setup provider] *********************************************************
ok: [f5]

TASK [CREATE NODES] ***********************************************************
changed: [f5] => (item=node1)
changed: [f5] => (item=node2)

TASK [CREATE POOL] ************************************************************
changed: [f5]

TASK [ADD POOL MEMBERS] *******************************************************
changed: [f5] => (item=node1)
changed: [f5] => (item=node2)

TASK [ADD VIRTUAL SERVER] ****************************************************
fatal: [f5]: FAILED! => changed=false
  msg: '0107163f:3: Pool (/Common/Automap1) of type (snatpool) doesn''t exist.'

TASK [DELETE VIRTUAL SERVER] **************************************************
ok: [f5]

TASK [DELETE POOL] ************************************************************
changed: [f5]

TASK [DELETE NODES] ***********************************************************
changed: [f5] => (item=node1)
changed: [f5] => (item=node2)

TASK [SAVE RUNNING CONFIGURATION] *********************************************
changed: [f5]

PLAY RECAP ********************************************************************
f5                         : ok=8    changed=6    unreachable=0    failed=0
skipped=0    rescued=1    ignored=0

```
{% endraw %}
# ソリューション

完成した Ansible Playbook
が、回答キーとしてここで提供されています。[bigip-error-handling.yml](https://github.com/network-automation/linklight/blob/master/exercises/ansible_f5/2.2-error-handling/bigip-error-handling.yml)
を表示するには、ここをクリックしてください。

You have finished this exercise.  [Click here to return to the lab
guide](../README.md)
