# 演習 1.7: bigip_config モジュールの使用

**他の言語でもお読みいただけます** :![uk](../../../images/uk.png) [English](README.md)、![japan](../../../images/japan.png) [日本語](README.ja.md).

## 目次

- [目的](#objective)  - [ガイド](#guide)  - [Playbook の出力](#playbook-output)  -
[ソリューション](#solution)

# 目的

[BIG-IP
設定モジュール](https://docs.ansible.com/ansible/latest/modules/bigip_config_module.html)
を使用して実行中の設定をディスクに保存する方法を説明します。

# ガイド

## ステップ 1:

VSCode を使用して、左側のペインの新規ファイルアイコンをクリックして、`bigip-config.yml`
という名前の新しいファイルを作成します。

![picture of create file
icon](../1.1-get-facts/images/vscode-openfile_icon.png)

## ステップ 2:

Ansible Playbook は **YAML** ファイルです。YAML
は構造化されたエンコーディング形式であり、人間が非常に読みやすくなっています (JSON 形式のサブセットとは異なり)。

次のプレイ定義を `bigip-config.yml` に入力します。

``` yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false
```

- ファイル上部の `---` は、これが YAML ファイルであることを示しています。  - `hosts: f5` は、プレイが F5 BIG-IP
デバイスでのみ実行されることを示します。  - `connection: local` は、（自身に SSH
接続するのではなく）ローカルで実行するように Playbook に指示します  - `gather_facts: false`
はファクト収集を無効にします。この Playbook では、ファクト変数を使用しません。

## ステップ 3

次に `task` を追加します。このタスクは `bigip-config` を使用して、実行中の設定をディスクに保存します。

{% raw %}
``` yaml
  tasks:
    - name: SAVE RUNNING CONFIG ON BIG-IP
      f5networks.f5_modules.bigip_config:
        provider:
          server: "{{private_ip}}"
          user: "{{ansible_user}}"
          password: "{{ansible_password}}"
          server_port: 8443
          validate_certs: false
        save: true
```
{% endraw %}

>プレイはタスクのリストです。タスクとモジュールには 1:1 の相関があります。Ansible モジュールは再利用可能なスタンドアロンのスクリプトで、Ansible API または ansibleやansible-playbook プログラムで使用できます。これらは、終了する前に JSON 文字列を stdout に出力して Ansible に情報を返します。

- `name: SAVE RUNNING CONFIG ON BIG-IP` は、ターミナル出力に表示されるユーザー定義の説明です。
- `bigip_config:` は、使用するモジュールをタスクに指示します。
- `server: "{{private_ip}}"` パラメーターは、F5 BIG-IP IP
  アドレスに接続するようにモジュールに指示します。このアドレスは、インベントリーの変数 `private_ip` として保存されます
- `provider:` パラメーターは、BIG-IP の接続詳細のグループです。
- `user: "{{ansible_user}}"` パラメーターは、F5 BIG-IP
  デバイスにログインするためのユーザー名をモジュールに指示します
- `password: "{{ansible_password}}"` パラメーターは、F5 BIG-IP
  デバイスにログインするためのパスワードをモジュールに指示します
- `server_port: 8443` パラメーターは、F5 BIG-IP デバイスに接続するためのポートをモジュールに指示します
- `save: "yes""`
  パラメーターは、実行中の設定をスタートアップ設定に保存するようモジュールに指示します。この操作は、現在の実行中の設定に変更を加えた後に必ず実行されます。変更が行われない場合でも、設定はスタートアップ設定に保存されます。このオプションにより、モジュールは常に変更された状態に戻ります。
- `validate_certs: "no"` パラメーターは、SSL 証明書を検証しないようにモジュールに指示します。これはラボなので、デモ目的のためにのみ使用されます。

ファイルを保存します。

## ステップ 4

Playbook を実行します。VS Code サーバーのターミナルに戻り、以下を実行します。

```
[student1@ansible ~]$ ansible-navigator run bigip-config.yml --mode stdout
```

# Playbook の出力

```yaml
[student1@ansible]$ ansible-navigator run bigip-config.yml --mode stdout

PLAY [BIG-IP SETUP] *******************************************************************************

TASK [SAVE RUNNING CONFIG ON BIG-IP] *******************************************************************************
changed: [f5]

PLAY RECAP ********************************************************************
f5                         : ok=1    changed=1    unreachable=0    failed=0
```

# ソリューション

完成した Ansible Playbook
が、回答キーとしてここで提供されています。[bigip-config.yml](https://github.com/network-automation/linklight/blob/master/exercises/ansible_f5/1.7-save-running-config/bigip-config.yml)
を表示するには、ここをクリックしてください。

You have finished this exercise.  [Click here to return to the lab
guide](../README.md)
