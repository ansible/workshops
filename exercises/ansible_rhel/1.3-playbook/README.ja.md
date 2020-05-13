# Workshop Exercise - 初めての Playbook 作成

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

# Table of Contents

* [Step 1 - Playbook Basics](#step-1---playbook-basics)
* [Step 2 - ディレクトリの構成とPlaybook用のファイルを作成しよう](#step-2---ディレクトリの構成とplaybook用のファイルを作成しよう)
* [Step 3 - Playbookを実行してみる](#step-3---playbookを実行してみる)
* [Step 4 - Playbookを拡張してみよう。Apacheの起動と有効化](#step-4---playbookを拡張してみようapacheの起動と有効化)
* [Step 5 - Playbookを拡張してみよう。web.htmlの作成](#step-5---playbookを拡張してみようindexhtmlの作成)
* [Step 6 - 練習: 複数ホストへの適用](#step-6---練習-複数ホストへの適用)

Ansibleのアドホックコマンドは単純なオペレーションの際にはとても役立ちますが、複雑な構成管理やオーケストレーションのシナリオには適していません。そのようなユースケースの時には、*playbooks*を用いてみると良いでしょう。

Playbook（プレイブック）は、管理対象に対して実装したいこうなってほしいという構成や手順を記述したファイルです。Playbookを用いることで、長く複雑な管理タスクたちを、成功が予測される状態で、簡単にいつでも再現できるルーチンへと変えることができます。

playbookは先ほど実行していたアドホックコマンドを複数取り込み、繰り返し実行可能な*plays* と *tasks* のセットとして利用することができるようになります。

Playbookには、複数のPlayを持たせることができ、Playは1つもしくは複数のTaskを持ちます。前の章で学習したように、Taskでは*module*が呼び出され実行されます。
*play*の目的は、ホストのグループをマッピングすることです。 *task*のゴールはそれらのホストに対して、モジュールを用いて実行することです。

## Step 1 - Playbook Basics

PlaybookはYAML形式で書かれたテキストファイルです。
以下のような記載が必要です。

  - 3つのダッシュ記号から始まります(`---`)

  - 正しいインデントをスペースを用いて記述します。**tabではありません**\!

いくつかの重要なコンセプトがあります:

  - **hosts**: タスクを実行する管理対象ホストです。

  - **tasks**: Ansibleモジュールを呼び出し、必要なオプションを渡すことで実行される操作たち

  - **become**: アドホックコマンドで `-b` を用いるのと同様に、Playbook内で権限昇格させます。

> **Warning**
>
> Ansibleはplayとtaskを表示されている順序で実行していくため、Playbook内のコンテンツの順序はとても重要です。

Playbookは**冪等性(べきとうせい。ある操作を1回行っても複数回行っても結果が同じになる性質)** を持っているべきです。一度、playbookを正しい状態にすべく実行されたのであれば、さらにもう一度playbookが実行された場合には安全であるべきです。そしてその際にはなんの変更もホストで発生するべきではありません。

> **Tip**
>
> ほとんどのAnsibleモジュールはべき等性を持っているので、比較的簡単に正しいかどうかは確認できます。

## Step 2 - ディレクトリの構成とPlaybook用のファイルを作成しよう

セオリーの話はもう十分でしょう。そろそろ最初のPlaybookを作成しましょう。
このラボでは、Apache webserverを3つのステップでセットアップするPlaybookを作成します。:

  - First step: httpd パッケージをインストールします。

  - Second step: httpd serviceを構成し、スタートさせます。

  - Third step: web.html ファイルを作成します。

このPlaybookは、Apache webserverなどのPackageが`node1`にインストールされているかを確認します。

Playbookの優先されるディレクトリ構造についての[ベストプラクティス](http://docs.ansible.com/ansible/playbooks_best_practices.html) はこちらを参考にしてください。
あなたが、Ansibleニンジャとしてのスキルを磨く時には、これらのプラクティスを読んで理解しておくことを強くお勧めします。
というのも、今日紹介するのはとても基本的なものですし、独自の複雑な構造なものを作ってしまうと混乱するだけだからです。

では、Playbookを非常に単純なディレクトリ構造で作成し、そこに2,3のファイルを追加します。

制御ホスト **ansible**のホームディレクトリ上に、`ansible-files`というディレクトリを作成し、そこに変更を加えていきます。

```bash
[student<X>@ansible ~]$ mkdir ansible-files
[student<X>@ansible ~]$ cd ansible-files/
```

以下の内容の`apache.yml`という名前のファイルを追加してください。
以前の章と同じように、`vi` や `vim` などを用いてください。
エディタの利用に慣れていない方は、[editor intro](../0.0-support-docs/editor_intro.md)をチェックしてみてください。

```yaml
---
- name: Apache server installed
  hosts: node1
  become: yes
```

これは、Ansibleの強みの一つを示しています。
Playbookの構造は、とても簡単で読みやすく、理解しやすいはずです。
例えばこのPlaybookでは以下を読み取ることができます:

  - このPlayの名前は、`name:`で設定されているものです。

  - Playbookが実行されるホストは、`hosts:`で定義されています

  - `become:`でユーザー権限の昇格を有効化しています。

> **Tip**
>
> パッケージをインストールしたり、root権限を必要とする諸々のタスクを実行するには、いうまでもなく権限昇格が必要になります。これは、Playbookが`become: yes`であることで実行可能です。

Playの定義ができたので、何がしかのタスクを追加していきましょう。
Apacheのパッケージの最新版がインストールされていることを確認するタスクを追加します。
次のリストのようにファイルを変更していきましょう。

```yaml
---
- name: Apache server installed
  hosts: node1
  become: yes
  tasks:
  - name: latest Apache version installed
    yum:
      name: httpd
      state: latest
```
> **Tip**
>
> PlaybookはYAMLで書かれているので、行とキーワードの位置関係は極めて重要です。`tasks`の *t*と、`become`の*b*が必ず縦に並ぶようによく確認してください。Ansibleに慣れてきたら、[YAML構文(YAML Syntax)](http://docs.ansible.com/ansible/YAMLSyntax.html)について少し時間をかけて勉強してみると良いでしょう。

追加された行は以下の通りです。:

  - Task箇所はキーワード`tasks`で始まっています。

  - タスクには名前がつけられ、タスクのためのモジュールが参照されています。ここでは、"yum"モジュールが用いられています。

  - モジュールに加えるパラメータが追加されました: `name: `はyumモジュールで管理されるパッケージの名称を指定しています。`state`はそのインストールされるパッケージの望ましい状態を定義しています。

> **Tip**
>
> モジュールのパラメータは、それぞれのモジュールで固有なものです。よくわからない場合には、再度`ansible-doc`コマンドを用いて調べてみてください。

## Step 3 - Playbookを実行してみる

Playbookは、管理ノード上で`ansible-playbook`コマンドを使うことで実行できます。新しいPlaybookを実行する前に、構文エラーを確認しておくことをお勧めします。

```bash
[student<X>@ansible ansible-files]$ ansible-playbook --syntax-check apache.yml
```

エラーがでなければ、これでPlaybookを実行する準備は整ったと言えます。:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook apache.yml
```
ここでは出力に何もエラーが表示されていないはずです。実行されたタスクの概要と実行結果が要約された`play recap`が提供されています。
リストされている中には、"Gathering Facts"と呼ばれるタスクがあると思います。これは、各Playのはじめに自動実行されるあらかじめ組み込またタスクです。
各管理対象ホストに関する様々な情報を収集します。これの説明については後の章で実施します。

SSHを用いて`node1`でApacheが確かにインストールされているかどうかを確認してください。IPアドレスの情報はインベントリに記載されています。IPアドレスを入力してSSHでノードへ接続してください。

```bash
[student<X>@ansible ansible-files]$ grep node1 ~/lab_inventory/hosts
node1 ansible_host=11.22.33.44
[student<X>@ansible ansible-files]$ ssh 11.22.33.44
student<X>@11.22.33.44's password:
Last login: Wed May 15 14:03:45 2019 from 44.55.66.77
Managed by Ansible
[student<X>@node1 ~]$ rpm -qi httpd
Name        : httpd
Version     : 2.4.6
[...]
```

`node1`からログアウトし制御ホストへ戻るには、`exit`コマンドを用いてください。制御ホストに戻ったら、AnsibleのAd-hocコマンドを用いてインストールされているパッケージを確認してみましょう\!

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m command -a 'rpm -qi httpd'
```

Playbookをもう一度実行して、出力結果を比較してみましょう。
先ほど`changed`だった出力は、`ok`へと変わり、色も黄色から緑色に変わったはずです。また、`play recap`の内容も変わりました。
この結果の差により、Ansibleが実際に何を変更したのかを簡単に見つけることができます。

## Step 4 - Playbookを拡張してみよう。Apacheの起動と有効化

Playbookの次のパートでは、確かにApache Webserverが`node1`上で有効でかつ起動していることを確認していきます。

制御ホスト上で、Student Userとして、`~/ansible-files/apache.yml`を編集し、`service`モジュールに２つ目のタスクを追加していきます。Playbookは以下のようになります。

```yaml
---
- name: Apache server installed
  hosts: node1
  become: yes
  tasks:
  - name: latest Apache version installed
    yum:
      name: httpd
      state: latest
  - name: Apache enabled and running
    service:
      name: httpd
      enabled: true
      state: started
```

繰り返しますが、これら追加された行の意味を理解するのは簡単なはずです。

  - 2つ目のタスクが作成され、名前がつけられました。

  - モジュールが指定されています。 (`service`)

  - パラメータが提供されています。

2つ目の追加されたタスクでは、Apacheサーバが実際にターゲットホスト上で実行状態かを確認しています。拡張したPlaybookを実行してみましょう。

```bash
[student<X>@ansible ansible-files]$ ansible-playbook apache.yml
```

出力された結果をみてみてください。
いくつかのタスクは緑色で"OK"と記載され、1つだけ黄色で"changed"と表示されているはずです。
  - もう一度、AnsibleのAd-Hocコマンドを用いてApacheが有効になっておりかつ起動していることを確認します。例えば、`systemctl status httpd`などを実行しましょう。

  - Playbookをもう一度実行して、出力結果が変わる様に慣れてみましょう。

## Step 5 - Playbookを拡張してみよう。web.htmlの作成

タスクが正しく実行され、Apacheが接続を受け付けているのかを確認してみましょう。
管理ノードから、Ad-hocコマンドでAnsibleの`uri`モジュールを使ってHTTPリクエストを実施します。 **\<IP\>** を皆さんの環境のインベントリファイルのノード情報に置き換えて実行することに注意してください。

> **Warning**
>
> **おそらく、たくさんの赤い文字列と403の文字が見えます\!**

```bash
[student<X>@ansible ansible-files]$ ansible localhost -m uri -a "url=http://<IP>"
```

たくさんの赤い列とエラーが表示されたことでしょう。
少なくとも、Apacheが提供すべき`web.html`ファイルがなければとても汚い"HTTP Error 403: Forbidden"ステータスが投げつけられるのはしょうがないことですし、Ansibleもエラーをレポートするはずです。


では、Ansibleを使って`web.html`をデプロイしてみましょう。
管理ノード上で`vim`などを用いて以下の内容の`~/ansible-files/web.html`を作成します。

```html
<body>
<h1>Apache is running fine</h1>
</body>
```

すでに今日の演習で`copy`モジュールを使いコマンドラインからファイルへテキストを入力した経験をしましたね？
それではPlaybookでモジュールを使って、ファイルをコピーしましょう。

管理ノード上で、StudentXユーザとして、`~/ansible-files/apache.yml`を編集し`copy`モジュールを利用する新しいタスクを追加してください。
それは以下のような記述になるはずです。

```yaml
---
- name: Apache server installed
  hosts: node1
  become: yes
  tasks:
  - name: latest Apache version installed
    yum:
      name: httpd
      state: latest
  - name: Apache enabled and running
    service:
      name: httpd
      enabled: true
      state: started
  - name: copy web.html
    copy:
      src: ~/ansible-files/web.html
      dest: /var/www/html/index.html
```

そろそろPlaybookの構文に慣れてきましたか？
では、このPlaybookでは何が起きるでしょうか。
新しいタスクでは、`copy`モジュールを使って、コピー操作のためのコピー元とコピー先のオプションをパラメータとして定義しています。

拡張したPlaybookを実行してみましょう。

```bash
[student<X>@ansible ansible-files]$ ansible-playbook apache.yml
```

  - 出力結果をよくみてください。

  - Apacheをテストするために、先ほどの`uri`モジュールを用いたAd-hocコマンドをもう一度実行してみましょう。コマンドは色々な情報を返していると思いますが、その中でもフレンドリーな緑色で"status: 200"を返しているはずです。

## Step 6 - 練習: 複数ホストへの適用

ここまでのラボはとてもよかったと思いますが、Ansibleの本当に良いところは同じ一連のタスクを様々なホストに確実に適用していくことです。

  - では、Playbook apache.yml を`node1` **と** `node2` **と** `node3`へ実行するように変更してみましょう。


覚えているかもしれませんが、インベントリには全てのノードが`web`グループとしてリストされていました。:

```ini
[web]
node1 ansible_host=11.22.33.44
node2 ansible_host=22.33.44.55
node3 ansible_host=33.44.55.66
```

> **Tip**
>
> 例示されているIPアドレスは単なる例であり、あなたのノードは異なるIPアドレスを持っているはずです。

Playbookをグループ`web`をさすように変更しましょう。

```yaml
---
- name: Apache server installed
  hosts: web
  become: yes
  tasks:
  - name: latest Apache version installed
    yum:
      name: httpd
      state: latest
  - name: Apache enabled and running
    service:
      name: httpd
      enabled: true
      state: started
  - name: copy web.html
    copy:
      src: ~/ansible-files/web.html
      dest: /var/www/html/index.html
```

Playbookを実行してみましょう:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook apache.yml
```

最後に、Apacheが実行された全てのノードで動作しているかどうかを確認してみてください。最初に、インベントリにおいて記載があるそれぞれのノードのIPアドレスを確認します。全てのWebサーバで先ほど`node1`で実行したのと同じように`uri`モジュールを用いたAd-hocコマンドを実行してみましょう。全ての出力結果は先ほどと同じようにグリーンで表示されるはずです。

> **ヒント**
>
> また、Apacheが実行された全てのノードで動作しているかどうかを確認する別方法として`ansible web -m uri -a "url=http://localhost/"`コマンドを実行することもできます。

----

[Ansible Engine ワークショップ表紙に戻る](../README.ja.md#section-1---ansible-engineの演習)
