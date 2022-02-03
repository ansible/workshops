# 演習 3.2 - Web アプリケーションの削除

**他の言語でもお読みいただけます** :![uk](../../../images/uk.png) [English](README.md)、![japan](../../../images/japan.png) [日本語](README.ja.md).

## 目次

- [目的](#objective)  - [ガイド](#guide)  - [Playbook の出力](#playbook-output)  -
[ソリューション](#solution)

# 目的

AS3 および uri モジュールを使用して Web アプリケーションを削除する方法を説明します。

# ガイド

## ステップ 1:

お好みのテキストエディターを使用して、`delete.yml` という名前の新規ファイルを作成します。

>RDP 経由の Visual Studio および Atom に加えて、`vim` および `nano` がコントロールノードで利用できます。

## ステップ 2:

次のプレイ定義を `delete.yml` に入力します。

{% raw %}
``` yaml
---
- name: LINKLIGHT AS3
  hosts: lb
  connection: local
  gather_facts: false

```
{% endraw %}

- ファイル上部の `---` は、これが YAML ファイルであることを示しています。  - `hosts: lb` は、プレイが lb
グループでのみ実行されることを示します。技術的には、F5 デバイスは 1 つだけしか存在しませんが、複数あれば、それぞれが同時に設定されます。  -
`connection: local` は、（自身に SSH 接続するのではなく）ローカルで実行するように Playbook に指示します  -
`gather_facts: false` はファクト収集を無効にします。この Playbook では、ファクト変数を使用しません。

## ステップ 3

以下を delete.yml Playbook に **追加します**。  
{% raw %}
``` yaml
  tasks:
    - name: PUSH AS3
      uri:
        url: "https://{{ ansible_host }}:8443/mgmt/shared/appsvcs/declare/WorkshopExample"
        method: DELETE
        status_code: 200
        timeout: 300
        body_format: json
        force_basic_auth: true
        user: "{{ ansible_user }}"
        password: "{{ ansible_password }}"
        validate_certs: false
      delegate_to: localhost
```
{% endraw %}

前回の演習から変更されたパラメーターは 3 つのみです。  - `url` は変更になりました。`declare` で終わる代わりに、テナント名の
`WorkshopExample` で終わります。  - `method` は POST から DELETE に変更されています。  - `body`
は削除されています。このテナント全体を削除するだけなので、必要ありません。

## ステップ 4
Playbook を実行します。コントロールホストのコマンドラインに戻り、以下を実行します。

```
[student1@ansible ~]$ ansible-playbook delete.yml
```

# Playbook の出力

出力は次のようになります。

{% raw %}
```yaml
[student1@ansible ~]$ ansible-playbook delete.yml

PLAY [LINKLIGHT AS3] **********************************************************

TASK [PUSH AS3] ***************************************************************
ok: [f5]

PLAY RECAP ********************************************************************
f5                         : ok=1    changed=0    unreachable=0    failed=0
```
{% endraw %}

# ソリューション

完成した Ansible Playbook
が、回答キーとしてここで提供されています。[delete.yml](https://github.com/network-automation/linklight/blob/master/exercises/ansible_f5/3.2-as3-delete/delete.yml)
を表示するには、ここをクリックしてください。

Web UI にログインし、`Partition` が削除されていることを確認します。

---
You have finished this exercise.  [Click here to return to the lab
guide](../README.md)
