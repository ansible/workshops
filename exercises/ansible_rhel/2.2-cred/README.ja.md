# ワークショップ演習 - インベントリー、認証情報、およびアドホックコマンド

**他の言語でもお読みいただけます**:
<br>![uk](../../../images/uk.png) [English](README.md)、![japan](../../../images/japan.png)[日本語](README.ja.md)、![france](../../../images/fr.png) [Française](README.fr.md)、![Español](../../../images/col.png) [Español](README.es.md)

## 目次

* [目的](#目的)
* [ガイド](#ガイド)
* [インベントリーの検証](#インベントリーの検証)
* [マシンの認証情報の検証](#マシンの認証情報の検証)
* [アドホックコマンドの実行](#アドホックコマンドの実行)
* [チャレンジラボ: アドホックコマンド](#チャレンジラボ-アドホックコマンド)

## 目的

ラボ環境を調べて理解します。この演習では、以下を対象とします。

* 以下を見つけて理解:

  * Ansible 自動コントローラー [**インベントリー**](https://docs.ansible.com/automation-controller/latest/html/userguide/inventories.html)
  * Ansible 自動コントローラー [**認証情報**](https://docs.ansible.com/automation-controller/latest/html/userguide/credentials.html)

* Ansible 自動コントローラー WebUI を介したアドホックコマンドの実行

## ガイド

### インベントリーの検証

最初に必要なのは、管理対象ホストのインベントリーです。これは、Ansible Engine のインベントリファイルーに相当します。それ以外にもたくさんありますが、まずは基本から始めましょう。

* すでに Web UI を開いているはずですが、開いていない場合は、指定された URL をブラウザーで開きます。これは、`https://student.workshopname.demoredhat.com` のような URL です。"workshopname" は現在のワークショップの名前に変更します。`admin` としてログインします。このパスワードは、インストラクターから渡されます。

**Workshop Inventory** というインベントリーが現れます。**Workshop Inventory** をクリックして、**Hosts** ボタンをクリックします。

`~/lab_inventory/hosts` のインベントリー情報は、プロビジョニング目的の一環として Ansible 自動コントローラーインベントリーに事前にロードされていました。

```bash
$ cat ~/lab_inventory/hosts
[web]
node1 ansible_host=22.33.44.55
node2 ansible_host=33.44.55.66
node3 ansible_host=44.55.66.77

[control]
ansible ansible_host=11.22.33.44
```

> **警告**
>
> 実際の環境のインベントリーでは、IP アドレスが異なることがあります。

### マシンの認証情報の検証

次に、自動コントローラーから管理対象ホストにアクセスするための認証情報を調べます。この Ansible ワークショップのプロビジョニングプロセスの一環として、**ワークショップ資格情報**はすでに設定されています。

**Resource** メニューで **Credentials** を選択します。次に、*Workshop Credential** をクリックします。

次の情報に注意してください。

<table>
  <tr>
    <th>パラメーター</th>
    <th>値</th>
  </tr>
  <tr>
    <td>Credential Type</td>
    <td><code>Machine</code>- Machine credentials define ssh and user-level privilege escalation access for playbooks. They are used when submitting jobs to run playbooks on a remote host.</td>
  </tr>
  <tr>
    <td>Username</td>
    <td><code>ec2-user</code> which matches our command-line Ansible inventory username for the other Linux nodes</td>
  </tr>
  <tr>
    <td>SSH Private Key</td>
    <td><code>Encrypted</code> - take note that you can't actually examine the SSH private key once someone hands it over to Ansible Automation controller</td>
  </tr>
</table>

### アドホックコマンドの実行

Ansible 自動コントローラーからアドホックコマンドを実行することもできます。

* Web UIで、**Resource → Inventories → Workshop Inventory** に移動します。

* **Host** タブをクリックしてホストビューに変更し、ホストエントリーの左側にあるボックスにチェックマークを付けて 3 つのホストを選択します。

* **Run Command** ボタンをクリックします。次の画面で、アドホックコマンドを指定する必要があります。

**Details** ウィンドウで、**Module** `ping` を選択し、**Next** をクリックします。

**Execution Environment** ウィンドウで **Default execution environment** を選択し、**Next** をクリックします。

**Machine Credential**ウィンドウで、**Workshop Credentials** を選択し、**Launch** をクリックします。

> **ヒント**
>
> 結果の出力は、コマンドが完了すると表示されます。
>

<hr>

単純な **ping** モジュールにはオプションは必要ありません。他のモジュールの場合、引数として実行するコマンドを指定する必要があります。**command** モジュールを試して、アドホックコマンドを使用して実行中のユーザーのユーザー ID を見つけてください。

* Web UIで、**Resource → Inventories → Workshop Inventory** に移動します。

* **Host** タブをクリックしてホストビューに変更し、ホストエントリーの左側にあるボックスにチェックマークを付けて 3 つのホストを選択します。

* **Run Command** ボタンをクリックします。次の画面で、アドホックコマンドを指定する必要があります。

**Details** ウィンドウで、**Arguments** タイプ `id` で **Module** `command` を選択し、**Next** をクリックします。

**Execution Environment** ウィンドウで **Default execution environment** を選択し、**Next** をクリックします。

**Machine Credential**ウィンドウで、**Workshop Credentials** を選択し、**Launch** をクリックします。


> **ヒント**
>
> 実行するモジュールを選択します。"Arguments" の隣の疑問符をクリックすると、Ansible 自動コントローラーにより、モジュールの docs ページへのリンクが表示されます。これは便利なのでお試しください。

<hr>

システムから秘密情報を取得してみるのはどうでしょうか？*/etc/shadow* を出力してみましょう。

* Web UIで、**Resource → Inventories → Workshop Inventory** に移動します。

* **Host** タブをクリックしてホストビューに変更し、ホストエントリーの左側にあるボックスにチェックマークを付けて 3 つのホストを選択します。

* **Run Command** ボタンをクリックします。次の画面で、アドホックコマンドを指定する必要があります。

**Details** ウィンドウで、**Arguments** `cat /etc/shadow` で **Module** `command` を選択し、**次へ** をクリックします。

**Execution Environment** ウィンドウで **Default execution environment** を選択し、**Next** をクリックします。

**Machine Credential**ウィンドウで、**Workshop Credentials** を選択し、**Launch** をクリックします。

> **警告**
>
> **エラーが発生します**

最後のはうまく動作しません。すべて赤く表示されています。

最後のアドホックコマンドを再実行しますが、今回は **Enable privilege escalation** にチェックマークを付けます。

ご覧のとおり、今度は成功しました。`root` として実行する必要があるタスクの場合は、特権を昇格する必要があります。これは、AnsiblePlaybook で使用されている **become:yes** と同じです。

### チャレンジラボ: アドホックコマンド

さて、小チャレンジです。アドホックを実行して、パッケージ「tmux」がすべてのホストにインストールされていることを確認します。不明な場合は、上記の Web UI を介して、または自動コントローラー制御ホストで `[ansible@controller ~]$ ansible-doc yum` を実行してドキュメントを参照してください。

> **警告**
>
> **回答を以下に示します。**

* Web UIで、**Resource → Inventories → Workshop Inventory** に移動します。

* **Host** タブをクリックしてホストビューに変更し、ホストエントリーの左側にあるボックスにチェックマークを付けて 3 つのホストを選択します。

* **Run Command** ボタンをクリックします。次の画面で、アドホックコマンドを指定する必要があります。

**Details** ウィンドウで、**Module** `yum` を選択し、**Arguments** タイプ `name=tmux` で **Enable privilege escalation** をチェックし、**Next** をクリックします。

**Execution Environment** ウィンドウで **Default execution environment** を選択し、**Next** をクリックします。

**Machine Credential**ウィンドウで、**Workshop Credentials** を選択し、**Launch** をクリックします。



> **ヒント**
>
「CHANGED」という出力でパッケージがインストールされたことに注目してください。この ad hoc コマンドを2回目に実行すると、出力には「SUCCESS」と表示され、messageパラメータで「何もすることはありません」と通知されます。

---
**ナビゲーション**
<br>
[前の演習](../2.1-intro) - [次の演習](../2.3-projects)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-2---ansible-tower-exercises)
