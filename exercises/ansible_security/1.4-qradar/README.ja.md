# 演習 1.4 - 最初の IBM QRadar の実行

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

## ステップ 4.1 - IBM QRadar

セキュリティー環境で SIEM を自動化する方法を紹介するために、このラボには、[IBM QRadar SIEM, community
edition](https://developer.ibm.com/qradar/ce/). が含まれています。

SIEM は Web UI および REST API からアクセスできます。このラボでは、作成した Playbook はバックグラウンドで API
と対話します。すべてのアクションは Web UI で検証されます。

## ステップ 4.2: Web UI へのアクセス

SIEM を最初に確認し、これが実際に機能していることを確認します。Web ブラウザーで `https://<qradar-IP>` に対してポイントします。ここで、`<qradar-IP>` は、インベントリーの `siem` セクションの `qradar` エントリーの IP アドレスになります。次に、証明書が自己署名されているため安全ではないという警告が表示されます。これを受け入れて次に進んでください。

> **注記**
>
> 実稼働環境では、安全でない証明書を受け入れるという選択肢はありません。ラボのセットアップは短期間のデモ目的のみであるため、このケースではリスクを受け入れます。

ログインフィールドに、ユーザー名 **admin** とパスワード **Ansible1!** を指定します
(特に指定されない場合)。**Login** ボタンを押します。

これで、IBM QRadar のメイン Web インターフェースが表示されます。

![QRadar main window](images/qradar-main-window.png#centreme)

QRadar と基本的な概念を理解するために、インターフェースを簡単に見てみましょう。上部には、QRadar
の主要部分に複数のエントリーポイントを持つナビゲーションバーがあります。

- **Dashboard** (主な概要を提供) - **Offenses** (監視された状態によって生成されたメッセージまたはイベント) -
**Log Activity** (ログソースから収集されたイベントの表示) - **Network Activity**
(特定ホスト間のネットワークトラフィック通信) - **Assets** (環境内の自動的に作成されたネットワークデバイスおよびホストのプロファイル)
- **Reports** (カスタマイズレポートまたは標準的なレポートで、環境内で起こったことを報告)

このデモの目的上、**Offenses**
を詳しく見てみます。メニュー項目をクリックします。新しいウィンドウで、左側にナビゲーションバーが表示され、オフェンスのフィルタリングが行われます。

![QRadar offense window](images/qradar-offense-window.png#centreme)

> **注記**
>
> これはデモ環境であるため、オフェンスリストが現在空である可能性があります。

オフェンスとは、悪意のあるログラインのように、ログメッセージやネットワークトラフィックでの発見に基づいて生成されるメッセージやイベントのことです。QRadar
は、ルールに基づいてオフェンスをトリガーします。ルールには条件が記述されており、条件が満たされるとオフェンスが発生します。

公式ドキュメントには、以下のように書かれています。

> *ルール (相関ルールと呼ばれることもある) は、イベント、フロー、またはオフェンスに適用され、異常の検索または検出を行います。テストの条件がすべて満たされた場合、ルールはレスポンスを生成します。([QRadar ドキュメント](https://www.ibm.com/support/knowledgecenter/en/SS42VS_7.3.2/com.ibm.qradar.doc/c_qradar_rul_mgt.html))*

生産性の高い環境では、時間をかけてさらに多くのカスタムルールを作成するのが一般的です。しかし、現時点では、システムにすでにインストールされているルールを見てみましょう。**Offenses**
ウィンドウのナビゲーションバーの左側で、**Rules**
をクリックします。ルールの長いリストが表示されます。このリストの上部にある検索バーに、`DDoS` という検索用語を入力します。その後に Enter
を押して、一覧をフィルタリングします。

この一覧はフィルタリングされ、DDOS に関連するいくつかのルールのみが表示されます。

![QRadar, filtered rules list](images/qradar-offenses-rules.png#centreme)

**"Potential DDoS Against Single Host (TCP)"**
という項目をクリックし、有効になっていることを確認します。これは、この演習で後ほど関連してきます。

QRadar の概要がわかったところで、今度は Ansible を使って QRadar を自動化する方法を見ていきましょう。

## ステップ 4.3 - QRadar モジュールおよび Ansible コレクション

最も基本的なレベルでは、Ansible Automation Platform
はタスクを実行します。これらのタスクはモジュールを実行します。モジュールは通常、特別なデバイスやプログラムの API
エンドポイントのように、対応するターゲット上で動作します。

Ansible には多くのモジュールが同梱されていますが、執筆時点では、Ansible は 追加設定なしの QRadar
のモジュールを出荷していません。その代わり、それらのモジュールは [Ansible
collections]](https://docs.ansible.com/ansible/devel/dev_guide/collections_tech_preview.html):
として提供されます。

> *コレクションは、Ansible コンテンツのディストリビューション形式です。コレクションを使用して、Playbook、ロール、モジュール、およびプラグインをパッケージ化および配布できます。Ansible Galaxy を介してコレクションを公開および使用できます。*

コレクションは、簡単なディレクトリー構造に従って Ansible コンテンツを提供します。ここで、Ansible
ロールを思い出した場合、これには理由があります。コレクションはロールの概念に基づいて構築されますが、その概念を一般的な Ansible
コンテンツ管理に拡張します。IBM QRadar のコレクションは、[ansible-security
project](https://github.com/ansible-security/ibm_qradar). にあります。

自動化実行環境は、必要なコレクションを含めるようにカスタマイズできます。この例として、このワークショップで使用する `security_ee`
カスタム実行環境があります。カスタムの `security_ee` 実行環境には、これらの演習で使用する `ibm.qradar`
コレクションが含まれます。



> **注記**
>
> Ansible Automation Platform には、独自のカスタム実行環境を作成するために使用できる `ansible-builder` が含まれています。`ansible-builder` の詳細は、[blog post](https://www.ansible.com/blog/introduction-to-ansible-builder). を参照してください。

## ステップ 4.4 - 最初の Playbook の例

QRadar とのインターフェースの最初の例では、ルールを有効化/無効化します。これは小規模ですが、一般的な変更であり、Ansible と QRadar
の対話方法を紹介します。これは 2 つのステップで行われます。最初のステップでは、変更するルールを見つけます。次のステップでは、変更を適用します。

VS Code のオンラインエディターで、ユーザーのホームディレクトリーに新規ファイル `find_qradar_rule.yml` を作成します。ここ
`qradar` に名前とターゲットホストを追加します。

```yaml
---
- name: Find QRadar rule state
  hosts: qradar
```

また、先ほど追加したばかりのコレクションも使用したいと思います。コレクションは複数の場所で参照することができます。たとえば、タスクレベルとプレイレベルの両方で参照できます。ここでは、プレイレベルでコレクションを参照し、後にコレクションに基づいて複数のタスクを作成できるようにします。

```yaml
---
- name: Find QRadar rule state
  hosts: qradar
  collections:
    - ibm.qradar
```

次に、実際のタスクを実行します。QRadar の REST API は、最初に適切なルールを検索して ID を検索し、指定の ID を参照してルールを非アクティブにする必要があるように設計されています。このラボでは、DDoS 攻撃の疑いに基づいてメッセージを作成するルールがあるとします。前のセクションでは、**Offenses** > **Rules** 経由の QRadar ルールをすでに確認し、**DDoS** という用語でフィルタリングしました。フィルタリングされたリストでは、ここで示されている最初のルール **"Potential DDoS Against Single Host (TCP)"** に注目してください。この文字列を使用して、モジュール `qradar_rule_info` を使用するロールを検索します。

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
```

このモジュールは多くの情報を返しますが、その中には実際にロールを無効にするために必要な ID も含まれています。ここでは、`register`
キーワードを使用して返された情報を変数に登録します。これは、モジュール自体で直接使用されます。これにより、次のタスクで変数の内容を使用することができます。

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
```

では、実際にモジュールが返す情報は、どのようになっているのでしょうか? 単に変数 `rule_info` を出力するのはどうでしょう?
そのためには、Playbook の実行中の変数の出力に使用できる `debug` タスクを追加します。

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

> **注記**
>
> デバッグモジュールのパラメーター "var" はすでに変数名を想定しています。そのため、通常、変数を参照するときのような中括弧や引用符は必要ありません。

どちらのタスクもデータを収集して出力するだけで、何も変更しません。さっそく Playbook を実行し、返ってきたデータを見てみましょう。

```bash
[student<X>@ansible-1 ~]$ ansible-navigator run find_qradar_rule.yml --mode stdout
```
![QRadar rule ID](images/1.4-qradar-id.png#centreme)

ご覧のように、デバッグタスク `output returned rule_info` は変数の内容を表示し、したがって、モジュール
`qradar_rule_info` によって返されたコンテンツを示しています。これらの返されたデータの中で、キー`id` (この例では値が
`100065`) に注意してください。これは私たちが必要とするキーになります。

> **注記**
>
> キー ID は、実際のケースでは異なる場合があります。

このような構造になっている場合、どのようにしてキーを取得するのでしょうか。まず、キーは変数のセグメント `rules`
にあり、`rule_info.rules` でアクセスできます。`rules` の中には、実際にはリスト (中括弧に注目) がありますが、エントリーは
1 つしかないので、`rule_info.rules[0]`
でアクセスします。そして、リストのエントリーの中から、各キーへはその名前`rule_info.rules[0]['id']`
で個別にアクセスすることができます。

では、これをモジュールに値として提供し、ルール `qradar_rule` を無効にできる新しい Playbook を作成してみましょう。

VS Code のオンラインエディターで、ホームディレクトリー `/home/student<X>/` に新しいファイル `change_qradar_rule.yml` を作成します。ここ `qradar` に名前およびターゲットホストを追加します。

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

これで Playbook が完了しました。ルールのリストを QRadar にクエリーし、検索すしているルールを非アクティブにします。

## ステップ 4.5 - Playbook の実行

Playbook が完了したら、これを実行してみましょう。

```bash
[student<X>@ansible-1 ~]$ ansible-navigator run change_qradar_rule.yml --mode stdout

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

ご覧のように、Playbook にはルールが変更されたと表示されています。ルールがすでに無効にされているため、Playbook
を再度実行しても変更を報告しません。

## ステップ 4.6: UI での変更の確認

Ansible が本当に何かを変えたことを確認するために、QRadar の UI に戻ります。Web ブラウザーで QRadar IP
を開きます。**Offenses** タブをクリックして、そこから左側の **Rules**
をクリックします。ルールの長い一覧が表示されます。この一覧の上部にある検索バーに、検索用語 `DDoS` を入力します。Enter
を押して一覧をフィルタリングし、DDOS に関連するルールのみを表示します。最後に、潜在的な DDOS
攻撃に関するルールに注意してください。そして、**Enabled** 列の状態を確認します。これは **False** に設定されています。

![QRadar, filtered rules list showing disabled
rule](images/qradar-rules-disabled.png#centreme)

Ansible で QRadar を自動化する最初のステップを完了しました。演習の概要に戻り、次のステップに進みます。

----

**Navigation**
<br><br>
[Previous Exercise](../1.3-snort/README.md) | [Continue to Section 2](../2.1-enrich/README.md)
<br><br>
[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md)
