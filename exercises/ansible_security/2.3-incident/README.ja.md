# 演習 2.3 - Incident response

**Read this in other languages**: <br>
[![uk](../../../images/uk.png) English](README.md),  [![japan](../../../images/japan.png) 日本語](README.ja.md), [![france](../../../images/fr.png) Français](README.fr.md).<br>

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

Playbook を実行できるようにするため `ids_rule` に、前回の Snort の演習で行ったように、用意された Role を使用して IDS ルールを変更します。それを逃していた場合には、次の方法でインストールしてください。
`ansible-galaxy install ansible_security.ids_rule`

同じことが Role の `ids.config` にも当てはまります。
`ansible-galaxy install ansible_security.ids_config`

Playbook を実行します:

```bash
[student<X>@ansible ~]$ ansible-playbook incident_snort_rule.yml
```

これらのルールでログを生成するには、疑わしいトラフィック、つまり攻撃が必要です。繰り返しになりますが、Tower を介して攻撃シミュレーションを開始できます。ブラウザを開き、Tower インスタンスへのリンクを入力します。提供された student ID とパスワードを使用してログインします。

左側のナビゲーションバーで、**Templates** をクリックします。テンプレートのリストで、右のロケットアイコンをクリックして、**Start SQL injection simulation** と呼ばれるテンプレートを見つけて実行します。これにより、数秒ごとに攻撃がシミュレートされます。これでTower ブラウザタブを閉じることができます。この演習では、これを再度必要とすることはありません。

また、QRadar コレクションも必要です。これは前回の QRadar 演習で既にインストールされています。その部分を見逃した場合は、次の方法でインストールしてください。`ansible-galaxy collection install ibm.qradar`

また、両方のマシン間のトラフィックを通過させるには、最初の Check Point の演習で2つのことを完了させておく必要があります: 最初に、Playbook `whitelist_attacker.yml` を実行する必要があります。次に、攻撃者のホワイトリストポリシーのロギングが有効になっている必要があります。これらの手順をやり逃した場合は、最初の Check Point 演習に戻り、Playbook を作成して実行し、手順に従ってロギングを有効にしてから、ここに戻ってください。

これで舞台は整いました。このユースケースが何であるかを学ぶためにお読みください。

## Step 3.3 - インシデントを特定する

企業の IDS を担当するセキュリティオペレータとして、あなたは日常的にログを確認します。VS Code オンラインエディタのターミナルから、ユーザ `ec2-user` として Snort ノードに SSH で接続し、ログを表示します:

```bash
[ec2-user@ip-172-16-11-22 ~]$ journalctl -u snort -f
-- Logs begin at Sun 2019-09-22 14:24:07 UTC. --
Sep 22 21:03:03 ip-172-16-115-120.ec2.internal snort[22192]: [1:99000030:1] Attempted SQL Injection [Classification: Attempted Administrator Privilege Gain] [Priority: 1] {TCP} 172.17.78.163:53376 -> 172.17.23.180:80
Sep 22 21:03:08 ip-172-16-115-120.ec2.internal snort[22192]: [1:99000030:1] Attempted SQL Injection [Classification: Attempted Administrator Privilege Gain] [Priority: 1] {TCP} 172.17.78.163:53378 -> 172.17.23.180:80
Sep 22 21:03:13 ip-172-16-115-120.ec2.internal snort[22192]: [1:99000030:1] Attempted SQL Injection [Classification: Attempted Administrator Privilege Gain] [Priority: 1] {TCP} 172.17.78.163:53380 -> 172.17.23.180:80
```

ご覧のように、このノードは **Attempted Administrator Privilege Gain** の複数のアラートを登録しました。`CTRL-C` を押してログビューを終了します。

Snort ログの詳細をさらに詳しく知りたい場合は、Snortマシン上のファイル `/var/log/snort/merged.log` の内容を確認してください:

```bash
[ec2-user@ip-172-16-180-99 ~]$ sudo tail -f /var/log/snort/merged.log
Accept: */*
[...]
GET /sql_injection_simulation HTTP/1.1
User-Agent: curl/7.29.0
Host: 172.17.30.140
Accept: */*
```
一部の奇妙な文字に加えて、ユーザの実際の不正な「攻撃」が `sql_injection_simulation` という文字列の形で表示されます。`exit` コマンドで Snort サーバから抜けます。

## Step 3.4 - ログを QRadar に転送するための Playbook を作成し実行する

このインシデントをより良く分析するためには、他のソースとデータを相関させることが重要です。そのためには、ログを SIEM である QRadar に与えたいと考えています。

ご存知のように、様々なセキュリティツールがお互いに統合されていないため、IDS を担当するセキュリティオペレータは、別チームに手動で連絡を取るか、電子メールでログを転送しなければなりません。あるいは、FTP サーバーにアップロードしたり、最悪の場合は USB スティックを持ち運んだりしなければなりません。幸いにも、前の演習で示したように、Ansible を使って Snort と Qradar を設定することができます。

VS Code オンラインエディタで、`incident_snort_log.yml` という Playbook を以下のように作成します:

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

