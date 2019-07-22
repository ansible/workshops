# 演習1.4 - 変数を使ってみる

前回までは Ansible Core の基礎部分を学習してきました。次の学習は playbook をより柔軟かつパワフルに使用できるより高度なスキルを学びたいと思います。

Ansible では task をよりシンプル、かつ再利用可能にできます。システムの設定にはユニークな設定が含まれる場合があり、
playbookを実行する際、そのユニークな設定を含んだ実行が必要な場合があります。このような場合には変数を使います。

Ansible は、playbook で使用可能な値を格納するための変数をサポートしています。変数はさまざまな場所で定義でき、明確な優先順位があります。Ansibleは、タスクが実行される際、変数をその値に置き換えます。

playbook では、変数名を二重中括弧で囲むことで変数を表現します。

<!-- {% raw %} -->
```yaml
変数は右の様に表現します　 {{ variable1 }}
```
<!-- {% endraw %} -->

変数とその値は、インベントリ、追加ファイル、コマンドラインなどのさまざまな場所で定義できます。

インベントリで変数を提供するための推奨される方法は、host_vars と group_vars という2つのディレクトリにあるファイルにそれらを定義することです。

たとえば、グループ "servers" の変数を定義するために、変数名が付けられたYAMLファイル group_vars/servers を作成します。

また、特定ホスト node1 専用の変数を定義するために、変数定義を含む node1 ファイル host_vars/node1 を作成します。


> **ヒント**
> 
> ホスト変数には優先順位があります。上記 Host 変数は、 Group 変数より優先されます。詳しくは製品マニュアルをご確認ください。

## ステップ 1.4.1 - 変数ファイルの作成

早速演習で変数の動きを確かめてみましょう。3台の Web Server を構築してみます。どのホストに接続されているかを示すため、 `index.html` を変更します。

まずは、Ansible Control Host で、変数ファイルの置き場所となるディレクトリを `~/ansible-files/`　に作成します。

```bash
[student<X>@ansible ansible-files]$ cd ~/ansible-files/
[student<X>@ansible ansible-files]$ mkdir host_vars group_vars
```

変数の定義を含むファイルを２つ作成しましょう。 `stage` という名前の変数に、`dev` or `prod`という異なる二つの値を定義します。

  - 以下の内容を含むファイルを `~/ansible-files/group_vars/web` として作成します。

```yaml
---
stage: dev
```

  - 同様に、以下の内容を含むファイルを `~/ansible-files/host_vars/node2` として作成します。

```yaml
---
stage: prod
```

これはどういう意味でしょう？

  -  `web` group のすべてのサーバーに対して、変数 `stage` に値 `dev` が定義されます。そして dev （開発）をデフォルト値として定義します。

  -  `node2` に関しては、上記で定義された変数 stage = dev が、prod で上書きされます。本番環境として定義されます。 

## Step 1.4.2 - index.html ファイルの作成

`~/ansible-files/` 内に、以下の2つのファイルを作成します:

まずは本番環境用の `prod_index.html` に以下の内容を記述し、保存します。

```html
<body>
<h1>This is a production webserver, take care!</h1>
</body>
```

同様に、開発環境用の `dev_index.html` に以下の内容を記述し、保存します。

```html
<body>
<h1>This is a development webserver, have fun!</h1>
</body>
```

## Step 1.4.3 - Playbook の作成

次に、上記手順で作成した本番用、開発用の `index.html` の内いずれかのファイルを "stage" 変数の値に従って Web Server にコピーするための playbook を作成します。

 `deploy_index_html.yml` という名前の playbook を `~/ansible-files/` ディレクトリ内に作成します。

> **Tip**
> 
> Note how the variable "stage" is used in the name of the file to copy.

<!-- {% raw %} -->
```yaml
---
- name: Copy index.html
  hosts: web
  become: yes
  tasks:
  - name: copy index.html
    copy:
      src: ~/ansible-files/{{ stage }}_index.html
      dest: /var/www/html/index.html
```
<!-- {% endraw %} -->

  - Run the Playbook:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook deploy_index_html.yml
