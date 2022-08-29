# 演習 1.1 - ラボ環境の調査

**他の言語でもお読みいただけます**: <br>
[![uk](../../../images/uk.png) English](README.md),  [![japan](../../../images/japan.png) 日本語](README.ja.md), [![france](../../../images/fr.png) Français](README.fr.md).<br>

## ステップ 1.1 - 目的

このラボの目的は、セキュリティーオペレーターが使用するセキュリティーツールを自動化する方法をより深く理解し、実際に体験していただくことです。そのために、セキュリティーオペレーターの日常的な課題として典型的な
3 つのセキュリティーユースケースに取り組みます。これらのケースでは、ほぼ同じツールセットを使用しますが、それぞれのユースケースでは、異なる視点
(セキュリティーアナリスト、ファイアウォールオペレーター、IDS スペシャリスト) を紹介するため、利用可能なツールに対する視点も異なってきます。

自動化コントローラーと、セキュリティー関連ツールの共通セットをセットアップしています。

| Role 	| Inventory name 	| Hostname 	| Username 	| Password 	|
|---	|---	|---	|---	|---	| | Ansible Control Host 	| ansible 	| ansible-1 	|
- 	| - 	| | IBM QRadar 	| qradar 	| qradar 	| admin 	| Ansible1! 	| |
Attacker 	| attacker 	| attacker 	| - 	| - 	| | Snort 	| snort 	| snort 	| -
  | - 	| | Check Point Management Server 	| checkpoint 	| checkpoint_mgmt 	|
admin 	| admin123 	| | Check Point Gateway 	| - 	| checkpoint_gw 	| - 	| -
  | | Windows Workstation 	| windows-ws 	| windows_ws 	| administrator 	|
*Provided by Instructor* 	| | Automation controller 	| ansible 	| ansible-1
  | admin 	| *Provided by Instructor* 	|


