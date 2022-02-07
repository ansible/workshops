**他の言語でもお読みいただけます**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).
<br>

この演習は、Ansible が Chocolatey を使用した Windows
ソフトウェアの管理のすべての側面を簡単に制御できるようにする方法を紹介することを目的としています。パッケージのインストール、更新、アンインストール、さまざまなソースの管理、chocolatey
クライアントの構成、およびシステム管理者が実行するその他の一般的なタスクについて説明します。

Chocolatey とは何でしょうか。簡単に言えば、Chocolatey は Windows 用のパッケージ管理システムです。Chocolatey
は、ソフトウェア管理を簡素化し、Windows ソフトウェアライフサイクル全体の自動化を容易にすることを目的としています。

オープンソースの Chocolatey クライアントは基本的なパッケージ管理機能を提供し、Chocolatey For Business
スイートは高度な機能セットを提供します。いくつかのハイライトを次に示します。

* Package Builder を使用すると、EXE、MSI、zip、またはスクリプトを取得して、わずか 5 秒で自動的に Chocolatey
  パッケージに変換できます (インストーラーのサイレント引数を把握できます)。
* Package Internalizer は、メンテナが Chocolatey Community Repository で既に構築した 8000
  以上のパッケージを取得し、内部で使用するためのローカライズされたオフラインバージョンを作成します (依存関係を含む)。
* Package Synchronizer を使用すると、Programs and Features
  にリストされているアプリケーション用のChocolatey パッケージを作成し、他のパッケージと同じように管理できます。
* Chocolatey セルフサービス GUI を使用すると、エンドユーザーは管理者権限や昇格された権限を必要とせずにパッケージを管理できます。
* Chocolatey Central Management は、Web ダッシュボードと API (Automation Controller
  に類似) であり、エンドポイントの資産全体の高レベルの概要とレポートを提供します。

*************************************************************************************************

# セクション 1: `win_chocolatey` モジュール

## ステップ 1: アドホックコマンドを使用してパッケージをインストールする

まず、アドホックコマンドを使用して、`win_chocolatey` モジュールを使用して `git` をインストールします。`win_chocolatey` モジュールは、Chocolatey を使用して Windows システム上のパッケージを管理するために使用されます。
<br>
まず、左側のパネルの **Inventories** をクリックしてから、インベントリー **Workshop Inventory** の名前をクリックします。Inventory Details ページが表示されたので、ホストを選択する必要があります。したがって、**HOSTS** をクリックします。

各ホストの横にはチェックボックスがあります。アドホックコマンドを実行する各ホストの横にあるチェックボックスをオンにします。次に、**RUN
COMMANDS** ボタンが有効になります。今すぐクリックしてください。

![Run Command](images/8-chocolatey-run-command.png)

これにより、**Execute Command** ウィンドウがポップアップ表示されます。ここから、ホストに対して単一のタスクを実行できます。

このフォームに次のように記入します。

| Key                | Value                    | Note                                                            |
|--------------------|--------------------------|-----------------------------------------------------------------|
| MODULE             | `win_chocolatey`         |                                                                 |
| ARGUMENTS          | `name=git state=present` | The name and state of the package                               |
| LIMIT              |                          | This will be pre-filled out for you with the hosts you selected |
| MACHINE CREDENTIAL |Student Account     |                                                                 |

![Run Win\_Chocolatey](images/8-chocolatey-run-win_chocolatey.png)

**LAUNCH** をクリックすると、ジョブログにリダイレクトされます。

ジョブの出力には、次のような結果が表示されます。

![Win\_Chocolatey Job
Output](images/8-chocolatey-run-win_chocolatey-result.png)

