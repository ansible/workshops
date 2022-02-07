# 演習 2.0 - プールメンバーの無効化

**他の言語でもお読みいただけます** :![uk](../../../images/uk.png) [English](README.md)、![japan](../../../images/japan.png) [日本語](README.ja.md).

## 目次

- [目的](#objective)  - [ガイド](#guide)  - [Playbook の出力](#playbook-output)  -
[ソリューション](#solution)

# 目的

この最後の演習では、ステップバイステップの順を追った説明ではなく、各ステップのヒントと共にフレームワークについて説明します。  

プールからのノードの削除を説明します。次の Playbook をビルドします。
  - BIG-IP にあるプール用に、BIG-IP からファクトを取得する（この例では 1 つのプールのみが存在します）
  - 利用可能なプールを表示する
  - ファクトとしてプール名を保存する
  - プール => IP およびポート情報に属するすべてのプールメンバーをターミナルウインドウに表示する
  - プールの特定のメンバーまたはすべてのメンバーを無効にするようにユーザーに要求する
  - 適切なプールメンバーを強制的にオフラインにする

# ガイド

## ステップ 1:

VSCode を使用して、左側のペインの新規ファイルアイコンをクリックして、`disable-pool-member.yml`
という名前の新しいファイルを作成します。

![picture of create file
icon](../1.1-get-facts/images/vscode-openfile_icon.png)

## ステップ 2:

次のプレイ定義を `disable-pool-member.yml` に入力します。

<!-- {% raw %} -->
``` yaml
---
- name: Disabling a pool member
  hosts: lb
  connection: local
  gather_facts: false

```
<!-- {% endraw %} -->

## ステップ 3

tasks
セクションを追加してからプロバイダーのファクトを設定します。プロバイダーを設定したら、server/user/password/server_port
および validate_certs 情報を各タスクに提供する代わりに、将来のタスクでこのキーを再利用できます。

<!-- {% raw %} -->
``` yaml
  tasks:
    - name: Setup provider
      set_fact:
        provider:
          server: "{{private_ip}}"
          user: "{{ansible_user}}"
          password: "{{ansible_password}}"
          server_port: 8443
          validate_certs: false
```
<!-- {% endraw %} -->

次のタスクで、以下のようにプロバイダーを使用できるようになりました。

<!-- {% raw %} -->
``` yaml
      f5networks.f5_modules.bigip_device_info:
        provider: "{{provider}}"
        gather_subset:
        - ltm-pools
```
<!-- {% endraw %} -->

今後は、各モジュールに server_ip/user/password などを渡す必要はありません。

``` yaml
---
- name: "Disabling a pool member"
  hosts: lb
  gather_facts: false
  connection: local
```

## ステップ 4

次に、以下に挙げる目的のためにタスクを追加します。

  - サブセット ltm-pools 用に BIG-IP からファクトを取得する

ヒント:
<a href="../1.1-get-facts" style="color: RED">演習 1.1</a> の bigip_device_info モジュールを使用してみます

## ステップ 5

次に、以下に挙げる目的のためにタスクを追加します。

  - ターミナルウィンドウにプール情報を表示する

ヒント:
上記のステップの出力で `loop` する方法を思い出してください。<a href="https://docs.ansible.com/ansible/latest/modules/debug_module.html" style="color: RED">デバッグモジュール</a> を使用するのも忘れないでください

## ステップ 6

次に、以下に挙げる目的のためにタスクを追加します。

  - プール名をファクトとして保存する

ヒント: Playbook 内でファクト変数を動的に設定する簡単な方法は、<a href="https://docs.ansible.com/ansible/latest/modules/set_fact_module.html" style="color: RED">set_fact モジュール</a> を使用することです

## ステップ 7

次に、以下に挙げる目的のためにタスクを追加します。

  - プールに属するメンバーを表示する

ヒント:
<a href="https://docs.ansible.com/ansible/latest/modules/debug_module.html" style="color: RED">デバッグ</a> を使用し、<a href="../1.4-add-pool-members" style="color: RED">演習 1.4</a> を参照することを思い出してください

## ステップ 8
次に、以下に挙げる目的のためにタスクを追加します。

  - プールに属するすべてのメンバーを無効にする

ヒント:
<a href="https://docs.ansible.com/ansible/latest/modules/bigip_pool_member_module.html" style="color: RED">BIG-IP プールメンバーモジュール</a> を使用するのを忘れないでください

## ステップ 9
Playbook を実行します。VS Code サーバーのターミナルに戻り、以下を実行します。

```
[student1@ansible ~]$ ansible-navigator run disable-pool-member.yml --mode stdout
```

# Playbook の出力

出力は次のようになります。

<!-- {% raw %} -->
```yaml
[student1@ansible ~]$ ansible-navigator run disable-pool-member.yml --mode stdout

PLAY [Disabling a pool member] *******************************************************************************

TASK [Setup provider] *******************************************************************************
ok: [f5]

TASK [Query BIG-IP facts] *****************************************************
changed: [f5]

TASK [Display Pools available] ************************************************
ok: [f5] => (item=http_pool) => {
    "msg": "http_pool"
}

TASK [Store pool name in a variable] ******************************************
ok: [f5] => (item=None)
ok: [f5]

TASK [Show members belonging to pool http_pool] *******************************
ok: [f5] => (item=node1:80) => {
    "msg": "node1:80"
}
ok: [f5] => (item=node2:80) => {
    "msg": "node2:80"
}

TASK [pause] ******************************************************************
[pause]
To disable a particular member enter member with format member_name:port
To disable all members of the pool enter 'all':
node1:80

TASK [Disable ALL pool members] ***********************************************
skipping: [f5] => (item=node1:80)
skipping: [f5] => (item=node2:80)

TASK [Disable pool member node1:80] *******************************************************************************
changed: [f5]

PLAY RECAP *******************************************************************************
f5                         : ok=7    changed=2    unreachable=0    failed=0
```
<!-- {% endraw %} -->

# ソリューション
答えに詰まったら、回答がインストラクターによって提供されます。GUI
の表示は、以下のようになるはずです。黒いダイヤマークは、指定されたノードが強制的にオフラインにされたことを示します。

![f5bigip-gui](f5bigip-gui.png)

--
You have finished this exercise.  [Click here to return to the lab
guide](../README.md)
