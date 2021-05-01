# 演習 1.2 - 最初のCheck Point用のPlaybookを実行してみよう

**Read this in other languages**: <br>
[![uk](../../../images/uk.png) English](README.md),  [![japan](../../../images/japan.png) 日本語](README.ja.md), [![france](../../../images/fr.png) Français](README.fr.md).<br>

## Step 2.1 - Check Point Next Generation Firewall

このラボでは、セキュリティ環境でファイアウォールを自動化する方法を紹介するために、Check Point Next Generaion Firewall (NGFW) を使用します。

NGFW は通常、直接管理するのではなく、中央セキュリティ管理サーバ(MGMT) を介して管理します。MGMT は、複数の NGFW や他のセキュリティ・ツールを一箇所で管理するためのツールです。

MGMTとのやりとりには複数の方法があります。私たちのラボでは、以下の2つの方法が重要になります。

- API: Ansible はほとんどの場合、API を使用して動作します。
- Windows クライアント: ユーザーのインタラクションは Windows クライアントで行われます

このラボでは、私たちが書くPlaybookはバックグラウンドでAPIと対話します。すべてのアクションは、WindowsクライアントのUIで検証されます。

## Step 2.2 - WindowsワークステーションからCheck Point MGMTサーバーにアクセスする

MGMT サーバへのアクセスには Windows クライアントが必要であり、ラボの参加者全員が Windows 環境にアクセスできるとは限らないため、本ラボでは Windows ワークステーションを用意しています。

このWindowsワークステーションは、リモートデスクトッププロトコル(RDP)を介してアクセスすることができます。利用可能な場合は、ネイティブのRDPクライアントを使用することをお勧めします。使用できない場合でも、ラボの参加者がブラウザを介してワークステーションにアクセスできるように、ワークステーションには HTML RDPクライアントが用意されています。

RDP クライアントでインベントリにある `windows-ws` の IPアドレスを指定して、MGMT サーバへのアクセスを試してみてください。

RDPクライアントをお持ちでない場合や、HTMLのRDPクライアントをテストしたい場合は、以下のURL( `http://<windows-wsIP>/myrtille` )をブラウザで開いてください。
`<windows-wsIP>` を、インベントリにある Windows ワークステーションの IPアドレスに置き換えてください。ログインフィールドには、ユーザ名とパスワードのみを入力してください。他に指示がなければ、ユーザ名は **Administrator**、パスワードはインベントリに記載されています。他のフィールドは空のままにして、**Connect** をクリックします。

Google Chromeブラウザがインストールされている状態で、デフォルトのWindowsワークステーションにアクセスできるようになりました。

> **Note**
>
> ログイン後すぐに、画面の右側にネットワーク設定の青いバーが表示される場合があります。画面上のどこかをクリックすると非表示になりますが、これを無視しても問題ありません。

## Step 2.3 - SmartConsole UIにアクセスする

デスクトップアイコンから Check Point SmartConsole を起動します。次のウィンドウでは、ユーザ名に `admin`、パスワードに `admin123` を指定します。入力するIPアドレスは、インベントリの **checkpoint** のものを使用します。

![SmartConsole login window](images/smartconsole-login-window.png)

**Login** ボタンを押します。その後、**PROCEED** ボタンをクリックしてサーバーのフィンガープリントを検証する必要があります。

> **Note**
>
> 本番環境では、まずサーバのフィンガープリントを把握し、表示されたフィンガープリントがサーバのものと同一であることを確認してから作業を進める必要があります。今回のデモ環境では、一時的なインスタンスを使用しているため、フィンガープリントは問題ないと推定することができます。

これで、Check Point SmartConsole の管理インターフェイスが表示されました。起動時に Internet Explorer の警告が表示される場合があります。これは、IEの動作に制限があるためで、安全に閉じることができます。

![SmartConsole main window](images/smartconsole-main-window.png)

次に、左側の **SECURITY POLICIES** をクリックし、現在インストールされているルール(すべてのトラフィックをdropする)が1つだけあることを確認します。これで、Check Point の管理インターフェイスがおおよそどうなっているのかがわかりました。後でもっと深く触ることになりますが、まずはコマンドラインに戻って、Check Point を操作する Ansible Playbookの書き方を学びましょう。

