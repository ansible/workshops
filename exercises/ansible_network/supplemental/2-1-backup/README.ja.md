# Exercise 2.1 - Routerのコンフィグをバックアップしてみよう


このシナリオでは、Ciscoルータの設定をバックアップするためのプレイブックを作成します。 
その後の演習で、このバックアップされたコンフィグを利用してデバイスを正常な状態にリストアします。

> Note: おそらく、ほとんどすべてのNetworkチームにおいて、このようなDay 2 オペレーション手順が存在しているのではないでしょうか。
> この演習のコンテンツをほとんどそのまま再利用することで、みなさんの環境にも適用できるかもしれません。

#### Step 1

`backup.yml`という新しいファイルを作成し、以下と同じようにplayを定義してください。
(これまでの章と同じく好きなエディタを用いてください)

``` yaml
---
- name: BACKUP ROUTER CONFIGURATIONS
  hosts: cisco
  connection: network_cli
  gather_facts: no

```

#### Step 2

`ios_config`モジュールを用いて、新しいtaskを記述します。
このタスクは`cisco`グループと定義された全ての機器からバックアップを取得するという内容です。

`backup` パラメータは自動的に`backup`というディレクトリをplaybookと同一のフォルダに作成し、バックアップが実行されたタイムスタンプを付けてコンフィグレーションのバックアップを保存します。

> Note: **ansible-doc ios_config** コマンドを実行するか、**docs.ansible.com**を確認することで、モジュールの利用方法を確認できます。


``` yaml
---
- name: BACKUP ROUTER CONFIGURATIONS
  hosts: cisco
  connection: network_cli
  gather_facts: no

  tasks:
    - name: BACKUP THE CONFIG
      ios_config:
        backup: yes
      register: config_output
```

なぜ、このタスクの中で`config_output`という変数を定義しているのでしょうか？

**Step 5**にてそれが明らかになります。


#### Step 3

playbookを実行して、次に進みましょう。

``` shell
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts backup.yml

PLAY [BACKUP ROUTER CONFIGURATIONS] *********************************************************************************************************************************************************

TASK [BACKUP THE CONFIG] ********************************************************************************************************************************************************************
ok: [rtr1]
ok: [rtr3]
ok: [rtr4]
ok: [rtr2]

PLAY RECAP **********************************************************************************************************************************************************************************
rtr1                       : ok=1    changed=0    unreachable=0    failed=0   
rtr2                       : ok=1    changed=0    unreachable=0    failed=0   
rtr3                       : ok=1    changed=0    unreachable=0    failed=0   
rtr4                       : ok=1    changed=0    unreachable=0    failed=0   

[student1@ansible networking-workshop]$

```


#### Step 4

プレイブックは `backup`というディレクトリを作成しました。次にこのディレクトリの内容をリストします。


``` shell
[student1@ansible networking-workshop]$ ls -l backup
total 1544
-rw-rw-r--. 1 student1 student1 393514 Jun 19 12:45 rtr1_config.2018-06-19@12:45:36
-rw-rw-r--. 1 student1 student1 393513 Jun 19 12:45 rtr2_config.2018-06-19@12:45:38
-rw-rw-r--. 1 student1 student1 390584 Jun 19 12:45 rtr3_config.2018-06-19@12:45:37
-rw-rw-r--. 1 student1 student1 390586 Jun 19 12:45 rtr4_config.2018-06-19@12:45:37
[student1@ansible networking-workshop]$

```

任意のバックアップされたファイルをエディターなどで開いて、きちんとバックアップが取れているのかを検証してみてください。

#### Step 5

この先、バックアップしたコンフィグをリストア用途で用いるかもしれません。
バックアップしたファイルを機器名称でリネームしておきましょう。

**Step 2**において、タスクの出力結果を`config_output`という変数名称に取り込んでいました。
この変数には、バックアップしたファイルの名前が含まれています。

`copy`モジュールを用いて、このファイルのコピーを作成してみましょう。

``` yaml
---
- name: BACKUP ROUTER CONFIGURATIONS
  hosts: cisco
  connection: network_cli
  gather_facts: no

  tasks:
    - name: BACKUP THE CONFIG
      ios_config:
        backup: yes
      register: config_output

    - name: RENAME BACKUP
      copy:
        src: "{{config_output.backup_path}}"
        dest: "./backup/{{inventory_hostname}}.config"
```


#### Step 6

再度playbookを実行してみます。

``` shell
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts backup.yml

PLAY [BACKUP ROUTER CONFIGURATIONS] *********************************************************************************************************************************************************

TASK [BACKUP THE CONFIG] ********************************************************************************************************************************************************************
ok: [rtr3]
ok: [rtr4]
ok: [rtr2]
ok: [rtr1]

TASK [RENAME BACKUP] ************************************************************************************************************************************************************************
changed: [rtr1]
changed: [rtr4]
changed: [rtr2]
changed: [rtr3]

PLAY RECAP **********************************************************************************************************************************************************************************
rtr1                       : ok=2    changed=1    unreachable=0    failed=0   
rtr2                       : ok=2    changed=1    unreachable=0    failed=0   
rtr3                       : ok=2    changed=1    unreachable=0    failed=0   
rtr4                       : ok=2    changed=1    unreachable=0    failed=0   

[student1@ansible networking-workshop]$

```

#### Step 7

もう一度 `backup`ディレクトリの内容をリストしてみましょう。

