# Exercise 2 - Ansible Towerのコンフィグレーション

この演習を実施することにより、Ansible Towerを用いてPlaybookが実行できるようになります。
* ブラウザで利用している言語により、この演習内のナビゲート情報は変更になります。適宜読み替えをお願い致します。

## Ansible Towerのコンフィグレーション

Anabilities Towerは、RestAPIでの実行、マルチテナント、通知、スケジューリングなどを可能にしますが、今回のワークショップでは以下へリストする、最低限必要な主要コンセプトに焦点を絞って説明します。

* `Credentials` 対象ノードへの認証情報を設定します。
* `Projects` Playbook一覧を登録します。
* `Inventory` 対象ノードの一覧を登録します。
* `Job Template` Credential, Playbook(Project), Inventory 情報を組み合わせて実行できるジョブを作成します。

## Ansible Towerへのログインとライセンスキーのインストール

### Step 1:

以下の認証情報を用いてAnsible Towerへログインします。

Username:`admin`

password:`ansibleWS`(もしくは1-install Step 6でインベントリーファイルへ記入したパスワード)

![Ansible Tower Login Screen](ansible-lab-figure01-logon-screen.png)

ログインが完了すると、ライセンスのリクエストか、ライセンスファイルの投入を求められるページが表示されます。


![Uploading a License](at_lic_prompt.png)

### Step 2:

次のURL [https://www.ansible.com/workshop-license](https://www.ansible.com/workshop-license) で workshop専用のlicenseをリクエストしてください。
通常はすぐ(1~2分)にメールでライセンスファイルが送られるはずです。
メールに添付されているライセンスファイルを用いて、AnsibleTowerのライセンスを有効化します。

Note: 講師がワークショップ用のライセンスを準備している場合にはそちらを利用してください。

### Step 3:

Ansible TowerのUIへ戻り、 BROWSEボタンをクリックします。 ![Browse button](at_browse.png) 
送付されてきたライセンスファイルをAnsibleTowerへアップロードしてください。

### Step 4:

使用許諾の確認へチェックを入れます。 "_I agree to the End User License Agreement_"

### Step 5:

SUBMITボタンをクリックし、完了です。![Submit button](at_submit.png)

## Credential(認証情報)の作成

Credentials(認証情報)は、Ansible Towerがジョブなどを実行する際に利用されます。サーバに対するジョブやインベントリー情報の同期、SCMとのプロジェクト同期を実行する際などに利用されます。

[認証情報のタイプ](http://docs.ansible.com/ansible-tower/latest/html/userguide/credentials.html#credential-types) は様々です。
 サーバ(Machine)や、Network、AWSなどのクラウドなどがありますが、このワークショップでは *Machine* の認証情報(クレデンシャル)を利用します。

### Step 1:

画面左の一覧からCREDENTIALS (認証情報) をクリックします。

### Step 2:

+ADD(+追加)をクリックします。 ![Add button](at_add.png)

### Step 3:

以下の表の通りに入力し、ワークショップの中で利用する認証情報をコンフィグします。

項目 | 値
-----|---------------------------
NAME (名前) |Ansible Workshop Credential
DESCRIPTION (説明)|Machine credential for run job templates during workshop
ORGANIZATION (組織)|Default
CREDENTIAL TYPE(認証情報タイプ)|Machine
USERNAME (ユーザー名)| studentXX(配布されたユーザ情報)
PASSWORD| ansible(配布されたパスワード)
PRIVILEGE ESCALATION METHOD(権限昇格方法)|Sudo


![Adding a Credential](at_cred_detail.png)

### Step 4:

SAVE(保存)をクリックします。 ![Save button](at_save.png)

## Projectの作成

Projectは、Ansible Tower内のPlaybookの論理的なコレクションです。
Projectを作成することで、あなたはPlaybookをTower Server内のProjectに基づいたPathへ直接配置したり、Git、Subversion、Mercurialなどに代表されるソースコードマネジメントシステム(SCM)を利用して配置するといった、Playbookの管理を行うことができます。

### Step 1:

PROJECTS(プロジェクト)をクリックします。

### Step 2:

+ADD (+追加)をクリックします。 ![Add button](at_add.png)

### Step 3:

以下の値を利用して新規プロジェクトを作成します。

項目 | 値
-----|------------------------
NAME(名前) |Ansible Workshop Project
DESCRIPTION(説明)|workshop playbooks
ORGANIZATION(組織)|Default
SCM TYPE(SCMタイプ)|Git
SCM URL| https://github.com/ansible/lightbulb
SCM BRANCH| 
SCM UPDATE OPTIONS(SCM更新オプション)

- [x] Clean(クリーニング) 
- [x] Delete on Update(更新時の削除)
- [x] Update on Launch(起動時の更新)

![Defining a Project](at_project_detail.png)

### Step 4:

SAVEをクリックします。 ![Save button](at_save.png)

## Inventory(インベントリ) の作成

インベントリとは、Jobが実行可能なホストのコレクションです。
インベントリはグループごとに分離され、グループ内にJobが実行されるホストが含まれることになります。
グループはAnsible Towerでホスト名を手動で入力したり、Ansible Towerがサポートしているクラウド・プロバイダーから入手します。

Inventoryは`tower-manage`コマンドを使ってAnsible Towerへインポートすることも可能で、今回のワークショップではこの方法でInventoryを追加します。


### Step 1:

INVENTORIESをクリックします。

### Step 2:

＋ADD(＋追加)をクリック、Inventory(インベントリー)を選択します ![Add button](at_add.png)

### Step 3:

以下の値を利用して、新規Inventoryを作成します。

項目 | 値
-----|--------------------------
NAME(名前) |Ansible Workshop Inventory
DESCRIPTION(説明)|workshop hosts
ORGANIZATION(組織)|Default

![Create an Inventory](at_inv_create.png)

### Step 4:

SAVE(保存)をクリックします。 ![Save button](at_save.png)

### Step 5:

SSHを利用し、Ansibleコントロールノードへログインします。

`tower-manage`　コマンドを利用して既存のインベントリファイルをAnsible Towerへインポートします。（以下のコマンドの_<location of you inventory>_をAnsibleEngineの演習で利用していたInventoryファイルのパスへ置き換えてください。)

```
sudo tower-manage inventory_import --source=<location of you inventory> --inventory-name="Ansible Workshop Inventory"
```

以下のような出力になるはずです:

![Importing an inventory with tower-manage](at_tm_stdout.png)

Ansible Towerのインベントリを確認してみてください。
先ほど作成したインベントリ"Ansible Workshop Inventory"内に、グループWebと、その中にノードが登録されていることが確認できるはずです。

![Inventory with Groups](at_inv_group.png)

### 結果

ここまでで、Ansible Towerの基本的な構成を終えることができました。
次の演習ではjob templateの作成と実行に焦点を当て、Ansible Towerがどのように機能するかを実際に見ていきます。

---

[Ansible Lightbulbのページへ戻ります - Ansible Tower Workshop](../README.md)
