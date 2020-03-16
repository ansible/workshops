# 演習 3 - Playbook 概要

この演習では、初めての Ansible Playbook を書いてみましょう。 Playbook は、実際の作業を記述する **タスク** と、タスクの実行条件などを記述する **プレイ** のセットで構成されます。このセットは Playbook 内で繰り返すことも可能です。まず、プレイブックを保存するためのディレクトリ構造をセットアップします。このディレクトリ構造は、**ソースコード管理**(SCM)システムと同期して、Playbook のバージョンや品質を管理します。 この演習では、SCM として**Git**を使用します。  

Playbook には1つ以上のプレイがあり、プレイには1つまたは複数のタスクがあります。 **プレイ**の目的の1つは、タスクを実行するホストのグループを記述することです。 **タスク**の目標は、それらのホストに対してモジュールを実行することです。  

最初の Playbook では、1つのプレイと3つのタスクを記述します。  

今回の演習では、全ての Playbook は単一のGit **リポジトリ**に保存されています。Git の様な SCM は、複数のユーザーが同じリポジトリを使用できるため、Playbook の品質とバージョンを管理に有用です。Ansible Tower では簡単に SCM と連携する事が出来ます。  

## 概要

この演習では、エディターとして Visual Studio Code を使ってみましょう。さらに、ソースコード管理に GitLab を使用します。これにより、Linuxコマンドラインを理解していなくても開発作業が楽に行えます。他のエディターまたはソースコードソリューションを使用することももちろん可能です。  

### ステップ 1: プレイブックのディレクトリ構造とファイルの作成

