# 演習 2.1: モジュールの組み合わせを使用した BIG-IP 上での設定の削除

**他の言語でもお読みいただけます** :![uk](../../../images/uk.png) [English](README.md)、![japan](../../../images/japan.png) [日本語](README.ja.md).

## 目次

- [目的](#objective)  - [ガイド](#guide)  - [Playbook の出力](#playbook-output)  -
[ソリューション](#solution)  - [ソリューションの確認](#verifying-the-solution)

# 目的

さまざまなモジュールを使用して BIG-IP 上で設定 (ノード/プール/仮想サーバー) を削除する方法を説明します。
# ガイド

## ステップ 1:

VSCode を使用して、左側のペインの新規ファイルアイコンをクリックして、`bigip-delete-configuration.yml`
という名前の新しいファイルを作成します。

![picture of create file
icon](../1.1-get-facts/images/vscode-openfile_icon.png)


## ステップ 2:

次のプレイ定義を `bigip-delete-configuration.yml` に入力します。

{% raw %}
``` yaml
---
- name: BIG-IP TEARDOWN
  hosts: lb
  connection: local
  gather_facts: false
```
{% endraw %} - ファイル上部の `---` は、これが YAML ファイルであることを示しています。  - `hosts: f5`
は、プレイが F5 BIG-IP デバイスでのみ実行されることを示します。  - `connection: local` は、（自身に SSH
接続するのではなく）ローカルで実行するように Playbook に指示します  - `gather_facts: false`
はファクト収集を無効にします。この Playbook では、ファクト変数を使用しません。

## ステップ 3

プロバイダー値を設定する set_fact で tasks セクションを追加します。

{% raw %}
``` yaml
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

次に、[bigip_virtual_server](https://docs.ansible.com/ansible/latest/modules/bigip_virtual_server_module.html)
を使用して、最初の `task` を追加します。このタスクは [演習 1.5 -
仮想サーバーの追加](../1.5-add-virtual-server/README.md) と同じですが、**state**
パラメーターが追加されています。`state: absent` は、F5 BIG-IP ロードバランサーから設定を削除します。

{% raw %}
``` yaml
    - name: DELETE VIRTUAL SERVER
      f5networks.f5_modules.bigip_virtual_server:
        provider: "{{provider}}"
        name: "vip"
        state: absent
```
{% endraw %} - `state: absent` は、設定を削除するようにモジュールに指示するパラメーターです。

## ステップ 5

次に、[bigip_pool](https://docs.ansible.com/ansible/latest/modules/bigip_pool_module.html)
を使用して、2 番目の `task` を追加します。このタスクは [演習 1.3 -
ロードバランシングプールの追加](../1.3-add-pool/README.md) と同じですが、**state** パラメーターが追加され
`absent` に設定されています。

{% raw %}
```yaml
    - name: DELETE POOL
      f5networks.f5_modules.bigip_pool:
        provider: "{{provider}}"
        name: "http_pool"
        state: absent
```
{% endraw %}

## ステップ 6

最後に、[bigip_node](https://docs.ansible.com/ansible/latest/modules/bigip_node_module.html)
を使用して、最後の `task` を追加します。このタスクは [演習 1.2 - F5 BIG-IP
へのノードの追加](../1.2-add-node/README.md) と同じですが、**state** パラメーターが追加され `absent`
に設定されています。

{% raw %}
```yaml
    - name: DELETE NODES
      f5networks.f5_modules.bigip_node:
        provider: "{{provider}}"
        name: "{{hostvars[item].inventory_hostname}}"
        state: absent
      loop: "{{ groups['web'] }}"
```
{% endraw %}

ファイルを保存します。

## ステップ 7
Playbook は、以前の演習で設定した仮想サーバーを削除してからプールを削除し、その後にノードを削除します。

Playbook を実行します。VS Code サーバーのターミナルに戻り、以下を実行します。

{% raw %}
```
[student1@ansible ~]$ ansible-navigator run bigip-delete-configuration.yml --mode stdout
```
{% endraw %}

# Playbook の出力

{% raw %}
```
[student1@ansible]$ ansible-navigator run bigip-delete-configuration.yml --mode stdout

PLAY [BIG-IP TEARDOWN] ********************************************************

TASK [Setup provider] *********************************************************
ok: [f5]

TASK [DELETE VIRTUAL SERVER] **************************************************
changed: [f5]

TASK [DELETE POOL] ************************************************************
changed: [f5]

TASK [DELETE NODES] ***********************************************************
changed: [f5] => (item=node1)
changed: [f5] => (item=node2)

PLAY RECAP ********************************************************************
f5                         : ok=4    changed=3    unreachable=0    failed=0

```
{% endraw %}

# ソリューション

完成した Ansible Playbook
が、回答キーとしてここで提供されています。[bigip-delete-configuration.yml](https://github.com/network-automation/linklight/blob/master/exercises/ansible_f5/2.1-delete-configuration/bigip-delete-configuration.yml)
を表示するには、ここをクリックしてください。

# ソリューションの確認

Web ブラウザーで F5 にログインし、設定された内容を確認します。lab_inventory/hosts ファイルから F5 ロードバランサーの
IP 情報を取得し、https://X.X.X.X:8443/ のように入力します。

BIG-IP のログイン情報: - ユーザー名: admin - パスワード: **インストラクターから提供、デフォルトは ansible**

左側のメニューでナビゲートし、設定が削除されていることを確認します
* Local Traffic Manager -> Virtual Server
* Local Traffic Manager -> Pool
* Local Traffic Manager -> Node

ここでの演習を完了しました。  

[Click here to return to the lab guide](../README.md)
