# ワークショップの演習 - 最初のプレイブックを書く

**他の言語で読む**:
<br>![uk](../../../images/uk.png) [英語](README.md), ![japan](../../../images/japan.png) [日本語](README.ja.md), ![brazil](../../../images/brazil.png) [ブラジルのポルトガル語](README.pt-br.md), ![france](../../../images/fr.png) [フランス語](README.fr.md), ![Español](../../../images/col.png) [スペイン語](README.es.md).

## 目次

- [ワークショップの演習 - 最初のプレイブックを書く](#ワークショップの演習---最初のプレイブックを書く)
  - [目的](#目的)
  - [ガイド](#ガイド)
    - [ステップ1 - プレイブックの基本](#ステップ1---プレイブックの基本)
    - [ステップ2 - プレイブックの作成](#ステップ2---プレイブックの作成)
    - [ステップ3 - プレイブックの実行](#ステップ3---プレイブックの実行)
    - [ステップ4 - プレイブックの確認](#ステップ4---プレイブックの確認)

## 目的

この演習では、Ansibleを使用してRed Hat Enterprise Linuxサーバーで基本的なシステム設定タスクを行います。`dnf`や`user`などの基本的なAnsibleモジュールに慣れ親しんで、プレイブックの作成と実行方法を学びます。

## ガイド

Ansibleのプレイブックは、基本的にYAML形式で書かれたスクリプトです。Ansibleがサーバーに適用するタスクと設定を定義するために使用されます。

### ステップ1 - プレイブックの基本
まず、プレイブック用のYAML形式のテキストファイルを作成します。覚えておくべきこと:
- 三つのダッシュ(`---`)から始めます。
- インデントにはタブではなくスペースを使用します。

主な概念:
- `hosts`: プレイブックが実行される対象のサーバーやデバイスを指定します。
- `tasks`: Ansibleが実行するアクションです。
- `become`: 権限の昇格（権限を持った状態でタスクを実行）を可能にします。

> 注: Ansibleのプレイブックは冪等性が設計されています。つまり、同じホストに対して複数回実行しても、望ましい状態を保証し、冗長な変更を加えないことを意味します。

### ステップ2 - プレイブックの作成
最初のプレイブックを作成する前に、`~/lab_inventory`に移動して正しいディレクトリにいることを確認します:

```bash
cd ~/lab_inventory
```

次に、基本的なシステム設定を行う`system_setup.yml`という名前のプレイブックを作成します:
- セキュリティ関連のすべてのパッケージを更新します。
- `myuser`という新しいユーザーを作成します。

基本的な構造は以下の通りです:

```yaml
---
- name: Basic System Setup
  hosts: node1
  become: true
  tasks:
    - name: Update all security-related packages
      ansible.builtin.dnf:
        name: '*'
        state: latest
        security: true

    - name: Create a new user
      ansible.builtin.user:
        name: myuser
        state: present
        create_home: true
```

> 注: パッケージの更新はAnsibleのプレイブックが完了する前に数分かかる場合があります。

* `dnf`モジュールについて: このモジュールは、RHELおよびその他のFedoraベースのシステムでDNF（Dandified YUM）を使用したパッケージ管理に使用されます。

* `user`モジュールについて: このモジュールは、ユーザーアカウントの管理に使用されます。

### ステップ3 - プレイブックの実行

`ansible-navigator`コマンドを使用してプレイブックを実行します:

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_setup.yml -m stdout
```

各タスクが正常に完了したことを確認するために出力を確認してください。

### ステップ4 - プレイブックの確認
次に、設定後のチェック用に`system_checks.yml`という名前の2つ目のプレイブックを作成しましょう:

```yaml
---
- name: System Configuration Checks
  hosts: node1
  become: true
  tasks:
    - name: Check user existence
      ansible.builtin.command:
        cmd: id myuser
      register: user_check

    - name: Report user status
      ansible.builtin.debug:
        msg: "User 'myuser' exists."
      when: user_check.rc == 0
```

チェック用のプレイブックを実行します:

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_checks.yml -m stdout
```

ユーザー作成が成功したことを確認するために出力を確認してください。

---
**ナビゲーション**
{% if page.url contains 'ansible_rhel_90' %}
[前の演習](../2-thebasics) - [次の演習](../4-variables)
{% else %}
[前の演習](../1.2-thebasics) - [次の演習](../1.4-variables)
{% endif %}
<br><br>

<br>

[Red Hat Enterprise Linux用Ansibleワークショップに戻る](../README.md)""

