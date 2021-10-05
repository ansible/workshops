# ワークショップ演習 - アドホックコマンドの実行

**その他の言語はこちらをお読みください。**
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## 目次

* [目的](#objective)
* [ガイド](#guide)
* [Step 1 - インベントリの操作](#step-1---work-with-your-inventory)
* [Step 2 - Ansible 設定](#step-2---the-ansible-configuration-files)
* [Step 3 - ホストに ping を実行](#step-3---ping-a-host)
* [Step 4 - モジュールの一覧とヘルプの利用](#step-4---listing-modules-and-getting-help)
* [Step 5 - コマンドモジュールの使用:](#step-5---use-the-command-module)
* [Step 6 - コピーモジュールとパーミッション](#step-6---the-copy-module-and-permissions)
* [チャレンジラボ: モジュール](#challenge-lab-modules)

## 目的

最初の演習では、Ansible の動作の感じをつかむために、いくつかアドホックコマンドを実行します。Ansible Ad-Hoc
コマンドでは、playbook を使わずにリモートノードでタスクを実行できます。これらは、1 つまたは 2
つのことを素早く頻繁に多くのリモートノードに行う必要がある場合に便利です

この演習の内容

* Ansible 設定ファイルの確認と理解 (`ansible.cfg`)
* `ini` 形式のインベントリーファイルの場所の確認と理解
* アドホックコマンドの実行

## ガイド

### Step 1 - インベントリーの操作

ホストの管理に ansible
コマンドを使用するには、インベントリーファイルを指定する必要があります。このファイルは、コントロールノードから管理されるホストの一覧を定義します。このラボでは、インベントリーはインストラクターから渡されます。このインベントリーは
ini 形式のファイルです。このファイルでは、グループで並び替えられたホストの一覧があります。また、変数いくつか指定しています。

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
ansible-1 ansible_host=44.55.66.77
```

Ansible
はすでに、お使いの環境に固有のインベントリーを使用するように設定されています。これを行うための次の手順を説明します。この事典では、簡単なコマンドをいくつか実行して、インベントリーの操作を行います。

インベントリーホストを参照するには、ansible コマンドにホストパターンを指定します。Ansible には `--list-hosts`
オプションがあります。これは、ansible コマンドでホストパターンが参照する管理対象ホストの明確化に役立ちます。

最も基本的なホストパターンは、インベントリーファイルに一覧されている単一の管理対象ホストの名前です。これにより、そのホストが、ansible
コマンドで機能する、インベントリーファイルで唯一のものとなるように指定されます。以下を実行します。

```bash
[student<X>@ansible-1 ~]$ ansible node1 --list-hosts
  hosts (1):
    node1
```

インベントリーファイルにはより多くの情報が含まれます。また、このファイルは、グループでホストを整理したり、変数を定義したりできます。この例では、現在のインベントリーにグループ
`web` と `control` がります。Ansible をこれらのホストパターンで実行し、出力を確認します。

```bash
[student<X>@ansible-1 ~]$ ansible web  --list-hosts
[student<X>@ansible-1 ~]$ ansible web,control --list-hosts
[student<X>@ansible-1 ~]$ ansible 'node*' --list-hosts
[student<X>@ansible-1 ~]$ ansible all --list-hosts
```

ご覧の通り、1 つ以上のグループにシステムを追加できます。たとえば、サーバーは Web サーバーとデータベースサーバーの両方が可能です。Ansible
では、グループが必ずしも階層階層にあるわけではないことに注意してください。

> **ヒント**
>
> このイベントリーには、その他のデータを含めることができます。たとえば、標準以外の SSH ポートで実行するホストがある場合は、コロン付きのホスト名の後にポート番号を指定できます。あるいは、Ansible 固有の名前を定義して、真の IP またはホスト名に参照するようにできます。

### Step 2 - Ansible 設定ファイル

Ansible の動作は、Ansible の ini スタイル設定ファイルの内容を変更してカスタマイズできます。Ansible
は、コントロールノードの利用可能な複数の場所から設定ファイルを選択します。[ドキュメント](https://docs.ansible.com/ansible/latest/reference_appendices/config.html).

> **ヒント**
>
> 推奨される方法としては、Ansible コマンドを実行するディレクトリーに `ansible.cfg` ファイルを作成します。このディレクトリーは、イベントリーや Playbook などの Ansible プロジェクトによって使用されるファイルも含まれます。別の方法としては、`.ansible.cfg` をホームディレクトリーに作成します。

利用するラボ環境では、`.ansible.cfg` ファイルに、コントロールノード上の `student<X>` ユーザーのホームディレクトリーに、必要の詳細が書かれたファイルがすでに作成されています。

```bash
[student<X>@ansible-1 ~]$ ls -la .ansible.cfg
-rw-r--r--. 1 student<X> student<X> 231 14. Mai 17:17 .ansible.cfg
```

ファイルの内容を出力します。

```bash
[student<X>@ansible-1 ~]$ cat .ansible.cfg
[defaults]
stdout_callback = community.general.yaml
connection = smart
timeout = 60
deprecation_warnings = False
host_key_checking = False
retry_files_enabled = False
inventory = /home/student<X>/lab_inventory/hosts
```

設定フラグは複数存在しますが、ここで重要ではありません。ただし、最後の行 (インベントリーの場所など)
には注意してください。これにより、以前のコマンドから、Ansible がどのマシンに接続するかを判断できます。

専用のインベントリーの内容を出力します。

```bash
[student<X>@ansible-1 ~]$ cat /home/student<X>/lab_inventory/hosts
[all:vars]
ansible_user=student<X>
ansible_ssh_pass=ansible
ansible_port=22

[web]
node1 ansible_host=11.22.33.44
node2 ansible_host=22.33.44.55
node3 ansible_host=33.44.55.66

[control]
ansible-1 ansible_host=44.55.66.77
```

> **ヒント**
>
> 各学習者には個別のラボ環境があります。上記の IP アドレスはサンプル用のものです。個々の環境の実際の IP アドレスは異なります。その他の場合には、**\<X\>** を実際の学習者番号に置き換えてください。

### Step 3 - ホストへの ping の実行

> **警告**
>
> **学習者ユーザーのホームディレクトリー `.ansible.cfg` からコマンドを実行することを忘れないでください。このディレクトリーに `/home/student<X>` があります。これがないと、Ansible は、使用するインベントリーを見つけられません。**

まずは、ホストに ping を実行するという基本的なことから始めます。これには、Ansible `ping` モジュールを使用します。`ping`
モジュールでは、ターゲットホストが応答するかどうかを確認できます。実際には、管理対象ホストに接続し、小さなスクリプトを実行して、結果を収集します。これにより、管理対象ホストが到達可能で、Ansible
がその環境で適切にコマンドを実行できるかどうかを確認できます。

> **ヒント**
>
> モジュールは、特定のタスクを行うためにデザインされたツールと考えてください。

Ansible は、`ping` モジュールを使用する必要があることを認識していなければなりません。`-m` オプションは、使用する Ansible
モジュールを定義します。オプションは、`-a` オプションを使用して、指定したモジュールに渡すことができます。

```bash
[student<X>@ansible-1 ~]$ ansible web -m ping
node2 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
[...]
```

各ノードが正常な実行と実際の結果 (ここでは「pong」) を報告します。

### Step 4 - モジュールの一覧表示とヘルプの利用

Ansible では、デフォルトで多くのモジュールを利用できます。実行するモジュールを一覧表示するには、以下を実行します。

```bash
[student<X>@ansible-1 ~]$ ansible-doc -l
```

> **ヒント**
>
> `ansible-doc` で、`q` ボタンを押して終了します。`up`/`down` 矢印を使用してコンテンツをスクロールします。

モジュールを確認するには、次のコマンドを実行します。

```bash
[student<X>@ansible-1 ~]$ ansible-doc -l | grep -i user
```

使用例を含む特定のモジュールのヘルプを取得します。

```bash
[student<X>@ansible-1 ~]$ ansible-doc user
```

> **ヒント**
>
> 必須のオプションは、`ansible-doc` では "=" でマークされています。

### Step 5 - コマンドモジュールの使用

次に、`command` モジュールを使用して、お約束の Linux
コマンドの実行方法や出力のフォーマット方法を見ていきます。管理対象ホスト上で指定したコマンドを実行するだけです。

```bash
[student<X>@ansible-1 ~]$ ansible node1 -m command -a "id"
node1 | CHANGED | rc=0 >>
uid=1001(student1) gid=1001(student1) Gruppen=1001(student1) Kontext=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
```

この場合、このモジュールは `command` と呼ばれ、`-a` で渡されるオプションは、実行する実際のコマンドです。`all`
ホストパターンを使用して、すべての管理対象ホストでこのアドホックコマンドの実行を試行してください。

別の例: ホストを実行しているカーネルバージョンを簡単に確認します。

```bash
[student<X>@ansible-1 ~]$ ansible all -m command -a 'uname -r'
```

ホストの出力は、1 行で行うのが望ましい場合もあります。

```bash
[student<X>@ansible-1 ~]$ ansible all -m command -a 'uname -r' -o
```

> **ヒント**
>
> 多くの Linux コマンドのように、`ansible` では、長いオプションを短くすることもできます (例: `ansible web --module-name ping` は `ansible web -m ping` と同じ)。ワークショップでは、短い形式を使用します。

### Step 6 - コピーモジュールとパーミッション

`copy` モジュールを使用して、`node1` でアドホックコマンドを実行し、`/etc/motd`
ファイルの内容を変更します。**この場合、コンテンツはオプションを介してモジュールに送信されます**。

以下のコマンドを実行します。ただし、**エラー発生は想定内です**。

```bash
[student<X>@ansible-1 ~]$ ansible node1 -m copy -a 'content="Managed by Ansible\n" dest=/etc/motd'
```

説明したように、**エラー**が発生します。

```bash
    node1 | FAILED! => {
        "changed": false,
        "checksum": "a314620457effe3a1db7e02eacd2b3fe8a8badca",
        "failed": true,
        "msg": "Destination /etc not writable"
    }
```

アドホックコマンドの出力では、**FAILED**が赤く表示されます。なぜでしょうか。これは、ユーザー**student\<X\>** による、motd ファイルへの書き込みが許可されていないためです。

この場合、権限昇格が必要となります。また、`sudo` を正しく設定することが重要というリマインダーでもあります。root
としてコマンドを実行するには、`-b` (become) パラメーターを指定して `sudo` を実行するように Ansible
に命令する必要があるのです。

> **ヒント**
>
> Ansible は、SSH と同じように、現在のユーザー名 (student\<X\>) を使用してマシンへの接続を行います。リモートユーザー名をオーバーライドするには、`-u` パラメーターを使用できます。

我々の環境では、`sudo` が設定されているため、`student<X>` として接続できます。このコマンドを変更して `-b` パラメーターを指定し、再度実行します。

```bash
[student<X>@ansible-1 ~]$ ansible node1 -m copy -a 'content="Managed by Ansible\n" dest=/etc/motd' -b
```

今回は失敗しません。

```text
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

汎用の `command` モジュールとともに Ansible を使用して、motd ファイルの内容を確認します。

```bash
[student<X>@ansible-1 ~]$ ansible node1 -m command -a 'cat /etc/motd'
node1 | CHANGED | rc=0 >>
Managed by Ansible
```

上記の `ansible node1 -m copy …​` コマンドを再度実行します。注記:

* 異なる出力色 (正しいターミナル設定が指定されています)。
* `"changed": true,` から `"changed": false,` への変更。
* 最初の行は、`SUCCESS` ではなく、`CHANGED` を示します。

> **ヒント**
>
> これにより、変更や、Ansible の実際の動作の確認が容易になります。

### チャレンジラボ: モジュール

* `ansible-doc` の使用

  * Yum を使用してソフトウェアパッケージを管理するモジュールを見つけます。
  * モジュールのヘルプ例を参照して、最新バージョンのパッケージのインストール方法を説明します。

* Ansible のアドホックコマンドを実行して、`node1` に最新の squid パッケージをインストールします。

> **ヒント**
>
> 上記のアドホックコマンドをテンプレートしてコピーして、モジュールとオプションを変更します。

> **警告**
>
> **回答を以下に示します。**

```bash
[student<X>@ansible-1 ~]$ ansible-doc -l | grep -i yum
[student<X>@ansible-1 ~]$ ansible-doc yum
[student<X>@ansible-1 ~]$ ansible node1 -m yum -a 'name=squid state=latest' -b
```

---
**ナビゲーション**
<br>
[前の演習](../1.1-setup) - [次の演習](../1.3-playbook)

[こちらをクリックして、Ansible for Red Hat Enterprise Linux Workshop
に戻ります](../README.md)
