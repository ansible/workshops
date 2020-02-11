# 演習 1.7 - コンフィグの保存

**Read this in other languages**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

## 目次

- [目的](#目的)
- [解説](#解説)
- [Playbookの出力](#playbookの出力)
- [解答](#解答)

# 目的

[BIG-IP config module](https://docs.ansible.com/ansible/latest/modules/bigip_config_module.html) を使って、稼働中のコンフィグを保存する方法を確認する。

# 解説

## Step 1:

テキストエディアを使って `bigip-config.yml` ファイルを作成します。

```
[student1@ansible ~]$ nano bigip-config.yml
```

>`vim` と`nano` がコントールノードで利用できます。もしくは RDP で接続して Visual Studio と Atom を利用することも可能です。

## Step 2:

Ansible の playbook は **YAML** ファイルです。YAML は構造化されたエンコードで人にとって読みやすい形式です(JSON と違い・・・)

以下の play 定義を `bigip-virtual-server.yml` に追加してください:

``` yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false
```

- ファイルの先頭の `---` はこのファイルが YAML であることを示します。
- `hosts: lb` はこのプレイブックが lb グループのみで実行されることを示しています。 本演習では、BIG-IP機器は１つだけですが、もし複数台が設定されている場合には同時に設定されます。
- `connection: local` は Playbook がローカル実行されることを示します。
- `gather_facts: no` Fact 情報の収集を無効にします。この演習では Playbook の中で Fact 情報を利用しません。

## Step 3

次に、`task` を追加します。このタスクは `bigip-config` を使って稼働中のコンフィグを保存します。

{% raw %}
``` yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false

  tasks:

  - name: SAVE RUNNING CONFIG ON BIG-IP
    bigip_config:
      provider:
        server: "{{private_ip}}"
        user: "{{ansible_user}}"
        password: "{{ansible_ssh_pass}}"
        server_port: "8443"
        validate_certs: "no"
      save: yes
```
{% endraw %}


>`play` はタスクのリストです。タスクとリストは1：1の関係を持ちます。Ansible モジュールは再利用可能で、Ansible API、`ansible` `ansible-playbook` コマンドから利用できるスタンドアローンなスクリプトです。実行されたモジュールは Ansible に JSON 形式の文字列を返します。

- `name: SAVE RUNNING CONFIG ON BIG-IP` は利用者が定義するタスクの説明文で、この内容がターミナルに表示されます。
- `bigip_config:` はタスクで使用されるモジュール名を指定します。
- The `server: "{{private_ip}}"` モジュールのパラメーターです。モジュールがどのBIG-IPのIPアドレスに接続するかを指定します。ここではインベントリーで定義された`private_ip`が指定されています。
- The `user: "{{ansible_user}}"` モジュールのパラメーターです。BIP-IPにログインするユーザー名を設定しています。
- The`password: "{{ansible_ssh_pass}}"` モジュールのパラメーターです。BIG-IPにログインするパスワードを指定します。
- The `server_port: 8443` モジュールのパラメーターです。BIP-IPに接続する際のポート番号を指定します。
- The `save: "yes""` モジュールのパラメーターです。running-config を startup-config へ保存するします。
  この操作は現在のコンフィグに変更が行われた後に実行されます。何も変更されなくても設定は startup-config に保存されます。このオプションは常に `changed` を返します。
- `validate_certs: "no"` モジュールのパラメーターです。証明書の検証を行いません。これは演習上のデモ環境のためです。

## Step 4

Playbook の実行 - コマンドラインへ戻ったら以下のコマンドでPlaybookを実行してください:

```
[student1@ansible ~]$ ansible-playbook bigip-config.yml
```

# Playbookの出力

```yaml
[student1@ansible]$ ansible-playbook bigip-config.yml

PLAY [BIG-IP SETUP] ************************************************************************************************************************

TASK [SAVE RUNNING CONFIG ON BIG-IP] ************************************************************************************************************************
changed: [f5]

PLAY RECAP *************************************************************************************************************
f5                         : ok=1    changed=1    unreachable=0    failed=0
```

# 解答

完成したPlaybookのサンプルは [bigip-config.yml](./bigip-config.yml) から参照できます。

本演習は終了です。   [Click here to return to the lab guide](../README.ja.md)
