# 演習 1.8 - ボーナスラボ  

**Read this in other languages**: ![uk](../../../../images/uk.png) [English](README.md),  ![japan](../../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md).

* [ステップ 1.8.1 - ボーナスラボ: アドホックコマンド](#ステップ-181---ボーナスラボ-アドホックコマンド)
* [ステップ 1.8.2 - ボーナスラボ: テンプレートと変数](#ステップ-182---ボーナスラボ-テンプレートと変数)
   * [変数を定義します:](#変数を定義します)
   * [テンプレートを準備します](#テンプレートを準備します)
   * [Playbook を作成します。](#playbook-を作成します)
   * [実行し確認します](#実行し確認します)

あなたは既にラボを完了しています・・・、が、さらに先に進みたい方は是非このボーナスラボにチャレンジしてみてください。  

## ステップ 1.8.1 - ボーナスラボ: アドホックコマンド  

アドホックコマンドを使って、適当なコメント付きで新しいユーザー "testuser"　を `node1` と `node3` に作成します。`node2` に作成してはいけません。実行後、想定通り作成できていることも確認します。  

  - `ansible-doc user` を使ってモジュールのパラメータを確認します。  

  - アドホックコマンドを使ってコメント "Test D User" 付きのユーザーを作成します。  

  - "command" モジュールを使ってユーザー ID を見つけます。  

  - ユーザーとユーザーのティレクトリを削除し、ユーザーが削除されたことを確認します。

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

`httpd.conf` のリッスンポートを都度 vi 等で編集してコピーするのではなく、変数としてテンプレートの中で定義し、その変数の値を変数ファイルを使って与える方法について考えてみます。  


  - `listen_port` に変数を埋め込んだ `httpd.conf` ファイルを作成し、 `httpd.conf.j2` テンプレートを使って各 node に送付します。  

  - `web` グループのリッスンポートとして `8080` 、 `node2` のリッスンポートとして `80` を取るように変数ファイルを作成します。

  - ハンドラーを使っ、`httpd.conf` に変更があった場合のみ Apache サービスを再起動する Playbook を作成します。  

  - Playbook を実行し、結果を `curl` コマンドで確認します。  

> **ヒント**  
>
> `group_vars`と`host_vars` ディレクトリを覚えていますか？ そうでない場合は、「演習1.4 変数を使ってみる」の章を参照してください。


> **回答は以下の通り**

### 変数を定義します:  


グループ変数を定義する `group_vars/web` に以下を記述します  

```ini
listen_port: 8080
```

node2 は設定が異なるので、ホスト変数を定義する `host_vars/node2` に以下を記述します  

```ini
listen_port: 80
```
### テンプレートを準備します  

  - node1 から `httpd.conf` を `httpd.conf.j2` としてコピーします。以前の演習でダウンロードしたファイルを "mv" で再利用してもOKです。  

  - コピーした `httpd.conf.j2` の "Listen" の項目を以下の通り変数 `listen_port` として定義しなおします。  

<!-- {% raw %} -->
```ini
[...]
Listen {{ listen_port }}
[]...]
```
<!-- {% endraw %} -->

### Playbook を作成します。

Playbook `apache_config_tpl.yml` を以下の内容で作成します。  

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

### 実行し確認します  

まずは playbook を実行し、curl コマンドで、 `node1` と `node3` にポート `8080` そして `node2` にポート `80` で接続してみます。  

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
[Ansible Engine ワークショップ表紙に戻る](../../README.ja.md#section-1---ansible-engineの演習)
