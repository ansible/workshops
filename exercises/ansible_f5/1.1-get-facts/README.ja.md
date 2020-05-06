# 演習 1.1 - Ansible による F5 BIG-IP の情報収集

**Read this in other languages**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

## 目次

- [目的](#目的)
- [解説](#解説)
- [Playbookの出力](#playbookの出力)
- [解答](#解答)
- [より深く](#より深く)

# 目的

[BIG-IP Facts module](https://docs.ansible.com/ansible/latest/modules/bigip_device_facts_module.html) を使って F5 BIG-IP 機器から情報を取得し、[debug module](https://docs.ansible.com/ansible/latest/modules/debug_module.html) でターミナルに情報を表示します。

# 解説

ホームディレクトリにいることを確認してください。

```
[student1@ansible f5-workshop]$ cd ~
```

## Step 1:

テキストエディタを使って `bigip-facts.yml` ファイルを作成します。

```
[student1@ansible ~]$ nano bigip-facts.yml
```

>`vim` と`nano` がコントールノードで利用できます。もしくは RDP で接続して Visual Studio と Atom を利用することも可能です。

## Step 2:

Ansible の playbook は **YAML** ファイルです。YAML は構造化されたエンコードで人にとって読みやすい形式です(JSON と違い・・・)

以下の play 定義を `bigip-facts.yml` に追加してください:

``` yaml
---
- name: GRAB F5 FACTS
  hosts: f5
  connection: local
  gather_facts: no
```

- ファイルの先頭の `---` はこのファイルが YAML であることを示します。
- `hosts: f5` はこの play が F5 BIG-IP 機器のグループに対して実行されることを示します。
- `connection: local` は Playbook がローカル実行されることを示します。
- `gather_facts: no` Fact 情報の収集を無効にします。この演習では Playbook の中で Fact 情報を利用しません。

## Step 3

次に最初の `task` を追加します。 このタスクでは `device_facts` モジュールを利用して BIG-IP から情報を取得します。

{% raw %}
``` yaml
---
- name: GRAB F5 FACTS
  hosts: f5
  connection: local
  gather_facts: no


  tasks:

    - name: COLLECT BIG-IP FACTS
      bigip_device_facts:
        gather_subset:
         - system-info
        provider:
          server: "{{private_ip}}"
          user: "{{ansible_user}}"
          password: "{{ansible_ssh_pass}}"
          server_port: 8443
          validate_certs: no
      register: device_facts
```
{% endraw %}

>`play` はタスクのリストです。タスクとリストは1：1の関係を持ちます。Ansible モジュールは再利用可能で、Ansible API、`ansible` `ansible-playbook` コマンドから利用できるスタンドアローンなスクリプトです。実行されたモジュールは Ansible に JSON 形式の文字列を返します。

- `name: COLLECT BIG-IP FACTS` は利用者が定義するタスクの説明文で、この内容がターミナルに表示されます。
- `bigip_device_facts:` はタスクで使用されるモジュール名を指定します。`register` 以外のモジュールパラメーターはドキュメントページで説明されています。
- `gather_subset: system_info` モジュールのパラメーターです。モジュールに対してシステムレベルの情報のみを取得するように指示します。
- `server: "{{private_ip}}"` モジュールのパラメーターです。モジュールがどのBIG-IPのIPアドレスに接続するかを指定します。ここではインベントリーで定義された`private_ip`が指定されています。
- `user: "{{ansible_user}}"` モジュールのパラメーターです。BIP-IPにログインするユーザー名を設定しています。
- `password: "{{ansible_ssh_pass}}"` モジュールのパラメーターです。BIG-IPにログインするパスワードを指定します。
- `server_port: 8443` モジュールのパラメーターです。BIP-IPに接続する際のポート番号を指定します。
- `register: device_facts` このタスクで取得された情報を変数 `device_facts` へ格納するように指示しています。

## Step 4

次に2つ目の `task` を追加します。 このタスクでは `debug` モジュールを使って、register
された `bigip_device_facts variable` 変数の値を出力します。

{% raw %}
```yaml
---
- name: GRAB F5 FACTS
  hosts: f5
  connection: local
  gather_facts: no


  tasks:

    - name: COLLECT BIG-IP FACTS
      bigip_device_facts:
        include: system_info
        provider:
          server: "{{private_ip}}"
          user: "{{ansible_user}}"
          password: "{{ansible_ssh_pass}}"
          server_port: 8443
          validate_certs: no
      register: device_facts

    - name: DISPLAY COMPLETE BIG-IP SYSTEM INFORMATION
      debug:
        var: device_facts
```
{% endraw %}

- `name: COMPLETE BIG-IP SYSTEM INFORMATION` はユーザーが指定するタスクの説明文です。この内容がターミナルへ表示されます。
- `debug:` タスクで使用するモジュール指定しています。
- `var: device_facts` モジュールのパラメーターです。`device_facts` 変数の値を出力するように指定しています。


## Step 5

Playbook の実行 - コマンドラインへ戻ったら以下のコマンドでPlaybookを実行してください:

```
[student1@ansible ~]$ ansible-playbook bigip-facts.yml
```

## Step 6

最後に、2つのタスクを追加して取得したファクト情報から特定の情報を取得します。

{% raw %}
```yaml
---
- name: GRAB F5 FACTS
  hosts: f5
  connection: local
  gather_facts: no

  tasks:
    - name: COLLECT BIG-IP FACTS
      bigip_device_facts:
        gather_subset:
         - system-info
        provider:
          server: "{{private_ip}}"
          user: "{{ansible_user}}"
          password: "{{ansible_ssh_pass}}"
          server_port: 8443
          validate_certs: no
      register: device_facts

    - name: DISPLAY COMPLETE BIG-IP SYSTEM INFORMATION
      debug:
        var: device_facts

    - name: DISPLAY ONLY THE MAC ADDRESS
      debug:
        var: device_facts['system_info']['base_mac_address']

    - name: DISPLAY ONLY THE VERSION
      debug:
        var: device_facts['system_info']['product_version']
```
{% endraw %}


- `var: device_facts['system_info']['base_mac_address']` BIG-IP のMACアドレスを取得します。
- `var: device_facts['system_info']['product_version']` BIG-IP のバージョン情報を取得します。

>`bigip_device_facts` モジュールは構造化されたデータを返すため、やっかいな正規表現やフィルターを使わずに必要な情報へと簡単にアクセスできます。Fact モジュールは後続のタスクに渡すデータを取得したり、動的なドキュメント作成(報告書, csv ファイル, markdown)するためにとても有益です。


## Step 7

Playbook の実行 - コマンドラインへ戻ったら以下のコマンドでPlaybookを実行してください:

```
[student1@ansible ~]$ ansible-playbook bigip-facts.yml
```

# Playbookの出力

以下のような出力となるはずです。

{% raw %}
```yaml
[student1@ansible ~]$ ansible-playbook bigip-facts.yml

PLAY [GRAB F5 FACTS] ****************************************************************************************************************************************

TASK [COLLECT BIG-IP FACTS] *********************************************************************************************************************************
changed: [f5]

TASK [DISPLAY COMPLETE BIG-IP SYSTEM INFORMATION] ***********************************************************************************************************
ok: [f5] => {
    "device_facts": {
        "changed": true,
        "failed": false,
        "system_info": {
            "base_mac_address": "0a:54:53:51:86:fc",
            "chassis_serial": "685023ec-071e-3fa0-3849dcf70dff",
            "hardware_information": [
                {
                    "model": "Intel(R) Xeon(R) CPU E5-2676 v3 @ 2.40GHz",
                    "name": "cpus",
                    "type": "base-board",
                    "versions": [
                        {
                            "name": "cpu stepping",
                            "version": "2"
                        },
                        {
                            "name": "cpu sockets",
                            "version": "1"
                        },
                        {
                            "name": "cpu MHz",
                            "version": "2399.981"
                        },
                        {
                            "name": "cores",
                            "version": "2  (physical:2)"
                        },
                        {
                            "name": "cache size",
                            "version": "30720 KB"
                        }
                    ]
                }
            ],
            "marketing_name": "BIG-IP Virtual Edition",
            "package_edition": "Point Release 7",
            "package_version": "Build 0.0.1 - Tue May 15 15:26:30 PDT 2018",
            "platform": "Z100",
            "product_build": "0.0.1",
            "product_build_date": "Tue May 15 15:26:30 PDT 2018",
            "product_built": 180515152630,
            "product_changelist": 2557198,
            "product_code": "BIG-IP",
            "product_jobid": 1012030,
            "product_version": "13.1.0.7",
            "time": {
                "day": 15,
                "hour": 23,
                "minute": 46,
                "month": 4,
                "second": 25,
                "year": 2019
            },
            "uptime": 1738.0
        }
    }
}

TASK [DISPLAY ONLY THE MAC ADDRESS] *************************************************************************************************************************
ok: [f5] => {
    "device_facts['system_info']['base_mac_address']": "0a:54:53:51:86:fc"
}

TASK [DISPLAY ONLY THE VERSION] *****************************************************************************************************************************
ok: [f5] => {
    "device_facts['system_info']['product_version']": "13.1.0.7"
}

PLAY RECAP **************************************************************************************************************************************************
f5                         : ok=4    changed=1    unreachable=0    failed=0

```
{% endraw %}


# 解答

完成したPlaybookのサンプルは [bigip-facts.yml](./bigip-facts.yml) から参照できます。

# より深く

オプション演習で `tags: debug` パラメーターを１つの debug タスクに追加してみましょう。

```yaml
- name: DISPLAY COMPLETE BIG-IP SYSTEM INFORMATION
  debug:
    var: device_facts
  tags: debug
```

`--skip-tags=debug` オプションをつけてコマンドを実行します。

```
ansible-playbook bigip-facts.yml --skip-tags=debug
```

`DISPLAY COMPLETE BIG-IP SYSTEM INFORMATION` タスクがスキップされ、３つのタスクの結果が表示されたはずです。

本演習は終了です。  [Click here to return to the lab guide](../README.ja.md)
