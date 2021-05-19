# 演習 1.3 - 最初のSnort用のPlaybookを実行してみよう

**Read this in other languages**: <br>
[![uk](../../../images/uk.png) English](README.md),  [![japan](../../../images/japan.png) 日本語](README.ja.md), [![france](../../../images/fr.png) Français](README.fr.md).<br>

## Step 3.1 - Snort

セキュリティ環境でネットワーク侵入検知および侵入防止システムを自動化する方法を紹介するために、このラボでは Snort IDS インスタンスの管理方法を説明します。Snort はネットワークトラフィックを分析し、与えられたルールセットと比較します。
このラボでは、Red Hat Enterprise Linux マシンに Snort をインストールし、SSH 経由で RHEL ノードにアクセスすることで Ansible が Snort を操作します。

## Step 3.2 - Snortサーバーにアクセスする

Snortに接続するためには、インストールされているマシンのIPアドレスを見つける必要があります。Snort マシンの IP アドレスは、インベントリファイル `~/lab_inventory/hosts` を調べることで取得できます。VS Code のオンラインエディタで、メニューバーの **File** > **Open File...** をクリックして、ファイル `/home/student<X>/lab_inventory/hosts` を開きます。snort のエントリを検索して、以下のようなエントリを見つけてください:

```bash
snort ansible_host=22.333.44.5 ansible_user=ec2-user private_ip=172.16.1.2
```

> **NOTE**
>
> ここに記載されているIPアドレスはデモ用のものであり、あなた用のものとは異なります。あなたのラボ環境には、あなた専用のSnort環境が用意されています。

IPアドレスを見つけたら、Snortサーバにアクセスします。接続には、コントロールホストにプリインストールされているSSHキーを使用します。VS Code のオンラインエディタでターミナルを開き、Snortサーバにアクセスします:

```bash
[student<X>@ansible ~]$ ssh ec2-user@22.333.44.5
Warning: Permanently added '22.333.44.5' (ECDSA) to the list of known hosts.
Last login: Mon Aug 26 12:17:48 2019 from h-213.61.244.2.host.de.colt.net
[ec2-user@ip-172-16-1-2 ~]$
```

Snortが正しくインストールされ設定されているかどうかを確認するには、sudo経由で呼び出してバージョンを確認することができます:

```bash
[ec2-user@ip-172-16-1-2 ~]$ sudo snort --version

   ,,_     -*> Snort! <*-
  o"  )~   Version 2.9.13 GRE (Build 15013)
   ''''    By Martin Roesch & The Snort Team: http://www.snort.org/contact#team
           Copyright (C) 2014-2019 Cisco and/or its affiliates. All rights reserved.
           Copyright (C) 1998-2013 Sourcefire, Inc., et al.
           Using libpcap version 1.5.3
           Using PCRE version: 8.32 2012-11-30
           Using ZLIB version: 1.2.7
```

また、`sudo systemctl` でサービスがアクティブに動作しているか確認してください:

```bash
[ec2-user@ip-172-16-1-2 ~]$ sudo systemctl status snort
● snort.service - Snort service
   Loaded: loaded (/etc/systemd/system/snort.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2019-08-26 17:06:10 UTC; 1s ago
 Main PID: 17217 (snort)
   CGroup: /system.slice/snort.service
           └─17217 /usr/sbin/snort -u root -g root -c /etc/snort/snort.conf -i eth0 -p -R 1 --pid-path=/var/run/snort --no-interface-pidfile --nolock-pidfile
[...]
```

> **NOTE**
>
> Snort サービスが起動していないことがあります。このデモ環境では問題ありませんが、その場合は `systemctl restart snort` で再起動してもういちど状態を確認してください。実行状態になっているはずです。

`CTRL` と `D` を押すか、コマンドラインで `exit` と入力して Snort サーバを終了します。これ以降の操作はすべて Ansible コントロールホストから Ansible を介して行われます。

## Step 3.3 - シンプルなSnortルール

Snortのもっとも基本的な機能として、Snort はいくつかのルールを読み込んで、それに従って動作します。このラボでは、Snort の簡単な例を使って、Ansible を使ってこの設定を自動化する方法を紹介します。このセッションでは、Snort のルールの詳細や、大規模なセットアップに伴う複雑さまで体験することはできませんが、シンプルなルールの基本的な構造を理解することで、自分が何を自動化しているのかを意識するのに役立ちます。

ルールは、ルールヘッダーとルールオプションで構成され、ファイルに保存されます。

Snortのルールヘッダーは以下のように分かれています:

