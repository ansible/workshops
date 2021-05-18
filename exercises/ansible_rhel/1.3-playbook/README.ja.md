# ワークショップ演習 - はじめての Playbook を書く

**その他の言語はこちらをお読みください。**
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## 目次

* [目的](#objective)
* [ガイド](#guide)
  * [Step 1 - Playbook の基本](#step-1---playbook-basics)
  * [Step 2 - Playbook
    のディレクトリー構造とファイルの作成](#step-2---creating-a-directory-structure-and-file-for-your-playbook)
  * [Step 3 - Playbook の実行](#step-3---running-the-playbook)
  * [Step 4 - Playbook の拡張: Apache
    の起動と有効化](#step-4---extend-your-playbook-start--enable-apache)
  * [Step 5 - Playbook の拡張: web.html
    の作成](#step-5---extend-your-playbook-create-an-indexhtml)
  * [Step 6 - 練習: 複数ホストへの適用](#step-6---practice-apply-to-multiple-host)

## 目的

この演習では、Ansible を使用して Red Hat Enterprise Linux 上に 2 つの Apache Web
サーバーを構築します。この動画では、以下の Ansible の基礎を取り上げます。

* Ansible モジュールパラメーターについて
* 以下のモジュールの概要および使用
  * [yum
    モジュール](https://docs.ansible.com/ansible/latest/modules/yum_module.html)
  * [サービスモジュール](https://docs.ansible.com/ansible/latest/modules/service_module.html)
  * [コピーモジュール](https://docs.ansible.com/ansible/latest/modules/copy_module.html)
* [冪等](https://en.wikipedia.org/wiki/Idempotence) と、Ansible モジュールの冪等について

## ガイド

Ansible
アドホックコマンドは単純な操作に便利ですが、複雑な設定管理やオーケストレーションのシナリオには適していません。このようなユースケースには、*Playbooks*
を使用します。

Playbook は、管理ホストに実装する必要な設定または手順を記述するファイルです。Playbook
は、長く複雑な管理タスクを、予測できる成功する結果で、簡単に繰り返し可能なルーチンに変更できます。

Playbook は、実行するアドホックコマンドの一部を取り、*plays* および *tasks* の反復可能なセットに配置できます。

1 つの Playbook には複数のプレイを含めることができ、単一または複数のタスクを指定できます。1つのタスクでは、前章のモジュールのように
*module* が呼び出されます。*play* の目的は、ホストのグループをマッピングすることです。*task*
の目的は、それらのホストにモジュールを実装することです。

> **ヒント**
>
>良い例を紹介します。Ansible モジュールがワークショップでのツールであるとすれば、インベントリーは素材で、Playbook は指示書のようなものです。

### Step 1 - Playbook の基本

Playbook は YAML 形式で記述されたテキストファイルなので、以下が必要になります。

* 3 つのダッシュ (`---`) で開始

* タブ**ではなく**、スペースを使用した正しいインデント

重要な点を以下に示します。

* **hosts**: タスクを実行する管理対象ホスト

* **tasks**: Ansible モジュールを呼び出して必要なオプションを渡すことで実行される操作。

* **become**: アドホックコマンドで `-b` を指定するのと同じように、Playbook での権限昇格。

> **警告**
>
> Playbook 内のコンテンツの順序は、Ansible が提示された順序でプレイやタスクを実行するため重要です。

Playbook は **冪等** である必要があります。そのため、Playbook を 1 回実行してホストを正しい状態にできるのであれば、2
回目の実行でも安全であるため、ホストをさらに変更する必要はありません。

> **ヒント**
>
> 多くの Ansible モジュールは冪等です。そのため、この作業は比較的簡単です。

### Step 2 - Playbook 用のディレクトリー構造とファイルの作成

実践的な説明に移ります。はじめての Ansible Playbook を作成してみましょう。このラボでは、以下の 3 つの手順で Apache Web
サーバーをセットアップする Playbook を作成します。

1. httpd のインストール
2. httpd サービスの有効化と起動
3. web.html ファイルを各 Web ホストにコピーします。

この Playbook により、Apache Web サーバーを含むパッケージが `node1` にインストールされます。

Playbook に推奨されるディレクトリー構造についての
[ベストプラクティス](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)
があります。Ansible スキルを発展させるためにも、これらのプラクティスを読んで理解することをお勧めします。とはいえ、現在の Playbook
は非常に基本的です。複雑な構造を作ると、混乱するだけです。

代わりに、Playbook 用に非常に簡単なディレクトリー構造を作成し、そこにいくつかのファイルを追加します。

コントロールホスト **ansible** で、ホームディレクトリーに `ansible-files`
というディレクトリーを作成し、そのディレクトリーにディレクトリーを変更します。

```bash
[student<X>@ansible-1 ~]$ mkdir ansible-files
[student<X>@ansible-1 ~]$ cd ansible-files/
```

以下の内容の `apache.yml` というファイルを追加します。前回の演習でも説明したように、`vi`/`vim`
を使います。あるいは、コマンドラインのエディターになれていない場合は、[エディター紹介](../0.0-support-docs/editor_intro.md)
を参照してください。

```yaml
---
- name: Apache server installed
  hosts: node1
  become: yes
```

これは、Ansible の強みの 1 つである、Playbook 構文が読みやすく、理解しやすいという特徴を示しています。この Playbook
では以下のような特徴があります。

* `name:` からのプレイ用に名前が指定されます。
* Playbook を実行するホストは、`hosts:` で定義します。
* `become:` でユーザー特権昇格を有効にします。

> **ヒント**
>
> 特権昇格は、パッケージのインストールや、root パーミッションが必要な他のタスクの実行に必要です。これは `become: yes` で、Playbook で行います。

プレイは定義できました。次は、何か実行するタスクを追加してみましょう。Apache パッケージが最新バージョンでインストールされていることを yum
が確認するタスクを追加します。以下のようにファイルを変更します。

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

> **ヒント**
>
> Playbook は YAML で記述されているため、行やキーワードを調整することが重要になります。`task` の *t* は、`become` の *b* に垂直にそろえるようにしてください。Ansible に慣れてきたら、[YAML 構文](http://docs.ansible.com/ansible/YAMLSyntax.html) を勉強するとよいでしょう。

追加した行:

* `tasks:` というキーワードでタスクの一部を開始しました。
* タスクには名前が付けられ、タスクのモジュールが参照されます。ここでは、`yum` モジュールを使用します。
* モジュールのパラメーターが追加されます。
  * パッケージ名を識別する `name:`
  * パッケージの必要状態を定義する `state:`

> **ヒント**
>
> モジュールパラメーターは、各モジュールに個別で指定します。不明な場合は、`ansible-doc` で再度確認します。

Playbook を保存し、エディターを終了します。

### Step 3 - Playbook の実行

Ansible Playbook は、コントロールノードで `ansible-playbook` コマンドを使用して実行されます。新しい
Playbook を実行する前に、構文エラーをチェックすることが推奨されます。

```bash
[student<X>@ansible-1 ansible-files]$ ansible-playbook --syntax-check apache.yml
```

これで、Playbook を実行する準備が整いました。

```bash
[student<X>@ansible-1 ansible-files]$ ansible-playbook apache.yml
```

この出力はエラーを報告しませんが、実行されたタスクの概要と、実行内容の概要をまとめたプレイ要約を示します。また、「Gathering
Facts」というタスクもあります。これは、各プレイの開始時に自動的に実行される組み込みタスクです。これは、管理対象ノードの情報を収集します。詳細は、後の演習で扱います。

SSH で `node1` に接続し、Apache がインストールされていることを確認します。

```bash
[student<X>@ansible-1 ansible-files]$ ssh node1
Last login: Wed May 15 14:03:45 2019 from 44.55.66.77
Managed by Ansible
```

`rpm -qi httpd` コマンドを使用して、httpd がインストールされていることを確認します。

```bash
[student<X>@node1 ~]$ rpm -qi httpd
Name        : httpd
Version     : 2.4.6
[...]
```

コントロールホストに戻るように `exit` コマンドで `node1` からログアウトし、インストールしたパッケージを Ansible
アドホックコマンドで確認します。

```bash
[student<X>@ansible-1 ansible-files]$ ansible node1 -m command -a 'rpm -qi httpd'
```

Playbook を 2 回実行し、出力を比較します。出力は「changed」から「ok」に変更され、色は黄色から緑色に変わります。さらに、「PLAY
RECAP」が変わりました。これにより、Ansible の実際の内容を簡単に識別できるようになります。

### Step 4 - Playbook の拡張: Apache の起動と有効化

Ansible Playbook の次の部分では、Apache アプリケーションが `node1` で有効化されて起動するようにします。

コントロールホストで、`~/ansible-files/apache.yml` を編集し、`service` モジュールを使用して 2
番目のタスクを追加します。実際の Playbook は以下のようになります。

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

これらの行で実行されることは、簡単に理解できます。

* 次のタスクが作成され、名前が付けられます。
* モジュールが指定されます (`service`)
* モジュールのパラメーターが指定されます

つまり、2 番目のタスクにより、Apache サーバーがターゲットマシンで実行されるようにしています。拡張 Playbook を実行します。

```bash
[student<X>@ansible-1 ansible-files]$ ansible-playbook apache.yml
```

出力に注意してください。一部のタスクは緑色で「ok」と表示されています。また、黄色で「changed」と表示されているものもあります。

* Ansible のアドホックコマンドを使用して、Apache が有効化され、起動していることを確認します (例: `systemctl status
  httpd`)。

* 出力内の変更に慣れるためにも、Playbook を再び実行してみてください。

### Step 5 - Playbook: web.html の作成

タスクが正しく実行され、Apache が接続を受け入れることを確認します。コントロールノードのアドホックコマンドで Ansible の `uri` モジュールを使用して HTTP リクエストを作成します。**\<IP\>** は、インベントリーから `ノード1` の IP に置き換えてください。

> **警告**
>
> **赤い行と 403 ステータスが多く表示されます。**

```bash
[student<X>@ansible-1 ansible-files]$ ansible localhost -m uri -a "url=http://<IP>"
```

赤い行やエラーが多く表示されます。Apache によって提供される `web.html` ファイルがなければ、「HTTP Error 403:
Forbidden」ステータスが表示され、Ansible はエラーを報告します。

では、Ansible を使用してシンプルな `web.html` ファイルをデプロイしてはどうでしょうか。ansible コントロールホストで、`student<X>` ユーザーとして `~/ansible-files/` にファイルリソースを保持するディレクトリー `files` を作成します。

```bash
[student<X>@ansible-1 ansible-files]$ mkdir files
```

次に、コントロールノードに `~/ansible-files/files/web.html` ファイルを作成します。

```html
<body>
<h1>Apache は正常に動作しています</h1>
</body>
```

Ansible の `copy` モジュールを使用してコマンドラインに出力されたテキストをファイルに書き込みました。次は、Playbook
でモジュールを使用してファイルを実際にコピーします。

コントロールノードで、ファイル `~/ansible-files/apache.yml` を編集して、`copy`
モジュールを使用して新しいタスクを追加します。以下のようになります。

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
      src: web.html
      dest: /var/www/html/index.html
```

Playbook 構文に慣れてきたのではないでしょうか。この新しいタスクは、`copy`
モジュールを使用し、コピー操作のソースオプションおよび宛先オプションをパラメーターとして定義します。

拡張 Playbook を実行します。

```bash
[student<X>@ansible-1 ansible-files]$ ansible-playbook apache.yml
```

* 出力をよく確認してみてください。

* 上記の「uri」モジュールを再度使用してアドホックコマンドを実行し、Apache
  をテストします。これで、このコマンドは、その他の情報とともに正常の「status: 200」の行が返されるはずです。

### Step 6 - 複数のホストに適用

単一のホストへの操作もよいのですが、Ansible の真の力は、複数の同じタスクを多数のホストに確実に適用できることです。

* そのため、`node1` **と** `node2` **と** `node3`で実行するように apache.yml Playbook
  を変更するのはどうでしょうか。

覚えているとおもいますが、インベントリーは、すべてのノードをグループ `web` のメンバーとして一覧表示します。

```ini
[web]
node1 ansible_host=11.22.33.44
node2 ansible_host=22.33.44.55
node3 ansible_host=33.44.55.66
```

> **ヒント**
>
> こちらに表示される IP アドレスは例です。実際のノードの IP アドレスは異なります。

Playbook がグループ「web」を参照するように変更します。

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
      src: web.html
      dest: /var/www/html/index.html
```

次に Playbook を実行します。

```bash
[student<X>@ansible-1 ansible-files]$ ansible-playbook apache.yml
```

最後に、Apache が両方のサーバーで現在実行されているかどうかを確認します。まずは、インベントリー内のノードの IP アドレスを調べ、上記の
`node1` ですで行ったように uri モジュールを使用して、各アドホックコマンドに使用します。

> **ヒント**
>
>Apache が両方のサーバーで実行されていることを確認する代替方法は `ansible node2,node3 -m uri -a "url=http://localhost/"` コマンドを使用することです。

---
**ナビゲーション**
<br>
[前の演習](../1.2-adhoc) - [次の演習](../1.4-variables)

[こちらをクリックして Ansible for Red Hat Enterprise Linux Workshop
に戻ります](../README.md#section-1---ansible-engine-exercises)
