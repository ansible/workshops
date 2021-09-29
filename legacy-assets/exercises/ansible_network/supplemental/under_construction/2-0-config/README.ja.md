# Exercise 2.0 - Routerのコンフィグを更新してみよう

Ansibleを用いて、ルータのコンフィグを更新することができます。
コンフィグファイルを機器へPushする方法や、コンフィグレーションを1列ごとにPushすることもできます。

#### Step 1

`router_configs.yml`という名前の新しいファイルを作成します(実行方法はお任せします。`vim` や `nano`がjumphostにはインストールされています。みなさんのラップトップにインストールされているエディタを用いて後ほどコピーをするなどの方法でも構いません)

```
[student1@ansible networking-workshop]$ vim router_configs.yml
```

以下の通りにplayを定義します。

``` yaml
---
- name: SNMP RO/RW STRING CONFIGURATION
  hosts: cisco
  gather_facts: no
  connection: network_cli
```

#### Step 2

全てのルータに、SNMP strings `ansible-public` と `ansible-private` の両方が存在するようにタスクを追加します。
このタスクには`ios_config`モジュールを利用します。

> Note: **ios_config** モジュールのヘルプについては、**ansible-doc ios_config** コマンドをCLIから実行するか、docs.ansible.comをチェックしましょう。
> いずれかのヘルプを確認すれば、モジュールの使用例から利用可能な全てのオプションを表示してくれるはずです。


``` yaml
---
- name: SNMP RO/RW STRING CONFIGURATION
  hosts: cisco
  gather_facts: no
  connection: network_cli

  tasks:

    - name: ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT
      ios_config:
        commands:
          - snmp-server community ansible-public RO
          - snmp-server community ansible-private RW
```

#### Step 3

playbookを実行します。

``` shell
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts router_configs.yml

PLAY [UPDATE THE SNMP RO/RW STRINGS] ********************************************************************

TASK [ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT] *************************************************
changed: [rtr4]
changed: [rtr1]
changed: [rtr3]
changed: [rtr2]

PLAY RECAP **********************************************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0   
rtr2                       : ok=1    changed=1    unreachable=0    failed=0   
rtr3                       : ok=1    changed=1    unreachable=0    failed=0   
rtr4                       : ok=1    changed=1    unreachable=0    failed=0   

```

必要に応じてルータへログインしてコンフィグがUpdateされたか確認してみましょう。

```
[student1@ansible networking-workshop]$ ssh rtr1

rtr1#show running-config
```
>このホストからの接続はユーザー名、パスワードが必要ありません。



#### Step 4

`ios_config`モジュールは冪等性(べきとうせい。常に同じ状態であろうとする性質)を有しています。
これの意味するところは、機器側のコンフィグに変更が必要な場合(差分が認められる場合)にのみ、Ansibleは変更をPushします。
冪等性を確認するために、playbookを再実行してみましょう。


``` shell
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts router_configs.yml

PLAY [UPDATE THE SNMP RO/RW STRINGS] ********************************************************************************************************************************************************

TASK [ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT] *************************************************************************************************************************************
ok: [rtr1]
ok: [rtr2]
ok: [rtr4]
ok: [rtr3]

PLAY RECAP **********************************************************************************************************************************************************************************
rtr1                       : ok=1    changed=0    unreachable=0    failed=0   
rtr2                       : ok=1    changed=0    unreachable=0    failed=0   
rtr3                       : ok=1    changed=0    unreachable=0    failed=0   
rtr4                       : ok=1    changed=0    unreachable=0    failed=0   

```

> Note: **PLAY RECAP** において、**changed** パラメータが0であることに注目してください。playが実行されたが変更は何もなかったことを示しています。


#### Step 5

もう一つ、SNMP RO ストリングを追加するタスクを追加してみましょう。


``` yaml
---
- name: UPDATE THE SNMP RO/RW STRINGS
  hosts: cisco
  gather_facts: no
  connection: network_cli

  tasks:

    - name: ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT
      ios_config:
        commands:
          - snmp-server community ansible-public RO
          - snmp-server community ansible-private RW
          - snmp-server community ansible-test RO
```


#### Step 6


今回は、プレイブックを実行して変更を機器にプッシュするのではなく、 `--check`フラグを使って実行します。
さらに、`-v`(またはverbose mode)フラグと組み合わせて詳細を見てみましょう。


``` shell
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts router_configs.yml --check -v
Using /home/student1/.ansible.cfg as config file

PLAY [UPDATE THE SNMP RO/RW STRINGS] ********************************************************************************************************************************************************

TASK [ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT] *************************************************************************************************************************************
changed: [rtr3] => {"banners": {}, "changed": true, "commands": ["snmp-server community ansible-test RO"], "updates": ["snmp-server community ansible-test RO"]}
changed: [rtr1] => {"banners": {}, "changed": true, "commands": ["snmp-server community ansible-test RO"], "updates": ["snmp-server community ansible-test RO"]}
changed: [rtr2] => {"banners": {}, "changed": true, "commands": ["snmp-server community ansible-test RO"], "updates": ["snmp-server community ansible-test RO"]}
changed: [rtr4] => {"banners": {}, "changed": true, "commands": ["snmp-server community ansible-test RO"], "updates": ["snmp-server community ansible-test RO"]}

PLAY RECAP **********************************************************************************************************************************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0   
rtr2                       : ok=1    changed=1    unreachable=0    failed=0   
rtr3                       : ok=1    changed=1    unreachable=0    failed=0   
rtr4                       : ok=1    changed=1    unreachable=0    failed=0   

```

