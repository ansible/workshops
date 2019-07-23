# 演習 1.5 - 条件, ハンドラ、繰り返し（ループ）

## ステップ 1.5.1 - 条件

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

詳しくは、次のドキュメントを参照してください: <https://docs.ansible.com/ansible/latest/user_guide/playbooks_conditionals.html#the-when-statement>

例として、 "ftpserver"インベントリグループにあるホストにのみ、FTPサーバーをインストールすることを考えてみます。

では早速やってみましょう。まず、デフォルトで指定されたインベントリファイル編集し、`ftpserver` グループに `node2` を入れます。
デフォルトのインベントリファイルは、`/home/student<X>/lightbulb/lessons/lab_inventory/student<X>-instances.txt` でしたね。♪
編集後は以下の様になります。

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

## ステップ 1.5.2 - ハンドラ

プレイブックを書いていると、特定のタスクが実行された時のみ、さらに追加のタスクを実行したい場合があります。たとえば、サービスの更新や設定ファイルを変更した場合に、変更した設定が有効になるようにサービスの再起動が必要となるケースです。

このような場合にハンドラを利用します。ハンドラーは、 "notify" ステートメントで定義されたタスクが実行された場合にのみ実行される非アクティブタスクです。詳しくはマニュアルをご確認ください。 [Ansible Handlers](http://docs.ansible.com/ansible/latest/playbooks_intro.html#handlers-running-operations-on-change) documentation.

早速演習で試してみましょう。以下のような Playbook を作ります。

  - 全 `web` グループのホストに対して、 Apache の構成ファイル `httpd.conf` をコピーする

  - ファイルが変更された時のみ Apache のサービスをリスタートする

演習を実行するため、コピーするための httpd.conf を node1 から取得します。

```bash
[student<X>@ansible ansible-files]$ scp <node1>:/etc/httpd/conf/httpd.conf ~/ansible-files/.
student<X>@11.22.33.44's password: 
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

So what’s new here?

  - "notify" セクションは、コピータスクがファイルを変更したときだけハンドラを呼び出します。つまり、サービス再起動は必要な場合にのみ（この例の場合はファイルの更新が行われた場合のみ）行われます。

  - "ハンドラ" セクションは、notify から呼び出された時に実際に実行されるタスクを定義します。

まずこのまま playbook を実行してみてください。まだ httpd.conf に何も変更を加えていないので、changed は "0" で、ハンドラも動作していないことが分かると思います。

  - httpd.conf の中の、 `Listen 80` の行を以下の通り変更します。


```ini
Listen 8080
```

  - Playbookをもう一度実行してください。興味深い結果が得られます。
    
      - httpd.conf が上書きコピーされた
    
      - ハンドラが呼び出され、 Apache サービスをリスタートした

Apacheはポート8080でリッスンしているはずです。試してみてください。

```bash
[student1@ansible ansible-files]$ curl http://<node1>
curl: (7) Failed connect to 22.33.44.55:80; Connection refused
[student1@ansible ansible-files]$ curl http://22.33.44.55:8080
<body>
<h1>This is a production webserver, take care!</h1>
</body>
```
httpd.conf ファイルを再度変更し、どうなるか試してみてください。

> **ヒント**
> 
> よく聞かれる質問として、notify セクションが実行されたらすぐにハンドラが呼び出されるのか？ということ。これは違います。今回の場合、notify 直下にハンドラが定義されているのですぐの実行となりますが、notiry とハンドラが離れていた場合は、あくまで上から順に実行され、ハンドラの順番になったところで実行されます。 notify でハンドラ実行のフラグを立てておく感じです。

## ステップ 1.5.3 - Simple Loops

Loops enable us to repeat the same task over and over again. For example, lets say you want to create multiple users. By using an Ansible loop, you can do that in a single task. Loops can also iterate over more than just lists: for example if you have a list of users with their coresponding group, loop can iterate over them as well. Find out more about loops in the [Ansible Loops](https://docs.ansible.com/ansible/latest/user_guide/playbooks_loops.html) documentation.

To show the loops feature we will generate three new users on `node1`. For that, create the file `loop_users.yml` in `~/ansible-files` on your control node as your student user. We will use the `user` module to generate the user accounts.

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

Understand the playbook and the output:

  - The names are not provided to the user module directly. Instead, there is only a variable called `{{ item }}` for the parameter `name`.

  - The `loop` keyword lists the actual user names. Those replace the `{{ item }}` during the actual execution of the playbook.

  - During execution the task is only listed once, but there are three changes listed underneath it.

## Step 5.4 - Loops over hashes

As mentioned loops can also be over lists of hashes. Imagine that the users should be assigned to different additional groups:

```yaml
- username: dev_user
  groups: ftp
- username: qa_user
  groups: ftp
- username: prod_user
  groups: apache
```

The `user` module has the optional parameter `groups` to list additional users. To reference items in a hash, the `{{ item }}` keyword needs to reference the subkey: `{{ item.groups }}` for example.

Let's rewrite the playbook to create the users with additional user rights:

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

Check the output:

  - Again the task is listed once, but three changes are listed. Each loop with its content is shown.

Verify that the user `prod_user` was indeed created on `node1`:

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m command -a "id dev_user"
node1 | CHANGED | rc=0 >>
uid=1002(dev_user) gid=1002(dev_user) Gruppen=1002(dev_user),50(ftp)
```

----

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-1---ansible-engine-exercises)

