# 演習 1.5 - ロール(Role): Playbookを再利用可能にする

今までの演習でやったようにPlaybookを1つのファイルに書くことは可能ですが、だんだんとファイルを再利用したり内容を整理したくなってくると思います。

Ansible ロールがその方法です。ロールはPlaybookを部品に分解し、これらの部品を決められたディレクトリ構造に配置します。これは演習1.2で紹介した [ベストプラクティスガイド](http://docs.ansible.com/ansible/playbooks_best_practices.html) に詳しく説明されています。

ここでは、先ほど書いたPlaybookをRoleにリファクタリングします。さらに、Ansible Galaxyについて学びます。

それでは、どのように router_configs.yml をRoleに分解していくのか見てみましょう。

![Figure 1: playbook role directory structure](roles.png)

幸運にもこれらのディレクトリ全てを手で作る必要はありません。それは Ansible Galaxy がやってくれます。

## セクション 1 - Ansible Galaxy を使って新ロールを初期化

Ansible Galaxy はロールを見つけたり、ダウンロードしたり、共有したりするための無料のサイトです。また、今やろうとしているようにロールを作るのにとても便利です。 

### ステップ 1: このプロジェクト用にディレクトリを作る

```bash
$ mkdir ~/test
$ cd ~/test
```

### ステップ 2: rolesというディレクトリを作り、そこに cd する

```bash
$ mkdir roles
$ cd roles
```

### ステップ 3: ansible-galaxy コマンドを使って system, interface, static_route という新ロールを初期化する

```bash
$ ansible-galaxy init system
$ ansible-galaxy init interface
$ ansible-galaxy init static_route

$ tree
.
├── interface
│   ├── defaults
│   │   └── main.yml
│   ├── files
│   ├── handlers
│   │   └── main.yml
│   ├── meta
│   │   └── main.yml
│   ├── README.md
│   ├── tasks
│   │   └── main.yml
│   ├── templates
│   ├── tests
│   │   ├── inventory
│   │   └── test.yml
│   └── vars
│       └── main.yml
├── static_route
│   ├── defaults
│   │   └── main.yml
...
```

### ステップ 4: tests ディレクトリ以下のファイルを削除する

```bash
$ cd ~/test/roles/
$ rm -rf roles/{system,interface,static_route}/{files,tests}
```

## セクション 2: router_configs.yml playbook を新しく作った system ロールに分解する

このセクションでは `vars:` や `tasks:` といったPlaybookの主要部分を分離していきます。

### deploy_network.yml を作ります。

deploy_network.yml を新規に作成します。

```bash
$ cd ~/test
$ vim deploy_network.yml
```

### ステップ 2: play の定義を追加します

```yml
---
- name: Deploy the Router configurations
  hosts: routers
  connection: network_cli
  gather_facts: no
  roles:
    - system
```

### ステップ 3: `roles/system/vars/main.yml` に変数を追加します

```yml
---
dns_servers:
  - 8.8.8.8
  - 8.8.4.4
```

### ステップ 4: `group_vars/all.yml` にグローバル変数を追加します

```bash
$ cd ~/test
$ mkdir group_vars
$ vim group_vars/all.yml
```

```yml
---
ansible_network_os: ios
ansible_connection: local
host1_private_ip: "172.18.2.125"
control_private_ip: "172.17.1.157"
ios_version: "16.09.01"
```  
host1_private_ip と control_private_ip を lab_inventory から転記します。

**Variables in multiple places?**
変数は限られた場所でのみ使用できます:
 - vars ディレクトリ
 - defaults ディレクトリ
 - group_vars ディレクトリ
 - playbook の `vars:` セクション下
 - どのファイルでもコマンドラインの `--extra_vars` -  オプションで指定できます

どこで変数を定義するか、どの場所が優先されるかについての情報は [変数の優先について](http://docs.ansible.com/ansible/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable) を参照してください。この演習ではいくつかの変数の定義にdefaultsを使用していますが、これは最も上書きされやすい場所です。その他に `/vars` にもいくつかの変数を定義していますが、こちらはdefaultsより高い優先度もっているのでデフォルト値に上書きされる事はありません。

### ステップ 6: `roles/system/tasks/main.yml` にタスクを追加

```yml
---
- name: gather ios_facts
  ios_facts:

- name: configure name servers
  ios_system:
    name_servers: "{{item}}"
  with_items: "{{dns_servers}}"
```        

### ステップ 7: もう2つのロールを編集します: 一つ目は interface 、そして2つ目は static_route です

For `roles/interface/tasks/main.yml`:

```yml
- block:
  - name: enable GigabitEthernet1 interface if compliant on r2
    ios_interface:
      name: GigabitEthernet1
      description: interface to host1
      state: present

  - name: dhcp configuration for GigabitEthernet1
    ios_config:
      lines:
        - ip address dhcp
      parents: interface GigabitEthernet1
  when:
    - ansible_net_version == ios_version
    - '"rtr2" in inventory_hostname'
```

For `roles/static_route/tasks/main.yml`:
```yml
##Configuration for R1
- name: Static route from R1 to R2
  ios_static_route:
    prefix: "{{host1_private_ip}}"
    mask: 255.255.255.255
    next_hop: 10.0.0.2
  when:
    - ansible_net_version == ios_version
    - '"rtr1" in inventory_hostname'

##Configuration for R2
- name: Static route from R2 to R1
  ios_static_route:
    prefix: "{{control_private_ip}}"
    mask: 255.255.255.255
    next_hop: 10.0.0.1
  when:
    - ansible_net_version == ios_version
    - '"rtr2" in inventory_hostname'
```

### ステップ 8: ロールをマスターplaybookである `deploy_network.yml` に追加します

```yml
---
- name: Deploy the Router configurations
  hosts: routers
  gather_facts: no
  roles:
    - system
    - interface
    - static_route
```

## セクション 3: ロールベースのPlaybookを実行する
元のPlaybookは無事にRoleに分解されました。さっそく実行してみてましょう。

### ステップ 1: playbookの実行

```bash
$ ansible-playbook deploy_network.yml
```

## セクション 3: レビュー

3つのロール、すなわち system、interface、static_route からなる deploy_network.yml ができました。Playbookをロールに構造化することの強みは、Ansible Galaxyを使ってPlaybookに新しいロールを追加できることです。もちろん自分自身でロールを作ることもできます。更に、ロールは変数、タスク、テンプレート等の変更をシンプルにします。

## Answer Key
ファイルが複数あるので [このGitHubを参照する](https://github.com/network-automation/linklight/tree/master/exercises/networking/1.5-roles) のがベストです。

 ---
[Ansible Linklight - ネット-ワークワークショップ に戻る](../README.ja.md)
