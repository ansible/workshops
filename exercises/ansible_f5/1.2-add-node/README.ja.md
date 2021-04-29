# 演習 1.2 - F5 BIG-IP へのノード追加

**Read this in other languages**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

## 目次

- [目的](#目的)
- [解説](#解説)
- [Playbook の出力](#Playbookの出力)
- [解答](#解答)
- [確認](#確認)

# 目的

本演習では、[BIG-IP node module](https://docs.ansible.com/ansible/latest/modules/bigip_node_module.html)を使用して、BIG-IP Load Balancer （以下、BIG-IP）へ、ウェブサーバーとなる２台のRHEL（Red Hat Enterprise Linux）を"ノード"として追加する方法を紹介します。

# 解説

## Step 1:

テキストエディタを使って、`bigip-node.yml` というファイルを新規作成します。

```
[student1@ansible ~]$ nano bigip-node.yml
```

>`vim` と `nano` はコントロールノード上で利用可能です。RDP経由でのVisual Studio と Atom も同様です。

## Step 2:

以下の定義を `bigip-node.yml` に入力します :

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

次に、最初のタスクを追加します。このタスクは、`bigip_node` モジュールを使用して、BIG-IP上に、２つの RHEL （Webサーバー）をノードとして設定します。

{% raw %}
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
{% endraw %}

>[loop](https://docs.ansible.com/ansible/latest/user_guide/playbooks_loops.html) は指定された一覧に対して、タスクを繰り返し実行します。  この演習では、二つのWebサーバーに対して一度づつタスクを実行します。


- `name: CREATE NODES` ：　ユーザーが定義する説明文です。これは実行時に端末に表示されることになります。
- `bigip_node:` ：　使用するモジュールを宣言しています。  `loop` を除く全てのものは、モジュールのドキュメント上で定義されている、モジュールパラメータです。
- `provider:` ：　BIG-IP の詳細な接続情報のオブジェクト。
- `server: "{{private_ip}}"` ：　接続先となるBIG-IPのIPアドレスを指定します。これはインベントリ内で `private_ip` として登録されているものです。
- `user: "{{ansible_user}}"` ：　BIG-IP へログインするユーザー名を指定します。
- `password: "{{ansible_password}}"` ：　BIG-IPへログインする際のパスワードを指定します。
- `server_port: 8443` ：　BIG-IPへ接続する際のポート番号を指定します。
- `validate_certs: false` ： （あくまで演習用ラボなので）SSL証明書の検証を行わないように設定します。
- `host: "{{hostvars[item].ansible_host}}"` ：　モジュールへインベントリに登録済みのWebサーバーのIPアドレスを追加します。
- `name: "{{hostvars[item].inventory_hostname}}"` ： `inventory_hostname` をホスト名（node1、node2 となります）として使うことを指示します。
- `loop:` ：　与えられた一覧に対してタスクをループ実行することを指定します。この演習では、二つのRHELホストを含む web グループが一覧となります。

ファイルを保存して、エディタを終了します。

## Step 4

プレイブックの実行 - コントロールホストのコマンドラインで以下を実行します。

```
[student1@ansible ~]$ ansible-playbook bigip-node.yml
```

# Playbookの出力

出力は以下のようになります。

```yaml
[student1@ansible]$ ansible-playbook bigip-node.yml

PLAY [BIG-IP SETUP] ************************************************************

TASK [CREATE NODES] ************************************************************
changed: [f5] => (item=node1)
changed: [f5] => (item=node2)

PLAY RECAP *********************************************************************
f5                         : ok=1    changed=1    unreachable=0    failed=0
```

# 解答

完成形のAnsible Playbook はこちらから参照可能です。 [bigip-node.yml](./bigip-node.yml).


# 確認

ブラウザでBIG-IPへログインして設定されたものを確認してみましょう。lab_inventory/hosts ファイルからBIG-IPのIPアドレスを確認して、https://X.X.X.X:8443/ のようにアクセスします。

BIG-IP へのログイン情報:
- username: admin
- password: **講師から指示されます** (default is admin)

画面左のメニューからノード一覧が確認できます。**Local Traffic** -> **Nodes** とクリックします。
![f5web](nodes.png)

これで本演習は終わりです。[演習ガイドへ戻る](../README.ja.md)
