# ワークショップ演習 - デバッグとエラーハンドリング

**他の言語で読む** :
<br>![uk](../../../images/uk.png) [英語](README.md), ![japan](../../../images/japan.png) [日本語](README.ja.md), ![brazil](../../../images/brazil.png) [ブラジルのポルトガル語](README.pt-br.md), ![france](../../../images/fr.png) [フランス語](README.fr.md), ![Español](../../../images/col.png) [スペイン語](README.es.md).

## 目次

- [目的](#目的)
- [ガイド](#ガイド)
  - [ステップ 1 - Ansibleでのデバッグ入門](#ステップ-1---Ansibleでのデバッグ入門)
  - [ステップ 2 - デバッグモジュールの利用](#ステップ-2---デバッグモジュールの利用)
  - [ステップ 3 - ブロックによるエラーハンドリング](#ステップ-3---ブロックによるエラーハンドリング)
  - [ステップ 4 - 詳細モードでの実行](#ステップ-4---詳細モードでの実行)
  - [まとめ](#まとめ)

## 目的

これまでの演習で得た基礎知識を基に、このセッションではAnsible内でのデバッグとエラーハンドリングに焦点を当てます。プレイブックのトラブルシューティング、エラーの上手な管理、堅牢で信頼性の高い自動化を実現するためのテクニックを学びます。

## ガイド

### ステップ 1 - Ansibleでのデバッグ入門

デバッグは、Ansibleプレイブック内の問題を特定し解決するための重要なスキルです。Ansibleはデバッグモジュール、詳細度レベルの増加、エラーハンドリング戦略など、自動化スクリプトのデバッグを支援するいくつかのメカニズムを提供します。

### ステップ 2 - デバッグモジュールの利用

`debug` モジュールは、変数の値を出力するためのシンプルだが強力なツールであり、プレイブックの実行フローを理解する上で重要です。

この例では、変数の値またはメッセージを出力するデバッグタスクを `tasks/main.yml` のApacheロールに追加します。

#### デバッグタスクの実装 :

変数の値やカスタムメッセージを表示するデバッグタスクを挿入します :

```yaml
- name: Display Variable Value
  ansible.builtin.debug:
    var: apache_service_name

- name: Display Custom Message
  ansible.builtin.debug:
    msg: "Apacheサービス名は {{ apache_service_name }} です"
```

### ステップ 3 - ブロックによるエラーハンドリング

Ansibleでは `block` を使用してタスクをグループ化し、`rescue` セクションでエラーを処理できます。これは伝統的なプログラミングのtry-catchに似ています。

この例では、`tasks/main.yml` ファイル内でApacheの設定中に発生する可能性のあるエラーを処理するためのブロックを追加します。

1. タスクのグループ化とエラーの処理 :

失敗する可能性のあるタスクをブロックでラップし、エラーを処理するためのレスキューセクションを定義します :

```yaml
- name: Apache Configuration with Potential Failure Point
  block:
    - name: Copy Apache configuration
      ansible.builtin.copy:
        src: "{{ apache_conf_src }}"
        dest: "/etc/httpd/conf/httpd.conf"
  rescue:
    - name: Handle Missing Configuration
      ansible.builtin.debug:
        msg: "Apache設定ファイル '{{ apache_conf_src }}' が見つかりません。デフォルト設定を使用します。"
```

2. apacheロールの `vars/main.yml` 内に `apache_conf_src` 変数を追加します。

```yaml
apache_conf_src: "files/missing_apache.conf"
```

> 注: このファイルは意図的に存在しないため、`tasks/main.yml` のレスキュー部分をトリガーすることができます。

### ステップ 4 - 詳細モードでの実行

Ansibleの詳細モード(-v, -vv, -vvv, -vvvv)は出力の詳細度を高め、プレイブックの実行と潜在的な問題に関するより多くの洞察を提供します。

#### 詳細モードでプレイブックを実行 :

詳細なログを取得するために `-vv` オプションを使用してプレイブックを実行します :

```bash
ansible-navigator run deploy_apache.yml -m stdout -vv
```

```
.
.
.

TASK [apache : Display Variable Value] *****************************************
task path: /home/rhel/ansible-files/roles/apache/tasks/main.yml:20
ok: [node1] => {
    "apache_service_name": "httpd"
}
ok: [node2] => {
    "apache_service_name": "httpd"
}
ok: [node3] => {
    "apache_service_name": "httpd"
}

TASK [apache : Display Custom Message] *****************************************
task path: /home/rhel/ansible-files/roles/apache/tasks/main.yml:24
ok: [node1] => {
    "msg": "Apacheサービス名は httpd です"
}
ok: [node2] => {
    "msg": "Apacheサービス名は httpd です"
}
ok: [node3] => {
    "msg": "Apacheサービス名は httpd です"
}

TASK [apache : Copy Apache configuration] **************************************
task path: /home/rhel/ansible-files/roles/apache/tasks/main.yml:30
タスク実行中に例外が発生しました。完全なトレースバックを見るには -vvv を使用してください。エラーは次の通りです : モジュールを使用していて、ファイルがリモートに存在することを期待している場合は、remote_srcオプションを確認してください
fatal: [node3]: FAILED! => {"changed": false, "msg": "'files/missing_apache.conf' を見つけることができないかアクセスできません\n検索された場所:\n\t/home/student/lab_inventory/roles/apache/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/missing_apache.conf\n\t/home/student/lab_inventory/files/files/missing_apache.conf\n\t/home/student/lab_inventory/files/missing_apache.conf on the Ansible Controller.\nモジュールを使用していて、ファイルがリモートに存在することを期待している場合は、remote_srcオプションを確認してください"}
fatal: [node1]: FAILED! => {"changed": false, "msg": "'files/missing_apache.conf' を見つけることができないかアクセスできません\n検索された場所:\n\t/home/student/lab_inventory/roles/apache/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/missing_apache.conf\n\t/home/student/lab_inventory/files/files/missing_apache.conf\n\t/home/student/lab_inventory/files/missing_apache.conf on the Ansible Controller.\nモジュールを使用していて、ファイルがリモートに存在することを期待している場合は、remote_srcオプションを確認してください"}
fatal: [node2]: FAILED! => {"changed": false, "msg": "'files/missing_apache.conf' を見つけることができないかアクセスできません\n検索された場所:\n\t/home/student/lab_inventory/roles/apache/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/missing_apache.conf\n\t/home/student/lab_inventory/files/files/missing_apache.conf\n\t/home/student/lab_inventory/files/missing_apache.conf on the Ansible Controller.\nモジュールを使用していて、ファイルがリモートに存在することを期待している場合は、remote_srcオプションを確認してください"}


TASK [apache : Handle Missing Configuration] ***********************************
task path: /home/rhel/ansible-files/roles/apache/tasks/main.yml:39
ok: [node1] => {
    "msg": "'files/missing_apache.conf' のApache設定ファイルが見つかりません。デフォルト設定を使用します。"
}
ok: [node2] => {
    "msg": "'files/missing_apache.conf' のApache設定ファイルが見つかりません。デフォルト設定を使用します。"
}
ok: [node3] => {
    "msg": "'files/missing_apache.conf' のApache設定ファイルが見つかりません。デフォルト設定を使用します。"
}

PLAY RECAP *********************************************************************
node1                      : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0
node2                      : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0
node3                      : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0

```

プレイブックがApache設定ファイルのコピー中にエラーが発生したこと、しかし提供されたレスキューブロックを通じてそれを処理できたことを示しています。最終タスク「Handle Missing Configuration」はファイルが見つからず、デフォルト設定を使用することを詳述しています。

最終的なプレイリキャップは、Webグループのノードごとに `rescued=1` を介して使用されたレスキューブロックがあることを示しています。

## まとめ

この演習では、Ansibleでの重要なデバッグ技術とエラーハンドリングメカニズムを探求しました。デバッグタスクを組み込み、エラーハンドリングのためにブロックを使用し、詳細モードを活用することで、Ansibleプレイブックのトラブルシューティングを効果的に行い、信頼性を向上させることができます。これらの実践は、予期しない問題を優雅に処理し、一貫性のある予測可能な結果を保証する堅牢なAnsible自動化を開発するための基礎です。

---
**ナビゲーション**
<br>
[前の演習](../1.7-role/README.ja.md) - [次の演習](../2.1-intro/README.ja.md)

[Red Hat Enterprise LinuxのためのAnsibleワークショップに戻る](../README.md#section-1---ansible-engine-exercises)

