# Exercise 1.0 - Anisbleのlab環境を確認してみよう

ラボを開始する前に、ぜひSlackに参加してみましょう!  
今後のAnsibleの学習に役立つはずです。
ここでは日本のAnsibleユーザ会と２つのSlackチャンネルを紹介します。  


[日本のAnsibleコミュニティ](https://ansible-users.connpass.com)  
[日本のAnsibleコミュニティSlackへ参加する](https://join.slack.com/t/ansiblejp/shared_invite/enQtNDEyOTc3OTI3OTQxLWE1NDAzM2I5MGExYzM5OGNlN2RiMjBmYTFiYzM5NzIzYzk1ZjYyMmQ5ZTAxNjA4NmQyMTdjM2MyM2UzNjM2N2E)  
[海外のAnsibleコミュニティSlackへ参加する](https://join.slack.com/t/ansiblenetwork/shared_invite/enQtMzEyMTcxMTE5NjM3LWIyMmQ4YzNhYTA4MjA2OTRhZDQzMTZkNWZlN2E3NzhhMWQ5ZTdmNmViNjk2M2JkYzJjODhjMjVjMGUxZjc2MWE)


## Step 1

`networking-workshop` ディレクトリへ移動します。


```
[student1@ansible ~]$ cd networking-workshop/
[student1@ansible networking-workshop]$pwd
/home/student1/networking-workshop
[student1@ansible networking-workshop]$

```

## Step 2

Run the `ansible` command with the `--version` command to look at what is configured:
`ansible` コマンドを `--version` オプションをつけて実行し、現在のコンフィグについて確認してみましょう。:


```
[student1@ansible networking-workshop]$ ansible --version
ansible 2.6.2
  config file = /home/student1/.ansible.cfg
  configured module search path = [u'/home/student1/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /usr/bin/ansible
  python version = 2.7.5 (default, May  3 2017, 07:55:04) [GCC 4.8.5 20150623 (Red Hat 4.8.5-14)]
[student1@ansible networking-workshop]$


```

> Note: 表示される ansible version は上記のものと異なる可能性があります。


このコマンドは、Ansibleのバージョン、実行ファイルの場所、Pythonのバージョン、利用するモジュールを検索する場所、`ansible configuration file`の場所などが確認できます。

## Step 3

`cat` コマンドを用いて、`ansible.cfg` ファイルの中身を見てみましょう。

```
[student1@ansible networking-workshop]$ cat ~/.ansible.cfg
[defaults]
connection = smart
timeout = 60
inventory = /home/student1/networking-workshop/lab_inventory/hosts
host_key_checking = False
private_key_file = /home/student1/.ssh/aws-private.pem
[student1@ansible networking-workshop]$

```

`ansible.cfg` ファイル内の以下のパラメータに注意してください。

 - `inventory`: ansible が利用するInventoryファイルの場所を指定しています。
 - `private_key_file`: デバイスにログインするためのprivate keyの場所を指定しています。



## Step 4

`playbook`内の`play`においては、Anisbleの**inventory**ファイル内で定義されているターゲットホストのグループの制限を行うことができます。  
Ansibleは複数の[inventory](http://docs.ansible.com/ansible/latest/intro_inventory.html)のタイプをサポートしています。
インベントリは、シンプルに定義されたホストのリストを定義することもできますし、(バックエンドのCMDBなどから)動的に実行されるスクリプトによって生成されるデバイスのリストでも構いません。

このラボでは、**ini**形式で書かれたファイルベースのインベントリを使用します。   
実際に登録されているインベントリを確認するには `cat`コマンドを使います：


```

[student1@ansible ~]$ cat ~/networking-workshop/lab_inventory/hosts
[all:vars]
ansible_port=22

[routers:children]
cisco
juniper

[cisco]
rtr1 ansible_host=35.182.226.163 private_ip=172.16.173.57
rtr2 ansible_host=35.183.197.179 private_ip=172.17.88.89

[juniper]
rtr3 ansible_host=35.183.209.131 private_ip=172.16.119.246
rtr4 ansible_host=35.183.244.146 private_ip=172.17.211.127

[cisco:vars]
ansible_user=ec2-user
ansible_network_os=ios

[juniper:vars]
ansible_user=jnpr
ansible_network_os=junos

[dc1]
rtr1
rtr3

[dc2]
rtr2
rtr4

[hosts]
host1 ansible_host=35.183.19.221 ansible_user=ec2-user private_ip=172.17.179.150

[control]
ansible ansible_host=35.183.137.160 ansible_user=ec2-user private_ip=172.16.45.102
[student1@ansible ~]$

```

## Step 5

出力結果を確認していきましょう。
`[ ]` は、グループを定義しています。  
例えば、`[dc1]`は *dc1グループ* において、 `rtr1` と `rtr3` の２つのホスト(ここではルーターですが)が含まれていることを示しています。  

また、グループ定義は、_ネスト構造_ を取ることができます。  
上記の例では、グループ `[routers]` は、 `[cisco]` と `[juniper]` の２つのグループが所属する親グループとなります。

> 親グループは、 `children` ディレクティブを用いて宣言されます。ネスト構造が可能なことで、構成や変数の割り当てに柔軟性を持たせることができます。

> 注意: **all** と定義されたグループがあります。このグループはデフォルトで定義されており、インベントリー内の全てのグループと全てのホストが含まれます。

また、グループやホストに変数を割り当てることができます。  
例えば、ホスト変数はホスト自体と同じ行に宣言/定義されています。  
`rtr1` での例を見てみましょう:

```
rtr1 ansible_host=52.90.196.252 ansible_ssh_user=ec2-user private_ip=172.16.165.205 ansible_network_os=ios

```
 - `rtr1` - Ansibleが利用するホスト名です。これはDNSにも依存しますが、ローカルで定義することもできます。
 - `ansible_host` - Ansibleが使用するIPアドレスです。設定されていない場合は、DNSへ名前解決を実行します。
 - `ansible_ssh_user` - ホストへログインするために利用されるユーザです。設定されていない場合には、Playbookを実行しているユーザがデフォルトでは割当たります。
 - `private_ip` - Anisbleによって定義はされていない、デフォルトでは利用しない値です。  
 ホストに対して利用する変数[host variable](http://docs.ansible.com/ansible/latest/intro_inventory.html#host-variables)としてユーザが名称を含め、任意に定義することができます。  
定義された値はPlaybookの中で利用されるか、利用されない場合は完全に無視されます。
 
- `ansible_network_os` - この変数は、`network_cli` というコネクションタイプをPlay定義内で使用する際に必要になります。コネクションタイプについては後ほど説明があります。

# Complete

お疲れ様でした。  
lab exercise 1.0 は以上です。

---
[ここをクリックすると Ansible Linklight - Networking Workshop へ戻ります](../../README.ja.md)
