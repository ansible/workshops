# ワークショップ演習 - はじめての Playbook の作成

**他の言語でもお読みいただけます**:
<br>![uk](../../../images/uk.png) [English](README.md)、![japan](../../../images/japan.png)[日本語](README.ja.md)、![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md)、![france](../../../images/fr.png) [Française](README.fr.md)、![Español](../../../images/col.png) [Español](README.es.md)

## 目次

* [目的](#目的)
* [ガイド](#ガイド)
  * [ステップ 1 - Playbook の基本](#ステップ-1---playbook-の基本)
  * [ステップ 2 - Playbook 用のディレクトリー構造とファイルの作成](#ステップ-2---playbook-用のディレクトリー構造とファイルの作成)
  * [ステップ 3 - Playbook の実行](#ステップ-3---playbook-の実行)
  * [ステップ 4 - Playbook の拡張: Apache の起動と有効化](#ステップ-4---playbook-の拡張-apache-の起動と有効化)
  * [ステップ 5 - Playbook の拡張: web.html の作成](#ステップ-5---playbook-の拡張-webhtml-の作成)
  * [ステップ 6 - 練習: 複数ホストへの適用](#ステップ-6---練習-複数ホストへの適用)

## 目的

この演習では、Ansible を使用して Red Hat Enterprise Linux 上に 2 つの Apache Web サーバーを構築します。この動画では、以下の Ansible の基礎を取り上げます。

* Ansible モジュールパラメーターについて
* 以下のモジュールの概要および使用
  * [yum モジュール](https://docs.ansible.com/ansible/latest/modules/yum_module.html)
  * [service モジュール](https://docs.ansible.com/ansible/latest/modules/service_module.html)
  * [copyモジュール](https://docs.ansible.com/ansible/latest/modules/copy_module.html)
* [べき等性](https://en.wikipedia.org/wiki/Idempotence) の概要および Ansible モジュールのべき等性について

## ガイド

Playbook は、管理ホストに実装する必要な設定または手順を記述するファイルです。Playbook は、長く複雑な管理タスクを、予測できる成功する結果で、簡単に繰り返し可能なルーチンに変更できます。

1 つの Playbook には複数のプレイを含めることができ、単一または複数のタスクを指定できます。1つのタスクでは、前章のモジュールのように *module* が呼び出されます。*play* の目的は、ホストのグループをマッピングすることです。*task* の目的は、それらのホストにモジュールを実装することです。

> **ヒント**
>
>良い例を紹介します。Ansible モジュールがワークショップでのツールであるとすれば、インベントリーは素材で、Playbook は指示書のようなものです。

### ステップ 1 - Playbook の基本

Playbook は YAML 形式で記述されたテキストファイルなので、以下が必要になります。

* 3 つのダッシュ (`---`) で開始

* タブ**ではなく**、スペースを使用した正しいインデント

重要な点を以下に示します。

* **hosts**: タスクを実行する管理対象ホスト

* **tasks**: Ansible モジュールを呼び出して必要なオプションを渡すことで実行される操作

* **become**: Playbook における特権昇格

> **警告**
>
> Playbook 内のコンテンツの順序は、Ansible が提示された順序でプレイやタスクを実行するため重要です。

Playbook は **冪等** である必要があります。そのため、Playbook を 1 回実行してホストを正しい状態にできるのであれば、2 回目の実行でも安全であるため、ホストをさらに変更する必要はありません。

> **ヒント**
>
> 多くの Ansible モジュールは冪等です。そのため、この作業は比較的簡単です。

### ステップ 2 - Playbook 用のディレクトリー構造とファイルの作成

実践的な説明に移ります。はじめての Ansible Playbook を作成してみましょう。このラボでは、以下の 3 つの手順で Apache Web サーバーをセットアップする Playbook を作成します。

1. httpd のインストール
2. httpd サービスの有効化と起動
3. web.html ファイルを各 Web ホストにコピーします。

この Playbook により、Apache Web サーバーを含むパッケージが `node1` にインストールされます。

Playbook に推奨されるディレクトリー構造についての [ベストプラクティス](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html) があります。Ansible スキルを発展させるためにも、これらのプラクティスを読んで理解することをお勧めします。とはいえ、現在の Playbook は非常に基本的です。複雑な構造を作ると、混乱するだけです。

代わりに、Playbook 用に非常に簡単なディレクトリー構造を作成し、そこにいくつかのファイルを追加します。

コントロールホスト **ansible** で、ホームディレクトリーに `ansible-files` というディレクトリーを作成し、そのディレクトリーにディレクトリーを変更します。

```bash
[student@ansible-1 ~]$ mkdir ansible-files
[student@ansible-1 ~]$ cd ansible-files/
```

以下の内容の `apache.yml` というファイルを追加します。前回の演習でも説明したように、`vi`/`vim` を使います。あるいは、コマンドラインのエディターになれていない場合は、[エディター紹介](../0.0-support-docs/editor_intro.md) を参照してください。

```yaml
---
- name: Apache server installed
  hosts: node1
  become: yes
```

これは、Ansible の強みの 1 つである、Playbook 構文が読みやすく、理解しやすいという特徴を示しています。この Playbook では以下のような特徴があります。

* `name:` からのプレイ用に名前が指定されます。
* Playbook を実行するホストは、`hosts:` で定義します。
* `become:` でユーザー特権昇格を有効にします。

> **ヒント**
>
> 特権昇格は、パッケージのインストールや、root パーミッションが必要な他のタスクの実行に必要です。これは `become: yes` で、Playbook で行います。

プレイは定義できました。次は、何か実行するタスクを追加してみましょう。Apache パッケージが最新バージョンでインストールされていることを yum が確認するタスクを追加します。以下のようにファイルを変更します。

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
> Playbook は YAML で記述されているため、行やキーワードを調整することが重要になります。`task` の *t* は、`become` の *b* に垂直にそろえるようにしてください。Ansible に慣れてきたら、[YAML 構文](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html) を勉強するとよいでしょう。

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

### ステップ 3 - Playbook の実行

Ansible Automation Platform 2 の導入に伴い、開発者の体験全体の一部として、いくつかの新しいキーコンポーネントが導入されています。実行環境は、オートメーションの実行時に使用する予測可能な環境を提供するために導入されました。すべてのコレクションの依存関係は実行環境に含まれ、開発環境で作成されたオートメーションが本番環境と同じように実行されることを確実にしています。

実行環境内で何が見つかるものについて

* RHEL UBI 8
* Ansible 2.9 または Ansible Core 2.11
* Python 3.8
* コンテンツコレクションについて
* Python またはバイナリーの依存関係のコレクション。

実行環境について

オートメーションが実行される環境を定義、構築、配布するための標準的な方法を提供します。一言で言えば、オートメーションの実行環境とは、プラットフォームの管理者が Ansible の管理を容易にするためのコンテナイメージです。

自動化の実行がコンテナー化されていくことを考えると、Ansible Automation Platform 2 以前に存在していた自動化開発のワークフローやツールは、再構築する必要があります。つまり、`ansible-navigator` は、`ansible-playbook` やその他の`ansible-*` コマンドラインユーティリティーに取って代わります。

この変更により、Ansible Playbook はコントロールノードの `ansible-navigator` コマンドを使用して実行されます。

`ansible-navigator` を使用するための前提条件およびベストプラクティスが、このラボで行われています。

これらには以下が含まれます。
* `ansible-navigator` パッケージのインストール
* 全プロジェクトに対するデフォルト設定 `/home/student/.ansible-navigator.yml` の作成（オプション）
* すべての実行環境(EE)ログは `/home/student/.ansible-navigator/logs/ansible-navigator.log` 内に保存されます
* Playbook アーティファクトは `/tmp/artifact.json` 下に保存されます

[Ansible ナビゲーター設定](https://github.com/ansible/ansible-navigator/blob/main/docs/settings.rst) の詳細

> **ヒント**
>
ansible-navigato rのパラメーターは、ユーザーの環境に合わせて変更することができます。現在の設定では、すべてのプロジェクトにデフォルトの`ansible-navigator.yml` を使用していますが、プロジェクトごとに特定の`ansible-navigator.yml` を作成することができ、これは推奨される方法です。

Playbook を実行するには、`ansible-navigator run <playbook>` コマンドを使用します。

```bash
[student@ansible-1 ansible-files]$ ansible-navigator run apache.yml
```

> **ヒント**
>
既存の`ansible-navigator.yml` ファイルでは、インベントリファイルの場所が指定されています。これが`ansible-navigator.yml` ファイル内で設定されていない場合、プレイブックを実行するコマンドは次のようになります。 `ansible-navigator run apache.yml -i /home/student/lab_inventory/hosts`

Playbook の実行時に、現在実行中の Playbook に関する他の情報間でプレイ名を表示するテキストユーザーインターフェース(TUI)が表示されます。

```bash
  PLAY NAME                        OK  CHANGED    UNREACHABLE      FAILED    SKIPPED    IGNORED    IN PROGRESS     TASK COUNT          PROGRESS
0│Apache server installed           2        1              0           0          0          0              0              2          COMPLETE
```

お気づきかもしれませんが、play 名 `Apache server installed` の前に`0` が表示されています。キーボードの `0` キーを押すと、Playbook 完了までに実行されたさまざまなタスクを表示する新しいウィンドウビューが表示されます。この例では、「Gathering Facts」と「latest Apache version installed」のタスクが表示されています。「Gathering Facts」は、各 play の開始時に自動的に実行されるビルトインタスクです。管理対象のノードに関する情報を収集します。この後の演習では、これについて詳しく説明します。「latest Apache version installed」は、`apache.yml` ファイル内に作成されたタスクで、`httpd`をインストールするものでした。

表示は以下のようになります。

```bash
  RESULT      HOST	NUMBER      CHANGED       TASK                                                   TASK ACTION           DURATION
0│OK          node1          0        False       Gathering Facts                                        gather_facts                1s
1│OK          node1          1         True       latest Apache version installed                        yum                         4s
```

よく見ると、各タスクには番号がついています。タスク1の「latest Apache version installed」は、変更があり、`yum` モジュールを使用しています。この場合の変更点は、ホスト`node1` に Apache (`httpd` パッケージ) をインストールしたことです。

キーボードで`0` または`1` を押すと、実行中のタスクの詳細を見ることができます。より伝統的な出力表示が必要な場合は、テキストユーザーインターフェースで `:st` と入力してください。

Ansible Playbook を確認してから、キーボードの Esc キーを使用して TUI から終了できます。

> **ヒント**
>
Esc キーは前の画面に戻るだけです。メインの概要画面でEscキーを押すと、ターミナルウィンドウに戻ります。


Playbook が完了したら、SSH で `node1` に接続し、Apache がインストールされていることを確認します。

```bash
[student@ansible-1 ansible-files]$ ssh node1
Last login: Wed May 15 14:03:45 2019 from 44.55.66.77
Managed by Ansible
```

`rpm -qi httpd` コマンドを使用して、httpd がインストールされていることを確認します。

```bash
[ec2-user@node1 ~]$ rpm -qi httpd
Name        : httpd
Version     : 2.4.37
[...]
```

コントロールホストに戻るように `exit` コマンドで `node1` からログアウトし、package.ymlと名前を付けたAnsible Playbookを作成、実行し、インストールしたパッケージを確認します。

{% raw %}
```yaml
---
- name: Check packages
  hosts: node1
  become: true
  vars:
    package: "httpd"

  tasks:
    - name: Gather the package facts
      ansible.builtin.package_facts:
        manager: auto

    - name: Check whether a {{ package }}  is installed
      ansible.builtin.debug:
        msg: "{{ package }} {{ ansible_facts.packages[ package ][0].version }} is installed!"
      when: "package in ansible_facts.packages"

```
{% endraw %}


```bash
[student@ansible-1 ~]$ ansible-navigator run package.yml -m stdout
```

```bash

PLAY [Check packages] **********************************************************

TASK [Gathering Facts] *********************************************************
ok: [ansible]

TASK [Gather the package facts] ************************************************
ok: [ansible]

TASK [Check whether a httpd  is installed] *************************************
ok: [ansible] => {
    "msg": "httpd 2.4.37 is installed!"
}

PLAY RECAP *********************************************************************
ansible                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

`ansible-navigator run apache.yml` Playbook を 2 回ずつ実行し、出力を比較します。出力「CHANGED」には `1` ではなく `0` が表示され、色が黄色から緑色に変更されます。これにより、Ansible Playbook の実行時に変更が生じると、その変更を簡単に配置できるようになります。

### ステップ 4 - Playbook の拡張: Apache の起動と有効化

Ansible Playbook の次の部分では、Apache アプリケーションが `node1` で有効化されて起動するようにします。

コントロールホストで、`~/ansible-files/apache.yml` を編集し、`service` モジュールを使用して 2 番目のタスクを追加します。実際の Playbook は以下のようになります。

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

何を行ったのでしょうか?

* 「Apache enabled and running」という名前の 2 番目のタスクが作成されます。
* モジュールが指定されます (`service`)
* モジュール `service` はサービス名 (`httpd`) を取ります。これを永続的に設定する必要がある場合は(`enabled`)、および現在の状態 (`started`) を使用します。


つまり、2 番目のタスクにより、Apache サーバーがターゲットマシンで実行されるようにしています。拡張 Playbook を実行します。

```bash
[student@ansible-1 ~]$ ansible-navigator run apache.yml
```

この出力では、プレイに `1` "CHANGED" が表示されますが、`0` を押してプレイの出力に入ることができます。そのタスク 2「Apache enabled and running」は、"CHANGED" 値が True に設定され、黄色でで強調表示されているタスクでした。


* 出力内の変更に慣れるためにも、`ansible-navigator` を使用して Playbook を再び実行してみてください。

* service_state.yml と名前を付けた Ansible Playbook を作成、実行し、`node1` 上で Apache（httpd）サービスが実行されていることを確認します（`systemctl status httpd` と同じように）。

{% raw %}
```yaml
---
- name: Check Status
  hosts: node1
  become: true
  vars:
    package: "httpd"

  tasks:
    - name: Check status of {{ package }} service
      service_facts:
      register: service_state

    - debug:
        var: service_state.ansible_facts.services["{{ package }}.service"].state
```

```bash
{% endraw %}

[student@ansible-1 ~]$ ansible-navigator run service_state.yml
```

### ステップ 5 - Playbook の拡張: web.html の作成

タスクが正しく実行され、Apache が接続を受け入れることを確認します。 Ansible の `uri` モジュールを使用して、コントロールノードから `node1` に HTTP リクエストを作成する、check_httpd.yml という名前の Playbook を作成、実行します。

{% raw %}
```yaml
---
- name: Check URL
  hosts: control
  vars:
    node: "node1"

  tasks:
    - name: Check that you can connect (GET) to a page and it returns a status 200
      uri:
        url: "http://{{ node }}"

```
{% endraw %}

> **警告**
>
> **赤い行と 403 ステータスが多く表示されます。**

```bash
[student@ansible-1 ~]$ ansible-navigator run check_httpd.yml -m stdout
```

赤い行やエラーが多く表示されます。Apache によって提供される `web.html` ファイルがなければ、「HTTP Error 403: Forbidden」ステータスが表示され、Ansible はエラーを報告します。

では、Ansible を使用してシンプルな `web.html` ファイルをデプロイしてはどうでしょうか。ansible コントロールホストで、`student` ユーザーとして `~/ansible-files/` にファイルリソースを保持するディレクトリー `files` を作成します。

```bash
[student@ansible-1 ansible-files]$ mkdir files
```

次に、コントロールノードに `~/ansible-files/files/web.html` ファイルを作成します。

```html
<body>
<h1>Apache は正常に動作しています</h1>
</body>
```

以前の例では、Ansible の `copy` モジュールを使用してコマンドラインに出力されたテキストをファイルに書き込みました。次は、Playbook でモジュールを使用してファイルをコピーします。

コントロールノードで、ファイル `~/ansible-files/apache.yml` を編集して、`copy` モジュールを使用して新しいタスクを追加します。以下のようになります。

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

この新しいコピータスクで何が起きるのでしょうか。この新しいタスクは、`copy` モジュールを使用し、コピー操作のソースオプションおよび宛先オプションをパラメーターとして定義します。

拡張 Playbook を実行します。

```bash
[student@ansible-1 ansible-files]$ ansible-navigator run apache.yml -m stdout
```

* 出力を確認し、「CHANGED」と、その変更に関連するタスクが変更されたことに注意してください。

* 上記の「uri」モジュールを再度使用して playbook (check_httpd.yml) を実行し、Apache をテストします。これで、このコマンドは、その他の情報とともに正常の「status: 200」の行が返されるはずです。

### ステップ 6 - 練習: 複数ホストへの適用

上記では、特定のホストに変更を加えることを簡単に説明しました。では、多くのホストに変更を加えたい場合はどうでしょうか。ここで Ansible の真価が発揮されます。Ansible は、同じタスクセットを多くのホストに確実に適用します。

* そのため、`node1` **と** `node2` **と** `node3`で実行するように apache.yml Playbook を変更するのはどうでしょうか。

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

Playbook の `hosts` パラメーターを、`node1` ではなく `web` を参照するように変更します。

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
[student@ansible-1 ansible-files]$ ansible-navigator run apache.yml -m stdout
```

Apache がすべての Web サーバー（node1、node2、node3）で実行されているかどうかを確認します。すべての出力が緑色である必要があります。

---
**ナビゲーション**
<br>

{% if page.url contains 'ansible_rhel_90' %}
[Previous Exercise](../2-thebasics) - [Next Exercise](../4-variables)
{% else %}
[Previous Exercise](../1.2-thebasics) - [Next Exercise](../1.4-variables)
{% endif %}
<br><br>
[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-1---ansible-engine-exercises)
