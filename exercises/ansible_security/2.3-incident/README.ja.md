# Exercise 2.3 - インシデントレスポンス

## Step 3.1 - 背景

この演習では、脅威の検出と対応能力に焦点を当てます。いつものように、セキュリティオペレータは、このタスクを実行するためにエンタープライズ IT の一連のツールを必要とします。

あなたは企業の IDS を担当するセキュリティオペレーターです。私たちの選択した IDS は Snort です。

## Step 3.2 - 準備

この演習では、Snort でログを見る操作から始めます。まず最初に実際にログエントリを生成するための Snort ルールを設定する必要があります。VS Code オンラインエディタで、Playbook を作成して実行します `incident_snort_rule.yml` :

<!-- {% raw %} -->
```yml
---
- name: Add ids signature for sql injection simulation
  hosts: ids
  become: yes

  vars:
    ids_provider: snort
    protocol: tcp
    source_port: any
    source_ip: any
    dest_port: any
    dest_ip: any

  tasks:
    - name: Add snort sql injection rule
      include_role:
        name: "ansible_security.ids_rule"
      vars:
        ids_rule: 'alert {{protocol}} {{source_ip}} {{source_port}} -> {{dest_ip}} {{dest_port}}  (msg:"Attempted SQL Injection"; uricontent:"/sql_injection_simulation"; classtype:attempted-admin; sid:99000030; priority:1; rev:1;)'
        ids_rules_file: '/etc/snort/rules/local.rules'
        ids_rule_state: present
```
<!-- {% endraw %} -->

Playbook を実行できるようにするため `ids_rule` に、前回の Snort の演習で行ったように、用意された Role を使用して IDS ルールを変更します。それを逃していた場合には、次の方法でインストールしてください。`ansible-galaxy install ansible_security.ids_rule`

同じことが Role の `ids.config` にも当てはまります。 `ansible-galaxy install ansible_security.ids_config`

Playbook を実行します:

```bash
[student<X>@ansible ~]$ ansible-playbook incident_snort_rule.yml
```

これらのルールでログを生成するには、疑わしいトラフィック、つまり攻撃が必要です。この演習の他のコンポーネントが後で反応する数秒ごとの単純なアクセスをシミュレートする Playbook があります。VS Code オンラインエディタで、以下の内容の Playbook `sql_injection_simulation.yml` を作成してください:

<!-- {% raw %} -->
```yml
---
- name: start sql injection simulation
  hosts: attacker
  become: yes
  gather_facts: no

  tasks:
    - name: simulate sql injection attack every 5 seconds
      shell: "/sbin/daemonize /usr/bin/watch -n 5 curl -m 2 -s http://{{ hostvars['snort']['private_ip2'] }}/sql_injection_simulation"
```
<!-- {% endraw %} -->

これを実行します:

```bash
[student<X>@ansible ~]$ ansible-playbook sql_injection_simulation.yml
```

また、QRadar コレクションも必要です。これは前回の QRadar 演習で既にインストールされています。その部分を見逃した場合は、次の方法でインストールしてください。`ansible-galaxy collection install ibm.qradar`

また、両方のマシン間のトラフィックを通過させるには、最初の Check Point の演習で2つのことを完了させておく必要があります: 最初に、Playbook `whitelist_attacker.yml` を実行する必要があります。次に、攻撃者のホワイトリストポリシーのロギングが有効になっている必要があります。これらの手順をやり逃した場合は、最初の Check Point 演習に戻り、Playbook を作成して実行し、手順に従ってロギングを有効にしてから、ここに戻ってください。

これで舞台は整いました。このユースケースが何であるかを学ぶためにお読みください。

## Step 3.3 - インシデントを特定する

企業の IDS を担当するセキュリティオペレータとして、あなたは日常的にログを確認します。VS Code オンラインエディタの端末から、ユーザ `ec2-user` として Snort ノードに SSH 接続し、ログを表示します:

