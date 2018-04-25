# 演習 1 - アドホック・コマンドの実行

最初のExcerciseは、Ansible の動きを確かめる上でいくつかの アドホック・コマンドを実行します。Ansible アドホック・コマンドはplaybookを作成せず直接タスクをリモードノードで実行する事が可能です。簡易かつクイックにいくつかのタスクを複数のリモートノードに実行したい場合にとても有効なコマンドです。

## ステップ 1.1 - インベントリの定義

インベントリを定義します。インベントリはコマンドやplaybookの実行対象となるリモートマシンを定義するものです。当Labではインストラクターよりインベントリファイルを提供しています。インベントリは、以下例のようにホスト名がリストされ、グループでソートされ、変数が追加されたini形式のファイルです。

```bash
[all:vars]
ansible_user=student1
ansible_ssh_pass=PASSWORD
ansible_port=22

[web]
node1 ansible_host=11.22.33.44 ansible_user=ec2-user
node2 ansible_host=22.33.44.55 ansible_user=ec2-user
node3 ansible_host=33.44.55.66 ansible_user=ec2-user

[control]
ansible ansible_host=44.55.66.77 ansible_ssh_user=ec2-user
```

## ステップ 1.2 - ホストへのping実行

まずはホストへのping実行から始めましょう。`ping` モジュールを利用しwebホストが応答可能であることを確認します。

```bash
ansible web -m ping
```

## ステップ 2:

Linuxコマンド形式で `command` モジュールを実行してみましょう。

```bash
ansible web -m command -a "uptime" -o
```

## ステップ 3:

webノードの定義を見てみましょう。`setup` モジュールを利用してエンドポイントの facts の内容を出力します。

```bash
ansible web -m setup
```

## ステップ 4:

`setup` モジュールを利用してApacheをインストールしてみましょう。

```bash
ansible web -m yum -a "name=httpd state=present" -b
```

## ステップ 5:

Apacheのインストールが完了したら、`service` モジュールを利用して起動してみましょう。

```bash
ansible web -m service -a "name=httpd state=started" -b
```

## ステップ 6:

最後にこれらをクリーンナップします、まずはhttpdサービスの停止を行います。

```bash
ansible web -m service -a "name=httpd state=stopped" -b
```

## ステップ 7:

次に、Apacheパッケージを削除します。

```bash
ansible web -m yum -a "name=httpd state=absent" -b
```


---
**NOTE**

多くのLinuxコマンドと同様に、Ansibleの実行コマンドも省略することが可能です。例えば、

```bash
ansible web --module-name ping
```

は、以下のように省略した形でも実行できます。

```bash
ansible web -m ping
```

当ワークショップでは以降、コマンドを省略した形で使用していきます。

---

[Click Here to return to the Ansible Linklight - Ansible Engine Workshop](../README.md)
