# 演習 - アンケート

**その他の言語はこちらをお読みください。**
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

## 目次

* [目的](#objective)
* [ガイド](#guide)
* [Apache-configuration ロール](#the-apache-configuration-role)
* [Survey によるテンプレートの作成](#create-a-template-with-a-survey)
  * [テンプレートの作成](#create-template)
  * [Aurvey の追加](#add-the-survey)
* [テンプレートの起動](#launch-the-template)
* [練習してみましょう](#what-about-some-practice)

## 目的

Ansible Tower Survey [survey
機能](https://docs.ansible.com/ansible-tower/latest/html/userguide/job_templates.html#surveys)
の使用のデモンストレーションを行います。Survey は、「Prompt for Extra Variables (追加変数のプロンプト)」と同様に
Playbook の追加変数を設定しますが、ユーザーが使いやすい質問と回答を使ってこれを実行します。また、Survey
ではユーザー入力を検証することもできます。

## ガイド

実行したジョブのすべてのホストに Apache をインストールしました。次に、これに拡張を行っていきます。

* jinja2 テンプレートを持つ適切なロールを使用して、`index.html`ファイルをデプロイします。

* survey でジョブ **Template** を作成し、`index.html` テンプレートの値を収集します。

* ジョブ **Template** を起動します。

さらに、このロールは、他の演習中に混ざった場合を考慮して、Apache 構成が適切に設定されていることも確認します。

> **ヒント**
>
> この survey 機能では、データにシンプルな query を提供します。4 つの目の原則、動的データに基づいたクエリー、ネストメニューには対応していません。

### Apache-configuration ロール

Jinja テンプレートの Playbook とロールが、ディレクトリー `rhel/apache` の Github
レポジトリーに既に存在します。[https://github.com/ansible/workshop-examples](https://github.com/ansible/workshop-exampleshttps://github.com/ansible/workshop-examples)

Github UI にアクセスして、コンテンツを確認します。Playbook `apache_role_install.yml` は単にロールを参照します。ロールは、`roles/role_apache` サブディレクトリーにあります。

* ロール内で、`{{…​}}` でマークされている `templates/index.html.j2` テンプレートファイルの 2
  つの変数をメモします。
* また、テンプレートからファイルをデプロイする、`tasks/main.yml` のタスクを確認します。

この Playbook はどのような操作を行うのでしょうか。テンプレート (**src**) の管理対象ホストでファイル (**dest**)
を作成します。

このロールは、Apache の静的構成も展開します。これにより、前の章で行ったすべての変更が上書きされ、例が正しく動作するようになります。

Playbook とロールは、`apache_install.yml` Playbook と同じ Github
レポジシトリーにあるため、この演習用に新しいプロジェクトを構成する必要はありません。

### Survey を持つテンプレートの作成

次は、survey を含む新しいテンプレートを作成します。

#### テンプレートの作成

* **Templates** に移動し、![plus](images/green_plus.png) ボタンをクリックして、**Job
  Template** を選択します。

* 次の情報を入力します。

<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>NAME</td>
    <td>Create index.html</td>
  </tr>
  <tr>
    <td>JOB TYPE</td>
    <td>Run</td>
  </tr>
  <tr>
    <td>INVENTORY</td>
    <td>Workshop Inventory</td>
  </tr>
  <tr>
    <td>Project</td>
    <td>Workshop Project</td>
  </tr>
  <tr>
    <td>PLAYBOOK</td>
    <td><code>rhel/apache/apache_role_install.yml</code></td>
  </tr>
  <tr>
    <td>CREDENTIAL</td>
    <td>Workshop Credentials</td>
  </tr>
  <tr>
    <td>LIMIT</td>
    <td>web</td>
  </tr>
  <tr>
    <td>OPTIONS</td>
    <td>Enable Privilege Escalation</td>
  </tr>
</table>

* **SAVE** をクリックします。

> **警告**
>
> **まだテンプレートは実行しないでください。**

#### Survey の追加

* Template で、**ADD SURVEY** ボタンをクリックします。

* **ADD SURVEY PROMPT**の下に、次のように入力します。

<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>PROMPT</td>
    <td>First Line</td>
  </tr>
  <tr>
    <td>ANSWER VARIABLE NAME</td>
    <td><code>first_line</code></td>
  </tr>
  <tr>
    <td>ANSWER TYPE</td>
    <td>Text</td>
  </tr>
</table>

* **+ADD** をクリックしてください。

* 同様に、2 番目の **Survey Prompt** を追加します。

<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>PROMPT</td>
    <td>Second Line</td>
  </tr>
  <tr>
    <td>ANSWER VARIABLE NAME</td>
    <td><code>second_line</code></td>
  </tr>
  <tr>
    <td>ANSWER TYPE</td>
    <td>Text</td>
  </tr>
</table>

* **+ADD** をクリックしてください。

* Survey の **SAVE** をクリックします。

* Template の **SAVE** をクリックします。

### テンプレートの起動

次に、**Create index.html** ジョブテンプレートを起動します。

実際に起動する前に、Survey により、**First Line** と **Second Line**
が求められます。テキストを入力して、**Next** をクリックします。次のウィンドウに値が表示されます。問題がなければ、**Launch**
をクリックしてジョブを実行します。

> **ヒント**
>
> 2 つの survey 行が **Extra Variables** としてジョブの左にどのように表示されているかに注意してください。

ジョブが完了したら、Apache ホームページを確認します。コントロールホストの SSH コンソールで、`node1` の IP アドレスに対して
`curl` を実行します。

```bash
$ curl http://22.33.44.55
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
[前の演習](../1.4-variables) - [次の演習](../../ansible_rhel_90/6-system-roles/)
{% else %}
[前の演習](../2.3-projects) - [次の演習](../2.5-rbac)
{% endif %}
<br><br>
[こちらをクリックして、Ansible for Red Hat Enterprise Linux Workshop に戻ります](../README.md)
