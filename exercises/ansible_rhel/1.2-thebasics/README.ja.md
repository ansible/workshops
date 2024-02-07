# ワークショップ演習 - Ansibleの基本

**他の言語で読む**:
<br>![uk](../../../images/uk.png) [英語](README.md), ![japan](../../../images/japan.png) [日本語](README.ja.md), ![brazil](../../../images/brazil.png) [ブラジルのポルトガル語](README.pt-br.md), ![france](../../../images/fr.png) [フランス語](README.fr.md), ![Español](../../../images/col.png) [スペイン語](README.es.md).

## 目次 <!-- tocを省略 -->

- [目的](#目的)
- [ガイド](#ガイド)
  - [インベントリファイルの基本](#インベントリファイルの基本)
  - [モジュールの発見](#モジュールの発見)
  - [モジュールドキュメントへのアクセス](#モジュールドキュメントへのアクセス)

## 目的

この演習では、最新のAnsibleコマンドラインユーティリティ `ansible-navigator` を探索し、インベントリファイルの取り扱いと必要なときのモジュールリストの利用方法を学びます。目標は、`ansible-navigator` の動作方法と、Ansible体験を豊かにするための使用方法に慣れることです。

## ガイド

### インベントリファイルの基本

インベントリファイルは、コントロールマシンによって管理されるノードを指定するテキストファイルです。管理されるノードには、それらのノードのホスト名またはIPアドレスのリストが含まれる場合があります。インベントリファイルを使用すると、ホストグループ名を角括弧([])内に宣言することで、ノードをグループに整理できます。

### インベントリの探索

`ansible-navigator` コマンドをホスト管理に使用するには、コントロールノードから管理されるホストのリストを定義するインベントリファイルを提供する必要があります。このラボでは、インベントリはあなたのインストラクターによって提供されます。インベントリファイルは、ホストをグループに分類してリストし、さらにいくつかの変数を提供する `ini` 形式のファイルです。例は以下のようになります：

```bash
[web]
node1 ansible_host=<X.X.X.X>
node2 ansible_host=<Y.Y.Y.Y>
node3 ansible_host=<Z.Z.Z.Z>

[control]
ansible-1 ansible_host=44.55.66.77
```

ansible-navigator でインベントリを表示するには、コマンド `ansible-navigator inventory --list -m stdout` を使用します。このコマンドは、すべてのノードとそれぞれのグループを表示します。

```bash
[student@ansible-1 rhel_workshop]$ cd /home/student
[student@ansible-1 ~]$ ansible-navigator inventory --list -m stdout
{
    "_meta": {
        "hostvars": {
            "ansible-1": {
                "ansible_host": "3.236.186.92"            },
            "node1": {
                "ansible_host": "3.239.234.187"
            },
            "node2": {
                "ansible_host": "75.101.228.151"
            },
            "node3": {
                "ansible_host": "100.27.38.142"
            }
        }
    },
    "all": {
        "children": [
            "control",
            "ungrouped",
            "web"
        ]
    },
    "control": {
        "hosts": [
            "ansible-1"
        ]
    },
    "web": {
        "hosts": [
            "node1",
            "node2",
            "node3"
        ]
    }
}

```

注意：`-m` は `--mode` の略で、テキストベースのユーザーインターフェース (TUI) を使用する代わりに標準出力にモードを切り替えることができます。

より詳細なビューが不要な場合、`ansible-navigator inventory --graph -m stdout` はグルーピングの視覚的表現を提供します。

```bash
[student@ansible-1 ~]$ ansible-navigator inventory --graph -m stdout
@all:
  |--@control:
  |  |--ansible-1
  |--@ungrouped:
  |--@web:
  |  |--node1
  |  |--node2
  |  |--node3

```

明らかに、`node1`、`node2`、`node3` は `web` グループの一部であり、`ansible-1` は `control` グループの一部です。

インベントリファイルは、ホストをグループに整理したり、変数を定義したりすることができます。私たちの例では、現在のインベントリには `web` と `control` のグループがあります。これらのホストパターンで `ansible-navigator` を実行し、出力を観察してください：

`ansible-navigator inventory` コマンドを使用すると、1つのホストまたはグループにのみ情報を提供するコマンドを実行できます。例えば、以下のコマンドを実行し、それぞれの出力を観察してください。

```bash
[student@ansible-1 ~]$ ansible-navigator inventory --graph web -m stdout
[student@ansible-1 ~]$ ansible-navigator inventory --graph control -m stdout
[student@ansible-1 ~]$ ansible-navigator inventory --host node1 -m stdout
```

> **ヒント**
>
> インベントリには、より多くのデータを含めることができます。例えば、標準ではないSSHポートで実行されているホストがある場合、ホスト名の後にコロンとポート番号を置くことができます。Ansibleに特有の名前も定義して、それをIPアドレスまたはホスト名に指すことができます。

### モジュールの発見

Ansibleオートメーションプラットフォームには、複数のサポートされている実行環境 (EE) が付属しています。これらのEEには、サポートされているコンテンツ、モジュールを含むサポートされたコレクションがバンドルされています。

> **ヒント**
>
> `ansible-navigator` では、`ESC` ボタンを押すことで終了できます。

利用可能なモジュールをブラウズするには、まずインタラクティブモードに入ります：

```bash
$ ansible-navigator
```

![ansible-navigatorの画像](images/interactive-mode.png)

`:collections` と入力してコレクションをブラウズします。

```bash
:collections
```

![ansible-navigatorの画像](images/interactive-collections.png)

### モジュールドキュメントへのアクセス

特定のコレクションのモジュールを探索するには、コレクション名の隣にある番号を入力します。

例えば、上のスクリーンショットでは、`0` の番号が `amazon.aws` コレクションに対応しています。コレクションにズームインするには、`0` と入力します。

```bash
0
```

![ansible-navigatorの画像](images/interactive-aws.png)

任意のモジュールの詳細なドキュメントに直接アクセスするには、その対応する番号を指定します。例えば、モジュール `ec2_tag` は `24` に対応しています。

```bash
:24
```

矢印キーまたはページアップ、ページダウンを使用してスクロールすると、ドキュメントと例を表示できます。

![ansible-navigatorの画像](images/interactive-ec2-tag.png)

`:doc namespace.collection.module-name` と入力するだけで、特定のモジュールに直接スキップできます。例えば `:doc amazon.aws.ec2_tag` と入力すると、上に示した最後のページに直接スキップします。

> **ヒント**
>
> 異なる実行環境では、異なるコレクションやそれらのコレクションの異なるバージョンにアクセスできます。組み込みのドキュメントを使用することで、その特定のコレクションのバージョンに対して正確であることがわかります。

---
**Navigation**
{% if page.url contains 'ansible_rhel_90' %}
[Previous Exercise](../1-setup) - [Next Exercise](../3-playbook)
{% else %}
[Previous Exercise](../1.1-setup) - [Next Exercise](../1.3-playbook)
{% endif %}
<br><br>

<br>

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md)
