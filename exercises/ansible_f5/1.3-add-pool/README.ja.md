# 演習 1.3 - ロードバランシングプールの追加

**他の言語でもお読みいただけます** :![uk](../../../images/uk.png) [English](README.md)、![japan](../../../images/japan.png) [日本語](README.ja.md).

## 目次

- [目的](#objective)  - [ガイド](#guide)  - [Playbook の出力](#playbook-output)  -
[ソリューション](#solution)  - [ソリューションの確認](#verifying-the-solution)

# 目的

[BIG-IP
プールモジュール](https://docs.ansible.com/ansible/latest/modules/bigip_pool_module.html)
を使用して BIG-IP
デバイスでロードバランシングプールを設定する方法を説明します。ロードバランシングプールは、トラフィックを受信して処理するためにグループ化する、Web
サーバーなどのデバイスの論理セットです。

# ガイド

## ステップ 1:

VSCode を使用して、左側のペインの新規ファイルアイコンをクリックして、`bigip-pool.yml` という名前の新しいファイルを作成します。

![picture of create file
icon](../1.1-get-facts/images/vscode-openfile_icon.png)

## ステップ 2:

次のプレイ定義を `bigip-pool.yml` に入力します。

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

次に、最初の `task` を上記の Playbook に追加します。このタスクは、`bigip_pool` モジュールを使用して 2 つの RHEL
Web サーバーを BIG-IP F5 ロードバランサー上のノードとして設定します。

<!-- {% raw %} -->

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

<!-- {% endraw %} -->

- `name: CREATE POOL` は、ターミナル出力に表示されるユーザー定義の説明です。  - `bigip_pool:`
は、使用するモジュールをタスクに指示します。  - `server: "{{private_ip}}"` パラメーターは、F5 BIG-IP IP
アドレスに接続するようにモジュールに指示します。このアドレスは、インベントリーの変数 `private_ip` として保存されます -
`provider:` パラメーターは、BIG-IP の接続詳細のグループです。  - `user: "{{ansible_user}}"`
パラメーターは、F5 BIG-IP デバイスにログインするためのユーザー名をモジュールに指示します - `password:
"{{ansible_password}}"` パラメーターは、F5 BIG-IP デバイスにログインするためのパスワードをモジュールに指示します -
`server_port: 8443` パラメーターは、F5 BIG-IP デバイスに接続するためのポートをモジュールに指示します - `name:
"http_pool"` パラメーターは、http_pool という名前のプールを作成するようにモジュールに指示します - `lb_method:
"round-robin"` パラメーターは、負荷分散方法がラウンドロビンであることをモジュールに指示します。方法の全リストは、bigip_pool
のドキュメントページに記載されています。  - `monitors: "/Common/http"` パラメーターは、http_pool が http
トラフィックだけを対象とすることをモジュールに指示します。  - `monitor_type: "and_list"`
は、すべてのモニターが確認されるようにします。  - `validate_certs: false` パラメーターは、SSL
証明書を検証しないようにモジュールに指示します。これはラボなので、デモ目的のためにのみ使用されます。

ファイルを保存して、エディターを終了します

## ステップ 4

Playbook を実行します。コントロールホストの VS Code サーバーのターミナルに戻り、以下を実行します。

```
[student1@ansible ~]$ ansible-navigator run bigip-pool.yml --mode stdout
```

# Playbook の出力

出力は次のようになります。

```yaml
[student1@ansible ~]$ ansible-navigator run bigip-pool.yml --mode stdout

PLAY [BIG-IP SETUP] ************************************************************

TASK [CREATE POOL] *************************************************************
changed: [f5]

PLAY RECAP *********************************************************************
f5                         : ok=1    changed=1    unreachable=0    failed=0
```

# ソリューション

完成した Ansible Playbook
が、回答キーとしてここで提供されています。[bigip-pool.yml](https://github.com/network-automation/linklight/blob/master/exercises/ansible_f5/1.3-add-pool/bigip-pool.yml)
を表示するには、ここをクリックしてください。

# ソリューションの確認

Web ブラウザーで F5 にログインし、設定された内容を確認します。lab_inventory/hosts ファイルから F5 ロードバランサーの
IP 情報を取得し、https://X.X.X.X:8443/ のように入力します。

BIG-IP のログイン情報: - ユーザー名: admin - パスワード: **インストラクターから提供、デフォルトは ansible**

ロードバランサーのプールは、左側のメニューからナビゲーションして探すことができます。Local Traffic をクリックし、続いて Pools をクリックします。
![f5pool](pool.png)

You have finished this exercise.  [Click here to return to the lab
guide](../README.md)
