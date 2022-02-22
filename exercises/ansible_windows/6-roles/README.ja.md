**他の言語でもお読みいただけます**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![france](../../../images/fr.png) [Français](README.fr.md).
<br>

このワークショップを通して行ったように、1 つのファイルで Playbook
を作成することは可能です。ただし、最終的には複数のファイルを再利用して、整理することをお勧めします。

これを行うには、Ansible Roles を使用します。ロールを作成するときは、Playbook
を複数のパーツに分け、それらのパーツをディレクトリー構造に配置します。これはベストプラクティスとして考えられており、将来多くの時間を節約することができます。

この演習では、作成したばかりの Playbook を使用して、ロールにリファクタリングします。

まず、iis-basic-playbook がどのように役割に分解されるかを見てみましょう...

セクション 1: 新しい役割のディレクトリー構造の作成
=========================================================================

ステップ 1
--------------

Visual Studio Code で、エクスプローラーと、以前に作成した `iis_advanced` *WORKSHOP_PROJECT*
セクションに移動します。

![iis\_advanced](images/6-vscode-existing-folders.png)

**iis_advanced** フォルダーを選択します。

**iis_advanced** を右クリックし、*New Folder* を選択して、**roles** というディレクトリーを作成します。

次に、**role** を右クリックして、その下に `iis_simple` という名前の新しいフォルダーを作成します。

ステップ 2
--------------

*iis\_simple* 内に、次のように新しいフォルダーを作成します。

* defaults

* vars

* handlers

* tasks

* templates

ステップ 3
--------------

これら各新しいフォルダー (テンプレートを除く) で、右クリックして *New File* を作成します。これらの各フォルダーに `main.yml`
というファイルを作成します。個別のテンプレートファイルを作成するため、テンプレートではこれを行いません。これは基本的なロール構造であり、main.yml
はロールが各セクションで使用するデフォルトのファイルになります。

完成した構造は次のようになります。

![ロール構造](images/6-create-role.png)

セクション 2: `site.yml` Playbook を、新しく作成された `iis_simple` ロールに分割
=====================================================================================================

このセクションでは、`vars:`、`tasks:`、`template:`、`handlers:` などの Playbook の主要部分を分離します。

ステップ 1
--------------

`site.yml` のバックアップコピーを作成してから、新しい `site.yml` を作成します。

`iis_advanced` ディレクトリーに移動し、`site.yml` を右クリックして `rename` をクリックし、これを
`site.yml.backup` と指定します。

同じフォルダーに `site.yml` という名前の空の新しいファイルを作成します

ステップ 2
--------------

site.yml を更新して、自分のロールのみを呼び出すようにします。以下のようになります。

```yaml
    ---
    - hosts: windows
      name: This is my role-based playbook

      roles:
        - iis_simple
```

![新しい site.yml](images/6-new-site.png)

ステップ 3
--------------

デフォルト変数をロールに追加します。以下のように `roles\iis_simple\defaults\main.yml` を編集します。

```yaml
    ---
    # defaults file for iis_simple
    iis_sites:
      - name: 'Ansible Playbook Test'
        port: '8080'
        path: 'C:\sites\playbooktest'
      - name: 'Ansible Playbook Test 2'
        port: '8081'
        path: 'C:\sites\playbooktest2'
```

ステップ 4
--------------

`roles\iis_simple\vars\main.yml` のロールにいくつかのロール固有の変数を追加します。

```yaml
    ---
    # vars file for iis_simple
    iis_test_message: "Hello World!  My test IIS Server"
```