Playbook のディレクトリ構造としては、ベストプラクティスがあります。  
[ベストプラクティス](http://docs.ansible.com/ansible/playbooks_best_practices.html)。  
Ansible の技術を習得する際には、上記を学習しておくことを強くお勧めします。とはいえ、この演習で利用する Playbook は非常に基本的なものですので複雑なディレクトリ構造は必要ありません。  

代わりに、非常にシンプルなディレクトリ構造を作成します。プレイブックを追加し、いくつかのファイルを追加します。  

### ステップ 2: Visual Studio Code への接続

Visual Studio Code を開きます。  

この演習では、あらかじめ各自の Git リポジトリはクローン済みです。  
VS Code へのアクセス先と認証情報を確認し接続を完了します。  

![VS Code Access](images/3-vscode-access.png)

Explorer サイドバーは、READMEファイルのみを含むWORKSHOP_PROJECT セクションとなっています。  

![Student Playbooks Repo](images/3-vscode-open-folder.png)

### ステップ 3: ディレクトリーと Playbook の作成

*WORKSHOP_PROJECT*セクションにカーソルを合わせ、*New Folder*ボタンをクリックします。  
`iis_basic`という名前のフォルダーを作成します。次に作成した新しいフォルダーを右クリックして、「install_iis.yml」というファイルを作成します。  

作成すると右ペインに編集可能なエディタが表示されます。ここに Playbook を記述していきます。♬  

![Empty install\_iis.yml](images/3-vscode-create-folders.png)

### ステップ 4: プレイの定義

`install_iis.yml`を編集します。まずプレイを記述してみましょう。  
次に、各行の意味をご説明します。  

```yaml
    ---
    - name: install the iis web service
      hosts: windows
```

- `---` YAMLであることを示しています。  

- `name: install the iis web service` プレイに対する名前です。  

- `hosts: windows` このプレイが実行されるインベントリ内のホストグループを定義します  

### ステップ 5: プレイに対するタスクの記述

次に、いくつかのタスクを追加します。（タスク）の**t**をhost`hosts`の**h**に（垂直に）位置合わせします。  
YAML ファイルではスペースはとても重要です。タブを使ってはいけません。  
Playbook 全体は一番下にありますので必要に応じてご参照ください。  

<!-- {% raw %} -->
```yaml
      tasks:
       - name: install iis
         win_feature:
           name: Web-Server
           state: present

       - name: start iis service
         win_service:
           name: W3Svc
           state: started

       - name: Create website index.html
         win_copy:
           content: "{{ iis_test_message }}"
           dest: C:\Inetpub\wwwroot\index.html

       - name: Show website address
         debug:
           msg: "http://{{ ansible_host }}"
```
<!-- {% endraw %} -->

- `tasks:` タスクが記述されていることを示しています。  

- `- name:` プレイブックの実行時に標準出力に表示される名前です。短くて分かりやすい名前が良いと思います。♬

<!-- -->

```yaml
    win_feature:
      name: Web-Server
      state: present
```

- 上記 3 行は、Ansible モジュール**`win_feature`**　を使って IIS Web サーバーをインストールしています。`win_feature` モジュールのすべてのオプションを表示します。win_feature モジュール詳細は下記参照ください。  
[Click here](http://docs.ansible.com/ansible/latest/win_feature_module.html)

<!-- -->
```yaml
    win_service:
      name: W3Svc
      state: started
```

- 続くいくつかの行で、Ansible モジュール **win_service** を使って IIS サービスを起動しています。この win_service モジュールは windows ホストのサービス管理するために有用なモジュールです。win_service モジュール詳細は下記参照ください。  
 [Click here](http://docs.ansible.com/ansible/latest/win_service_module.html)

<!-- {% raw %} -->
```yaml
    win_copy:
      content: "{{ iis_test_message }}"
      dest: C:\Inetpub\wwwroot\index.html
```
<!-- {% endraw %} -->

- このタスクでは、win_copy モジュールを使用して、特定のコンテンツを含むファイルを作成します。 ここでは、変数を使用してコンテンツを取得しているため、もう少し複雑になっています。変数については、後のレッスンで説明いたします。ここではAnsible ホストから リモートホストに index.html としてファイルをコピーしていることだけ理解いただければ大丈夫です！    

<!-- {% raw %} -->
```yaml
    debug:
      msg: http://{{ ansible_host }}
```
<!-- {% endraw %} -->

- This task uses the `debug` module to post a message at the end of playbook execution. This particular message prints out `http://` + the variable name that contains the IP address of the host we're running the playbook on (our Windows IIS server)


### ステップ 6: Playbook の保存

Playbook の記述が完了しましたので、保存しましょう。  
左上から `File > Save` をクリックします。  

And that should do it. You should now have a fully written playbook
called `install_iis.yml`.

でもまだ終わってません！！！ **ローカル**コピーから**git**への変更（コミット）が必要です。以下に示すように、[Source Code]アイコンをクリックします（ページの一番左の中央にある青い円に\＃1が含まれています）

![Git Commit](images/3-vscode-click-commit.png)

サイドバーの上部にあるテキストボックスに*Adding install _iis.yml* などのコミットメッセージを入力した上で、上部ののチェックボックスをクリックしてコミットします。このメッセージは、バージョンを比較するときに他の人（自分を含む）が何が変更されているかをよりよく理解できるように、行った変更を説明することを目的としています。  

![Git Commit install\_iis.yml](images/3-vscode-commit.png)

次に、コミットした変更をリポジトリにプッシュする必要があります。  

左下の青いバーで、円形矢印を含むセクションをクリックして、変更をプッシュします。  

![Git Push Origin](images/3-vscode-push.png)

プッシュするのに30秒程度かかる場合があります。 最初のプッシュの後、git fetch を定期的に実行するかどうかを尋ねるポップアップメッセージが表示される場合があります。**Yes** or **No** どちらを選択いただいてもかまいません。  

![Git Push Origin](images/3-vscode-push-initial-pop-up.png)

コードがgitにあることを検証したい場合は、GitLabに接続して確認してみましょう。  

![GitLab access](images/3-vscode-gitlab-access.png)

これであなたは、自動化の準備が整いました♬  

> **Note**
>
> Ansible（実際、YAML）は、特にインデント/スペースの周りの書式設定に少しこだわりがあります。YAML の書き方は、[こちら](http://docs.ansible.com/ansible/YAMLSyntax.html)をご確認ください。  
上記で完成したプレイブックは次のようになります。スペースに特に注意してください。

<!-- {% raw %} -->
```yaml
    ---
    - name: install the iis web service
      hosts: windows

      tasks:
        - name: install iis
          win_feature:
            name: Web-Server
            state: present

        - name: start iis service
          win_service:
            name: W3Svc
            state: started

        - name: Create website index.html
          win_copy:
            content: "{{ iis_test_message }}"
            dest: C:\Inetpub\wwwroot\index.html

        - name: Show website address
          debug:
            msg: http://{{ ansible_host }}
```
<!-- {% endraw %} -->

[ワークショップ一覧に戻る](../readme.ja.md)
