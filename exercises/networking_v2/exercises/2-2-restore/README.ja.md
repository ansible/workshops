# Exercise 2.2 - バックアップしたコンフィグでRouterをリストアしてみよう

ここまでの演習で、4つのCiscoルータのコンフィグをバックアップする方法を学びました。
この演習では、どのようにリストアをするのか？を学習します。
バックアップファイルは、Anisbleノードの`backup`ディレクトリへ格納されています。

```
[student1@ansible networking-workshop]$ tree backup
backup
├── rtr1.config
├── rtr1_config.2018-06-07@20:36:05
├── rtr2.config
├── rtr2_config.2018-06-07@20:36:07
├── rtr3.config
├── rtr3_config.2018-06-07@20:36:04
├── rtr4.config
└── rtr4_config.2018-06-07@20:36:06
```


我々の目的は、"最後に動いていた状態のバックアップ"をルータへ適用するということです。


#### Step 1

いずれかのルータ(ここでは`rtr1`を例)の設定を、マニュアルで変更してみましょう。
ルータ上で、新しいloopback interfaceを設定します。

`ssh rtr1`コマンドを実行して`rtr1`へログインし、以下の通りにコンフィグを追加します。

```
rtr1#config terminal
Enter configuration commands, one per line.  End with CNTL/Z.
rtr1(config)#interface loopback 101
rtr1(config-if)#ip address 169.1.1.1 255.255.255.255
rtr1(config-if)#end
rtr1#

```

新しく作成されたloopback interfaceを確認してみましょう。

```
rtr1#sh run interface loopback 101
Building configuration...

Current configuration : 67 bytes
!
interface Loopback101
 ip address 169.1.1.1 255.255.255.255
end

rtr1#
```
#### Step 2

Step 1では、マニュアルオペレーションによって想定外の変更がNetwork機器上に発生したことをシミュレーションしました。
この変更はリバートされる必要があります。
そのためには、新しいplaybookを作成し、直前の演習で取得したバックアップを適用できるようにしましょう。

新しく`restore_config.yml`というファイルを作成し、新しいplayを以下のように定義します。

``` yaml
---
- name: RESTORE CONFIGURATION
  hosts: cisco
  connection: network_cli
  gather_facts: no

```


#### Step 3

以前にバックアップしたファイルをルータにコピーするタスクを記述します。

{%raw%}
``` yaml
---
- name: RESTORE CONFIGURATION
  hosts: cisco
  connection: network_cli
  gather_facts: no

  tasks:
    - name: COPY RUNNING CONFIG TO ROUTER
      command: scp ./backup/{{inventory_hostname}}.config  {{inventory_hostname}}:/{{inventory_hostname}}.config
```
{%endraw%}

> Note: **inventory_hostname**変数の利用方法に注意してください。
> インベントリーファイル内でciscoグループに定義されているそれぞれのデバイスへ、このタスクによって各デバイスのbootflash上へバックアップコンフィグが直接SCPでコピーされ渡されます。


#### Step 4

続いてplaybookを実行してみましょう。


```
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts restore_config.yml

PLAY [RESTORE CONFIGURATION] *********************************************************

TASK [COPY RUNNING CONFIG TO ROUTER] *************************************************
changed: [rtr1]
changed: [rtr2]
changed: [rtr3]
changed: [rtr4]

PLAY RECAP ***************************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0   
rtr2                       : ok=1    changed=1    unreachable=0    failed=0   
rtr3                       : ok=1    changed=1    unreachable=0    failed=0   
rtr4                       : ok=1    changed=1    unreachable=0    failed=0   

[student1@ansible networking-workshop]$

```


#### Step 5

ルータへログインして、ファイルがコピーされたことを確認してみましょう。

> Note bootflash:/ディレクトリの一番下に**rtr1.config**があるはずです。