この`--check`モードと`-v`オプションの組み合わせは、実際に変更を実施することはなく、実行対象になっている機器側での変更点のみを表示させています。
これは、実際には作業を実施する前に変更点のみを確認することができる非常に優れたテクニックです。

> いずれかの機器(複数でも構いません)へログインして、実際に変更が実施されたかどうかを確認してみてください。

この後のStep7でplaybook実行時に冪等性の意味が少しわかると思います。
ポイントとしては、作成されたplaybookの中では3つのコマンドが定義されていますが、まだ実行されていない(機器に設定されていない)コマンド1つだけが実行されるというところです。


#### Step 7

playbookを再実行します。
今度は`-v`や`--check`などのオプションは付けずに実行し、機器に対して変更をPushしましょう。

``` shell
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts router_configs.yml

PLAY [UPDATE THE SNMP RO/RW STRINGS] ********************************************************************************************************************************************************

TASK [ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT] *************************************************************************************************************************************
changed: [rtr1]
changed: [rtr2]
changed: [rtr4]
changed: [rtr3]

PLAY RECAP **********************************************************************************************************************************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0   
rtr2                       : ok=1    changed=1    unreachable=0    failed=0   
rtr3                       : ok=1    changed=1    unreachable=0    failed=0   
rtr4                       : ok=1    changed=1    unreachable=0    failed=0   

[student1@ansible networking-workshop]$
```


#### Step 8


個々のコンフィグの行における変更をPushするのではなく、コンフィグレーションの塊をデバイスに対してPushすることもできます。
playbookと同じディレクトリへ、`secure_router.cfg`というファイルと作成し、次の通りに追記しましょう。

```shell
[student1@ansible networking-workshop]$ vim secure_router.cfg
```

``` shell
line con 0
 exec-timeout 5 0
line vty 0 4
 exec-timeout 5 0
 transport input ssh
ip ssh time-out 60
ip ssh authentication-retries 5
service password-encryption
service tcp-keepalives-in
service tcp-keepalives-out
```


#### Step 9

playbookには、playのリストが含まれるということを忘れないでください。
`HARDEN IOS ROUTERS`という新しいplayを`router_configs.yml` playbookへ追加します。

``` yaml
---
- name: UPDATE THE SNMP RO/RW STRINGS
  hosts: cisco
  gather_facts: no
  connection: network_cli

  tasks:

    - name: ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT
      ios_config:
        commands:
          - snmp-server community ansible-public RO
          - snmp-server community ansible-private RW
          - snmp-server community ansible-test RO


- name: HARDEN IOS ROUTERS
  hosts: cisco
  gather_facts: no
  connection: network_cli

```

#### Step 10

**STEP 8**で作成した `secure_router.cfg`ファイルの設定をプッシュするために、新しいプレイにタスクを追加します。


``` yaml
---
- name: UPDATE THE SNMP RO/RW STRINGS
  hosts: cisco
  gather_facts: no
  connection: network_cli

  tasks:

    - name: ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT
      ios_config:
        commands:
          - snmp-server community ansible-public RO
          - snmp-server community ansible-private RW
          - snmp-server community ansible-test RO


- name: HARDEN IOS ROUTERS
  hosts: cisco
  gather_facts: no
  connection: network_cli

  tasks:

    - name: ENSURE THAT ROUTERS ARE SECURE
      ios_config:
        src: secure_router.cfg
```


#### Step 11

playbookを実行しましょう。

``` shell
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts router_configs.yml

PLAY [UPDATE THE SNMP RO/RW STRINGS] ********************************************************************************************************************************************************

TASK [ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT] *************************************************************************************************************************************
ok: [rtr3]
ok: [rtr2]
ok: [rtr1]
ok: [rtr4]

PLAY [HARDEN IOS ROUTERS] *******************************************************************************************************************************************************************

TASK [ENSURE THAT ROUTERS ARE SECURE] *******************************************************************************************************************************************************
changed: [rtr4]
changed: [rtr3]
changed: [rtr2]
changed: [rtr1]

PLAY RECAP **********************************************************************************************************************************************************************************
rtr1                       : ok=2    changed=1    unreachable=0    failed=0   
rtr2                       : ok=2    changed=1    unreachable=0    failed=0   
rtr3                       : ok=2    changed=1    unreachable=0    failed=0   
rtr4                       : ok=2    changed=1    unreachable=0    failed=0   

[student1@ansible networking-workshop]$

```

# Complete

お疲れ様でした。
以上でlab exercise 2.0 は終了です。

---
[ここをクリックすると Ansible Linklight - Networking Workshop へ戻ります](../../README.ja.md)
