# 演習 1.2 - 最初の Check Point 用 Playbook の実行

**他の言語でもお読みいただけます**: <br>
[![uk](../../../images/uk.png) English](README.md),  [![japan](../../../images/japan.png) 日本語](README.ja.md), [![france](../../../images/fr.png) Français](README.fr.md).<br>

<div id="section_title">
  <a data-toggle="collapse" href="#collapse2">
    <h3>Workshop access</h3>
  </a>
</div>
<div id="collapse2" class="panel-collapse collapse">
  <table>
    <thead>
      <tr>
        <th>Role</th>
        <th>Inventory name</th>
        <th>Hostname</th>
        <th>Username</th>
        <th>Password</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Ansible Control Host</td>
        <td>ansible</td>
        <td>ansible-1</td>
        <td>-</td>
        <td>-</td>
      </tr>
      <tr>
        <td>IBM QRadar</td>
        <td>qradar</td>
        <td>qradar</td>
        <td>admin</td>
        <td>Ansible1!</td>
      </tr>
      <tr>
        <td>Attacker</td>
        <td>attacker</td>
        <td>attacker</td>
        <td>-</td>
        <td>-</td>
      </tr>
      <tr>
        <td>Snort</td>
        <td>snort</td>
        <td>snort</td>
        <td>-</td>
        <td>-</td>
      </tr>
      <tr>
        <td>Check Point Management Server</td>
        <td>checkpoint</td>
        <td>checkpoint_mgmt</td>
        <td>admin</td>
        <td>admin123</td>
      </tr>
      <tr>
        <td>Check Point Gateway</td>
        <td>-</td>
        <td>checkpoint_gw</td>
        <td>-</td>
        <td>-</td>
      </tr>
      <tr>
        <td>Windows Workstation</td>
        <td>windows-ws</td>
        <td>windows_ws</td>
        <td>administrator</td>
        <td><em>Provided by Instructor</em></td>
      </tr>
    </tbody>
  </table>
  <blockquote>
    <p><strong>Note</strong></p>
    <p>
    The workshop includes preconfigured SSH keys to log into Red Hat Enterprise Linux hosts and don't need a username and password to log in.</p>
  </blockquote>
</div>

## ステップ 2.1 - Check Point Next Generation Firewall

セキュリティー環境でファイアウォールを自動化する方法を紹介するため、このラボには Check Point Next Generation
Firewall (NGFW) が含まれます。

通常、NGFW は直接管理されず、中央のセキュリティー管理サーバー (MGMT) を介して管理されます。MGMT は、1 つのスポットで複数の NGFW
またはその他のセキュリティーツールを管理する主要なツールです。

MGMT と対話する方法は複数あります。このラボでは、以下の 2 つの方法が重要となります。

- API: Ansible は主に API と連携します。 - Windows クライアント: ユーザー対話は Windows
クライアントで行われます。

このラボでは、作成する Playbook はバックグラウンドで API と対話します。すべてのアクションは Windows クライアント UI
で検証されます。

## ステップ 2.2 - Windows ワークステーションを介した Check Point MGMT サーバーへのアクセス

MGMT サーバーにアクセスするには Windows クライアントが必要ですが、ラボの受講者全員が Windows
環境にアクセスできるか確認できないため、このラボの一部として Windows ワークステーションをプロビジョニングしました。

Windows ワークステーションは Remote Desktop Protocol (RDP)
経由でアクセスすることができます。利用可能な場合は、ネイティブの RDP
クライアントを使用することを推奨しています。利用可能でない場合は、ラボの参加者がブラウザー経由でワークステーションにアクセスできるようにする HTML
RDP クライアントがワークステーションに搭載されています。

RDP クライアントをインベントリーの `windows-ws` IP にポイントして、MGMT サーバーへのアクセスをテストします。

