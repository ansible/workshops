# Exercise 1 - アドホック・コマンドの実行

最初のExcerciseは、Ansible の動きを確かめる上でいくつかの アドホック・コマンドを実行します。  
Ansible アドホック・コマンドはplaybookを作成せずに、CLIから様々なタスクをリモードノードで実行する事ができます。  
簡易かつクイックにタスクを複数のリモートノードに実行したい場合にとても有効な利用方法です。

## Step 1.1 - インベントリの定義

今回のLabでは事前にインベントリファイルが定義されているため、Step1において、設定などは不要です。  
ここでは、インベントリファイルが存在するということを認識してください。  
インベントリとは、Anisbleが実行対象とするホスト群を定義するファイルです。  
インベントリでは、以下の例のようにホスト名やIPアドレスがリストされ、グループでソートが可能であり、場合によっては変数などが追加されたini形式のファイルです。

```bash
[all:vars]
ansible_user=studentX
ansible_ssh_pass=PASSWORD
ansible_port=22

[web]
node1 ansible_host=11.22.33.44
node2 ansible_host=22.33.44.55
node3 ansible_host=33.44.55.66

[control]
ansible ansible_host=44.55.66.77
```

## Step 1.2 - ホストへのping実行

まずはホストへのping実行から始めましょう。  
`ping` モジュールを利用しwebグループのホストがAnsibleに応答可能であることを確認します。

```bash
ansible web -m ping
```

## Step 2:

Linuxコマンド形式で `command` モジュールを実行してみましょう。

```bash
ansible web -m command -a "uptime" -o
```

## Step 3:

webノードの定義を見てみましょう。  
`setup` モジュールを利用してエンドポイントの facts の内容を出力します。

```bash
ansible web -m setup
```

## Step 4:

`yum` モジュールを利用してApacheをインストールしてみましょう。

```bash
ansible web -m yum -a "name=httpd state=present" -b
```

## Step 5:

Apacheのインストールが完了したら、`service` モジュールを利用してサービスを起動してみましょう。

```bash
ansible web -m service -a "name=httpd state=started" -b
```

## Step 6:

最後に設定した情報をクリーンナップしていきます。  
まずはhttpdサービスの停止を行います。

```bash
ansible web -m service -a "name=httpd state=stopped" -b
```

## Step 7:

次に、Apacheパッケージを削除します。

```bash
ansible web -m yum -a "name=httpd state=absent" -b
```


---
**NOTE**

多くのLinuxコマンドと同様に、Ansibleの実行コマンドも省略することが可能です。  
例えば、

```bash
ansible web --module-name ping
```

は、以下のように省略した形でも実行できます。

```bash
ansible web -m ping
```

当ワークショップでは以降、コマンドを省略した形で使用していきます。

この章で利用したモジュールについては、以下で利用方法などが確認できます。
https://docs.ansible.com/ansible/latest/modules/list_of_all_modules.html

コマンドラインで利用されているオプションを調べる際には、以下のコマンドを実行してください。
```bash
ansible --help
```
以下のリンクを参照すると、この後の章で出てくるコマンドとそのオプションを調べることができます。
https://docs.ansible.com/ansible/latest/user_guide/command_line_tools.html

---

[Click Here to return to the Ansible Linklight - Ansible Engine Workshop](../README.md)
