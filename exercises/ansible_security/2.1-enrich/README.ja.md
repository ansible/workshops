# 演習 2.1 - 調査の強化

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

## ステップ 1.1 - 背景

前のセクションでは、単一のツールと、それらを Ansible
で自動化する方法に焦点を当てましたが、セキュリティー担当者の日常業務では、もう少し踏み込んだ方法が必要となります。何か疑わしいことが発生し、さらに注意が必要な場合、セキュリティー操作では、企業の
IT
を保護するために多くのツールをデプロイする必要があります。多くの企業環境では、セキュリティーソリューションは相互に統合されておらず、大規模な組織では、さまざまなチームが
IT
セキュリティーのさまざまな側面を担当しており、共通のプロセスはありません。そのため、多くの場合、異なるチームのメンバー間での手作業ややりとりが必要となり、エラーが発生しやすい上、時間もかかります。

セキュリティー侵害の防止には、複数の利害関係者が関与しており、サイバー攻撃が成功した場合は、セキュリティー侵入を可能な限り迅速に修正します。

どのような人物が関わっているのかを簡単に見てみましょう。

| Persona 	| Tasks 	| Challenges 	|
|---	|---	|---	|
| Chief Information Security Officer (CISO) 	| Manage the risk and ensure that security incidents are effectively handled.<br>Create a security ops program. 	| I have multiple teams managing security in silos. Security is not integrated into larger IT practices and landscape. 	|
| Security Operator 	| Reduce the change delivery time.<br>Enable the escalation of potential threats. 	| I receive an increasing number of requests from Governance, SOC and ITOps that I don’t have time to review and execute. 	|
| Security Analyst 	| Increase the number of events analysed and streamline the coordination of remediation processes. 	| Attacks are becoming more frequent, faster and complex. The tools I use don’t live up to expectations. 	|

Ansible Automation Platform
を使用して、前のセクションで学んだやりとりのレベルを引き上げて、セキュリティーツールを自動化されたワークフローに統合します。

## ステップ 1.2 - 準備

この演習が正しく動作するには、前の [Check Point 演習](../1.2-checkpoint/README.md)
で、いくつかの手順が完了していることを確認する必要があります。

1. `whitelist_attacker.yml` Playbook は、少なくとも 1 回実行されている必要があります。
2. また、攻撃者のホワイトリストポリシーのロギングが、Check Point SmartConsole でアクティベートされている必要があります。

いずれも [Check Point 演習](../1.2-checkpoint/README.md)
で行いました。これらの手順を飛ばしている場合は、手順に戻って Playbook
を実行し、手順に従ってロギングをアクティベートしてから、こちらに戻ってきてください。

`ibm.qradar` コレクションおよび `ids_rule` ロールを使用して、前の Snort 演習から IDS ルールを変更します。

次に、これはセキュリティーラボなので、疑わしいトラフィック、つまり攻撃が必要です。ここでは、5 秒ごとに単純なアクセスをシミュレートする
Playbook を用意し、この演習の他のコンポーネントが後に反応するようにします。VS Code
オンラインエディターで、ユーザーのホームディレクトリーに以下の内容の Playbook `web_attack_simulation.yml`
を作成します。

<!-- {% raw %} -->
```yml
---
- name: start attack
  hosts: attacker
  become: yes
  gather_facts: no

  tasks:
    - name: simulate attack every 5 seconds
      shell: "/sbin/daemonize /usr/bin/watch -n 5 curl -m 2 -s http://{{ hostvars['snort']['private_ip2'] }}/web_attack_simulation"
```
<!-- {% endraw %} -->

Playbook を実行します。

```bash
[student@ansible-1 ~]$ ansible-navigator run web_attack_simulation.yml --mode stdout
```

> **注記**
>
> 基本的に、この Playbook では、5 秒ごとにコマンドを実行する watch を実行する小さなデーモンを登録します。これは繰り返しのタスクを開始するためのかなり厳しい方法ですが、このラボの目的を果たします。

これで準備は完了しました。このユースケースの概要を知るには、次へと進んでください。

## ステップ 1.3 - 異常の確認

あなたは、ある企業のセキュリティーアナリストだとします。たった今、あるアプリケーションの異常を知らされました。VS Code
オンラインエディターのターミナルから、snort マシンに ssh します。