RDP クライアントが利用できない場合や、HTML RDP クライアントをテストする必要がある場合は、ブラウザーで `https://<windows-wsIP>/myrtille` の URL を開いてください。`<windows-wsIP>` は、インベントリーの Windows ワークステーションの IP に置き換えます。ログインフィールドでは、ユーザー名とパスワードのみを指定します。ユーザー名は **Administrator** で、パスワードはインベントリーに記載されています。他のフィールドは空のままにして、**Connect** をクリックします。

これで、Google Chrome ブラウザーがインストールされたデフォルトの Windows ワークステーションにアクセスできるようになりました。

>**注記**
>
> ログインした直後に、画面の右側に、ネットワーク設定に関する幅広い青いバーが表示されることがあります。これは無視しても問題ありません。画面のどこかをクリックすると、この質問は非表示になります。

## ステップ 2.3: SmartConsole UI へのアクセス

デスクトップアイコンから Check Point SmartConsole を起動します。以下のウィンドウでは、ユーザー名に `admin`
を使用し、パスワードに `admin123` を使用します (特に指示がない場合)。

オンラインエディターで **lab inventory** を開き、**firewall**
インベントリーグループを検索します。`checkpoint` エントリーがあるはずです。`ansible_host` IP アドレスを使用して
SmartConsole にログインします。


