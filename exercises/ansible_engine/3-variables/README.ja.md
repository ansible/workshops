# Exercise 3 - 変数、ループ、ハンドラを使う

前回までは Ansible Core の基礎部分を学習してきました。次の学習は playbook をより柔軟かつパワフルに使用できるより高度なスキルを学びたいと思います。

Ansible では task をよりシンプル、かつ再利用可能にできます。私たちは全てのシステムが全く同じではないことはわかっていますし、
playbookを実行する際、その違いに伴ってしばしば若干の変更が求められる場合があります。その際は変数を使います。

変数はシステム毎の違う部分の扱い、例えば port番号、IPアドレス、ディレクトリなどの違いの部分を吸収し扱う事ができます。

ループは task を繰り返し実行する場合に使います。例えば10個のソフトウェアパッケージを導入したい場合、ループを使うことにより1つの task で実現できます。

ハンドラはサービス再起動が必要な場合に使います。新たに設定ファイルの登録や、新規パッケージの導入が行われてはいませんでしたか?
その際、有効にするにはサービス再起動が必要かもしれません。その場合にハンドラを使用します。

変数、ループ、ハンドラの十分な理解のためには; Ansible documentation の以下部分を確認してください。

- [Ansible 変数](http://docs.ansible.com/ansible/latest/playbooks_variables.html)
- [Ansible ループ](http://docs.ansible.com/ansible/latest/playbooks_loops.html)
- [Ansible ハンドラ](http://docs.ansible.com/ansible/latest/playbooks_intro.html#handlers-running-operations-on-change)

## Section 1: Playbook の実行

まずは新しいplaybookを作成します。既に先の演習で作成していることもあり慣れた作業かと思います。


### Step 1:

ホームディレクトリにてプロジェクトとplaybookを作成します。

```bash
cd
mkdir apache-basic-playbook
cd apache-basic-playbook
vim site.yml
```


### Step 2:

playの定義といくつかの変数をPlaybookに追加します。このPlaybook中には、利用しているWebサーバへの追加パッケージのインストールと、Webサーバに特化したいくつかの構成が含まれています。

```yml
---
- hosts: web
  name: This is a play within a playbook
  become: yes
  vars:
    httpd_packages:
      - httpd
      - mod_wsgi
    apache_test_message: This is a test message
    apache_max_keep_alive_requests: 115
```

- `vars:` この後に続いて記述されるものが変数名であることをAnsibleに伝えています。
- `httpd_packages` httpd_packagesと命名したリスト型（list-type）の変数を定義しています。その後に続いているのはパッケージのリストです。
- `apache_test_message`, `apache_max_keep_alive_requests` 変数にはそれぞれ文字列と数字が設定されています。


### Step 3:

*install httpd packages* と命名した新規taskを追加します。

```yml
  tasks:
    - name: install httpd packages
      yum:
        name: "{{ item }}"
        state: present
      with_items: "{{ httpd_packages }}"
      notify: restart apache service
```

- `with_items: "{{ httpd_packages }}` Ansibleに `httpd_packages` の `item` 毎にタスクをループ実行するよう Ansible に伝えます
- `{{ item }}` この記述によって `httpd` や `mod_wsgi` といったリストのアイテムを展開するようAnsibleに伝えています。
- `notify: restart apache service` この行は `handler`であり、詳細は Section 3 で触れます


## Section 2: ファイルの実装とサービスの起動

ファイルやディレクトリを扱う必要がある場合には、[Ansible ファイル](http://docs.ansible.com/ansible/latest/list_of_files_modules.html) モジュールを用います。
今回は `file` や `template` モジュールを利用します。

その後、Apacheのサービスを起動するtaskを定義します。


### Step 1:

プロジェクトディレクトリ内の `templates` ディレクトリの作成と2ファイルのダウンロードを実施します。

```bash
mkdir templates
cd templates
curl -O http://ansible-workshop.redhatgov.io/workshop-files/httpd.conf.j2
curl -O http://ansible-workshop.redhatgov.io/workshop-files/index.html.j2

cd ../
```

### Step 2:
いくつかの file task と service task をplaybookに追加します。

```yml
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

- `file:` このモジュールを使ってファイル、ディレクトリ、シンボリックリンクの作成、変更、削除を行います。
- `template:` このモジュールで、jinja2テンプレートの利用と実装を指定しています。 `template` は `Files` モジュール・ファミリの中に含まれています。その他の[ファイル管理モジュール](http://docs.ansible.com/ansible/latest/list_of_files_modules.html) についても、一度目を通しておくことをお勧めします。
- *jinja* - [jinja2](http://docs.ansible.com/ansible/latest/playbooks_templating.html)は、Ansibleでテンプレートの中のfiltersのような式の中のデータを変更する場合に用います。
- *service* - serviceモジュールはサービスの起動、停止、有効化、無効化を行います。

template モジュールでは元となるファイル（今回は`templates/{index.html.j2,httpd.conf.j2}`）を予め準備しておき、この中にホストや状況に合わせて書き換えたい部分を変数化しておきます。そして、モジュールがこのファイルを配置する際に、変数化された箇所を値と入れ替えて配置してくれます。今回のように設定ファイルの配布に便利に使える以外にも、レポートを動的に生成して出力するなどとても応用範囲の広いモジュールです。


## Section 3: ハンドラの定義と利用

構成ファイルの実装や新しいパッケージのインストールなど、様々な理由でサービスやプロセスを再起動する必要が出てきます。このセクションには、Playbookへのハンドラの追加、そして意図しているtaskの後でこのハンドラを呼び出す、という2つの内容が含まれています。それではPlaybookへのハンドラの追加を見てみましょう。

### Step 1:
ハンドラを定義する。

```yml
  handlers:
    - name: restart apache service
      service:
        name: httpd
        state: restarted
        enabled: yes
```

---
**NOTE**

- `handler:` これで *play* に対して `tasks:` の定義が終わり、`handlers:` の定義が開始されたことを伝えています。これに続く箇所は、名前の定義、そしてモジュールやそのモジュールのオプションの指定のように他のtaskと変わらないように見えますが、これがハンドラの定義になります。
- `notify: restart apache service` そしてついに、この部分でハンドラが呼び出されるのです！ `nofify` 宣言は名前を使ってハンドラを呼び出します。単純明快ですね。先に書いた `copy httpd.conf` task中に `notify` 宣言を追加した理由がこれで理解できたと思います。

---

## Section 4: この演習の最後に

これで洗練されたPlaybookの完成です!
でもまだPlaybookを実行しないでください。それはこの後の演習で行います。
その前に、全てが意図した通りになっているかもう一度見直してみましょう。
もしも間違っていれば修正してください。
以下の見本を参考に、スペースとインデントに注意して見てください。`--syntax-check` で構文をチェックするのも良いアイデアです。


```yml
---
- hosts: web
  name: This is a play within a playbook
  become: yes
  vars:
    httpd_packages:
      - httpd
      - mod_wsgi
    apache_test_message: This is a test message
    apache_max_keep_alive_requests: 115

  tasks:
    - name: httpd packages are present
      yum:
        name: "{{ item }}"
        state: present
      with_items: "{{ httpd_packages }}"
      notify: restart apache service

    - name: site-enabled directory is present
      file:
        name: /etc/httpd/conf/sites-enabled
        state: directory

    - name: latest httpd.conf is present
      template:
        src: templates/httpd.conf.j2
        dest: /etc/httpd/conf/httpd.conf
      notify: restart apache service

    - name: latest index.html is present
      template:
        src: templates/index.html.j2
        dest: /var/www/html/index.html

    - name: httpd is started and enabled
      service:
        name: httpd
        state: started
        enabled: yes

  handlers:
    - name: restart apache service
      service:
        name: httpd
        state: restarted
        enabled: yes
```

---

[Click Here to return to the Ansible Linklight - Ansible Engine Workshop](../README.ja.md)