出力は、`git` がインストールされたことを示す CHANGED ステータスを報告していることがわかります。結果には、Chocolatey
クライアントがシステムにないという警告も表示されるため、このタスク実行の一部としてインストールされました。`win_chocolatey`
モジュールを使用する将来のタスクは、クライアントを検出し、何もインストールせずに使用する必要があります。確認するには、**DETAILS**
セクションのロケットアイコンをクリックしてジョブを再実行します。出力に警告が表示されず、変更も報告されません。ただし、`win_chocolatey`
(多くの Ansible モジュールと同様) モジュールが冪等 (以前の実行が 2
つのパッケージをインストールしましたが、これはなにもインストールしないため、実行時間は短くなります) であるため、代わりに SUCCESS
ステータスが報告されます。

![Win\_Chocolatey re run Job
Output](images/8-chocolatey-rerun-win_chocolatey-result.png)

そのようにして、`git` がインストールされています。

## ステップ 2: 特定のバージョンの複数のパッケージをインストールする

最後のステップでは、アドホックな方法で 1 つのパッケージをインストールしました。ただし、実際には、マルチステッププレイの 1
つのステップとしてパッケージのインストールを含めることをお勧めします。また、複数のパッケージ (場合によってはそのパッケージの特定のバージョン)
をインストールすることも考えられます。この演習では、これを行います。

まずは Visual StudioCode に戻ります。*WORKSHOP_PROJECT* セクションの下に **chocolatey**
というディレクトリーと `install_packages.yml` というファイルを作成します。

これで、Playbook の作成に使用できるエディターが右側のペインで開いているはずです。

<!-- TODO: INSERT Image of Empty text editor here-->
<!-- ![Empty install\_packages.yml](images/8-vscode-create-install_playbook.png) -->
![Empty install\_packages.yml](images/8-chocolatey-empty-install_packages-editor.png)

まず、プレイを定義します。

```yaml
---
- name: Install Specific versions of packages using Chocolatey
  hosts: all
  gather_facts: false
  vars:
    choco_packages:
      - name: nodejs
        version: 13.0.0
      - name: python
        version: 3.6.0
```

Ansible によって収集されたファクトは必要ないか使用しないため、オーバーヘッドを減らすために `gather_facts: false`
を設定してファクト収集を無効にしました。また、Chocolatey を使用してインストールするパッケージの名前とバージョンを保持するために、`vars`
ディレクティブの下に `choco_packages` という名前の1つの辞書変数を定義しました。

次に、タスクを追加します。

{% raw %}
```yaml
  tasks:

  - name: Install specific versions of packages sequentially
    win_chocolatey:
      name: "{{ item.name }}"
      version: "{{ item.version }}"
    loop: "{{ choco_packages }}"

  - name: Check python version
    win_command: python --version
    register: check_python_version

  - name: Check nodejs version
    win_command: node --version
    register: check_node_version

  - debug:
      msg: Python Version is {{ check_python_version.stdout_lines[0] }} and NodeJS version is {{ check_node_version.stdout_lines[0] }}
```
{% endraw %}

タスクセクションに 4 つのタスクを追加しました。

* 最初のタスクは `win_chocolatey` モジュールを使用し、`choco_packages`
  変数をループして、指定されたバージョンの各製品をインストールします
* 2 番目と 3 番目のタスクは、`win_command` モジュールを使用してコマンドを実行し、それぞれ `python` と `node`
  のバージョンをチェックして、それぞれの出力を登録します。
* 4 番目の最後のタスクでは、`debug` モジュールを使用して、手順 2 と 3 で収集した情報を含むメッセージを表示しました。

