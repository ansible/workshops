# 演習 1 - ラボ環境の探索

**他の言語でもお読みいただけます**: ![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English](README.md)、![japan](https://github.com/ansible/workshops/raw/devel/images/japan.png) [日本語](README.ja.md), ![Español](https://github.com/ansible/workshops/raw/devel/images/es.png) [Español](README.es.md)


## 目次

* [目的](#objective)
* [図](#diagram)
* [ガイド](#guide)
   * [ステップ 1 - VS Code を使用した接続](#step-1---connecting-via-vs-code)
   * [ステップ 2 - ターミナルの使用](#step-2---using-the-terminal)
   * [ステップ 3 - 実行環境の検証](#step-3---examining-execution-environments)
   * [ステップ 4 - ansible-navigator
     設定の検証](#step-4---examining-the-ansible-navigator-configuration)
   * [ステップ 5 - インベントリーの検証](#step-5---examining-inventory)
   * [ステップ 6 - インベントリーについて](#step-6---understanding-inventory)
   * [ステップ 7 - ansible-navigator
     を使用したインベントリーの探索](#step-7---using-ansible-navigator-to-explore-inventory)
   * [ステップ 8 - ネットワークデバイスへの接続](#step-8---connecting-to-network-devices)
* [完了](#complete)

## 目的

ラボ環境を調べて理解します。

この最初のいくつかのラボ演は、Ansible Automation Platform
のコマンドラインユーティリティーを使用します。これには、以下が含まれます。

- [ansible-navigator](https://github.com/ansible/ansible-navigator) -
Ansible オートメーションコンテンツを実行・開発するためのコマンドラインユーティリティとテキストベースのユーザーインターフェース（TUI）。-
[ansible-core](https://docs.ansible.com/core.html) - Ansible Automation
Platform
を支えるフレームワーク、言語、機能を提供する基本的な実行ファイルです。また、`ansible`、`ansible-playbook`、`ansible-doc`
などのさまざまなクリエートツールも含まれています。Ansible Coreは、無料でオープンソースのAnsibleを提供する上流のコミュニティと、Red
Hatが提供する下流のエンタープライズオートメーション製品であるAnsible Automation Platformとの橋渡しの役割を果たします。-
[実行環境](https://docs.ansible.com/automation-controller/latest/html/userguide/execution_environments.html)
- このワークショップでは特に取り上げません。なぜなら、ビルトインの Ansible 実行環境には、Red
Hatがサポートするすべてのコレクションがすでに含まれており、このワークショップで使用するすべてのネットワークコレクションも含まれているからです。実行環境とは、Ansible
の実行環境として利用できるコンテナイメージです。-
[ansible-builder](https://github.com/ansible/ansible-builder) -
このワークショップでは特に取り上げませんが、`ansible-builder`
は実行環境の構築プロセスを自動化するためのコマンドラインユーティリティです。

Ansible Automation Platformの新しいコンポーネントに関する情報が必要な場合は、このランディングページをブックマークしてください
[https://red.ht/AAP-20](https://red.ht/AAP-20)

> チャットでコミュニケーションしましょう
>
> 始める前に、slack にご参加ください! <a href="https://join.slack.com/t/ansiblenetwork/shared_invite/zt-3zeqmhhx-zuID9uJqbbpZ2KdVeTwvzw">ansiblenetwork slack に参加するには、こちらをクリック</a>。これにより、他のネットワーク自動化エンジニアとチャットしたり、ワークショップの終了後にサポートを受けたりすることができます。リンクが古くなっている場合は、<a href="mailto:ansible-network@redhat.com">Ansible テクニカルマーケティング</a></th> にメールでご連絡ください。


## 図

![Red Hat Ansible
Automation](https://github.com/ansible/workshops/raw/devel/images/ansible_network_diagram.png)



## ガイド

### ステップ 1 - VS Code を使用した接続

<table>
<thead>
  <tr>
    <th>ワークショップの演習には、Visual Studio Codeの使用が強く推奨されます。Visual Studio Codeは以下を提供します。
    <ul>
    <li> ファイルブラウザ</li>
    <li>構文強調表示の機能付きテキストエディタ</li>
    <li>ブラウザ内ターミナル</li>
    </ul>
    バックアップとして、あるいはVisual Studio Codeでは不十分な場合には、SSHによる直接アクセスが可能です。さらなる説明が必要な場合は、短い YouTube ビデオが用意されています。<a href="https://youtu.be/Y_Gx4ZBfcuk"> Ansible Workshops - ワークベンチ環境へのアクセス</a>
</th>
</tr>
</thead>
</table>

- ワークショップの起動ページ（講師が用意したもの）からVisual Studio
Codeに接続します。パスワードは、WebUIのリンクの下に記載されています。

  ![launch page](images/launch_page.png)

- 接続する提供されたパスワードを入力します。

  ![login vs code](images/vscode_login.png)

- Visual Studio Code で `network-workshop` ディレクトリーを開きます。

  ![picture of file browser](images/vscode-networkworkshop.png)

- `playbook.yml` をクリックしてコンテンツを表示します。

  ![picture of playbook](images/vscode-playbook.png)

### ステップ 2 - ターミナルの使用

- Visual Studio Code でターミナルを開きます。

  ![picture of new terminal](images/vscode-new-terminal.png)

Ansible コントロールノードターミナルで `network-workshop` ディレクトリーに移動します。

```bash
[student@ansible-1 ~]$ cd ~/network-workshop/
[student@ansible-1 network-workshop]$ pwd
/home/student/network-workshop
[student@ansible-1 network-workshop]$
```

* `~` - このコンテキストでのチルダは `/home/student` のショートカットです
* `cd` - ディレクトリーを変更する Linux コマンド
* `pwd` - 作業ディレクトリーを印刷するための Linux コマンド。これにより、現在の作業ディレクトリーへのフルパスが表示されます。

### ステップ 3 - 実行環境の検証

`ansible-navigator` 引数を指定して `images` コマンドを実行し、コントロールノードに設定された実行環境を確認します。

```bash
$ ansible-navigator images
```

![ansible-navigator images](images/navigator-images.png)


> 注記
>
> 表示される出力は、上記の出力とは異なる場合があります

このコマンドは、現在インストールされているすべての実行環境（略してEE）に関する情報を提供します。対応する番号を押すことで、EE
を調べることができます。例えば、上記の例で **0** を押すと、`network-ee` の実行環境が表示されます。

![ee メインメニュー](images/navigator-ee-menu.png)

`2` に `Ansible version and collections` を選択すると、その特定の EE にインストールされたすべての
Ansible Collections と、`ansible-core` のバージョンが表示されます。

![ee info](images/navigator-ee-collections.png)

### ステップ 4 - ansible-navigator 設定の検証

Visual Studio Code を使用して `ansible-navigator.yml` ファイルを開くか、`cat`
コマンドを使用してファイルの内容を表示します。このファイルはホームディレクトリーにあります。

```bash
$ cat ~/.ansible-navigator.yml
---
ansible-navigator:
  ansible:
    inventories:
    - /home/student/lab_inventory/hosts

  execution-environment:
    image: quay.io/acme_corp/network-ee:latest
    enabled: true
    container-engine: podman
    pull-policy: missing
    volume-mounts:
    - src: "/etc/ansible/"
      dest: "/etc/ansible/"
```

`ansible-navigator.yml` ファイル内の次のパラメータに注意してください。

* `inventories`: 使用されている Ansible インベントリーの場所を示します
* `execution-environment`: デフォルトの実行環境が設定されている場所

設定可能なすべての knob
の詳細な一覧については、[ドキュメント](https://ansible-navigator.readthedocs.io/en/latest/settings/)
を参照してください。

### ステップ 5 - インベントリーの検証

`playbook` 内の `play` の範囲は、Ansible **inventory**
内で宣言されたホストのグループに制限されます。Ansible は複数の
[インベントリー](http://docs.ansible.com/ansible/latest/intro_inventory.html)
タイプに対応しています。インベントリーは、その中で定義されたホストのコレクションが含まれるシンプルなファイルや、Playbook
を実行するデバイスのリストを生成する動的スクリプト (CMDBバックエンドのクエリーを行うものなど) が考えられます。

このラボでは、**ini** 形式で記述されたファイルベースのインベントリーを操作します。Visual Studio Code を使用して
`~/lab_inventory/hosts` ファイルを開くか、`cat` コマンドを使用してファイルの内容を表示します。

```bash
$ cat ~/lab_inventory/hosts
```

```bash
[all:vars]
ansible_ssh_private_key_file=~/.ssh/aws-private.pem

[routers:children]
cisco
juniper
arista

[cisco]
rtr1 ansible_host=18.222.121.247 private_ip=172.16.129.86
[arista]
rtr2 ansible_host=18.188.194.126 private_ip=172.17.158.197
rtr4 ansible_host=18.221.5.35 private_ip=172.17.8.111
[juniper]
rtr3 ansible_host=3.14.132.20 private_ip=172.16.73.175

[cisco:vars]
ansible_user=ec2-user
ansible_network_os=ios
ansible_connection=network_cli

[juniper:vars]
ansible_user=ec2-user
ansible_network_os=junos
ansible_connection=netconf

[arista:vars]
ansible_user=ec2-user
ansible_network_os=eos
ansible_connection=network_cli
ansible_become=true
ansible_become_method=enable

[dc1]
rtr1
rtr3

[dc2]
rtr2
rtr4

[control]
ansible ansible_host=13.58.149.157 ansible_user=student private_ip=172.16.240.184
```

### ステップ 6 - インベントリーについて

上記の出力では、すべての `[ ]` がグループを定義しています。たとえば、`[dc1]` は、ホスト `rtr1` と `rtr3`
を含むグループです。グループは _ネスト_ することもできます。グループ `[routers]` はグループ `[cisco]` の親グループです

親グループは、`children`
ディレクティブを使用して宣言されます。ネストされたグループがあると、より具体的な値を変数に柔軟に割り当てることができます。

グループとホストには、変数を関連付けることができます。

> 注記:
>
> ** all ** というグループは常に存在し、インベントリ内で定義されたすべてのグループとホストが含まれます。

ホスト変数は、ホスト自体と同じ行で定義できます。たとえば、ホスト `rtr1` の場合:

```sh
rtr1 ansible_host=18.222.121.247 private_ip=172.16.129.86
```

* `rtr1` - Ansible が使用する名前。これは DNS に依存できますが、必須では必要ありません
* `ansible_host` - ansible が使用する IP アドレス。設定されていない場合は、デフォルトで DNS になります
* `private_ip` - この値は ansible によって予約されていないため、デフォルトで
  [ホスト変数](http://docs.ansible.com/ansible/latest/intro_inventory.html#host-variables)
  になります。この変数は、Playbook で使用することも、完全に無視することもできます。

グループ変数グループは、`vars`
ディレクティブを使用して宣言されます。グループを持つことで、共通の変数を複数のホストに柔軟に割り当てることができます。`[group_name:vars]`
セクションで複数のグループ変数を定義できます。たとえば、グループ `cisco` を見てください。

```sh
[cisco:vars]
ansible_user=ec2-user
ansible_network_os=ios
ansible_connection=network_cli
```

* `ansible_user` - ユーザー ansible
  は、このホストへのログインに使用されます。設定されていない場合は、デフォルトで、プレイブックの実行元のユーザーになります。
* `ansible_network_os` - この変数は、後で説明するように、play 定義内で `network_cli`
  接続タイプを使用するときに必要です。
* `ansible_connection` - この変数は、このグループの
  [接続プラグイン](https://docs.ansible.com/ansible/latest/plugins/connection.html)
  を設定します。これは、この特定のネットワークプラットフォームがサポートするものに応じて、`netconf`、`httpapi`、`network_cli`
  などの値に設定できます。

### ステップ 7 - ansible-navigator を使用したインベントリーの探索

`ansible-navigator` TUI を使用してインベントリーを調べることもできます。

`ansible-navigator inventory` コマンドを実行して、TUI にインベントリーを取り込みます。

![ansible-navigator tui](images/ansible-navigator.png)

キーボードで **0** または **1** を押すと、それぞれグループまたはホストが開きます。

![ansible-navigator groups](images/ansible-navigator-groups.png)

**Esc** キーを押して、上のレベルに移動することができます。または、個々のホストにズームできます。

![ansible-navigator host](images/ansible-navigator-rtr-1.png)

### ステップ 8 - ネットワークデバイスへの接続

ラボ環境には、rtr1、rtr2、rtr3、rtr4 という名前の 4
つのルーターがあります。ネットワークの図は、[ネットワーク自動化ワークショップの目次](../README.md) でいつでも利用できます。SSH
設定ファイル (`~/.ssh/config`)
はすでにコントロールノードにセットアップされています。したがって、コントロールノードから任意のルーターにログインせずに SSH で接続できます。

たとえば、Ansible コントロールノードから rtr1 に接続するには、次のように入力します。

```bash
$ ssh rtr1
```

例:
```
$ ssh rtr1
Warning: Permanently added 'rtr1,35.175.115.246' (RSA) to the list of known hosts.



rtr1#show ver
Cisco IOS XE Software, Version 16.09.02
```

## 完了

ラボ演習 1 を完了しました!  

以下の内容について理解できるようになりました。

* Visual Studio Code を使用してラボ環境に接続する方法
* `ansible-navigator` を使用して **実行環境** を調べる方法
* Ansible Navigator 設定 (`ansible-navigator.yml`) が保管される場所
* インベントリーがコマンドライン演習用に保存されている場所
* ansible-navigator TUI（テキストベースのユーザーインターフェース）の使用方法



---
[次の演習](../2-first-playbook/README.ja.md)

[Ansible Network Automation ワークショップに戻る](../README.ja.md)