```

## Step 4.4 - Test the Result

The Playbook should copy different files as index.html to the hosts, use `curl` to test it. Check the inventory again if you forgot the IP addresses of your nodes.

```bash
[student<X>@ansible ansible-files]$ grep node ~/lab_inventory/hosts
node1 ansible_host=11.22.33.44
node2 ansible_host=22.33.44.55
node3 ansible_host=33.44.55.66
[student<X>@ansible ansible-files]$ curl http://11.22.33.44
<body>
<h1>This is a development webserver, have fun!</h1>
</body>
[student1@ansible ansible-files]$ curl http://22.33.44.55
<body>
<h1>This is a production webserver, take care!</h1>
</body>
[student1@ansible ansible-files]$ curl http://33.44.55.66
<body>
<h1>This is a development webserver, have fun!</h1>
</body>
```

> **Tip**
> 
> If by now you think: There has to be a smarter way to change content in files…​ you are absolutely right. This lab was done to introduce variables, you are about to learn about templates in one of the next chapters.

## Step 4.5 - Ansible Facts

Ansible facts are variables that are automatically discovered by Ansible from a managed host. Remeber the "Gathering Facts" task listed in the output of each `ansible-playbook` execution? At that moment the facts are gathered for each managed nodes. Facts can also be pulled by the `setup` module. They contain useful information stored into variables that administrators can reuse.

To get an idea what facts Ansible collects by default, on your control node as your student user run:

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup
```

This might be a bit too much, you can use filters to limit the output to certain facts, the expression is shell-style wildcard:

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup -a 'filter=ansible_eth0'
```
Or what about only looking for memory related facts:

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup -a 'filter=ansible_*_mb'
```

## Step 4.6 - Challenge Lab: Facts

  - Try to find and print the distribution (Red Hat) of your managed hosts. On one line, please.

> **Tip**
> 
> Use grep to find the fact, then apply a filter to only print this fact.

> **Warning**
> 
> **Solution below\!**

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup|grep distribution
[student<X>@ansible ansible-files]$ ansible node1 -m setup -a 'filter=ansible_distribution' -o
```

## Step 4.7 - Using Facts in Playbooks

Facts can be used in a Playbook like variables, using the proper naming, of course. Create this Playbook as `facts.yml` in the `~/ansible-files/` directory:

<!-- {% raw %} -->
```yaml    
---
- name: Output facts within a playbook
  hosts: all
  tasks:
  - name: Prints Ansible facts
    debug:
      msg: The default IPv4 address of {{ ansible_fqdn }} is {{ ansible_default_ipv4.address }}
```
<!-- {% endraw %} -->

> **Tip**
> 
> The "debug" module is handy for e.g. debugging variables or expressions.

Execute it to see how the facts are printed:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook facts.yml 

PLAY [Output facts within a playbook] ******************************************

TASK [Gathering Facts] *********************************************************
ok: [node3]
ok: [node2]
ok: [node1]
ok: [ansible]

TASK [Prints Ansible facts] ****************************************************
ok: [node1] => 
  msg: The default IPv4 address of node1 is 172.16.190.143
ok: [node2] => 
  msg: The default IPv4 address of node2 is 172.16.30.170
ok: [node3] => 
  msg: The default IPv4 address of node3 is 172.16.140.196
ok: [ansible] => 
  msg: The default IPv4 address of ansible is 172.16.2.10

PLAY RECAP *********************************************************************
ansible                    : ok=2    changed=0    unreachable=0    failed=0   
node1                      : ok=2    changed=0    unreachable=0    failed=0   
node2                      : ok=2    changed=0    unreachable=0    failed=0   
node3                      : ok=2    changed=0    unreachable=0    failed=0   
```

----

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-1---ansible-engine-exercises)
