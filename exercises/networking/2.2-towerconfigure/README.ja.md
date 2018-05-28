# 演習 2.2 - Ansible Tower の設定

この演習ではPlaybookを実行できるようにAnsible Towerを設定します。

# Ansible Tower のユーザーインターフェース

Ansible Towerのユーザーインターフェースには、マルチテナンシー、通知機能、スケジュール実行などに関連したものもありますが、ここではこのワークショップで必要になる最小限のユーザーインターフェースのみを説明します。

- クリデンシャル(Credentials, 認証情報のこと)
- プロジェクト(Projects, 様々な情報をひとまとめにする単位)
- インベントリー(Inventory, Playbookを実行する対象)
- ジョブテンプレート(Job Template, Playbook,Inventory,Credentialをまとめて実行できるようにしたもの)

## Ansible Towerにログインし、ライセンスキーをインストールする

### ステップ 1: ログイン
ユーザ名 `admin` 、パスワード `ansibleWS` (演習2.1で使用したパスワード)

![Figure 1: Ansible Tower Login Screen](tower.png)

ログインすると、ライセンスキーをリクエストする(1)か、入手済みのライセンスファイルをブラウズする(2)かを促されます。

![Figure 2: Uploading a License](license.png)

## ステップ 2: ライセンスファイルのダウンロード
別のブラウザタブで [ワークショップ用のライセンスファイルリクエスト](https://www.ansible.com/workshop-license )リンクを開いてライセンスファイルをリクエストします。

## ステップ 3: ライセンスファイルのアップロード
TowerのGUIに戻り,  ![BROWSE](browse.png) をクリックしてe-mailで受け取ったライセンスファイルをTowerにアップロードします。

## ステップ 4: ライセンスの確認
"I agree to the End User License Agreement" を選択

## ステップ 5: Submit
![SUBMIT](submit.png) をクリック

# クリデンシャル(Credential)の作成

クリデンシャルは、ジョブをマシンに対して実行する時、インベントリーをソースと同期する時、プロジェクトのコンテンツをバージョン管理システムからインポートする時の認証に使用されます。


多くの [クリデンシャルの種類](http://docs.ansible.com/ansible-tower/latest/html/userguide/credentials.html#credential-types) 、マシン(machine), ネットワーク(network), クラウドプロバイダー(cloud providers)などがあります。このワークショップではネットワーククリデンシャルを使います。

## ステップ 1: ギヤアイコンを選択
ブラウザウィンドウ右上の ![GEAR](gear.png) アイコンをクリック

## ステップ 2: CREDENTIAL を選択

## ステップ 3: CREDENTIAL を追加
![ADD](add.png) ボタンをクリック

## ステップ 4: 以下の値でフォームを入力

| Field                | Value                                                                 |
| -------------------- |-----------------------------------------------------------------------|
| **NAME**             | Ansible Workshop Credential                                           |
| **DESCRIPTION**      | Credentials for Ansible Workshop                                      |
| **ORGANIZATION**     | Default                                                               |
| **CREDENTIAL TYPE**  | Network                                                               |
| **USERNAME**         | ec2-user                                                              |
| **SSH Key**          | Ansible Towerノードからsshプライベートキーをコピーペースト `cat ~/.ssh/aws-private.pem`  |

![Figure 3: Adding a Credential](credential.png)

## ステップ 5: 保存
![SAVE](save.png) ボタンをクリック

# プロジェクトの作成
プロジェクトはAnsible PlaybookのTower内での論理的な集まりです。PlaybookとPlaybookのフォルダはTowerサーバのプロジェクトベースパスの下に手動で配置するか、ソースコード管理システム(SCM)に配置することができます。TowerがサポートするSCMは Git, Subversion, Mercurial です。

## ステップ 1: PROJECT をクリック
トップメニューの **PROJECTS** タブをクリック

## ステップ 2: Project の追加
![Add](add.png) ボタンをクリック

## ステップ 3: 以下の値をフォームに入力

| Field                  | Value                                                                 |
| ---------------------- |-----------------------------------------------------------------------|
| **NAME**               | Ansible Workshop Project                                              |
| **DESCRIPTION**        | Workshop playbooks                                                    |
| **ORGANIZATION**       | Default                                                               |
| **SCM TYPE**           | Git                                                                   |
| **SCM URL**            | https://github.com/network-automation/linklight/                      |
| **SCM UPDATE OPTIONS** | Cleanをチェック, Delete on Updateのチェックを外す, Update on Launchをチェック         |

![Figure 4: Defining a Project](project.png)

# インベントリー(Inventory)の作成

インベントリーはジョブが実行されるホストの集まりです。インベントリーはグループに分けられ、このグループに実際のホストが含まれます。グループはAnsible Towerに手動でホスト名を入力する事もできますし、Ansible Towerがサポートしているクラウドプロバイダーから自動的に取得することもできます。

また、インベントリーは `tower-manage` コマンドを使用してTowerにインポートすることもできます。このワークショップではこの方法でインベントリーを追加します。

## ステップ 1: インベントリーの作成
トップメニューの **INVENTORIES** タブをクリック

## ステップ 2: インベントリーの追加
![Add](add.png) ボタンをクリックし、 **Inventory** (Smart Inventoryでは無い)を選択

## ステップ 3: 以下の値でフォームを入力

| Field                  | Value                                                                 |
| ---------------------- |-----------------------------------------------------------------------|
| **NAME**               | Ansible Workshop Inventory                                            |
| **DESCRIPTION**        | Ansible Inventory                                                     |
| **ORGANIZATION**       | Default                                                               |

![Figure 5: Create an Inventory](inventory.png)

## ステップ 4: インベントリーの保存
![Save](save.png) ボタンをクリック

## ステップ 5: sshを使ってTowerノードにログイン
```bash
ssh studentXX@<IP_Address_of_your_tower_node>
```

## ステップ 6: 既存インベントリーのインポート

tower-manage コマンドを使って既存のインベントリーをインポート (studentXX を自分のstudent番号に変更してください)

```bash
sudo tower-manage inventory_import --source=/home/studentXX/networking-workshop/lab_inventory/hosts --inventory-name="Ansible Workshop Inventory"
```

以下の様なアウトプットになります。

```
[student2@ip-172-17-3-250 ~]$ sudo tower-manage inventory_import --source=/home/student1/networking-workshop/lab_inventory/hosts --inventory-name="Ansible Workshop Inventory"
    1.676 INFO     Updating inventory 2: Ansible Workshop Inventory
    1.755 INFO     Reading Ansible inventory source: /home/student2/linklight/lessons/lab_inventory/hosts
    2.704 ERROR     [WARNING]: Found both group and host with same name: control
    2.704 INFO     Processing JSON output...
    2.704 INFO     Loaded 3 groups, 4 hosts
    2.708 INFO     Inventory variables unmodified
    2.715 INFO     Group "control" added
    2.720 INFO     Group "hosts" added
    2.724 INFO     Group "routers" added
    2.734 INFO     Host "tower" added
    2.739 INFO     Host "host1" added
    2.743 INFO     Host "rtr1" added
    2.748 INFO     Host "rtr2" added
    2.759 INFO     Host "tower" added to group "control"
    2.766 INFO     Host "host1" added to group "hosts"
    2.773 INFO     Host "rtr1" added to group "routers"
    2.773 INFO     Host "rtr2" added to group "routers"
    2.856 INFO     Inventory import completed for  (Ansible Workshop Inventory - 9) in 1.2s
```

TowerのGUIでインベントリーを確認してみてください。インベントリーにはグループが登録され、それぞれのグループにホストが含まれています。

![Figure 7: Inventory with Groups](groups.png)

# 結果

Ansible Towerの基本設定をしました。次の演習ではジョブテンプレートの作成と実行を行います。

 ---
[Ansible Linklight - ネットワークワークショップ に戻る](../README.ja.md)