- アクション
- TCP のような対象のプロトコル
- IPアドレスやポートなどの接続元情報
- IPアドレスやポートなどの接続先情報

Snortルールのオプションは、`;`で区切られたキーワードで、以下のように指定することができます:

- ルールがマッチしたときに出力するメッセージ
- ルールの一意の識別子であるSID
- 疑わしい文字列などのパケットペイロードの中で検索するコンテンツ
- バイナリデータをチェックするためのバイトテスト
- ルールのリビジョン
- 「priority」と呼ばれる攻撃の深刻度
- 他のルールとよりよくグループ化するための「classtype」と呼ばれるあらかじめ定義された攻撃タイプ
- その他

すべてのオプションが必須というわけではなく、既存のデフォルト値を上書きするだけのものもあります。

Snortルールの概要は以下の通りです:

```
[action][protocol][sourceIP][sourceport] -> [destIP][destport] ( [Rule options] )
```

Snortのルールについて詳しく知りたい場合は、[Snort Rule Infographic](https://www.snort.org/documents/snort-rule-infographic)や、[Snort Users Manual (PDF)](https://www.snort.org/documents/snort-users-manual)をご覧ください。実際の Snort ルールを見たい場合は、ラボの Snort インストールにアクセスして `/etc/snort/rules` ディレクトリの内容を見ることもできます。

## Step 3.4 - Playbookの例

 前述したように、Ansible の自動化は Playbook で記述されています。Playbook は Task で構成されています。各Taskは、Module とModule に対応するパラメータを使用して、実行する必要のある変更や望ましい状態を記述します。

Ansible のリリースには Module が同梱されていますが、Ansible 2.9 では Snort と対話するためのモジュールはまだありません。このため、Snortを管理するためのモジュール群を書きました。このようにして、新しいAnsibleのリリースを待たずに価値を提供することができます。また、Moduleの更新作業も早くなりました。これは、新しく開発されたModuleの初期の段階では特に重要です。

これらのSnort Moduleは「Role」の一部として出荷されます。Role をよりよく記述するために、最後のセクションで自分の Playbook をどのように書いたかを考えてみましょう。以前行ったように1つのファイルに Playbook を書くことは可能ですが、多くの場合ですべての自動化のピースを1つの場所に書くことは、長くて複雑な Playbook をつくることになります。一方で、最終的にPlaybook に書いた自動化の部品を再利用したくなる場合もあります。したがって、複数のより小さく、よりシンプルな Playbook が一緒に動作するように整理する必要があります。Roleは、それを実現する方法です。Roleを作成するときは、プレイブックを部品に分解し、それらの部品をディレクトリ構造に配置します。

Role を使って自動化を実施することには、複数のメリットがあります。最も注目すべきは、複雑さとプレイブックのインテリジェンスがユーザーから隠されていることです。もう一つの重要な利点は、Role を簡単に共有して再利用できることです。

Snortのユースケースに戻ります。前述の通り、Snort Module は Role の一部として出荷されます。このRoleは[ids_rule](https://github.com/ansible-security/ids_rule)と呼ばれています。WebブラウザでGithubリポジトリのリンクを開き、[library](https://github.com/ansible-security/ids_rule/tree/master/library)のパスをクリックします。そこには `snort_rule.py` という Module があります。この Module は ids_rule Role の一部として出荷され、snort ルールを作成したり変更したりすることができます。

Role を詳しく見てみると、[tasks/snort.yml](https://github.com/ansible-security/ids_rule/blob/master/tasks/snort.yml)に再利用可能な Playbook が付属していることがわかります。

この Playbook がどのように書き換えてRoleを直接使えるようになるか見てみましょう。まず、コントロールホストに Role をダウンロードしてインストールする必要があります。これには様々な方法がありますが、非常に便利なのは `ansible-galaxy` というコマンドラインツールです。このツールは、アーカイブやGitのURL、[Ansible Galaxy](https://galaxy.ansible.com)から直接Roleをインストールします。Ansible Galaxy は、Ansible のコンテンツを見つけて共有するためのコミュニティハブです。レーティング、品質テスト、適切な検索などの機能を提供しています。例えば、上記のRoleはAnsible Galaxyの[ansible_security/ids_rule](https://galaxy.ansible.com/ansible_security/ids_rule)にあります。

コマンドラインでは、`ansible-galaxy` ツールを使って `ids_rule` Role をダウンロードしてインストールすることができます。VSCodeオンラインエディタのターミナルで以下のコマンドを実行します:

```bash
[student<X>@ansible ~]$ ansible-galaxy install ansible_security.ids_rule
- downloading role 'ids_rule', owned by ansible_security
- downloading role from https://github.com/ansible-security/ids_rule/archive/master.tar.gz
- extracting ansible_security.ids_rule to /home/student<X>/.ansible/roles/ansible_security.ids_rule
- ansible_security.ids_rule (master) was installed successfully
```


ご覧のように、Role はデフォルトパスである `~/.ansible/roles/` にインストールされ、プレフィックスとして `ansible_security` が付けられています。これは、このラボで使用しているものなど、security roleに使用されるプロジェクトの名前です。

Role がコントロールホストにインストールされているので、Playbook で使用することができます。Role を使用するためには、VSCodeのオンラインエディタで `add_snort_rule.yml` という名前の新しいファイルを作成します。これをユーザのホームディレクトリに保存し、`Add Snort rule`という名前と対象となるホストを追加します。Snort上で変更を行うにはroot権限が必要なので、`become`フラグを追加して、Ansibleが特権昇格に対処できるようにします。

```yaml
---
- name: Add Snort rule
  hosts: snort
  become: yes
```

次に、Playbookに必要な変数を追加する必要があります。私たちが使用しているRoleは、複数のIDSプロバイダで動作するように書かれています。ユーザが提供する必要があるのはIDSの名前だけで、Roleは残りの部分を担当します。Snort IDSを管理しているので、`ids_provider` 変数の値を `snort` に設定する必要があります。

```yaml
---
- name: Add Snort rule
  hosts: snort
  become: yes

  vars:
    ids_provider: snort
```

次に、Taskを追加する必要があります。Taskは、ターゲットマシン上で実際の変更を行うコンポーネントです。Roleを使用しているので、Taskの `include_role` を使ってシンプルな手順でPlaybookに追加することができます。私たちのユースケースに適したRoleを作るために、以下のTask固有の変数を追加します:

- 実際のルール定義
- Snortのルールファイル
- ルールの状態(present/absent)

```yaml
---
- name: Add Snort rule
  hosts: snort
  become: yes

  vars:
    ids_provider: snort

  tasks:
    - name: Add snort password attack rule
      include_role:
        name: "ansible_security.ids_rule"
      vars:
        ids_rule: 'alert tcp any any -> any any (msg:"Attempted /etc/passwd Attack"; uricontent:"/etc/passwd"; classtype:attempted-user; sid:99000004; priority:1; rev:1;)'
        ids_rules_file: '/etc/snort/rules/local.rules'
        ids_rule_state: present
```

ルールヘッダは `alert tcp any any -> any any any` となっているので、任意のソースから任意の宛先への tcp トラフィックのアラートを作成します。
ルールオプションは、ルールがマッチした際の人間が読めるSnortメッセージを定義します。これは `content` の専門化されたバージョンであり、URIの解析を簡単にします。`classtype` は `attempted-user` に設定され、これは「ユーザの特権獲得の試み」のデフォルトクラスです。SIDは、ユーザー定義のルールに十分な高い値が設定されています。優先度は `1` で、最後にこれはこのルールの最初のバージョンなので、リビジョンを `1` に設定します。

他の変数 `ids_rules_file` と `ids_rule_state` は、ユーザ定義のルールファイルの場所を指定し、ルールがまだ存在しない場合にはルールを作成すべきであることを示します(`present`)。

## Step 3.5 - Run the playbook

いよいよPlaybookを実行する時が来ました。Playbook名を指定して `ansible-playbook` を実行します:

```bash
[student1@ansible ~]$ ansible-playbook add_snort_rule.yml

PLAY [Add Snort rule] *****************************************************************

TASK [Gathering Facts] ****************************************************************
ok: [snort]

TASK [Add snort password attack rule] *************************************************

TASK [ansible_security.ids_rule : verify required variable ids_provider is defined] ***
skipping: [snort]

TASK [ansible_security.ids_rule : ensure ids_provider is valid] ***********************
skipping: [snort]

TASK [ansible_security.ids_rule : verify required variable ids_rule is defined] *******
skipping: [snort]

TASK [ansible_security.ids_rule : verify required variable ids_rule_state is defined] *
skipping: [snort]

TASK [ansible_security.ids_rule : include ids_provider tasks] *************************
included: /home/student1/.ansible/roles/ansible_security.ids_rule/tasks/snort.yml for
snort

TASK [ansible_security.ids_rule : snort_rule] *****************************************
changed: [snort]

RUNNING HANDLER [ansible_security.ids_rule : restart snort] ***************************
changed: [snort]

PLAY RECAP ****************************************************************************
snort  : ok=4  changed=2  unreachable=0  failed=0  skipped=4  rescued=0  ignored=0
```

このPlaybookを実行するとわかるように、ルールの追加とともに実行されるTaskがたくさんあります。たとえば、ルールが追加された後、RoleはSnortサービスをリロードします。その他のTaskでは、変数の定義と検証を確実に行います。
これは、Roleを使うことの価値を改めて強調しています。Roleを活用することで、コンテンツを再利用可能なものにするだけでなく、検証Taskなどの重要なステップを追加し、Roleの中にすっきりと隠しておくことができます。このRoleのユーザは、セキュリティ自動化の一部としてこのRoleを使用するために、Snortがどのように動作するか詳細を知る必要がありません。

## Step 3.6 - 変更を検証する

ルールが正しく書かれているかどうかを確認する簡単な方法は、SnortサーバにSSHして `/etc/snort/rules/local.rules` ファイルの内容を確認することです。 

もう一つの方法は、コントロールホストでAnsibleを使用することです。これを行うには、別の Roleを使用してSnortルールがあるかどうかを確認します。[ids_rule_facts](htithub.com/ansible-security/ids_rule_facts)というRoleは、Snortの既存のルールを検索して見つけます。
このRoleを使うには、先ほどと同じように `ansible-galaxy` を使ってインストールします:

```bash
[student<X>@ansible ~]$ ansible-galaxy install ansible_security.ids_rule_facts
- downloading role 'ids_rule_facts', owned by ansible_security
- downloading role from https://github.com/ansible-security/ids_rule_facts/archive/master.tar.gz
- extracting ansible_security.ids_rule_facts to /home/student1/.ansible/roles/ansible_security.ids_rule_facts
- ansible_security.ids_rule_facts (master) was installed successfully
```

VSCodeのオンラインエディタで、`verify_attack_rule.yml`というPlaybookを作成します。Playbookの名前を「Verify Snort rule」などに設定します。hosts、IDSプロバイダの変数、`become`フラグの値は、前回のPlaybookと同じように設定することができます。

```yaml
---
- name: Verify Snort rule
  hosts: snort
  become: yes

  vars:
    ids_provider: snort
```

次に、`ids_rule_facts` Role をインポートします。また、探しているルールを特定するための検索文字列を提供する必要があります。この例では、作成したルールを考慮すると、この目的では `uricontent` ルールオプションを使用するのがよいでしょう。

```yaml
---
- name: Verify Snort rule
  hosts: snort
  become: yes

  vars:
    ids_provider: snort

  tasks:
    - name: import ids_rule_facts
      import_role:
        name: 'ansible_security.ids_rule_facts'
      vars:
        ids_rule_facts_filter: 'uricontent:"/etc/passwd"'
```

そして何よりも、実際に発見されたものを見られるようにしたいです。ids_rule_facts` は収集したデータを Ansible のFactとして保存します。Ansible のFactは、個々のホストに固有の情報であり、更なるTaskで使用することができます。そこで、これらのFactを出力するための別のTaskを追加します。

```yaml
---
- name: Verify Snort rule
  hosts: snort
  become: yes

  vars:
    ids_provider: snort

  tasks:
    - name: import ids_rule_facts
      import_role:
        name: 'ansible_security.ids_rule_facts'
      vars:
        ids_rule_facts_filter: 'uricontent:"/etc/passwd"'

    - name: output rules facts
      debug:
        var: ansible_facts.ids_rules
```

では、Playbookを実行して、ルールがSnortインストールの一部であることを確認してみましょう:

```bash
[student<X>@ansible ~]$ ansible-playbook verify_attack_rule.yml

PLAY [Verify Snort rule] **************************************************************

TASK [Gathering Facts] ****************************************************************
ok: [snort]

TASK [ansible_security.ids_rule_facts : collect snort facts] **************************
ok: [snort]

TASK [debugoutput rules facts] ********************************************************
ok: [snort] =>
  ansible_facts.ids_rules:
  - alert tcp and any -> any any (msg:"Attempted /etc/passwd Attack";
  uricontent:"/etc/passwd"; classtype:attempted-user; sid:99000004; priority:1; rev:1;)

PLAY RECAP ****************************************************************************
snort  : ok=3  changed=0  unreachable=0  failed=0  skipped=0  rescued=0  ignored=0
```

最後のタスクは、Roleで見つけたルールを出力します。見ての通り、以前に追加したルールです。

おめでとうございます！これで Ansible で Snort を自動化する最初のステップが完了しました。演習の概要に戻り、次のステップに進みます。

----

[Ansible Security Automation Workshopの表紙に戻る](../README.ja.md)
