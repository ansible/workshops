# Workshop Exercise - Ad-hoc コマンドを実行しよう

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

最初の演習では、Ansible がどのように動作するかを学習するために アドホック・コマンド を実行します。
Ansible Ad-hocコマンドは、プレイブックを作成しなくてもリモートノードへのタスク実行を可能にします。
1つか2つ程度のタスクをたくさんのリモートノードに実行する必要がある時などにとても便利なコマンドです。

## Table of Contents

* [Step 1 - インベントリを操作してみよう](#step-1---インベントリを操作してみよう)
* [Step 2 - Ansibleの設定ファイルについて](#step-2---ansibleの設定ファイルについて)
* [Step 3 - Ping a host](#step-3---ping-a-host)
* [Step 4 - モジュールのリストとヘルプを表示しよう](#step-4---モジュールのリストとヘルプを表示しよう)
* [Step 5 - コマンドモジュールを使ってみよう。](#step-5---コマンドモジュールを使ってみよう)
* [Step 6 - Copyモジュールとパーミッション](#step-6---copyモジュールとパーミッション)
* [チャレンジラボ: Modules](#チャレンジラボ-modules)

## Step 1 - インベントリを操作してみよう

ホスト管理にAnsibleコマンドを使用するためには、管理したいホストの一覧を定義したインベントリファイルをコントロールノード上に用意する必要があります。
このラボでは、インベントリファイルはすでにインストラクターによって提供されているはずです。
インベントリはiniフォーマットのファイルで、ホストの情報がリストされています。また、グループやいくつかの変数を提供しています。
実例をみていきましょう。

```bash
[all:vars]
ansible_user=student1
ansible_ssh_pass=PASSWORD
ansible_port=22

[web]
node1 ansible_host=<X.X.X.X>
node2 ansible_host=<Y.Y.Y.Y>
node3 ansible_host=<Z.Z.Z.Z>

[control]
ansible ansible_host=44.55.66.77
```
皆さんのAnsible環境はすでに固有のインベントリを利用するよう設定されています。
次のステップでは、どのように設定されているかを説明します。
今から、インベントリを操作するための簡単なコマンドをいくつか紹介します。

インベントリに記述されているホスト群を参照するには、Ansibleコマンドを用いてホストのパターンを指定します。
`--list-hosts` オプションを用いてみましょう。
このコマンドを用いると、Ansibleコマンドが実行される際にどの管理対象ホストが含まれたホストパターンが参照されるのかを明確にするのに役立ちます。

もっとも基本的なホストパターンは、インベントリファイル内に記載がある管理対象のホスト名です。
この指定方法を用いると、ansibleコマンドによって操作が実行されるホストが、インベントリファイル内の一つのホストだけになります。
では実行してみましょう。

```bash
[student<X@>ansible ~]$ ansible node1 --list-hosts
  hosts (1):
    node1
```

インベントリファイルにはたくさんの情報を含めることができます。
ホストをグループごとにまとめたり、変数を定義することができます。
ここで登場する例では、インベントリには`web`と`control`の2つのグループ名が記載されています。
グループ名やホスト名など様々なパターンでAnsibleを実行して、結果を確認してみましょう。:

```bash
[student<X@>ansible ~]$ ansible web  --list-hosts
[student<X@>ansible ~]$ ansible web,ansible --list-hosts
[student<X@>ansible ~]$ ansible 'node*' --list-hosts
[student<X@>ansible ~]$ ansible all --list-hosts
```

また、システムを1つ以上の複数のグループへ所属させることもできます。
例えば、サーバをwebとdatabaseどちらにも属することができます。
Ansibleでは、グループが常に階層的である必要は無いことに注意してください。

> **Tip**
>
> インベントリには様々なデータを含めることができます。例えば、標準的では無いSSHポートで動作するホストがある場合には、ホスト名の後にコロンをつけて利用したいポート番号を入力できます。もしくは、Ansibleで利用する固有の名前を定義し、それらと実IPを紐付けることもできます。

## Step 2 - Ansibleの設定ファイルについて

Ansibleは、Ansibleがもつini形式の設定ファイルを変更することで、動作をカスタマイズすることができます。
Ansibleはコントロールノード上のいくつかの設定可能な場所の1つから設定ファイルを読み込みます。
こちらの [documentation](https://docs.ansible.com/ansible/latest/reference_appendices/config.html)を参考にしてみてください。

> **Tip**
>
> Ansibleコマンドを実行するディレクトリに`ansible.cfg`ファイルを作成・配置することが推奨されるやり方です。このディレクトリには、インベントリやPlaybookなどみなさんのAnsibleプロジェクトで利用されるファイルも含まれます。他にも、ホームディレクトリに`.ansible.cfg`を作成するやり方もあります。

みなさんに提供されているラボ環境では、コントロールノードの`student <X>`ホームディレクトリに、`ansible.cfg`が必要な詳細な情報が記載され、すでに作成済みです。
以下は`student <X>`ホームディレクトリで実行することに注意してください。

```bash
[student<X>@ansible ~]$ ls -la .ansible.cfg
-rw-r--r--. 1 student<X> student<X> 231 14. Mai 17:17 .ansible.cfg
```

ファイルの内容を出力します。

```bash
[student<X>@ansible ~]$ cat .ansible.cfg
[defaults]
stdout_callback = yaml
connection = smart
timeout = 60
deprecation_warnings = False
host_key_checking = False
retry_files_enabled = False
inventory = /home/student<X>/lab_inventory/hosts
```

このファイルには複数の設定内容が存在しています。
ほとんどの行の解説はここでは触れませんが、出力された内容の最後の行にだけ注意してください:そこには、インベントリの場所が記述されています。これが、Anisbleがこれまでのコマンド実行時にどのマシンが接続できるのかを知っていた理由です。

みなさんに提供されているインベントリの内容を確認してみましょう。

```bash
[student<X>@ansible ~]$ cat /home/student<X>/lab_inventory/hosts
[all:vars]
ansible_user=student<X>
ansible_ssh_pass=ansible
ansible_port=22

[web]
node1 ansible_host=11.22.33.44
node2 ansible_host=22.33.44.55
node3 ansible_host=33.44.55.66

[control]
ansible ansible_host=44.55.66.77
```

> **Tip**
>
> 各受講者はそれぞれ個別のラボ環境を持っていることに注意してください。テキストの結果に表示されているIPアドレスは例であり実際のものではありません。みなさん個々の環境の実際のIPアドレスは異なります。
他の場合と同様に、**\<X\>** をStudent Numberに置き換えてください。

## Step 3 - Ping a host

> **Warning**
>
> **みなさんのラボ環境では、ホームディレクトリ `/home/student<X>`でコマンドを実行することを忘れないでください。 そこは、あなたの `.ansible.cfg`ファイルがあるところです。それなしでは、Ansibleはどのインベントリを使うべきかを知ることはできません。**

基本的なところから始めていきましょう - ホストへのpingです。
Ansibleの`ping`モジュールを使ってみましょう。
この`ping`モジュールは、webホストが確実に反応できるのかどうかを確認できます。
基本的には、管理対象ホストへ接続し、そこで小さなスクリプトを実行させ結果を収集する動作をします。このモジュールが実行できれば、管理対象ホストに到達可能で、Ansibleが対象ホスト上でコマンドを正しく実行できることが確認できています。

> **Tip**
>
> 特定のタスクを実行するために設計されたツールがモジュールだと考えてみてください。

Ansibleでは`ping`モジュールを使うべきです。`-m`オプションを用いてどのAnsibleモジュールを利用するかを定義します。`-a`を使うことで特定の文字列をオプションとしてモジュールに渡すこともできます。

```bash
[student<X>@ansible ~]$ ansible web -m ping
node2 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
[...]
```

結果の通り、各ノードから実行時の動作と結果が通知されます。 - ここでは`pong`が結果です。

## Step 4 - モジュールのリストとヘルプを表示しよう

Ansibleにはたくさんのモジュールが準備されています。全てのモジュールをリストしてみましょう:

```bash
[student<X>@ansible ~]$ ansible-doc -l
```

> **Tip**
>
> `ansible-doc` では、 `q` を押して終了してください。`up`/`down`を用いることで、コンテンツをスクロールすることができます。

モジュールを探したい時には、次のようにしてみてください。:

```bash
[student<X>@ansible ~]$ ansible-doc -l | grep -i user
```

使用例を含む、特定のモジュールのヘルプをみたい時には次のようにします。:

```bash
[student<X>@ansible ~]$ ansible-doc user
```

> **Tip**
>
> 必須のオプションは、`ansible-doc`内では "=" で表現されます。

## Step 5 - コマンドモジュールを使ってみよう。

それでは、`command`モジュールを利用して、古き良きLinuxコマンドを実行し、アウトプットを定型化してみましょう。
これは、管理対象ホスト上でコマンドを単純に実行します。:

```bash
[student<X>@ansible ~]$ ansible node1 -m command -a "id"
node1 | CHANGED | rc=0 >>
uid=1001(student1) gid=1001(student1) Gruppen=1001(student1) Kontext=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
```

ここでは、`command`モジュールを実行していますが、これは`-a`でオプションとして渡された文字列を対象ホストで実行するだけのモジュールです。`all`のホストパターンを使用してこのアドホックなコマンド実行を試してみてください。

その他の例: みなさんのホストで実行されているkernelバージョンを調べてみてください。

```bash
[student<X>@ansible ~]$ ansible all -m command -a 'uname -r'
```

時には、ホストの実行結果を１行にする方が良い時もあるかと思います。:

```bash
[student<X>@ansible ~]$ ansible all -m command -a 'uname -r' -o
```

> **Tip**
>
> 多くのLinuxコマンドのように、`ansible`は短い形式のオプションだけでなく長い形式にも対応しています。 例えば、`ansible web --module-name ping`は、`ansible web -m ping`と同じ意味となります。 このワークショップでは、短縮系のオプションが用いられます。

## Step 6 - Copyモジュールとパーミッション

`copy` モジュールを使って、アドホックコマンドで`node1`の`/etc/motd`ファイルを変更してみましょう。 **このケースでは、コンテンツはオプションを介して、モジュールに渡されます。**

実行してみましょう:

> **Warning**
>
> **おそらく失敗するでしょう!**

```bash
[student<X>@ansible ~]$ ansible node1 -m copy -a 'content="Managed by Ansible\n" dest=/etc/motd'
```

前述の通り、これは*failed*になったはずです。

```bash
    node1 | FAILED! => {
        "changed": false,
        "checksum": "a314620457effe3a1db7e02eacd2b3fe8a8badca",
        "failed": true,
        "msg": "Destination /etc not writable"
    }
```

アドホックコマンドの結果は、赤字で **FAILED!** と表示されているはずです。 なぜでしょうか？ なぜなら、ユーザー **student\<X\>** はmotdファイルの編集を許されていないからです。

これは、権限昇格(privilege escalation)が必要なケースであり、`sudo`が適切に設定されなければならない理由でもあります。`sudo`を用いてrootとしてコマンドを実行するために、`-b`のパラメータを用います。("become"と考えてください)

> **Tip**
>
> Ansibleは、SSHと同じように、現在のユーザ名(今回の場合にはstudent\<X\>)を用いて接続しに行きます。リモートユーザ名を上書きするには`-u`のパラメータを使います。
今回のラボでは、`sudo`がすでに設定済みなので`student<X>` で接続されても問題ありません。`-b`のパラメータを使ってもう一度実行してみましょう。

```bash
[student<X>@ansible ~]$ ansible node1 -m copy -a 'content="Managed by Ansible\n" dest=/etc/motd' -b
```

今度はうまくいったはずです。

```bash
node1 | CHANGED => {
    "changed": true,
    "checksum": "4458b979ede3c332f8f2128385df4ba305e58c27",
    "dest": "/etc/motd",
    "gid": 0,
    "group": "root",
    "md5sum": "65a4290ee5559756ad04e558b0e0c4e3",
    "mode": "0644",
    "owner": "root",
    "secontext": "system_u:object_r:etc_t:s0",
    "size": 19,
    "src": "/home/student1/.ansible/tmp/ansible-tmp-1557857641.21-120920996103312/source",
    "state": "file",
    "uid": 0
```

一般的な`command`モジュールを利用して、motdファイルの内容をチェックしてみましょう。:

```bash
[student<X>@ansible ~]$ ansible node1 -m command -a 'cat /etc/motd'
node1 | CHANGED | rc=0 >>
Managed by Ansible
```
`ansible node1 -m copy …?`コマンドを再実行してみてください。以下の点に着目してみてください:

  - 出力結果は、異なる色だったはずです。(適切な端末の設定がされている場合)
  - `"changed": true,` から `"changed": false,`へ変更されたはずです。
  - 最初の行が、`CHANGED` から `SUCCESS`に変わったはずです。

> **Tip**
>
> これにより、どこが変更されて、Ansibleがなにをやったのかをとても簡単に見つけることができるようになります。

## チャレンジラボ: Modules

  - `ansible-doc`を利用します。

      - ソフトウェアパッケージを管理するために、Yumを利用できるモジュールを見つけてください。

      - 最新バージョンのパッケージをインストールするためにはどうすれば良いのかをヘルプの例から探してみてください。

  - Ansibleのアドホックコマンドを実行して、`node1`に`squid`の最新パッケージをインストールしてみてください。

> **Tip**
>
> copyモジュールで実行したアドホックコマンドを参考にして、モジュールとオプションを変更すると良いでしょう。

> **Warning**
>
> **以下は答えです\!**

```bash
[student<X>@ansible ~]$ ansible-doc -l | grep -i yum
[student<X>@ansible ~]$ ansible-doc yum
[student<X>@ansible ~]$ ansible node1 -m yum -a 'name=squid state=latest' -b
```

----

[Ansible Engine ワークショップ表紙に戻る](../README.ja.md#section-1---ansible-engineの演習)
