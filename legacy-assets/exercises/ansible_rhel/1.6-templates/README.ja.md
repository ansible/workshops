# ワークショップ演習 - テンプレート

**その他の言語はこちらをお読みください。**
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## 目次

* [目的](#objective)
* [ガイド](#guide)
* [Step 1 - Playbooks でのテンプレートの使用](#step-1---using-templates-in-playbooks)
* [Step 2 - チャレンジラボ](#step-2---challenge-lab)

## 目的

この演習では、Jinja2 テンプレートについて説明します。Ansible は Jinja2
テンプレートを使用して、ファイルが管理対象ホストに配布される前にファイルを変更します。Jinja2は、Python
で最も使用されているテンプレートエンジンの1つです (<http://jinja.pocoo.org/>)。

## ガイド

### Step 1 - Playbook でのテンプレートの使用

ファイルのテンプレートが作成されると、`template`
モジュールを使用して管理対象ホストに展開できます。これは、制御ノードから管理対象ホストへのローカルファイルの転送に対応しています。

テンプレートの使用例として、ホスト固有のデータを含むように motd ファイルを変更します。

最初に、テンプレートリソースを保持するディレクトリー `templates` を `~/ansible-files/` に作成します。

```bash
[student<X>@ansible-1 ansible-files]$ mkdir templates
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

次に、このテンプレートを使用するための Playbook が必要です。`~/ansible-files/` ディレクトリーで、Playbook
`motd-facts.yml` を作成します。

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

### Step 2 - チャレンジラボ

テンプレートに行を追加して、管理対象ノードの現在のカーネルを一覧表示します。

* 「Ansible ファクト」の章で学習したコマンドを使用して、カーネルバージョンを含むファクトを見つけます。

> **ヒント**
>
> カーネルについて `grep -i` を実行します

* テンプレートを変更して、見つけたファクトを使用します。

* 再び Playbook を実行します。

* node1 にログインして motd を確認します

> **警告**
>
> **回答を以下に示します。**

* ファクトを見つけます。

```bash
[student<X>@ansible-1 ansible-files]$ ansible node1 -m setup|grep -i kernel
       "ansible_kernel": "3.10.0-693.el7.x86_64",
```

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
[student<X>@ansible-1 ~]$ ansible-playbook motd-facts.yml
```

* `node1` への SSH ログインを介して新しいメッセージを確認します。

```bash
[student<X>@ansible-1 ~]$ ssh node1
Welcome to node1.
RedHat 8.1
deployed on x86_64 architecture
running kernel 4.18.0-147.8.1.el8_1.x86_64.
```

---
**ナビゲーション**
<br>
[前の演習](../1.5-handlers) - [次の演習](../1.7-role)

[こちらをクリックして Ansible for Red Hat Enterprise Linux Workshop
に戻ります](../README.md#section-1---ansible-engine-exercises)
