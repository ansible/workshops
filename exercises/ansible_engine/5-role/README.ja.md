# Exercise 1.5 - Roles: Playbookを再利用可能にする

このワークショップで行ってきているように、Playbookを1つのファイルに書くことも可能です。
しかし実際の運用においては、他の人が作成したPlaybookを再利用したくなってくる筈です。

これを実現するのがAnsibleのRolesという考え方です。
roleを作成する事でPlaybookをパーツとして分解し、構造化されたディレクトリに格納することができます。
「え?? それはExercise 1.2で触れられていた、ややこしい[ベスト・プラクティス](http://docs.ansible.com/ansible/playbooks_best_practices.html)のことですか?」って？
はい、まさにその通りです。

この演習では先に作成したPlaybookをリファクタリングしてroleへと変えます。さらにAnsible Galaxyの使い方も学びます。

では apache-basic-playbook をroleへとブレークダウンする方法を見て行きましょう。

![apache-basic-playbookのroleディレクトリ構造](roledir_1.png)

幸いにも、これらのディレクトリやファイルの全てを手動で作成する必要はありません。ここで登場するのがAnsible Galaxyです。

## Section 1: Ansible Galaxyを使って新しいroleを初期化する

Ansible Galaxyは、roleの検索とダウンロード、そして共有を可能にするフリーのサイトです。そしてまた、これを使えば今ここで行おうとしている事も容易に行えます。


### Step 1:

 `apache-basic-playbook` プロジェクトへ移動します。

```bash
cd ~/apache-basic-playbook
```


### Step 2:

 `roles` と命名したディレクトリを作成し `cd` で作成したディレクトリへ移動し、ファイルが何もないことを確認します。

```bash
mkdir roles
cd roles
ls -la
```


### Step 3:

 `ansible-galaxy` コマンドで `apache-simple` と命名した新しいroleを用いて、Ansibleのベストプラクティスに則った空のフレームワークを構成します。

```bash
ansible-galaxy init apache-simple

tree apache-simple
```

ここまでで作成された構造を`tree`コマンドなどで確認してください。
先の図 1とよく似た構造になっている筈です。
次のセクションへ進む前にあと1つだけ終らせるステップが残っています。

それはgalaxyコマンドで作成されたからのフレームワークから、利用しないディレクトリとファイルをクリーンアップすることです。
今回作成したroleでは `files` と `tests` からは何も利用しません。


### Step 4:

`files` と `tests` ディレクトリを削除します。

```bash
cd ~/apache-basic-playbook/roles/apache-simple/
rm -rf files tests
```


## Section 2: `site.yml` Playbookを新たに作成した`apache-simple` roleへ切り分ける


このセクションではPlaybookに含まれている`vars:`、 `tasks:`、 `template:`、 そして `handlers:` を主要パーツとして切り分けます。

### Step 1:

`site.yml` のバックアップ・コピーを作成し、新しい `site.yml` を作成します。

```bash
cd ~/apache-basic-playbook
mv site.yml site.yml.bkup
vim site.yml
```

### Step 2:

play の定義と role の呼び出しを追加します。

```yml
---
- hosts: web
  name: This is my role-based playbook
  become: yes

  roles:
    - apache-simple
```

### Step 3:

`roles/apache-simple/defaults/main.yml` のroleにデフォルトの変数を追加します。

```yml
---
# defaults file for apache-simple
apache_test_message: This is a test message
apache_max_keep_alive_requests: 115
```

### Step 4:

roleに特化した変数を`roles/apache-simple/vars/main.yml` のroleへ追加します。

```yml
---
# vars file for apache-simple
httpd_packages:
  - httpd
  - mod_wsgi
```

---
**NOTE**
####
> えっと、ちょっと待ってください…​ いま変数を2つの場所に分けて置きませんでしたか？

ええ…​ 実はその通りです。変数は柔軟に配置することができます。例をあげると: +

- vars ディレクトリ
- defaultsディレクトリ
- group_varsディレクトリ
- Playbookの `vars:` セクション配下
- コマンドラインを使い `--extra_vars` オプションで指定された全てのファイル

結論から言えば、[variable precedence(英語)](http://docs.ansible.com/ansible/latest/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable) に目を通し、どこで変数を定義するのか、そしてどのロケーションが優先されるのかを理解する必要があります。融通が利くように、この演習ではrole defaultsを利用していくつかの変数を定義しています。 それに続いて、role defaultsよりも高い優先性を持ち、デフォルトの変数をオーバーライドできる`/vars`にいくつかの変数を定義しています。

---

### Step 5:

`roles/apache-simple/handlers/main.yml` にroleのハンドラを作成します。


```yml
---
# handlers file for apache-simple
- name: restart apache service
  service:
    name: httpd
    state: restarted
    enabled: yes
```

### Step 6:

`roles/apache-simple/tasks/main.yml` のroleにtasksを追加します。

```yml
---
# tasks file for apache-simple
- name: install httpd packages
  yum:
    name: "{{ item }}"
    state: present
  with_items: "{{ httpd_packages }}"
  notify: restart apache service

- name: create site-enabled directory
  file:
    name: /etc/httpd/conf/sites-enabled
    state: directory

- name: copy httpd.conf
  template:
    src: templates/httpd.conf.j2
    dest: /etc/httpd/conf/httpd.conf
  notify: restart apache service

- name: copy index.html
  template:
    src: templates/index.html.j2
    dest: /var/www/html/index.html

- name: start httpd
  service:
    name: httpd
    state: started
    enabled: yes
```

### Step 7:

`roles/apache-simple/templates/` へいくつかのテンプレートをダウンロードします。
その後すぐ、演習 2.1の古いテンプレート・ディレクトリを削除し、クリーンアップを行います。

```bash
mkdir -p ~/apache-basic-playbook/roles/apache-simple/templates/
cd ~/apache-basic-playbook/roles/apache-simple/templates/
curl -O http://ansible-workshop.redhatgov.io/workshop-files/httpd.conf.j2
curl -O http://ansible-workshop.redhatgov.io/workshop-files/index.html.j2
rm -rf ~/apache-basic-playbook/templates/
```

### Step 8:

作成したロールの全体像を確認してみましょう。

```bash
cd ~/apache-basic-playbook

tree .
```


## Section 3: ロール・ベースの新しいPlaybookを実行します。

これでオリジナルのPlaybookをroleに切り分けることができました。では実際に実行してみましょう。

### Step 1:

playbookを実行します。

```bash
ansible-playbook site.yml
```

もしも問題なく実行されれば、標準出力は以下の図のようになる筈です。

![ロール・ベースの標準出力](stdout_3.png)

## Section 4: この演習の最後に

これで、1つの `apache-simple` roleを持つPlaybook、`site.yml` は完成です。Playbookを構造化されたrolesにすることの利点は、新たなrolesをAnsible Galaxyを使って、または自身の手で記述して追加できることにあります。またrolesを用いれば、容易に変数やtasksやテンプレート等を変更できます。

---

[Click Here to return to the Ansible Linklight - Ansible Engine Workshop](../README.ja.md)