この Playbook は見慣れているはずです。Snort が QRadar にログを送信するように設定し、QRadar がログを受信するように設定し、Offence を有効にします。それを実行してください:

```bash
[student<X>@ansible ~]$ ansible-playbook incident_snort_log.yml
```

## Step 3.5 - QRadar の新しい設定を確認する

パースペクティブを簡単にセキュリティアナリストの視点に変更しましょう。主に SIEM を使用しており、Snort からログを取得しています。これを確認するには、QRadar UI にアクセスして、**Log Activity** タブを開いて、イベントが Snort から QRadar に送信されていることを確認します。

![QRadar logs view, showing logs from Snort](images/qradar_incoming_snort_logs.png)

QRadar ログビューにフィルターを追加すると、より良い概要を得ることができます。これらのログには、すでに左側にオフェンスマーカーが表示されていることに注意してください！

> **Note**
>
> ログが表示されない場合は少し待ってください。最初のエントリが表示されるまでに1分以上かかるかもしれません。また、最初のログは "デフォルト "のログソース（**Snort rsyslog source**ではなく**SIM Generic Log DSM-7**と表示されます）で識別される可能性がありますので、少し時間をおいてください。

**Offence** タブで、**Error Based SQL Injection** のオフェンスのリストをフィルタリングします。オフェンスサマリーを開いて、以前に Snort ログで確認した攻撃者の IP アドレスの詳細を確認します。

## Step 3.6 - ブラックリスト IP

手元にある全ての情報から、このイベントは攻撃であると確信しています。だから防ぎましょう！攻撃者のソース IP を ブラックリストに登録します。

一般的な環境では、この改善策を実行するには、ファイアウォールを担当するセキュリティオペレータとのやりとりが必要になります。しかし、数時間や数日ではなく、数秒で同じ目標を達成するためには Ansible の Playbook を起動することで実現できます。

VS Code オンラインエディタで `incident_blacklist.yml` というファイルを作成します。Ansible はすでにインベントリからの情報があるため、ここでは IP アドレスではなく変数を入力することに注意してください。

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

Playbookを実行し、IP アドレスを効果的にブラックリストに登録します:

```bash
[student<X>@ansible ~]$ ansible-playbook incident_blacklist.yml
```

QRadar UI の、**Log Activity** タブで Snort からのアラートを受信していないことを確認してください。ファイアウォールを QRadar に接続した場合、実際にはそこからログが入ってくることに注意してください。

また、Check Point に新しいルールが追加されたことを簡単に確認してみましょう。Windows ワークステーションにアクセスし、SmartConsole インターフェイスを開きます。左側の [**SECURITY POLICIES**] をクリックして、アクセス制御ポリシーのエントリが **Accept** から **Drop** に変更されていることに注意してください。

![SmartConsole Blacklist Policy](images/check_point_policy_drop.png)

攻撃を特定し、攻撃の原因となるトラフィックをブロックすることに成功しました！

## Step 3.7 - ロールバック

最後のステップとして、ロールバック Playbook を実行して Snort の設定を元に戻し、リソースの消費と分析のワークロードを削減できます。

前の演習で書いた Playbook `rollback.yml` を実行して、すべての変更をロールバックします。

```bash
[student<X>@ansible ~]$ ansible-playbook rollback.yml
```

今回は QRadar のログソースとして Check Point を設定していませんが、Playbook は問題なく実行されることに注目してください。Ansible のタスクの多くは冪等性があるので、タスクを何度も実行しても、目的の状態を確保することができます。

最後に、攻撃シミュレーションを停止する必要があります。student ユーザーとして Tower にログインします。**Templates** セクションで、**Stop sql injection simulation** と呼ばれるジョブテンプレートを見つけて実行します。

これで最後の練習は終了です。おめでとう！

## Step 3.8 - まとめ

必要なツールが揃っていても、ツール同士が統合されていないため、CISO とそのチームの仕事は難しいです。セキュリティ違反が発生した場合、アナリストはトリアージを行い、インフラストラクチャ全体にわたって関連するすべての情報を追跡し、何が起きているのかを理解し、最終的にはあらゆる種類の修正を実行する必要があります。

Ansible Security Automation は、共通のオープンな自動化言語である Ansible を通じて、幅広いセキュリティソリューションの統合を促進するRed Hatの取り組みです。Ansible Security Automation は、セキュリティアナリストがセキュリティインシデントをより迅速に調査および修正できるように設計されています。

Ansible Security Automation は、エンタープライズファイアウォール、IDS、SIEM の3つの異なるセキュリティ製品を統合して、セキュリティアナリストやオペレータがInvestigation Enrichment、Threat hunting、Incident response に役立ちます。

Ansible Security Automation を使用すると、セキュリティ組織は、事前承認された Playbook と呼ばれる自動化ワークフローを作成できます。また、Ansible Tower のサポートにより、これらの自動化ワークフローを、制御されたユーザーフレンドリーで使いやすい方法で他のチームに提供することもできます。

----

[Ansible Security Automation Workshopの表紙に戻る](../README.ja.md)