``` shell
[student1@ansible networking-workshop]$ ls -l backup
total 3088
-rw-rw-r--. 1 student1 student1 393514 Jun 19 13:35 rtr1.config
-rw-rw-r--. 1 student1 student1 393514 Jun 19 13:35 rtr1_config.2018-06-19@13:35:14
-rw-rw-r--. 1 student1 student1 393513 Jun 19 13:35 rtr2.config
-rw-rw-r--. 1 student1 student1 393513 Jun 19 13:35 rtr2_config.2018-06-19@13:35:13
-rw-rw-r--. 1 student1 student1 390584 Jun 19 13:35 rtr3.config
-rw-rw-r--. 1 student1 student1 390584 Jun 19 13:35 rtr3_config.2018-06-19@13:35:12
-rw-rw-r--. 1 student1 student1 390586 Jun 19 13:35 rtr4.config
-rw-rw-r--. 1 student1 student1 390586 Jun 19 13:35 rtr4_config.2018-06-19@13:35:13
[student1@ansible networking-workshop]$

```

ディレクトリには別のバックアップされたコンフィグファイルがありますが、デバイスの名前のみが反映されたファイルがあるということに注意してください。


#### Step 8


取得したファイルの内容でそれぞれのデバイスを手動でリストアしようとすると、コンフィグにエラーが発生する行が2箇所あります。

``` shell
Building configuration...

Current configuration with default configurations exposed : 393416 bytes

```

これらの邪魔な行を避けてリストア可能なコンフィグとするためには、"クリーンナップ"を実行する必要があります。

Ansibleの`lineinfile` モジュールを利用して新しいタスクを作成することで、最初の行を削除することができます。

``` yaml
---
- name: BACKUP ROUTER CONFIGURATIONS
  hosts: cisco
  connection: network_cli
  gather_facts: no

  tasks:
    - name: BACKUP THE CONFIG
      ios_config:
        backup: yes
      register: config_output

    - name: RENAME BACKUP
      copy:
        src: "{{config_output.backup_path}}"
        dest: "./backup/{{inventory_hostname}}.config"

    - name: REMOVE NON CONFIG LINES
      lineinfile:
        path: "./backup/{{inventory_hostname}}.config"
        line: "Building configuration..."
        state: absent
```

> Note: モジュールのパラメータ **line** は、指定されたファイルにおいて"Building configuration ..."と一致している行があるかを検索し、`absent`(不在/欠けている)状態にします。


#### Step 9

playbookを実行する前に、もう一つタスクを追加し、２つ目の不要な行("Current configuration ...etc")を削除する必要があります。  
しかし、この行には可変データ(バイト数)があるので、先ほどのように`lineinfile`モジュールと`line`パラメータを用いることはできません。  
その代わりに、 `regexp`パラメータを使用して正規表現で照合し、ファイル内の行を削除します：


``` yaml
---
- name: BACKUP ROUTER CONFIGURATIONS
  hosts: cisco
  connection: network_cli
  gather_facts: no

  tasks:
    - name: BACKUP THE CONFIG
      ios_config:
        backup: yes
      register: config_output

    - name: RENAME BACKUP
      copy:
        src: "{{config_output.backup_path}}"
        dest: "./backup/{{inventory_hostname}}.config"

    - name: REMOVE NON CONFIG LINES
      lineinfile:
        path: "./backup/{{inventory_hostname}}.config"
        line: "Building configuration..."
        state: absent

    - name: REMOVE NON CONFIG LINES - REGEXP
      lineinfile:
        path: "./backup/{{inventory_hostname}}.config"
        regexp: 'Current configuration.*'
        state: absent
```


#### Step 10

では、playbookを実行してみましょう。


``` shell
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts backup.yml

PLAY [BACKUP ROUTER CONFIGURATIONS] *********************************************************************************************************************************************************

TASK [BACKUP THE CONFIG] ********************************************************************************************************************************************************************
ok: [rtr2]
ok: [rtr4]
ok: [rtr1]
ok: [rtr3]

TASK [RENAME BACKUP] ************************************************************************************************************************************************************************
changed: [rtr2]
changed: [rtr4]
changed: [rtr3]
changed: [rtr1]

TASK [REMOVE NON CONFIG LINES] **************************************************************************************************************************************************************
changed: [rtr4]
changed: [rtr1]
changed: [rtr2]
changed: [rtr3]

TASK [REMOVE NON CONFIG LINES - REGEXP] *****************************************************************************************************************************************************
changed: [rtr1]
changed: [rtr3]
changed: [rtr2]
changed: [rtr4]

PLAY RECAP **********************************************************************************************************************************************************************************
rtr1                       : ok=4    changed=3    unreachable=0    failed=0   
rtr2                       : ok=4    changed=3    unreachable=0    failed=0   
rtr3                       : ok=4    changed=3    unreachable=0    failed=0   
rtr4                       : ok=4    changed=3    unreachable=0    failed=0   

[student1@ansible networking-workshop]$

```


#### Step 11

エディタを利用してファイルの中を確認してみましょう。
先ほどまであった最初の2行が削除されているはずです。

``` shell
[student1@ansible networking-workshop]$ head -n 10 backup/rtr1.config

!
! Last configuration change at 14:25:42 UTC Tue Jun 19 2018 by ec2-user
!
version 16.8
downward-compatible-config 16.8
no service log backtrace
no service config
no service exec-callback
no service nagle

```

> Note: **head** というunixコマンドは引数で指定されたn行目までを表示します。

# Complete

お疲れ様でした。
以上でlab exercise 2.1 は終了です。

---
[ここをクリックすると Ansible Linklight - Networking Workshop へ戻ります](../../README.ja.md)
