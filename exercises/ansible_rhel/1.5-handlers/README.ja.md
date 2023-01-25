# ワークショップ演習 - 条件、ハンドラー、ループ

**他の言語でもお読みいただけます**:
<br>![uk](../../../images/uk.png) [English](README.md)、![japan](../../../images/japan.png)[日本語](README.ja.md)、![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md)、![france](../../../images/fr.png) [Française](README.fr.md)、![Español](../../../images/col.png) [Español](README.es.md)

## 目次

* [目的](#目的)
* [ガイド](#ガイド)
  * [ステップ 1 - 条件](#ステップ-1---条件)
  * [ステップ 2 - ハンドラー](#ステップ-2---ハンドラー)
  * [ステップ 3 - 簡単なループ](#ステップ-3---簡単なループ)
  * [ステップ 4 - ハッシュのループ](#ステップ-4---ハッシュのループ)

## 目的

3 つの基本的な Ansible 機能は次のとおりです。

* [条件](https://docs.ansible.com/ansible/latest/user_guide/playbooks_conditionals.html)
* [ハンドラー](https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html#handlers-running-operations-on-change)
* [ループ](https://docs.ansible.com/ansible/latest/user_guide/playbooks_loops.html)

## ガイド

### ステップ 1 - 条件

Ansible は条件を使用して、特定の条件が満たされたときにタスクまたは再生を実行できます。

条件を実装するには、`when` ステートメントを使用します。その後にテストする条件が続きます。条件は、たとえば比較のような利用可能なオペレーターのひとつを使って表現します。

|      |                                                                        |
| ---- | ---------------------------------------------------------------------- |
| \==  | Compares two objects for equality.                                     |
| \!=  | Compares two objects for inequality.                                   |
| \>   | true if the left hand side is greater than the right hand side.        |
| \>=  | true if the left hand side is greater or equal to the right hand side. |
| \<   | true if the left hand side is lower than the right hand side.          |
| \<= | true if the left hand side is lower or equal to the right hand side.   |

詳細は、以下のドキュメントを参照してください。<http://jinja.pocoo.org/docs/2.10/templates/>

例として、FTP サーバーをインストールしたいと思っていますが、「ftpserver」インベントリーグループにあるホストにのみにインストールしたいとします。

これを行うには、インベントリーを編集して別のグループを追加し、`node2` を配置します。追加するセクションは以下のとおりです。

``` ini
[ftpserver]
node2
```

それらの行を追加するために `~/lab_inventory/hosts` を編集します。 完了すると、以下のリストのような表示になります。



> **ヒント**
> 
> ansible_host 変数はノードに対して一度だけ指定する必要があります。
> 他のグループへノードを追加する場合、再度変数を指定する必要はありません。

**重要** 以下の例をコピー&ペーストしないでください。 ファイルを編集して、上記の行を追加するだけです。

```ini
[web]
node1 ansible_host=xx.xx.xx.xx
node2 ansible_host=xx.xx.xx.xx
node3 ansible_host=xx.xx.xx.xx

[ftpserver]
node2

[control]
ansible-1 ansible_host=xx.xx.xx.xx
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

そして、それを実行して結果を検証します。予期される結果: このタスクは、node1、node3、ansible ホスト (コントロールホスト)ではスキップされます。これは、インベントリーファイルの ftpserver グループに存在しないためです。

```bash
TASK [Install FTP server when host in ftpserver group] *******************************************
skipping: [ansible-1]
skipping: [node1]
skipping: [node3]
changed: [node2]
```

### ステップ 2 - ハンドラー

タスクがシステムに変更を加える場合は時折、その他の単一のタスクまたは複数タスクを実行しなければならない場合があります。たとえば、サービスの設定ファイルを変更すると、変更した構成の有効化にサービスを再起動しなければならないことがあります。

ここで、Ansible のハンドラーが機能します。ハンドラーは、「notify」ステートメントを使用して明示的に呼び出された場合にのみトリガーされる非アクティブなタスクと見なすことができます。詳細は、[Ansible ハンドラー](http://docs.ansible.com/ansible/latest/playbooks_intro.html#handlers-running-operations-on-change) のドキュメントをご覧ください。

例として、次のような playbook を作成しましょう。

* `web` グループのすべてのホスト上で Apache の設定ファイル `/etc/httpd/conf/httpd.conf` を管理
* ファイルが変更されたときに Apache を再起動

まず、Ansible がデプロイするファイルが必要です。node1 からファイルを取得しましょう。以下のリストに示されている IP アドレスは、個人の `node1` の IP アドレスに置き換えることを忘れないでください。

```bash
[student@ansible-1 ansible-files]$ scp node1:/etc/httpd/conf/httpd.conf ~/ansible-files/files/.
httpd.conf
```

次に、Playbook `httpd_conf.yml` を作成します。ディレクトリー `~/ansible-files` にいることを確認してください。

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

playbook を実行します。このファイルではまだ何も変更していないので `changed` の行は出力に表示されません。もちろん、ハンドラーは起動していません。

* 今すぐ、`~/ansible-files/files/httpd.conf` の `Listen 80` を以下に変更します。

```ini
Listen 8080
```

* playbook を再び実行します。これで、Ansible の出力はもっと興味深いものになるはずです。

  * httpd.conf がコピーされているはずです
  * ハンドラーは Apache を再起動しているはずです

Apache はポート 8080 でリッスンするはずです。確認は簡単です。

```bash
[student@ansible-1 ansible-files]$ curl http://node1
curl: (7) Failed to connect to node1 port 80: Connection refused
[student@ansible-1 ansible-files]$ curl http://node1:8080
<body>
<h1>Apache is running fine</h1>
</body>
```

8080 番ポートでリッスンする設定のままにします。後でこれを使用します。

### ステップ 3 - 簡単なループ

ループを使用すると、同じタスクを何度も繰り返すことができます。たとえば、複数のユーザーを作成するとします。Ansibleループを使用することで、1 つのタスクでそれを行うことができます。ループは、基本的なリスト以上のものを繰り返すこともできます。たとえば、対応するグループを持つユーザーのリストがある場合、ループはそれらを反復処理することもできます。ループの詳細については、[Ansible Loops](https://docs.ansible.com/ansible/latest/user_guide/playbooks_loops.html) のドキュメントをご覧ください。

ループ機能のデモとして、`node1` で 3 つの新しいユーザーをつくります。この作業用に、お使いの学習者ユーザーとしてコントロールノードの `~/ansible-files` に `loop_users.yml` ファイルを作成します。`user` モジュールを使用して、ユーザーアカウントを生成します。

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
* `loop` キーワードは実際のユーザー名をリストします。これらは、Playbook を実際に実行しているときに `{{ item }}` を置き換えます。
* 実行中、タスクは1回だけリストされますが、その下に 3 つの変更がリストされます。

<!-- {% endraw %} -->

### ステップ 4 - ハッシュのループ

前述のように、ループはハッシュのリストでも実行できます。ユーザーを別の追加グループに割り当てる必要があると想像してください。

```yaml
- username: dev_user
  groups: ftp
- username: qa_user
  groups: ftp
- username: prod_user
  groups: apache
```

`user` モジュールには、その他のユーザーを一覧表示するためのオプションのパラメーター `groups` があります。ハッシュでアイテムを参照するには、`{{ item }}` キーワードが、サブキーを参照する必要があります (例: `{{item.groups }}`)。

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

以下の Playbook を使用して、`dev_user` が `node1` で作成されたことを確認します。

{% raw %}
```yaml
---
- name: Get user ID
  hosts: node1
  vars:
    myuser: "dev_user"
  tasks:
    - name: Get {{ myuser }} info
      getent:
        database: passwd
        key: "{{ myuser }}"
    - debug:
        msg:
          - "{{ myuser }} uid: {{ getent_passwd[myuser].1 }}"
```
{% endraw %}

```bash
$ ansible-navigator run user_id.yml -m stdout

PLAY [Get user ID] *************************************************************

TASK [Gathering Facts] *********************************************************
ok: [node1]

TASK [Get dev_user info] *******************************************************
ok: [node1]

TASK [debug] *******************************************************************
ok: [node1] => {
    "msg": [
        "dev_user uid: 1002"
    ]
}

PLAY RECAP *********************************************************************
node1                      : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```
---
**ナビゲーション**
<br>
[前の演習](../1.4-variables) - [次の演習](../1.6-templates)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-1---ansible-engine-exercises)
