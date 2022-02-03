# 演習 1.6: bigip_irule モジュールの使用

**他の言語でもお読みいただけます** :![uk](../../../images/uk.png) [English](README.md)、![japan](../../../images/japan.png) [日本語](README.ja.md).

## 目次

- [目的](#objective)  - [ガイド](#guide)  - [Playbook の出力](#playbook-output)  -
[ソリューション](#solution)  - [ソリューションの確認](#verifying-the-solution)

# 目的

[BIG-IP irule
モジュール](https://docs.ansible.com/ansible/latest/modules/bigip_irule_module.html)
を使用して iRules を BIG-IP に追加し、続いて iRules を仮想サーバーにアタッチする方法を説明します。

# ガイド

## ステップ 1:

VSCode を使用して、左側のペインの新規ファイルアイコンをクリックして、`bigip-irule.yml` という名前の新しいファイルを作成します。

![picture of create file
icon](../1.1-get-facts/images/vscode-openfile_icon.png)

## ステップ 2:

Ansible Playbook は **YAML** ファイルです。YAML
は構造化されたエンコーディング形式であり、人間が非常に読みやすくなっています (JSON 形式のサブセットとは異なり)。

次のプレイ定義を `bigip-irule.yml` に入力します。

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

保存して、エディターを終了します。

## ステップ 3

'irule1' と 'irule2' という名前のダミーの irules を 2 つ作成します。

`irule1` の内容
```
when HTTP_REQUEST {
    log local0. "Accessing iRule1"
}
```
ファイルを保存します。

`irule2` の内容
```
when HTTP_REQUEST {
    log local0. "Accessing iRule2"
}
```
ファイルを保存します。

## ステップ 4

次に、`bigip-irule.yml` を再度開き、`task` を追加します。このタスクでは、`bigip-irule` を使用して irules
を BIG-IP に追加します。

{% raw %}
``` yaml
  vars:
    irules: ['irule1', 'irule2']

  tasks:
    - name: ADD iRules
      f5networks.f5_modules.bigip_irule:
        provider:
          server: "{{private_ip}}"
          user: "{{ansible_user}}"
          password: "{{ansible_password}}"
          server_port: 8443
          validate_certs: false
        module: "ltm"
        name: "{{item}}"
        content: "{{lookup('file','{{item}}')}}"
      with_items: "{{irules}}"
```
{% endraw %}

>プレイはタスクのリストです。タスクとモジュールには 1:1 の相関があります。Ansible モジュールは再利用可能なスタンドアロンのスクリプトで、Ansible API または ansibleやansible-playbook プログラムで使用できます。これらは、終了する前に JSON 文字列を stdout に出力して Ansible に情報を返します。

- `A variable 'irules'` は、2 つの irules ('irule1' と irule2') で定義されるリストです。
- `name: ADD iRules` は、ターミナル出力に表示されるユーザー定義の説明です。
- `bigip_irule:` は、使用するモジュールをタスクに指示します。
- `server: "{{private_ip}}"` パラメーターは、F5 BIG-IP IP
  アドレスに接続するようにモジュールに指示します。このアドレスは、インベントリーの変数 `private_ip` として保存されます
- `provider:` パラメーターは、BIG-IP の接続詳細のグループです。
- `user: "{{ansible_user}}"` パラメーターは、F5 BIG-IP
  デバイスにログインするためのユーザー名をモジュールに指示します
- `password: "{{ansible_password}}"` パラメーターは、F5 BIG-IP
  デバイスにログインするためのパスワードをモジュールに指示します
- `server_port: 8443` パラメーターは、F5 BIG-IP デバイスに接続するためのポートをモジュールに指示します
- `module: ltm` パラメーターは、iRule が対象となっている BIG-IP モジュール (ltm) をモジュールに指示します。
- `name: "{{item}}"` パラメーターは、モジュールに対し、'irule1' と 'irule2' という名前の iRule
  を作成するように指示します。
- `content: "{{lookup('file','{{item}}')}}" ` パラメーターは、[lookup
  プラグイン]https://docs.ansible.com/ansible/latest/plugins/lookup.html) を使用して
  iRule に追加するコンテンツをモジュールに指示します。
- `validate_certs: "no"` パラメーターは、SSL
  証明書を検証しないようにモジュールに指示します。これはラボなので、デモ目的のためにのみ使用されます。
- `loop:` は、提供された一覧をループするようにタスクに指示を出します。ここでは、このリストは iRules の一覧です。


## ステップ 5

次に、`task` を上記の Playbook に追加します。このタスクは、`bigip_virtual_server` を使用して iRules を
BIG-IP 上の仮想サーバーにアタッチします。

{% raw %}
``` yaml

    - name: ATTACH iRules TO VIRTUAL SERVER
      f5networks.f5_modules.bigip_virtual_server:
        provider:
          server: "{{private_ip}}"
          user: "{{ansible_user}}"
          password: "{{ansible_password}}"
          server_port: 8443
          validate_certs: false
        name: "vip"
        irules: "{{irules}}"
```
{% endraw %}

- `irules: "{{irules}}` は、仮想サーバー「irule1」および「irule2」にアタッチされる irules の一覧です。

[BIG-IP virtual_Server
モジュール](https://docs.ansible.com/ansible/latest/modules/bigip_irule_module.html)
の詳細または参照 [演習
1.5](https://github.com/network-automation/linklight/blob/master/exercises/ansible_f5/1.5-add-virtual-server/bigip-virtual-server.yml)

ファイルを保存します。

## ステップ 6

Playbook を実行します。VS Code サーバーのターミナルに戻り、以下を実行します。

```
[student1@ansible ~]$ ansible-navigator run bigip-irule.yml --mode stdout
```

# Playbook の出力

```yaml
[student1@ansible]$ ansible-navigator run bigip-irule.yml --mode stdout

PLAY [BIG-IP SETUP] ***********************************************************

TASK [ADD iRules] *******************************************************************************
changed: [f5] => (item=irule1)
changed: [f5] => (item=irule2)

TASK [ATTACH iRules TO VIRTUAL SERVER] ****************************************
changed: [f5]

PLAY RECAP *******************************************************************************
f5                         : ok=2    changed=2    unreachable=0    failed=0

```

# ソリューション

完成した Ansible Playbook
が、回答キーとしてここで提供されています。[bigip-irule.yml](https://github.com/network-automation/linklight/blob/master/exercises/ansible_f5/1.6-add-irules/bigip-irule.yml)
を表示するには、ここをクリックしてください。

# ソリューションの確認

設定した **iRules および仮想サーバー** を表示するには、Web ブラウザーを使用して F5 ロードバランサーにログインします。  

>`/home/studentX/networking_workshop/lab_inventory/hosts` ファイルから F5 ロードバランサーの IP 情報を取得し、https://X.X.X.X:8443/ のように入力します。

BIG-IP のログイン情報: - ユーザー名: admin - パスワード: **インストラクターから提供**、デフォルトは ansible

iRules の一覧は、左側のメニューからナビゲーションして探すことができます。Local Traffic -> iRules -> iRules List をクリックします。

仮想サーバーを表示するには、Local Traffic -> Virtual Servers をクリックし、Virtual Server をクリックしてから 'resoruces' タブをクリックし、仮想サーバーにアタッチされた iRules を表示します
![irules](bigip-irule.png)

You have finished this exercise.  [Click here to return to the lab
guide](../README.md)
