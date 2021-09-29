# ワークショップ演習 - 変数の使用

**その他の言語はこちらをお読みください。**
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## 目次

* [目的](#objective)
* [ガイド](#guide)
* [変数の概要](#intro-to-variables)
* [Step 1 - 変数ファイルの作成](#step-1---create-variable-files)
* [Step 2 - index.html ファイルの作成](#step-2---create-indexhtml-files)
* [Step 3 - Playbook の作成](#step-3---create-the-playbook)
* [Step 4 - 結果のテスト](#step-4---test-the-result)
* [Step 5 - Ansible ファクト](#step-5---ansible-facts)
* [Step 6 - チャレンジラボ: ファクト](#step-6---challenge-lab-facts)
* [Step 7 - Playbooks でのファクトの使用](#step-7---using-facts-in-playbooks)

## 目的

Ansibleは、Playbook
で使用できる値を格納するための変数をサポートしています。変数はさまざまな場所で定義でき、明確な優先順位があります。Ansible
は、タスクの実行時に変数をその値に置き換えます。

この演習では、特に以下についての変数について説明します。

* 変数区切り文字 `{{`や `}}` の使用方法
* `host_vars` と `group_vars` について、また使用するとき
* `ansible_facts` の使い方
* `debug` モジュールを使用して、コンソールウィンドウに変数を出力する方法

## ガイド

### 変数の概要

変数は、変数名を二重中括弧で囲むことにより、AnsiblePlaybooks で参照されます。

<!-- {% raw %} -->

```yaml
こちらが変数です。{{ variable1 }}
```

<!-- {% endraw %} -->

変数とその値は、インベントリー、追加ファイル、コマンドラインなどのさまざまな場所で定義できます。

インベントリーで変数を使う場合は、`host_vars` と `group_vars` という名前の 2
つのディレクトリーにあるファイルで変数を定義することが推奨されます。

* グループ「servers」の変数を定義するために、変数定義のある `group_vars/servers.yml` という YAML
  ファイルが作成されます。
* ホスト `node1` 専用の変数を定義するために、変数定義のある `host_vars/node1.yml` ファイルが作成されます。

> **ヒント**
>
> ホスト変数はグループ変数よりも優先されます (優先順位の詳細については、[docs](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable) を参照してください)。

### Step 1 - 変数ファイルの作成

理解を深め練習するためにも、ラボをみていきましょう。「Webサーバーを構築しましょう。1 つまたは 2
つ。またはそれ以上…」というテーマに続いて、`index.html` を変更し、サーバーがデプロイされている開発環境 (dev / prod)
を表示します。

Ansible コントロールホストでは、`student<X>` ユーザーとして、`~/ansible-files/` に変数定義を保持するディレクトリーを作成します。

```bash
[student<X>@ansible-1 ansible-files]$ mkdir host_vars group_vars
```

次に、変数定義を含む 2 つのファイルを作成します。異なる環境 `dev` または `prod` を参照する `stage` を定義します。

* 以下の内容で `~/ansible-files/group_vars/web.yml` ファイルを作成します。

```yaml
---
stage: dev
```

* 以下の内容で `~/ansible-files/host_vars/node2.yml` ファイルを作成します。

```yaml
---
stage: prod
```

これはなんでしょうか。

* `web` グループのサーバーすべてには、値 `dev` を持つ `stage`
  が定義されています。そのため、デフォルトでは、開発環境のメンバーとしてフラグを立てます。
* サーバー `node2` については、これはオーバーライドされ、ホストは実稼働サーバーとしてフラグが立てられます。

### Step 2 - web.html ファイルの作成

次に、`~/ansible-files/files/` で 2 つのファイルを作成します。

1 つは、以下の内容の `prod_web.html` と呼ばれます。

```html
<body>
<h1>これは稼働 Web サーバーです。それでは！</h1>
</body>
```

もう 1 つは、以下のない用の `dev_web.html` と呼ばれるファイルです。

```html
<body>
<h1>これは開発用ウェブサーバーです。お楽しみください！</h1>
</body>
```

### Step 3 - Playbook の作成

次に、「stage」変数にしたがって、prod または dev `web.html` ファイルをコピーする Playbook が必要です。

`~/ansible-files/` ディレクトリーに `deploy_index_html.yml` という新しい Playbook を作成します。

> **ヒント**
>
> 変数「stage」がどのように、コピーするファイルの名前で使用さているかに注意してください。

<!-- {% raw %} -->

```yaml
---
- name: Copy web.html
  hosts: web
  become: true
  tasks:
  - name: copy web.html
    copy:
      src: "{{ stage }}_web.html"
      dest: /var/www/html/index.html
```

<!-- {% endraw %} -->

* Playbook を実行します。

```bash
[student<X>@ansible-1 ansible-files]$ ansible-playbook deploy_index_html.yml
```

### Step 4 - 結果のテスト

Ansible Playbook は、さまざまなファイルを index.html としてホストにコピーし、`curl` を使用してテストします。

node1:

```bash
[student<X>@ansible-1 ansible-files]$ curl http://node1
<body>
<h1>This is a development webserver, have fun!</h1>
</body>
```

node2:

```bash
[student<X>@ansible-1 ansible-files]$ curl http://node2
<body>
<h1>This is a production webserver, take care!</h1>
</body>
```

node3:

```bash
[student<X>@ansible-1 ansible-files]$ curl http://node3
<body>
<h1>This is a development webserver, have fun!</h1>
</body>
```

> **ヒント**
>
> おそらくこのような考えがありませんでしょうか。ファイルの内容を変更する、もっと賢い方法があるはず...。その通りです。このラボは、変数の説明を行うためのものでした。次の章では、テンプレートについて学びます。

### Step 5 - Ansible ファクト

Ansible ファクトは、管理対象ホストから Ansible によって自動的に検出される変数です。それぞれの `ansible-playbook`
実行の出力にリストされている「ファクトの収集」タスクを覚えていますか？その時点で、管理対象ノードごとにファクトが収集されます。ファクトは、`setup`
モジュールでプルできます。これらには、管理者が再利用できる変数に格納された有用な情報が含まれています。

Ansible がデフォルトで収集するファクトを把握するには、コントロールノードで、student ユーザーとして次を実行します。

```bash
[student<X>@ansible-1 ansible-files]$ ansible node1 -m setup
```

多すぎる場合は、特定のファクトに出力を制限するフィルターを使用できます。使用する表現は、シェルスタイルのワイルドカードです。

```bash
[student<X>@ansible-1 ansible-files]$ ansible node1 -m setup -a 'filter=ansible_eth0'
```

あるいは、メモリ関連のファクトだけを探すのはどうでしょうか。

```bash
[student<X>@ansible-1 ansible-files]$ ansible node1 -m setup -a 'filter=ansible_*_mb'
```

### Step 6 - チャレンジラボ: ファクト

* 管理対象ホストのディストリビューション (Red Hat) の検索と出力を試行します。これは一行で行います。

> **ヒント**
>
> grep を使用してファクトを検索し、フィルターを適用して、このファクトのみを出力します。

> **警告**
>
> **回答を以下に示します。**

```bash
[student<X>@ansible-1 ansible-files]$ ansible node1 -m setup|grep distribution
[student<X>@ansible-1 ansible-files]$ ansible node1 -m setup -a 'filter=ansible_distribution' -o
```

### Step 7 - Playbook でのファクトの使用

もちろん、ファクトは、正しい名前を使用して、変数のように Playbook
で使用できます。このプレイブックを次のように、`~/ansible-files/` ディレクトリーに `facts.yml` として作成します。

<!-- {% raw %} -->

```yaml
---
- name: Output facts within a playbook
  hosts: all
  tasks:
  - name: Prints Ansible facts
    debug:
      msg: The default IPv4 address of {{ ansible_fqdn }} is {{ ansible_default_ipv4.address }}
```

<!-- {% endraw %} -->

> **ヒント**
>
> 「debug」モジュールは、変数と式のデバッグを行うのに便利です。

それを実行して、ファクトがどのように出力されるかを確認します。

```bash
[student<X>@ansible-1 ansible-files]$ ansible-playbook facts.yml

PLAY [Output facts within a playbook] ******************************************

TASK [Gathering Facts] *********************************************************
ok: [node3]
ok: [node2]
ok: [node1]
ok: [ansible-1]

TASK [Prints Ansible facts] ****************************************************
ok: [node1] =>
  msg: The default IPv4 address of node1 is 172.16.190.143
ok: [node2] =>
  msg: The default IPv4 address of node2 is 172.16.30.170
ok: [node3] =>
  msg: The default IPv4 address of node3 is 172.16.140.196
ok: [ansible-1] =>
  msg: The default IPv4 address of ansible is 172.16.2.10

PLAY RECAP *********************************************************************
ansible-1                  : ok=2    changed=0    unreachable=0    failed=0
node1                      : ok=2    changed=0    unreachable=0    failed=0
node2                      : ok=2    changed=0    unreachable=0    failed=0
node3                      : ok=2    changed=0    unreachable=0    failed=0
```

---
**ナビゲーション**
<br>

{% if page.url contains 'ansible_rhel_90' %}
[前の演習](../3-playbook) - [次の演習](../5-surveys)
{% else %}
[前の演習](../1.3-playbook) - [次の演習](../1.5-handlers)
{% endif %}
<br><br>
[こちらをクリックして Ansible for Red Hat Enterprise Linux Workshop に戻ります](../README.md)
