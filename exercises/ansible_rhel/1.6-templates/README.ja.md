# ワークショップ演習 - テンプレート

**他の言語でもお読みいただけます**:
<br>![uk](../../../images/uk.png) [English](README.md)、![japan](../../../images/japan.png)[日本語](README.ja.md)、![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md)、![france](../../../images/fr.png) [Française](README.fr.md)、![Español](../../../images/col.png) [Español](README.es.md)

## 目次

* [目的](#目的)
* [ガイド](#ガイド)
  * [ステップ 1 - Playbooks でのテンプレートの使用](#ステップ-1---playbooks-でのテンプレートの使用)
  * [ステップ 2 - チャレンジラボ](#ステップ-2---チャレンジラボ)

## 目的

この演習では、Jinja2 テンプレートについて説明します。Ansible は Jinja2 テンプレートを使用して、ファイルが管理対象ホストに配布される前にファイルを変更します。Jinja2は、Python で最も使用されているテンプレートエンジンの1つです (<http://jinja.pocoo.org/>)。

## ガイド

### ステップ 1 - Playbooks でのテンプレートの使用

ファイルのテンプレートが作成されると、`template` モジュールを使用して管理対象ホストに展開できます。これは、制御ノードから管理対象ホストへのローカルファイルの転送に対応しています。

テンプレートの使用例として、ホスト固有のデータを含むように motd ファイルを変更します。

最初に、テンプレートリソースを保持するディレクトリー `templates` を `~/ansible-files/` に作成します。

```bash
[student@ansible-1 ansible-files]$ mkdir templates
```

その後、`~/ansible-files/templates/` ディレクトリーに、テンプレートファイル `motd-facts.j2` を作成します。

<!-- {% raw %} -->

```html+jinja
Welcome to {{ ansible_hostname }}.
{{ ansible_distribution }} {{ ansible_distribution_version}}
deployed on {{ ansible_architecture }} architecture.
```

<!-- {% endraw %} -->

このテンプレートファイルには、後でコピーされる基本的なテキストが含まれています。また、ターゲットマシンで個別に置き換えられる変数も含まれています。

次に、このテンプレートを使用するための Playbook が必要です。`~/ansible-files/` ディレクトリーで、Playbook `motd-facts.yml` を作成します。

```yaml
---
- name: Fill motd file with host data
  hosts: node1
  become: true
  tasks:
    - template:
        src: motd-facts.j2
        dest: /etc/motd
        owner: root
        group: root
        mode: 0644
```

この操作はこれまで数回行ってきました。

* Playbook の内容を把握します。
* Playbook `motd-facts.yml` を実行します。
* SSH 経由で node1 にログインし、その日の内容のメッセージを確認します。
* node1 からログアウトします。

Ansible がシステムから検出したファクトに変数置き換える方法を確認してください。

### ステップ 2 - チャレンジラボ

テンプレートに行を追加して、管理対象ノードの現在のカーネルを一覧表示します。

* 「Ansible ファクト」の章で学習したコマンドを使用して、カーネルバージョンを含むファクトを見つけます。

> *ヒント**
>
> カーネルのフィルター

> 新規作成された Playbook を実行してファクト名を検索します。 

* テンプレートを変更して、見つけたファクトを使用します。

* 再び motd Playbook を実行します。

* node1 にログインして motd を確認します

> **警告**
>
> **回答を以下に示します。**

* ファクトを見つけます。

```yaml
---
- name: Capture Kernel Version
  hosts: node1

  tasks:

    - name: Collect only kernel facts
      ansible.builtin.setup:
        filter:
        - '*kernel'
      register: setup

    - debug:
        var: setup
```

ワイルドカードが導入されると、出力は以下のようになります。

```bash

TASK [debug] *******************************************************************
ok: [node1] => {
    "setup": {
        "ansible_facts": {
            "ansible_kernel": "4.18.0-305.12.1.el8_4.x86_64"
        },
        "changed": false,
        "failed": false
    }
}
```

これにより、検索する変数に `ansible_kernel` というラベルが付けられます。

次に、motd-facts.j2 テンプレートを更新して、メッセージの一部として `ansible_kernel` を含めることができます。

* テンプレート `motd-facts.j2` 変更します。

<!-- {% raw %} -->

```html+jinja
Welcome to {{ ansible_hostname }}.
{{ ansible_distribution }} {{ ansible_distribution_version}}
deployed on {{ ansible_architecture }} architecture
running kernel {{ ansible_kernel }}.
```

<!-- {% endraw %} -->

* Playbook を実行します。

```bash
[student@ansible-1 ~]$ ansible-navigator run motd-facts.yml -m stdout
```

* `node1` への SSH ログインを介して新しいメッセージを確認します。

```bash
[student@ansible-1 ~]$ ssh node1
Welcome to node1.
RedHat 8.1
deployed on x86_64 architecture
running kernel 4.18.0-305.12.1.el8_4.x86_64.
```

---
**ナビゲーション**
<br>
[前の演習](../1.5-handlers) - [次の演習](../1.7-role)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-1---ansible-engine-exercises)
