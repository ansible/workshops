# 演習 3.1 - AS3 での操作変更

**他の言語でもお読みいただけます** :![uk](../../../images/uk.png) [English](README.md)、![japan](../../../images/japan.png) [日本語](README.ja.md).

## 目次

- [目的](#objective)  - [ガイド](#guide)  - [Playbook の出力](#playbook-output)  -
[ソリューション](#solution)

# 目的

既存の Web アプリケーション AS3 テンプレートを変更する方法を説明します。既存のテンプレートに問題があり、serviceMain が赤で表示されています。何が悪いのでしょうか?  
![serviceMain-offline.png](serviceMain-offline.png)

# ガイド

## ステップ 1:

何が問題かを調べます。Web ブラウザーで F5 にログインし、設定された内容を確認します。

  1. `ServiceMain` をクリックし、そのダウンしている理由を確認します。
  2. 表の `Availability` フィールドに注目します。

![pool-nodes-down.png](pool-nodes-down.png)

  3. `Local Traffic` セクションで `Pools` をクリックします。
  4. `app_pool` をクリックします。
  5. `Members` ボタンをクリックします

![443](443.png)

ポート **443** は正しくありません。2 つの RHEL Web サーバーはポート 80
でのみ実行されます。これが、それらがダウンしている理由となっています。

## ステップ 2:

~/j2 ディレクトリーの既存の jinja テンプレート `as3_template.j2` を開きます。

## ステップ 3:

ポート **443** の場所を探し、これをポート **80** に変更します。

この行は、以下のようになっています->
{% raw %}
``` json
                "servicePort": 443,
```
{% endraw %}

これを以下のように変更します->

{% raw %}
``` json
                "servicePort": 80,
```
{% endraw %}

## ステップ 4
Playbook を実行します。コントロールホストの VS Code サーバーのターミナルに戻り、以下を実行します。

```
[student1@ansible ~]$ ansible-navigator as3.yml --mode stdout
```

# Playbook の出力

出力は次のようになります。

{% raw %}
```yaml
[student1@ansible ~]$ ansible-navigator as3.yml --mode stdout

PLAY [Linklight AS3] **********************************************************

TASK [Create AS3 JSON Body] ***************************************************
ok: [f5]

TASK [Push AS3] ***************************************************************
ok: [f5]

PLAY RECAP ********************************************************************
f5                         : ok=2    changed=0    unreachable=0    failed=0
```
{% endraw %}

# ソリューション

修正した Jinja テンプレートが、回答キーとしてここで提供されています。
[as3_template.j2](https://github.com/network-automation/linklight/blob/master/exercises/ansible_f5/3.1-as3-change/j2/as3_template.j2)
を表示するには、ここをクリックしてください。

# ソリューションの確認

Web ブラウザーで F5 にログインし、設定された内容を確認します。lab_inventory/hosts ファイルから F5 ロードバランサーの
IP 情報を取得し、https://X.X.X.X:8443/ のように入力します。

![f5 gui as3](as3-fix.gif)

1. 左側のメニューで Local Traffic をクリックします
2. Virtual Servers をクリックします。
3. 右上の `Partition` というドロップダウンメニューをクリックし、WorkshopExample を選択します
4. 仮想サーバー `serviceMain` が表示されます。
5. 今回は緑で表示されます (`Available (Enabled) - The virtual server is available`)
6. `Pools` セクションの `app_pool` で、両方の Web サーバーの `service_port` がポート **80**
   に設定されていることを確認します。

----

You have finished this exercise.  [Click here to return to the lab
guide](../README.md)
