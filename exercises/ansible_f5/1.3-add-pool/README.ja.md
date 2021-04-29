# 演習 1.3 - プールの追加

**Read this in other languages**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

## 目次

- [目的](#目的)
- [解説](#解説)
- [Playbook の出力](#Playbookの出力)
- [解答](#解答)
- [確認](#確認)

# 目的

本演習では、[BIG-IP pool module](https://docs.ansible.com/ansible/latest/modules/bigip_pool_module.html) を使って、BIG-IPへ負荷分散プール（省略して「プール」と表記する場合もあります）の設定を行います。負荷分散プールとは、トラフィックの受信および負荷分散を行うための論理的なデバイス（例：Webサーバー）の集合です。

# 解説

## Step 1:

テキストエディタを使って `bigip-pool.yml` というファイルを新規作成します。

```
[student1@ansible ~]$ nano bigip-pool.yml
```

>`vim` と `nano` はコントロールノード上で利用可能です。RDP経由でのVisual Studio と Atom も同様です。

## Step 2:

`bigip-pool.yml` へ、以下のプレイブック定義を記述します。

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

次に、タスクを追加します。このタスクは、`bigip_pool` モジュールを使用して、BIG-IP上に、http_poolという名前のプールを設定します。

{% raw %}
``` yaml
  tasks:
    - name: CREATE POOL
      f5networks.f5_modules.bigip_pool:
        provider:
          server: "{{private_ip}}"
          user: "{{ansible_user}}"
          password: "{{ansible_password}}"
          server_port: 8443
          validate_certs: false
        name: "http_pool"
        lb_method: "round-robin"
        monitors: "/Common/http"
        monitor_type: "and_list"

```

{% endraw %}

- `name: CREATE POOL` ：　ユーザーが定義する説明文です。これは実行時に端末に表示されることになります。
- `bigip_pool:` ： 使用するモジュールを宣言しています。
- `provider:` ：　BIG-IP の詳細な接続情報のオブジェクト。
- `server: "{{private_ip}}"` ：　接続先となるBIG-IPのIPアドレスを指定します。これはインベントリ内で `private_ip` として登録されているものです。
- `user: "{{ansible_user}}"` ：　BIG-IP へログインするユーザー名を指定します。
- `password: "{{ansible_password}}"` ：　BIG-IPへログインする際のパスワードを指定します。
- `server_port: 8443` ：　BIG-IPへ接続する際のポート番号を指定します。
- `validate_certs: false` ： （あくまで演習用ラボなので）SSL証明書の検証を行わないように設定します。
- `name: "http_pool"` ： 作成するプールの名前を指定します。
- `lb_method: "round-robin"`  ： 負荷分散方式を round-robin に指定します。全ての設定可能な負荷分散方式は bigip_pool モジュールのドキュメンテーションで確認できます。
- `monitors: "/Common/http"` ： http_poolというプールはHTTPトラフィックだけを扱うことを指定します。
- `monitor_type: "and_list"` ： 全てのモニターがチェックされるように指定します。

ファイルを保存して、エディタを終了してください。

## Step 4

プレイブックの実行 - コントロールホストのコマンドラインで以下を実行します。

```
[student1@ansible ~]$ ansible-playbook bigip-pool.yml
```

# Playbook の出力

出力は以下のようになります。

```yaml
[student1@ansible ~]$ ansible-playbook bigip-pool.yml

PLAY [BIG-IP SETUP] ************************************************************

TASK [CREATE POOL] *************************************************************
changed: [f5]

PLAY RECAP *********************************************************************
f5                         : ok=1    changed=1    unreachable=0    failed=0
```

# 解答

完成形のAnsible Playbook はこちらから参照可能です。[bigip-pool.yml](./bigip-pool.yml).

# 確認

ブラウザでBIG-IPへログインして設定されたものを確認してみましょう。lab_inventory/hosts ファイルからBIG-IPのIPアドレスを確認して、https://X.X.X.X:8443/ のようにアクセスします。

BIG-IP へのログイン情報:
- username: admin
- password: **講師から指示されます** (default is admin)

画面左のメニューからプールが確認できます。**Local Traffic** -> **Pools** とクリックします。
![f5pool](pool.png)

これで本演習は終わりです。[演習ガイドへ戻る](../README.ja.md)
