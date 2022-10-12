# ワークショップ演習 - ロール: Playbook を再利用可能にする

**他の言語でもお読みいただけます**:
<br>![uk](../../../images/uk.png) [English](README.md)、![japan](../../../images/japan.png)[日本語](README.ja.md)、![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md)、![france](../../../images/fr.png) [Française](README.fr.md)、![Español](../../../images/col.png) [Español](README.es.md)

## 目次

* [目的](#目的)
* [ガイド](#ガイド)
  * [ステップ 1 - Ansible ロール構造について](#ステップ-1---ansible-ロール構造について)
  * [ステップ 2 - 基本的なロールディレクトリー構造の作成](#ステップ-2---基本的なロールディレクトリー構造の作成)
  * [ステップ 3 - タスクファイルの作成](#ステップ-3---タスクファイルの作成)
  * [ステップ 4 - ハンドラーの作成](#ステップ-4---ハンドラーの作成)
  * [ステップ 5 - web.html と vhost 設定ファイルテンプレートの作成](#ステップ-5---webhtml-と-vhost-設定ファイルテンプレートの作成)
  * [ステップ 6 - ロールのテスト](#ステップ-6---ロールのテスト)
* [トラブルシューティング問題](#トラブルシューティング問題)

## 目的

このワークショップ全体で行ったように、1 つのファイルで Playbook を作成することは可能ですが、最終的には複数のファイルを再利用して、整理することをお勧めします。

これを行うには、Ansible Roles を使用します。ロールを作成するときは、Playbook を複数のパーツに分け、それらのパーツをディレクトリー構造に配置します。これについては、[ヒントとコツ](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html) および [Ansible 設定の例](https://docs.ansible.com/ansible/latest/user_guide/sample_setup.html) で詳しく説明されています。

この演習では、以下について説明します。

* Ansible Role のフォルダー構造
* Ansible Role を構築する方法
* ロールを使用して実行するための Ansible Play の作成
* Ansible を使用した node2 での Apache VirtualHost の作成

## ガイド

### ステップ 1 - Ansible ロール構造について

ロールは、定義されたディレクトリ構造に従います。ロールは、最上位ディレクトリーによって名前が付けられます。一部のサブディレクトリーには、`main.yml` という YAML ファイルが含まれています。ファイルとテンプレートのサブディレクトリーには、YAML ファイルによって参照されるオブジェクトを含めることができます。

プロジェクト構造の例は次のようになります。ロールの名前は「apache」になります。

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

さまざまな `main.yml` ファイルには、上記のディレクトリー構造内の場所に応じたコンテンツが含まれています。例えば、`vars/main.yml` は変数を参照し、`handlers/main.yaml` はハンドラーなどについて説明します。Playbook とは対照的に、`main.yml` ファイルには特定のコンテンツのみが含まれ、ホスト、`become` またはその他のキーワードなどの追加の Playbook 情報は含まれません。

> **ヒント**
>
> `vars` と `default` には、実際には 2 つのディレクトリーがあります。デフォルトの変数 `defaults/main.yml` には最も低い優先度が付けられます。また、ロールの作成者によって設定されたデフォルト値が含まれます。これは、これらの値のオーバーライドが意図されているときに使用されます。`vars/main.yml` で設定されている変数は、変更しないことを想定した変数です。

Playbook でのロールの使用は簡単です。

```yaml
---
- name: launch roles
  hosts: web
  roles:
    - role1
    - role2
```

各ロールについては、そのロールのタスク、ハンドラー、および変数が、その順序で Playbook に含まれます。ロール内のコピー、スクリプト、テンプレート、またはインクルードタスクは、*絶対パス名または相対パス名なしで*関連するファイル、テンプレート、またはタスクを参照できます。Ansible は、それらの使用に基づいて、ロールのファイル、テンプレート、またはタスクで検索します。


### ステップ 2 - 基本的なロールディレクトリー構造の作成

Ansible は、プロジェクト内の `roles` というサブディレクトリーを探します。これは、Ansible 構成でオーバーライドできます。各ロールには独自のディレクトリーがあります。新しいロールの作成を容易にするには、`ansible-galaxy` というツールを使用できます。

> **ヒント**
>
> Ansible Galaxy は、最適な Ansible コンテンツの検索、再利用、共有を行うためのハブです。`ansible-galaxy` は、Ansible Galaxy とのやりとりに便利です。今の時点では、ディレクトリー構造の構築を行うためのヘルパーとして使用します。

さて、ロールを作ってみましょう。仮想ホストにサービスを提供するように Apache をインストールして構成するロールを構築します。これらのコマンドは `~/ansible-files` ディレクトリーで実行します。

```bash
[student@ansible-1 ansible-files]$ mkdir roles
[student@ansible-1 ansible-files]$ ansible-galaxy init --offline roles/apache_vhost
```

ロールディレクトリーとその内容を見てください。

```bash
[student@ansible-1 ansible-files]$ tree roles
```

```text
roles/
└── apache_vhost
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

### ステップ 3 - タスクファイルの作成

ロールのタスクサブディレクトリーの `main.yml` は、以下を行う必要があります。

* httpd がインストールされていることを確認
* httpd が起動し、有効になっていることを確認
* HTML コンテンツを Apache ドキュメントルートに配置
* vhost の設定用のテンプレートのインストール

> **警告**
>
> **`main.yml` (main.yml に含まれる可能性のあるその他ファイル) は、完全な Playbook *ではなく* タスクのみを含めることができます。**

`roles/apache_vhost/tasks/main.yml` ファイルを編集します。

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

タスクが追加されたことに注意してください。Playbook の詳細は表示されません。

これまで追加されたタスクは以下を行います。

* yum モジュールを使用した httpd パッケージのインストール
* サービスモジュールを使用した httpd の有効化と起動

次に、vhost ディレクトリー構造を確認し、html コンテンツをコピーするための、さらに 2 つのタスクを追加します。

<!-- {% raw %} -->

```yaml
- name: ensure vhost directory is present
  file:
    path: "/var/www/vhosts/{{ ansible_hostname }}"
    state: directory

- name: deliver html content
  copy:
    src: web.html
    dest: "/var/www/vhosts/{{ ansible_hostname }}/index.html"
```

<!-- {% endraw %} -->

vhost ディレクトリーは、`file` モジュールで作成/確認されることに注意してください。

追加する最後のタスクはテンプレートモジュールを使用して、j2-template から vhost 構成ファイルを作成します。

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

構成の更新後にハンドラーを使用して httpd を再起動していることに注意してください。

完全な `tasks/main.yml` ファイルは以下の通りです。

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
    src: web.html
    dest: "/var/www/vhosts/{{ ansible_hostname }}/index.html"

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

### ステップ 4 - ハンドラーの作成

`roles/apache_vhost/handlers/main.yml` ファイルにハンドラーを作成し、テンプレートタスクで通知されたときに httpd を再起動します。

```yaml
---
# handlers file for roles/apache_vhost
- name: restart_httpd
  service:
    name: httpd
    state: restarted
```

### ステップ 5 - web.html と vhost 設定ファイルテンプレートの作成

Web サーバーによってサービスされる HTML コンテンツを作成します。

* ロールの「src」ディレクトリー `files` に web.html ファイルを作成します。

```bash
#> echo 'simple vhost index' > ~/ansible-files/roles/apache_vhost/files/web.html
```

* ロールの `templates` サブディレクトリーに `vhost.conf.j2` テンプレートを作成します。

`vhost.conf.j2` テンプレートファイルの内容を以下に示します。

<!-- {% raw %} -->

```text
# {{ ansible_managed }}

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

### ステップ 6 - ロールのテスト

`node2` に対してロールをテストする準備が整いました。ただし、役割をノードに直接割り当てることはできないため、最初に役割とホストを接続する Playbook を作成します。ファイル `test_apache_role.yml` をディレクトリー `~/ansible-files` に作成します。

```yaml
---
- name: use apache_vhost role playbook
  hosts: node2
  become: true

  pre_tasks:
    - debug:
        msg: 'Beginning web server configuration.'

  roles:
    - apache_vhost

  post_tasks:
    - debug:
        msg: 'Web server has been configured.'
```

`pre_tasks` および `post_tasks` キーワードに注目してください。通常、Playbook のタスクの前に、ロールのタスクが実行されます。実行の順序を制御するため、ロールが適用される前に `pre_tasks` が実行されます。`post_tasks` は、すべてのロールが完了した後に実行されます。ここでは、これを使用して、実際のロールが実行されたときに、わかりやすくなるようにします。

これで、Playbook を実行する準備が整いました。

```bash
[student@ansible-1 ansible-files]$ ansible-navigator run test_apache_role.yml
```

`node2` に curl コマンドを実行して、ロールが動作したことを確認します。

```bash
[student@ansible-1 ansible-files]$ curl -s http://node2:8080
simple vhost index
```

おめでとうございます。これでこの演習は終わりです。

## トラブルシューティング問題

最後の curl は動作しましたか？ ss コマンドを実行すると、Web サーバーが動作しているポートを確認できます。

```bash
#> sudo ss -tulpn | grep httpd
```

次のような行があるはずです。

```bash
tcp   LISTEN 0      511                *:8080               *:*    users:(("httpd",pid=182567,fd=4),("httpd",pid=182566,fd=4),("httpd",pid=182565,fd=4),("httpd",pid=182552,fd=4))
```

これが機能していない場合は、`/etc/httpd/conf/httpd.conf` に `Listen 8080` が指定されていることを確認してください。これは、[演習 1.5](../1.5-handlers) で変更しています。

---
**ナビゲーション**
<br>
[前の演習](../1.6-templates) - [次の演習](../2.1-intro)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-1---ansible-engine-exercises)