> **ヒント**
>
> `win_chocolatey` モジュールの `name` 属性は、実際にはループの必要性を回避してパッケージのリストを取得できますが、ループを使用すると、各パッケージのバージョンを指定し、順序が適切な場合はそれらを順番にインストールできます。`win_chocolatey` モジュールの詳細は、[docs](https://docs.ansible.com/ansible/latest/collections/chocolatey/chocolatey/win_chocolatey_module.html を参照してください。

完成した Playbook `install_packages.yml` は次のようになります。

{% raw %}
```yaml
---
- name: Install Specific versions of packages using Chocolatey
  hosts: all
  gather_facts: false
  vars:
    choco_packages:
      - name: nodejs
        version: 13.0.0
      - name: python
        version: 3.6.0
  tasks:

  - name: Install specific versions of packages sequentially
    win_chocolatey:
      name: "{{ item.name }}"
      version: "{{ item.version }}"
    loop: "{{ choco_packages }}"

  - name: Check python version
    win_command: python --version
    register: check_python_version

  - name: Check nodejs version
    win_command: node --version
    register: check_node_version

  - debug:
      msg: Python Version is {{ check_python_version.stdout_lines[0] }} and NodeJS version is {{ check_node_version.stdout_lines[0] }}
```
{% endraw %}

これで Playbook の準備ができました。

* メニューから `File > Save` をクリックして (または Ctrl+S で) 作業内容を保存します。
* 変更を git にコミットします。*Adding install\_packages.yml* などの関連するコミットメッセージを使用します。
* 円形の矢印をクリックして、コミットされた変更をリポジトリにプッシュします。
* (オプション) **GitLab Access** の下の情報を使用して GitLab に移動し、コードが git であることを確認します。

次に、Automation Controller に戻り、プロジェクトを同期して、Controller が新しい Playbook
を使うようにします。**Projects** をクリックしてから、プロジェクトの横にある同期アイコンをクリックします。

![プロジェクトの同期](images/8-project-sync.png)

これが完了したら、新しいジョブテンプレートを作成します。**Templates** を選択し、![追加](images/add.png)
アイコンをクリックして、ジョブテンプレートを選択します。新しいテンプレートには次の値を使用します。

| Key         | Value                                            | Note |
|-------------|--------------------------------------------------|------|
| Name        | Chocolatey - Install Packages                    |      |
| Description | Template for the install_packages playbook       |      |
| JOB TYPE    | Run                                              |      |
| INVENTORY   | Workshop Inventory                               |      |
| PROJECT     | Ansible Workshop Project                         |      |
| PLAYBOOK    | `chocolatey/install_packages.yml`                |      |
| CREDENTIAL  | Type: **Machine**. Name: **Student Account**     |      |
| LIMIT       | windows                                          |      |
| OPTIONS     |                                                  |      |

<br>

![ジョブテンプレートの作成](images/8-create-install-packages-job-template.png)

SAVE、LAUNCH の順にクリックして、ジョブを実行します。ジョブは正常に実行され、変数で指定されたパッケージの Ansible
ループとインストールを確認できるはずです。

![ジョブテンプレートの実行](images/8-install-packages-job-run-successful.png)

> **ヒント**
>
> これで、Playbook の作成または編集、変更のコミット、および git へのプッシュのフローが理解できたと思います。また、プロジェクトの更新、Automation Controller でのジョブテンプレートの作成と実行にも慣れたことでしょう。後のステップでは、各ステップを省略します。

## ステップ 3: インストールされているすべてのパッケージを更新する

`win_chocolatey`
モジュールは、パッケージをインストールするだけでなく、パッケージのアンインストールおよび更新にも使用されます。モジュールが実行するアクションは、`state`
パラメーターに渡す値に基づいています。渡すことができるオプションには、次のものがあります。

* `present`: パッケージがインストールされていることを確認します。
* `absent`: パッケージがインストールされていないことを確認します。
* `latest`: パッケージが利用可能な最新バージョンにインストールされていることを確認します。

前回のプレイブックでは `state` の値を明示的に定義および設定していなかったため、パッケージをインストールするための state
パラメーターの設定値としてデフォルト値の `present`
が使用されました。ただし、意図的に古いバージョンのパッケージをインストールしたため、それらのパッケージを更新する必要があります。

Visual Studio Code で、`chocolatey` フォルダーの下に `update_packages.yml`
という名前の新しいファイルを作成します。この Playbook では、`latest` パラメータに値として渡された `state` を使用して
`win_chocolatey` モジュールを使用するプレイを作成します。Chocolatey
によって以前にインストールされたすべてのパッケージを更新するため、`name` パラメーターには特定のパッケージ名を指定せずに、値 `all`
を使用します。

> **ヒント**
>
> `name` 属性に設定される値として `all` を使用する方法に関する情報は、`win_chocolatey` のモジュール [docs](https://docs.ansible.com/ansible/latest/collections/chocolatey/chocolatey/win_chocolatey_module.html) にあります。初めて使用するモジュールのドキュメントを常に確認してください。多くの場合、多くの作業を節約するのに役立つ情報があります。

`update_packages.yml` の内容は次のとおりです。

```yaml
---
- name: Update all packages using Chocolatey
  hosts: all
  gather_facts: false
  tasks:

  - name: Update all installed packages
    win_chocolatey:
      name: all
      state: latest

  - name: Check python version
    win_command: python --version
    register: check_python_version

  - name: Check nodejs version
    win_command: node --version
    register: check_node_version

  - debug:
      msg: Python Version is {{ check_python_version.stdout_lines[0] }} and NodeJS version is {{ check_node_version.stdout_lines[0] }}
```

他のタスクは、更新タスクの実行後に `nodejs` と `python` のバージョンを確認できるようにするためにあります。簡単です。

次に、新しい Playbook が Git にあり、Automation Controller
がそれを認識できることを確認してから、次の値を使用して新しいジョブテンプレートを作成して実行します。

> **ヒント**
>
> ほぼすべてが、パッケージをインストールするために作成した最初のジョブテンプレートと同様です。`Tempates` に移動し、`Chocolatey - Install Packages` テンプレートの隣の ![コピー](images/8-copy.png) アイコンをクリックすると、そのジョブテンプレートを `copy` できます。これにより、そのテンプレートのコピーが作成されます。その名前をクリックして編集し、実行する名前、説明、および Playbook に変更を加えることができます。Playbook は最初から作成することもできます。

| Key         | Value                                            | Note |
|-------------|--------------------------------------------------|------|
| Name        | Chocolatey - Update Packages                     |      |
| Description | Template for the update_packages playbook        |      |
| JOB TYPE    | Run                                              |      |
| INVENTORY   | Workshop Inventory                               |      |
| PROJECT     | Ansible Workshop Project                         |      |
| PLAYBOOK    | `chocolatey/update_packages.yml`                 |      |
| CREDENTIAL  | Type: **Machine**. Name: **Student Account**     |      |
| LIMIT       | windows                                          |      |
| OPTIONS     |                                                  |      |

新しいテンプレートを実行した後、`debug` タスクメッセージを調べて、バージョンを `install_packages`
ジョブ出力からのものと比較します。これらのパッケージは更新であるため、バージョンは高くなるはずです (アドホックコマンドを使用してインストールした
`git` パッケージも更新がチェックされます。インストールの数分後に更新される可能性はほとんどありません)。

![ジョブテンプレートの実行](images/8-update-packages-job-run-successful.png)

# セクション 2: Chocolatey のファクトと設定

`win_chocolatey` モジュールは Chocolatey でパッケージを管理するために実際に使用されるものですが、Ansible
で使用できる Chocolatey モジュールはこれだけではなく、Windows ターゲットで Chocolatey
を管理および構成するのに役立つ他のモジュールがあります。この演習では、`win_chocolatey_facts` と
`win_chocolatey_config` の 2 つを見ていきます。

## ステップ 1: Chocolatey ファクトの収集

最初に使用するモジュールは `win_chocolatey_facts`
モジュールです。このモジュールは、インストールされたパッケージ、設定、機能、ソースなどの情報を Chocolatey
から収集するために使用されます。これは、レポート生成としてのタスク、または他のタスクで定義された条件に役立ちます。

> **ヒント** > 

> 詳細は、[docs](https://docs.ansible.com/ansible/latest/collections/chocolatey/chocolatey/win_chocolatey_facts_module.html). の `win_chocolatey_facts` を参照してください。

それでは、収集した情報を収集して表示するための簡単な Playbook を作成して、このモジュールによって収集された情報を詳しく見ていきましょう。

Visual Studio Code の `chocolatey` フォルダーの下に、`chocolatey_configuration.yml`
という名前の新しいファイルを作成します。そのファイルの内容は次のようになります。

```yaml
---
- name: Chocolatey Facts and Configuration
  hosts: all
  gather_facts: false
  tasks:

  - name: Gather facts from Chocolatey
    win_chocolatey_facts:

  - name: Displays the gathered facts
    debug:
      var: ansible_chocolatey
```

最初のタスクは、`win_chocolatey_facts` を使用してターゲット Windows マシン上の Chocolatey
から利用可能なすべての情報を収集し、この情報を `ansible_chocolatey` という名前の変数に格納します。この変数は、`debug`
モジュールを使用して内容を出力して詳細を調べます。

新しい Playbook をソース管理リポジトリに追加し、Automation Controller で
プロジェクトを同期してから、次の値を使用して新しいジョブテンプレートを作成して実行します。

| Key         | Value                                            | Note |
|-------------|--------------------------------------------------|------|
| Name        | Chocolatey - Facts and configuration             |      |
| Description | Template for the chocolatey_configuration playbook |      |
| JOB TYPE    | Run                                              |      |
| INVENTORY   | Workshop Inventory                               |      |
| PROJECT     | Ansible Workshop Project                         |      |
| PLAYBOOK    | `chocolatey/chocolatey_conguration.yml`          |      |
| CREDENTIAL  | Type: **Machine**. Name: **Student Account**     |      |
| LIMIT       | windows                                          |      |
| OPTIONS     |                                                  |      |

<br>

ジョブの出力には、最初のタスクで収集された `ansible_chocolatey` 変数の内容が表示されます。

![ジョブテンプレートの実行](images/8-chocolatey-configuration-job-run-1-successful.png)

出力をスクロールして値を確認すると、Windows ターゲットでの Chocolatey
クライアントの設定、有効および無効な機能、インストールされているパッケージ
(前の演習でインストールしたパッケージが表示されているでしょうか)、およびソースが表示されます。そこからパッケージをインストールします
(これについては後で詳しく説明します)。この情報は JSON
形式であるため、オブジェクトツリーをトラバースすることで個々の値にアクセスできることに注意してください。たとえば、インストールされたパッケージに関する情報のみに関心があり、たとえばインストールされたパッケージのレポートを生成する場合は、`ansible_chocolatey.packages`
キーを使用してそれらの値にアクセスできます。

<br>

> **ヒント**
>
> `win_chocolatey_facts` モジュールによって収集された情報を表示するためだけに `debug` タスクを使用する必要はありませんでした。代わりに、Ansible Tower のジョブ出力ペインで、Windows ターゲットでタスクを実行した結果をクリックします。これにより、その特定のホストのホストイベントダイアログが開きます。選択したイベントの影響を受けるホストとそのイベントの出力に関する情報が表示されます (この場合、`win_chocolatey_facts` モジュールによって返される JSON オブジェクトが実行されます)

<br>

## ステップ 2: Chocolatey を構成する

前の手順で、`win_chocolatey_facts` モジュールを使用して Windows ターゲット上の Chocolatey
クライアントの構成を収集できることを確認しました。では、これらの構成を変更する場合はどうでしょうか。そのためのモジュールが存在します。

`win_chocolatey_config`
モジュールを使用して、設定オプションの値を変更するか、それらをすべてまとめて設定解除することにより、Chocolatey 設定を管理できます。

<br>

> **ヒント** > 

> 詳細は、[docs](https://docs.ansible.com/ansible/latest/collections/chocolatey/chocolatey/win_chocolatey_config_module.html の `win_chocolatey_config` を参照してください。

<br>

> **ヒント**
>
> 詳細は、 Chocolatey の設定 [こちら](https://docs.chocolatey.org/en-us/configurationを参照してください。

`cacheLocation` と `commandExecutionTimeoutSeconds` の 2
つの設定オプションの値を変更します。前の手順の出力では、`cacheLocation`
が設定されていないか、値が構成されていないことがわかりました。これはデフォルト設定であり、`commandExecutionTimeoutSeconds`
の値がデフォルト値の 2700 に設定されています。これらの設定オプションを変更します。

* `cacheLocation` を `C:\ChocoCache` に設定します。
* `commandExecutionTimeoutSeconds` を 1 時間または `3600` 秒に設定します。

Visual Studio Codeで、`chocolatey_configuration.yml` Playbook
を編集して、次のタスクを追加します。

```yaml
  - name: Create a directory for the new Chocolatey caching directory
    win_file:
      path: C:\ChocoCache
      state: directory

  - name: Configure Chocolatey to use the new directory as the cache location
    win_chocolatey_config:
      name: cacheLocation
      state: present
      value: C:\ChocoCache

  - name: Change the Execution Timeout Setting
    win_chocolatey_config:
      name: commandExecutionTimeoutSeconds
      state: present
      value: 3600

  - name: ReGather facts from Chocolatey after new reconfiguring
    win_chocolatey_facts:

  - name: Displays the gathered facts
    debug:
      var: ansible_chocolatey.config
```

これらの新しいタスクは、以下を実行します。

* `win_file` モジュールを使用してディレクトリー `C:\ChocoCache` を作成します。
* `cacheLocation` を使用して、`win_chocolatey_config` の値を新たに作成されたディレクトリーに変更します。
* `commandExecutionTimeoutSeconds` の値を `3600` に変更します。
* 設定値を変更した後、Chocolatey ファクトを再収集します。
* そして最後に、刷新された Chocolatey ファクトの`config`の部分を出力します。

`chocolatey_configuration.yml` Playbook の内容は以下のようになります。

```yaml
---
- name: Chocolatey Facts and Configuration
  hosts: all
  gather_facts: false
  tasks:

  - name: Gather facts from Chocolatey
    win_chocolatey_facts:

  - name: Displays the gathered facts
    debug:
      var: ansible_chocolatey

  - name: Create a directory for the new Chocolatey caching directory
    win_file:
      path: C:\ChocoCache
      state: directory

  - name: Configure Chocolatey to use the new directory as the cache location
    win_chocolatey_config:
      name: cacheLocation
      state: present
      value: C:\ChocoCache

  - name: Change the Execution Timeout Setting
    win_chocolatey_config:
      name: commandExecutionTimeoutSeconds
      state: present
      value: 3600

  - name: ReGather facts from Chocolatey after new reconfiguring
    win_chocolatey_facts:

  - name: Displays the gathered facts
    debug:
      var: ansible_chocolatey.config
```

変更をコミットしてソース管理にプッシュし、Automation Controller でプロジェクトを同期して、`Chocolatey - Facts and Configuration` ジョブテンプレートを実行します。
> **ヒント**
>
> [演習 1](../1-tower) で Automation Controller でプロジェクトを作成したときに、`UPDATE REVISION ON LAUNCH` のオプションをチェックしたので、Controller でプロジェクトを更新する必要はありませんでした。しかし、そのオプションをチェックしていない場合を想定しています。

Playbook を実行して設定を変更し、`ansible_chocolatey.config` セクションの値を示す最後の `debug`
タスクからの出力にそれらの変更を反映し、`cacheLocation` と `commandExecutionTimeoutSeconds`
の新しい値を表示する必要があります。

![ジョブテンプレートの実行](images/8-chocolatey-configuration-job-run-2-successful.png)

<br><br>

これで終わりです。今回の演習では、Chocolatey に関連する Ansible モジュールの多くをカバーしました
(ただし、`win_chocolatey_source`と`win_chocolatey_feature` については
[こちら](https://docs.ansible.com/ansible/latest/collections/chocolatey/chocolatey/win_chocolatey_feature_module.htmlと
[こちら](https://docs.ansible.com/ansible/latest/collections/chocolatey/chocolatey/win_chocolatey_source_module.html)
を参照してください) 願わくば、Ansible と Chocolatey を組み合わせて Windows
パッケージを管理することで、その可能性を味わっていただきたいと思います。

<br><br>
[Click here to return to the Ansible for Windows Workshop](../README.md)
