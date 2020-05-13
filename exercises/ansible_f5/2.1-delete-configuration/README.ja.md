# 演習 2.1 - モジュールの組み合わせを使用してBIG-IPの構成を削除する

**Read this in other languages**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

## 目次

- [目的](#目的)
- [解説](#解説)
- [Playbook の出力](#Playbookの出力)
- [解答](#解答)
- [確認](#確認)

# 目的

異なるモジュールを使用して、BIG-IPの構成(ノード/プール/仮想サーバ)を削除します。

# 解説

## Step 1:

テキストエディタで新規ファイル `bigip-delete-configuration.yml` を作成します:

{% raw %}
```
[student1@ansible ~]$ nano bigip-delete-configuration.yml
```
{% endraw %}

>`vim` と`nano` がコントールノードで利用できます。もしくは RDP で接続して Visual Studio と Atom を利用することも可能です。

## Step 2:

以下の play 定義を `bigip-delete-configuration.yml` に追加してください:

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

次に、[bigip_virtual_server](https://docs.ansible.com/ansible/latest/modules/bigip_virtual_server_module.html) を使用してタスクを追加します。このタスクは、[演習 1.5 - virtual server の追加](../1.5-add-virtual-server/README.ja.md) と同じです。 `state:absent` は、F5BIG-IP ロードバランサから構成を削除します。

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

  - name: DELETE VIRTUAL SERVER
    bigip_virtual_server:
      provider: "{{provider}}"
      name: "vip"
      state: absent
```
{% endraw %}
- `state: absent` はモジュールに設定を削除するように指示するパラメータです。

## Step 5

次に、[bigip_pool](https://docs.ansible.com/ansible/latest/modules/bigip_pool_module.html) を使用して2番目のタスクを追加します。このタスクは[演習 1.3 - プールの追加](../1.3-add-pool/README.ja.md) に **state** パラメーター `absent` をつけたものと同じです。

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
```
{% endraw %}

## Step 6

最後に、[bigip_node](https://docs.ansible.com/ansible/latest/modules/bigip_node_module.html) を使用して最後のタスクを追加します。このタスクは、[演習 1.2 - F5 BIG-IP へのノード追加](../1.2-add-node/README.ja.md) に **state** パラメーター `absent` をつけたものと同じです。

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
    loop: "{{ groups['webservers'] }}"
```
{% endraw %}
上記のPlaybookは、仮想サーバ、プール、前の実習で構成したノードの順に削除します。

## Step 7

Playbook の実行 - コマンドラインへ戻ったら以下のコマンドでPlaybookを実行してください:

{% raw %}
```
[student1@ansible ~]$ ansible-playbook bigip-delete-configuration.yml
```
{% endraw %}

# Playbookの出力

{% raw %}
```
[student1@ansible]$ ansible-playbook bigip-delete-configuration.yml

PLAY [BIG-IP TEARDOWN] **************************************************************************************************************************************

TASK [Setup provider] ***************************************************************************************************************************************
ok: [f5]

TASK [DELETE VIRTUAL SERVER] ********************************************************************************************************************************
changed: [f5]

TASK [DELETE POOL] *********************************************************************************************************************************
changed: [f5]

TASK [DELETE NODES] *************************************************************************************************************************************
changed: [f5] => (item=node1)
changed: [f5] => (item=node2)

PLAY RECAP **************************************************************************************************************************************
f5                         : ok=4    changed=3    unreachable=0    failed=0

```
{% endraw %}

# 解答

完成したPlaybookのサンプルは [bigip-delete-configuration.yml](./bigip-delete-configuration.yml) から参照できます。

# 確認

Webブラウザを使用してF5にログインし、設定内容を確認します。F5ロードバランサーのIP情報を `lab_inventory/hosts` ファイルから取得し、https://X.X.X.X:8443/のように入力します。

BIG-IPのログイン情報:
- username: admin
- password: admin

左側のメニューに移動し、構成が削除されたことを確認します。
* Local Traffic Manager -> Virtual Server
* Local Traffic Manager -> Pool
* Local Traffic Manager -> Node

本演習は終了です。[Click here to return to the lab guide](../README.ja.md)
