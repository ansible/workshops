**他の言語でもお読みいただけます**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![france](../../../images/fr.png) [Français](README.fr.md).
<br>

前の演習では、Ansible Playbook の基本を説明しました。次のいくつかの演習では、自動化に柔軟性とパワーを追加する、より高度な
ansible スキルをいくつか紹介します。

Ansible の存在意義は、タスクをシンプルかつ繰り返し可能にすることです。すべてのシステムが完全に同じであるとは限らず、Ansible
Playbook の実行の仕組みを少し変更しなければならいことは理解しています。そこで変数を使用します。

変数は、システム間の違いに対処する方法です。これにより、ポート、IP アドレス、またはディレクトリーなどの変更を考慮に入れることができます。

ループでは、同じタスクを何度も繰り返すことができます。たとえば、複数のサービスの起動、複数の機能のインストール、複数のディレクトリーの作成を行いたいとします。Ansible
ループを使用することで、1 つのタスクでこれらすべてを行うことができます。

ハンドラーは、サービスを再起動する方法です。新しい設定ファイルをデプロイし、新しいパッケージをインストールしましたでしょうか。その場合、これらの変更を有効にするためにサービスの再起動が必要となる場合があります。これはハンドラーを使用して行います。

変数、ループ、ハンドラーの詳細については、これらのテーマに関する Ansible のドキュメントをご覧ください。  [Ansible
Variables](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html
[Ansible
Loops](https://docs.ansible.com/ansible/latest/user_guide/playbooks_loops.html
[Ansible
Handlers](https://docs.ansible.com/ansible/latest/user_guide/playbooks_handlers.html#handlers

セクション 1: Playbook の作成
=====================================

まず、新しい Playbook を作成しますが、演習 3 で作成したものに非常によく似ていると思います。

ステップ 1
--------------

Visual Studio Code 内で、git リポジトリーに新しいディレクトリーを作成し、site.yml ファイルを作成します。

Explorer で、以前に `iis_basic` を作成した場所に *WORKSHOP_PROJECT* セクションがあるはずです。

![学習者 Playbooks](images/5-vscode-existing-folders.png)

ステップ 2: **iis_advanced** というフォルダーと `site.yml` というファイルを作成します
------------------------------------------------------------------------

*WORKSHOP_PROJECT* セクションにカーソルを合わせ、*New Folder* ボタンをクリックします。

`iis_advanced` と入力し、Enter キーを押します。次に、そのフォルダーをクリックして選択します。

`iis_advanced` フォルダーを右クリックし、*New File* を選択します。

`site.yml` と入力し、Enter キーを押します。

これで、Playbook の作成に使用できるエディターが右側のペインで開いているはずです。

![Empty site.yml](images/5-vscode-create-folders.png)

ステップ 3
--------------

プレイ定義といくつかの変数を Playbook に追加します。これらには、Playbook が Web
サーバーにインストールする追加のパッケージに加えて、いくつかの Web サーバー固有の設定が含まれます。

```yaml
---
- name: This is a play within a playbook
  hosts: windows
  vars:
    iis_sites:
      - name: 'Ansible Playbook Test'
        port: '8080'
        path: 'C:\sites\playbooktest'
      - name: 'Ansible Playbook Test 2'
        port: '8081'
        path: 'C:\sites\playbooktest2'
    iis_test_message: "Hello World!  My test IIS Server"
```

ステップ 4
--------------

**install IIS** という新しいタスクを追加します。Playbook を作成したら `File` &gt; `Save`
をクリックして変更を保存します。

<!-- {% raw %} -->

```yaml
  tasks:
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
```

<!-- {% endraw %} -->

![site.yml part 1](images/5-vscode-iis-yaml.png)

> **注意**
>
> **ここで起きていることを説明します。**
>
> - `vars:` Ansible に、次のものが
>  変数名であることを指示しています。
>
> - `iis_sites`: iis \ _sites というリストタイプの変数を定義しています
>   これに続くのは、関連した変数を持つ各サイトの
>   リストです
>
> - `win_file:`: このモジュールは、ファイル、ディレクトリー、シンボリックリンクの作成、変更、削除に
>   使用されます。
>
>  - `{{ item }}` これがリストアイテムに広がることを Ansible に伝えています
>   各アイテムには、`name`、`port`、`path` などの
>   いくつかの変数があります。
>
> - `with_items: "{{ iis_sites }}` これは、
>   Ansible に、`iis_sites` においてすべての `item` に、このタスクを実行するように指示する
>   ループです。
>
> - `notify: restart iis service` このステートメントは `handler` なので、
>   セクション 3 で説明します。

セクション 2: ファイアウォールを開いてファイルを展開する
==================================================================================

その後、IIS サービスを開始するタスクを定義します。

ステップ 1
--------------

プロジェクトディレクトリーに `templates` ディレクトリーを作成し、次のようにテンプレートを作成します。

** iis_advanced folder** が強調表示されていることを確認してから、*WORKSHOP_PROJECT*
セクションにカーソルを合わせ、*New Folder* ボタンをクリックします。

`templates` と入力し、Enter キーを押します。*templates* フォルダーを右クリックし、*New File*
ボタンをクリックします。

`index.html.j2` と入力し、Enter キーを押します。

これで、テンプレートの作成に使用できるエディターが右側のペインで開いているはずです。次の詳細を入力します。

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

![index.html template](images/5-vscode-template.png)

ステップ 2
--------------

ファイアウォールポートを開いてテンプレートを作成することにより、Playbook `site.yml`
を編集し直します。スラッシュをエスケープしないように、`win_template` には一重引用符を使用してください。

<!-- {% raw %} -->

```yaml
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

> **注意**
>
> **では、実際に書いたものを詳しく見ていきます。**
>
> - `win_firewall_rule:` このモジュールは、ファイアフォールルールの作成、変更、および
>   更新に使用されます。AWS の場合は、次の点にも注意してください。
>   通信に影響を与える可能性のあるセキュリティグループルール。この例では、
>   そのポートのルールを開きました。
>
> - `win_template:` このモジュールは、jinja2 テンプレートが
>   使用およびデプロイされていることを指定します。
>
> - テンプレート式内 (フィルター) のデータを変換するために
> Ansible で使用されます。
>
> - `debug:` 繰り返しになりますが、`iis_basic` Playbook のように、このタスクは、この演習用に作成しているサイトにアクセスするための URL を表示します

セクション 3: ハンドラーの定義と使用
====================================================

設定ファイルのデプロイ、新しいパッケージのインストールなど、サービス/プロセスを再起動する必要がある理由はいくつもあります。このセクションには、実際には
2 つのパートがあります。Playbook にハンドラーを追加し、タスクの後にハンドラーを呼び出します。前者から始めます。

`handlers` ブロックは、1 レベルのインデント、つまり 2 つのスペースの後に開始する必要があります。`tasks`
ブロックと整列する必要があります。

ステップ 1
--------------

ハンドラーを定義します。

```yaml
  handlers:
    - name: restart iis service
      win_service:
        name: W3Svc
        state: restarted
        start_mode: auto
```

> **注意**
>
> **後者を語らずして、前者を始めることはできません。**
>
> - `handler:` これは **play** に `tasks:` が
>   終了していて、`handlers:` を定義していることを指示します。その下のすべては、
>   他のタスクと同じように見えます。つまり、名前、
>   モジュール、およびそのモジュールのオプションを指定します。これが、ハンドラーの
>   定義です。
>
> - `notify: restart iis service` ...そして、ここからがようやく後者の部分です。
>   `notify` ステートメントは、名前によるハンドラーの呼び出しです。
>   明らかですね。
>   `win_iis_website` タスクに `notify` ステートメントを追加したことには既にお気づきでしょう。
>   これがその理由です。

セクション 4: コミットとレビュー
==============================================

新しく改良された Playbook が完成しました。ただし、ソースコード管理への変更をコミットする必要があることを忘れないでください。

`File` → `Save All` をクリックして、書き込んだファイルを保存します

![site.yml part 2](images/5-vscode-iis-yaml.png)

ソースコードアイコン (1) をクリックし、*Adding advanced playbook* (2)
などのコミットメッセージを入力して、上のチェックボックス (3) をクリックします。

![Commit site.yml](images/5-commit.png)

左下の青いバーの矢印をクリックして、gitlab に同期します。プロンプトが表示されたら、`OK` をクリックしてコミットをプッシュおよびプルします。

![Push to Gitlab.yml](images/5-push.png)

コミットが完了するまで 5〜30 秒かかります。青いバーは回転を停止し、問題がないことを示しています...。

今一度、自分の意図した通りになっているかどうかを確認してみましょう。もしそうでなければ、今こそ修正する時です。以下の playbook
は正常に実行されるはずです。

<!-- {% raw %} -->

```yaml
---
- hosts: windows
  name: This is a play within a playbook
  vars:
    iis_sites:
      - name: 'Ansible Playbook Test'
        port: '8080'
        path: 'C:\sites\playbooktest'
      - name: 'Ansible Playbook Test 2'
        port: '8081'
        path: 'C:\sites\playbooktest2'
    iis_test_message: "Hello World!  My test IIS Server"

  tasks:
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

  handlers:
    - name: restart iis service
      win_service:
        name: W3Svc
        state: restarted
        start_mode: auto
```

<!-- {% endraw %} -->

セクション 5: ジョブテンプレートの作成
=======================================================

ステップ 1
--------------

ジョブテンプレートを作成する前に、まずプロジェクトを再同期する必要があります。これを行います。

> **注意**
>
> ジョブテンプレートから選択する新しい *ベース* Playbook ファイルを作成するときは、
> 常にこれを行う必要があります。新しいファイルは、
> ジョブテンプレート Playbook ドロップダウンで利用可能になる前に Controller に
> 同期する必要があります。

ステップ 2
--------------

この Playbook をテストするには、この Playbook
を実行するための新しいジョブテンプレートを作成する必要があります。したがって、*Template* に移動し、*Add* をクリックして、`Job
Template` を選択し、2 番目のジョブテンプレートを作成します。

次の値を使用してフォームに記入します

| Key         | Value                      | Note |
|-------------|----------------------------|------|
| Name        | IIS Advanced               |      |
| Description | Template for iis_advanced  |      |
| Job Type    | Run                        |      |
| Inventory   | Workshop Inventory |      |
| Execution Environment     | windows workshop execution environment   |      |
| Project     | Ansible Workshop Project   |      |
| Playbook    | `iis_advanced/site.yml`    |      |
| Credentials  | Workshop Credential            |      |
| OPTIONS     | [\*] Enable Fact Storage         |      |

ステップ 3
--------------

SAVE ![保存](images/at_save.png) をクリックし、以下のページで **Survey** タブを選択します。

ステップ 4
--------------

以下の値を使用して新規 survey を作成します。

| Key                    | Value                                                    | Note |
|------------------------|----------------------------------------------------------|------|
| Question               | Please enter a test message for your new website         |      |
| Description            | Website test message prompt                              |      |
| Answer Variable Name   | `iis_test_message`                                       |      |
| Answer Type            | Text                                                     |      |
| Minimum/Maximum Length | Keep the defaults                                        |      |
| Default Answer         | Be creative, keep it clean, we’re all professionals here |      |

![Survey ファーム](images/5-survey.png)

ステップ 5
--------------

SAVE ![追加](images/at_save.png) を選択し、**On** スイッチを入れることを忘れないでください ![On
switch](images/controller_on.png) を選択します。


セクション 6: 新しいプレイブックの実行
=======================================================

それを実行して、どのように機能するかを見てみましょう。

ステップ 1
--------------

テンプレートを選択します

> **注意**
>
> あるいは、ジョブテンプレートから移動していない場合
> 作成ページでは、下にスクロールして既存のすべてのジョブテンプレートを表示できます

ステップ 2
--------------

**IIS Advanced** ジョブテンプレートのロケットアイコン！[追加](images/at_launch_icon.png)
をクリックします。

ステップ 3
--------------

プロンプトが表示されたら、目的のテストメッセージを入力します

起動後、リダイレクトされ、ジョブの出力をリアルタイムで監視できます。

ジョブが正常に完了すると、ジョブ出力の下部に Web サイトへの 2 つの URL が出力されます。

![Job output](images/5-job-output.png)

<br><br>
[Click here to return to the Ansible for Windows Workshop](../README.md)
