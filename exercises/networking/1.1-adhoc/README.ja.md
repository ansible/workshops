# 演習 1.1 - アドホック・コマンドの実行

最初の演習は、Ansible の動きを確かめる上でいくつかの アドホック・コマンドを実行します。Ansible アドホック・コマンドはplaybookを作成せず直接タスクをリモードノードで実行する事が可能です。簡易かつクイックにいくつかのタスクを複数のリモートノードに実行したい場合にとても有効なコマンドです。

多くのコマンドと同様に、`ansible`実行コマンドも省略することが可能です。例えば、

```bash
ansible control --module-name ping
```

は、以下のように省略した形でも実行できます。
```
ansible control -m ping
```
当ワークショップでは以降、コマンドを省略した形で使用していきます。

ansible コマンドの後に指定されている `control` はインベントリで定義される自動化の対象ノード（複数または単体）を表します。ここではインベントがどのような定義になっているかは気にする必要はありません。

## Table of Contents
 - [ステップ 1: Ping](#ステップ-1-ホストへのping実行)
 - [ステップ 2: Command](#ステップ-2-command)
 - [ステップ 3: ios_facts](#ステップ-3-ios_facts)
 - [ステップ 4: ios_command](#ステップ-4-ios_command)
 - [ステップ 5: ios_banner](#ステップ-5-ios_banner)
 - [ステップ 6: ios_banner の削除](#ステップ-6-ios_banner-の削除)

### ステップ 1: ホストへのping実行

まずは基本的なLinuxホストへのping実行から始めましょう。これは所謂 ICMPの ping ではなく、同ホスト上での python スクリプト実行である点を認識してください。

```bash
ansible control -m ping
```

全てのAnsibleモジュールの関連オプションは、各モジュール毎にドキュメントページが存在しています。[Ansible ping モジュールはこちら](http://docs.ansible.com/ansible/latest/ping_module.html)

### ステップ 2: Command
Linuxコマンド形式で `command` モジュールを実行してみましょう。
```bash
ansible control -m command -a "uptime" -o
```

Ansible ドキュメントページはこちら [command モジュール](http://docs.ansible.com/ansible/latest/command_module.html)

### ステップ 3: ios_facts

今後は、ルーターを見てみることにしましょう。ios_facts モジュールにより ios デバイスの ansible facts を表示します。

```bash
ansible routers -m ios_facts -c network_cli
```

Ansible ドキュメントページはこちら [ios_facts モジュール](http://docs.ansible.com/ansible/latest/ios_facts_module.html)

### ステップ 4: ios_command

ios_command モジュールを使い、インターフェースサマリを収集します。

```bash
ansible routers -m ios_command -a 'commands="show ip int br"' -c network_cli
```
Ansible ドキュメントページはこちら [ios_command モジュール](http://docs.ansible.com/ansible/latest/ios_command_module.html)
### ステップ 5: ios_banner
これらを変更する前にルーターのバナーをチェックします。
```bash
ansible routers -m ios_command -a 'commands="show banner motd"' -c network_cli
```
現在 motd バナーは使用されてないことがわかるでしょう。

では、ios_bannerモジュールを利用し、motd バナーを追加しましょう。

```bash
ansible routers -m ios_banner -a 'banner=motd text="Ansible is awesome!" state=present' -c network_cli
```
では、今からテストを再実行し、違いを見てみましょう。
```bash
ansible routers -m ios_command -a 'commands="show banner motd"' -c network_cli
```
Ansible ドキュメントページはこちら [ios_banner module](http://docs.ansible.com/ansible/latest/ios_banner_module.html)

### ステップ 6: ios_banner の削除

最後に、もとに戻すためバナーを削除します。

```bash
ansible routers -m ios_banner -a 'banner=motd state=absent' -c network_cli
```
気軽に ios_command コマンドを使って再びチェックしてみてください。

# 完了
演習 1.1 はこれで完了です。

 ---
[Click Here to return to the Ansible Linklight - Networking Workshop](../README.ja.md)
