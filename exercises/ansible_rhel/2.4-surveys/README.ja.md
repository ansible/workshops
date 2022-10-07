# 演習 - Survey

**他の言語でもお読みいただけます**:
<br>![uk](../../../images/uk.png) [English](README.md)、![japan](../../../images/japan.png)[日本語](README.ja.md)、![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md)、![france](../../../images/fr.png) [Française](README.fr.md)、![Español](../../../images/col.png) [Español](README.es.md)

## 目次

* [目的](#目的)
* [ガイド](#ガイド)
* [Apache-configuration ロール](#apache-configuration-ロール)
* [Survey を持つテンプレートの作成](#survey-を持つテンプレートの作成)
  * [テンプレートの作成](#テンプレートの作成)
  * [Survey の追加](#survey-の追加)
* [テンプレートの起動](#テンプレートの起動)

## 目的

Ansible 自動コントローラー [survey 機能](https://docs.ansible.com/automation-controller/latest/html/userguide/job_templates.html#surveys) の使用のデモンストレーションを行います。Survey は、「Prompt for Extra Variables (追加変数のプロンプト)」と同様に Playbook の追加変数を設定しますが、ユーザーが使いやすい質問と回答を使ってこれを実行します。また、Survey ではユーザー入力を検証することもできます。

## ガイド

実行したジョブのすべてのホストに Apache をインストールしました。次に、これに拡張を行っていきます。

* jinja2 テンプレートを持つ適切なロールを使用して、`index.html`ファイルをデプロイします。

* survey でジョブ **Template** を作成し、`index.html` テンプレートの値を収集します。

* ジョブ **Template** を起動します。

さらに、この演習のために Apache の設定が適切に設定されていることを確認する役割もあります。

> **ヒント**
>
> この survey 機能では、データにシンプルな query を提供します。4 つの目の原則、動的データに基づいたクエリー、ネストメニューには対応していません。

### Apache-configuration ロール

Jinja2 テンプレートの Playbook とロールが、ディレクトリー `rhel/apache` の Github リポジトリー [https://github.com/ansible/workshop-examples](https://github.com/ansible/workshop-examples) に既に存在します。

 Github UI にアクセスして、コンテンツを確認します。Playbook `apache_role_install.yml` は単にロールを参照します。ロールは、`roles/role_apache` サブディレクトリーにあります。

* ロール内で、`{{…​}}` でマークされている `templates/index.html.j2` テンプレートファイルの 2 つの変数をメモします。
* また、テンプレートからファイルをデプロイする、`tasks/main.yml` のタスクを確認します。

この Playbook はどのような操作を行うのでしょうか。テンプレート (**src**) の管理対象ホストでファイル (**dest**) を作成します。

このロールは、Apache の静的構成も展開します。これにより、前の章で行ったすべての変更が上書きされ、例が正しく動作するようになります。

Playbook とロールは、`apache_install.yml` Playbook と同じ Github レポジシトリーにあるため、この演習用に新しいプロジェクトを構成する必要はありません。

### Survey を持つテンプレートの作成

次は、survey を含む新しいテンプレートを作成します。

#### テンプレートの作成

* **Resources → Templates** に移動し、**Add** ボタンをクリックして、**Add job template** を選択します。

* 次の情報を入力します。

<table>
  <tr>
    <th>パラメーター</th>
    <th>値</th>
  </tr>
  <tr>
    <td>Name</td>
    <td>Create index.html</td>
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
    <td>Eecution Environment</td>
    <td>Default execution environment</td>
  </tr>
  <tr>
    <td>Playbook</td>
    <td><code>rhel/apache/apache_role_install.yml</code></td>
  </tr>
  <tr>
    <td>Credentials</td>
    <td>Workshop Credential</td>
  </tr>
  <tr>
    <td>Limit</td>
    <td>web</td>
  </tr>
  <tr>
    <td>Options</td>
    <td>Privilege Escalation</td>
  </tr>
</table>

* **Save** をクリックします。

> **警告**
>
> **まだテンプレートは実行しないでください。**

#### Survey の追加

* テンプレートで **Survey** タブをクリックして、**Add** ボタンをクリックします。

* 次の情報を入力します。

<table>
  <tr>
    <th>パラメーター</th>
    <th>値</th>
  </tr>
  <tr>
    <td>Question</td>
    <td>First Line</td>
  </tr>
  <tr>
    <td>Answer Variable Name</td>
    <td>first_line</td>
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
    <td>Second Line</td>
  </tr>
  <tr>
    <td>Answer Variable Name</td>
    <td>second_line</td>
  </tr>
  <tr>
    <td>Answer Type</td>
    <td>Text</td>
  </tr>
</table>

* **Save** をクリックします。

* トグルをクリックして、質問を **Survey Enabled** に切り替えます

### テンプレートの起動

**Details** タブを選択し、**Launch** ボタンをクリックしてジョブテンプレートの作成 **Create index.html** を起動します。

実際に起動する前に、Survey により、**First Line** と **Second Line** が求められます。テキストを入力して、**Preview** をクリックします。次のウィンドウに値が表示されます。問題がなければ、**Launch** をクリックしてジョブを実行します。

ジョブが完了したら、Apache ホームページを確認します。コントロールホストの SSH コンソールで、`node1` の以下に対して `curl` を実行します。

```bash
$ curl http://node1
<body>
<h1>Apache is running fine</h1>
<h1>This is survey field "First Line": line one</h1>
<h1>This is survey field "Second Line": line two</h1>
</body>
```

Playbook によって使用されている 2 つの変数が `index.html` ファイルの内容を作成するかに注意してください。

---
**ナビゲーション**
<br>

{% if page.url contains 'ansible_rhel_90' %}
[Previous Exercise](../4-variables) - [Next Exercise](../../ansible_rhel_90/6-system-roles/)
{% else %}
[Previous Exercise](../2.3-projects) - [Next Exercise](../2.5-rbac)
{% endif %}
<br><br>
[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md)
