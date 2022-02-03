# 演習 1.3 - 最初の Snort Playbook の実行

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
    ワークショップには、Red Hat Enterprise Linux ホストにログインするための事前設定された SSH キーが含まれているので、ログイン用のユーザー名とパスワードは必要ありません。</p>
  </blockquote>
</div>

## ステップ 3.1 - Snort

セキュリティー環境でのネットワーク侵入検出および侵入防止システムを自動化する方法を紹介するために、このラボでは、Snort IDS
インスタンスの管理について説明します。Snort はネットワークトラフィックを分析し、これを特定のルールセットと比較します。このラボでは、Snort は
Red Hat Enterprise Linux マシンにインストールされ、Ansible は SSH 経由で RHEL
ノードにアクセスして対話します。

## ステップ 3.2 - Snort サーバーへのアクセス

Snort インストールに接続するには、インストールされているマシンの IP アドレスを確認する必要があります。続いて、Snort マシンの IP アドレスを取得するには、インベントリーファイル `~/lab_inventory/hosts` に関する情報を検索します。VS Code のオンラインエディターで、メニューバーの **File** > **Open File...** をクリックして `/home/student<X>/lab_inventory/hosts` ファイルを開き、以下のような snort のエントリーを検索して確認します。

```bash
snort ansible_host=22.333.44.5 ansible_user=ec2-user private_ip=172.16.1.2
```

> **注記**
>
> ここに記載されている IP アドレスはデモ目的のもので、お客様のケースとは異なります。お使いのラボ環境には、専用の Snort セットアップがあります。

Snort サーバーへの接続は、制御ホストに事前にインストールされた SSH 鍵を使用します。Snort サーバーのユーザーは `ec2-user`
です。VS Code のオンラインエディターでターミナルを開き、以下のように snort サーバーにアクセスします。

```bash
[student<X>@ansible-1 ~]$ ssh ec2-user@snort
Warning: Permanently added '22.333.44.5' (ECDSA) to the list of known hosts.
Last login: Mon Aug 26 12:17:48 2019 from h-213.61.244.2.host.de.colt.net
[ec2-user@snort ~]$
```

snort が正しくインストールされ、設定されていることを確認するには、sudo で呼び出してバージョンを要求します。

```bash
[ec2-user@snort ~]$ sudo snort --version

   ,,_     -*> Snort! <*-
  o"  )~   Version 2.9.13 GRE (Build 15013)
   ''''    By Martin Roesch & The Snort Team: http://www.snort.org/contact#team
           Copyright (C) 2014-2019 Cisco and/or its affiliates. All rights reserved.
           Copyright (C) 1998-2013 Sourcefire, Inc., et al.
           Using libpcap version 1.5.3
           Using PCRE version: 8.32 2012-11-30
           Using ZLIB version: 1.2.7
```

また、サービスが `sudo systemctl` 経由でアクティブに実行されているかどうかを確認します。

```bash
[ec2-user@snort ~]$ sudo systemctl status snort
● snort.service - Snort service
   Loaded: loaded (/etc/systemd/system/snort.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2019-08-26 17:06:10 UTC; 1s ago
 Main PID: 17217 (snort)
   CGroup: /system.slice/snort.service
           └─17217 /usr/sbin/snort -u root -g root -c /etc/snort/snort.conf -i eth0 -p -R 1 --pid-path=/var/run/snort --no-interface-pidfile --nolock-pidfile
[...]
```

> **注記**
>
> snort サービスが実行されていない可能性があります。このデモ環境では問題ありませんが、もし実行されていない場合は、`systemctl restart snort` で再起動し、再度ステータスを確認してください。実行されているはずです。

Snort サーバーを終了するには、`CTRL` および `D` を押すか、コマンドラインで `exit`
と入力します。追加の対話はすべて、Ansible コントロールホストから Ansible 経由で行われます。

## ステップ 3.3: Snort の簡単なルール

最も基本的なキャパシティーでは、Snort はいくつかのルールを読み取り、それらに従って動作することで機能します。このラボでは、Snort
の簡単な例を使用して、Ansible でこの設定を自動化する方法を紹介します。このセッションは、Snort
ルールの詳細や大規模な設定に伴う複雑さについては扱いませんが、簡単なルールの基本構造を理解することで、何を自動化するのかを認識することができます。

ルールはルールヘッダーとルールオプションで構成され、ファイルに保存されます。

Snort のルールヘッダーは以下のように分かれています。

- アクション - TCP などを探すプロトコル - IP やポートなどのソース情報 - IP やポートなどの宛先情報

Snort ルールオプションは `;` で区切られたキーワードで、以下のようになります。