### ファイアウォール
-
ファイアウォールとは、送受信されるネットワークトラフィックを監視し、定義されたセキュリティールールに基づいて特定のトラフィックを許可するかブロックするかを決定するネットワークセキュリティーデバイスです。
- このワークショップでは、[Check Point Next Generation
Firewall](https://www.checkpoint.com/products/next-generation-firewall/)
を使用します。

### Security Incident and Events Management (SIEM)
- SIEM は、セキュリティー情報管理 (SIM) とセキュリティーイベント管理 (SEM)
を組み合わせたものです。イベントのリアルタイム監視および分析だけでなく、コンプライアンスまたは監査目的でセキュリティーデータの追跡およびロギングを提供します。本ワークショップでは、[QRadar](https://www.ibm.com/security/security-intelligence/qradar)
SIEM インスタンスを用意しています。

### Intrusion Prevention and Detection System (IDPS)
- 侵入検知防止システム (IDPS)
は、起こりうるインシデントを特定し、それに関する情報をログに記録し、その阻止を試み、セキュリティー管理者にこれらを報告することに重点を置いています。
- 本ワークショップでは、演習用の [Snort](https://www.snort.org) インスタンスを用意しています。

このラボの最初のセクションの演習では、上述の個々のソリューションについて説明します。これらのソリューションへのアクセス方法、使用目的、および
Ansible を使用した対話方法を学びます。

最初の演習では、Ansible Automation Platform
の機能やコマンドラインユーティリティーについても紹介します。これらをより詳しく見てみましょう。

### Ansible Automation Platform コマンドラインユーティリティー

- [ansible-navigator](https://github.com/ansible/ansible-navigator) -
Ansible 自動化コンテンツを実行および開発するためのコマンドラインユーティリティーとテキストベースのユーザーインターフェース (TUI)。  -
[ansible-core](https://docs.ansible.com/core.html) - Ansible Automation
Platform
を支えるフレームワーク、言語、機能を提供する基本的な実行ファイルです。また、`ansible`、`ansible-playbook`、`ansible-doc`
などのさまざまな cli ツールも含まれています。Ansible Core は、無料でオープンソースの Ansible
を提供する上流のコミュニティーと、Red Hat が提供する下流のエンタープライズ自動化製品である Ansible Automation
Platform との橋渡しの役割を果たします。  -
[実行環境](https://docs.ansible.com/automation-controller/latest/html/userguide/execution_environments.html)
- このワークショップでは特に取り上げません。なぜなら、実行環境はすでにこのワークショップに組み込まれているからです。実行環境とは、Ansible
の実行環境として利用できるコンテナーイメージのことです。  -
[ansible-builder](https://github.com/ansible/ansible-builder) -
このワークショップでは特に取り上げませんが、`ansible-builder`
は実行環境の構築プロセスを自動化するためのコマンドラインユーティリティです。

Ansible Automation Platformの新しいコンポーネントに関する情報が必要な場合は、このランディングページをブックマークしてください
[https://red.ht/AAP-20](https://red.ht/AAP-20)


このラボの第 2
セクションの演習は、実際のセキュリティー運用のユースケースに焦点を当てています。つまり、特定の課題を解決しなければならない状況で、通常は、上記のソリューションの
1
つだけでなく、いくつかを組み合わせて使用することになります。課題を設定し、その状況を解決するために手動で行わなければならない作業を説明した後、Ansible
を使ってその作業を自動化する手順をラボで説明します。

## ステップ 1.2 - ラボ、ノード、およびサービスのアーキテクチャー

このラボでは、事前設定されたラボ環境で作業します。ここでは、以下のホストとサービスにアクセスできます。


>**注記**
>
> ワークショップには、Red Hat Enterprise Linux ホストにログインするための事前設定された SSH キーが含まれ、ログインにユーザー名とパスワードは必要ありません。

ラボは個別にセットアップされています。独自の環境、独自のサービス、独自の仮想マシンがあります。

![Red Hat Ansible Security Workshop Pod](images/diagram.png#centreme)

セクション 2 の演習では、セキュリティーインシデントが必要です。これらは、**target** マシン、つまり Snort
サーバー上で発生する必要があります。基本的には、RHEL に Snort をインストールし、攻撃を行うための簡易 Web サーバーを実行させます。

## ステップ 1.3 - Ansible 環境へのアクセス

すべての自動化は、Ansible コントロールホスト（Red Hat Enterprise Linux
マシン）から行われます。コントロールホストへのアクセスやファイルの管理を容易にするために、オンライン版の VS Code
エディターがコントロールホストに直接インストールされています。これにより、通常の Web ブラウザーでアクセスできるようになっています。コマンドは、VS
Code エディター内のターミナルから直接実行できます。

<table>
<thead>
  <tr>
    <th>ワークショップの演習には、Visual Studio Codeの使用が強く推奨されます。Visual Studio Codeは以下を提供します。
    <ul>
    <li> ファイルブラウザ</li>
    <li>構文強調表示の機能付きテキストエディタ</li>
    <li>ブラウザ内ターミナル</li>
    </ul>
    バックアップとして、あるいはVisual Studio Codeでは不十分な場合には、SSHによる直接アクセスが可能です。さらなる説明が必要な場合は、短い YouTube ビデオが用意されています。<a href="https://youtu.be/Y_Gx4ZBfcuk"> Ansible Workshops - ワークベンチ環境へのアクセス</a>
</th>
</tr>
</thead>
</table>


Visual Studio Code にアクセスしてみましょう。ワークショップページから VS Code アクセスのリンクをクリックします。

![VS Code Access](images/1-vscode-access.png#centreme)

この時点で、**Welcome** ページが表示されます。

![VS Code - Welcome](images/1-vscode-welcome-page.png#centreme)

この環境内では、ファイルの作成や変更のほか、ターミナルを開いてコマンドを実行することができます。

## ステップ 1.4: VS Code でターミナルを開いて使用する

では、VS Code で新しいターミナルを開いてみましょう。メニューバーで、**Terminal** > **New Terminal** をクリックします。

![VS Code - New Terminal](images/1-vscode-new-terminal.png#centreme)

エディターの下位部分に新しいターミナルが開き、コマンドプロンプトが表示されます。前提条件とされる多くのタスクがすでに完了している点に留意してください。

  - Ansible ソフトウェアのインストール

  - SSH 接続および鍵の設定

  - root 権限が必要なコマンドを実行できるように、`sudo` が管理対象ホストで設定されています。

各受講者には受講者番号 (X など) が割り当てられており、明示的に指示されない限り、コントロールノードで受講者 <X> ユーザーとして作業する必要があることに注意してください。

## ステップ 1.5: 自動化実行環境の検証

次に進み、Ansible Automation Platform が正しく設定されていることを確認します。

```bash
    [student@ansible-1 ~]$ ansible-navigator images
```

結果は以下のようになります。   

![VS Code - Check Ansible
Version](images/1-vscode-navigator_list_ee.png#centreme)

実行環境 (EE) は、開発から実稼働まで、一貫して自動化を実行するための移植可能および保守可能な環境を開発者およびオペレーターに提供します。

このワークショップは、`security_ee` と呼ばれるカスタム自動化実行環境を使用します。では、詳しく見るために、対応する番号 (**0**)
を押します。出力は以下のようになります。

![ee main menu](images/1-vscode-navigator-ee-menu.png#centreme)

`Ansible version and collections` に `2` を選択すると、その特定の EE
にインストールされたすべてのコンテンツコレクションと、`ansible-core` のバージョンが表示されます。

![ee info](images/1-vscode-navigator-ee-collections.png#centreme)

`ansible-navigator` の以前の画面に戻るには、`Esc` ボタンを押します。今回の例では、`Esc` を 3
回押すとプロンプトに戻ります。


> **注記**
>
> 詳細は、[execution environment documentation](https://docs.ansible.com/automation-controller/latest/html/userguide/execution_environments.html) を参照してください。   

## ステップ 1.6 - ansible-navigator 設定の検証

Visual Studio Code を使用して `ansible-navigator.yml` ファイルを開くか、`cat`
コマンドを使用してファイルの内容を表示します。このファイルはホームディレクトリーにあります。

```bash
$ cat ~/.ansible-navigator.yml
---
ansible-navigator:
  ansible:
    inventories:
    - /home/student/lab_inventory/hosts

  execution-environment:
    image: quay.io/acme_corp/security_ee:latest
    enabled: true
    container-engine: podman
    pull-policy: missing
    volume-mounts:
    - src: "/etc/ansible/"
      dest: "/etc/ansible/"
```

`ansible-navigator.yml` ファイル内の次のパラメータに注意してください。

* `inventories`: 使用されている Ansible インベントリーの場所を示します
* `execution-environment`: デフォルトの実行環境が設定されている場所

> **注記**
>
> 設定の完全な一覧については、`ansible-navigator` [documentation](https://ansible-navigator.readthedocs.io/en/latest/settings/). を参照してください。   

## ステップ 1.7: インベントリー

VS Codeでファイルを開いてみましょう。メニューバーで、**File**、**Open File**
をクリックします。画面の中央でドロップダウンメニューが開き、ユーザーのホームディレクトリーにある利用可能なファイルの内容が表示されます。

![VS Code - VS Code file picker](images/1-vscode-filepicker.png#centreme)

**lab_inventory** を選択すると、ファイル一覧がすぐに更新されます。新規のファイル一覧で **hosts**
を選択します。これにより、お使いの環境のインベントリーが開きます。

ご覧のように、環境のインベントリーは静的な ini-type ファイルで提供されます。ここでは、以下の一覧のようになっています。ここで提供される IP
アドレスは単なる一例であり、ラボ環境では異なる点に注意してください。

```ini
[all:vars]
ansible_user=student
ansible_ssh_pass=ansible
ansible_port=22

[attack]
attacker ansible_host=99.88.77.66 ansible_user=ec2-user private_ip=172.16.99.66 private_ip2=172.17.44.66

[control]
ansible ansible_host=22.33.44.55 ansible_user=ec2-user private_ip=192.168.2.3

[siem]
qradar ansible_host=22.44.55.77 ansible_user=admin private_ip=172.16.3.44 ansible_httpapi_pass="Ansible1!" ansible_connection=httpapi ansible_httpapi_use_ssl=yes ansible_httpapi_validate_certs=False ansible_network_os=ibm.qradar.qradar

[ids]
snort ansible_host=33.44.55.66 ansible_user=ec2-user private_ip=192.168.3.4 private_ip2=172.17.33.77

[firewall]
checkpoint ansible_host=44.55.66.77 ansible_user=admin private_ip=192.168.4.5 ansible_network_os=checkpoint ansible_connection=httpapi ansible_httpapi_use_ssl=yes ansible_httpapi_validate_certs=no

[windows]
windows-ws ansible_host=55.66.77.88 ansible_user=Administrator ansible_pass=RedHat19! ansible_port=5986 ansible_connection=winrm ansible_winrm_server_cert_validation=ignore private_ip=192.168.5.6
```

すべての IP アドレスは、お使いの環境に固有のものです。演習で特定のマシンへのアクセスを求められた場合、コントロールホストのインベントリーでいつでも
IP を調べることができます。

Ansible は、お客様の環境に特化したインベントリーを使用するようにすでに設定されています。上の例で示したように、インベントリーにはホスト名や IP
アドレス以外の情報も含まれています。特に、Windows ワークステーションの場合は、さらにいくつかのパラメーターが設定されています。

> **注記**
>
> ラボ内のすべてのホストが SSH または WinRM 経由でアクセスできるわけではありません。一部のホストは、REST API、RDP、または Web ブラウザー経由でアクセスします。演習では、各ノードタイプが詳細に説明され、リソースにアクセスする方法がステップごとに表示されます。

## ステップ 1.8 - ラボでの作業

もうお分かりかもしれませんが、このラボではコマンドラインを頻繁に使用します。...したがって、すべてを手動で入力するのではなく、必要に応じてブラウザーからのコピー＆ペーストを使用することをお勧めします。ただし、一度手を止めて考え、理解を深めるようにしてください。

----
**Navigation**
<br><br>
[Next Exercise](../1.2-checkpoint/README.md)
<br><br>
[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md)
