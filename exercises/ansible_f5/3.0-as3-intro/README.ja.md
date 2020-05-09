# 演習 3.0 - AS3の概要

**Read this in other languages**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

## 目次

- [目的](#目的)
- [解説](#解説)
- [Playbook の出力](#Playbookの出力)
- [解答](#解答)

# 目的

F5 AS3 を使った virtual server 構築(Section 1 Ansible F5 Exercisesで学んだもの)のデモンストレーション

  - AS3([Application Services 3 拡張](https://clouddocs.f5.com/products/extensions/f5-appsvcs-extension/3/userguide/about-as3.html)) の宣言型モデルについて学習します。AS3 を徹底的に学ぶことはこの演習の意図ではありませんが、概念をいくらか紹介して、それがAnsible Playbook と、どのように簡単な統合がなされているかを示すだけです。
  - [set_fact モジュール](https://docs.ansible.com/ansible/latest/modules/set_fact_module.html) について学びます。
  - [uri モジュール](https://docs.ansible.com/ansible/latest/modules/uri_module.html) について学びます。


# Guide

#### BIG-IP の設定がクリーンになっていることを確認し、次に進む前に [演習 2.1 - コンフィグの削除](../2.1-delete-configuration/README.ja.md)  を必ず実行してください。

## Step 1:

お使いの F5 BIG-IP は AS3 が有効になっている事を確認してください。

  1. Webブラウザーから F5 BIG-IP にログインします。
  2. 左側のメニューから iApps ボタンをクリックします。
  3. `Package Management LX` のリンクをクリックします。
  4. `f5-appsvcs` がインストールされている事を確認します。

これでうまくいかない場合は、インストラクターに助けを求めましょう。

![f5 gui](f5-appsvcs.gif)

## Step 2:

Playbook を作り始める前に、AS3 がどのように動くのか理解する必要があります。AS3 は F5 BIG-IP を API 呼び出しを行う際に JSON テンプレートを渡す必要があります。この演習のテンプレートは提供されます。受講者は、すべてのパラメーターについて完全に理解する必要はありません。また、ゼロからテンプレートを作れる必要はありません。
これらは2つのパートに分かれています。

1. `tenant_base.j2`

```
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

 `tenant_base` は標準テンプレートです。F5 Networks が自社の顧客に対して提供しています。もっとも重要なパートとしては:

  - `"WorkshopExample": {` - これは Tenant の名前です。AS3 は 特別な WebApp のための Tenant を作ります。WebApp は、今回の場合、virtual server を示します。2つの Web サーバーに対してロードバランスします。
  - `"class": "Tenant",` - `WorkshopExample` は Tenant であることを示します。
  - `as3_app_body` - これは現在の WebApp に対する 2つ目の Jinja2 テンプレートの名前を示す変数です。

----

2. `as3_template.j2`

{% raw %}
```
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
{% endraw %}

このテンプレートは Web アプリケーションに対する JSON の表記です。ここのパートで重要な点としては、

- 今回の virtual server の名前は `serviceMain` です。
  - 以前の演習のタスクで行ったようにテンプレートの中で変数を使用できます。この場合、virtual IP address は、定義したインベントリー中に定義されている private_ip です。
- `app_pool` という名前の Pool があります。
  - Jinja2 テンプレートはループ処理を使用して、すべての Pool member (これは web servers グループを指しています)を取得できます。

** 要約 **
`tenant_base.j2` と `as3_template.j2` の2つのテンプレートファイルは、Web アプリケーションのための1つの JSON ペイロードを作ります。次に Playbook を構築することで F5 BIG-IP に対して、この JSON ペイロードを送ります。

**これらのテンプレートを作業ディレクトリにコピーしてください。**

```
mkdir j2
cp ~/f5-workshop/3.0-as3-intro/j2/* j2/
```

## Step 3:

テキストエディターを使って `as3.yml` という名前でファイルを作成します。

> コントロールノードでは `vim` と `nano`、また、RDP 経由では Visual Studio と Atom が利用可能です。

## Step 4:

以下の定義を Playbook `as3.yml` の先頭に入力してください:

``` yaml
---
- name: LINKLIGHT AS3
  hosts: lb
  connection: local
  gather_facts: false

  vars:
    pool_members: "{{ groups['web'] }}"
```
- `---` はファイルの先頭である事を示します。このファイルは YAML ファイルです。
- `hosts: lb` は lb グループに属するホストに対してのみ処理を実行するという意味です。F5 デバイスは今回1つだけですが、しかし、複数台ある場合には複数台を同時に指定できます。
- `connection: local` を指定することで　Playbook がローカル実行されます。(SSHで接続せず)
- `gather_facts: false` を指定することで facts の収集を無効化します。これは今回の Playbook 中で、facts を何も利用しないためです。

以下のセクションは
```
  vars:
    pool_members: "{{ groups['web'] }}"
```
... `pool_members` と呼ばれる変数を定義し、web グループを値として指定します。workbench に2台のWebサーバーがあり、`pool_members` の値を参照することで2台のWebサーバーのリストを取得することができます。

## Step 5

** 追記 ** 次のタスクをPlaybook `as3.yml` の後ろに追記します。

```
  tasks:

  - name: CREATE AS3 JSON BODY
    set_fact:
      as3_app_body: "{{ lookup('template', 'j2/as3_template.j2', split_lines=False) }}"
```

この [set_fact モジュール](https://docs.ansible.com/ansible/latest/modules/set_fact_module.html) は、Playbook 内のタスクにおいて使用できる変数を作成(再定義)することができます。これにより新しい facts を動的に作成することができます。今回の場合、 [template lookup プラグイン](https://docs.ansible.com/ansible/latest/plugins/lookup/template.html) を使用します。このタスクには以下の内容を記述しています。
  1. 表示用にJinja2 テンプレート `j2/as3_template.j2` が提供されている
  2. `as3_app_body` という新しい fact を作成する(中身はJSON 形式のテキスト)

## Step 6

** 追記 ** 以下は as3.yml の Playbook に追記します。このタスクは uri モジュールを使い、HTTP および HTTPS Web サービスと対話するためのものです。Digest認証、Basic認証、および WSSE HTTP 認証メカニズムをサポートします。このモジュールは非常に一般的で非常に使いやすいです。このワークショップの演習環境をプロビジョニングした Playbook の中でで uri モジュールを使って、Red Hat Ansible Tower の設定や、ライセンス登録を行っています。

```
  - name: PUSH AS3
    uri:
      url: "https://{{ ansible_host }}:8443/mgmt/shared/appsvcs/declare"
      method: POST
      body: "{{ lookup('template','j2/tenant_base.j2', split_lines=False) }}"
      status_code: 200
      timeout: 300
      body_format: json
      force_basic_auth: yes
      user: "{{ ansible_user }}"
      password: "{{ ansible_ssh_pass }}"
      validate_certs: no
    delegate_to: localhost
```

パラメーターの説明:

<table>
  <tr>
    <th>parameter</th>
    <th>explanation</th>

  </tr>
  <tr>
    <td><code>- name: PUSH AS3</code></td>
    <td>human description of Playbook task, prints to terminal window</td>
  </tr>
  <tr>
    <td><code>uri:</code></td>
    <td>this task is calling the <a href="https://docs.ansible.com/ansible/latest/modules/uri_module.html">uri module</a></td>
  </tr>
  <tr>
    <td><code>url: "https://{{ ansible_host }}:8443/mgmt/shared/appsvcs/declare"</code></td>
    <td>webURL (API) for AS3</td>
  </tr>
  <tr>
    <td><code>method: POST</code></td>
    <td>HTTP method of the request, must be uppercase.  Module documentation page has list of all options.  This could also be a <code>DELETE</code> vs a <code>POST</code></td>
  </tr>
  <tr>
    <td><code>body: "{{ lookup('template','j2/tenant_base.j2', split_lines=False) }}"</code></td>
    <td>This sends the combined template (the <code>tenant_base.j2</code> which contains <code>as3_template.j2</code>) and is passed as the body for the API request.</td>
  </tr>
  <tr>
    <td><code>status_code: 200</code></td>
    <td>A valid, numeric, <a href="https://en.wikipedia.org/wiki/List_of_HTTP_status_codes">HTTP status code</a> that signifies success of the request. Can also be comma separated list of status codes.  200 means OK, which is a standard response for successful HTTP requests</td>
  </tr>
</table>

残りのパラメーターは、F5 BIG-IP への認証するためのもので、かなり簡単です。(すべての BIG-IP モジュールで共通)

## Step 7
Playbook を実行します - コントロールホストのコマンドラインに戻って次のコマンドを実行します。

```
[student1@ansible ~]$ ansible-playbook as3.yml
```

# Playbookの出力

実行時の出力結果は次のようになります。

```yaml
[student1@ansible ~]$ ansible-playbook as3.yml

PLAY [Linklight AS3] ***********************************************************

TASK [Create AS3 JSON Body] ****************************************************
ok: [f5]

TASK [Push AS3] ****************************************************************
ok: [f5 -> localhost]

PLAY RECAP *********************************************************************
f5                         : ok=2    changed=0    unreachable=0    failed=0
```

# 解答

Ansible Playbookが完了したら、Answer キーが提供されます。こちらをクリック！ [as3.yml](./as3.yml).

# 解答の確認

Webブラウザーから F5 BIG-IP にログインして、設定が行われている事を確認しましょう。lab_inventory/hosts というインベントリファイルから F5 ロードバランサーのIP情報を取得してください。ブラウザーには「https://X.X.X.X:8443/」のような感じで HTTPS にて 8443 ポートにアクセスします。

![f5 gui as3](f5-as3.gif)

1. 左側のメニューから Local Traffic をクリックします。
2. 次に Virtual Servers をクリックします。
3. 右側の上部の `Partition` のドロップダウンメニューを開き、WorkshopExample を選択します。
4. Virtual Server `serviceMain` を開きます。

----

この演習は完了です。 [Lab ガイドに戻ってください。](../README.ja.md)
