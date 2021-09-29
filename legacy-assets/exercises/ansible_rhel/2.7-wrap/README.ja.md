# ワークショップ演習 - まとめ

**その他の言語はこちらをお読みください。**
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

## 目次

* [目的](#objective)
* [ガイド](#guide)
  * [ステージの設定](#lets-set-the-stage)
  * [Git リポジトリー](#the-git-repository)
  * [インベントリーの準備](#prepare-inventory)
  * [テンプレートの作成](#create-the-template)
  * [結果の確認](#check-the-results)
  * [Survey の追加](#add-survey)
  * [ソリューション](#solution)
* [終わり](#the-end)

## 目的

これは、これまで学んだことの復習を目的とした最後のチャレンジです。

## ガイド

### ステージを設定しましょう

運営チームとアプリケーション開発チームは、AnsibleTower の機能を気に入っています。実際の環境で使用するために、要件を次にまとめました。

* すべてのウェブサーバー (`node1`、`node2`、`node3`) を 1 つのグループに入れる必要があります

* Web サーバーは開発目的または本番環境で使用できるため、それに応じて「stage dev」または「stage
  prod」としてフラグを立てる方法が必要です。

  * 現在、`node1` と `node3` が開発システムとして使用され、`node2` が稼働環境となっています。

* もちろん、世界的に有名なアプリケーション「index.html」の内容は、開発段階と製品段階で異なります。

  * 環境を示した、ページにタイトルが表示されます。
  * コンテンツフィールドがあります。

* コンテンツライター `wweb` には、dev サーバーと prod サーバーのコンテンツを変更するための調査にアクセスできる必要があります。

### Git レポジトリー

すべてのコードはすでに配置されています。これは Tower
ラボですから。[https://github.com/ansible/workshop-examples](https://github.com/ansible/workshop-examples)
にある** Workshop Project ** git リポジトリを確認してください。そこに Playbook `role_webcontent`
があります。これは、ロール `webcontent.yml` を呼び出します。

以前の Apache インストールのロールと比較すると、大きな違いがあります。現在、2つのバージョンの `index.html`
テンプレート、およびソースファイル名の一部として変数を持つテンプレートファイルをデプロイするタスクがあります。

`dev_index.html.j2`

<!-- {% raw %} -->

```html
<body>
<h1>これは開発 Web サーバーです。お楽しみください!</h1>
{{ dev_content }}
</body>
```

<!-- {% endraw %} -->

`prod_index.html.j2`

<!-- {% raw %} -->

```html
<body>
<h1>This is a production webserver, take care!</h1>
{{ prod_content }}
</body>
```

<!-- {% endraw %} -->

`main.yml`

<!-- {% raw %} -->

```yaml
[...]
- name: Deploy index.html from template
  template:
    src: "{{ stage }}_index.html.j2"
    dest: /var/www/html/index.html
  notify: apache-restart
```

<!-- {% endraw %} -->

### インベントリーの準備

もちろん、これを達成する方法は複数ありますが、次のことを行う必要があります。

* すべてのホストがインベントリグループ `Webserver` に含まれていることを確認してください。
* `Webserver` インベントリーに値 `stage` で変数 `dev` を定義します。

  * 開始用の 3 つのダッシュ (---) の下の **VARIABLES** で、インベントリー `Webserver` に `stage:
    dev` を追加します。

* 同じように、変数 `stage: prod` を追加しますが、今回は、`node2` に対してのみ行います
  (ホスト名をクリック)。インベントリー変数が上書きされます。

> **ヒント**
>
> YAML の開始をマークする 3 つのダッシュと `ansible_host` の行を所定の位置に配置するようにしてください。

### テンプレートの作成。

* 以下ような新しい `Create Web Content` という **Job Template** を作成します。

  * `Webserver` インベントリーを対象
  * **Workshop Project** プロジェクトから Playbook `rhel/apache/webcontent.yml` を使用
  * 2 つの変数 `dev_content: default dev content` と `prod_content: default prod
    content` を **EXTRA VARIABLES FIELD** に定義します。
  * `Workshop Credentials` を使用して、特権昇格で実行します。

* テンプレートを保存して実行します。

### 結果を確認します。

今回は、Ansible の機能で、結果の確認を行います。curl を実行して、各ノードから Web コンテンツを取得しすると、Tower
コントロールホストのコマンドラインで、アドホックコマンドで調整されます。

> **ヒント**
>
> インベントリーグループの各ノードにアクセスするために、URL に `ansible_host` 変数を使用しています。 

<!-- {% raw %} -->

```bash
[student<X>@ansible-1 ~]$ ansible web -m command -a "curl -s http://{{ ansible_host }}"
 [WARNING]: Consider using the get_url or uri module rather than running 'curl'.  If you need to use command because get_url or uri is insufficient you can add 'warn: false' to this command task or set 'command_warnings=False' in ansible.cfg to get rid of this message.

node2 | CHANGED | rc=0 >>
<body>
<h1>This is a production webserver, take care!</h1>
prod wweb
</body>

node1 | CHANGED | rc=0 >>
<body>
<h1>This is a development webserver, have fun!</h1>
dev wweb
</body>

node3 | CHANGED | rc=0 >>
<body>
<h1>This is a development webserver, have fun!</h1>
dev wweb
</body>
```

<!-- {% endraw %} -->

`command` モジュールから `curl` を使用しないことについての最初の行の警告に注目してください。Ansible
には、より優れたモジュールがあるため、これについては次のパートで説明します。

### Survey の追加

* Template に survey を追加して、変数 `dev_content` と `prod_content` を変更できるようにします。
* Team `Web Content` にパーミッションを追加すると、Template **Create Web Content** が `wweb`
  で実行できます。
* ユーザー `wweb` として survey を実行します。

Tower コントロールホストから再び結果を確認します。前回は、`command` モジュールから `curl`
を使用して警告を受けたため、今回は専用の `uri` モジュールを使用します。これは引数として実際の URL
とフラグを使用し、今回は結果の本文を出力します。

<!-- {% raw %} -->

```bash
[student<X>@ansible-1 ~]$ ansible web -m uri -a "url=http://{{ ansible_host }}/ return_content=yes"
node3 | SUCCESS => {
    "accept_ranges": "bytes",
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "connection": "close",
    "content": "<body>\n<h1>This is a development webserver, have fun!</h1>\nwerners dev content\n</body>\n",
    "content_length": "87",
    "content_type": "text/html; charset=UTF-8",
    "cookies": {},
    "cookies_string": "",
    "date": "Tue, 29 Oct 2019 11:14:24 GMT",
    "elapsed": 0,
    "etag": "\"57-5960ab74fc401\"",
    "last_modified": "Tue, 29 Oct 2019 11:14:12 GMT",
    "msg": "OK (87 bytes)",
    "redirected": false,
    "server": "Apache/2.4.6 (Red Hat Enterprise Linux)",
    "status": 200,
    "url": "http://18.205.236.208"
}
[...]
```

<!-- {% endraw %} -->

### ソリューション

> **警告**
>
> **以下に回答を示します。**

このラボでは、必要なすべての設定手順を実行しました。不明な点があれば、関連の章に戻って確認してください。

## 終わり

おめでとうございます。ラボを完了しました。我々がラボの構築を楽しめたように、Ansible Tower を楽しんでいただければ光栄です。

----
**ナビゲーション**
<br>
[前の演習](../2.6-workflows)

[クリックして Ansible for Red Hat Enterprise Linux Workshop
に戻ります](../README.md#section-2---ansible-tower-exercises)