```
[student1@ansible networking-workshop]$ ssh rtr1


rtr1#dir
Directory of bootflash:/

   11  drwx            16384  May 11 2018 21:30:28 +00:00  lost+found
   12  -rw-        380928984  May 11 2018 21:32:05 +00:00  csr1000v-mono-universalk9.16.08.01a.SPA.pkg
   13  -rw-         38305434  May 11 2018 21:32:06 +00:00  csr1000v-rpboot.16.08.01a.SPA.pkg
   14  -rw-             1967  May 11 2018 21:32:06 +00:00  packages.conf
235713  drwx             4096   Jun 4 2018 18:08:56 +00:00  .installer
186945  drwx             4096   Jun 4 2018 18:08:44 +00:00  core
   15  -rw-               58   Jun 4 2018 18:08:30 +00:00  iid_check.log
113793  drwx             4096   Jun 4 2018 18:08:32 +00:00  .prst_sync
73153  drwx             4096   Jun 4 2018 18:08:44 +00:00  .rollback_timer
81281  drwx             4096   Jun 7 2018 22:03:48 +00:00  tracelogs
227585  drwx             4096   Jun 4 2018 18:16:10 +00:00  .dbpersist
130049  drwx             4096   Jun 4 2018 18:09:41 +00:00  virtual-instance
   16  -rw-               30   Jun 4 2018 18:11:05 +00:00  throughput_monitor_params
   17  -rw-            10742   Jun 4 2018 18:16:08 +00:00  cvac.log
   18  -rw-               16   Jun 4 2018 18:11:14 +00:00  ovf-env.xml.md5
   19  -rw-               16   Jun 4 2018 18:11:14 +00:00  .cvac_skip_once
   20  -rw-              209   Jun 4 2018 18:11:15 +00:00  csrlxc-cfg.log
170689  drwx             4096   Jun 4 2018 18:11:16 +00:00  onep
373889  drwx             4096   Jun 8 2018 00:41:04 +00:00  syslog
   21  -rw-               34   Jun 4 2018 18:16:15 +00:00  pnp-tech-time
   22  -rw-            50509   Jun 4 2018 18:16:16 +00:00  pnp-tech-discovery-summary
341377  drwx             4096   Jun 4 2018 18:16:21 +00:00  iox
   23  -rw-           394307   Jun 8 2018 01:26:51 +00:00  rtr1.config

7897378816 bytes total (7073292288 bytes free)
rtr1#

```




#### Step 6

かつて動いていたはずのコンフィグが送付先のデバイス上にあることが確認できました。
新しいtaskをplaybookへ追加して、running-configをコピーしたものに入れ替えましょう。


{%raw%}
``` yaml
---
- name: RESTORE CONFIGURATION
  hosts: cisco
  connection: network_cli
  gather_facts: no

  tasks:
    - name: COPY RUNNING CONFIG TO ROUTER
      command: scp ./backup/{{inventory_hostname}}.config {{inventory_hostname}}:/{{inventory_hostname}}.config

    - name: CONFIG REPLACE
      ios_command:
        commands:
          - config replace flash:{{inventory_hostname}}.config force
```
{%endraw%}

> Note: Cisco機器が持っている**archive**機能を利用していることに注意してください。
> config replaceコマンドは全てのコンフィグの入れ替えを実施せず、差分のみを更新します。


#### Step 7

アップデートされたplaybookを実行してみましょう。

```

[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts restore_config.yml

PLAY [RESTORE CONFIGURATION] *********************************************************

TASK [COPY RUNNING CONFIG TO ROUTER] *************************************************
changed: [rtr1]
changed: [rtr3]
changed: [rtr2]
changed: [rtr4]

TASK [CONFIG REPLACE] ****************************************************************
ok: [rtr1]
ok: [rtr2]
ok: [rtr4]
ok: [rtr3]

PLAY RECAP ***************************************************************************
rtr1                       : ok=2    changed=1    unreachable=0    failed=0   
rtr2                       : ok=2    changed=1    unreachable=0    failed=0   
rtr3                       : ok=2    changed=1    unreachable=0    failed=0   
rtr4                       : ok=2    changed=1    unreachable=0    failed=0   

[student1@ansible networking-workshop]$


```


#### Step 8


我々がマニュアルオペレーションによるミスで**Step 1**にて追加してしまったインターフェースが存在していないことを確認してみてください。

```
[student1@ansible networking-workshop]$ ssh rtr1

rtr1#sh ip int br
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet1       172.16.165.205  YES DHCP   up                    up      
Loopback0              192.168.1.101   YES manual up                    up      
Loopback1              10.1.1.101      YES manual up                    up      
Tunnel0                10.100.100.1    YES manual up                    up      
Tunnel1                10.200.200.1    YES manual up                    up      
VirtualPortGroup0      192.168.35.101  YES TFTP   up                    up      

rtr1#sh run interface Loopback 101
                               ^
% Invalid input detected at '^' marker.

rtr1#

```

上記の出力結果は、Loopback 101 interfaceがもはや存在していないことを示しています。
あなたはCiscoルータのコンフィグのバックアップと、リストア作業の自動化に成功しました！

# Complete

お疲れ様でした。
以上でlab exercise 2.2 は終了です。

---
[ここをクリックすると Ansible Linklight - Networking Workshop へ戻ります](../../README.ja.md)