- ルールが一致するときに出力するメッセージ - SID (ルールの一意識別子)、パケットペイロードで検索するコンテンツ (疑わしい文字列など) -
バイナリーデータを確認するバイトテスト - ルールのリビジョン - "priority" と呼ばれる攻撃の重大度 -
ルールを他のルールとより適切にグループ化するための "classtype" と呼ばれる事前に定義された攻撃タイプ - その他。

すべてのオプションが必須ではなく、既存のデフォルト値を上書きするだけのものもあります。

Snort ルールの概要は以下のようになります。

```
[action][protocol][sourceIP][sourceport] -> [destIP][destport] ( [Rule options] )
```

Snort ルールの詳細は、[Snort Rule
Infographic](https://www.snort.org/documents/snort-rule-infographic) または
Snort Users Manual
(PDF)](https://www.snort.org/documents/snort-users-manual). を確認してください。また、実際の
Snort のルールを確認したい場合は、ラボの Snort インストールにアクセスして、`/etc/snort/rules`
ディレクトリーの内容を見ることもできます。

## ステップ 3.4: Playbook の例

前述したように、Ansible の自動化については Playbook で説明されています。Playbook はタスクで構成されています。各タスクは、モジュールとモジュールの対応するパラメーターを使用して、必要な変更や、必要な状態を記述します。

Ansible リリースにはモジュールのセットが同梱されていますが、Ansible Core 2.11 には、Snort
と対話するためのモジュールがまだありません。このため、Snort を管理するためのモジュールのセットを作成し、`security_ee`
実行環境に含めました。実行環境を使用すると、モジュールの更新時間が短縮されます。これは、新たに開発されたモジュールの初期段階で特に重要です。

これらの Snort モジュールは "role" の一部として同梱されます。ロールをよりよく説明するには、最後のセクションで Playbook
をどのように書いたかを考えてみましょう。Playbook は以前のように 1 つのファイルに書くことができますが、多くの場合、すべての自動化部分を 1
つの場所に書くと、長くて複雑な Playbook が作成されます。ある時点で、すでに Playbook
に書いた自動化コンテンツを再利用したくなるでしょう。したがって、複数の小さな Playbook
を組み合わせて連携させるためには、これらを整理する必要があります。これを実現する方法が Ansible ロールです。ロールを作成すると、Playbook
が複数のパーツに分けられ、それらのパーツはディレクトリー構造に置かれます。

ロールを使用して自動化を作成する利点は複数あります。最も注目すべき点は、複雑さと Playbook
のインテリジェンスがユーザーから非表示になっていることです。もう 1 つの重要な利点は、ロールを簡単に共有して再利用できることです。

Snort の使用例に戻ります。前述のように、Snort モジュールはロールの一部として出荷されます。このロールは
[ids_rule](https://github.com/ansible-security/ids_rule). と呼ばれます。Web ブラウザーで
Github
リポジトリーのリンクを開き、[library](https://github.com/ansible-security/ids_rule/tree/master/library)
パスをクリックします。そこには、モジュール `snort_rule.py` があります。`ids_rule`
ロールの一部として出荷されたこのモジュールは、snort のルールを作成および変更することができます。

ロールの詳細を確認すると、[tasks/snort.yml](https://github.com/ansible-security/ids_rule/blob/master/tasks/snort.yml).
に再利用可能な Playbook が付属していることがわかります。

ここでは、この Playbook を書き換えて、ロールを直接使用する方法を見てみましょう。前述の通り、`ids_rule` ロールは
`security_ee` 実行環境にバンドルされています。

ロールを使用するには、オンラインエディターで `add_snort_rule.yml`
という名前の新しいファイルを作成します。これをユーザーのホームディレクトリーに保存して、名前 `Add Snort rule` とターゲットホストを
`snort` に追加します。Snort で変更を行うために root 権限が必要なため、Ansible が権限昇格を処理するように `become`
フラグを追加します。

```yaml
---
- name: Add Snort rule
  hosts: snort
  become: true
```

次に、Playbook で必要な変数を追加する必要があります。使用するロールは、複数の IDS プロバイダーと連携できる方法で書かれており、ユーザーが
IDS の名前を入力するだけで、あとはロールが処理してくれます。ここでは Snort IDS を管理しているので、`ids_provider`
変数の値を `snort` に設定する必要があります。

```yaml
---
- name: Add Snort rule
  hosts: snort
  become: true

  vars:
    ids_provider: snort
```

次にタスクを追加する必要があります。タスクはターゲットマシンで実際の変更を加えるコンポーネントです。ここではロールを使用しているため、タスクの中の 1
つのステップ `include_role` を使用するだけで、Playbook に追加することができます。

>注記
>
> Ansible `include_role` モジュールは、指定されたロールをタスクとして動的に読み込み、実行します。詳細は、 [include_role documentation](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/include_role_module.html) を参照してください.


ここでは、`include_role` モジュールを使用して `ids_rule` ロールを使用します。

ユースケースに適したロールにするためには、以下のタスク固有の変数を追加します。

- 実際のルール - Snort ルールファイル (present または absent のルールの状態)

```yaml
---
- name: Add Snort rule
  hosts: snort
  become: true

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

ここで何が起こっているのかを簡単に見てみましょう。ルールヘッダーは `alert tcp any any -> any any` なので、任意のソースから任意の宛先に tcp トラフィックに対するアラートを作成します。
ルールオプションは、ルールが一致した場合に、人間が判読できる Snort メッセージを定義します。`uricontent` は、`content` の特殊バージョンで、URI の分析を容易にします。`classtype` は、"attempted user privilege gain" のデフォルトクラスである `attempted-user` に設定されます。SID は、ユーザー定義のルールに十分な高い値に設定されています。優先順位は `1` で、最後に、このルールの最初のバージョンであるため、リビジョンを `1` に設定します。

他の変数 `ids_rules_file` および `ids_rule_state`
は、ルールファイルのユーザー定義の場所を提供し、ルールが存在しない場合にルールを作成する必要があることを示します(`present`)。

## ステップ 3.5: Playbook の実行

VS Code のオンラインエディターで、Playbook を実行します。ターミナルで以下のコマンドを実行します。

```bash
[student1@ansible-1 ~]$ ansible-navigator run add_snort_rule.yml --mode stdout

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

この Playbook の実行時に分かるように、ルールの追加に加えて多数のタスクが実行されます。たとえば、ロールは、ルールの追加後に Snort
サービスを再読み込みします。その他のタスクでは、変数の定義と検証が行われることを確認します。

このことからも、ロールを使用することの価値がわかります。ロールを活用することで、コンテンツを再利用できるようになるだけでなく、検証タスクやその他の重要なステップを追加して、それらをロールの中にきちんと隠しておくことができます。このロールのユーザーは、セキュリティー自動化の一環としてこのロールを使用するために、Snort
の仕組みの詳細を知る必要はありません。

## ステップ 3.6: 変更の確認

ルールが正しく書き込まれたかどうかを確認する簡単な方法は、Snort サーバーに SSH
で接続し、`/etc/snort/rules/local.rules` ファイルの内容を確認することです。

もう 1 つの方法は、コントロールホストで Ansible を使用することです。そのためには、Snort
のルールがあるかどうかを検証するために、別のロールを使います。このロールは Snort
で既存のルールを検索し、[ids_rule_facts](http://github.com/ansible-security/ids_rule_facts).
と呼ばれます。このロールは、`security_ee` 実行環境に含まれています。

VS Code のオンラインエディターで、Playbook `verify_attack_rule.yml`
を作成し、これを使用します。Playbook の名前を "Verify Snort rule" などのように設定します。ホスト、IDS
プロバイダー変数、および `become` フラグの値は、以前の Playbook と同じ値に設定できます。

```yaml
---
- name: Verify Snort rule
  hosts: snort
  become: yes

  vars:
    ids_provider: snort
```

次に、ロール `ids_rule_facts`
をインポートします。また、検索文字列を指定して、検索するルールを識別する必要があります。この例では、作成したルールを考慮すると、`uricontent`
ルールオプションをこの目的で使用することが理にかなっています。

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
>注記
>
> Ansible `import_role` タスクは、ロールを読み込み、プレイの他のタスク間でロールタスクが実行されるタイミングを制御できます。詳細は、[import_role documentation](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/import_role_module.html) を参照してください。

そして最も重要なのは、実際に見つかったものを確認できるようにすることです。`ids_rule_facts` は、収集したデータを Ansible
ファクトとして保存します。Ansible
ファクトは、個々のホストに固有の情報であり、今後のタスクで利用することができます。そこで、これらのファクトを出力するために、別のタスクを追加します。

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

次に、Playbook を実行して、ルールが Snort インストールに含まれていることを確認します。

```bash
[student<X>@ansible-1 ~]$ ansible-navigator run verify_attack_rule.yml --mode stdout

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

最後のタスクは、ロールによって見つかったルールを出力します。ご覧のように、以前に追加したのはルールです。

おめでとうございます。Ansible で Snort を自動化する最初のステップを完了しました。演習の概要に戻り、次のステップに進みます。

----

**Navigation**
<br><br>
[Previous Exercise](../1.2-checkpoint/README.md) | [Next Exercise](../1.4-qradar/README.md) 
<br><br>
[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md)
