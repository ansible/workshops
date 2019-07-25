# 演習 1.8 - ボーナスラボ

あなたは既にラボを完了しています・・・、が、さらに先に進みたい方は是非このボーナスラボにチャレンジしてみてください。

## ステップ 1.8.1 - ボーナスラボ: アドホックコマンド

アドホックコマンドを使って、適当なコメント付きで新しいユーザー "testuser"　を `node1` と `node3` に作成します。`node2` に作成してはいけません。きちんとできたことも確認してください。  
    
  - `ansible-doc user` を使ってモジュールのパラメータを確認します。

  - アドホックコマンドを使ってコメント "Test D User" 付きのユーザーを作成します。

  - "command" モジュールを使ってユーザー ID を見つけます。

  - ユーザーを削除し、それが削除されたことを確認します

> **ヒント**
> 
> 権限昇格の記述を忘れないこと！

> **答えは以下の通り**

コマンドは次のようになります。

```bash
[student<X>@ansible ansible-files]$ ansible-doc -l | grep -i user
[student<X>@ansible ansible-files]$ ansible-doc user
[student<X>@ansible ansible-files]$ ansible node1,node3 -m user -a "name=testuser comment='Test D User'" -b
[student<X>@ansible ansible-files]$ ansible node1,node3 -m command -a " id testuser" -b
[student<X>@ansible ansible-files]$ ansible node2 -m command -a " id testuser" -b
[student<X>@ansible ansible-files]$ ansible node1,node3 -m user -a "name=testuser state=absent remove=yes" -b
[student<X>@ansible ansible-files]$ ansible web -m command -a " id testuser" -b
```

## ステップ 1.8.2 - ボーナスラボ: テンプレートと変数

皆さんは今までのラボで、Ansibleのテンプレート、変数、そしてハンドラについての基本を既に学んでいます。これらすべてを組み合わせてみましょう。  

`httpd.conf` のリッスンポートを編集してコピーするのではなく、ポートの値を変数としてテンプレートの中で定義し、その変数の値をホストごとに適切に与えるる方法について考えてみます。

  - `web` グループのリッスンポートとして "8080" 、 `node2` のリッスンポートとして `80` を取るように変数ファイルを作成します。

  - `httpd.conf` ファイルを `httpd.conf.j2` テンプレートを使い、かつ、 `listen_port` に上記変数を埋め込んだ上で各 node に送付します。

  - テンプレートをデプロイし、ハンドラを使用して変更があった場合にApacheを再起動するPlaybookを作成します。

  - Playbook を実行し、結果を `curl` コマンドで確認します。

> **Tip**
>
> `group_vars`と` host_vars` ディレクトリを覚えていますか？ そうでない場合は、「Ansible変数」の章を参照してください。


> **Warning**
> 
> **Solution below\!**

### Define the variables:


Add this line to `group_vars/web`:

```ini
listen_port: 8080
```

Add this line to `host_vars/node2`:

```ini
listen_port: 80
```
### Prepare the template:

  - Copy `httpd.conf` to `httpd.conf.j2`

  - Edit the "Listen" directive in `httpd.conf.j2` to make it look like this:

<!-- {% raw %} -->
```ini
[...]
Listen {{ listen_port }}
[]...]
```
<!-- {% endraw %} -->

### Create the Playbook

Create a playbook called `apache_config_tpl.yml`:

```yaml
---
- name: Apache httpd.conf
  hosts: web
  become: yes
  tasks:
  - name: Create Apache configuration file from template
    template:
      src: httpd.conf.j2
      dest: /etc/httpd/conf/httpd.conf
    notify:
        - restart apache
  handlers:
    - name: restart apache
      service:
        name: httpd
        state: restarted
```

### Run and test

First run the playbook itself, then run curl against `node1` with port `8080` and `node2` with port `80`.

```bash
[student1@ansible ansible-files]$ ansible-playbook apache_config_tpl.yml 
[...]
[student1@ansible ansible-files]$ curl http://18.195.235.231:8080
<body>
<h1>This is a development webserver, have fun!</h1>
</body>
[student1@ansible ansible-files]$ curl http://35.156.28.209:80
<body>
<h1>This is a production webserver, take care!</h1>
</body>
```

----

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-1---ansible-engine-exercises)