```bash
[ec2-user@ip-172-16-11-22 ~]$ journalctl -u snort -f
-- Logs begin at Sun 2019-09-22 14:24:07 UTC. --
Sep 22 21:03:03 ip-172-16-115-120.ec2.internal snort[22192]: [1:99000030:1] Attempted SQL Injection [Classification: Attempted Administrator Privilege Gain] [Priority: 1] {TCP} 172.17.78.163:53376 -> 172.17.23.180:80
Sep 22 21:03:08 ip-172-16-115-120.ec2.internal snort[22192]: [1:99000030:1] Attempted SQL Injection [Classification: Attempted Administrator Privilege Gain] [Priority: 1] {TCP} 172.17.78.163:53378 -> 172.17.23.180:80
Sep 22 21:03:13 ip-172-16-115-120.ec2.internal snort[22192]: [1:99000030:1] Attempted SQL Injection [Classification: Attempted Administrator Privilege Gain] [Priority: 1] {TCP} 172.17.78.163:53380 -> 172.17.23.180:80
```

ご覧のように、このノードは**Attempted Administrator Privilege Gain**に対して複数のアラートを登録しました。CTRL-C`を押してログビューを残します。

snortログの詳細を詳しく見たい場合は、Snortマシン上のファイル `/var/log/snort/merged.log` の内容を確認してください:

```bash
[ec2-user@ip-172-16-180-99 ~]$ sudo tail -f /var/log/snort/merged.log
Accept: */*
[...]
GET /sql_injection_simulation HTTP/1.1
User-Agent: curl/7.29.0
Host: 172.17.30.140
Accept: */*
```
奇妙な文字の他に、ユーザの実際の不正な「攻撃」が `sql_injection_simulation` という文字列の形で表示されます。コマンド `exit` で Snort サーバを離れる。

## Step 3.4 - Create and run a playbook to forward logs to QRadar

このインシデントをより良く分析するためには、他のソースとデータを相関させることが重要です。そのためには、ログを当社のSIEMであるQRadarにフィードしたいと考えています。

ご存知のように、様々なセキュリティツールがお互いに統合されていないため、IDSを担当するセキュリティオペレータとしては、別のチームに手動で連絡を取るか、電子メールでログを転送しなければなりません。あるいは、FTPサーバーにアップロードしたり、USBスティックや最悪の場合は持ち運んだりしなければなりません。幸いにも、最後の演習で示したように、Ansibleを使ってSnortとQradarを設定することができます。

VS Codeのオンラインエディタで、`incident_snort_log.yml` というplaybookを以下のように作成します:

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
        identifier: "{{ hostvars['snort']['private_ip']|regex_replace('\\.','-')|regex_replace('^(.*)$', 'ip-\\1') }}"

    - name: deploy the new log sources
      qradar_deploy:
        type: INCREMENTAL
      failed_when: false
```
<!-- {% endraw %} -->

このplaybookは見覚えがあると思いますが、SnortがQRadarにログを送信するように設定し、QRadarがログを受信するように設定し、攻撃を有効にします。実行してください:

```bash
[student<X>@ansible ~]$ ansible-playbook incident_snort_log.yml
```

## Step 3.5 - Verify new configuration in QRadar

主にSIEMを使用していますが、Snortからログが入ってきました。それを確認するには、QRadar UIにアクセスして、**Log Activity**タブを開き、SnortからQRadarにイベントが発生していることを確認してください。

![QRadar logs view, showing logs from Snort](images/qradar_incoming_snort_logs.png)

QRadarログビューにフィルターを追加すると、より良い概観を得ることができます。これらのログには、すでに左側にオフェンスマーカーが表示されていることに注意してください!

> **Note**
>
> ログが表示されない場合は少し待ってください。最初のエントリが表示されるまでに1分以上かかるかもしれません。また、最初のログは "デフォルト "のログソース（**Snort rsyslog source**ではなく**SIM Generic Log DSM-7**と表示されます）で識別される可能性がありますので、少し時間をおいてください。

オフェンス] タブで、**Error Based SQL Injection** のオフェンスのリストをフィルタリングします。オフェンスサマリーを開いて、以前に Snort ログで確認した攻撃者の IP アドレスの詳細を確認します。

## Step 3.6 - Blacklist IP

手元にある全ての情報から、このイベントは攻撃であると確信しています。だから止めましょう! 攻撃者のソースIPを ブラックリストに登録します。

一般的な環境では、この改善策を実行するには、ファイアウォールを担当するセキュリティオペレータとのやりとりが必要になります。しかし、数時間や数日ではなく、数秒で同じ目標を達成するために Ansible のplaybookを起動することができます。

VS Code オンラインエディタで `incident_blacklist.yml` というファイルを作成します。ここでは IP アドレスは入力しませんが、Ansible はすでにインベントリからの情報を持っているので、ここでも変数を入力することに注意してください。

