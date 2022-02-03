# 演習 1.5: bigip_virtual_server モジュールの使用

**他の言語でもお読みいただけます** :![uk](../../../images/uk.png) [English](README.md)、![japan](../../../images/japan.png) [日本語](README.ja.md).

## 目次

- [目的](#objective)  - [ガイド](#guide)  - [Playbook の出力](#playbook-output)  -
[ソリューション](#solution)  - [ソリューションの確認](#verifying-the-solution)

# 目的

[BIG-IP
仮想サーバーモジュール](https://docs.ansible.com/ansible/latest/modules/bigip_virtual_server_module.html)
を使用して BIG-IP 上で仮想サーバーを設定する方法を説明します。仮想サーバーは IP:Port の組み合わせです。

# ガイド

## ステップ 1:

VSCode を使用して、左側のペインの新規ファイルアイコンをクリックして、`bigip-virtual-server.yml`
という名前の新しいファイルを作成します。

![picture of create file
icon](../1.1-get-facts/images/vscode-openfile_icon.png)

## ステップ 2:

Ansible Playbook は **YAML** ファイルです。YAML
は構造化されたエンコーディング形式であり、人間が非常に読みやすくなっています (JSON 形式のサブセットとは異なり)。

次のプレイ定義を `bigip-virtual-server.yml` に入力します。

``` yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false
```

- ファイル上部の `---` は、これが YAML ファイルであることを示しています。  - `hosts: f5` は、プレイが F5 BIG-IP
デバイスでのみ実行されることを示します。  - `connection: local` は、（自身に SSH
接続するのではなく）ローカルで実行するように Playbook に指示します  - `gather_facts: no`
はファクト収集を無効にします。この Playbook では、ファクト変数を使用しません。

まだエディターを終了しないでください。

## ステップ 3

次に、`task` を上記の Playbook に追加します。このタスクは、`bigip-virtual-server` を使用して BIG-IP
上で仮想サーバーを設定します。

<!-- {% raw %} -->

``` yaml
  tasks:
    - name: ADD VIRTUAL SERVER
      f5networks.f5_modules.bigip_virtual_server:
        provider:
          server: "{{private_ip}}"
          user: "{{ansible_user}}"
          password: "{{ansible_password}}"
          server_port: 8443
          validate_certs: false
        name: "vip"
        destination: "{{private_ip}}"
        port: "443"
        enabled_vlans: "all"
        all_profiles: ['http', 'clientssl', 'oneconnect']
        pool: "http_pool"
        snat: "Automap"
```

<!-- {% endraw %} -->

>プレイはタスクのリストです。タスクとモジュールには 1:1 の相関があります。Ansible モジュールは再利用可能なスタンドアロンのスクリプトで、Ansible API または ansibleやansible-playbook プログラムで使用できます。これらは、終了する前に JSON 文字列を stdout に出力して Ansible に情報を返します。

- `name: ADD VIRTUAL SERVER` は、ターミナル出力に表示されるユーザー定義の説明です。  -
`bigip_virtual_server:` は、使用するモジュールをタスクに指示します。  - `server: "{{private_ip}}"`
パラメーターは、F5 BIG-IP IP アドレスに接続するようにモジュールに指示します。このアドレスは、インベントリーの変数 `private_ip`
として保存されます - `provider:` パラメーターは、BIG-IP の接続詳細のグループです。  - `user:
"{{ansible_user}}"` パラメーターは、F5 BIG-IP デバイスにログインするためのユーザー名をモジュールに指示します -
`password: "{{ansible_password}}"` パラメーターは、F5 BIG-IP
デバイスにログインするためのパスワードをモジュールに指示します - `server_port: 8443` パラメーターは、F5 BIG-IP
デバイスに接続するためのポートをモジュールに指示します - `name: "vip"` パラメーターは、vip
という名前の仮想サーバーを作成するようにモジュールに指示します - `destination"` パラメーターは、仮想サーバーに割り当てる IP
アドレスをモジュールに指示します - `port` パラメーターは、仮想サーバーがリッスンするポートをモジュールに指示します -
`enabled_vlans` パラメーターは、仮想サーバーが有効なすべての vlan をモジュールに指示します - `all_profiles`
パラメーターは、仮想サーバーに割り当てられるすべてのプロファイルをモジュールに指示します - `pool`
パラメーターは、仮想サーバーに割り当てられるプールをモジュールに指示します - `snat`
パラメーターは、ソースネットワークアドレスをモジュールに指示します。このモジュールでは、自動マッピングされるように割り当てます。したがって、バックエンドサーバーに送信されるリクエストのソースアドレスは、BIG-IP
の自己 ip アドレスです - `validate_certs: "no"` パラメーターは、SSL
証明書を検証しないようにモジュールに指示します。これはラボなので、デモ目的のためにのみ使用されます。

ファイルを保存して、エディターを終了します

## ステップ 4

Playbook を実行します。VS Code サーバーのターミナルに戻り、以下を実行します。

```
[student1@ansible ~]$ ansible-navigator run bigip-virtual-server.yml --mode stdout
```

# Playbook の出力

```yaml
[student1@ansible]$ ansible-navigator run bigip-virtual-server.yml --mode stdout

PLAY [BIG-IP SETUP] ***********************************************************

TASK [ADD VIRTUAL SERVER] *****************************************************
changed: [f5]

PLAY RECAP ********************************************************************
f5                         : ok=1    changed=1    unreachable=0    failed=0
```

# ソリューション

完成した Ansible Playbook
が、回答キーとしてここで提供されています。[bigip-virtual-server.yml](https://github.com/network-automation/linklight/blob/master/exercises/ansible_f5/1.5-add-virtual-server/bigip-virtual-server.yml)
を表示するには、ここをクリックしてください。

# ソリューションの確認

設定した **仮想サーバー** を表示するには、Web ブラウザーを使用して F5 ロードバランサーにログインします。  

>`/home/studentX/networking_workshop/lab_inventory/hosts` ファイルから F5 ロードバランサーの IP 情報を取得し、https://X.X.X.X:8443/ のように入力します。

BIG-IP のログイン情報: - ユーザー名: admin - パスワード: **インストラクターから提供**、デフォルトは ansible

ロードバランサーの仮想サーバーは、左側のメニューからナビゲーションして探すことができます。**Local Traffic**
をクリックしてから、**Virtual Server** をクリックします。以下のスクリーンショットを参照してください。![f5 vip
image](f5vip.png)

## Web サーバーの確認

各 RHEL Web サーバーでは、すでに apache が実行されています。演習 1.1 から 1.5 では、Web
サーバーのプールのロードバランサーを正常に設定しました。Web ブラウザーで F5 ロードバランサーのパブリック IP を開きます。

>今回は、ポート 8443 の代わりに 443 を使用します (例: https://X.X.X.X:443/)

ホストをリフレッシュするたびに、**node1** と **node2** が切り替わります。ホストフィールドが変更されるアニメーションを、以下に示します。
![animation](animation.gif)
>アニメーションは特定のブラウザーでは機能しない可能性があります。

## その他の検証方法

ブラウザーウィンドウを使用する代わりに、Ansible コントロールノードでコマンドラインを使用することもできます。**ansible_host**
で、`--insecure` および `--silent` コマンドライン引数と組み合わせて `curl` コマンドを使用して、F5
ロードバランサーのパブリック IP またはプライベート IP アドレスにアクセスします。ウェブサイト全体がコマンドラインで読み込まれるため、`|
grep` を使用して該当するワークベンチに割り当てられた学生番号を検索することを推奨します (例: student5 の場合は `| grep
student5`)

```
[studentX@ansible ~]$ curl https://172.16.26.136:443 --insecure --silent | grep studentX
    <p>F5TEST-studentX-node1</p>
[studentX@ansible ~]$ curl https://172.16.26.136:443 --insecure --silent | grep studentX
    <p>F5TEST-studentX-node2</p>
[studentX@ansible ~]$ curl https://172.16.26.136:443 --insecure --silent | grep studentX
    <p>F5TEST-studentX-node1</p>
```

You have finished this exercise.  [Click here to return to the lab
guide](../README.md)
