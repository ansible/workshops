# 演習 - インベントリ、認証情報、Ad Hoc コマンド

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),![japan](../../../images/japan.png)[日本語](README.ja.md),![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## 目次

* [目的](#目的)
* [ガイド](#ガイド)
* [インベントリを調べる](#インベントリを調べる)
* [マシンの資格情報を調べる](#マシンの資格情報を調べる)
* [Ad Hoc コマンドを実行する](#Ad-Hoc-コマンドを実行する)
* [チャレンジ Lab: Ad Hoc コマンド](#チャレンジ-Lab-Ad-Hoc-コマンド)

# 目的

この演習では、Lab 環境を探索して理解します。
- 項目と理解:
  - Ansible Tower [**Inventory**](https://docs.ansible.com/ansible-tower/latest/html/userguide/inventories.html)
  - Ansible Tower [**Credentials**](https://docs.ansible.com/ansible-tower/latest/html/userguide/credentials.html)
- Ansible Tower Web UIを介した Ad Hoc コマンドの実行

# ガイド

## インベントリを調べる

最初に必要なのは、管理対象ホストの一覧です。これは、Ansible Engineのインベントリファイルに相当します。動的インベントリのように、それ以外にもたくさんありますが、基本から始めましょう。

  - すでに Web UI を開いているはずですが、開いていない場合は **https://student\<X\>.workshopname.rhdemo.io** ("\<X\>"を学生番号に、"workshopname" を現在のワークショップ名に置き換えてください) のように URL をブラウザで指定して、`admin` としてログインしてください。パスワードは講師が教えてくれます。

**Workshop Inventory** が１つあります。**Workshop Inventory** をクリック後、**ホスト** ボタンをクリックします。

`~/lab_inventory/hosts` のインベントリ情報は、プロビジョニングプロセスの一部として Ansible Tower Inventory に事前にロードされています。

```bash
$ cat ~/lab_inventory/hosts
[all:vars]
ansible_user=student<X>
ansible_ssh_pass=PASSWORD
ansible_port=22

[web]
node1 ansible_host=22.33.44.55
node2 ansible_host=33.44.55.66
node3 ansible_host=44.55.66.77

[control]
ansible ansible_host=11.22.33.44
```
> **警告**
>
> あなたのインベントリの IP アドレスは異なります。

## マシンの資格情報を調べる

ここでは、Tower から管理ホストにアクセスするための資格情報を調べてみましょう。 この Ansible Workshop のプロビジョニングプロセスの一部として、**Workshop Credential** はすでに設定されています。

**リソース** メニューで、**資格情報** を選択します。その後、**Workshop Credential** をクリックします。

Note the following information:

<table>
  <tr>
    <th>パラメータ</th>
    <th>値</th>
  </tr>
  <tr>
    <td>Credential Type</td>
    <td><code>Machine</code>- マシン資格情報は、プレイブックの ssh およびユーザレベルの特権エスカレーションアクセスを定義します。これらは、リモートホスト上でプレイブックを実行するためにジョブを送信するときに使用されます</td>
  </tr>
  <tr>
    <td>username</td>
    <td><code>ec2-user</code> これは他の linux ノードのコマンドライン Ansible インベントリのユーザ名と一致します</td>
  </tr>
  <tr>
    <td>SSH PRIVATE KEY</td>
    <td><code>ENCRYPTED</code> - Ansible Tower に SSH 秘密鍵を渡すと、実際には調べられないことに注意してください</td>
  </tr>
</table>

## Ad Hoc コマンドを実行する

Ansible Tower から Ad Hoc コマンドを実行することも可能です。

  - Web UI で **リソース → インベントリ → Workshop Inventory** に移動します。

  - **ホスト** ボタンをクリックし、ホストビューに切り替え、ホストエントリの左側にあるボックスをチェックして3つのホストを選択します。

  - **コマンドの実行** をクリックします。 次の画面で、Ad Hoc コマンドを指定する必要があります:

  <table>
    <tr>
      <th>パラメータ</th>
      <th>値</th>
    </tr>
    <tr>
      <td>MODULE</td>
      <td>ping</td>
    </tr>
    <tr>
      <td>MACHINE CREDENTIAL</td>
      <td>Workshop Credentials</td>
    </tr>
  </table>

  - **起動** をクリックし、出力を確認します。

<hr>

シンプルな **ping** モジュールはオプションを必要としません。他のモジュールでは、実行するコマンドを引数として指定する必要があります。**command** モジュールを試し、Ad Hoc コマンドを使用して実行中のユーザーの user ID を見つけます。

  <table>
    <tr>
      <th>パラメータ</th>
      <th>値</th>
    </tr>
    <tr>
      <td>MODULE</td>
      <td>command</td>
    </tr>
    <tr>
      <td>ARGUMENTS</td>
      <td>id</td>
    </tr>
  </table>

> **ヒント**
>
> 実行するモジュールを選択した後、"Arguments" の横にある疑問符をクリックすると、Tower はモジュールのドキュメントページへのリンクを提供します。これは便利ですので試してみてください。

<hr>

システムから秘密の情報を取得しようとするとどうでしょうか？ */etc/shadow* を出力してみてください。

<table>
  <tr>
    <th>パラメータ</th>
    <th>値</th>
  </tr>
  <tr>
    <td>MODULE</td>
    <td>command</td>
  </tr>
  <tr>
    <td>ARGUMENTS</td>
    <td>cat /etc/shadow</td>
  </tr>
</table>


> **警告**
>
> **エラーが発生します！**

おっと、最後の1つはうまくいかず、すべて赤でした。

最後のアドホックコマンドを再実行しますが、今度は **ENABLE PRIVILEGE ESCALATION** チェックボックスをオンにします。

ごらんの通り、今回は実行できました。rootとして実行する必要があるタスクの場合は、特権を昇格させる必要があります。これは Ansible playbook で使用されている **become: yes** と同じです。

## チャレンジ Lab: Ad Hoc コマンド

さて、小さなチャレンジ: Ad Hoc コマンドを実行して "tmux" パッケージがすべてのホストにインストールされていることを確認します。もし不明な場合は、上記の Web UI を利用、もしくは `[ansible@tower ~]$ ansible-doc yum` コマンドを Tower コントロールホストで実行し、ドキュメントを参照してください。

> **警告**
>
> **以下は解答です！**

<table>
  <tr>
    <th>パラメータ</th>
    <th>値</th>
  </tr>
  <tr>
    <td>yum</td>
    <td>command</td>
  </tr>
  <tr>
    <td>ARGUMENTS</td>
    <td>name=tmux</td>
  </tr>
  <tr>
    <td>ENABLE PRIVILEGE ESCALATION</td>
    <td>✓</td>
  </tr>
</table>

> **ヒント**
>
> コマンドの黄色の出力は、Ansibleが実際に何かを実行したことを示しています（ここでは、パッケージをインストールする必要がありました）。アドホックコマンドをもう一度実行すると、出力が緑色になり、パッケージが既にインストールされていることが通知されます。Ansible の黄色は、「注意してください」という意味ではありません... ;-)

----
**ナビゲーション**
<br>
[前の演習](../2.1-intro/README.ja.md) - [次の演習](../2.3-projects/README.ja.md)

[ここをクリックして Ansible for Red Hat Enterprise Linux Workshop に戻ります](../README.ja.md#Section-2---Ansible-Towerの演習)
