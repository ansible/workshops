# 演習 3.2 - Web アプリケーションの削除

**Read this in other languages**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

## 目次

- [目的](#目的)
- [解説](#解説)
- [Playbook の出力](#Playbookの出力)
- [解答](#解答)

# 目的

AS3および `uri` モジュールによりWebアプリケーションを削除します。

# 解説

## Step 1:

テキストエディタで新規ファイル `delete.yml` を作成します:

{% raw %}
```
[student1@ansible ~]$ nano delete.yml
```
{% endraw %}

>`vim` と`nano` がコントールノードで利用できます。もしくは RDP で接続して Visual Studio と Atom を利用することも可能です。

## Step 2:

以下の play 定義を `delete.yml` に追加してください:

{% raw %}
``` yaml
---
- name: LINKLIGHT AS3
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

以下を delete.yml へ **追加** してください。
{% raw %}
```
  tasks:

  - name: PUSH AS3
    uri:
      url: "https://{{ ansible_host }}:8443/mgmt/shared/appsvcs/declare/WorkshopExample"
      method: DELETE
      status_code: 200
      timeout: 300
      body_format: json
      force_basic_auth: yes
      user: "{{ ansible_user }}"
      password: "{{ ansible_ssh_pass }}"
      validate_certs: no
    delegate_to: localhost
```
{% endraw %}

前の演習から変更したパラメータは以下の3つだけです。
- `url` が変更され、最後が `declare` ではなく、テナント名（ここでは `WorkshopExample` ）になっています。
- `method` が POST から DELETE に変更されています。
- `body` が削除されています。ここでは、テナント全体を削除するだけなので必要ありません。

## Step 4

Playbook の実行 - コマンドラインへ戻ったら以下のコマンドでPlaybookを実行してください:

```
[student1@ansible ~]$ ansible-playbook delete.yml
```

# Playbookの出力

出力例は以下となります。

{% raw %}
```yaml
[student1@ansible ~]$ ansible-playbook delete.yml

PLAY [LINKLIGHT AS3] ***********************************************************

TASK [PUSH AS3] ********************************************************************************
ok: [f5 -> localhost]

PLAY RECAP ********************************************************************************
f5                         : ok=1    changed=0    unreachable=0    failed=0
```
{% endraw %}

# 解答

完成したPlaybookのサンプルは [delete.yml](./delete.yml) から参照できます。

Web UIにログインして、 `Partition` が削除されていることを確認します。

--

本演習は終了です。[Click here to return to the lab guide](../README.ja.md)
