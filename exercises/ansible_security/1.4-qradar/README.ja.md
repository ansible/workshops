# Exercise 1.4 - 最初の IBM QRadar playbook の実行

**Read this in other languages**: <br>
[![uk](../../../images/uk.png) English](README.md),  [![japan](../../../images/japan.png) 日本語](README.ja.md), [![france](../../../images/fr.png) Français](README.fr.md).<br>

## Step 4.1 - IBM QRadar

セキュリティ環境で SIEM を自動化する方法を紹介するために、このラボでは、[IBM QRadar SIEM, community edition](https://developer.ibm.com/qradar/ce/) が含まれています。

SIEM には、Web UI および REST API を介してアクセスすることができます。このラボでは、私たちが作成する Playbook はバックグラウンドで API と対話します。すべてのアクションは Web UI で検証されます。

## Step 4.2 - Web UI にアクセスする

最初に SIEM を見て、実際に動作していることを確認してください。Web ブラウザから `https://<qradar-IP>` にアクセスします。`<qradar-IP>` はインベントリの `siem` セクションにある `qradar` エントリの IP アドレスです。次に、証明書は自己署名されているため安全ではないという警告が表示されます。これを受け入れて次に進んでください。

> **Note**
>
> 本番環境では、安全でない証明書を受け入れることはできません。ラボのセットアップは短命であり、デモを目的としているだけなので、この場合のリスクを受け入れます。

ログインフィールドに、他に指示が無ければ、ユーザー名: **admin** とパスワード: **Ansible1!** を入力し、**login**ボタンを押します。

これで IBM QRadar のメイン Web インターフェイスが表示されます。

![QRadar main window](images/qradar-main-window.png)

QRadar と基本的な概念を理解するために、インターフェースを簡単に見てみましょう。上部には、QRadar の主要部分への複数のエントリー・ポイントがあるナビゲーション・バーがあります。

- **Dashboard**, 概要の一覧を表示
- **Offenses**, モニタリングにより生成されたイベントやメッセージの確認
- **Log Activity**, ログソースから収集したイベントの確認
- **Network Activity**, 特定ホスト間のネットワークトラフィックの確認
- **Assets**, 環境内のネットワークデバイスとホストのプロファイルを自動的に作成
- **Reports**, カスタマイズされたレポートや標準レポートを使用して、環境で何が起こっているかのレポート

デモのために、**Offenses** を詳しく見てみましょう: メニュー項目をクリックします。新しいウィンドウの左側に、違反をフィルタリングするためのナビゲーションバーが表示されます。

![QRadar offense window](images/qradar-offense-window.png)

> **Note**
>
> デモ環境のため、Offense のリストは現在空になっている可能性があります。

Offense は、悪意のあるログ行のようなログメッセージやネットワークトラフィックの発見に基づいて生成されるメッセージやイベントのことです。QRadar はルールに基づいて Offense をトリガーします。ルールには条件が記述されており、条件が満たされると Offense が発生します。

公式ドキュメントの説明は以下です:

> *相関ルールと呼ばれることもあるルールは、異常を検索または検出するために、イベント、フロー、または Offense に適用されます。テストのすべての条件が満たされた場合、ルールはレスポンスを生成します。([QRadar ドキュメント](https://www.ibm.com/support/knowledgecenter/en/SS42VS_7.3.2/com.ibm.qradar.doc/c_qradar_rul_mgt.html))*

本番環境では、時間の経過とともにカスタムルールを作成していくのが一般的です。ただしここでは、システムにすでにインストールされているルールを見てみます: **Offenses**  ウィンドウの左側のナビゲーションバーから **Rules** をクリックします。ルールの長いリストが表示されます。このリストの上部にある検索バーに、次の検索キーワードを入力してください: `DDoS`。リストをフィルタリングするには、その後に Enter キーを押してください。

リストはフィルタリングされており、DDoS に関連するいくつかのルールのみが表示されます。

![QRadar, filtered rules list](images/qradar-offenses-rules.png)

**"Potential DDoS Against Single Host (TCP)"** をクリックしてください。これは、この演習の後に関連しています。

QRadar を一目見たところで、次は Ansible でどのように自動化できるかを見てみます。

## Step 4.3 - QRadar モジュールと Ansible collections

最も基本的なレベルでは、Ansible の自動化はタスクを実行します。これらのタスクはモジュールを実行し、通常は特別なデバイスやプログラムの API エンドポイントのような対応するターゲットで動作します。

Ansible には多くのモジュールが付属しています。しかし、この記事を書いている時点では、Ansible は QRadar モジュールを提供していません。代わりに、それらのモジュールは [Ansible collections](https://docs.ansible.com/ansible/devel/dev_guide/collections_tech_preview.html) として提供されています:

> *Collections は Ansible コンテンツの配布フォーマットです。Collections は、Playbook 、Role 、Module 、および Plugin をパッケージ化して配布するために使用できます。Ansible Galaxy を通じて Collections を公開して使用することができます。*

Collections は、Ansible のコンテンツを提供するためのシンプルなディレクトリ構造に従っています。ここで Ansible の Role を思い出すかもしれませんが、これには理由があります。Collections は Role の概念に基づいて構築されていますが、その概念を一般的な Ansible コンテンツ管理にまで拡張しています。IBM QRadar 用のコレクションは [ansible-security project](https://github.com/ansible-security/ibm_qradar) にあります。

Role と同様に、Collections も使用する前に最初にインストールする必要があります。これらは Ansible を実行しているマシンにインストールされますが、ラボの場合はこれがコントロールホストです。

QRadar module の Collection をコントロールホストにインストールします。VS Code Online エディタで新しいターミナルを開きます。コマンド `ansible-galaxy collection --help` を実行して、Collections 機能が正しく動作していることを確認します:

```bash
[student<X>@ansible ~]$ ansible-galaxy collection --help
usage: ansible-galaxy collection [-h] COLLECTION_ACTION ...

positional arguments:
  COLLECTION_ACTION
    init             Initialize new collection with the base structure of a
                     collection.
    build            Build an Ansible collection artifact that can be publish
                     to Ansible Galaxy.
    publish          Publish a collection artifact to Ansible Galaxy.
    install          Install collection(s) from file(s), URL(s) or Ansible
                     Galaxy

optional arguments:
  -h, --help         show this help message and exit
```

これを念頭に置いて、`ibm.qradar` Collections をインストールします:

```bash
[student<X>@ansible ~]$ ansible-galaxy collection install ibm.qradar
Process install dependency map
Starting collection install process
Installing 'ibm.qradar:0.0.1' to '/home/student<X>/.ansible/collections/ansible_collections/ibm/qradar'
```

Collections が正しくインストールされていることを確認します:

```bash
[student<X>@ansible ~]$ ls -1 ~/.ansible/collections/ansible_collections/ibm/qradar
docs
LICENSE
plugins
README.md
tests
```

必要なファイルはすべてそこにあります - 特に実際のモジュールは `plugins/modules` ディレクトリにあります。

Collection が揃ったことで、あとは Playbook の作成に取り掛かることができるようになりました。

> **Note**
>
> 自宅でも試してみたい方へ: Collection command は最低でも Ansible のバージョン 2.9 が必要なのでご注意ください！

## Step 4.4 - 最初のサンプル Playbook

QRadar とのインターフェイスの最初の例では、ルールの有効化/無効化を行います。これはかなり小さな変更ですが、一般的な変更であり、Ansible と QRadar がどのように相互作用するかを示しています。まず最初に変更したいルールを見つけ、その後で変更を適用します。

VS Code Online エディタで、ユーザのホームディレクトリに `find_qradar_rule.yml` という新しいファイルを作成します。ここでは `qradar` の名前とターゲットとなるホストを追加します。

```yaml
---
- name: Find QRadar rule state
  hosts: qradar
```

また、先ほど追加した Collection を使います。Collection は、play レベルだけでなく task レベルなど複数の場所で参照することができます。play レベルで参照することで、後からそれらに基づいて複数の task を作成することができます。

```yaml
---
- name: Find QRadar rule state
  hosts: qradar
  collections:
    - ibm.qradar
```

次に実際の task を紹介します。QRadar の REST API は、まず適切なルールを検索してその ID を見つけ、与えられた ID を参照してルールを非アクティブにするように設計されています。このラボのために、DDoS 攻撃の疑いに基づいてメッセージを作成するルールを考えてみます。前のセクションでは、 **Offenses** > **Rules** で QRadar のルールを確認し、 **DDoS** という用語でフィルタリングしました。フィルタリングされたリストの中で、最初に表示されているルールは **"Potential DDoS Against Single Host (TCP) "** であることに注意してください。この文字列を使って、モジュール `qradar_rule_info` を使ってロールを検索します:

```yaml
---
- name: Find QRadar rule state
  hosts: qradar
  collections:
    - ibm.qradar

  tasks:
    - name: get info about qradar rule
      qradar_rule_info:
        name: "DDoS Attack Detected"
```

このモジュールは多くの情報を返しますが、その中でも Role を実際に無効にするために必要な ID を返します。キーワード `register` の助けを借りて、返ってきた情報を変数に登録してみます。これはモジュール自身で直接利用します。これにより、変数の内容を次の task で利用することができます。

```yaml
---
- name: Find QRadar rule state
  hosts: qradar
  collections:
    - ibm.qradar

  tasks:
    - name: get info about qradar rule
      qradar_rule_info:
        name: "DDoS Attack Detected"
      register: rule_info
```

では、モジュールが返す情報は実際にはどのように見えるのでしょうか？変数 `rule_info` を出力するだけではどうでしょうか？そのためには、Playbook の実行中に変数を出力するための `debug` task を追加します:

```yaml
---
- name: Find QRadar rule state
  hosts: qradar
  collections:
    - ibm.qradar

  tasks:
    - name: get info about qradar rule
      qradar_rule_info:
        name: "Potential DDoS Against Single Host (TCP)"
      register: rule_info

    - name: output returned rule_info
      debug:
        var: rule_info
```

> **Note**
>
> デバッグモジュールのパラメータ "var" は、すでに変数名を想定しています - そのため、通常の変数参照時のような中括弧や引用符は必要ありません。

どちらのタスクもデータを収集して出力するだけで、何かを変更することはありません。すぐに Playbook を実行して、返されたデータを見てみます:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook find_qradar_rule.yml

PLAY [Find QRadar rule state] ***************************************************

TASK [Gathering Facts] ************************************************************
ok: [qradar]

TASK [get info about qradar rule] *************************************************
ok: [qradar]

TASK [output returned rule_info] **************************************************
ok: [qradar] => {
    "rule_info": {
        "changed": false,
        "failed": false,
        "rules": [
            {
                "average_capacity": 0,
                "base_capacity": 0,
                "base_host_id": 0,
                "capacity_timestamp": 0,
                "creation_date": 1278524200032,
                "enabled": true,
                "id": 100065,
                "identifier": "SYSTEM-1520",
                "linked_rule_identifier": null,
                "modification_date": 1566928030130,
                "name": "Potential DDoS Against Single Host (TCP)",
                "origin": "SYSTEM",
                "owner": "admin",
                "type": "FLOW"
            }
        ]
    }
}

PLAY RECAP ************************************************************************
qradar  : ok=3  changed=0  unreachable=0  failed=0  skipped=0  rescued=0  ignored=0
```

ご覧のように、デバッグタスク `output returned rule_info` は変数の内容を示し、モジュール `qradar_rule_info` によって返された内容を示しています。これらの戻り値の中にはキー `id` が含まれていることに注意してください。これが必要なキーです。

> **Note**
>
> あなたの環境ではキー ID が違う可能性があります。

この構造体にキーがある場合、どのようにしてキーを取得するのでしょうか？ まず、変数のセグメント `rules` の中にあり、`rule_info.rules` でアクセスすることができます。`rules` の中にはリスト(中括弧に注意)がありますが、エントリは1つしかありません。そして、リストの中から各キーに個別にアクセスすることができます: `rule_info.rules[0]['id']`.

そこで、新しい Playbook を作成して、これを値としてモジュールに提供し、ルール `qradar_rule` を無効にできるようにします。

VS Code Online エディタで、ホームディレクトリ `/home/student<X>/` に `change_qradar_rule.yml` という新しいファイルを作成します。ここでは `qradar` の名前とターゲットとなるホストを追加します。

<!-- {% raw %} -->
```yaml
---
- name: Change QRadar rule state
  hosts: qradar
  collections:
    - ibm.qradar

  tasks:
    - name: get info about qradar rule
      qradar_rule_info:
        name: "Potential DDoS Against Single Host (TCP)"
      register: rule_info

    - name: disable rule by id
      qradar_rule:
        state: disabled
        id: "{{ rule_info.rules[0]['id'] }}"
```
<!-- {% endraw %} -->

Playbook が完成しました: それは QRadar にルールのリストを照会し、我々が探しているものを非アクティブにします。

## Step 4.5 - Playbook を実行します

Playbook を完成させたら、実行してみます:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook change_qradar_rule.yml

PLAY [Change QRadar rule state] ***************************************************

TASK [Gathering Facts] ************************************************************
ok: [qradar]

TASK [get info about qradar rule] *************************************************
ok: [qradar]

TASK [disable rule by id] *********************************************************
changed: [qradar]

PLAY RECAP ************************************************************************
qradar  : ok=3  changed=1  unreachable=0  failed=0  skipped=0  rescued=0  ignored=0
```

ご覧のように、Playbook は変更を示しています: ルールが変更されました。Playbook をもう一度実行してみてください - ルールはすでに無効化されているので、変更は報告されません。

## Step 4.6 - UI から変更を確認します

Ansible が実際に何かを変更したことを確認するために、QRadar の UI に戻ります。Web ブラウザで QRadar の IP を開きます。**Offenses** タブをクリックし、そこから左側の **Rules** をクリックします。ルールの長いリストが表示されます。このリストの上部にある検索バーに、以下の検索語を入力します: `DDoS`
リストをフィルタリングするために、DDoS に関連するいくつかのルールのみが表示されるように、後から Enter キーを押します。最後に、潜在的な DDoS 攻撃に関するルールに注意して、**Enabled** 列の状態を確認してください。

![QRadar, filtered rules list showing disabled rule](images/qradar-rules-disabled.png)

これで、Ansible で QRadar を自動化する最初のステップは終了です。エクササイズの概要に戻り、次のエクササイズに進みます。

----

[Ansible Security Automation Workshopの表紙に戻る](../README.ja.md)