<!-- {% raw %} -->
```yaml
---
- name: Blacklist attacker
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

    - name: Create access rule to deny access from source to destination
      checkpoint_access_rule:
        auto_install_policy: yes
        auto_publish_session: yes
        layer: Network
        position: top
        name: "asa-accept-{{ source_ip }}-to-{{ destination_ip }}"
        source: "asa-{{ source_ip }}"
        destination: "asa-{{ destination_ip }}"
        action: drop

    - name: Install policy
      cp_mgmt_install_policy:
        policy_package: standard
        install_on_all_cluster_members_or_fail: yes
      failed_when: false
```
<!-- {% endraw %} -->

playbookを実行し、効果的にIPをブラックリストにするには:

```bash
[student<X>@ansible ~]$ ansible-playbook incident_blacklist.yml
```

QRadar UIで、ログアクティビティタブでSnortからのアラートを受信していないことを確認してください。ファイアウォールをQRadarに接続した場合、実際にはそこからログが入ってくることに注意してください。

また、チェック・ポイントに新しいルールが追加されたことをすばやく確認してみましょう。Windowsワークステーションにアクセスし、SmartConsoleインターフェイスを開きます。左側の[**SECURITY POLICIES**]をクリックして、アクセス制御ポリシーのエントリが**Accept**から**Drop**に変更されていることに注意してください。

![SmartConsole Blacklist Policy](images/check_point_policy_drop.png)

攻撃を識別し、攻撃の背後にあるトラフィックをブロックすることに成功しました!

## Step 3.7 - Roll back

最後のステップとして、ロールバックplaybookを実行してSnortの設定を元に戻すことで、リソースの消費と解析作業負荷を削減することができます。

前回の演習で書いたplaybook `rollback.yml` を実行して、すべての変更をロールバックします。

```bash
[student<X>@ansible ~]$ ansible-playbook rollback.yml
```

今回は QRadar のログソースとして Check Point を設定していませんが、playbookは問題なく実行されています。これは、Ansible のタスクの多くは、何度も何度も実行することができ、目的の状態を確保することができるからです。

また、我々は攻撃を送信するプロセスを殺す必要があります。あなたのVSコードのオンラインエディタのターミナルから、次のAnsibleのad-hocコマンドを実行します:

<!-- {% raw %} -->
```bash
[student1@ansible ~]$ ansible attacker -b -m shell -a "sleep 2;ps -ef | grep -v grep | grep -w /usr/bin/watch | awk '{print $2}'|xargs kill &>/dev/null; sleep 2"
attacker | CHANGED | rc=0 >>
```
<!-- {% endraw %} -->

もし、`Share connection to ... closed.`というエラーが出たら、心配しないでください: もう一度コマンドを実行してください。

これで最後の練習は終了です。おめでとうございます。

## Step 3.8 - Wrap it all up

必要なツールが揃っていても、ツール同士が統合されていないため、ＣＩＳＯとそのチームの仕事は難しい。セキュリティ侵害が発生した場合、アナリストはトリアージを行い、インフラ全体の関連情報を追いかけ、何が起きているのかを理解し、最終的に何らかの修復を行うのに何日もかかります。

Ansible Security Automationは、共通のオープンな自動化言語を通じて、幅広いセキュリティソリューションの統合を促進するRed Hatの取り組みです。Ansible を使用しています。Ansible Security Automation は、セキュリティアナリストがセキュリティインシデントの調査と修正を迅速に行えるように設計されています。

ansibleのセキュリティ自動化が、エンタープライズファイアウォール、IDS、SIEMの3つの異なるセキュリティ製品を統合して、セキュリティアナリストや運用者が調査の充実、脅威狩り、インシデント対応を行う際にどのように役立つかを紹介します。

Ansible Security Automation を使用すると、セキュリティ組織はplaybookと呼ばれる事前承認済みの自動化ワークフローを作成し、それを一元的に管理し、異なるチーム間で共有することができます。また、Tower の助けを借りて、これらの自動化ワークフローを管理されたユーザーフレンドリーでシンプルな方法で他のチームに提供することもできます。

----

[こちらをクリックし、Ansible Security Automation Workshop に戻ります](../README.md#section-2---ansible-security-automation-use-cases)
