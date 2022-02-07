# 演習 3.0 - AS3 の概要

**他の言語でもお読みいただけます** :![uk](../../../images/uk.png) [English](README.md)、![japan](../../../images/japan.png) [日本語](README.ja.md).

## 目次

- [目的](#objective)  - [ガイド](#guide)  - [Playbook の出力](#playbook-output)  -
[ソリューション](#solution)

# 目的

仮想サーバー（セクション 1 Ansible F5 の演習とまったく同じ）を F5 AS3 でビルドする方法を説明します。

  - AS3 ([Application Services 3
    エクステンション](https://clouddocs.f5.com/products/extensions/f5-appsvcs-extension/3/userguide/about-as3.html))
    宣言モデルについて学びます。この演習は、AS3 について完全に学習することを目的としてはいません。コンセプトの概要と Ansible
    Playbook と簡単に統合できることを説明するだけです。
  - [set_fact
    モジュール](https://docs.ansible.com/ansible/latest/modules/set_fact_module.html)
    について学びます
  - [uri
    モジュール](https://docs.ansible.com/ansible/latest/modules/uri_module.html)
    について学びます

# ガイド

#### 次に進む前に、BIG-IP 設定がクリーンであることを確認し、演習 [2.1-delete-configuration](../2.1-delete-configuration/README.md) を実行します。

## ステップ 1:

F5 BIG-IP で AS3 が有効になっていることを確認します。  

  1. Web ブラウザーを使用して F5 BIG-IP にログインします。
  2. 左側のメニューの iApps ボタンをクリックします。
  3. `Package Management LX` のリンクをクリックします。
  4. `f5-appsvcs` がインストールされていることを確認します。

このようにならない場合は、インストラクターにお問い合わせください。

![f5 gui](f5-appsvcs.gif)

## ステップ 2:

Playbook の構築を開始する前に、AS3 の仕組みを理解することが重要です。AS3 では、F5 BIG-IP への API コールとして渡される
JSON
テンプレートが必要です。この演習では、**テンプレートが用意されています**。すべてのパラメーターを完全に理解したり、これらのテンプレートをゼロから作成したりする必要はありません。テンプレートは、以下の
2 つの部分で構成されます。

1. `tenant_base.j2`

<!-- {% raw %} -->
``` yaml
{
    "class": "AS3",
    "action": "deploy",
    "persist": true,
    "declaration": {
        "class": "ADC",
        "schemaVersion": "3.2.0",
        "id": "testid",
        "label": "test-label",
        "remark": "test-remark",
        "WorkshopExample":{
            "class": "Tenant",
            {{ as3_app_body }}
        }
    }
}
```
<!-- {% endraw %} -->

 `tenant_base` は、F5 ネットワークが顧客に提供する標準テンプレートです。理解すべき重要な部分は以下のとおりです。

  - `"WorkshopExample"` - これはテナントの名前です。AS3 はこの特定の WebApp
    のテナントを作成します。ここでは、WebApp は 2 つの Web サーバー間で負荷分散を行う仮想サーバーです。
  - `"class": "Tenant"` - これは、`WorkshopExample` がテナントであることを示しています。
  - `as3_app_body` - これは、実際の WebApp である 2 番目の jinja2 テンプレートを参照する変数です。

----

2. `as3_template.j2`

<!-- {% raw %} -->
``` yaml
"web_app": {
    "class": "Application",
    "template": "http",
    "serviceMain": {
        "class": "Service_HTTP",
        "virtualAddresses": [
            "{{private_ip}}"
        ],
        "pool": "app_pool"
    },
    "app_pool": {
        "class": "Pool",
        "monitors": [
            "http"
        ],
        "members": [
            {
                "servicePort": 443,
                "serverAddresses": [
                    {% set comma = joiner(",") %}
                    {% for mem in pool_members %}
                        {{comma()}} "{{  hostvars[mem]['ansible_host']  }}"
                    {% endfor %}

                ]
            }
        ]
    }
}
```
<!-- {% endraw %} -->

このテンプレートは、Web アプリケーションの JSON 表現です。注意すべき重要な部分は以下のとおりです。

- `serviceMain` という名前の仮想サーバーがあります。
  - テンプレートは、前の演習のタスクと同様に変数を使用できます。この場合、仮想 IP アドレスはインベントリーからの private_ip
    になります。
- `app_pool` という名前のプールがあります
  - jinja2 テンプレートは、ループを使用してすべてのプールメンバーを取得できます（以下で説明される Web サーバーグループを参照します）。

**要約すると**、`tenant_base.j2` および `as3_template.j2` は、Web アプリケーションを表す単一の JSON ペイロードを作成します。この JSON ペイロードを F5 BIG-IP に送信する Playbook を構築します。

**VSCode のターミナルウィンドウを使用して、これらのテンプレートを作業用ディレクトリーにコピーしてください**
<!-- {% raw %} -->
```
mkdir j2
cp ~/f5-workshop/3.0-as3-intro/j2/* j2/
```
<!-- {% endraw %} -->

## ステップ 3:

VSCode を使用して、左側のペインの新規ファイルアイコンをクリックして、`as3.yml` という名前の新しいファイルを作成します。

![picture of create file
icon](../1.1-get-facts/images/vscode-openfile_icon.png)

## ステップ 4:

次のプレイ定義を `as3.yml` に入力します。
<!-- {% raw %} -->
``` yaml
---
- name: LINKLIGHT AS3
  hosts: lb
  connection: local
  gather_facts: false

  vars:
    pool_members: "{{ groups['web'] }}"
```
<!-- {% endraw %} -->

- ファイル上部の `---` は、これが YAML ファイルであることを示しています。  - `hosts: lb` は、プレイが lb
グループでのみ実行されることを示します。技術的には、F5 デバイスは 1 つだけしか存在しませんが、複数あれば、それぞれが同時に設定されます。  -
`connection: local` は、（自身に SSH 接続するのではなく）ローカルで実行するように Playbook に指示します  -
`gather_facts: false` はファクト収集を無効にします。この Playbook では、ファクト変数を使用しません。

- `vars` セクションは、`pool_members` という名前の変数を Web グループに設定します。ワークベンチには `node1` と
`node2` の 2 つの Web があります。つまり、`pool_members` 変数は 2 つの Web のリストを参照します。

## ステップ 5

以下を as3.yml Playbook に **追加します**。  

<!-- {% raw %} -->
``` yaml
  tasks:
    - name: CREATE AS3 JSON BODY
      set_fact:
        as3_app_body: "{{ lookup('template', 'j2/as3_template.j2', split_lines=False) }}"
```
<!-- {% endraw %} -->

モジュール [set_fact モジュール](https://docs.ansible.com/ansible/latest/modules/set_fact_module.html) により、Playbook はプレイ内のタスクとして変数を作成（または上書き）できます。これを使用して、プレイのその時点まで存在していなかったファクトを新たにその場で動的に作成することができます。この場合、[テンプレートルックアッププラグイン](https://docs.ansible.com/ansible/latest/plugins/lookup/template.html) が使用されます。このタスクは、
  1. 提供された j2/as3_template.j2 jinja テンプレートをレンダリングします。
  2. JSON テキストのみである `as3_app_body` という名前の新しいファクトを作成します。

## ステップ 6

以下を as3.yml Playbook に **追加します**。このタスクは、HTTP および HTTPS Web サービスとの対話に使用される uri モジュールを使用し、Digest、Basic、および WSSE HTTP 認証メカニズムをサポートします。このモジュールは非常に一般的で、非常に簡単に使用できます。ワークショップ自体（ワークベンチをプロビジョニングした Playbook）は uri モジュールを使用して Red Hat Ansible Tower の設定とライセンスを行います。

<!-- {% raw %} -->
``` yaml
    - name: PUSH AS3
      uri:
        url: "https://{{ ansible_host }}:8443/mgmt/shared/appsvcs/declare"
        method: POST
        body: "{{ lookup('template','j2/tenant_base.j2', split_lines=False) }}"
        status_code: 200
        timeout: 300
        body_format: json
        force_basic_auth: true
        user: "{{ ansible_user }}"
        password: "{{ ansible_password }}"
        validate_certs: false
      delegate_to: localhost
```
<!-- {% endraw %} -->

パラメーターの説明：

<table>
  <tr>
    <th>パラメーター</th>
    <th>説明</th>

  </tr>
  <tr>
    <td><code>- name: PUSH AS3</code></td>
    <td>Playbook タスクの人間用の説明、ターミナルウィンドウに出力します</td>
  </tr>
  <tr>
    <td><code>uri:</code></td>
    <td>このタスクは <a href="https://docs.ansible.com/ansible/latest/modules/uri_module.html">uri モード</a> を呼び出しています</td>
  </tr>
  <tr>
    <td><code>url: "https://{{ ansible_host }}:8443/mgmt/shared/appsvcs/declare"</code></td>
    <td>AS3 の Web URL (API)</td>
  </tr>
  <tr>
    <td><code>method: POST</code></td>
    <td>リクエストの HTTP メソッド、大文字でなければなりません。モジュールのドキュメントページに、すべてのオプションのリストが記載されています。<code>POST</code> ではなく <code>DELETE</code> とすることもできます</td>
  </tr>
  <tr>
    <td><code>body: "{{ lookup('template','j2/tenant_base.j2', split_lines=False) }}"</code></td>
    <td>このパラメーターは組み合わせたテンプレート (<code>as3_template.j2</code> が含まれる <code>tenant_base.j2</code>) を送信し、API リクエストのボディーとして渡されます。</td>
  </tr>
  <tr>
    <td><code>status_code: 200</code></td>
    <td>リクエストが成功したことを表す、有効な数値の <a href="https://en.wikipedia.org/wiki/List_of_HTTP_status_codes">HTTP ステータスコード</a>。ステータスコードのコンマ区切りリストとすることもできます。200 は OK を意味し、成功した HTTP リクエストに対する標準的な応答です</td>
  </tr>
</table>

残りのパラメーターは、F5 BIG-IP への認証用で、非常に簡単です（すべての BIG-IP モジュールと同様）。

## ステップ 7
Playbook を実行します。保存して VS Code サーバーのターミナルに戻り、以下を実行します。

<!-- {% raw %} -->
```
[student1@ansible ~]$ ansible-navigator run as3.yml --mode stdout
```
<!-- {% endraw %} -->

# Playbook の出力

出力は次のようになります。

<!-- {% raw %} -->
```yaml
[student1@ansible ~]$ ansible-navigator run as3.yml --mode stdout

PLAY [Linklight AS3] **********************************************************

TASK [Create AS3 JSON Body] ***************************************************
ok: [f5]

TASK [Push AS3] ***************************************************************
ok: [f5]

PLAY RECAP ********************************************************************
f5                         : ok=2    changed=0    unreachable=0    failed=0
```
<!-- {% endraw %} -->

# ソリューション

完成した Ansible Playbook
が、回答キーとしてここで提供されています。[as3.yml](https://github.com/network-automation/linklight/blob/master/exercises/ansible_f5/3.0-as3-intro/as3.yml)
を表示するには、ここをクリックしてください。

# ソリューションの確認

Web ブラウザーで F5 にログインし、設定された内容を確認します。lab_inventory/hosts ファイルから F5 ロードバランサーの
IP 情報を取得し、https://X.X.X.X:8443/ のように入力します。

![f5 gui as3](f5-as3.gif)

1. 左側のメニューで Local Traffic をクリックします
2. Virtual Servers をクリックします。
3. 右上の `Partition` というドロップダウンメニューをクリックし、WorkshopExample を選択します
4. 仮想サーバー `serviceMain` が表示されます。

----

You have finished this exercise.  [Click here to return to the lab
guide](../README.md)
