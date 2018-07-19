# 演習 2.1 - Ansible Tower のインストール

この演習ではコントロールノードにAnsible Towerをインストールします。

## ステップ 1: コントロールノードに ssh します

```bash
ssh <username>@<IP of control node>
```

## ステップ 2: /tmp ディレクトリに移動します

```bash
cd /tmp
```

## ステップ 3: 最新のAnsible Towerパッケージをダウンロードします

```bash
curl -O https://releases.ansible.com/ansible-tower/setup/ansible-tower-setup-latest.tar.gz
```

## ステップ 4: パッケージファイルを解凍(untar)します

```bash
tar xvfz /tmp/ansible-tower-setup-latest.tar.gz
```

## ステップ 5: 解凍したAnsible Towerパッケージのディレクトリに移動します

```bash
cd /tmp/ansible-tower-setup-*
```

## ステップ 6: 適当なテキストエディタを使ってインベントリーファイルを開きます

```bash
vim inventory
```

## ステップ 7: インベントリーファイルのいくつかの変数を設定します: `admin_password`, `rabbitmq_password`, `pg_password`

```yml
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

# Needs to be true for fqdns and ip addresses
rabbitmq_use_long_name=false
```

## ステップ 8: Ansible Towerセットアップスクリプトを実行します

```bash
sudo ./setup.sh
```
ステップ 8 は概ね10-15分かかります。休憩するのに丁度良いタイミングです。

## 結果

Ansible Towerのインストールは終了です。`https://<IP-of-your-control-node>` でTowerにアクセスできます。

以下の様にTowerのURL(コントロールノードのIPアドレス)をブラウズできれば成功です。

![Figure 1: Ansible Tower Login Screen](tower.png)

 ---
[Ansible Linklight - ネットワークワークショップ に戻る](../README.ja.md)
