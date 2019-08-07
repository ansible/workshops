# 演習 2.4 - Survey

テンプレート構成ビューの**SURVEYの追加**ボタンに気付いたかもしれません。Survey は、**テンプレート**が**ジョブ**として起動されたときに変数として使用されるパラメーターへの値の入力を要求する簡単なフォームです。  

先ほどの演習で、全てのホストに Apache をインストールしました。次にこれを拡張します  

- Jinja2テンプレートを持つ適切なロールを使用して、`index.html` ファイルをデプロイします  

- Survey を含むジョブテンプレートを作成し、 `index.html` テンプレート用の情報を収集します  

- ジョブテンプレートを起動します  

さらに、このロールでは、他の演習で失敗していることも想定し、Apache 構成が適切にセットアップされていることも確認します。  

> **ヒント**  
> 
> Survey は入力するデータの単純なクエリのみを提供します。動的なデータに基づくクエリやネストされたメニューには対応していません。  

## プロジェクトを作成する  

Playbook と Jinja2 テンプレートを持つ Roles は Github リポジトリ **https://github.com/ansible/workshop-examples** の `rhel/apache` にあります。 Github UIに移動して、 `apache_role_install.yml` の中身を見てみてください。単に Role を参照しているだけです。 Role は `roles/role_apache` サブディレクトリに存在します。ロール内の jinja2 テンプレート `templates/index.html.j2` 内に定義された二つの変数を確認します。変数は `{{…​}}`\で定義されるんでしたね。また、メインのタスクを担う、 `tasks/main.yml` の中で、template からファイルをコピーするタスクをチェックします。この Playbook は何をやっているのでしょう、分かりますか？  テンプレート (**src**) から、対象ホスト上にファイル (**dest**) としてコピーしています。この際、コピー先のファイルには変数に値が入力されます。値を入力するのは、そう、 Survey インターフェースです。  

ロールは、Apache のコンフィグレーションもデプロイします。前の章で行われたすべての変更が上書きされ、今回のサンプルが適切に機能することを保証するためのものです。  

## Survey を作成  

Survey を含むジョブテンプレートを作成します。  

### テンプレートの作成  

- 左のメニューで**テンプレート**を選択し、![plus](images/green_plus.png) ボタンをクリック。 **ジョブテンプレート**を選択します。  

- **名前** Create index.html

- テンプレートを次のように構成してください！
  
    - 既存の**プロジェクト** の中から今回の件に適応するものを選択。さらに適切な **Playbook**を選びます。
  
    - `node1` のみで実行されるようにインベントリーを定義します
  
    - 権限昇格を行います

やり方はわかりますか？答えは以下の通りです。そんなに難しくないですね？♬

> **回答**

- **名前** Create index.html

- **ジョブタイプ:** Run

- **インベントリー** Webserver

- **プロジェクト** Ansible Workshop Examples

- **PLAYBOOK** `rhel/apache/apache_role_install.yml`

- **認証情報** Workshop Credentials

- **オプション** Enable Privilege Escalation

- **保存**をクリック

> **Warning**
>
> **Do not run the template yet!**

### Add the Survey

- In the Template, click the **ADD SURVEY** button

- Under **ADD SURVEY PROMPT** fill in:
  
    - **PROMPT:** First Line
  
    - **ANSWER VARIABLE NAME:** `first_line`
  
    - **ANSWER TYPE:** Text

- Click **+ADD**

- In the same way add a second **Survey Prompt**
  
    - **PROMPT:** Second Line
  
    - **ANSWER VARIABLE NAME:** `second_line`
  
    - **ANSWER TYPE:** Text

- Click **+ADD**

- Click **SAVE** for the Survey

- Click **SAVE** for the Template

## Launch the Template

Now launch **Create index.html** job template.

Before the actual launch the survey will ask for **First Line** and **Second Line**. Fill in some text and click **Next**. The next window shows the values, if all is good run the Job by clicking **Launch**.

> **Tip**
> 
> Note how the two survey lines are shown to the left of the Job view as **Extra Variables**.

After the job has completed, check the Apache homepage. In the SSH console on the control host, execute `curl` against the IP address of your `node1`:

```bash
$ curl http://22.33.44.55
<body>
<h1>Apache is running fine</h1>
<h1>This is survey field "First Line": line one</h1>
<h1>This is survey field "Second Line": line two</h1>
</body>
```
Note how the two variables where used by the playbook to create the content of the `index.html` file.

## What About Some Practice?

Here is a list of tasks:

> **Warning**
> 
> **Please make sure to finish these steps as the next chapter depends on it\!**

- Take the inventory `Webserver` and add the other nodes, `node2` and `node3` as well.

- Run the **Create index.html** Template again.

- Verify the results on the other two nodes by using `curl` against their IP addresses.

----

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-2---ansible-tower-exercises)