## Step 2.4 - 最初のサンプルPlaybook

Ansible では、自動化はPlaybookで記述されています。Playbook とは、管理されているホストに実装するために必要な設定や手順を記述したファイルです。Playbookは、長くて複雑な管理タスクを、予測可能で成功した結果が得られる簡単に再現可能なルーチンに変えることができます。

Playbookは、再実行可能な *Play* と *Task* のセットです。

Playbook は複数の Play を持つことができ、Play は1つまたは複数の Task を持つことができます。Task は1つまたは複数の *Module* で構成され、Module は実際の作業を行うコンポーネントです。

*Play* の目的はホストのグループをマップすることです。 *Task* の目標は、それらのホストに対して Module を実行することです。

Ansible にあまり慣れていない方は、以下の Playbook の例をご覧ください:

```yaml
---
- name: install and start apache
  hosts: web
  become: yes
  vars:
    http_port: 80

  tasks:
    - name: httpd package is present
      yum:
        name: httpd
        state: latest

    - name: latest index.html file is present
      template:
        src: files/index.html
        dest: /var/www/html/

    - name: httpd is started
      service:
        name: httpd
        state: started
```

> **ヒント**
>
> 例えるなら、Ansible Moduleが作業場にある工具だとすると、Inventoryは材料であり、Playbook は指示書です。

ここでは、Check Point の設定を変更するための Playbook を書いてみましょう。まず、ファイアウォールの設定に whiltelist エントリを追加して、特定のマシンから別のマシンへのトラフィックを許可する簡単な例から始めます。この例では、**attacker** というマシンから **snort** というマシンにトラフィックを送信できるようにします。

