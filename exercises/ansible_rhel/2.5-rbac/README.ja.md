# ワークショップ演習 - ロールベースのアクセス制御

**他の言語でもお読みいただけます**:
<br>![uk](../../../images/uk.png) [English](README.md)、![japan](../../../images/japan.png)[日本語](README.ja.md)、![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md)、![france](../../../images/fr.png) [Française](README.fr.md)、![Español](../../../images/col.png) [Español](README.es.md)

## 目次

* [目的](#目的)
* [ガイド](#ガイド)
* [Ansible 自動コントローラーユーザー](#ansible-自動コントローラーユーザー)
* [Ansible 自動コントローラーチーム](#ansible-自動コントローラーチーム)
* [パーミッションの付与](#パーミッションの付与)
* [パーミッションのテスト](#パーミッションのテスト)

## 目的

Ansible 自動コントローラーが認証情報をユーザーから分離する方法をすでに学習しました。Ansible 自動コントローラーのもう 1 つの利点は、ユーザーとグループの権利管理です。この演習では、役割ベースのアクセス制御 (RBAC) について説明します。

## ガイド

### Ansible 自動コントローラーユーザー

自動コントローラーユーザーには、以下の 3 つのタイプがあります。

* **Normal User (通常ユーザー)**: このユーザーには、適切なロールや権限が付与されているユーザーのインベントリーやプロジェクトに限定される読み取りおよび書き込みアクセスがあります。

* **System Auditor (システム監査者)**: この監査者は、自動コントローラー環境内のすべてのオブジェクトの読み取り専用機能を暗黙的に継承します。

* **System Administrator (システム管理者)**: このユーザーには、自動コントローラーインストール全体にわたる管理者、読み込み、書き込み特権があります。

ユーザーを作成しましょう。

* **Access** 下の自動化コントローラーメニューで、**Users** をクリックします。

* **追加** ボタンをクリックします。

* 新しいユーザーの値を入力します。

<table>
  <tr>
    <th>パラメーター</th>
    <th>値</th>
  </tr>
  <tr>
    <td>Username</td>
    <td>wweb</td>
  </tr>
  <tr>
    <td>Email</td>
    <td>wweb@example.com</td>
  </tr>
  <tr>
    <td>Password</td>
    <td>ansible</td>
  </tr>
  <tr>
    <td>Confirm Password</td>
    <td>ansible</td>
  </tr>
  <tr>
    <td>First Name</td>
    <td>Werner</td>
  </tr>
  <tr>
    <td>Last Name</td>
    <td>Web</td>
  </tr>
  <tr>
    <td>Organization</td>
    <td>Default</td>
  </tr>
  <tr>
    <td>User Type</td>
    <td>Normal User</td>
  </tr>
</table>

* **Save** をクリックします。

### Ansible 自動コントローラーチーム

Team (チーム) は、関連付けられたユーザー、プロジェクト、認証情報、およびパーミッションを持つ組織の下位区分のことです。チームは、ロールベースのアクセス制御スキームを実装し、組織全体で責任を委任する手段となります。たとえば、パーミッションは、チームの各ユーザーではなく、チーム全体に付与することができます。

チームの作成:

* メニューで **Access → Teams** に移動します。

* **Add** ボタンをクリックして、`Default` 組織内に `Web Content` という名前のチームを作成します。

* **Save** をクリックします。

ユーザーを Team に追加できるようになりました。

* チーム `Web Content` をクリックし、**Access** タブをクリックして **Add** をクリックします。

* **Select a Resource Type** ウィンドウで、**Users** リソースタイプをクリックし、**Next** をクリックします。

* **Select Items from List** で、`wweb` ユーザーの横にあるチェックボックスを選択し、**Next** をクリックします。

* **Select Roles to Apply** で、`wweb` ユーザーに適用するロールとして **Member** を選択します。

**保存** をクリックします。

パーミッションにより、プロジェクト、インベントリ、およびその他の自動コントローラー要素の読み取り、変更、および管理が可能になります。さまざまなリソースにパーミッションを設定できます。

### パーミッションの付与

ユーザーまたはチームが実際に何かを実行できるようにするには、パーミッションを設定する必要があります。ユーザー** wweb **は、割り当てられた Web サーバーのコンテンツのみを変更できるようにする必要があります。

`Create index.html` テンプレートを使用するためのパーミッションを追加します。

* **Resources** -> **Templates** 内で、`Create index.html` を選択します。

* メニューから **Access** タブを選択し、**Add** をクリックします。

* **Select a Resource Type** ウィンドウで、**Users** リソースタイプをクリックし、**Next** をクリックします。

* **Select Items from List** で、`wweb` ユーザーの横にあるチェックボックスを選択し、**Next** をクリックします。

* **Select Roles to Apply** で、`wweb` ユーザーに適用するロールとして**Read** と **Execute** を選択します。

* **Save** をクリックします。

### パーミッションのテスト

次に、自動コントローラーの Web UI からログアウトし、**wweb** ユーザーとして再度ログインします。

* **Templates** ビューに移動します。wweb については、`Create index.html` テンプレートが一覧表示されます。これはテンプレートを表示および起動することはできますが、編集することはできません。(Edit ボタンは利用できません)

* ロケットアイコンをクリックして、Job Template を実行します。好みに合わせて survey 内容を入力し、ジョブを開始します。

* 次の **Jobs** ビューでは、いろいろ見てください。ホストが変更される場所に注意してください。

結果の確認: コントロールホストで `curl` を再び実行し、`node1` の Web サーバーのコンテンツを取得します (`node2` や
`node3` も同様)。

```bash
#> curl http://node1
```

今行ったことを思い出してください。これで、制限されたユーザーが AnsiblePlaybook を実行できるようにしました

* 認証情報にアクセスせずに

* Playbook 自体を変更せずに

* 事前に定義した変数を変更できる状態で

事実上、認証情報を配布したり、ユーザーに自動化コードを変更する機能を与えたりすることなく、別のユーザーに自動化を実行する機能を提供しました。また、同時に、ユーザーは作成した survey に基づいて変更を加えることができます。

この機能は、Ansible 自動コントローラーの主な強みの1つです。

---
**ナビゲーション**
<br>
[前の演習](../2.4-surveys) - [次の演習](../2.6-workflows)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-2---ansible-tower-exercises)