VS Code オンラインエディターで新しいターミナルを開き、SSH 経由で Snort サーバーに接続します。

> **注記**
>
> Snort サーバーのログインユーザーとして、`ec2-user` を使用する必要があります。

ログイン後、異常なログエントリーに対して grep を実行します。

```bash
[student@ansible-1 ~]$ ssh ec2-user@snort
Last login: Sun Sep 22 15:38:36 2019 from 35.175.178.231
[ec2-user@snort ~]$ sudo grep web_attack /var/log/httpd/access_log
172.17.78.163 - - [22/Sep/2019:15:56:49 +0000] "GET /web_attack_simulation HTTP/1.1" 200 22 "-" "curl/7.29.0"
...
```

Snort サーバーからログアウトするには、`exit` コマンドを実行するか、`CTRL` と `D` を同時に押します。

> **注記**
>
> もうお分かりかもしれませんが、このログエントリーは、この演習のはじめに起動したデーモンによって 5 秒ごとにトリガーされます

セキュリティーアナリストであるあなたは、異常は侵入やその他の深刻な原因の兆候である可能性があることを認識しています。あなたは調査することにしました。今のところ、この異常を誤検出と断定するには十分な情報がありません。したがって、ファイアウォールや
IDS などから、より多くのデータポイントを収集する必要があります。ファイアウォールと IDS
のログを手作業で調べるのは、非常に時間がかかります。大規模な組織では、セキュリティーアナリストは必要なアクセス権さえ持っていない可能性があり、企業のファイアウォールと
IDS
の両方を担当するチームと連絡をとり、それぞれのログを手動で調べて異常を直接チェックし、その結果を返信するよう依頼する必要があります。この作業には数時間から数日かかることもあります。

## ステップ 1.4: 新規のログソースを作成するための Playbook の作成

SIEM を使用する場合は、ログを一元的に収集および分析できるので、状況は改善されます。この場合、SIEM は QRadar です。QRadar
には、他のシステムからログを収集し、疑わしいアクティビティーを検索する機能があります。では、QRadar ではどのようにログを分析するのでしょうか?
これらのログを確認する前に、それらを QRadar にストリーミングする必要があります。これには 2 つの手順があります。まず、ソース (Check
Point および Snort) を設定してログを QRadar に転送する必要があります。次に、これらのシステムをログソースとして QRadar
に追加する必要があります。

これを手作業で行うには、複数のマシンで多くの作業を行う必要があり、やはり時間がかかる上に、セキュリティーアナリストが持っていない権限が必要になる場合もあります。しかし、Ansible
では、セキュリティー組織が事前に承認した自動化ワークフローを Playbook の形で作成することができます。Playbook
は、一元的に管理し、さまざまなチームで共有することで、ボタンを押すだけでセキュリティーワークフローを実現することもできます。Playbook
を使えば、セキュリティーアナリストとして、エンタープライズファイアウォールと IDS の両方を自動的に設定し、イベントやログを QRadar
インスタンスに送信することができます。これにより、データを相互に関連付け、疑わしいアプリケーションをどのように進めるかを決定することができます。

> **注記**
>
> それらのログを QRadar に永続的に追加しないのはなぜでしょうか? それは、多くのログシステムは消費するログの量によってライセンス/料金が決まるため、必要のないログを押し込むと、膨大な量となってしまうからです。また、ログが多すぎると、データを適切かつタイムリーに分析することが難しくなります。

では、まずログソース (Snort および Check Point) を設定して、ログを QRadar に送信し、その後これらのログソースを
QRadar に追加して QRadar が認識できるようにする Playbook を作成してみましょう。

いつものように、Playbook には名前と実行するホストが必要です。今回のワークフローでは、異なるマシンで作業を行うため、Playbook を異なる
"[plays](https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html#playbook-language-example)"
に分けることにします。

> プレイの目的は、ホストのグループをいくつかの明確に定義されたロールにマップすることです。これは、Ansible がタスクと呼ぶものによって表されます。基本的なレベルでは、タスクは Ansible モジュールの呼び出しにすぎません。

これは、"host" のセクションが 1 つの Playbook に複数回表示され、各セクションに専用のタスクリストがあることを意味します。

