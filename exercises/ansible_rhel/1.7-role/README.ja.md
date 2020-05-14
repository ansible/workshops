# 演習 - Roles: Playbook を再利用可能にする

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

* [ステップ 1 - Ansible Roles 構造を理解する](#ステップ-1---ansible-roles-構造を理解する)
* [ステップ 2 - 基本的な Role ディレクトリ構造を作成する](#ステップ-2---基本的な-role-ディレクトリ構造を作成する)
* [ステップ 3 - タスクファイルの作成](#ステップ-3---タスクファイルの作成)
* [ステップ 4 - ハンドラーの作成](#ステップ-4---ハンドラーの作成)
* [ステップ 5 - index.html の作成とバーチャルホスト用テンプレートファイルの作成](#ステップ-5---indexhtml-の作成とバーチャルホスト用テンプレートファイルの作成)
* [ステップ 6 -  Role のテスト実行](#ステップ-6----role-のテスト実行)

今までのワークショップで学習してきた通り、Playbook を1つのファイルに書くことは可能です。しかしそのうち、作成した Playbook を再利用したいと考えるようになると思います。  

これを実現するのが Ansible の Roles です。Role という形で Playbook をパーツとして分解し、構造化されたディレクトリに納めるのです。詳しくはこちらの [ベストプラクティス](http://docs.ansible.com/ansible/playbooks_best_practices.html) をご確認ください。  

## ステップ 1 - Ansible Roles 構造を理解する

Roles は基本的に、includeディレクティブを自動化したものであり、実際には参照ファイルの検索パス処理に対するいくつかの機能を超えた追加の魔法的な手段は含まれていません。

Roles は定義されたディレクトリ構造に従い、最上位ディレクトリ名で区別されます。いくつかのサブディレクトリの中には `main.yml` という名前の YAML ファイルが含まれています。 `files` と `templates` のサブディレクトリには YAML ファイルによって参照されるオブジェクトを入れておくことができます。  

一例を下記します。Roles の名前は "apache" です。  

```text
apache/
├── defaults
│   └── main.yml
├── files
├── handlers
│   └── main.yml
├── meta
│   └── main.yml
├── README.md
├── tasks
│   └── main.yml
├── templates
├── tests
│   ├── inventory
│   └── test.yml
└── vars
    └── main.yml
```

`main.yml` ファイルは、対応するディレクトリに応じたコンテンツが含まれています。例えば、  `vars/main.yml` では変数が定義され、 `handlers/main.yaml` では、ハンドラーが記述される等です。一見 Playbook と似ていますが、これらの `main.yml` ファイルの中には特定のコンテンツが含まれるのみで、その他の例えば host の `become` やその他のキーワードなど通常のプレイブックに記載される情報は含まれません。

> **ヒント**
>
> 変数定義に関しては、 `vars` と `default` という2つのディレクトリがあります。変数定義には優先順位があり、`default` は最も優先順位が低くなっています。Playbook 実行時に、上書きされることも意識した、まさにデフォルトの値を定義する場所です。

Playbook で Roles を呼び出すのは以下の通り簡単です。  

```yaml
---
- name: launch roles
  hosts: web
  roles:
    - role1
    - role2
```

タスク、ハンドラー、変数など各々の Roles がこの順番で Playbook に組み込まれます。 Roles で定義されたディレクトリに、コピー、スクリプト、テンプレート、タスクを入れることで、絶対パスや相対パスを意識することなくそれぞれの Role にアクセスすることができます。    

## ステップ 2 - 基本的な Role ディレクトリ構造を作成する    

Ansible は、プロジェクトディレクトリ内の `roles` サブディレクトリの中から該当する Role を探します。これは　Ansible　の設定ファイルで上書きすることも可能です。それぞれの Role は独自のディレクトリ構造を持っています。新規 Role のディレクトリを作成するために `ansible-galaxy` を利用することも可能です。  

> **ヒント**
>
> Ansible Galaxyは、最高の Ansible コンテンツを見つけて利用したり、逆に、共有するためのハブとしての利用が可能です。Ansible Galaxy の利用には、 `ansible-galaxy` コマンドを使います。今回は、 Role ディレクトリ構造を作成するために使用します。  

早速 Role を作成してみましょう。Apache をインストールして仮想ホストとして機能するように設定する Role のディレクトリを構築します。このコマンドは、 `~/ansible-files` ディレクトリで実行してください。  

```bash
[student<X>@ansible ansible-files]$ mkdir roles
[student<X>@ansible ansible-files]$ ansible-galaxy init --offline roles/apache_vhost
```

作成された Role ディレクトリとその中身を確認してみてください。

```bash
[student<X>@ansible ansible-files]$ tree roles
```

## ステップ 3 - タスクファイルの作成  

サブディレクトリにある "tasks" の中の `main.yml` ファイルに以下の内容を記述していきます。  

  - httpd をインストールする  

  - httpd を有効化する  

  - HTML コンテンツを Apache のルートディレクトリに配置する  

  - バーチャルホストを構成するためのテンプレートを作成し読み込ませる  

> **注意**  
>
> **`main.yml` にはタスクのみを記述します。今まで記述した Playbook 丸ごとではありません！**

`roles/apache_vhost` ディレクトリ内の `tasks/main.yml` ファイルを以下の様に編集します。  

```yaml
---
- name: install httpd
  yum:
    name: httpd
    state: latest

- name: start and enable httpd service
  service:
    name: httpd
    state: started
    enabled: true
```

上記で追加したタスクは以下のとおりです。  

  - yum モジュールを使ってhttpdパッケージをインストールする  

  - service モジュールを使って httpd を起動し、有効化します。  

次に、仮想ホストのディレクトリ構造を確認・作成し、HTMLコンテンツをコピーするためのタスクをさらにそれぞれ追記します。追記するファイルは先ほどの `main.yml`です。  

<!-- {% raw %} -->
```yaml
- name: ensure vhost directory is present
  file:
    path: "/var/www/vhosts/{{ ansible_hostname }}"
    state: directory

- name: deliver html content
  copy:
    src: index.html
    dest: "/var/www/vhosts/{{ ansible_hostname }}"
```
<!-- {% endraw %} -->

vhost ディレクトリは、 `file` モジュールを使って、無ければ作成、既に存在すればスキップされることに注意ください。  

そして最後に、テンプレートモジュールを使用してj2-templateから仮想ホストの設定ファイルを作成するためのタスクを追記します。追記するファイルは同じく `main.yml`です。    

```yaml
- name: template vhost file
  template:
    src: vhost.conf.j2
    dest: /etc/httpd/conf.d/vhost.conf
    owner: root
    group: root
    mode: 0644
  notify:
    - restart_httpd
```
設定の更新が行われた場合、ハンドラーを使用して httpd を再起動していることに注意してください。  

出来上がった `tasks/main.yml` ファイルは以下の通りです。

<!-- {% raw %} -->
```yaml
---
- name: install httpd
  yum:
    name: httpd
    state: latest

- name: start and enable httpd service
  service:
    name: httpd
    state: started
    enabled: true

- name: ensure vhost directory is present
  file:
    path: "/var/www/vhosts/{{ ansible_hostname }}"
    state: directory

- name: deliver html content
  copy:
    src: index.html
    dest: "/var/www/vhosts/{{ ansible_hostname }}"

- name: template vhost file
  template:
    src: vhost.conf.j2
    dest: /etc/httpd/conf.d/vhost.conf
    owner: root
    group: root
    mode: 0644
  notify:
    - restart_httpd
```
<!-- {% endraw %} -->


## ステップ 4 - ハンドラーの作成  

`handlers/main.yml` を以下の通り編集し、テンプレートタスクから呼び出された時に httpd を再起動するハンドラーを作成します。  

```yaml
---
# handlers file for roles/apache_vhost
- name: restart_httpd
  service:
    name: httpd
    state: restarted
```

## ステップ 5 - index.html の作成とバーチャルホスト用テンプレートファイルの作成  

Webサーバーによって提供されるHTMLコンテンツを作成します。  

  - `files` サブディレクトリの中に、 index.html ファイルを作成します。   

```bash
[student<X>@ansible ansible-files]$ echo 'simple vhost index' > roles/apache_vhost/files/index.html
```

  -  `templates` サブディレクトリの中に `vhost.conf.j2` テンプレートを作成します。

<!-- {% raw %} -->
```html
# {{ ansible_managed }}
Listen 8080
<VirtualHost *:8080>
    ServerAdmin webmaster@{{ ansible_fqdn }}
    ServerName {{ ansible_fqdn }}
    ErrorLog logs/{{ ansible_hostname }}-error.log
    CustomLog logs/{{ ansible_hostname }}-common.log common
    DocumentRoot /var/www/vhosts/{{ ansible_hostname }}/

    <Directory /var/www/vhosts/{{ ansible_hostname }}/>
  Options +Indexes +FollowSymlinks +Includes
  Order allow,deny
  Allow from all
    </Directory>
</VirtualHost>
```
<!-- {% endraw %} -->

> **ヒント**
>
> 上記はバーチャルホストを追加するための httpd 用の設定ファイルで、ここでは深く理解する必要はありません。8080 ポートをリッスンする Webサーバー が立ち上がり、ルートフォルダは "/var/www/vhosts/{{ ansible_hostname }}/"。その中に、'simple vhost index' と記載された index.html がコピーされる・・・、くらいの理解で大丈夫です。  

## ステップ 6 -  Role のテスト実行

`node2` に対し、 Roles をテストする準備が整いました。しかし、 Roles はノードに直接割り当てることができないため、まず Roles とホストを紐づけるプレイブックを作成します。 `~/ansible-files` ディレクトリの直下に `test_apache_role.yml` ファイルを以下の内容で作成します。

```yaml
---
- name: use apache_vhost role playbook
  hosts: node2
  become: yes

  pre_tasks:
    - debug:
        msg: 'Beginning web server configuration.'

  roles:
    - apache_vhost

  post_tasks:
    - debug:
        msg: 'Web server has been configured.'
```

`pre_tasks` と `post_tasks` というキーワードに注意してください。通常、 Roles のタスクはプレイブックのタスクの前に実行されます。この順番を制御するため、 `pre_tasks` を指定してRolesの前に実行されるタスクを定義できます。逆に `post_tasks` は、すべての Roles が完了した後に実行されます。ここでは、実際の Roles が実行されたときにどういう順番で実行されたかを確認するため、これら2つのタスクをあえて入れています。  

Playbook を実行する準備が整いましたので、実行してみましょう！  

```bash
[student<X>@ansible ansible-files]$ ansible-playbook test_apache_role.yml
```

`node2` に対して curl コマンドを実行して、 Roles が機能していることを確認します。バーチャルホストのポートは8080です。  

```bash
[student<X>@ansible ansible-files]$ curl -s http://node2:8080
simple vhost index
```

> **ヒント**
>
> 8080 →　80 に代えるとどうなりますか？

うまくいきましたか？  
おめでとうございます！ これで Ansible Engine のワークショップは終了です！！

----

[Ansible Engine ワークショップ表紙に戻る](../README.ja.md#section-1---ansible-engineの演習)
