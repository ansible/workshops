# 演習 2 - 初めての Ansible プレイブック

**他の言語でもお読みいただけます**: ![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English](README.md)、![japan](https://github.com/ansible/workshops/raw/devel/images/japan.png) [日本語](README.ja.md), ![Español](https://github.com/ansible/workshops/raw/devel/images/es.png) [Español](README.es.md)


## 目次

* [目的](#objective)
* [ガイド](#guide)
   * [ステップ 1 - Ansible Playbook の検証](#step-1---examine-ansible-playbook)
   * [ステップ 2 - Ansible Playbook の実行](#step-2---execute-ansible-playbook)
   * [ステップ 3 - ルーターの設定の確認](#step-3---verify-configuration-on-router)
   * [ステップ 4 - べき等性の検証](#step-4---validate-idempotency)
   * [ステップ 5 - Ansible Playbook の変更](#step-5---modify-ansible-playbook)
   * [ステップ 6 - チェックモードの使用](#step-6---use-check-mode)
   * [ステップ 7 - 設定が存在しないことの確認](#step-7---verify-configuration-is-not-present)
   * [ステップ 8 - Ansible Playbook の再実行](#step-8---re-run-the-ansible-playbook)
   * [ステップ 9 - 設定が適用されていることの確認](#step-9---verify-configuration-is-applied)
* [重要なこと](#takeaways)
* [ソリューション](#solution)
* [完了](#complete)

## 目的

Ansible を使用して、ルーターの構成を更新します。この演習では、Ansible Playbook は作成しませんが、提供されている既存の
Playbook を使用します。

この演習では、以下について説明します。

* 既存の AnsiblePlaybook の検証
* `ansible-navigator` コマンドを使用したコマンドラインでの AnsiblePlaybook の実行
* チェックモード (`--check` パラメーター)
* 詳細モード (`--verbose` または `-v` パラメーター)

## ガイド

### ステップ 1 - Ansible Playbook の検証

`network-workshop` ディレクトリーに移動していない場合は、移動します。

```bash
[student@ansible ~]$ cd ~/network-workshop/
[student@ansible network-workshop]$
[student@ansible network-workshop]$ pwd
/home/student/network-workshop
```

`playbook.yml` という名前の提供された Ansible Playbook を調べます。Visual Studio Code
でファイルを開くか、または `cat` でファイルの中身を表示します。

```yaml
---
- name: snmp ro/rw string configuration
  hosts: cisco
  gather_facts: no

  tasks:

    - name: ensure that the desired snmp strings are present
      cisco.ios.config:
        commands:
          - snmp-server community ansible-public RO
          - snmp-server community ansible-private RW
```

* `cat` - ファイルの内容を表示できる Linux コマンド
* `playbook.yml` - 提供された Ansible Playbook

次の演習では、Ansible Playbook のコンポーネントについて詳しく説明します。今のところ、このハンドブックが 2 つの
CiscoIOS-XE コマンドを実行することを確認するだけで十分です。

```sh
snmp-server community ansible-public RO
snmp-server community ansible-private RW
```

### ステップ 2 - Ansible Playbook の実行

`ansible-navigator` コマンドを使用して Playbook を実行します。完全なコマンドは ``ansible-navigator
run playbook.yml --mode stdout`` です

```bash
[student@ansible-1 network-workshop]$ ansible-navigator run playbook.yml --mode stdout

PLAY [snmp ro/rw string configuration] *****************************************

TASK [ensure that the desired snmp strings are present] ************************
changed: [rtr1]

PLAY RECAP *********************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

[student@ansible-1 network-workshop]$
```

* `--mode stdout` - デフォルトでは、`ansible-navigator` は対話モードで実行されます。デフォルトの動作は
  `ansible-navigator.yml` を変更することで変更できます。Playbook
  が長くなり複数のホストが関係するようになると、対話モードではデータをリアルタイムに「ズームイン」し、絞り込み、さまざまな Ansible
  コンポーネント間の移動を行うことができます。このタスクは、1 つのホストで 1 つのタスクのみを実行するため、`stdout` で十分です。

### ステップ 3 - ルーターの設定の確認

Ansible Playbook が機能したことを確認します。`rtr1` にログインし、CiscoIOS-XE デバイスで実行設定を確認します。

```bash
[student@ansible network-workshop]$ ssh rtr1

rtr1#show run | i snmp
snmp-server community ansible-public RO
snmp-server community ansible-private RW
```

### ステップ 4 - べき等性の検証

`cisco.ios.config`
モジュールはべき等です。つまり、構成の変更は、その構成がエンドホストに存在しない場合にのみ、デバイスにプッシュされます。

> Ansible Automation の用語についてサポートが必要ですか?  
>
> べき等性などの用語について詳しく知るには、[用語集](https://docs.ansible.com/ansible/latest/reference_appendices/glossary.html) を確認してください。

冪等性の概念を検証するには、Playbook を再実行します。

```bash
[student@ansible-1 network-workshop]$ ansible-navigator run playbook.yml --mode stdout

PLAY [snmp ro/rw string configuration] *****************************************

TASK [ensure that the desired snmp strings are present] ************************
ok: [rtr1]

PLAY RECAP *********************************************************************
rtr1                       : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

> 注意:
>
> **PLAY RECAP** の **changed** パラメーターが変更がないことを示していることを確認してください。

Ansible Playbook を複数回再実行すると、**ok=1** と **change=0**
で、まったく同じ出力になります。別のオペレーターまたはプロセスが rtr1 の既存の設定を削除または変更しない限り、この AnsiblePlaybook
は **ok=1** を報告し続け、設定が既に存在し、ネットワークデバイスで正しく構成されていることを示します。

### ステップ 5 - Ansible Playbook の変更

次に、タスクを更新して、`ansible-test` という名前の SNMPRO コミュニティ文字列をもう 1 つ追加します。

```sh
snmp-server community ansible-test RO
```

Visual Studio Code を使用して `playbook.yml` ファイルを開き、コマンドを追加します。


Ansible Playbook は次のようになります。

```yaml
---
- name: snmp ro/rw string configuration
  hosts: cisco
  gather_facts: no

  tasks:

    - name: ensure that the desired snmp strings are present
      cisco.ios.config:
        commands:
          - snmp-server community ansible-public RO
          - snmp-server community ansible-private RW
          - snmp-server community ansible-test RO
```

必ず、変更を加えた `playbook.yml` を保存します。

### ステップ 6 - チェックモードの使用

ただし、今回は、Playbook を実行して変更をデバイスにプッシュする代わりに、`--check` フラグを `-v`
または冗長モードフラグと組み合わせて使用して実行します。

```bash
[student@ansible-1 network-workshop]$ ansible-navigator run playbook.yml --mode stdout --check -v
Using /etc/ansible/ansible.cfg as config file

PLAY [snmp ro/rw string configuration] *****************************************

TASK [ensure that the desired snmp strings are present] ************************
changed: [rtr1] => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python"}, "banners": {}, "changed": true, "commands": ["snmp-server community ansible-test RO"], "updates": ["snmp-server community ansible-test RO"], "warnings": ["To ensure idempotency and correct diff the input configuration lines should be similar to how they appear if present in the running configuration on device"]}

PLAY RECAP *********************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

`--check` モードと `--verbose`
フラグを組み合わせると、実際に変更をプッシュすることなく、エンドデバイスにデプロイされる正確な変更が表示されます。これは、デバイスをプッシュする前に、デバイスにプッシュしようとしている変更を検証するための優れた手法です。

### ステップ 7 - 設定が存在しないことの確認

Ansible Playbook が `ansible-test` コミュニティーを適用していないことを確認します。`rtr1`
にログインし、CiscoIOS-XE デバイスの実行設定を確認します。

```bash
[student@ansible network-workshop]$ ssh rtr1

rtr1#show run | i snmp
snmp-server community ansible-public RO
snmp-server community ansible-private RW
```

### ステップ 8 - Ansible Playbook の再実行

最後に、変更をプッシュするために、`-v` または `--check` フラグを指定せずにこの Playbook を再実行します。

```bash
[student@ansible-1 network-workshop]$ ansible-navigator run playbook.yml --mode stdout

PLAY [snmp ro/rw string configuration] *****************************************

TASK [ensure that the desired snmp strings are present] ************************
changed: [rtr1]

PLAY RECAP *********************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

### ステップ 9 - 設定が適用されていることの確認

Ansible Playbook が **ansible-test** コミュニティーを適用したことを確認します。`rtr1`
にログインし、CiscoIOS-XE デバイスの実行設定を確認します。

```bash
[student@ansible network-workshop]$ ssh rtr1

rtr1#sh run | i snmp
snmp-server community ansible-public RO
snmp-server community ansible-private RW
snmp-server community ansible-test RO
```

## 重要なこと

* **config** (例：cisco.ios.config) モジュールはべき等であり、ステートフルであることを意味します
* **check mode** により、Ansible Playbook がリモートシステムに変更を加えなくなります
* **verbose mode** を使用すると、適用されるコマンドを含め、ターミナルウィンドウへの出力をより多く表示できます。
* この AnsiblePlaybook は、構成を実施するために **自動コントローラー** でスケジュールできます。たとえば、これは、Ansible
  Playbook を特定のネットワークに対して 1 日 1 回実行できることを意味します。**check mode**と
  組み合わせると、ネットワーク上で設定が欠落しているか変更されているかどうかを確認して報告する、読み取り専用の Ansible Playbook
  となります。

## ソリューション

こちらには、完成した Ansible Playbook があります [playbook.yml](../playbook.yml)。

## 完了

ラボ演習 2 を完了しました

---
[前の演習](../1-explore/README.ja.md) | [次の演習](../3-facts/README.ja.md)

[Ansible Network Automation ワークショップに戻る](../README.ja.md)
