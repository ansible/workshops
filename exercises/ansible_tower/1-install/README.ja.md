# Exercise 1 - Ansible Towerのインストール

この演習では、あなたのコントロールノードへAnsible Towerのインストールが実行されます。

## Ansible Towerのインストール


### Step 1:

ディレクトリを /tmp へ移動してください。

```bash
cd /tmp
```

### Step 2:

Ansible Tower の最新版packageをダウンロードします。

```bash
curl -O https://releases.ansible.com/ansible-tower/setup/ansible-tower-setup-latest.tar.gz
```

### Step 3:

ダウンロードしたパッケージファイルの Untar と unzip を実行します。

```bash
tar xvfz /tmp/ansible-tower-setup-latest.tar.gz
```

### Step 4:

Ansible Towerパッケージを解凍したディレクトリへ移動します。

```bash
cd /tmp/ansible-tower-setup-*/
```

### Step 5:

inventoryファイルを編集します。(ここではvimを用いていますが、好みのエディターを使ってください)

```bash
vim inventory
```

### Step 6:

inventoryファイル内で、AnsibleTowerが必要とするパスワードを変数として追加します。
以下の3つへ任意のパスワード情報を記述してください。:
`admin_password, pg_password, rabbitmq_password`

```ini
[tower]
localhost ansible_connection=local

[database]

[all:vars]
admin_password='ansibleWS'

pg_host=''
pg_port=''

pg_database='awx'
pg_username='awx'
pg_password='ansibleWS'

rabbitmq_port=5672
rabbitmq_vhost=tower
rabbitmq_username=tower
rabbitmq_password='ansibleWS'
rabbitmq_cookie=cookiemonster

= Needs to be true for fqdns and ip addresses
rabbitmq_use_long_name=false

```

### Step 7:

Ansible Tower のセットアップスクリプトを実行します。

```bash
sudo ./setup.sh
```

---
**NOTE**
Step 7 のセットアップスクリプトの完了まで10-15分ほど時間がかかります。
良いタイミングなので、休憩を取りましょう。

---


### 結果

セットアップスクリプトがfail=0で終了している場合、あなたのAnsible Towerのインストレーションは無事に完了しているはずです。
以下のURLからAnsible Towerへアクセスしてみましょう。


```bash
https://コントローラーノードのIPアドレス
```

### インストール結果の確認
ブラウザでの確認では、証明書エラーが表示されるかもしれませんが、本日のWSでは無視してください。
コントローラーノードのIPアドレスへアクセスし、以下のようなAnsible TowerのGUIが確認できれば、インストレーション結果の確認までが完了しました。

![Ansible Tower Login Screen](ansible-lab-figure01-logon-screen.png)

---

[Ansible Lightbulbのページへ戻ります - Ansible Tower Workshop](../README.ja.md)
