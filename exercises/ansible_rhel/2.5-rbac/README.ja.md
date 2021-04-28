# ワークショップ演習 - ロールベースのアクセス制御

**その他の言語はこちらをお読みください。**
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

## 目次

* [目的](#objective)
* [ガイド](#guide)
* [Ansible Tower ユーザー](#ansible-tower-users)
* [Ansible Tower チーム](#ansible-tower-teams)
* [パーミッションの付与](#granting-permissions)
* [パーミッションのテスト]（＃test-permissions）

## 目的

AnsibleTower が認証情報をユーザーから分離する方法をすでに学習しました。Ansible Tower のもう 1
つの利点は、ユーザーとグループの権利管理です。この演習では、役割ベースのアクセス制御 (RBAC) について説明します。

## ガイド

### Ansible Tower ユーザー

Tower ユーザーには 3 つのタイプがあります。

* **Normal User (通常ユーザー)**:
  このユーザーには、適切なロールや権限が付与されているユーザーのインベントリーやプロジェクトに限定される読み取りおよび書き込みアクセスがあります。

* **System Auditor (システム監査者)**: この監査者は、Tower
  環境内のすべてのオブジェクトの読み取り専用機能を暗黙的に継承します。

* **System Administrator (システム管理者)**: このユーザーには、Tower
  インストール全体にわたる管理者、読み込み、書き込み特権があります。

ユーザーを作成しましょう。

* **ACCESS** の Tower メニューで、**Users** をクリックします。

* 緑のプラスボタンをクリックします。

* 新しいユーザーの値を入力します。

<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>FIRST NAME </td>
    <td>Werner</td>
  </tr>
  <tr>
    <td>LAST NAME</td>
    <td>Web</td>
  </tr>
  <tr>
    <td>Organization</td>
    <td>Default</td>
  </tr>
  <tr>
    <td>EMAIL</td>
    <td>wweb@example.com</td>
  </tr>
  <tr>
    <td>USERNAME</td>
    <td>wweb</td>
  </tr>
  <tr>
    <td>PASSWORD</td>
    <td>ansible</td>
  </tr>
  <tr>
    <td>CONFIRM PASSWORD</td>
    <td>ansible</td>
  </tr>
  <tr>
    <td>USER TYPE</td>
    <td>Normal User</td>
  </tr>
</table>

* パスワードの確認

* **SAVE** をクリックします。

### Ansible Tower Team

Team (チーム)
は、関連付けられたユーザー、プロジェクト、認証情報、およびパーミッションを持つ組織の下位区分のことです。チームは、ロールベースのアクセス制御スキームを実装し、組織全体で責任を委任する手段となります。たとえば、パーミッションは、チームの各ユーザーではなく、チーム全体に付与することができます。

チームの作成:

* メニューで **ACCESS → Teams** に移動します。

* 緑のプラスボタンをクリックして、`Web Content` というチームを作成します。

* **SAVE** をクリックします。

ユーザーを Team に追加できるようになりました。

* **USERS** ボタンをクリックして、`Web Content` Team の User ビューに切り替えます。

* 緑プラスボタンをクリックして、`wweb` ユーザーの隣のボックスにチェックを入れ、**SAVE** をクリックします。

**TEAMS** ビューの **PERMISSIONS** ボタンをクリックすると、「パーミッションが付与されていません」(No
Permissions Have Been Granted) というメッセージが表示されます。

パーミッションにより、プロジェクト、インベントリ、およびその他の Tower
要素の読み取り、変更、および管理が可能になります。さまざまなリソースにパーミッションを設定できます。

### パーミッションの付与

ユーザーまたはチームが実際に何かを実行できるようにするには、パーミッションを設定する必要があります。ユーザー **wweb** は、割り当てられた
Web サーバーのコンテンツのみを変更できるようにする必要があります。

テンプレートを使用するためのパーミッションを追加します。

* Team `Web Content` の Permission ビューで、緑色のプラスボタンをクリックして、権限を追加します。

* 新しいウィンドウが開きます。多数のリソースの権限を設定することを選択できます。

  * リソースタイプ **JOB TEMPLATES** を選択します。

  * 隣のボックスをチェックして `Create index.html` Template を選択します。

* ウィンドウの次の部分が開きます。ここでは、選択したリソースにロールを割り当てます。

  * **EXECUTE** を選択します。

* **SAVE** をクリックします。

### パーミッションのテスト

次に、Tower の Web UI からログアウトし、**wweb** ユーザーとして再度ログインします。

* **Templates** ビューに移動します。wweb については、`Create index.html`
  テンプレートが一覧表示されます。これはテンプレートを表示および起動することはできますが、編集することはできません。テンプレートを開いて変更してみてください。

* ロケットアイコンをクリックして、Job Template を実行します。好みに合わせて survey 内容を入力し、ジョブを開始します。

* 次の **Jobs** ビューでは、いろいろ見てください。ホストが変更される場所に注意してください。

結果の確認: コントロールホストで `curl` を再び実行し、`node1` の IP アドレス上の Web サーバーのコンテンツを取得します
(`node2` や `node3` も同様)。

```bash
#> curl http://22.33.44.55
```

今行ったことを思い出してください。これで、制限されたユーザーが AnsiblePlaybook を実行できるようにしました

* 認証情報にアクセスせずに

* Playbook 自体を変更せずに

* 事前に定義した変数を変更できる状態で

事実上、認証情報を配布したり、ユーザーに自動化コードを変更する機能を与えたりすることなく、別のユーザーに自動化を実行する機能を提供しました。また、同時に、ユーザーは作成した
survey に基づいて変更を加えることができます。

この機能は、Ansible Tower の主な強みの1つです。

---
**ナビゲーション**
<br>
[前の演習](../2.4-surveys) - [次の演習](../2.6-workflows)

[クリックして Ansible for Red Hat Enterprise Linux Workshop
に戻ります](../README.md#section-2---ansible-tower-exercises)
