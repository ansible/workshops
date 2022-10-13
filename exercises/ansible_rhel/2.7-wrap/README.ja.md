# ワークショップ演習 - まとめ

**他の言語でもお読みいただけます**:
<br>![uk](../../../images/uk.png) [English](README.md)、![japan](../../../images/japan.png)[日本語](README.ja.md)、![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md)、![france](../../../images/fr.png) [Française](README.fr.md)、![Español](../../../images/col.png) [Español](README.es.md)

## 目次

* [目的](#目的)
* [ガイド](#ガイド)
  * [ステージの設定](#ステージの設定)
  * [Git リポジトリー](#git-リポジトリー)
  * [インベントリーの準備](#インベントリーの準備)
  * [テンプレートの作成](#テンプレートの作成)
  * [結果の確認](#結果の確認)
  * [Survey の追加](#survey-の追加)
  * [ソリューション](#ソリューション)
* [終わり](#終わり)

## 目的

これは、これまで学んだことの復習を目的とした最後のチャレンジです。

## ガイド

### ステージの設定

運営チームとアプリケーション開発チームは、Ansible 自動コントローラーの機能を気に入っています。実際の環境で使用するために、要件を次にまとめました。

* すべてのウェブサーバー (`node1`、`node2`、`node3`) を 1 つのグループに入れる必要があります

* Web サーバーは開発目的または本番環境で使用できるため、それに応じて「stage dev」または「stage prod」としてフラグを立てる方法が必要です。

  * 現在、`node1` と `node3` が開発システムとして使用され、`node2` が稼働環境となっています。

* もちろん、世界的に有名なアプリケーション「index.html」の内容は、開発段階と製品段階で異なります。

  * 環境を示した、ページにタイトルが表示されます。
  * コンテンツフィールドがあります。

* コンテンツライター `wweb` には、dev サーバーと prod サーバーのコンテンツを変更するための調査にアクセスできる必要があります。

### Git リポジトリー

すべてのコードはすでに配置されています。これは自動コントローラーラボですから。[https://github.com/ansible/workshop-examples](https://github.com/ansible/workshop-examples) にある **Workshop Project** git リポジトリを確認してください。そこに Playbook `webcontent.yml` があります。これは、ロール `role_webcontent` を呼び出します。

以前の Apache インストールのロールと比較すると、大きな違いがあります。現在、2つのバージョンの `index.html` テンプレート、およびソースファイル名の一部として変数を持つテンプレートファイルをデプロイするタスクがあります。

`dev_index.html.j2`

<!-- {% raw %} -->

```html
<body>
<h1>This is a development webserver, have fun!</h1>
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

これを実行する方法は 1 つありますが、このラボでは Ansible 自動化コントローラーを使用します。

**Resources** -> **Inventories** 内で、「Workshop Inventory」を選択します。

**Groups** タブで、**Add** ボタンをクリックして、`Webserver` というラベルが付けられた新規インベントリーグループを作成し、**Save** をクリックします。

`Webserver` グループの **Details** タブで、**Edit** をクリックします。**Variables** テキストボックスでは、`stage` という値を持つ変数 `dev` を定義し、**Save** をクリックします。

```yaml
---
stage: dev
```

`Webserver` インベントリーの **Details** タブで、**ホスト** タブをクリックし、**Add** および **Add existing host** ボタンをクリックします。`Webserver` インベントリーに含まれるホストとして、`node1`、`node2`、および `node3` を選択します。


**Resources** -> **Inventories** 内で、`Workshop` インベントリーを選択します。また、`Hosts` タブをクリックして、`node2` をクリックします。`Edit` をクリックし、**Variables** ウィンドウで `stage: prod` 変数を追加します。これは、Playbook の実行時に変数にアクセスする方法により、インベントリー変数を上書きします。


**Variables** テキストボックスで、`stage` という値を持つ `prod` というラベルが付いた変数を定義し、**Save** をクリックします。

```yaml
---
ansible_host: <IP_of_node2>
stage: prod
```
> **ヒント**
>
> YAML の開始をマークする 3 つのダッシュと `ansible_host` の行を所定の位置に配置するようにしてください。

### テンプレートの作成

**Resources** -> **Templates** 内で、**Add** ボタンと **Add job template* を以下のように選択します。

  <table>
    <tr>
      <th>パラメーター</th>
      <th>値</th>
    </tr>
    <tr>
      <td>Name</td>
      <td>Create Web Content</td>
    </tr>
    <tr>
      <td>Job Type</td>
      <td>Run</td>
    </tr>
    <tr>
      <td>Inventory</td>
      <td>Workshop Inventory</td>
    </tr>
    <tr>
      <td>Project</td>
      <td>Workshop Project</td>
    </tr>
    <tr>
      <td>Execution Environment</td>
      <td>Default execution environment</td>
    </tr>
    <tr>
      <td>Playbook</td>
      <td>rhel/apache/webcontent.yml</td>
    </tr>
    <tr>
      <td>Credentials</td>
      <td>Workshop Credential</td>
    </tr>
    <tr>
      <td>Variables</td>
      <td>dev_content: "default dev content", prod_content: "default prod content"</td>
    </tr>
    <tr>
      <td>Options</td>
      <td>Privilege Escalation</td>
    </tr>
  </table>

**保存** をクリックします。

**Launch** ボタンをクリックしてテンプレートを実行します。


### 結果の確認

今回は、Ansible パワーを使って結果を確認します。各ノードから Web コンテンツを取得するために uri を実行し、Ansible Playbook (`check_url.yml`) によってオーケストレーションされます。

> **ヒント**
>
> インベントリーグループの各ノードにアクセスするために、URL に `ansible_host` 変数を使用しています。

<!-- {% raw %} -->

```yaml
---
- name: Check URL results
  hosts: web

  tasks:
    - name: Check that you can connect (GET) to a page and it returns a status 200
      uri:
        url: "http://{{ ansible_host }}"
        return_content: yes
      register: content

    - debug:
       var: content.content
```

```bash
[student@ansible-1 ~]$ ansible-navigator run check_url.yml -m stdout
```

出力のスニペット:

```bash
TASK [debug] *******************************************************************
ok: [node1] => {
    "content.content": "<body>\n<h1>This is a development webserver, have fun!</h1>\ndev wweb</body>\n"
}
ok: [node2] => {
    "content.content": "<body>\n<h1>This is a production webserver, take care!</h1>\nprod wweb</body>\n"
}
ok: [node3] => {
    "content.content": "<body>\n<h1>This is a development webserver, have fun!</h1>\ndev wweb</body>\n"
}
```

<!-- {% endraw %} -->

### Survey の追加

* Survey をテンプレートに追加して、変数 `dev_content` および `prod_content` の変更を可能にします。
** テンプレートでは、**Survey** タブをクリックして、**Add** ボタンをクリックします。
** 以下の情報を確認してください。

<table>
  <tr>
    <th>パラメーター</th>
    <th>値</th>
  </tr>
  <tr>
    <td>Question</td>
    <td>What should the value of dev_content be?</td>
  </tr>
  <tr>
    <td>Answer Variable Name</td>
    <td>dev_content</td>
  </tr>
  <tr>
    <td>Answer Type</td>
    <td>Text</td>
  </tr>
</table>

* **Save** をクリックします。
* **追加** ボタンをクリックします。

同じ方法で、2 番目の **Survey Question** を追加します。

<table>
  <tr>
    <th>パラメーター</th>
    <th>値</th>
  </tr>
  <tr>
    <td>Question</td>
    <td>What should the value of prod_content be?</td>
  </tr>
  <tr>
    <td>Answer Variable Name</td>
    <td>prod_content</td>
  </tr>
  <tr>
    <td>Answer Type</td>
    <td>Text</td>
  </tr>
</table>

* **Save** をクリックします。
* トグルをクリックして Survey の質問を **On** に切り替えます。

* Survey の **Preview** をクリックします。

* Team `Web Content` にパーミッションを追加すると、Template **Create Web Content** が `wweb` で実行できます。
* **Resources** -> **Templates** 内で、*Create Web Content** をクリックし、ユーザー `wweb` に **Access** を追加し、テンプレートを実行します。
  * **Select a Resource Type** -> **Users**をクリックし、**Next** をクリックします。
  * **Select Items from List** -> `wweb` チェックボックスを選択して、**Next** をクリックします。
  * **Select Roles to Apply** -> **Excute** チェックボックスを選択して、**Save** をクリックします。
* ユーザー `wweb` として survey を実行します。
  * Ansible 自動コントローラーのユーザー `admin` からログアウトします。
  * `wweb` としてログインし、**Resources** -> **Templates** に移動して、**Create Web Content** テンプレートを実行します。

オートメーションコントローラーのホストから再度結果を確認します。ここでは、専用の`uri` モジュールを Ansible Playbook 内で使用します。引数として、実際の URL と、結果に本文を出力するためのフラグが必要です。

<!-- {% raw %} -->


```bash
[student@ansible-1 ~]$ ansible-navigator run check_url.yml -m stdout
```

<!-- {% endraw %} -->

### ソリューション

> **警告**
>
> **以下に回答を示します。**

このラボでは、必要なすべての設定手順を実行しました。不明な点があれば、関連の章に戻って確認してください。

## 終わり

おめでとうございます。ラボを完了しました。我々がラボの構築を楽しめたように、Ansible 自動コントローラーを楽しんでいただければ光栄です。

----
**ナビゲーション**
<br>
[前の演習](../2.6-workflows)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-2---ansible-automation-controller-exercises)