まず、Snort の設定から始めましょう。QRadar サーバーにログを送信するためには、Snort
のログサーバーが必要です。これは、[ids_config](https://github.com/ansible-security/ids_config)
という既存のロールで設定できますので、あとはロールをインポートして、適切なパラメーターで使用するだけです。

`security_ee` カスタム実行環境には、`ids_config` ロールが含まれます。

では、ロールを使用する Playbook を作成してみましょう。VS Code オンラインエディターで、以下の内容で
`enrich_log_sources.yml` ファイルを作成します。

<!-- {% raw %} -->
```yaml
---
- name: Configure snort for external logging
  hosts: snort
  become: true
  vars:
    ids_provider: "snort"
    ids_config_provider: "snort"
    ids_config_remote_log: true
    ids_config_remote_log_destination: "{{ hostvars['qradar']['private_ip'] }}"
    ids_config_remote_log_procotol: udp
    ids_install_normalize_logs: false

  tasks:
    - name: import ids_config role
      include_role:
        name: "ansible_security.ids_config"
```
<!-- {% endraw %} -->

ご覧のとおり、前回の Snort
ルールの設定と同様に、ロールを再利用して、あとはロールに任せています。パラメーターを介して変更するのは、ロールの動作だけです。QRadar の IP
を変数で指定して、IDS プロバイダーを `snort` に設定し、パッケージが `UDP` として送信されるプロトコルを定義します。

ここで、この新しい Snort ログソースがあることを QRadar に知らせる必要があります。以下のプレイを Playbook
`enrich_log_sources.yml` に追加します。

<!-- {% raw %} -->
```yaml
- name: Add Snort log source to QRadar hosts: qradar collections:
    - ibm.qradar

  tasks:
    - name: Add snort remote logging to QRadar
      qradar_log_source_management:
        name: "Snort rsyslog source - {{ hostvars['snort']['private_ip'] }}"
        type_name: "Snort Open Source IDS"
        state: present
        description: "Snort rsyslog source"
        identifier: "{{ hostvars['snort']['ansible_fqdn'] }}"
```
<!-- {% endraw %} -->

次に、Check Point についても同じことを行う必要があります。ログを QRadar に転送するように Check Point
を設定する必要があります。これは、既存のロールである
[log_manager](https://github.com/ansible-security/log_manager).
で設定できます。`ids_config` ロールと同様に、`security_ee` 実行環境には `log_manager` が含まれます。

ここで、Snort と QRadar をすでにまとめた既存の Playbook `enrich_log_sources.yml`
を再度編集し、Check Point の別のセクションを追加します。

<!-- {% raw %} -->
```yaml
- name: Configure Check Point to send logs to QRadar
  hosts: checkpoint

  tasks:
    - include_role:
        name: ansible_security.log_manager
        tasks_from: forward_logs_to_syslog
      vars:
        syslog_server: "{{ hostvars['qradar']['private_ip'] }}"
        checkpoint_server_name: "YOURSERVERNAME"
        firewall_provider: checkpoint
```
<!-- {% endraw %} -->

このスニペットでは、`YOURSERVERNAME` を、`gw-77f3f6` などの Check Point
管理インスタンスの実際のサーバー名に置き換える必要があることに注意してください。SmartConsole にログインすると、個々の Check
Point インスタンスの名前を見つけることができます。これは、画面の下部分にある **Summary** の下の **GATEWAYS &
SERVERS** タブに表示されます。

![Check Point Gateway Name](images/check_point_gw_name.png#centreme)

Playbook の文字列 `YOURSERVERNAME` を、個別の名前に置き換えます。

> **注記**
>
> これは、2 つの API 呼び出しで自動的に実行できますが、ここでの Playbook の一覧が複雑になってしまいます。

ここで、別のログソース (今回は Check Point ) があることを QRadar に知らせる必要があります。以下のプレイを Playbook
`enrich_log_sources.yml` に追加します。

<!-- {% raw %} -->
```yaml
- name: Add Check Point log source to QRadar hosts: qradar collections:
    - ibm.qradar

  tasks:
    - name: Add Check Point remote logging to QRadar
      qradar_log_source_management:
        name: "Check Point source - {{ hostvars['checkpoint']['private_ip'] }}"
        type_name: "Check Point FireWall-1"
        state: present
        description: "Check Point log source"
        identifier: "{{ hostvars['checkpoint']['private_ip'] }}"

    - name: deploy the new log source
      qradar_deploy:
        type: INCREMENTAL
      failed_when: false
```
<!-- {% endraw %} -->

前回の QRadar プレイと比較して、今回は `deploy the new log source`
というタスクが追加されていることに注意してください。これは、QRadar
の変更がスプールされ、追加のリクエストがあった場合にのみ適用されるという事実によるものです。エラーは、API 呼び出しの実際の機能に影響を与えない
REST API のタイムアウトにより発生する可能性があるため、無視しています。

これらのすべての部分をまとめると、Playbook `enrich_log_sources.yml` 全体は以下のようになります。

<!-- {% raw %} -->
```yaml
---
- name: Configure snort for external logging
  hosts: snort
  become: true
  vars:
    ids_provider: "snort"
    ids_config_provider: "snort"
    ids_config_remote_log: true
    ids_config_remote_log_destination: "{{ hostvars['qradar']['private_ip'] }}"
    ids_config_remote_log_procotol: udp
    ids_install_normalize_logs: false

  tasks:
    - name: import ids_config role
      include_role:
        name: "ansible_security.ids_config"

- name: Add Snort log source to QRadar
  hosts: qradar
  collections:
    - ibm.qradar

  tasks:
    - name: Add snort remote logging to QRadar
      qradar_log_source_management:
        name: "Snort rsyslog source - {{ hostvars['snort']['private_ip'] }}"
        type_name: "Snort Open Source IDS"
        state: present
        description: "Snort rsyslog source"
        identifier: "{{ hostvars['snort']['ansible_fqdn'] }}"

- name: Configure Check Point to send logs to QRadar
  hosts: checkpoint

  tasks:
    - include_role:
        name: ansible_security.log_manager
        tasks_from: forward_logs_to_syslog
      vars:
        syslog_server: "{{ hostvars['qradar']['private_ip'] }}"
        checkpoint_server_name: "YOURSERVERNAME"
        firewall_provider: checkpoint

- name: Add Check Point log source to QRadar
  hosts: qradar
  collections:
    - ibm.qradar

  tasks:
    - name: Add Check Point remote logging to QRadar
      qradar_log_source_management:
        name: "Check Point source - {{ hostvars['checkpoint']['private_ip'] }}"
        type_name: "Check Point FireWall-1"
        state: present
        description: "Check Point log source"
        identifier: "{{ hostvars['checkpoint']['private_ip'] }}"

    - name: deploy the new log sources
      qradar_deploy:
        type: INCREMENTAL
      failed_when: false
```
<!-- {% endraw %} -->

> **注記**
>
> 上記のように、値 `YOURSERVERNAME` を実際のサーバー名に置き換えることを忘れないでください。

## ステップ 1.5: ログ転送を有効化するための Playbook の実行

完全な Playbook を実行して、両方のログソースを QRadar に追加します。

```bash
[student@ansible-1 ~]$ ansible-navigator run enrich_log_sources.yml --mode stdout
```
Check Point SmartConsole では、進捗状況を知らせる小さなウィンドウが、左下隅にポップアップ表示されるされることもあります。

![Check Point progress](images/2.1-checkpoint-progress.png#centreme)

>注記
>
>それが10％で止まった場合、通常は無視しても問題ありません。ログエクスポーターは、いずれにせよ機能します。



## ステップ 1.6: ログソース設定の確認

Ansible Playbook が呼び出される前は、QRadar は Snort または Check Point
からデータを受信していませんでした。直後に、セキュリティーアナリストである私たちの介入なしに、Check Point のログが QRadar
ログの概要に表示され始めます。

QRadar Web UI にログインし、**Log Activity** をクリックします。ご覧のとおり、常にたくさんのログが入ってきています。

> **IBM QRadar Credentials**  
> Username: `admin`  
> Password: `Ansible1!`

![QRadar Log Activity showing logs from Snort and Check
Point](images/qradar_log_activity.png#centreme)

これらのログの多くは、実際には QRadar の内部ログです。概要を把握するには、ログリストの中央上にある **Display**
の隣のドロップダウンメニューをクリックします。エントリーを **Raw Events** に変更します。

次に、その上のメニューバーで、緑色のじょうごマークと **Add Filter**
というテキストが表示されているボタンをクリックします。**Parameter** として **Log Source [Indexed]**
を選び、**Operator** として **Equals any of** を選びます。次に、ログソースのリストから、**Check Point
source** を選び、右側の小さなプラスボタンをクリックします。同様に **Snort rsyslog source** を選び、**Add
Filter** ボタンを押します。

![QRadar Log Activity showing logs from Snort and Check
Point](images/qradar_filter_logs.png#centreme)

>**注記**
>
> この時点では、Check Point のログのみが表示されます。Snort ログは、この演習の後半のいくつかのステップを完了した後でのみ、QRadar に表示されます。

これで、ログのリストが分析しやすくなりました。Check Point から QRadar にイベントが送信されていることを確認します。QRadar
が新しいログソースを完全に適用するには、数秒必要な場合があります。新しいログソースが完全に設定されるまでは、受信するログには、未知のログに対する「デフォルト」のログソースがあり、これは
**SIM GENERIC LOG DSM-7** と呼ばれます。このデフォルトのログソースからのログが表示された場合は、1、2
分待ってください。この待ち時間の後、新しいログソースの設定が正しく適用され、QRadar はログを正しいログソース (ここでは Check Point)
に帰属させます。

また、**View** を **Real Time** から **Last 5 Minutes**
などに変更すると、個別のイベントをクリックして、ファイアウォールから送られてくるデータの詳細を見ることもできます。

QRadar がログソースもきちんと表示するか確認してみましょう。QRadar の UI で、左上隅の「ハンバーガーボタン」(3本の横棒)
をクリックしてから、下にある **Admin** をクリックします。

![QRadar hamburger](images/2-qradar-hamburger.png#centreme)

そこで、**Log Sources** をクリックします。  

![QRadar log sources](images/2-qradar-log-sources.png#centreme)

新しいウィンドウが開き、新しいログソースが表示されます。

![QRadar Log Sources](images/2-qradar-log-sources-window.png#centreme)

Check Point で、ログソースが設定されているかどうかを確認する最も簡単な方法は、実際にコマンドラインを使用することです。VS Code
オンラインエディタのターミナルから、SSH を使用して Check Point の管理サーバー IP にユーザー admin でログインし、次の
`ls` コマンドを実行します。

```bash
[student@ansible-1 ~]$ ssh admin@checkpoint_mgmt
[Expert@gw-77f3f6:0]# ls -l /opt/CPrt-R80/log_exporter/targets
total 0
drwxr-xr-x 6 admin root 168 Sep 16 11:23 syslog-22.33.44.55
```

ご覧のとおり、中央のログサーバーは Check Point の内部ログエクスポーターツールを介して設定されました。Check Point
サーバーを離れ、コントロールホストに戻ります。

また、バックグランドでの Snort の設定が成功したことを確認しましょう。VS Code オンラインエディターのターミナルから、`ec2-user`
ユーザーとして SSH で Snort インスタンスにログインします。root になり、rsyslog の転送設定を確認します。

```bash
[student@ansible-1 ~]$ ssh ec2-user@snort
Last login: Wed Sep 11 15:45:00 2019 from 11.22.33.44
[ec2-user@snort ~] sudo cat /etc/rsyslog.d/ids_confg_snort_rsyslog.conf
$ModLoad imfile
$InputFileName /var/log/snort/merged.log
$InputFileTag ids-config-snort-alert
$InputFileStateFile stat-ids-config-snort-alert
$InputFileSeverity alert
$InputFileFacility local3
$InputRunFileMonitor
local3.* @44.55.66.77:514
```

Snort サーバーを再び離れて、コントロールホストに戻ります。

今のところ、Snort から QRadar にはログが送られていない点に留意してください。Snort
は、このトラフィックが注目に値することをまだ認識していません。

しかし、セキュリティーアナリストとしては、自由に使えるデータが増えたことで、アプリケーションの異常な動作の原因の可能性について、ようやく以前よりも把握できるようになりました。ファイアウォールのログを確認し、誰が誰にトラフィックを送っているのかを確認できますが、イベントを誤検出と見なすのに十分なデータはまだありません。

## ステップ 1.7 - Snort 署名の追加

この異常が誤検出であるかどうかを判断するためには、セキュリティーアナリストとして、潜在的な攻撃をすべて除外する必要があります。手元にあるデータをもとに、IDS
に新しい署名を実装し、そのようなトラフィックが再び検出された場合に、警告ログを取得することにします。

一般的な状況では、新しいルールの実装には、Snort を担当するセキュリティーオペレーターと再度やりとりする必要があります。しかし幸運なことに、今回も
Ansible Playbook を使って、数時間や数日ではなく数秒で、同じ目的を達成することができます。

前回の Snort の演習では、より多くの情報を得るために、署名で Snort ルールを既に追加していたので、Playbook
を再利用して、ルールのデータだけを変更することができます。VS Code オンラインエディターで、ユーザーのホームディレクトリーに
`enrich_snort_rule.yml` というファイルを作成し、以下の内容を記述します。

<!-- {% raw %} -->
```yaml
---
- name: Add Snort rule
  hosts: snort
  become: yes

  vars:
    ids_provider: snort
    protocol: tcp
    source_port: any
    source_ip: any
    dest_port: any
    dest_ip: any

  tasks:
    - name: Add snort web attack rule
      include_role:
        name: "ansible_security.ids_rule"
      vars:
        ids_rule: 'alert {{protocol}} {{source_ip}} {{source_port}} -> {{dest_ip}} {{dest_port}}  (msg:"Attempted Web Attack"; uricontent:"/web_attack_simulation"; classtype:web-application-attack; sid:99000020; priority:1; rev:1;)'
        ids_rules_file: '/etc/snort/rules/local.rules'
        ids_rule_state: present
```
<!-- {% endraw %} -->

このプレイでは、TCP 上のトラフィックを制御する必要があるという内容の変数を Snort に提供します。その後、`ids_rule`
ロールを利用して、`web_attack_simulation`
文字列をコンテンツとして含む新しいルールを設定することで、今後発生するであろうこの動作を特定できるようになります。

それでは、Playbook を実行します。

```bash
[student@ansible-1 ~]$ ansible-navigator run enrich_snort_rule.yml --mode stdout
```

新しいルールが実際に追加されたことをすぐに確認してみましょう。VS Code オンラインエディターのターミナルから、Snort サーバーに
`ec2-user` として ssh で接続、カスタムルールのディレクトリーを見てみます。

```bash
[student@ansible-1 ~]$ ssh ec2-user@snort
Last login: Fri Sep 20 15:09:40 2019 from 54.85.79.232
[ec2-user@snort ~]$ sudo grep web_attack /etc/snort/rules/local.rules
alert tcp any any -> any any  (msg:"Attempted Web Attack"; uricontent:"/web_attack_simulation"; classtype:web-application-attack; sid:99000020; priority:1; rev:1;)
```

## ステップ 1.8: オフェンスを特定して閉じる

Playbook が実行された数分後に、QRadar
でオフェンスが表示されているかどうかを確認できます。そして、実際に表示されていることがわかりました。QRadar の UI にログインして
**Offenses** をクリックし、続いて左側の**All Offenses**をクリックします。

![QRadar Offenses](images/qradar_offenses.png#centreme)

これらの情報が手元にあれば、これでようやくこのタイプのすべてのオフェンスをチェックして、それらがすべて 1
つのホスト、つまり攻撃者からのみ発生していることを確認することができます。

次のステップは、そのマシンを担当しているチームと連絡を取り、その動作について話し合うことです。このデモでは、そのマシンのチームが、この動作は本当に必要なものであり、セキュリティーアラートは誤検出であるというフィードバックを提供したと仮定します。したがって、QRadar
のオフェンスを退けることができます。

Offense ビューで Offense をクリックし、上部のメニューの **Actions** をクリックして、ドロップダウンメニューで
**close** をクリックします。ウィンドウがポップアップ表示されますので、追加情報を入力し、最後に誤検出としてオフェンスをクローズします。

## ステップ 1.9 - ロールバック

最後のステップでは、すべての設定変更を調査前の状態にロールバックし、リソースの消費を抑え、私たちと他のセキュリティーアナリストの分析ワークロードの負担を軽減します。また、攻撃シミュレーションを停止する必要があります。

`enrich_log_sources.yml` に基づいて新しい Playbook `rollback.yml`
を作成します。主な違いは、QRadar の場合はログソースの状態を `absent` に設定し、Snort の場合は
`ids_config_remote_log` を `false` に設定し、Check Point の場合は
`unforward_logs_to_syslog` のタスクを開始することです。

Playbook `rollback.yml` には、以下の内容が必要です。

<!-- {% raw %} -->
```yaml
---
- name: Disable external logging in Snort
  hosts: snort
  become: true
  vars:
    ids_provider: "snort"
    ids_config_provider: "snort"
    ids_config_remote_log: false
    ids_config_remote_log_destination: "{{ hostvars['qradar']['private_ip'] }}"
    ids_config_remote_log_procotol: udp
    ids_install_normalize_logs: false

  tasks:
    - name: import ids_config role
      include_role:
        name: "ansible_security.ids_config"

- name: Remove Snort log source from QRadar
  hosts: qradar
  collections:
    - ibm.qradar

  tasks:
    - name: Remove snort remote logging from QRadar
      qradar_log_source_management:
        name: "Snort rsyslog source - {{ hostvars['snort']['private_ip'] }}"
        type_name: "Snort Open Source IDS"
        state: absent
        description: "Snort rsyslog source"
        identifier: "{{ hostvars['snort']['ansible_fqdn'] }}"

- name: Configure Check Point to not send logs to QRadar
  hosts: checkpoint

  tasks:
    - include_role:
        name: ansible_security.log_manager
        tasks_from: unforward_logs_to_syslog
      vars:
        syslog_server: "{{ hostvars['qradar']['private_ip'] }}"
        checkpoint_server_name: "YOURSERVERNAME"
        firewall_provider: checkpoint

- name: Remove Check Point log source from QRadar
  hosts: qradar
  collections:
    - ibm.qradar

  tasks:
    - name: Remove Check Point remote logging from QRadar
      qradar_log_source_management:
        name: "Check Point source - {{ hostvars['checkpoint']['private_ip'] }}"
        type_name: "Check Point NGFW"
        state: absent
        description: "Check Point log source"
        identifier: "{{ hostvars['checkpoint']['private_ip'] }}"

    - name: deploy the log source changes
      qradar_deploy:
        type: INCREMENTAL
      failed_when: false
```
<!-- {% endraw %} -->

> **注記**
>
> ここでも、`YOURSERVERNAME` の値を Check Point インスタンスの実際のサーバー名に置き換えることを忘れないでください。

この Playbook
は、今回の演習の中で最も長いものになるかもしれませんが、その構造や内容はすでにおなじみのものになっているはずです。少し時間をとって各タスクに目をとおし、何が起きているのかを理解してください。

>**注記**
>
> `rollback.yml` Playbook を実行する前に、現在のすべての ssh セッションを終了し、**control-node** プロンプトを開いていることを確認してください。

Playbook を実行してログソースを削除します。

```bash
[student@ansible-1 ~]$ ansible-navigator run rollback.yml --mode stdout
```

また、Web 攻撃をシミュレートするプロセスを停止する必要があります。`shell` モジュールを使用して **attacker**
マシンで実行しているプロセスを停止する簡単な Playbook を作成してみましょう。

`shell`
モジュールを使用していますが、これは、[piping](https://www.redhat.com/sysadmin/pipes-command-line-linux).
を使用することができるからです。シェルパイピングでは、プロセスを停止するために必要な複数のコマンドを連鎖させることができます。

VS Code オンラインエディターを使用して `stop_attack_simulation.yml` という新しい Playbook
を作成し、以下の内容を追加してみましょう。

<!-- {% raw %} -->
```yaml
---
- name: stop attack simulation
  hosts: attacker
  become: yes
  gather_facts: no

  tasks:
    - name: stop attack process
      shell: >
        sleep 2;ps -ef | grep -v grep | grep -w /usr/bin/watch | awk '{print $2}'|xargs kill &>/dev/null; sleep 2
```
<!-- {% endraw %} -->
次に、`stop_attack_simulation.yml` Playbook を実行します。
<!-- {% raw %} -->
```bash
[student@ansible-1 ~]$ ansible-navigator run stop_attack_simulation.yml --mode stdout
```
<!-- {% endraw %} -->

これで演習は終わりました。次の演習に進むには、演習のリストへ戻ってください。

----
**Navigation**
<br><br>
[Previous Exercise](../1.3-snort/README.md) | [Next Exercise](../2.2-threat/README.md)
<br><br>
[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md)
