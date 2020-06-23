# 演習 - Survey 機能

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

* [目的](#目的)
* [ガイド](#ガイド)
* [Apache-configuration Role](#apache-configuration-role)
* [プロジェクトを作成する](#プロジェクトを作成する)
* [Survey 付きのテンプレートを作成](#survey-付きのテンプレートを作成)
   * [テンプレートの作成](#テンプレートの作成)
   * [Survey を追加する](#survey-を追加する)
* [テンプレートを起動します](#テンプレートを起動します)
* [さらに次のタスクを実行ください](#さらに次のタスクを実行ください)

# 目的

Ansible Towerの [Survey機能](https://docs.ansible.com/ansible-tower/latest/html/userguide/job_templates.html#surveys) の使用方法をデモします。Surveyは、「Prompt for Extra Variables」と同様にPlaybookに追加変数を設定しますが、ユーザーフレンドリーな質問と回答の方法で行います。Surveyでは、ユーザーの入力を検証することもできます。

# ガイド

先ほど実行したジョブでは、すべてのホストにApacheをインストールしました。これを拡張してみましょう。

- Jinja2テンプレートを持つ適切なroleを使って `index.html` ファイルをデプロイします。

- index.html` テンプレートの値を収集するためのSurveyを持つ ジョブ **テンプレート**を作成します。

- ジョブ **テンプレート** を起動します。

> **ヒント**
>
> Survey機能では、データに対する簡単なクエリのみを提供していますが、4つの目の原則、つまり動的データや入れ子になったメニューに基づくクエリはサポートしていません。

## Apache-configuration Role

Playbook と Jinja2 テンプレートを持つ Roles は Github リポジトリ **https://github.com/ansible/workshop-examples** の `rhel/apache` にあります。  

Github UIに移動して、 `apache_role_install.yml` の中身を見てみてください。単に Role を参照しているだけです。 Role は `roles/role_apache` サブディレクトリに存在します。

 - Role 内の jinja2 テンプレート `templates/index.html.j2` 内に定義された二つの変数を確認します。変数は `{{…?}}` で定義されるんでしたね。
 - また、メインのタスクを担う、 `tasks/main.yml` の中で、template からファイルをコピーするタスクをチェックします。

この Playbook は何をやっているのでしょうか？これはテンプレート (**src**) から、対象ホスト上にファイル (**dest**) としてコピーしています。

この Role は、Apache の静的な設定もデプロイします。前の章で行われた全ての変更が上書きされ、今回の演習が問題なく実行できることを保証するためのものです。

この Playbook と Role は `apache_install.yml` と同じ Github リポジトリに配置されているため、この演習用に新しいプロジェクトを作成する必要はありません。

## Survey 付きのテンプレートを作成

ここでは Survey を含む新しいジョブテンプレートを作成します。

### テンプレートの作成

- 左のメニューで**テンプレート**を選択し、![plus](images/green_plus.png) ボタンをクリック。 **ジョブテンプレート**を選択します。  

- 以下の情報を入力します:


<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>名前</td>
    <td>Create index.html</td>
  </tr>
  <tr>
    <td>ジョブタイプ</td>
    <td>Run</td>
  </tr>
  <tr>
    <td>インベントリー</td>
    <td>Workshop Inventory</td>
  </tr>
  <tr>
    <td>プロジェクト</td>
    <td>Workshop Project</td>
  </tr>  
  <tr>
    <td>PLAYBOOK</td>
    <td><code>rhel/apache/apache_role_install.yml</code></td>
  </tr>
  <tr>
    <td>認証情報</td>
    <td>Workshop Credentials</td>
  </tr>
  <tr>
    <td>制限</td>
    <td>web</td>
  </tr>  
  <tr>
    <td>オプション</td>
    <td>権限昇格の有効化</td>
  </tr>          
</table>

> **注意**  
>
> **まだジョブテンプレートを実行しないでください！**  

### Survey を追加する

- ジョブテンプレートの中で、**SURVEY の追加** ボタンをクリックします  

- **Survey プロンプトの追加** フォームで以下を入力します  

    <table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>プロンプト</td>
    <td>First Line</td>
  </tr>
  <tr>
    <td>回答の変数名</td>
    <td><code>first_line</code></td>
  </tr>
  <tr>
    <td>回答タイプ</td>
    <td>テキスト</td>
  </tr>         
</table>

- **+ADD**をクリックします。

- 同じように2つ目の変数入力フォームを定義します

<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>プロンプト</td>
    <td>Second Line</td>
  </tr>
  <tr>
    <td>回答の変数名</td>
    <td><code>second_line</code></td>
  </tr>
  <tr>
    <td>回答タイプ</td>
    <td>テキスト</td>
  </tr>         
</table>

- **+ADD**をクリックします

- **保存** をクリックし、 Survey を保存します

- **保存** をクリックし、ジョブテンプレートを保存します

## テンプレートを起動します

作成したジョブテンプレート **Create index.html** を起動してみます。  

実際の起動の際に、Survey は **First Line** と **Second Line** の2つについて入力を要求します。お好きなテキストを入力して、「次へ」をクリックします。次のウィンドウに入力した値が表示されます。問題なければ、「起動」をクリックしてジョブを実行します。

> **ヒント**
>
> 入力した 2つの値がジョブ実行画面の左下の **追加変数**に表示されていることを確認します。  

ジョブが完了したら、Apache ホームページを確認してください。確認するのは、そう、`node1` です。 Tower Server の SSH コンソールの curl コマンドで確認したもよいですし、ブラウザで直接 node1 に接続してみてもOKです。  

```bash
$ curl http://<node1>
<body>
<h1>Apache is running fine</h1>
<h1>This is survey field "First Line": line one</h1>
<h1>This is survey field "Second Line": line two</h1>
</body>
```
この index.html ファイルが Playbook と Survey によってどのように作成されたのか、よく理解しておいて下さい。

----

[Ansible Tower ワークショップ表紙に戻る](../README.ja.md#section-2---ansible-towerの演習)
