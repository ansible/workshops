# Exercise 1 - ラボ環境の確認

**別の言語で読む**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

## Table of Contents

- [Objective](#objective)
- [Diagram](#diagram)
- [Guide](#guide)
- [Takeaways](#takeaways)

# Objective

ラボ環境を確認して理解します。この演習は以下を含みます。
- コントロールノードで稼働する Ansible バージョンを確認します。
- Ansible の設定ファイル (`ansible.cfg`)を理解する。
- `ini` 形式のインベントリーファイルを理解する。

演習を開始する前にぜひSlackへ参加してみましょう。[日本のAnsibleコミュニティ](https://ansible-users.connpass.com) [日本のAnsible slack コミュニティ](https://ansiblejp.slack.com/join/shared_invite/enQtNzQwNTEyNTc2Mjc3LTRmYzBkY2FhM2RhOGIzNjVhYTczMDdiODY0YWFiMjdmMGRkNGJiZDYzN2I4M2NjZDA5MjkxYzU3ZWQyMzFhYjU) [海外のAnsible slack コミュニティ](https://join.slack.com/t/ansiblenetwork/shared_invite/enQtNTU4ODIyNzA1MDkyLThiYmQ3MmNkMWRmOTdjYjMxNzdlNDc4OTk5YTc1ZDBiNDAwOTZlZjE0NDliODJiMjJhMDBkZWM4Nzg2NjkzNDA)。参加すると他の自動化エンジニアと交流し、情報交換することが可能です。

# Diagram

![Red Hat Ansible Automation Lab Diagram](../../../images/network_diagram.png)

この環境には rtr1, rtr2, rtr3, rtr4 と名付けられた4つのルーターがあります。[この図](../README.ja.md)はワークショップ中にいつでも参照できます。SSH設定ファイル (~/.ssh/config)は設定済みで、コントローラーノードから各ルーターへ簡単に接続できるようになっています。

例えば、コントローラーノードから rtr1 へ接続する場合は、以下のように入力します:

```bash
[student1@ansible ~]$ ssh rtr1
```

この環境ではユーザー名、パスワードを入力する必要はありません。

# Guide

## Step 1

コントローラーノードの `network-workshop` ディレクトリへ移動します。プロンプトの `ansible` はホスト名を示し、これは正しいノード上にいることを示しています。

```
[student1@ansible ~]$ cd ~/network-workshop/
[student1@ansible network-workshop]$
[student1@ansible network-workshop]$ pwd
/home/student1/network-workshop
```
 - `~` - チルダはホームディレクトリ `/home/student1` の短縮表記
 - `cd` - ディレクトリを移動するコマンド
 - `pwd` - 現在のディレクトリを表示するコマンドで、フルパスが表示されます。

## Step 2

`ansible` コマンドを `--version` オプションをつけて実行すると、Ansible に関する情報を確認することができます:

```
[student1@ansible ~]$ ansible --version
ansible 2.8.1
  config file = /home/student1/.ansible.cfg
  configured module search path = [u'/home/student1/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /usr/bin/ansible
  python version = 2.7.5 (default, Jun 11 2019, 12:19:05) [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
```

> Note: Ansibleのバージョンは上記の表示と異なる場合があります。

このコマンドはAnsibleのバージョン、実行ファイルの場所、Pythonのバージョン、モジュールの検索パスと `ansible の設定ファイル` の場所を表示します。

## Step 3

`cat` コマンドで `ansible.cfg` ファイルの内容を確認します(実際の環境の値とは異なる部分があるかもしれませんが演習には影響はありません)。

```
[student1@ansible ~]$ cat ~/.ansible.cfg
[defaults]
stdout_callback = yaml
connection = smart
timeout = 60
deprecation_warnings = False
host_key_checking = False
retry_files_enabled = False
inventory = /home/student1/lab_inventory/hosts
[persistent_connection]
connect_timeout = 60
command_timeout = 60
```

`ansible.cfg` に含まれる以下の値に注意してください:

 - `inventory`: Ansibleインベントリーファイルの場所が示されます。

## Step 4

`playbook` の `play` のスコープは **インベントリー** で宣言されたグループに制限されます。Ansible は複数の [インベントリー](http://docs.ansible.com/ansible/latest/intro_inventory.html) タイプをサポートしています。インベントリーはPlaybookの対象となるホストの一覧を持つシンプルなフラットファイルです。それ以外に、ホストの一覧を返すスクリプト（裏側でCMDBに問い合わせを行う）も利用可能です。

この演習では **ini** 形式で記述されたファイルベースのインベントリーを利用します。`cat` コマンドを利用して演習環境のインベントリーを確認してみます。

```bash
[student1@ansible ~]$ cat ~/lab_inventory/hosts
```

```
[all:vars]
ansible_ssh_private_key_file=/home/student1/.ssh/aws-private.pem

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
ansible ansible_host=13.58.149.157 ansible_user=student1 private_ip=172.16.240.184
```

## Step 5

上記の出力では、すべての `[ ]` はグループを定義しています。例えば `[dc1]` はホスト `rtr1` と `rtr3` を含むグループです。グループは _ネスト_ することが可能です。`[routers]` グループは `[cisco]` の親グループになります。

> 親グループは `children` ディレクティブを使って宣言されます。ネストされたグループを用いると、柔軟な変数割当が可能となります。


> Note: **all** というグループは常に存在し、インベントリー内で定義された全てのグループとホストを含みます。


変数をグループやホストへと割り当てることが可能です。

ホスト変数はホスト自身の定義と同じ行で定義できます。例えば、`rtr1` では:

```
rtr1 ansible_host=18.222.121.247 private_ip=172.16.129.86
```

 - `rtr1` - Ansibleが使う名前で、DNSと連携する必要はありません。
 - `ansible_host` - Ansibleが接続に利用するIPアドレス。指定しない場合は、名前をDNSへ問い合わせます。
 - `private_ip` - ユーザーが定義した [ホスト変数](http://docs.ansible.com/ansible/latest/intro_inventory.html#host-variables) で、この値をPlaybook内で使うことができるようになります。もしくは、全く無視してしまっても問題ありません。

グループ変数は `vars` ディレクティブで宣言できます。グループ変数を使うと、複数のホストに共通の値を柔軟に指定できます。グループ変数は `[group_name:vars]` セクション以下で定義されます。例として `cisco` を見てみます:

```
[cisco:vars]
ansible_user=ec2-user
ansible_network_os=ios
ansible_connection=network_cli
```

 - `ansible_user` - Ansibleがこのホスト/グループにログインするために利用するユーザー名で、設定されていない場合はデフォルトでPlaybookを実行したユーザーの名前が利用されます。
 - `ansible_network_os` - この次に定義されている `network_cli` コネクションタイプが利用される場合にこの定義は必須となります。
 - `ansible_connection` - この変数は [connection plugin](https://docs.ansible.com/ansible/latest/plugins/connection.html) をこのグループに設定します。これは `netconf`, `httpapi` `network_cli` など対象のネットワークプラットフォームがサポートしている形式を設定します。


# Complete

以上で exercise 1 は終了です。

---
[Click Here to return to the Ansible Network Automation Workshop](../README.ja.md)
