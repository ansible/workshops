# ワークショップ演習 - テンプレート

**他の言語で読む**:
<br>![uk](../../../images/uk.png) [英語](README.md), ![japan](../../../images/japan.png) [日本語](README.ja.md), ![brazil](../../../images/brazil.png) [ブラジルポルトガル語](README.pt-br.md), ![france](../../../images/fr.png) [フランス語](README.fr.md), ![Español](../../../images/col.png) [スペイン語](README.es.md).

## 目次

- [目的](#目的)
- [ガイド](#ガイド)
  - [ステップ 1 - Jinja2 テンプレーティングへの導入](#ステップ-1---jinja2-テンプレーティングへの導入)
  - [ステップ 2 - はじめてのテンプレートを作成する](#ステップ-2---はじめてのテンプレートを作成する)
  - [ステップ 3 - プレイブックでテンプレートを展開する](#ステップ-3---プレイブックでテンプレートを展開する)
  - [ステップ 4 - プレイブックを実行する](#ステップ-4---プレイブックを実行する)

## 目的

演習 1.5 では、Ansible 内での Jinja2 テンプレーティングが紹介されます。これは、テンプレートから動的なファイルを生成するための強力な機能です。ホスト固有のデータを組み込んだテンプレートを作成する方法を学び、管理されている各ホストに合わせた設定ファイルを作成できるようになります。

## ガイド

### ステップ 1 - Jinja2 テンプレーティングへの導入

Ansible は Jinja2 を活用しています。Jinja2 は Python 用の広く使用されているテンプレート言語で、ファイル内で動的なコンテンツの生成を可能にします。この機能は、ホストごとに異なる必要がある設定ファイルを構成する場合に特に便利です。

### ステップ 2 - はじめてのテンプレートを作成する

テンプレートは `.j2` 拡張子で終わり、静的なコンテンツと `{{ }}` で囲まれた動的なプレースホルダーを混在させます。

次の例では、動的なホスト情報を含む「本日のメッセージ」(MOTD) のテンプレートを作成しましょう。

#### テンプレートディレクトリの設定:

テンプレートを整理するために、lab_inventory ディレクトリ内にテンプレートディレクトリが存在することを確認してください。

```bash
mkdir -p ~/lab_inventory/templates
```

#### MOTD テンプレートの開発:

テンプレートディレクトリに `motd.j2` という名前のファイルを作成し、以下の内容を含めます:

```jinja
{{ ansible_hostname }} へようこそ。
OS: {{ ansible_distribution }} {{ ansible_distribution_version }}
アーキテクチャ: {{ ansible_architecture }}
```

このテンプレートは、管理されている各ホストのホスト名、OS の配布、バージョン、およびアーキテクチャを動的に表示します。

### ステップ 3 - プレイブックでテンプレートを展開する

プレイブック内で `ansible.builtin.template` モジュールを使用して、管理されているホストにテンプレートを配布し、レンダリングします。

以下の内容で `system_setup.yml` プレイブックを変更します:

```yaml
---
- name: 基本的なシステムセットアップ
  hosts: all
  become: true
  tasks:
    - name: Jinja2 テンプレートから MOTD を更新
      ansible.builtin.template:
        src: templates/motd.j2
        dest: /etc/motd

  handlers:
    - name: ファイアウォールの再読み込み
      ansible.builtin.service:
        name: firewalld
        state: reloaded
```

`ansible.builtin.template` モジュールは `motd.j2` テンプレートを取り、各ホストに `/etc/motd` ファイルを生成し、テンプレートのプレースホルダーを実際のホストの事実で埋めます。

### ステップ 4 - プレイブックを実行する

管理されているすべてのホストにカスタム MOTD を適用するために、プレイブックを実行します:

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_setup.yml -m stdout
```

```plaintext
PLAY [基本的なシステムセットアップ] *********************************************
.
.
.

TASK [Jinja2 テンプレートから MOTD を更新] **************************************
changed: [node1]
changed: [node2]
changed: [node3]
changed: [ansible-1]

RECAP ************************************************************************
ansible-1                  : ok=6    changed=1    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
node1                      : ok=8    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node2                      : ok=8    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node3                      : ok=8    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

 ノードにSSHで接続して変更を確認し、その日のメッセージが表示されるはずです：

```plaintext
[rhel@control ~]$ ssh node1

node1 へようこそ。
OS: RedHat 8.7
アーキテクチャ: x86_64
このシステムを Red Hat Insights に登録する：insights-client --register
アカウントを作成するか、https://red.ht/insights-dashboard で全てのシステムを表示する
最終ログイン：2024年1月29日 月曜日 16:30:31 から 10.5.1.29
```


---
**ナビゲーション**
<br>
[前の演習](../1.5-handlers/README.ja.md) - [次の演習](../1.7-role/README.ja.md)

