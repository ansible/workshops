# 追加の演習: Ansible ネットワークリソースモジュール

**他の言語でもお読みいただけます**: ![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English](README.md)、![japan](https://github.com/ansible/workshops/raw/devel/images/japan.png) [日本語](README.ja.md).

## 目次

  * [目的](#objective)
    * [ステップ 1 - Arista のコンフィグを手動で変更する](#step-1---manually-modify-the-arista-configuration)
    * [ステップ 2 - Playbook の実行](#step-2---run-the-playbook)
    * [ステップ 3 - Playbook の変更](#step-3---modify-the-playbook)
    * [ステップ 4 - replaced に変更した Playbook を実行する](#step-4---run-replaced-playbook) 
    * [ステップ 5 - rtr2 に VLAN を追加する](#step-5---add-a-vlan-to-rtr2)
    * [ステップ 6 - overridden パラメーターの使用](#step-6---use-overridden-parameter)
    * [ステップ 7 - rendered パラメーターの使用](#step-7---using-rendered-parameter)
    * [ステップ 8 - parsed パラメーターの使用](#step-8---using-the-parsed-parameter)
  * [重要なこと](#takeaways)
  * [ソリューション](#solution)
  * [完了](#complete)

## 目的

[Ansible ネットワークリソースモジュール](https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html)のデモ使用

この演習は [演習 4 - Ansible ネットワークリソースモジュール](../../4-resource-module/README.ja.md)に基づいています。 演習を始める前に、演習 4 を完了させてください。

この演習には 2 つのパートがあります。

1. 設定用の `state` パラメーターを扱います

  * `replaced`
  * `overridden`

  さらに `merged` で確認したものと対比します。

2. 読み取り専用の `state` パラメーターを扱います

  * `rendered`
  * `parsed`

  さらに `gathered` パラメーターと比較します。

### ステップ 1 - Arista のコンフィグを手動で変更する

* Arista スイッチにログインします。演習 4 のコンフィグが既に適用されていることを前提としています。

  ```bash
  vlan 20
     name desktops
  !
  vlan 30
     name servers
  !
  vlan 40
     name printers
  !
  vlan 50
     name DMZ
  ```

* コントロールノードのターミナルから、`ssh rtr2` に続いて `enable` と入力します。

  ```bash
  $ ssh rtr2
  Last login: Wed Sep  1 13:44:55 2021 from 44.192.105.112
  rtr2>enable
  ```

* `configure terminal` コマンドを使用して、手動でAristaのコンフィグを変更します。

  ```bash
  rtr2#configure terminal
  rtr2(config)#
  ```
* ここで vlan 50 を `state suspend` に設定します。

  ```bash
  rtr2(config)#vlan 50
  rtr2(config-vlan-50)#state ?
    active   VLAN Active State
    suspend  VLAN Suspended State

  rtr2(config-vlan-50)#state suspend
  ```

* コンフィグを保存します。

  ```bash
  rtr2(config-vlan-50)#exit
  rtr2(config)#end
  rtr2#copy running-config startup-config
  Copy completed successfully.
  ```

* コンフィグを確認します。

  ```bash
  rtr2#sh run | s vlan
  vlan 20
     name desktops
  !
  vlan 30
     name servers
  !
  vlan 40
     name printers
  !
  vlan 50
     name DMZ
     state suspend
  ```

  * running-configuration は Playbook と一致しなくなりました! vlan 50 は現在 suspend という状態です。

### ステップ 2 - Playbook の実行

* `ansible-navigator run` コマンドを使用して、Playbook を実行します。

  ```bash
  $ ansible-navigator run resource.yml --mode stdout
  ```

* 以下のように表示されます。

  ```bash
  [student@ansible-1 network-workshop]$ ansible-navigator run resource.yml --mode stdout

  PLAY [configure VLANs] *********************************************************

  TASK [use vlans resource module] ***********************************************
  ok: [rtr4]
  ok: [rtr2]

  PLAY RECAP *********************************************************************
  rtr2                       : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
  rtr4                       : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  
  ```

* Playbook はコンフィグを変更しませんでした。 `state: merged` は、指定された構成がネットワークデバイスに存在することのみを強制します。Arista デバイスにログインすると、まだ `state suspend` が表示されます。

### ステップ 3 - Playbook の変更

* Playbook `resource.yml` を変更して、`state: merged` を `state: replaced` にします。

* Playbook は以下のようになります。

  ```yaml
  ---
  - name: configure VLANs
    hosts: arista
    gather_facts: false

    tasks:

    - name: use vlans resource module
      arista.eos.vlans:
        state: replaced
        config:
          - name: desktops
            vlan_id: 20
          - name: servers
            vlan_id: 30
          - name: printers
            vlan_id: 40
          - name: DMZ
            vlan_id: 50
  ```

### ステップ 4 - replaced に変更した Playbook を実行する

* `ansible-navigator run` コマンドを使用して Playbook を実行します。 タスクは 1 つしかないので、`--mode stdout` を使用できます。

  ```bash
  $ ansible-navigator run resource.yml --mode stdout
  ```

* 以下のように表示されます。

  ```bash
  $ ansible-navigator run resource.yml --mode stdout

  PLAY [configure VLANs] *********************************************************

  TASK [use vlans resource module] ***********************************************
  changed: [rtr4]
  changed: [rtr2]

  PLAY RECAP *********************************************************************
  rtr2                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
  rtr4                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
  ```
* rtr2 のコンフィグを確認すると `state suspend` がなくなっています。`replaced` は、指定された設定を (指定された VLAN に対して) 強制します。これは、`state: suspend` が指定されておらず、VLAN のデフォルトではないため、ネットワークデバイスから `state suspend` が削除されることを意味します。

### ステップ 5 - rtr2 に VLAN を追加する

* `rtr2`に vlan 100 を追加します。

  ```bash
  rtr2(config)#vlan 100
  rtr2(config-vlan-100)#name ?
    WORD  The ASCII name for the VLAN
  rtr2(config-vlan-100)#name artisanal
  ```

* 誰かが自動化の外でこの VLAN を作成したと想定できます (たとえば、VLAN を手作業で作成した、今回の場合 artisanal VLAN)。これは、アウトオブバンドのネットワークの変更と呼ばれます。これはネットワーク業界で非常によくあることで、ネットワークエンジニアが問題を解決した後、文書化したり、この設定を削除するために周到に準備したりすることがなかったからです。この手動による構成の変更は、ベストプラクティスや文書化されたポリシーと一致しません。これにより、誰かが将来この VLAN を使用しようとして、この設定を認識しないという問題が発生する可能性があります。

  ```bash
  rtr2#show vlan
  VLAN  Name                             Status    Ports
  ----- -------------------------------- --------- -------------------------------
  1     default                          active   
  20    desktops                         active   
  30    servers                          active   
  40    printers                         active   
  50    DMZ                              active   
  100   artisanal                        active   
  ```

* Playbook を再実行します。VLAN 100 は削除されません。

### ステップ 6 - overridden パラメーターの使用

* 再度 Playbook を変更します。今回は `state: overridden` を使用します。

    ```yaml
    ---
    - name: configure VLANs
      hosts: arista
      gather_facts: false

      tasks:

      - name: use vlans resource module
        arista.eos.vlans:
          state: overridden
          config:
            - name: desktops
              vlan_id: 20
            - name: servers
              vlan_id: 30
            - name: printers
              vlan_id: 40
            - name: DMZ
              vlan_id: 50
    ```
* `ansible-navigator run` コマンドを使用して、Playbook を実行します。

  ```bash
  $ ansible-navigator run resource.yml --mode stdout
  ```
* デバイス `rtr2` にログインして、VLAN を確認します。
  ```bash
  rtr2#show vlan
  VLAN  Name                             Status    Ports
  ----- -------------------------------- --------- -------------------------------
  1     default                          active   
  20    desktops                         active   
  30    servers                          active   
  40    printers                         active   
  50    DMZ                              active
  ```

* artisanal VLAN 100 が削除されました! 同じリソースモジュールを使用して、ネットワークデバイスを設定するだけでなく、どの VLAN を構成するかを強制することもできます。これはポリシーの適用と呼ばれ、構成管理の大部分を占めます。 `merged` から `replaced`、`overridden` への移行は、ネットワークチームが自動化にますます自信を持てるようになるにつれて、多くの場合、自動化ジャーニーと一致します。

### ステップ 7 - rendered パラメーターの使用

ここで、読み取り専用パラメーターの使用に戻りましょう。これらのパラメーターは、ネットワークデバイスの設定を変更しません。演習 4 では、`state: gathered` を使用して、Arista ネットワークデバイスから VLAN の設定を取得しました。今回は、`rendered` を使用して、Arista の設定コマンドを取得します。

* Playbook `resource.yml` を変更して、`state: rendered` します。

* タスクの実行結果を変数 `rendered_config` に登録します。

* ターミナルウィンドウに出力するために `debug` タスクを追加します。

* Playbook は以下のようになります。

{% raw %}
  ```yaml
  - name: use vlans resource module
    arista.eos.vlans:
      state: rendered
      config:
        - name: desktops
          vlan_id: 20
        - name: servers
          vlan_id: 30
        - name: printers
          vlan_id: 40
        - name: DMZ
          vlan_id: 50
    register: rendered_config

  - name: use vlans resource module
      debug:
        msg: "{{ rendered_config }}"
  ```
  {% endraw %}

* `ansible-navigator run` コマンドを使用して、Playbook を実行します。

  ```bash
  $ ansible-navigator run resource.yml --mode stdout

* 以下のように表示されます。

  ```bash
  [student@ansible-1 network-workshop]$ ansible-navigator run resource.yml --mode stdout

  PLAY [configure VLANs] *********************************************************

  TASK [use vlans resource module] ***********************************************
  ok: [rtr2]
  ok: [rtr4]

  TASK [use vlans resource module] ***********************************************
  ok: [rtr4] => {
      "msg": {
          "ansible_facts": {
              "discovered_interpreter_python": "/usr/bin/python"
          },
          "changed": false,
          "failed": false,
          "rendered": [
              "vlan 20",
              "name desktops",
              "vlan 30",
              "name servers",
              "vlan 40",
              "name printers",
              "vlan 50",
              "name DMZ"
          ]
      }
  }
  ok: [rtr2] => {
      "msg": {
          "ansible_facts": {
              "discovered_interpreter_python": "/usr/bin/python"
          },
          "changed": false,
          "failed": false,
          "rendered": [
              "vlan 20",
              "name desktops",
              "vlan 30",
              "name servers",
              "vlan 40",
              "name printers",
              "vlan 50",
              "name DMZ"
          ]
      }
  }

  PLAY RECAP *********************************************************************
  rtr2                       : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
  rtr4                       : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
  ```

* `rendered` キーでは、設定の生成に使用される Arista コマンドが表示されます!これにより、ネットワーク自動化担当者は、実際に自動化を実行してコマンドを適用する前に、どのコマンドが実行されるかを正確に知ることができます。

### ステップ 8 - parsed パラメーターの使用

最後に、`parsed` パラメーターについて説明します。このパラメーターは、既存のファイルにネットワークデバイスのコンフィグが含まれている場合に使用されます。すでにバックアップが実行されている場合を想像してください。

* まずコンフィグをバックアップします。コンフィグをバックアップするシンプルな Playbook はこちらです。 [backup.yml](backup.yml) 

{% raw %}
  ```yaml
  ---
  - name: backup config
    hosts: arista
    gather_facts: false

    tasks:

    - name: retrieve backup
      arista.eos.config:
        backup: true
        backup_options:
          filename: "{{ inventory_hostname }}.txt"
  ```
{% endraw %}

* Playbook を実行します。

  ```bash
  $ ansible-navigator run backup.yml --mode stdout
  ```

* バックアップファイルが生成されたことを確認します。

  ```bash
  $ ls backup
  rtr2.txt  rtr4.txt
  ```

* ここで、 `parsed` を使用するように Playbook `resource.yml` を変更します。

{% raw %}
  ```yaml
  ---
  - name: use parsed
    hosts: arista
    gather_facts: false

    tasks:

    - name: use vlans resource module
      arista.eos.vlans:
        state: parsed
        running_config: "{{ lookup('file', 'backup/{{ inventory_hostname }}.txt') }}"
      register: parsed_config

    - name: print to terminal screen
      debug:
        msg: "{{ parsed_config }}"
  ```
{% endraw %}

* いくつか追加の変更があります

  * `config` の代わりに `running-config` を利用してバックアップファイルを指定しています。
  * モジュールの実行結果を`parsed_config` 変数に登録しています。
  * debug モジュールを使用して `parsed_config` 変数を出力しています。

* Playbook を実行します。

    ```bash
    $ ansible-navigator run resource.yml --mode stdout
    ```

* 以下のように表示されます。

  ```yaml
  [student@ansible-1 network-workshop]$ ansible-navigator run resource.yml --mode stdout

  PLAY [use parsed] **************************************************************

  TASK [use vlans resource module] ***********************************************
  ok: [rtr4]
  ok: [rtr2]

  TASK [print to terminal screen] ************************************************
  ok: [rtr2] => {
      "msg": {
          "ansible_facts": {
              "discovered_interpreter_python": "/usr/bin/python"
          },
          "changed": false,
          "failed": false,
          "parsed": [
              {
                  "name": "desktops",
                  "state": "active",
                  "vlan_id": 20
              },
              {
                  "name": "servers",
                  "state": "active",
                  "vlan_id": 30
              },
              {
                  "name": "printers",
                  "state": "active",
                  "vlan_id": 40
              },
              {
                  "name": "DMZ",
                  "state": "active",
                  "vlan_id": 50
              }
          ]
      }
  }
  ok: [rtr4] => {
      "msg": {
          "ansible_facts": {
              "discovered_interpreter_python": "/usr/bin/python"
          },
          "changed": false,
          "failed": false,
          "parsed": [
              {
                  "name": "desktops",
                  "state": "active",
                  "vlan_id": 20
              },
              {
                  "name": "servers",
                  "state": "active",
                  "vlan_id": 30
              },
              {
                  "name": "printers",
                  "state": "active",
                  "vlan_id": 40
              },
              {
                  "name": "DMZ",
                  "state": "active",
                  "vlan_id": 50
              }
          ]
      }
  }

  PLAY RECAP *********************************************************************
  rtr2                       : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
  rtr4                       : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
  ```

* 上記の出力では、フラットファイル形式のバックアップが、構造化データにパースされていることがわかります。

  ```json
  "parsed": [
      {
          "name": "desktops",
          "state": "active",
          "vlan_id": 20
      }
  ```

* デフォルトの出力は JSON ですが、YAML に簡単に変換できます。

## 重要なこと

追加の設定用 `state` パラメーターについて扱いました:

  * `replaced` - 指定された VLAN を矯正
  * `overridden`- すべての VLAN を矯正

`merged` から `replaced` 、`overridden` へと移行することは、ネットワークチームが自動化により自信を深めるにつれて、自動化ジャーニーをたどります。

読み取り専用の `state` パラメーターについても扱いました。

  * `rendered` - 希望するコンフィギュレーションを生成するコマンドを表示しまK
  * `parsed` - フラットファイルの設定（バックアップなど）を構造化されたデータに変換（実機は変更せず）

これらにより、ネットワーク自動化ツールは、切断された環境などのシナリオでリソースモジュールを使用できます。ネットワークリソースモジュールは、異なるネットワークデバイス間で一貫したエクスペリエンスを提供します。

[ネットワークリソースモジュールのドキュメント](https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html)には、更に情報が掲載されています。

## ソリューション

完成した Ansible Playbook は、回答キーとしてここで提供されています。

-  [overridden.yml](overridden.yml)
-  [backup.yml](backup.yml)
-  [parsed.yml](parsed.yml)


## 完了

追加の演習を完了しました!


---
[追加の演習に戻る](../README.ja.md)

[Ansible Network Automation ワークショップに戻る](../../README.ja.md)