![SmartConsole login window](images/smartconsole-login-window.png#centreme)

**Login** ボタンを押します。その後、**PROCEED** ボタンをクリックして、サーバーのフィンガープリントを確認する必要があります。

> **注記**
>
> 実稼働環境では、まずサーバーのフィンガープリントを把握し、表示されたフィンガープリントがサーバーのものと同一であることを確認してから作業を進めることになります。短期間のインスタンスを使用したこのデモセットアップでは、フィンガープリントが良好であると想定できます。

これで Check Point SmartConsole 管理インターフェースが表示されます。起動時に Internet Explorer
の警告が表示される可能性があります。これは、IE の動作の制限によるもので、安全に閉じることができます。

![SmartConsole main window](images/smartconsole-main-window.png#centreme)

次に、左側で **SECURITY POLICIES** をクリックし、現在インストールされているルールは 1 つだけ
(すべてのトラフィックをドロップするルール) であることに注意してください。これで、管理インターフェースの観点から Check Point
がどのように見えるかについての概要がわかりました。Check Point との対話はもっとありますが、その前にコマンドラインに戻って、Check
Point と対話する Ansible Playbook の作成方法について学びます。

## ステップ 2.4 - 最初の Playbook の例

Ansible Automation Platform では、自動化は Playbook で説明されています。Playbook
は、管理対象ホストに実装するための必要な設定またはステップを記述するファイルです。Playbook
は、長くて複雑な管理タスクを、簡単に反復できるルーチンに変え、結果を予測して成功させることができます。

Playbook は、*plays* および *tasks* の反復可能なセットです。

Playbook は複数のプレイを持つことができ、1 つのプレイは 1 つまたは複数のタスクを持つことができます。タスクは 1 つ以上の
*modules* で構成されており、モジュールは実際の作業を行うコンポーネントです。

*play* の目的は、ホストのグループをマッピングすることです。*task* の目的は、それらのホストに対してモジュールを実装することです。

Ansible に慣れていない場合は、以下の Playbook の例を参照してください。

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
> ここで、わかりやすい例えを紹介します。Ansible モジュールがワークショップのツールだとすると、インベントリーは材料で、Playbook は指示書になります。

次に、Check Point の設定を変更するための Playbook
を作成します。まずは、ファイアウォール設定にホワイトリストエントリーを追加して、特定のマシンから別のマシンにトラフィックを許可する簡単な例から始めます。この例では、**attacker**
というマシンから **snort** マシンへのトラフィック送信を許可します。

Playbook は Ansible コントロールホストで書かれ、実行されます。Playbook が書かれている言語は [YAML](https://en.wikipedia.org/wiki/YAML). です。ブラウザーで、VS Code のオンラインエディターにアクセスします。メニューバーで、**File** -> **New File** をクリックします。新しい空のファイルが開きます。続行する前にこれを保存しましょう。再びメニューバーで、**File** -> **Save As...** をクリックします。ドロップダウンメニューが開き、**lab_inventory** ディレクトリーにファイル名 **Untitled-1** が表示されます。これを `whitelist_attacker.yml` に変更し、**lab_inventory** ディレクトリーを削除して、完全なファイル名 `/home/student/whitelist_attacker.yml`。

> **注記**
>
> ファイルおよび今後のすべての操作は、常にホームディレクトリー **/home/student** で実行するようにしてください。これは、演習を正しく実行する上で重要となります。

ファイルを適切な場所に保存したら、Playbook コードを追加することができます。まず、Playbook
には名前と実行するホストが必要です。では、これらを追加してみましょう。

```yaml
---
- name: Whitelist Attacker
  hosts: checkpoint
```

上部の 3 つのダッシュ (`---`) は、YAML ファイルの開始を示しています。

> **注記**
>
> Playbook を `hosts: all` にポイントして、後でコマンドラインまたは自動化コントローラーを介して実行を制限することにより、Playbook をより再利用可能にすることをお勧めします。しかし今のところは、Playbook で直接ホストに名前を付けることでプロセスを簡素化します。

前述したように、ここでは簡単な例としてホワイトリストエントリーを追加します。シンプルなホワイトリストエントリーは、送信元 IP アドレス、送信先 IP
アドレス、それらの間のアクセスを許可するルールで構成されています。

そのため、送信元と送信先の IP を変数として Playbook に追加します。Ansible はインベントリーからすべてのマシンを認識しており、IP
はインベントリーに記載されているため、これらの情報を対応するホストの
[variables](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html)
として参照することができます。

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

ご覧のように、変数は中括弧で囲まれています。2 番目のプライベート IP
を使用していることに注意してください。これらは、アプリケーショントラフィックのために FW
を介して特別にルーティングされるネットワークに属しています。最初のプライベート IP
は、管理ネットワークに属しています。これらの変数は、それぞれがさらに別の (短い) 変数を定義するために使用され、Playbook
全体で使用されます。これは、データを実行から切り離すための一般的な方法です。

> **注記**
>
> 空白文字とインデントが正確に表示されていることを確認してください。YAML はこの点に厳しく、Playbook の実行時のエラーの多くはインデントが間違っていることが原因です。

次にタスクを追加する必要があります。タスクセクションでは、ターゲットマシン上での実際の変更が行われます。この場合、これは 3 つのステップで行われます。

- 最初に、ソースオブジェクトを作成します。次に、宛先オブジェクトを作成します。最後に、これら 2 つのオブジェクト間のアクセスルールを作成します。

ソースオブジェクトを定義するタスクから始めましょう。

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

ご覧のとおり、タスク自体にはプレイ自体と同様に名前が付いており、モジュールを参照しています (ここでは`checkpoint_host`)。モジュールは「それを実現する」 Ansible の一部です。この場合のモジュールは、CheckPoint でホストオブジェクトエントリーを作成または変更します。モジュールにはパラメーターがあり、`name` と `ip_address` がそれにあたります。各モジュールには個別のパラメーターがあり、多くの場合、パラメーターの中には必須のものとオプションのものがあります。モジュールに関する詳細な情報を得るには、VS Code オンラインエディタでターミナルを開き、ヘルプを呼び出すことができます。たとえば、メニューバーで **Terminal** > **New Terminal** をクリックし、以下のコマンドを実行します。これにより、モジュール `checkpoint_host` のヘルプが表示されます。

```bash
[student@ansible-1 ~]$ ansible-navigator doc checkpoint_host
```

> **ヒント**
>
> `ansible-navigator` で、`up`/`down` の矢印を使用してコンテンツをスクロールし、`Esc` を使用して終了します。

ソース IP ホストオブジェクトを定義したのと同じ方法で、宛先 IP ホストオブジェクトを追加します。

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

最後に、これらの 2 つのホストオブジェクト間で、実際のアクセスルールを定義しています。ルールを適用する必要がありますが、これには 2
つの方法があります。モジュールパラメーター `auto_install_policy: yes`
を介して示されるタスクごとのベースへの適用、またはモジュール `cp_mgmt_install_policy`
を持つ最終的な専用タスクとしての適用のいずれかになります。この Playbook
では、モジュール式アプローチの柔軟性を強調するために、どちらも紹介しています。ただし、モジュールがすでに適用プロセスを開始している場合、最後のインストールポリシーモジュールが失敗する可能性があるため、エラーの可能性を無視するための特別なフラグを追加しています(`failed_when:
false`)。

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

## ステップ 2.5 - Playbook の実行

Playbook は、コントロールノードで `ansible-navigator` コマンドを使用して実行されます。新しい Playbook を実行する前に、構文エラーを確認することが推奨されます。VS Code のオンラインエディターのメニューバーで、**Terminal** -> **New Terminal** をクリックします。ターミナルで以下のコマンドを実行します。

```bash
[student@ansible-1 ~]$ ansible-navigator run whitelist_attacker.yml --syntax-check --mode stdout
```

構文チェックでは、エラーは報告されないはずです。エラーが報告された場合は出力を確認し、Playbook コードで問題の修正を試みてください。

これで、Playbook を実行する準備が整いました。

```bash
[student@ansible-1 ~]$ ansible-navigator run whitelist_attacker.yml --mode stdout

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

## ステップ 2.6 - UI での変更の確認

次に、この変更が実際に行われ、Check Point MGMT サーバーの設定が変更されたかどうかを確認します。

Windows ワークステーションにアクセスし、SmartConsole インターフェースを開きます。右側の **Object Categories**
の下で **Network Objects** をクリックしてから、**Hosts** を選択します。両方の新しいホストエントリーが表示されます。

![SmartConsole Hosts list](images/smartconsole-hosts-list.png#centreme)

次に、左側の **SECURITY POLICIES**
をクリックします。フィールドの中央に追加されたアクセス制御ポリシーのエントリーに注目して、先ほど見たときと比較してください。トラフィックが許可されるようになったので、**Action**
列のエントリーが変更され、色が変わっています。

![SmartConsole Policy
Entries](images/smartconsole-policy-entry.png#centreme)

また、左下隅には、システム全体に変更が適用されることを示す緑色のバーが表示されていることに注意してください。

## ステップ 2.7 - 新しいポリシーのロギングをオンにする

Check Point との通常の手動対話で変更がどのように実行されるかを確認するには、後で便利な小さな変更を行います。デフォルトでは、Check
Point
は新しいルールのロギングをオンにしません。ここでは、新しいポリシーのロギングをアクティブ化してみましょう。メインウィンドウの左側で、**SECURITY
POLICIES** をクリックします。両方のルールが一覧表示されています。。**Track** 列で、新しく作成したルールの **None**
エントリー上にマウスをかざします。これを右クリックし、表示されるボックスで **Log** を選択します。

![SmartConsole, change
logging](images/smartconsole-change-logging.png#centreme)

その後、ポリシー一覧の上部にある **Install Policy** ボタンをクリックして、**Publish & Install**
で開いたダイアログを確認し、最後のダイアログで **Install** を再度クリックします。

その結果、左隅に、変更のデプロイメントの進捗状況を通知する小さなウィンドウがポップアップします。

このように、設定を少し変更するだけでも、ユーザーは何度もクリックしなければなりません。これらのステップをより多く自動化できるほど、結果は良くなります。
<br>

----

**Navigation**
<br><br>
[Previous Exercise](../1.1-explore/README.md) | [Next Exercise](../1.3-snort/README.md)
<br><br>
[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md)
