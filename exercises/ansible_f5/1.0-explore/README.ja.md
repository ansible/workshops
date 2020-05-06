# 演習 1.0 - 演習環境の確認

**Read this in other languages**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

演習を開始する前にぜひ Ansible Slack へ参加してください！(任意)

- [クリックして ansiblejp slack (日本語) へ参加](https://bit.ly/slack-ansiblejp)
- [クリックして ansiblenetwork slack (英語) へ参加](https://join.slack.com/t/ansiblenetwork/shared_invite/enQtMzEyMTcxMTE5NjM3LWIyMmQ4YzNhYTA4MjA2OTRhZDQzMTZkNWZlN2E3NzhhMWQ5ZTdmNmViNjk2M2JkYzJjODhjMjVjMGUxZjc2MWE)

ここでは他のネットワークエンジニアと自動化をテーマに交流することができます。

#### Step 1

`f5-workshop` ディレクトリへ移動してください。

```
[student1@ansible ~]$ cd f5-workshop/
[student1@ansible f5-workshop]$
```

#### Step 2

設定を確認するために `ansible` コマンドに `--version` オプションをつけて実行します:

```
[student1@ansible f5-workshop]$ ansible --version
ansible 2.6.2
  config file = /home/student1/.ansible.cfg
  configured module search path = [u'/home/student1/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /usr/bin/ansible
  python version = 2.7.5 (default, May  3 2017, 07:55:04) [GCC 4.8.5 20150623 (Red Hat 4.8.5-14)]
```

> Note: 実際の演習環境ではバージョンが異なる場合があります


このコマンドは Ansible のバージョン、実行ファイルの場所、Python のバージョン、モジュールの検索パスおよび `ansible 設定ファイル` の場所を表示します。

#### Step 3

`cat` コマンドを使って `ansible.cfg` ファイルの中身を確認します。


```
[student1@ansible f5-workshop]$ cat ~/.ansible.cfg
[defaults]
connection = smart
timeout = 60
inventory = /home/student1/lab_inventory/hosts
host_key_checking = False
private_key_file = /home/student1/.ssh/aws-private.pem
[student1@ansible f5-workshop]$

```

Note: `ansible.cfg` には以下のパラメーターが含まれています:

 - `inventory`: 利用される Ansible インベントリーの場所を示します。
 - `private_key_file`: デバイスのログインに使用される秘密鍵の場所を示します。

#### Step 4

`playbook` 内の `play` のスコープは Ansible  **inventory** 内で宣言されたホストグループに制限されます。Ansible は複数の [inventory](http://docs.ansible.com/ansible/latest/intro_inventory.html) タイプをサポートします。インベントリは、その中に定義されたホストの集合を含む単純なフラットファイルである場合もあれば、Playbook を実行するデバイスのリストを生成する動的スクリプト（バックエンドのCMDBへ問い合わせる）場合もあります。

この演習では **ini** 形式で書かれたファイルを使います. `cat` コマンドでインベントリーの中身を確認します:

`[student1@ansible f5-workshop]$ cat ~/lab_inventory/hosts`

以下が student2 の出力例です:
```
[all:vars]
ansible_user=student2
ansible_ssh_pass=ansible
ansible_port=22

[lb]
f5 ansible_host=34.199.128.69 ansible_user=admin private_ip=172.16.26.136 ansible_ssh_pass=ansible

[control]
ansible ansible_host=107.23.192.217 ansible_user=ec2-user private_ip=172.16.207.49

[web]
node1 ansible_host=107.22.141.4 ansible_user=ec2-user private_ip=172.16.170.190
node2 ansible_host=54.146.162.192 ansible_user=ec2-user private_ip=172.16.160.13
```

#### Step 5

上の出力では `[ ]` でグループを定義しています。例えば `[web]` は `node1` と `node2` を含んむグループです。

> Note: **all** というグループは常に存在し、インベントリー内で定義された全てのホストとグループを含みます。


グループとホストに変数を関連付けることができます。ホスト変数はホストの定義と同じ行に宣言/定義します。ホスト `f5` の例を見てみます:

```
f5 ansible_host=34.199.128.69 ansible_user=admin private_ip=172.16.26.136 ansible_ssh_pass=ansible
```

 - `f5` - Ansible が使う名前。DNS参照できる形式でも良いですが、そうでなくても問題はありません。
 - `ansible_host` - Ansible が使うIPアドレスです。指定されなかった場合にはDNSが利用されます。
 - `ansible_user` - Ansible が接続に使うユーザー名です。指定されなかったときは、デフォルトで Playbook を実行したユーザーの名前が使われます。
 - `private_ip` - この変数は Ansible で予約されたものではなく [ホスト変数](http://docs.ansible.com/ansible/latest/intro_inventory.html#host-variables) として定義されています。この変数は Playbook の中で使うこともできますし、完全に無視しても問題はありません。
- `ansible_ssh_pass` - Ansible がホストにログインするためのパスワードです。指定されなかった場合、デフォルトでは Playbook を実行したユーザーの SSH 鍵を使ってホストへアクセスします。

> 実際にはパスワードを平文で保存しておく必要はありません。Red Hat Ansible Tower では認証情報の管理を GUI から簡単に行うことが可能です。もしくは [ansible-vault](https://docs.ansible.com/ansible/latest/network/getting_started/first_inventory.html#protecting-sensitive-variables-with-ansible-vault) を使うこともできます。

ホームディレクトリへ戻ります。

```
[student1@ansible f5-workshop]$ cd ~
```

本演習は以上となります。  [Click here to return to the lab guide](../README.ja.md)
