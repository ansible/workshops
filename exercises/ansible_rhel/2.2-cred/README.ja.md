# ワークショップ演習 - インベントリー、認証情報、およびアドホックコマンド

**その他の言語はこちらをお読みください。**:
<br>![uk](../../../images/uk.png) [English](README.md),![japan](../../../images/japan.png)[日本語](README.ja.md),![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## 目次

* [目的](#objective)
* [ガイド](#guide)
* [インベントリーを調べる](#examine-an-inventory)
* [マシンの認証情報を調べる](#examine-machine-credentials)
* [アドホックコマンドの実行](#run-ad-hoc-commands)
* [チャレンジラボ: アドホックコマンド](#challenge-lab-ad-hoc-commands)

## 目的

ラボ環境を調べて理解します。この演習では、以下を対象とします。

* 以下を見つけて理解:

  * Ansible Tower
    [**インベントリー**](https://docs.ansible.com/ansible-tower/latest/html/userguide/inventories.html)
  * Ansible Tower
    [**認証情報**](https://docs.ansible.com/ansible-tower/latest/html/userguide/credentials.html)

* Ansible Tower WebUI を介したアドホックコマンドの実行

## ガイド

### インベントリーを調べる

最初に必要なのは、管理対象ホストのインベントリーです。これは、Ansible Engine
のインベントリファイルーに相当します。それ以外にもたくさんありますが、まずは基本から始めましょう。

* すでに Web UI を開いているはずですが、開いていない場合は、指定された URL
  をブラウザーで開きます。これは、**https://student\<X\>.workshopname.rhdemo.io** のような URL
  です。<X\> は学習者番号に、"workshopname" は現在のワークショップの名前に変更します。`admin`
  としてログインします。このパスワードは、インストラクターから渡されます。

**Workshop Inventory** というインベントリーが現れます。**Workshop Inventory**
をクリックして、**Hosts** ボタンをクリックします。

`~/lab_inventory/hosts` のインベントリー情報は、プロビジョニング目的の一環として Ansible Tower
インベントリーに事前にロードされていました。

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
ansible-1 ansible_host=11.22.33.44
```

> **警告**
>
> 実際の環境のインベントリーでは、IP アドレスが異なることがあります。

### マシンの認証情報を調べる

次に、Tower から管理対象ホストにアクセスするための認証情報を調べます。この Ansible
ワークショップのプロビジョニングプロセスの一環として、**ワークショップ資格情報**はすでに設定されています。

**RESOURCES** メニューで **Credentials** を選択します。次に、*Workshop Credential**
をクリックします。

次の情報に注意してください。

<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>Credential Type</td>
    <td><code>Machine</code>- Machine credentials define ssh and user-level privilege escalation access for playbooks. They are used when submitting jobs to run playbooks on a remote host.</td>
  </tr>
  <tr>
    <td>username</td>
    <td><code>ec2-user</code> which matches our command-line Ansible inventory username for the other linux nodes</td>
  </tr>
  <tr>
    <td>SSH PRIVATE KEY</td>
    <td><code>ENCRYPTED</code> - take note that you can't actually examine the SSH private key once someone hands it over to Ansible Tower</td>
  </tr>
</table>

### アドホックコマンドの実行

AnsibleTower からアドホックコマンドを実行することもできます。

* Web UIで、**RESOURCES → Inventories → Workshop Inventory** に移動します。

* **HOSTS** ボタンをクリックしてホストビューに変更し、ホストエントリーの左側にあるボックスにチェックマークを付けて 3
  つのホストを選択します。

* **RUN COMMANDS**をクリックします。次の画面で、アドホックコマンドを指定する必要があります。

  <table>
    <tr>
      <th>Parameter</th>
      <th>Value</th>
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

  * ** LAUNCH **をクリックして、出力を確認します。

<hr>

単純な **ping**
モジュールにはオプションは必要ありません。他のモジュールの場合、引数として実行するコマンドを指定する必要があります。**command **
モジュールを試して、アドホックコマンドを使用して実行中のユーザーのユーザー ID を見つけてください。

  <table>
    <tr>
      <th>Parameter</th>
      <th>Value</th>
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
> 実行するモジュールを選択します。"Arguments" の隣の疑問符をクリックすると、モジュールの docs ページへのリンクが表示されます。これは便利なのでお試しください。

<hr>

システムから秘密情報を取得してみるのはどうでしょうか？*/etc/shadow* を出力してみましょう。

<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
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
> **エラーが発生します**

最後のはうまく動作しません。すべて赤く表示されています。

最後のアドホックコマンドを再実行しますが、今回は **ENABLE PRIVILEGE ESCALATION** ボックスにチェックマークを付けます。

ご覧のとおり、今度は成功しました。root として実行する必要があるタスクの場合は、特権を昇格する必要があります。これは、AnsiblePlaybook
で使用されている * become: yes** と同じです。

### チャレンジラボ: アドホックコマンド

さて、小チャレンジです。アドホックを実行して、パッケージ「tmux」がすべてのホストにインストールされていることを確認します。不明な場合は、上記の
Web UI を介して、または Tower 制御ホストで `[ansible@tower ~]$ ansible-doc yum`
を実行してドキュメントを参照してください。

> **警告**
>
> **回答を以下に示します。**

<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
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
> コマンドの黄色い出力では、Ansible が実際に行ったことを示しています (ここでは、パッケージをインストールする必要がありました)。2 回目にアドホックコマンドを実行すると、出力が緑色になり、パッケージが既にインストールされていることが通知されます。そのため、Ansible での黄色の出力は、「注意」と示しているわけではありません。

---
**ナビゲーション**
<br>
[前の演習](../2.1-intro) - [次の演習](../2.3-projects)

[クリックして Ansible for Red Hat Enterprise Linux Workshop
に戻ります](../README.md#section-2---ansible-tower-exercises)
