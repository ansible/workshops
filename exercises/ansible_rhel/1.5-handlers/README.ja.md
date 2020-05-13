# 演習 - 条件分岐、ハンドラー、ループを使う

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

* [ステップ 1 - 条件分岐](#ステップ-1---条件分岐)
* [ステップ 2 - ハンドラー](#ステップ-2---ハンドラー)
* [ステップ 3 - 単純な繰り返し（ループ実行）](#ステップ-3---単純な繰り返しループ実行)
* [ステップ 4 - ハッシュをループする](#ステップ-4---ハッシュをループする)


## ステップ 1 - 条件分岐

Ansible は特定の条件が満たされたときにタスクを実行したり再生したりすることができます。

特定の条件を指定するには、 `when` ステートメントを利用し、続いて具体的な条件を記述します。 条件は、比較などに使用可能な演算子の1つを使用します。



|      |                                                                        |
| ---- | ---------------------------------------------------------------------- |
| \==  | Compares two objects for equality.                                     |
| \!=  | Compares two objects for inequality.                                   |
| \>   | true if the left hand side is greater than the right hand side.        |
| \>=  | true if the left hand side is greater or equal to the right hand side. |
| \<   | true if the left hand side is lower than the right hand side.          |
| \< = | true if the left hand side is lower or equal to the right hand side.   |

詳しくは、次のドキュメントを参照してください。  
<https://docs.ansible.com/ansible/latest/user_guide/playbooks_conditionals.html#the-when-statement>

例として、 "ftpserver"インベントリグループにあるホストにのみ、FTPサーバーをインストールすることを考えてみます。

では早速やってみましょう。まず、デフォルトで指定されたインベントリファイルを編集し、`ftpserver` グループに `node2` を入れます。
デフォルトのインベントリファイルは、  
`~/lab_inventory/hosts` でしたね。♪

編集後は以下の様になります。node2 のIPアドレスはご自身のものを入力してください！

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
ansible ansible_host=44.55.66.77
```

次に、`~/ansible-files/` ディレクトリ内に `ftpserver.yml` という名前の Playbook を作成します。ファイルの中身は以下の通りです。

```yaml
---
- name: Install vsftpd on ftpservers
  hosts: all
  become: yes
  tasks:
    - name: Install FTP server when host in ftpserver group
      yum:
        name: vsftpd
        state: latest
      when: inventory_hostname in groups["ftpserver"]
```

> **ヒント**
>
> 作成完了したら playbook を実行してみてください。やり方は・・・、もう分かってますね (^^♪

実行した結果を確認してみてください。 `ftpserver` グループに記載された node2 以外のホストはタスクがスキップされ、node2 のみタスクの実行が行われていることが確認できます。  

```bash
TASK [Install FTP server when host in ftpserver group] *******************************************
skipping: [ansible]
skipping: [node1]
skipping: [node3]
changed: [node2]
```

## ステップ 2 - ハンドラー

プレイブックを書いていると、特定のタスクが実行された時のみ、さらに追加のタスクを実行したい場合があります。たとえば、サービスの更新や設定ファイルを変更した場合に、変更した設定が有効になるようにサービスの再起動が必要となるケースです。  

このような場合にハンドラーを利用します。ハンドラーは、"notify" ステートメントで定義されたタスクが実行された場合にのみ実行される非アクティブタスクです。詳しくは[Ansible Handlers](http://docs.ansible.com/ansible/latest/playbooks_intro.html#handlers-running-operations-on-change)のマニュアルをご確認ください。

早速演習で試してみましょう。以下のような Playbook を作ります。  

  - 全 `web` グループのホストに対して、 Apache の構成ファイル `httpd.conf` をコピーする  

  - ファイルが変更された時のみ Apache のサービスをリスタートする  

まずはコピー元として利用する httpd.conf を node1 から取得します。  

> **ヒント**
>
>このファイルは既に node1 node2 node3 に配置されています。  


```bash
[student<X>@ansible ansible-files]$ scp <node1>:/etc/httpd/conf/httpd.conf ~/ansible-files/.
student<X>@<node1>'s password:
httpd.conf             
```

次に、 `~/ansible-files` ディレクトリに、Playbook `httpd_conf.yml` を作成します。 playbook には以下を記述します。  

```yaml
---
- name: manage httpd.conf
  hosts: web
  become: yes
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

playbook は以下の様になっています。

  - "notify" セクションは、コピータスクがファイルを変更したときだけハンドラーを呼び出します。つまり、サービス再起動は必要な場合にのみ（この例の場合はファイルの更新が行われた場合のみ）行われます。  

  - "ハンドラー" セクションは、notify から呼び出された時に実際に実行されるタスクを定義します。  

まずこのまま playbook を実行してみてください。まだ httpd.conf に何も変更を加えていないので、changed は "0" で、ハンドラーも動作していないことが分かると思います。  

  - httpd.conf の中の、 `Listen 80` の行を以下の通り変更します。  


```ini
Listen 8080
```

  - Playbookをもう一度実行してください。興味深い結果が得られます。  

      - httpd.conf が上書きコピーされた  

      - ハンドラーが呼び出され、 Apache サービスをリスタートした  

Apacheはポート8080でリッスンしているはずです。試してみてください。  

```bash
[student1@ansible ansible-files]$ curl http://<node1>
curl: (7) Failed connect to <node1>:80; Connection refused
[student1@ansible ansible-files]$ curl http://22.33.44.55:8080
<body>
<h1>This is a production webserver, take care!</h1>
</body>
```
httpd.conf ファイルを再度 "80" に変更し、どうなるか試してみてください。

> **注意**
>
> 演習1.7で、ポート8080を使います。この時点で 80ポートをリッスンするよう設定を戻しておいてください。


> **ヒント**
>
> よく聞かれる質問として、notify セクションが実行されたらすぐにハンドラーが呼び出されるのか？ということがありますが、これは違います。今回の場合、notify 直下にハンドラーが定義されているのですぐの実行となりますが、notiry とハンドラーが離れていた場合は、あくまで上から順に実行され、ハンドラーの順番になったところで実行されます。 notify でハンドラー実行のフラグを立てておく感じです。  

## ステップ 3 - 単純な繰り返し（ループ実行）

ループを使用すると、同じタスクを繰り返し実行することができます。たとえば、複数のユーザーを作成したいとしましょう。Ansible ループを使用すると、単一のタスクでそれを実行できます。ループは、単なるリスト以外にも反復することができます。たとえば、対応するグループを持つユーザーのリストがある場合、ループはそれらに対しても反復することができます。 詳しくは[Ansible Loops](https://docs.ansible.com/ansible/latest/user_guide/playbooks_loops.html)のマニュアルをご確認ください。

ループの機能を確認してみましょう。 node1 に3人の新しいユーザーを作成します。 `~/ansible-files` ディレクトリの中に、 `loop_users.yml` という名前の playbook を作成します。使用するのは `user` モジュールで、playbook の中身は以下の通りです。  

<!-- {% raw %} -->
```yaml
---
- name: Ensure users
  hosts: node1
  become: yes

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

作成出来たら実行してみてください。playbook は以下の内容になっています。  

  - 作成するユーザー名は直接 user モジュールには与えられません。代わりに `{{ item }}` パラメータで呼び出される変数が定義されています

  - `loop` 内のキーワードには、実際に作成するユーザー名が3名分列挙されています。この値が、`{{ item }}` 内に順に入力され、 playbook が実行されます。    

  - 実行中、タスクは一度だけ表示されますが、その下に loop された3つの変更点が表示されます。  

## ステップ 4 - ハッシュをループする

ハッシュリストにまたがったループも可能です。例えば、上記の例で、ユーザーを別の追加グループに割り当てる必要があるとします。例えば以下のような感じです。  

```yaml
- username: dev_user
  groups: ftp
- username: qa_user
  groups: ftp
- username: prod_user
  groups: apache
```

`user` モジュールはオプションパラメータとして `groups` を持っています。 ハッシュ内のこの値を取得する場合、 `{{ item }}` 内にサブキーワード、例えば、 `{{ item.groups }}` の様に入力します。  


<!-- {% raw %} -->
```yaml
---
- name: Ensure users
  hosts: node1
  become: yes

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

再度 playbook を実行し、出力を確認してみてください。  

  - 再度タスクが一覧表示されます。ただし、3つの変更が表示されます。その内容を含む各ループが表示されます。  

node1 内に `dev_user` がグループ `ftp` で作成されていることを確認します。  

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m command -a "id dev_user"
node1 | CHANGED | rc=0 >>
uid=1002(dev_user) gid=1002(dev_user) Gruppen=1002(dev_user),50(ftp)
```

----

[Ansible Engine ワークショップ表紙に戻る](../README.ja.md#section-1---ansible-engineの演習)
