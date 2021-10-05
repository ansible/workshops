# ワークショップ演習 - 条件、ハンドラー、ループ

**その他の言語はこちらをお読みください。**
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## 目次

* [目的](#objective)
* [ガイド](#guide)
  * [Step 1 - 条件](#step-1---conditionals)
  * [Step 2 - ハンドラー](#step-2---handlers)
  * [Step 3 - シンプルループ](#step-3---simple-loops)
  * [Step 4 - ハッシュのループ](#step-4---loops-over-hashes)

## 目的

3 つの基本的な Ansible 機能は次のとおりです。

* [Conditionals](https://docs.ansible.com/ansible/latest/user_guide/playbooks_conditionals.html)
* [Handlers](https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html#handlers-running-operations-on-change)
* [Loops](https://docs.ansible.com/ansible/latest/user_guide/playbooks_loops.html)

## ガイド

### Step 1 - 条件

Ansible は条件を使用して、特定の条件が満たされたときにタスクまたは再生を実行できます。

条件を実装するには、`when`
ステートメントを使用します。その後にテストする条件が続きます。条件は、たとえば比較のような利用可能なオペレーターのひとつを使って表現します。

|      |                                                                        |
| ---- | ---------------------------------------------------------------------- |
| \==  | 2 つのオブジェクトが等しいかを比較します。                                     |
| \!=  | 2 つのオブジェクトが等しくないかどうかを比較します。                                   |
| \>   | 左側が右側よりも大きい場合に真になります。        |
| \>=  | 左側が右側よりも小さい場合に真になります。       |
| \<   | 左側が右側よりも小さい場合に真になります。          |
| \<= | 左側が右側と等しいか、右側よりも小さい場合に真になります。   |

詳細は、以下のドキュメントを参照してください。<http://jinja.pocoo.org/docs/2.10/templates/> 

例として、FTP
サーバーをインストールしたいと思っていますが、「ftpserver」インベントリーグループにあるホストにのみにインストールしたいとします。

これを行うには、インベントリーを編集して別のグループを追加し、`node2` を配置します。`node2` の IP アドレスは、`node2`
がリストされたときと常に同じになるようにしてください。以下のリストのようにインベントリー `~/lab_inventory/hosts` を編集します。

```ini
[all:vars]
ansible_user=student1
ansible_ssh_pass=ansible
ansible_port=22

[web]
node1 ansible_host=11.22.33.44
node2 ansible_host=22.33.44.55
node3 ansible_host=33.44.55.66

[ftpserver]
node2 ansible_host=22.33.44.55

[control]
ansible-1 ansible_host=44.55.66.77
```

次に、`~/ansible-files/` ディレクトリーのコントロールホストで `ftpserver.yml` ファイルを作成します。

```yaml
---
- name: Install vsftpd on ftpservers
  hosts: all
  become: true
  tasks:
    - name: Install FTP server when host in ftpserver group
      yum:
        name: vsftpd
        state: latest
      when: inventory_hostname in groups["ftpserver"]
```

> **ヒント**
>
> これで、Ansible Playbook の実行方法をご理解いただけたと思いますので、これからは説明を少し簡潔にしていき、作成して実行するというスタイルにします。

そして、それを実行して結果を検証します。予期される結果: このタスクは、node1、node3、ansible ホスト (コントロールホスト)
ではスキップされます。これは、インベントリーファイルの ftpserver グループに存在しないためです。

```bash
TASK [Install FTP server when host in ftpserver group] *******************************************
skipping: [ansible-1]
skipping: [node1]
skipping: [node3]
changed: [node2]
```

### Step 2 - ハンドラー

タスクがシステムに変更を加える場合は時折、その他の単一のタスクまたは複数タスクを実行しなければならない場合があります。たとえば、サービスの設定ファイルを変更すると、変更した構成の有効化にサービスを再起動しなければならないことがあります。

ここで、Ansible
のハンドラーが機能します。ハンドラーは、「notify」ステートメントを使用して明示的に呼び出された場合にのみトリガーされる非アクティブなタスクと見なすことができます。詳細は、[Ansible
ハンドラー](http://docs.ansible.com/ansible/latest/playbooks_intro.html#handlers-running-operations-on-change)
のドキュメントをご覧ください。

例として、次のような playbook を作成しましょう。

* `web` グループのすべてのホスト上で Apache の設定ファイル `/etc/httpd/conf/httpd.conf` を管理
* ファイルが変更されたときに Apache を再起動

まず、Ansible がデプロイするファイルが必要です。node1 からファイルを取得しましょう。以下のリストに示されている IP アドレスは、個人の
`node1` の IP アドレスに置き換えることを忘れないでください。

```bash
[student<X>@ansible-1 ansible-files]$ scp node1:/etc/httpd/conf/httpd.conf ~/ansible-files/files/.
student<X>@11.22.33.44's password:
httpd.conf
```

次に、Playbook `httpd_conf.yml` を作成します。ディレクトリー `~/ansible-files`
にいることを確認してください。

```yaml
---
- name: manage httpd.conf
  hosts: web
  become: true
  tasks:
  - name: Copy Apache configuration file
    copy:
      src: httpd.conf
      dest: /etc/httpd/conf/
    notify:
        - restart_apache
  handlers:
    - name: restart_apache
      service:
        name: httpd
        state: restarted
```

さて、なにがこれまでと違うのでしょうか。

* 「notify」セクションは、コピータスクが実際にファイルを変更したときにのみハンドラーを呼び出します。そうすれば、そのサービスは必要なときだけ再起動され、プレイブックが実行されるたびに再起動されなくなります。
* 「handlers」セクションは、通知時にのみ実行されるタスクを定義します。

<hr>

playbook を実行します。このファイルではまだ何も変更していないので `changed`
の行は出力に表示されません。もちろん、ハンドラーは起動していません。

* 今すぐ、`~/ansible-files/files/httpd.conf` の `Listen 80` を以下に変更します。

```ini
Listen 8080
```

* playbook を再び実行します。これで、Ansible の出力はもっと興味深いものになるはずです。

  * httpd.conf がコピーされているはずです
  * ハンドラーは Apache を再起動しているはずです

Apache はポート 8080 でリッスンするはずです。確認は簡単です。

```bash
[student<X>@ansible-1 ansible-files]$ curl http://node1
curl: (7) Failed to connect to node1 port 80: Connection refused
[student<X>@ansible-1 ansible-files]$ curl http://node1:8080
<body>
<h1>This is a production webserver, take care!</h1>
</body>
```

httpd.conf ファイルを自由に再度変更して、playbook を実行してください。

### Step 3 - 簡単なループ

ループを使用すると、同じタスクを何度も繰り返すことができます。たとえば、複数のユーザーを作成するとします。Ansibleループを使用することで、1
つのタスクでそれを行うことができます。ループは、基本的なリスト以上のものを繰り返すこともできます。たとえば、対応するグループを持つユーザーのリストがある場合、ループはそれらを反復処理することもできます。ループの詳細については、[Ansible
Loops](https://docs.ansible.com/ansible/latest/user_guide/playbooks_loops.html)
のドキュメントをご覧ください。

ループ機能のデモとして、`node1` で 3 つの新しいユーザーをつくります。この作業用に、お使いの学習者ユーザーとしてコントロールノードの
`~/ansible-files` に `loop_users.yml` ファイルを作成します。`user`
モジュールを使用して、ユーザーアカウントを生成します。

<!-- {% raw %} -->

```yaml
---
- name: Ensure users
  hosts: node1
  become: true

  tasks:
    - name: Ensure three users are present
      user:
        name: "{{ item }}"
        state: present
      loop:
         - dev_user
         - qa_user
         - prod_user
```

<!-- {% endraw %} -->

Playbook と出力の概要:

<!-- {% raw %} -->

* この名前はユーザーモジュールに直接指定されません。代わりに、パラメーター `name` 用の `{{ item }}` と呼ばれる変数のみがあります
* `loop` キーワードは実際のユーザー名をリストします。これらは、Playbook を実際に実行しているときに `{{ item }}`
  を置き換えます。
* 実行中、タスクは1回だけリストされますが、その下に 3 つの変更がリストされます。

<!-- {% endraw %} -->

### Step 4 - ハッシュのループ

前述のように、ループはハッシュのリストでも実行できます。ユーザーを別の追加グループに割り当てる必要があると想像してください。

```yaml
- username: dev_user
  groups: ftp
- username: qa_user
  groups: ftp
- username: prod_user
  groups: apache
```

`user` モジュールには、その他のユーザーを一覧表示するためのオプションのパラメーター `groups`
があります。ハッシュでアイテムを参照するには、`{{ item }}` キーワードが、サブキーを参照する必要があります (例: `{{
item.groups }}`)。

Playbook を書き直して、追加のユーザー権限を持つユーザーを作成しましょう。

<!-- {% raw %} -->

```yaml
---
- name: Ensure users
  hosts: node1
  become: true

  tasks:
    - name: Ensure three users are present
      user:
        name: "{{ item.username }}"
        state: present
        groups: "{{ item.groups }}"
      loop:
        - { username: 'dev_user', groups: 'ftp' }
        - { username: 'qa_user', groups: 'ftp' }
        - { username: 'prod_user', groups: 'apache' }

```

<!-- {% endraw %} -->

出力を確認します。

* ここでも、タスクは 1 回リストされていますが、3 つの変更がリストされています。各ループとその内容が表示されます。

ユーザー `dev_user` が `node1` で確実に作成されたことを確認します。

```bash
[student<X>@ansible-1 ansible-files]$ ansible node1 -m command -a "id dev_user"
node1 | CHANGED | rc=0 >>
uid=1002(dev_user) gid=1002(dev_user) Gruppen=1002(dev_user),50(ftp)
```

---
**ナビゲーション**
<br>
[前の演習](../1.4-variables) - [次の演習](../1.6-templates)

[こちらをクリックして Ansible for Red Hat Enterprise Linux Workshop
に戻ります](../README.md#section-1---ansible-engine-exercises)
