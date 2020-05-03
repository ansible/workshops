# Exercise 4 - Jinja2 template を使ったネットワーク設定

**別の言語で読む**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
- [Takeaways](#takeaways)
- [Solution](#solution)

# Objective

ネットワーク構成をテンプレート化して機器に送ります。

- 必要となるIPアドレスをグループ[変数](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html) にストアして利用する。
- [Jinja2 template lookup plugin](https://docs.ansible.com/ansible/latest/plugins/lookup.html) を利用する。
- [cli_config モジュール](https://docs.ansible.com/ansible/latest/modules/cli_config_module.html) を利用してネットワーク自動化を確認する。

# Guide

#### Step 1

このステップでは Ansible の変数を作成して Playbook の中で利用します。この演習では以下のIPアドレスを rtr1 と rtr2 のループバックアドレスとして利用します:

Device  | Loopback100 IP |
------------ | ------------- |
rtr1  | 192.168.100.1/32 |
rtr2  | 192.168.100.2/32 |

変数の情報は host_vars と group_vars に格納することができます。この演習のために `group_vars` という名前のディレクトリを作成します:

```bash
[student1@ansible network-workshop]$ mkdir ~/network-workshop/group_vars
```

そしてこのディレクトリ内に `all.yml` という名前のファイルを好きなエディタで作成してください。コントローラーノードでは vim か nano がインストールされています。

```
[student1@ansible network-workshop]$ nano group_vars/all.yml
```

インターフェースとIPアドレスの情報は Playbook から利用できるように、変数として上記のファイルに格納されている必要があります。上記のテーブル表を格納するためにシンプルな YAML の辞書データを作ることから始めます。トップレベルの変数(例えば `nodes`)を使用し、`inventory_hostname` に基づいて検索可能となるよう以下のように定義します:

```yaml
nodes:
  rtr1:
    Loopback100: "192.168.100.1"
  rtr2:
    Loopback100: "192.168.100.2"
```

group_vars/all.yml ファイルに上記の YAML 辞書データを記入して保存します。

>全てのデバイスはデフォルトで **all** グループの一部です。もし **cisco** グループを作成し、このグループにしか所属しないデバイスがあったとしても、この変数にはアクセスすることができます。

#### Step 2

`template.j2` という名前のファイルを作成します:

```
[student1@ansible network-workshop]$ nano template.j2
```

以下を template.j2 ファイルに記述します:

<!-- {% raw %} -->
```yaml
{% for interface,ip in nodes[inventory_hostname].items() %}
interface {{interface}}
  ip address {{ip}} 255.255.255.255
{% endfor %}
```
<!-- {% endraw %} -->


ファイルを保存します。

#### Step 3

このステップでは新しく作成された template.j2 ファイルの各行について詳しく説明します。

<!-- {% raw %} -->
```yaml
{% for interface,ip in nodes[inventory_hostname].items() %}
```
<!-- {% endraw %} -->

<!-- {% raw %} -->
- Jinja テンプレートの中ではコード部分は `{%` と `%}` でエスケープされます。`for` はループ処理の開始をプログラムに指示します。`interface,ip` は、辞書形式を `interface` という名前のキーと、`ip` という名前の値に分解します。
<!-- {% endraw %} -->

- `nodes[inventory_hostname]` は辞書形式で、`group_vars/all.yml` ファイルの中を検索します。**inventory_hostname** はインベントリーファイルの中で設定されたホスト名が入ります。Playbookが `rtr1` に対して実行されるときには inventory_hostname は `rtr1` となり、`rtr2` に対して実行されるときには inventory_hostname は `rtr2` となり、その他も同様です。

>変数 inventory_hostname は自動的に提供される [magic variable](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#magic-variables-and-how-to-access-information-about-other-hosts) です。

- `items()` キーワードは辞書形式のリストを返します。この場合は、辞書形式のキーはインターフェース名 (例 Loopback100) で、値は IP アドレス (例 192.168.100.1)となります。

<!-- {% raw %} -->
```yaml
interface {{interface}}
  ip address {{ip}} 255.255.255.255
```
<!-- {% endraw %} -->

- 変数は次のように中括弧で表現します: `{{ variable_here }}`  この場合、変数名のキーと値はループの中に存在しています。ループの外側でこの2つの変数は存在しません。それぞれの繰り返しで変数の値は、元の変数値に基づいて再割当てされます。

最終行:
<!-- {% raw %} -->
```
{% endfor %}
```
<!-- {% endraw %} -->

- Jinja の中ではループの終了が必要となります。

#### Step 4

config.yml という Playbook を作成します:

```
[student1@ansible network-workshop]$ nano config.yml
```

以下を config.yml へと記述します:

<!-- {% raw %} -->
```
---
- name: configure network devices
  hosts: rtr1,rtr2
  gather_facts: false
  tasks:
    - name: configure device with config
      cli_config:
        config: "{{ lookup('template', 'template.j2') }}"
```
<!-- {% endraw %} -->

- この Playbook は *configure device with config* と名付けられた1つのタスクを持ちます。
- **cli_config** モジュールはベンダー非依存です。このモジュールは Arista、Cisco、Juniper に対して同じように動作します。このモジュールは **network_cli** コネクションプラグインを利用しているときにのみ動作します。
- cli_config モジュールは1つのパラメーターが必要で、ここでは **config** です。ここには lookup プラグインで検索されるフラットファイルを指定しています。利用可能な lookup プラグインはこちらです [visit the documentation](https://docs.ansible.com/ansible/latest/plugins/lookup.html)  
- template lookup プラグインは2つのパラメーターを必要とします。プラグインのタイプである *template* と対応したテンプレート名の *template.j2* です。

#### Step 5

Playbook を実行します:

```
[student1@ansible network-workshop]$ ansible-playbook config.yml
```

出力は以下のようになるはずです。

```
[student1@ansible ~]$ ansible-playbook config.yml

PLAY [rtr1,rtr2] ********************************************************************************

TASK [configure device with config] ********************************************************************************
changed: [rtr1]
changed: [rtr2]

PLAY RECAP ********************************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
rtr2                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

#### Step 6

`show ip int br` コマンドを実行して、ネットワークデバイスに設定されたIPアドレスを確認します。

```
[student1@ansible network-workshop]$ ssh rtr1

rtr1#show ip int br | include Loopback100
Loopback100            192.168.100.1   YES manual up                    up
```

# Takeaways

- [Jinja2 template lookup plugin](https://docs.ansible.com/ansible/latest/plugins/lookup.html) はデバイスのコンフィグをテンプレート化することが可能です。
- `*os_config` (例 ios_config) と cli_config モジュールは Jinja2 テンプレートを読み込み、機器に直接プッシュすることが可能です。もしコントローラーノード上で単純にコンフィグファイルを記述したい場合は [template モジュール](https://docs.ansible.com/ansible/latest/modules/template_module.html) が利用できます。
- 変数は一般的に group_vars と host_vars に格納されています。この演習では group_vars を利用しました。

# Solution

完成したPlaybookはここから参照できます: [config.yml](config.yml).

完成したJinja2 templateはここから参照できます: [template.j2](template.j2).

---

# Complete

以上で exercise 4 は終了です。

[Click here to return to the Ansible Network Automation Workshop](../README.ja.md)
