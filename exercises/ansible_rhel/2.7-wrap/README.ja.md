# 演習 2.7 - まとめ

# 最終チャレンジとまとめ  

今までに学んだことを踏まえて以下の課題を実施してみましょう。  

## ステージの設定  

Your operations team and your application development team like what they see in Tower. To really use it in their environment they put together these requirements:

- すべてのWebサーバー（`node1`、`node2`および`node3`）は1つのグループに入れる必要があります

- Webサーバーは開発目的または本番稼働で使用するため、 "stage dev" または "stage prod" としてそれに応じてフラグを立てる必要があります

    - 現在 `node1` `node3` は開発用として利用されており、 `host2` は本番環境として稼働しています

- もちろん、世界的に有名な♬アプリケーション "index.html" は開発と本番で内容が異なります  

    - ページに環境を説明するタイトルが必要です  

    - コンテンツ用の場所を作りましょう

- Web コンテンツの開発者 `wweb` 開発及び本番ホストのコンテンツ変更のため、Survey 入力を行うための権限が必要です

## Git リポジトリ

すべてのコードは Github にあるものを使います。https://github.com/ansible/workshop-examples で **Ansible Workshop Examples** の gitリポジトリを確認してください。そこに `role_webcontent Role` を呼び出すプレイブック `webcontent.yml` があります。

以前の Apache インストールロールと比較すると、大きな違いがあります。`index.html` テンプレートには2つのバージョンがあり、そのソースファイルの一部には変数入力が存在し、タスクによりこのテンプレートがデプロイされます。  

`dev_index.html.j2` 

```html
<body>
<h1>This is a development webserver, have fun!</h1>
{{ dev_content }}
</body>
```

`prod_index.html.j2`

```html
<body>
<h1>This is a production webserver, take care!</h1>
{{ prod_content }}
</body>
```

`main.yml`

```yaml
[...]
- name: Deploy index.html from template
  template:
    src: "{{ stage }}_index.html.j2"
    dest: /var/www/html/index.html
  notify: apache-restart
```

## インベントリーを確認する

これを達成する方法は1つだけではありませんが、次のことを行う必要があります。  

- すべてのホストがインベントリグループ `Webserver` に含まれていることを確認します

- `Webserver` インベントリーで、変数 `stage` を `dev` で定義

    - `Webserver` インベントリー の**変数**欄で、２行目に `stage: dev` を入力します  

- 同じ要領で、今度は、`node2` に対して変数 `stage: prod` を指定しますが、今回は `node2` をクリックしてインベントリー変数を上書きします。

> **ヒント**
>
> YAML スタートを意味する１行目のハイフンは消さないでください！

## テンプレートの作成

- 新しい **ジョブテンプレート** を `Create Web Content` という名前で作成します

    - ターゲットは `Webserver` インベントリーです

    - Playbook は、**Ansible Workshop Examples** の `rhel/apache/webcontent.yml` を使います  

    - 2 つの変数の値を、 `dev_content: default dev content` と `prod_content: default prod content` として、**追加変数**欄に入力します。   

    - 認証情報は `Workshop Credentials` を使い、権限昇格の上実行します

- テンプレートを保存します  

## 結果を確認します

今回は、Ansibleのアドホックコマンドを使って結果を確認します。利用するモジュールは command モジュールで、各ノードの curl 実行結果を確認してみます。  

```bash
$ ansible web -m command -a "curl -s http://localhost:80"
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

Note the warining in the first line about not to use `curl` via the `command` module since there are better modules right within Ansible. We will come back to that in the next part.

## Add Survey

- Add a survey to the Template to allow changing the variables `dev_content` and `prod_content`

- Add permissions to the Team `Web Content` so the Template **Create Web Content** can be executed by `wweb`.

- Run the survey as user `wweb`

Check the results. Since we got a warning last time using `curl` via the `command` module, this time we will use the dedicated `uri` module. As arguments it needs the actual URL and a flag to output the body in the results.

```bash
$ ansible web -m uri -a "url=http://localhost return_content=yes"
node2 | SUCCESS => {
    "accept_ranges": "bytes",
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "connection": "close",
    "content": "<body>\n<h1>This is a production webserver, take care!</h1>\nprod wweb\n</body>\n",
    "content_length": "77",
    "content_type": "text/html; charset=UTF-8",
    "cookies": {},
    "cookies_string": "",
    "date": "Wed, 10 Jul 2019 22:15:45 GMT",
    "elapsed": 0,
    "etag": "\"4d-58d5aef2a5666\"",
    "last_modified": "Wed, 10 Jul 2019 22:09:42 GMT",
    "msg": "OK (77 bytes)",
    "redirected": false,
    "server": "Apache/2.4.6 (Red Hat Enterprise Linux)",
    "status": 200,
    "url": "http://localhost"
}
[...]
```

## Solution

> **Warning**
>
> **Solution Not Below**

You have done all the required configuration steps in the lab already. If unsure, just refer back to the respective chapters.

# The End

Congratulations, you finished your labs\! We hope you enjoyed your first encounter with Ansible Tower as much as we enjoyed creating the labs.

----

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-2---ansible-tower-exercises)