Playbook は Ansible コントロールホスト上で書かれ、実行されます。Playbook の言語は [YAML](https://en.wikipedia.org/wiki/YAML) です。ブラウザでVS Codeのオンラインエディタにアクセスします。メニューバーの **File** -> **New File** をクリックします。新しい空のファイルが開きます。続ける前に、保存しておきましょう。メニューバーの **File** -> **Save As...** をクリックします。ドロップダウンメニューが開き、**lab_inventory** ディレクトリの **Untitled-1** というファイル名が表示されます。このファイル名を`whitelist_attacker.yml`に変更し、**lab_inventory** ディレクトリを削除して、絶対パスでのファイル名が `/home/student<X>/whitelist_attacker.yml` となるようにしてください。`<X>` には割り当てられた生徒IDが入ります。

> **Note**
> 
> ファイルと今後のすべての操作は、常にホームディレクトリの **/home/student<X>** で行われます。これは演習を適切に実行するために非常に重要です。

ファイルを適切な場所に保存したら、Playbook のコードを追加することができます。まず、Playbook には名前と実行するホストが必要です。そこで、下記を追加してみましょう:

```yaml
---
- name: Whitelist Attacker
  hosts: checkpoint
```

3つのダッシュ(`---`)が先頭にあることを不思議に感じるかもしれませんが、これはYAMLファイルの先頭であることを表します。

> **Note**
>
> Playbook 内で `hosts: all` を指定して再利用性を高め、後からコマンドラインや Tower 経由で対象を制限するのは良い練習になります。しかし今のところは、Playbookのホストに直接ホスト名を指定することでプロセスを単純化しています。

前述したように、この簡単な例ではホワイトリストのエントリを追加します。シンプルなホワイトリストのエントリは、送信元 IP アドレス、送信先 IP アドレス、およびそれらの間のアクセスを許可するルールで構成されています。

このために、送信元と送信先のIPアドレスを変数として Playbook に追加します。Ansible はインベントリからすべてのマシンを把握し、IPアドレスはインベントリに記載されているので、それらの情報を対応するホストの [変数](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html) として参照すればよいだけです:

<!-- {% raw %} -->
```yaml
---
- name: Whitelist Attacker
  hosts: checkpoint

  vars:
    source_ip: "{{ hostvars['attacker']['private_ip2'] }}"
    destination_ip: "{{ hostvars['snort']['private_ip2'] }}"
```
<!-- {% endraw %} -->

ご覧のように、変数は中括弧でマークされています。2番目のプライベート IP を使用していることに注目してください。これらの IP はアプリケーショントラフィックのために FW を介して特別にルーティングされたネットワークに属しています。最初のプライベート IP は管理ネットワークに属します。変数は、Playbook を通して使用される別の(短い)変数を定義するために使用されます。これは、実行からデータを切り離すための一般的な方法です。

> **Note**
>
> 空白とインデントがこの資料に記述されている通りになっていることを確認してください。YAMLはインデントや空白に非常に敏感で、Playbook を実行する際のほとんどのエラーは間違ったインデントによるものです。

次に、Task を追加する必要があります。tasks セクションは、ターゲットマシン上の実際の変更を行う場所です。今回は、以下の3つのステップを実行します:

- 最初に、source オブジェクトを作成します
- 次に、destination オブジェクトを作成します
- 最後に、これら2つのオブジェクト間のアクセスルールを作成します

まずは source オブジェクトを定義するところからはじめましょう: 

<!-- {% raw %} -->
```yaml
---
- name: Whitelist attacker
  hosts: checkpoint

  vars:
    source_ip: "{{ hostvars['attacker']['private_ip2'] }}"
    destination_ip: "{{ hostvars['snort']['private_ip2'] }}"

  tasks:
    - name: Create source IP host object
      checkpoint_host:
        name: "asa-{{ source_ip }}"
        ip_address: "{{ source_ip }}"
```
<!-- {% endraw %} -->

ご覧のように、Task 自体には名前があり、Module を参照しています（ここでは `checkpoint_hosts`）。 Module は Ansible の「変更を行う」部分で、ここでは Check Point のホストオブジェクトのエントリを作成したり、変更したりします。この Module にはパラメータがあり、ここでは `name` と `ip_address` を指定します。各 Module には個別のパラメータがあり、必須のものと任意のものがあります。モジュールに関する詳細な情報を確認するには、VSCodeでターミナルを開き、ヘルプを呼び出すことができます。メニューバーの **Terminal** > **New Terminal** をクリックして、以下のコマンドを実行します。すると、 `checkpoint_host` のヘルプが表示されます。

```bash
[student<X>@ansible ~]$ ansible-doc checkpoint_host
```

> **Tip**
>
> `ansible-doc` では、`up`/`down` の矢印を使って内容をスクロールし、`q` を使って終了することができます。

接続元IPアドレスのホストオブジェクトを定義したのと同じように、今度は接続先IPアドレスのホストオブジェクトを追加します:

<!-- {% raw %} -->
```yaml
---
- name: Whitelist attacker
  hosts: checkpoint

  vars:
    source_ip: "{{ hostvars['attacker']['private_ip2'] }}"
    destination_ip: "{{ hostvars['snort']['private_ip2'] }}"

  tasks:
    - name: Create source IP host object
      checkpoint_host:
        name: "asa-{{ source_ip }}"
        ip_address: "{{ source_ip }}"

    - name: Create destination IP host object
      checkpoint_host:
        name: "asa-{{ destination_ip }}"
        ip_address: "{{ destination_ip }}"
```
<!-- {% endraw %} -->

最後に、これら2つのホストオブジェクト間に実際のアクセスルールを定義します。ルールを実際に適用する必要がありますが、これには2つの方法があります。 Task 単位で、Module パラメータ `auto_install_policy: yes` で指定する方法と、`cp_mgmt_install_policy` モジュールで最終的な専用の Task として指定する方法です。この Playbook では、モジュラー方式の柔軟性を強調するために、両方を示しています。しかし、Module がすでに適用プロセスを開始している場合、最後のインストールポリシー Module が失敗する可能性があるので、起こりうるエラーを無視するための特別なフラグ `failed_when: false` を追加します:

<!-- {% raw %} -->
```yaml
---
- name: Whitelist attacker
  hosts: checkpoint

  vars:
    source_ip: "{{ hostvars['attacker']['private_ip2'] }}"
    destination_ip: "{{ hostvars['snort']['private_ip2'] }}"

  tasks:
    - name: Create source IP host object
      checkpoint_host:
        name: "asa-{{ source_ip }}"
        ip_address: "{{ source_ip }}"

    - name: Create destination IP host object
      checkpoint_host:
        name: "asa-{{ destination_ip }}"
        ip_address: "{{ destination_ip }}"

    - name: Create access rule to allow access from source to destination
      checkpoint_access_rule:
        auto_install_policy: yes
        auto_publish_session: yes
        layer: Network
        position: top
        name: "asa-accept-{{ source_ip }}-to-{{ destination_ip }}"
        source: "asa-{{ source_ip }}"
        destination: "asa-{{ destination_ip }}"
        action: accept

    - name: Install policy
      cp_mgmt_install_policy:
        policy_package: standard
        install_on_all_cluster_members_or_fail: yes
      failed_when: false
```
<!-- {% endraw %} -->

## Step 2.5 - Playbookを実行する

Playbook はコントロールノードの `ansible-playbook` コマンドを使って実行します。新しい Playbook を実行する前に、構文エラーをチェックすることをおすすめします。VSCode オンラインエディタで、メニューバーの **Terminal** -> **New Terminal** をクリックします。ターミナルで、以下のコマンドを実行します:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook --syntax-check whitelist_attacker.yml
```

構文チェックではエラーが報告されないはずです。エラーが報告された場合は、出力をチェックし、Playbookを見直して問題を修正してみてください。

これで Playbook を実行する準備が整いました:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook whitelist_attacker.yml

PLAY [Whitelist attacker] *********************************************************

TASK [Gathering Facts] ************************************************************
ok: [checkpoint]

TASK [Create source IP host object] ***********************************************************************************
changed: [checkpoint]

TASK [Create destination IP host object] ***********************************************************************************
changed: [checkpoint]

TASK [Create access rule to allow access from source to destination] ***********************************************************************************
changed: [checkpoint]

PLAY RECAP ************************************************************************
checkpoint  : ok=4 changed=3 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0
```

## Step 2.6 - UIで変更を確認する

ここで、変更が本当に行われたかどうか、Check Point MGMTサーバの設定が変更されたかどうかを確認してみましょう。

Windows ワークステーションにアクセスし、SmartConsole インタフェースを開きます。右側の **Object Categories** の下の **Network Objects** をクリックし、**Hosts** を選択します。新しいホストエントリの両方がリストアップされているはずです。

![SmartConsole Hosts list](images/smartconsole-hosts-list.png)

次に、左側の **SECURITY POLICIES** をクリックします。フィールドの中央にアクセス制御ポリシーのエントリが追加されていることを確認してください。トラフィックが許可されるようになったので、**Action** 列のエントリが変更され、色が変わっています。

![SmartConsole Policy Entries](images/smartconsole-policy-entry.png)

また、左下には、システム全体に変更が適用されたことを示す緑色のバーがあることにも注意してください。

## Step 2.7 - 新しいポリシーのロギングを有効化する

Check Point の通常の手作業による操作でどのように変更が実行されるかを確認するために、後で便利な小さな変更を行ってみましょう。デフォルトでは、Check Point は新しいルールのロギングを有効にしません。新しいポリシーのロギングを有効にしてみましょう。メイン・ウィンドウの左側にある **SECURITY POLICIES** をクリックします。両方のルールがリストされています。列の **Track** で、新しく作成したルールの **None** エントリの上にマウスを置きます。その上で右クリックし、表示されるボックスで **Log** を選択します。

![SmartConsole, change logging](images/smartconsole-change-logging.png)

その後、ポリシーのリストの一番上にある **Install Policy** ボタンをクリックし、**Publish & Install** と表示されるダイアログを確認し、最後のダイアログで **Install** を再度クリックします。

その結果、左側に小さなウィンドウがポップアップし、変更の進捗状況を知らせてくれます。

ご覧のように、設定の小さな変更でも、ユーザーが何度もクリックする必要があります。これらのステップを自動化できたほうがよいですね。

----

[Ansible Security Automation Workshopの表紙に戻る](../README.ja.md)