> **注意**
>
> **では...、2 つの別々の場所に、変数を配置しました。**
>
> そうです。変数は、さまざまな場所に配置して使用できます。
> いくつか例を挙げます。
>
> * vars ディレクトリー
> * defaults ディレクトリー
> * group\_vars ディレクトリー
> * Playbook の `vars:` セクション
> * `--extra_vars` オプションを使用して、
>   コマンドラインで指定できるファイル
> * いなかのおばあちゃんのおうち *(ウソですので注意してください)*
>
> 詳しくは [変数
> 優先順位](https://docs.ansible.com/ansible/latest/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable) をお読みください。
> 変数と、優先順位を受け入れる場所の両方を
> 理解できます。この演習では、ロールのデフォルトを使用して
> いくつかの変数を定義します。これらは、発展させることができます。その後、
> デフォルトよりも優先度の高い `/vars` にいくつか変数を定義しました。
> これは、デフォルト変数として上書きできません。

ステップ 5
--------------

`roles\iis_simple\handlers\main.yml` にロールハンドラーを作成します。

```yaml
    ---
    # handlers file for iis_simple
    - name: restart iis service
      win_service:
        name: W3Svc
        state: restarted
        start_mode: auto
```

ステップ 6
--------------

`roles\iis_simple\tasks\main.yml` のロールにタスクを追加します。

<!-- {% raw %} -->

```yaml
    ---
    # tasks file for iis_simple

    - name: Install IIS
      win_feature:
        name: Web-Server
        state: present

    - name: Create site directory structure
      win_file:
        path: "{{ item.path }}"
        state: directory
      with_items: "{{ iis_sites }}"

    - name: Create IIS site
      win_iis_website:
        name: "{{ item.name }}"
        state: started
        port: "{{ item.port }}"
        physical_path: "{{ item.path }}"
      with_items: "{{ iis_sites }}"
      notify: restart iis service

    - name: Open port for site on the firewall
      win_firewall_rule:
        name: "iisport{{ item.port }}"
        enable: yes
        state: present
        localport: "{{ item.port }}"
        action: Allow
        direction: In
        protocol: Tcp
      with_items: "{{ iis_sites }}"

    - name: Template simple web site to iis_site_path as index.html
      win_template:
        src: 'index.html.j2'
        dest: '{{ item.path }}\index.html'
      with_items: "{{ iis_sites }}"

    - name: Show website addresses
      debug:
        msg: "{{ item }}"
      loop:
        - http://{{ ansible_host }}:8080
        - http://{{ ansible_host }}:8081
```

<!-- {% endraw %} -->

ステップ 7
--------------

index.html テンプレートを追加します。

`roles\iis_simple\templates` を右クリックして、以下のない用で `index.html.j2`
という新しいファイルを作成します。

<!-- {% raw %} -->

```html
    <html>
    <body>

      <p align=center><img src='http://docs.ansible.com/images/logo.png' align=center>
      <h1 align=center>{{ ansible_hostname }} --- {{ iis_test_message }}</h1>

    </body>
    </html>
```

<!-- {% endraw %} -->

この Playbook のベースレベルにはまだ *templates* フォルダーがあるので、ここで削除します。それを右クリックして、*Delete*
を選択します。

ステップ 8: コミット
----------------------------

File → Save All をクリックして、すべてのファイルが保存されるようにします。

以下に示すように、ソースコードアイコンをクリックします (1)。

`Adding iis_simple role` (2) のようなコミットメッセージを入力し、上のチェックボックスをクリックします (3)。

![Commit iis\_simple\_role](images/6-commit.png)

左下の青いバーにある `synchronize changes` ボタンをクリックします。これも問題なく戻るはずです。

セクション 3: 新しい Playbook の実行
===============================================

元の Playbook をロールに正常に分離したので、それを実行して、どのように機能するかを見てみましょう。演習 5
のテンプレートを再利用しているため、新しいテンプレートを作成する必要はありません。このテンプレートを再度実行すると、git
から自動的に更新され、新しい役割が開始されます。

ステップ 1
--------------

ジョブテンプレートを変更する前に、まずプロジェクトを再同期する必要があります。これを行います。

ステップ 2
--------------

テンプレートを選択します

> **注意**
>
> あるいは、ジョブテンプレートから移動していない場合
> 作成ページでは、下にスクロールして既存のすべてのジョブテンプレートを表示できます

ステップ 3
--------------

**IIS Advanced** ジョブテンプレートのロケットアイコン！[追加](images/at_launch_icon.png)
をクリックします。

ステップ 4
--------------

プロンプトが表示されたら、目的のテストメッセージを入力します

成功すると、標準出力は次の図のようになります。以前にサーバーを設定し、サービスは既に実行中であるため、ほとんどのタスクは OK
を返すことに注意してください。

![ジョブ出力](images/6-job-output.png)

ジョブが正常に完了すると、ジョブ出力の下部に Web サイトへの 2 つの URL が出力されます。それらがまだ機能していることを確認します。

セクション 5: レビュー
===============================

これで、`site.yml` という単一の役割を持つ完全な Playbook `iis_simple` ができました。Playbook
をロールに構造化する利点は、Playbook に再利用性を追加できるだけでなく、変数、タスク、テンプレートなどへの変更を簡素化できることです。

[Ansible Galaxy](https://galaxy.ansible.com) は、使用または参照するための役割の優れたリポジトリーです。

<br><br>
[Click here to return to the Ansible for Windows Workshop](../README.md)
