# Exercise 1 - アドホック・コマンドの実行

最初の演習では、Ansible の動きを確かめる上でいくつかの アドホック・コマンドを実行します。
Ansible アドホック・コマンドではplaybookの中で利用される`モジュール`を直接CLIから実行します。
モジュールは「よくあるインフラ作業」を部品化したもので、呼び出すことで様々なタスクをリモードノードで実行する事ができます。
簡易かつクイックにタスクを複数のリモートノードに実行したい場合にとても有効な利用方法です。
この後で、実際に皆様が自動化を組み立てる際には、この`モジュール`を`Playbook`に記述していくことになります。

## Step 1.1 - インベントリの定義

今回のLabでは事前にインベントリファイルが定義されているため、Step1において設定などは不要です。
ここでは、インベントリファイルが存在するということを認識してください。
インベントリとは、Anisbleが実行対象とするホスト群を定義するファイルです。
インベントリでは、以下の例のようにホスト名やIPアドレスがリストされ、グループでソートが可能であり、場合によっては変数などが追加されたini形式のファイルです。
デフォルトのインベントリファイルは Ansible の設定ファイルである `.ansible.cfg` に定義されています。この内容を確認して、インベントリーファイルの中身を確認してみましょう。

```bash
cat ~/.ansible.cfg

[defaults]
connection = smart
timeout = 60
deprecation_warnings = False
inventory = /home/studentX/lightbulb/lessons/lab_inventory/studentX-instances.txt
host_key_checking = False
private_key_file = /home/studentX/.ssh/aws-private.pem
```

`inventory=`で指定されている箇所が、デフォルトのインベントリーファイルを示しています。

```bash
cat /home/studentX/lightbulb/lessons/lab_inventory/studentX-instances.txt

[all:vars]
ansible_user=studentX
ansible_ssh_pass=ansible
ansible_port=22

[web]
node1 ansible_host=13.230.247.75
node2 ansible_host=3.112.26.239

[control]
ansible ansible_host=52.68.45.53
```

ここでは、3台のホストが定義されており、`[control]`に1台、`[web]`というグループに2台が含まれているということを覚えておいてください。


## Step 1.2 - ホストへのping実行

まずはホストへのping実行から始めましょう。
`ping` モジュールを利用しwebグループのホストがAnsibleに応答可能であることを確認します。

```bash
ansible web -m ping
```

このpingモジュールは、通常のICMPのpingではなく「Ansibleとしてのping」になります。このpingが正常終了するということは、対象のノードが「Ansibleで操作可能な状態である」ということを示します。


## Step 2:

Linuxコマンド形式で `command` モジュールを実行してみましょう。command モジュールはリモートホスト情報で任意のコマンドを実行して、その結果を回収するモジュールになります。

```bash
ansible web -m command -a "uptime" -o

ansible control -m command -a "uptime" -o

ansible all -m command -a "uptime" -o
```

`web`, `control`, `all` とすることで、実行対象がどのように変わるのかをインベントリーの定義を見ながら確認してください。

Note: `all` は特別なキーワードで、インベントリーに記載されたすべてのホストを対象します。


## Step 3:

webノードの定義を見てみましょう。
`setup` モジュールを利用してエンドポイントの facts の内容を出力します。setupモジュールは対象となるノードの設定情報やOS、ハードウェアの情報を取得するためのモジュールです。

```bash
ansible web -m setup
```

## Step 4:

`yum` モジュールを利用してApacheをインストールしてみましょう。yum モジュールは対象のパッケージを操作します。

```bash
ansible web -m yum -a "name=httpd state=present" -b
```

- `-b` はAnsibleがリモートノードで処理を行う際に、`sudo` で権限昇格をさせるためのオプションです。パッケージのインストールには root 権限が必要となります。


## Step 5:

Apacheのインストールが完了したら、`service` モジュールを利用してサービスを起動してみましょう。serviceモジュールはOSのサービスを操作するモジュールです。同等のモジュルートして`systemd`というモジュールも存在します。

```bash
ansible web -m service -a "name=httpd state=started" -b
```

このコマンドが正常終了したら、インベントリーで確認した`[web]`のサーバー2台のIPアドレスへブラウザでアクセスしてください。正常に設定が行われていれば、Apacheの初期画面が表示されます。


## Step 6:

最後に設定した情報をクリーンナップしていきます。
逆の手順でまずはhttpdサービスの停止を行います。

```bash
ansible web -m service -a "name=httpd state=stopped" -b
```

## Step 7:

次に、Apacheパッケージを削除します。

```bash
ansible web -m yum -a "name=httpd state=absent" -b
```

再び、ブラウザで2台のサーバーへアクセスするとHTTPDサービスが停止したためエラーとなるはずです。



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

[Click Here to return to the Ansible Linklight - Ansible Engine Workshop](../README.ja.md)
