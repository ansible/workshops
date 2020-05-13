# 演習 - 変数を使ってみよう

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

* [ステップ 1 - 変数ファイルの作成](#ステップ-1---変数ファイルの作成)
* [ステップ 2 - index.html ファイルの作成](#ステップ-2---indexhtml-ファイルの作成)
* [ステップ 3 - Playbook の作成](#ステップ-3---playbook-の作成)
* [ステップ 4 - 実行結果の確認](#ステップ-4---実行結果の確認)
* [ステップ 5 - Ansible ファクト](#ステップ-5---ansible-ファクト)
* [ステップ 6 - チャレンジラボ: ファクト](#ステップ-6---チャレンジラボ-ファクト)
* [Step 1.4.7 - Playbook の中でファクトを使う](#step-147---playbook-の中でファクトを使う)

前回までは Ansible Engine の基礎部分を学習してきました。この演習では Playbook をより柔軟かつパワフルに使用できる、より高度なスキルを学びます。

Ansible では task をよりシンプル、かつ再利用可能にできます。システムの設定にはユニークな設定が含まれる場合があり、
Playbook を実行する際、そのユニークな設定を含んだ実行が必要な場合があります。このような場合には変数を使います。

Ansible は、Playbook で使用可能な値を格納するための変数をサポートしています。変数はさまざまな場所で定義でき、明確な優先順位があります。Ansibleは、タスクが実行される際、変数をその値に置き換えます。

Playbook では、変数名を二重中括弧で囲むことで変数を表現します。

<!-- {% raw %} -->
```yaml
変数は右の様に表現します　 {{ variable1 }}
```
<!-- {% endraw %} -->

変数とその値は、インベントリ、追加ファイル、コマンドラインなどのさまざまな場所で定義できます。

インベントリで変数を提供するための推奨される方法は、host_vars と group_vars という2つのディレクトリにあるファイルにそれらを定義することです。

たとえば、グループ "servers" の変数を定義するために、変数名が付けられたYAMLファイル group_vars/servers を作成します。

また、特定ホスト node1 専用の変数を定義するために、変数定義を含む node1 ファイル host_vars/node1 を作成します。


> **ヒント**
>
> ホスト変数には優先順位があります。上記 Host 変数は、 Group 変数より優先されます。詳しくは製品マニュアルをご確認ください。

## ステップ 1 - 変数ファイルの作成

早速演習で変数の動きを確かめてみましょう。3台の Web Server を構築してみます。どのホストに接続されているかを示すため、 `index.html` を変更します。

まずは、Ansible Control Host で、変数ファイルの置き場所となるディレクトリを `~/ansible-files/`　に作成します。

```bash
[student<X>@ansible ansible-files]$ cd ~/ansible-files/
[student<X>@ansible ansible-files]$ mkdir host_vars group_vars
```

変数の定義を含むファイルを２つ作成しましょう。 `stage` という名前の変数に、`dev` or `prod`という異なる二つの値を定義します。

  - 以下の内容を含むファイルを `~/ansible-files/group_vars/web` として作成します。

```yaml
---
stage: dev
```

  - 同様に、以下の内容を含むファイルを `~/ansible-files/host_vars/node2` として作成します。

```yaml
---
stage: prod
```

これはどういう意味でしょう？

  -  `web` group のすべてのサーバーに対して、変数 `stage` に値 `dev` が定義されます。そして dev （開発）をデフォルト値として定義します。

  -  `node2` に関しては、上記で定義された変数 stage = dev が、prod で上書きされます。本番環境として定義されます。

## ステップ 2 - index.html ファイルの作成

`~/ansible-files/` 内に、以下の2つのファイルを作成します:

まずは本番環境用の `prod_index.html` に以下の内容を記述し、保存します。

```html
<body>
<h1>This is a production webserver, take care!</h1>
</body>
```

同様に、開発環境用の `dev_index.html` に以下の内容を記述し、保存します。

```html
<body>
<h1>This is a development webserver, have fun!</h1>
</body>
```

## ステップ 3 - Playbook の作成

次に、上記手順で作成した本番用、開発用の `index.html` の内いずれかのファイルを "stage" 変数の値に従って Web Server にコピーするための Playbook を作成します。

 `deploy_index_html.yml` という名前の Playbook を `~/ansible-files/` ディレクトリ内に作成します。

> **ヒント**
>
> コピーするファイル名の中に指定された変数 "stage" がホストごとに取る値に注意してください。

<!-- {% raw %} -->
```yaml
---
- name: Copy index.html
  hosts: web
  become: yes
  tasks:
  - name: copy index.html
    copy:
      src: ~/ansible-files/{{ stage }}_index.html
      dest: /var/www/html/index.html
```
<!-- {% endraw %} -->

  - Playbook を実行します

```bash
[student<X>@ansible ansible-files]$ ansible-playbook deploy_index_html.yml
```

## ステップ 4 - 実行結果の確認

各ホストには、変数 stage の値に従って異なるファイルがコピーされているはずです。デフォルトが dev で、node2 のみ、prod となっているはず。それぞれのweb server に curl コマンド（もしくはブラウザ）で接続して確認してみましょう。

```bash
[student<X>@ansible ansible-files]$ grep node ~/lab_inventory/hosts
node1 ansible_host=11.22.33.44
node2 ansible_host=22.33.44.55
node3 ansible_host=33.44.55.66
[student<X>@ansible ansible-files]$ curl http://11.22.33.44
<body>
<h1>This is a development webserver, have fun!</h1>
</body>
[student1@ansible ansible-files]$ curl http://22.33.44.55
<body>
<h1>This is a production webserver, take care!</h1>
</body>
[student1@ansible ansible-files]$ curl http://33.44.55.66
<body>
<h1>This is a development webserver, have fun!</h1>
</body>
```

> **ヒント**
>
> 鋭い人はちょっと思うかもしれません、”もっと柔軟にファイルの中身を変更出来たら・・・、と”。こちらについては次の章（template モジュール）で学びます！

## ステップ 5 - Ansible ファクト

Ansible ファクトは Ansible によって管理対象ホストから自動的に収集される変数です。"Gathering Facts" が各 ansible-playbook で実行されたことを思い出してください。ファクトは `setup` モジュールからも取得可能です。このファクトには、再利用可能な有用な情報が変数として格納されています。

Ansibleがデフォルトでどのような事実を収集しているのか、コントロールノードで次のように入力し確認してみましょう。

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup
```

結果表示がちょっと長すぎるので、フィルタを使ってみましょう。表現はシェルスタイルのワイルドカードです：

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup -a 'filter=ansible_eth0'
```
メモリ関連の情報が見たい場合は以下の様に実行します。

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup -a 'filter=ansible_*_mb'
```

## ステップ 6 - チャレンジラボ: ファクト

  - 管理対象ホストのディストリビューション（Red Hat）を表示してください。ただし、結果は一行で出力してください。

> **ヒント**
>
> grep を使ってファクトの中から必要な情報を探してみます。次に、 filter を使ってこのファクトのみの情報を抽出してみましょう。一行での表示の方法は ansible コマンドの -h (help) を使って調べてみましょう！


> **答えは下記の通り\!**

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup|grep distribution
[student<X>@ansible ansible-files]$ ansible node1 -m setup -a 'filter=ansible_distribution' -o
```

## Step 1.4.7 - Playbook の中でファクトを使う

取得したファクトの値は Playbook の中で変数同様に利用することが可能です。早速 Playbook `facts.yml` を `~/ansible-files/` ディレクトリに作成し、試してみましょう！

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
> "debug" モジュールは変数や式を確認するのに有用です。

取得されたファクトがどのような形で表示されるか Playbook を実行してみてください。

```bash
[student<X>@ansible ansible-files]$ ansible-playbook facts.yml

PLAY [Output facts within a playbook] ******************************************

TASK [Gathering Facts] *********************************************************
ok: [node3]
ok: [node2]
ok: [node1]
ok: [ansible]

TASK [Prints Ansible facts] ****************************************************
ok: [node1] =>
  msg: The default IPv4 address of node1 is 172.16.190.143
ok: [node2] =>
  msg: The default IPv4 address of node2 is 172.16.30.170
ok: [node3] =>
  msg: The default IPv4 address of node3 is 172.16.140.196
ok: [ansible] =>
  msg: The default IPv4 address of ansible is 172.16.2.10

PLAY RECAP *********************************************************************
ansible                    : ok=2    changed=0    unreachable=0    failed=0   
node1                      : ok=2    changed=0    unreachable=0    failed=0   
node2                      : ok=2    changed=0    unreachable=0    failed=0   
node3                      : ok=2    changed=0    unreachable=0    failed=0   
```

----

[Ansible Engine ワークショップ表紙に戻る](../README.ja.md#section-1---ansible-engineの演習)
