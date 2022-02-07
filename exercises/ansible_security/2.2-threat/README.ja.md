# 演習 2.2: 脅威ハンティング

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

## ステップ 2.1 - 背景

脅威の検出および対応機能では、通常、セキュリティーオペレーターは、企業の IT
を保護するための多くのツールをデプロイする必要があります。これは、プロセスが欠落したり、手作業が多かったりするため、適切な IT
セキュリティー運用にとって深刻な課題となっています。

この演習では、私たちは大規模な組織のエンタープライズファイアウォールを担当するセキュリティーオペレーターであると前提とします。ここで使用するファイアウォール製品は、Point
Next Generation Firewall.です。この演習では、さまざまなチーム間のやりとりに特に焦点を当て、それらのやりとりを
[automation
controller](https://docs.ansible.com/automation.html). でどのように効率化できるかを考えます。

## ステップ 2.2 - 準備

前の演習と同じように、前の [Check Point 演習](../1.2-checkpoint/README.md)
でいくつかの手順が完了していることを確認する必要があります。

1. `whitelist_attacker.yml` Playbook は、少なくとも 1 回実行されている必要があります。
2. また、攻撃者のホワイトリストポリシーのロギングが、Check Point SmartConsole でアクティベートされている必要があります。

いずれも [Check Point 演習](../1.2-checkpoint/README.md)
で行いました。これらの手順を飛ばしている場合は、手順に戻って Playbook
を実行し、手順に従ってロギングをアクティベートしてから、こちらに戻ってきてください。

## Step 2.3: コントローラーの設定を調べる

準備にはさらに 2
つの手順が必要ですが、前の演習とは対照的に、自動化コントローラーを使用してこれを実行します。自動化コントローラのインストールには、ユーザー、インベントリー、認証情報などがすでに入力されており、直接使用することができます。では、詳しく見ていきましょう。

自動化コントローラーはブラウザー経由でアクセスされます。パーソナルコントローラーインスタンスへの URL が必要です。これは、VS Code
のオンラインエディターの URL に似ていますが、`-code` がついていません。ワークショップのページで確認することもできます。

![Controller URL example](images/controller_url.png#centreme)

> **注記**
>
> この URL とログイン情報は一例です。お使いのコントローラーの URL とログイン情報は異なります。

ブラウザーを開き、自動化コントローラーインスタンスへのリンクを入力します。受講者 ID
と、指定したパスワードを使用してログインします。ダッシュボードと、左側のナビゲーションバーが表示されます。

![Automation controller dashboard](images/controller_dashboard.png#centreme)

左側の **Templates**
をクリックします。すでに設定されたすべてのジョブテンプレートの一覧が表示されます。ジョブテンプレートは、Ansible
ジョブを実行するための定義およびパラメーターセットです。これは、自動化の実行に必要なインベントリー、認証情報、Playbook、制限、become
権限などを定義します。この一覧で、**Blacklist attacker**
と呼ばれるエントリーを見つけ、その右側にあるロケットのアイコンをクリックします。

![Blacklist attacker](images/controller_blacklist.png#centreme)

このクリックでジョブの概要が表示され、自動化ジョブ実行のライブデータと、ジョブに関連するすべてのパラメーターの概要が表示されます。この自動化の実行により、2
台のマシン間でパッケージをドロップするようにファイアウォールの既存のポリシーを変更しました。

これで、必要なのは攻撃だけとなりました。前回の演習とは異なり、Playbook
を書いて実行するのではなく、ここでもコントローラーを使って攻撃を開始します。左側のナビゲーションバーで、**Templates**
をクリックします。テンプレートのリストの中から、**Start DDOS attack simulation**
という名前のテンプレートを探し、その右側にあるロケットのアイコンをクリックして、これを実行します。これにより、数秒ごとに攻撃のシミュレーションが行われます。

これで準備は完了しました。このユースケースの概要を知るには、次へと進んでください。

## ステップ 2.4 - 攻撃の確認

あなたは大規模な組織のエンタープライズファイアウォールを担当するセキュリティーオペレーターです。ビジネスアプリケーションを保護する Check
Point Next Generation Firewall (NGFW)
よって適用されるポリシーが、繰り返し違反されていることに気づきました。これを確認するには、Windows ワークステーションで SmartConsole
を開き、Check Point 管理サーバーにアクセスし、左側の **LOGS & MONITOR**
タブをクリックします。新しいウィンドウが開き、**Audit Logs** および **Logs** の 2 つの選択肢が表示されます。**Logs**
をクリックし、ログの実際のビューを表示します。

>**Check Point NGFW Credentials**   
>
> Username: `admin`   
> Password: `admin123`   
> 

![Check Point logs view, violation
logs](images/smartconsole_violation_logs.png#centreme)

ご覧のとおり、**http Traffic Dropped** という説明が付いた一連のメッセージが、時間の経過とともに何度も繰り返されています。

> **注記**
>
> ログが表示されない場合は、自動更新が有効になっていない可能性があります。その場合は、対応するボタン (丸印の隣にある A) をクリックしてください。

![Check Point logs view, auto refresh
button](images/smartconsole_auto_refresh.png#centreme)

このような違反があった場合、これらが攻撃の結果であるかどうかを評価するために調査を開始する必要があります。調査のための最良の方法は、QRadar
のようなログ管理ツールで、ファイアウォールのログを、ネットワークにデプロイされている他のセキュリティーソリューション (Snort など)
で生成されたログと相関させることです。

## ステップ 2.5: QRadar へのログの転送

しかし、前述したように、多くの企業環境では、セキュリティーソリューションが互いに統合されておらず、大規模な組織では、さまざまなチームが IT
セキュリティーのさまざまな側面を担当しており、共通のプロセスはありません。このシナリオでは、セキュリティーオペレーターが問題をエスカレーションして調査を開始する一般的な方法は、セキュリティー分析チームに連絡し、ルール違反を特定するために使用したファイアウォールログを手動で送信し、応答を待つというものでした。これは、時間のかかる、手動によるプロセスです。

しかし、前回の演習で示したように、Ansible Automation Platform
を使ってこのプロセスを自動化することができます。自動化コントローラーのような中央自動化ツールを介して、Playbook
の形式で事前に承認された自動化ワークフローを用意することができます。このような一連の Ansible Playbook
があれば、脅威ハンティングの状況になるたびに、エンタープライズファイアウォールがイベントやログを QRadar
インスタンスに送信するように自動的に設定することができます。セキュリティーアナリストは、QRadar
インスタンスを使用してデータを相互に関連付け、潜在的な脅威に対処する方法を決定します。

これを試してみましょう。コントローラーのインスタンスからログアウトし、ファイアウォールユーザーである `opsfirewall`
でログインします。デモを簡単にするために、パスワードは受講者ユーザーのものと同じになります。ログインしてダッシュボードが表示されたら、**Templates**
に移動します。ご覧のように、ファイアウォール管理者として、表示および実行できるジョブテンプレートはごくわずかです。

- **Blacklist attacker** - **Send firewall logs to QRadar** - **Whitelist
attacker**

ファイアウォールのドメイン所有者であるため、これらのジョブテンプレートを変更、削除、および実行することができます。テンプレート **Send
firewall logs to QRadar**
の横にある小さなロケットのアイコンをクリックして、これを実行してみましょう。ジョブの実行には数秒かかります。ファイアウォールオペレーターの観点では、これでファイアウォールが中央の
SIEM にログを送信するように再構成されました。

ただし、SIEM は引き続きログを受け入れ、QRadar
のログソースと呼ばれる適切なストリームに分類する必要があります。視点をセキュリティーアナリストの立場に切り替えてみましょう。ファイアウォールで何か変なことが起きているという連絡があり、すでにログがこちらに送られてきました。コントローラーからログアウトし、`analyst`
ユーザーとしてログインし直します。再度、**Templates**
を確認してください。ここでも、自動化テンプレートの別のリストが手元にあります。このうち、自分たちのジョブに関連するものだけを確認して使用することができます。ファイアウォールログを
SIEM に許可してみましょう。ジョブテンプレート **Accept firewall logs in QRadar** を実行します。

Playbook
は数秒後に実行され、新しいセキュリティー設定が完了します。前回の演習とは対照的に、これらの手順では、オペレーターやアナリストがコマンドラインへアクセスしたり、Playbook
を書いたり、ロールまたはコレクションをインストールしたりする必要はありませんでした。Playbook は事前に承認され、実際には Git
リポジトリー内からアクセスされていました。自動化コントローラーは、実行のほか、ロールまたはコレクションのダウンロードにも対応していました。これにより、自動化操作が大幅に簡素化されます。

右側の **Jobs**
をクリックすると、以前実行したジョブに常にアクセスできることが確認できます。これにより、チームは何がいつ実行され、どのような結果になったかをより正確に追跡することができます。これにより、実行された自動化の透過性と明確な理解が可能になります。

>**注記**
>
> ジョブは、ジョブテンプレートを起動する自動化コントローラーのインスタンスです。***Jobs** リンクには、ジョブのリストとステータスが表示されます。ステータスは、正常に完了したか失敗したか、またはアクティブな (実行中の) ジョブであるかのいずれかで表示されます。

## ステップ 2.6 - 新しい設定の確認

QRadar のログが表示されるようになったことを簡単に確認してみましょう。QRadar の Web UI にログインします。**Log
Activity** をクリックし、Check Point から QRadar にイベントが送信されていることを確認します。

>**IBM QRadar Credentials**   
>
> Username: `admin`   
> Password: `Ansible1!`   
> 

![QRadar Log Activity showing logs from Check
Point](images/qradar_checkpoint_logs.png#centreme)

> **注記**
>
> 入ってくるログが表示されない場合は、**View** の横にあるドロップダウンメニューをクリックし、**Real Time (streaming)** を選択します。

ログが、QRadar 独自のログに埋もれてしまう場合は、フィルターを作成します。または、**Log Source**
列の不要なログ行をクリックし、**Filter on Log Source is not ...**
を選択すると、不要なトラフィックをフィルタリングするためのフィルターをその場で作成することができます。

QRadar がログソースもきちんと表示するか確認してみましょう。QRadar の UI
で、左上隅のハンバーガーボタンをクリックしてから、**Admin** をクリックします。そこで **Log Sources**
をクリックします。新しいウィンドウが開き、新しいログソースが表示されます。

![QRadar Log Sources](images/qradar_log_sources.png#centreme)

## ステップ 2.7 - オフェンス

次に、QRadar
に表示されるオフェンスを管理する必要があります。現在は何も生成されていませんが、このユースケースのためにあらかじめ設定されているものがあるでしょうか?
QRadar Web UI で、**Offenses** タブを開きます。左側のメニューで **Rules** をクリックします。その上の
**Group:** ドロップダウンメニューの中から、**Ansible**
を選択します。このワークショップ用に事前に設定されたオフェンスルールがすべて表示されます。

![QRadar Pre-configured
Rules](images/qradar_preconfigured_rules.png#centreme)

**Ansible Workshop DDOS Rule**
というルールをダブルクリックします。ルールウィザードウィンドウが開き、必要に応じてオフェンスルールへの変更が可能になります。

![QRadar Rules Wizard](images/qradar_rule_wizard.png#centreme)

ウィザードから、使用するチェックがごくわずかであることがわかります。(ウィンドウの 2
番目のボックス)。ルールはもっと複雑にすることができ、他のルールに依存することもできます。その結果、オフェンスを作成する必要はありませんが、たとえば、追加のログエントリーを作成することができます。ここでは何も変更しませんので、右下隅の
**Cancel** をクリックしてウィザードを終了し、ブラウザーの終了警告を確認してください。

この違反が誤検出であるかどうかを判断するためには、ファイアウォールに表示されないような攻撃を他のソースが実行していないことを確認する必要があります。そのためには、IDS
によって生成されたログにアクセスし、ファイアウォールでの違反と互換性のある特定の攻撃パターンを確認する必要があります。

## ステップ 2.8: Snort ルールの追加

新しい IDS ルールを追加してみましょう。ここでも、すでにコントローラー内にある事前承認済みの Playbook
を使って行います。コントローラーからログアウトし、`opsids` ユーザー (IDPS 担当の IDPS オペレーター)
としてログインします。**Templates** に移動します。Snort にルールを追加するために利用できる **Add IDPS Rule**
という事前に作成されたジョブテンプレートがあります。小さいロケットのアイコンをクリックして、これを実行します。ところが、ご覧のように、ジョブの出力画面ではなく、アンケートが表示されます。

![Automation controller survey](images/controller_snort_survey.png#centreme)

Playbook はコンテンツを追加せずに実行することはできません。デプロイする必要がある実際のルールを指定する必要があります。当然ながら、Snort
では、追加する必要のあるルールは実際のユースケースによって異なるため、毎回異なる可能性があります。そこで、このジョブテンプレートでは、実行前に入力をクエリーする自動化コントローラーのメソッドである
***survey*** を有効にしています。

この場合、適切な署名、つまりこの特定の攻撃に対する適切な Snort ルールをクエリーします。フィールドに以下の文字列を入力します。

```
alert tcp any any -> any any (msg:"Attempted DDoS Attack"; uricontent:"/ddos_simulation"; classtype:successful-dos; sid:99000010; priority:1; rev:1;)
```

ご覧のとおり、攻撃のパラメーターに一致する新しい Snort ルールを追加しています。この例では、再び URI
コンテンツをチェックします。文字列の追加後、**Next** をクリックしてから **Launch** をクリックします。

Playbook が実行され、新しいルールのインストール、サービスの再起動などの処理が行われます。

Snort インスタンスで新しいルールをすばやく確認します。VS Code のオンラインエディターのターミナルから、`ec2-user`
ユーザーを使用して SSH 経由で Snort にログインします。

```bash
[student<X>@ansible-1 ~]$ ssh ec2-user@snort
Last login: Fri Sep 20 15:09:40 2019 from 54.85.79.232
[ec2-user@snort ~]$ sudo grep ddos_simulation /etc/snort/rules/local.rules
alert tcp any any -> any any  (msg:"Attempted DDoS Attack"; uricontent:"/ddos_simulation"; classtype:successful-dos; sid:99000010; priority:1; rev:1;)
```

> **注記**
>
> また、snort サービスが `sudo systemctl status snort` 経由で実行されていることを確認します。致命的なエラーがある場合は、入力したルールでエラーが発生した可能性があります。ファイル `/etc/snort/rules/local.rules` からルール行を削除して、Playbook を再び実行します。

ルールを確認したら、`exit` コマンドで Snort サーバーを終了します。

次に、ルールがヒットした場合に IDPS が QRadar にログを送信するようにします。これは、対応するジョブテンプレートを `opsids`
ユーザーとして実行するだけで済みます。ただし、今回は別のパスを使用します。IDPS オペレーターが準備された Playbook
を実行する代わりに、自動化コントローラーが、他のユーザーにドメインを制御させることなく、そのような実行権を委任できる方法を紹介します。

アナリストチームと IDPS オペレータチームが、IDPS から QRadar にログを転送するための事前定義された Playbook
に合意したとします。IDPS チームはこの Playbook の作成に関与し、合意しているため、Playbook
をアナリストチームに提供します。アナリストチームは、IDPS チームの関与なしに、必要なときにいつでも Playbook を実行することができます。

コントローラーからログアウトし、`analyst` ユーザーとしてログインし直します。**Templates** セクションには、複数の
Playbook があります。

- **Accept firewall logs in QRadar** - **Accept IDPS logs in QRadar** -
**Roll back all changes** - **Send IDPS logs to QRadar**

2 つの **Accept...**
ジョブテンプレートのみがアナリストに属し、これらを修正したり、たとえば、小さなゴミ箱のアイコンからもわかるように、削除したりすることができます。ジョブテンプレート
**Send IDPS logs to QRadar**
は、実行権限のためだけに提供されているため、修正や削除はできず、実行のみが可能です。これにより、自動化を実行する権利がチームの枠を越えて提供されますが、修正や変更の権利はドメイン知識を持つチーム
(ここでは IDPS チーム) が維持したままとなります。また、認証情報にも注意してください。IDPS へのアクセスには SSH
キーが必要です。これらはジョブテンプレートで参照されますが、ユーザーアナリストは、コントローラーの **Credentials**
セクションでその内容を検索することはできません。このようにして、自動化を実行する権利を、ターゲットマシンにアクセスする権利から確実に分離することができます。

ここで、ジョブテンプレートの横にある小さなロケットのアイコンを押して、**Accept IDPS logs in QRadar** および **Send
IDPS logs to QRadar** の両方のジョブテンプレートを実行します。

## ステップ 2.9 - ホワイトリストへの IP 登録

SIEM QRadar を簡単に見てみましょう。ログアクティビティタブにアクセスします。QRadar で IDS からのイベントが
**生成されていない** ことを確認します。そうすれば、表示されている異常が、ファイアウォールにある 1 つの IP
によってのみ引き起こされていることを確実に知ることができます。他のトラフィックが異常を引き起こしていないため、表示されている異常は誤検出であると考えても問題ありません。

> **注記**
>
> 実際には、マシンの動作を分析する追加の手順を実行して、不正アクセスの可能性を排除することがあります。

ホストが攻撃を行っていないと判断し、ファイアーウォールのポリシー違反が誤検出であることを最終的に確認しました。これは、おそらくそのアプリケーションのホワイトリストグループの設定ミスが原因だと思われます。そこで、ファイアウォールでその
IP をホワイトリストに登録し、イベントを通過させることができます。

コントローラーからログアウトして、`opsfirewall` ユーザーとしてログインし直します。**Templates**
の概要に移動し、ジョブテンプレート **Whitelist attacker** を起動します。しばらくすると、トラフィックが許可されます。

QRadar が Snort のログイベントを正しく表示することを確認してみましょう。QRadar の UI で、上部の **Log
Activity** メニューをクリックします。以下のような **Snort rsyslog source**
からのログエントリーが表示されるはずです。

![QRadar Snort logs](images/qradar_snort_logs.png#centreme)


## ステップ 2.10 - ロールバック

アナリストは脅威ハンティングを終了しました。リソース消費とアナリストのワークロードを減らすには、Check Point と Snort
のログ設定を調査前の状態にロールバックすることをお勧めします。これを行うには、アナリストは **Roll back all changes**
と呼ばれる事前承認済みのジョブテンプレートを利用できます。

`analyst` ユーザーとして自動化コントローラーにログインし、**Roll back all changes**
ジョブテンプレートの隣りにある小さなロケットのアイコンをクリックし、これを実行します。すぐにすべてのロギング設定が正常に戻ります。

最後に、攻撃シミュレーションを停止する必要があります。コントローラーからログアウトして、受講者 (admin)
ユーザーとしてログインし直します。**Templates** のセクションで、*Stop DDOS attack simulation**
というジョブテンプレートを検索して実行します。

これで演習は終わりました。次の演習に進むには、演習のリストへ戻ってください。

----

**Navigation**
<br><br>
[Previous Exercise](../2.1-enrich/README.md) | [Next Exercise](../2.3-incident/README.md) 
<br><br>
[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md)
