# 演習 1.4 - ルータの追加設定

前の演習ではAnsibleの基本を見てきました。この演習ではさらにplaybookに柔軟性とパワフルさを追加してくれるAnsibleのコンセプトを紹介します。

## 目次
 - [紹介](#intro)
 - [セクション 1 - playbookに変数を使う](#section-1---using-variables-in-a-playbook)
 - [セクション 2 - rtr1のフロックを作成する](#section-2---create-a-block-for-rtr1)
 - [セクション 3 - rtr2を設定する](#section-3---configuring-rtr2)
 - [セクション 4 - レビュー](#section-4-review)

## 紹介

Ansibleはtaskをシンプルに、かつ繰り返し可能になっています。Ansible playbookを実行する際、全てのシステムが全く同じ状態ではなく、僅かな違いを合わせる必要があります。

- **変数** システム間の差異を変数で埋め、ポートやIPアドレス、そしてディレクトリの変更が出来るようにします。
- **ループ** ループを使えば同じtaskを何度でも繰り返すことができます。10のパッケージをインストールする場合などが分かりやすい例でしょう。 ループを用いれば、これを1つのtaskで行えます。
- **ブロック** taskの論理グループや、play内のエラーハンドリングにおいて利用します。ブロックレベルであるタスクを実行したい場合、データや指示をタスク共通でセットしたい場合に使いやすいです。

**jinja?** - jinja2 は Ansible に動的表現と変数へのアクセスを可能にします。

変数、ループ、ブロック、jinja2のすべてを把握するには、以下のAnsible Document内容を確認してください:
- [Ansible 変数](http://docs.ansible.com/ansible/playbooks_variables.html)
- [Ansible ループ](http://docs.ansible.com/ansible/playbooks_loops.html)
- [Ansible ブロック](http://docs.ansible.com/ansible/latest/playbooks_blocks.html)

## セクション 1 - plsybook内の変数の利用

まずは新しいrouter_configs.yml という名のplaybookを作成してみましょう。

新たなplaybookを作成するため、networking-workshopディレクトリに移動します。

```bash
cd ~/networking-workshop
vim router_configs.yml
```
4つの変数をセットします :
  - **ansible_network_os**: ネットワークOSタイプを決めるため、Minimum Viable Platform Agnostic (MVPA) モジュール (**_net** モジュール として知られています) を使用します
  - **dns_servers**: `rtr1` と `rtr2` 上に設定したい複数のDNSサーバのリスト
  - **host1_private_ip**: `host1` が使う プライベートアドレス 172.17.X.X
  - **control_private_ip**: `ansible` が使う プライベートアドレス 172.16.X.X

**host1** ノード と **ansible** ノード の private_ips を取得する必要があります:

 - IPアドレスは private_ip=x.x.x.x として右記ファイルに設定されます: `~/networking-workshop/lab_inventory/hosts`

変数は以下にあるように hostvars と呼ばれる変数に動的に呼び出されます。

{% raw %}
```yml
---
- name: Router Configurations
  hosts: routers
  gather_facts: no
  connection: local
  vars:
    ansible_network_os: ios
    dns_servers:
      - 8.8.8.8
      - 8.8.4.4
    host1_private_ip: "{{hostva‌rs['host1']['private_ip']}}"
    control_private_ip: "{{hostvars['ansible']['private_ip']}}"
```      
{% endraw %}

## セクション 2: Create a block for rtr1
ブロックを作成し、条件付きでrtr1 用の task を追加します。わかりやすい playbook にするためコメントを追加します。

{% raw %}
```
    ##Configuration for R1
    - block:
      - name: Static route from R1 to R2
        net_static_route:
          prefix: "{{host1_private_ip}}"
          mask: 255.255.255.255
          next_hop: 10.0.0.2
      - name: configure name servers
        net_system:
          name_servers: "{{item}}"
        with_items: "{{dns_servers}}"
      when:
        - '"rtr1" in inventory_hostname'
```
{% endraw %}

  - `vars:` この後に続いて記述されるものが変数名であることをAnsibleに伝えています
  - `dns_servers` dns_serversと命名したリスト型（list-type）の変数を定義しています。その後に続いているのは、DNSサーバのリストです
  - {% raw %}`{‌{ item }}`{% endraw %} この記述によって 8.8.8.8 や 8.8.4.4 といったリストのアイテムを展開するようAnsibleに伝えています。
  - {% raw %}`with_items: "{‌{ dns_servers }}`{% endraw %} これがループの本体で、Ansibleに対して `dns_servers` に含まれている全ての `item` に対してこのtaskを実行するよう伝えています。
  - `block:` このブロックは関連するいくつかのtaskを持ちます
  - `when:` when 節 はブロックと関連しています。特定の条件に合致する場合、ブロック内で全てのtaskを実行するようAnsibleに伝えます。

## セクション 3 - rtr2 の設定

このブロック内に4つのtaskがあります
- net_interface
- ios_config
- net_static_route
- net_system

{% raw %}
```yml
##Configuration for R2
- block:
  - name: enable GigabitEthernet1 interface if compliant
    net_interface:
      name: GigabitEthernet1
      description: interface to host1
      state: present
  - name: dhcp configuration for GigabitEthernet1
    ios_config:
      lines:
        - ip address dhcp
      parents: interface GigabitEthernet1
  - name: Static route from R2 to R1
    net_static_route:
      prefix: "{{control_private_ip}}"
      mask: 255.255.255.255
      next_hop: 10.0.0.1
  - name: configure name servers
    net_system:
      name_servers: "{{item}}"
    with_items: "{{dns_servers}}"
  when:
    - '"rtr2" in inventory_hostname'
```
{% endraw %}

**で、何が起こった?**
  - [net_interface](http://docs.ansible.com/ansible/latest/net_interface_module.html): このモジュールはインターフェースの状態 (up, admin down, など) を定義することができます。このケースでは GigabitEthernet1 は起動しており、かつ正しい記述であることを確かめています。
  - [ios_config](http://docs.ansible.com/ansible/latest/ios_config_module.html): 前のplaybookでこのmoduleは使用していました。2つのtask(ip addr + static route)は結合できますが、特定の状態に至った場合ににtaskを分解するほうが好ましい場合もあります。  
  - [net_system](https://docs.ansible.com/ansible/2.4/net_system_module.html): このモジュールは net_interface に似ており、ネットワーク装置のシステム属性を管理します。ルータに渡したい name_servers をフィードする際にこのモジュールをループと共に使用します。
  - [net_static_route](https://docs.ansible.com/ansible/2.4/net_static_route_module.html): このモジュールはネットワーク装置のスタティックIPのルートを管理するために利用します。

## セクション 4 - レビュー

playbook は完成ですが、まだ実行しないでください。次の演習で実行します。その前に、全てが意図した通りになっているかもう一度見直してみましょう。もしも間違っていれば修正してください。

# 完了
演習 1.4 は完了です。

# 答え
完成されたplaybookを見たい、または実行してみたい場合はこちら [演習 1.5!](../1.5-run_routing_configs)

 ---
[Click Here to return to the Ansible Linklight - Networking Workshop](../README.md)
