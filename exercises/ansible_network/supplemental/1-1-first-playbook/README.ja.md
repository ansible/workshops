# Exercise 1.1 - 初めてのplaybookを書いてみよう

ここまでで、インベントリファイルとグループ/ホストの変数について把握ができたと思います。
このセクションでは、playbookの作成について説明をします。

> このセクションでは、playbookがどのような構造かを理解し、あなたが本番環境でplaybookを実行できるくらいの初歩的なベースラインを達成することを目指しています。

#### Step 1:

好みのエディターを利用して、 `gather_ios_data.yml` というファイルを作成して見ましょう。  
(`vim` と `nano` がコントロールホストでは利用可能です)

```
[student1@ansible networking-workshop]$ vim gather_ios_data.yml
```

>必要に応じてお好きなGUIエディターをラップトップなどで利用してください。

>Ansible playbookは **YAML** ファイル形式で作成します。
>YAML は構造化されたデータを表現するフォーマットであり、人が見ても読みやすい形式になります(JSONのフォーマットとは異なります)。


#### Step 2:

作成した `gather_ios_data.yml`へ、次の例を参考にplayを追加してみましょう。

>vimを利用している場合は、"i"を押して編集モードへ入ります。

``` yaml
---
- name: GATHER INFORMATION FROM ROUTERS
  hosts: cisco
  connection: network_cli
  gather_facts: no
```

- `---` このファイルが、YAMLファイルであることを示しています。
- `hosts: cisco` このplaybookを`cisco`グループに対して実行します。グループ名は先の演習で確認をしたインベントリーファイル内で定義されていました。
- `connection: network_cli` ネットワーク機器に対して実行するplaybookは`netowrk_cli`という接続プラグインを指定してあげる必要があります。

Ansibleは、`connection`で指定が可能な数種類のコネクションプラグインが用意されています。これにより、操作対象によって異なる接続方式が利用できます。
この`network_cli`プラグインはネットワーク機器専用に開発されたコネクションプラグインで、複数のタスク間で永続的なSSH接続が確保されるように構成されています。

この部分がいわゆるPlaybookのヘッダー部分に相当し`Play`部と呼ばれます。Playbookの動作全体に影響する項目をここに定義します。


#### Step 3

次に、最初の`task`を追加しましょう。
今回作成するタスクでは、`ios_facts`モジュールを使用して、(`cisco`グループに属する)各デバイスから情報を収集します。


``` yaml
---
- name: GATHER INFORMATION FROM ROUTERS
  hosts: cisco
  connection: network_cli
  gather_facts: no

  tasks:
    - name: GATHER ROUTER FACTS
      ios_facts:
```

>playは、タスクのリストになります。
>モジュールとは、タスクを実行するために事前に用意されているコードです。

このタスク部分に「自分のやりたいこと」を記述していきます。
自分のやりたいことは「モジュール」にパラメーターを与えて定義していきます。
モジュールは、「インフラ作業でよくある手順」を部品化したものです。ここでは`ios_facts`というモジュール（部品）をパラメーターなしで呼び出しています。


#### Step 4

エディタから実行ホストのCLIに戻り、playbookを実行して見ましょう。 
playbookの実行は以下のコマンドを参考にしてください。

>vimで編集した内容を保存してエディタを終了するには、`wq!`と入力しましょう。

```
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts gather_ios_data.yml

```

出力結果は以下のようになるはずです。

```
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts gather_ios_data.yml

PLAY [GATHER INFORMATION FROM ROUTERS] ******************************************************************

TASK [GATHER ROUTER FACTS] ******************************************************************************
ok: [rtr1]
ok: [rtr4]
ok: [rtr3]
ok: [rtr2]

PLAY RECAP **********************************************************************************************
rtr1                       : ok=1    changed=0    unreachable=0    failed=0   
rtr2                       : ok=1    changed=0    unreachable=0    failed=0   
rtr3                       : ok=1    changed=0    unreachable=0    failed=0   
rtr4                       : ok=1    changed=0    unreachable=0    failed=0   

[student1@ansible networking-workshop]$


```

#### Step 5

playは問題なく成功し、ルーター4台に対する操作が完了しました。
しかし、実行結果はどこに出力されているのでしょうか？
playbookを、`-v`オプションをつけてもう一度実行してみましょう。

> Note: Ansibleは、実行結果の出力ログの詳細度合いを段階的に設定できます。最大四つのv(verbose mode)を設定して実行することができます。`-vvvv`


```
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts gather_ios_data.yml -v
Using /home/student1/.ansible.cfg as config file

PLAY [GATHER INFORMATION FROM ROUTERS] ******************************************************************

TASK [GATHER ROUTER FACTS] ******************************************************************************
ok: [rtr3] => {"ansible_facts": {"ansible_net_all_ipv4_addresses": ["10.100.100.3", "192.168.3.103", "172.16.235.46", "192.168.35.101", "10.3.3.103"], "ansible_net_all_ipv6_addresses": [], "ansible_net_filesystems": ["bootflash:"], "ansible_net_gather_subset": ["hardware", "default", "interfaces"], "ansible_net_hostname": "rtr3", "ansible_net_image": "boot:packages.conf", "ansible_net_interfaces": {"GigabitEthernet1": {"bandwidth": 1000000, "description": null, "duplex": "Full", "ipv4": [{"address": "172.16.235.46", "subnet": "16"}], "lineprotocol": "up ", "macaddress": "0e93.7710.e63c", "mediatype": "Virtual", "mtu": 1500, "operstatus": "up", "type": "CSR vNIC"}, "Loopback0": {"bandwidth": 8000000, "description": null, "duplex": null, "ipv4": [{"address": "192.168.3.103", "subnet": "24"}], "lineprotocol": "up ", "macaddress": "192.168.3.103/24", "mediatype": null, "mtu": 1514, "operstatus": "up", "type": null}, "Loopback1": {"bandwidth": 8000000, "description": null, "duplex": null, "ipv4": [{"address": "10.3.3.103", "subnet": "24"}], "lineprotocol": "up ", "macaddress": "10.3.3.103/24", "mediatype": null, "mtu": 1514, "operstatus": "up", "type": null}, "Tunnel0": {"bandwidth": 100, "description": null, "duplex": null, "ipv4": [{"address": "10.100.100.3", "subnet": "24"}]

.
.
.
.
.
<output truncated for readability>
```

> Note: 出力結果には、keyとvelueのペアになった情報が含まれています。これらの出力されたkey-velueペアの情報は、以降のplaybook内のtaskで利用することができます。また、 **ansible_**で始まる全ての変数は、anisbleが定義している値であり、後続のplayの中で定義をしなくても自動的に利用な値であるということに注意してください。


#### Step 6

Ansibleは実行時にオプションをつけることで実行先を限定的(limit)にすることができます。

このオプションを実行するためには、インベントリーファイル内でデバイス名やグループ名などがあらかじめ定義されている必要があります。実行時には、`--limit`を付与します。

先ほど実行したタスクに、`rtr1`をつけてrtr1だけに実行してみましょう。次に、`rtr1` と `rtr3`を２つ同時に実行してみましょう。

```
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts gather_ios_data.yml -v --limit rtr1
```

```
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts gather_ios_data.yml -v --limit rtr1,rtr3
```


#### Step 7

playbookをverbose mode(-vオプション)で実行するのは、タスクからどのような出力があるかを検証するのに適していることをStep5で学んだ通りです。
playbook内で扱われている変数をコントロールするためには、`debug`モジュールを使ってみましょう。`debug`はパラメーターで指定された変数の値を出力するモジュールです。

この演習では、2つのタスクを作成します。ルータのOS Versionと、シリアルナンバーを表示させるタスクです。

```
[student1@ansible networking-workshop]$ vim gather_ios_data.yml
```

{%raw%}
``` yaml
---
- name: GATHER INFORMATION FROM ROUTERS
  hosts: cisco
  connection: network_cli
  gather_facts: no

  tasks:
    - name: GATHER ROUTER FACTS
      ios_facts:

    - name: DISPLAY VERSION
      debug:
        msg: "The IOS version is: {{ ansible_net_version }}"

    - name: DISPLAY SERIAL NUMBER
      debug:
        msg: "The serial number is:{{ ansible_net_serialnum }}"
```
{%endraw%}


#### Step 8

では、playbookを再実行してみましょう。今回の実行では`verbose`オプションは必要ありません。また、全てのホストに対して実行させます。

```
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts gather_ios_data.yml

PLAY [GATHER INFORMATION FROM ROUTERS] ******************************************************************

TASK [GATHER ROUTER FACTS] ******************************************************************************
ok: [rtr4]
ok: [rtr1]
ok: [rtr2]
ok: [rtr3]

TASK [DISPLAY VERSION] **********************************************************************************
ok: [rtr4] => {
    "msg": "The IOS version is: 16.08.01a"
}
ok: [rtr1] => {
    "msg": "The IOS version is: 16.08.01a"
}
ok: [rtr2] => {
    "msg": "The IOS version is: 16.08.01a"
}
ok: [rtr3] => {
    "msg": "The IOS version is: 16.08.01a"
}

TASK [DISPLAY SERIAL NUMBER] ****************************************************************************
ok: [rtr1] => {
    "msg": "The serial number is:96F0LYYKYUZ"
}
ok: [rtr4] => {
    "msg": "The serial number is:94KZZ28ZT1Y"
}
ok: [rtr2] => {
    "msg": "The serial number is:9VBX7BSSLGS"
}
ok: [rtr3] => {
    "msg": "The serial number is:9OLKU6JWXRP"
}

PLAY RECAP **********************************************************************************************
rtr1                       : ok=3    changed=0    unreachable=0    failed=0   
rtr2                       : ok=3    changed=0    unreachable=0    failed=0   
rtr3                       : ok=3    changed=0    unreachable=0    failed=0   
rtr4                       : ok=3    changed=0    unreachable=0    failed=0   

[student1@ansible networking-workshop]$

```


たった、20行以下の"code"で、ネットワーク機器のバージョンとシリアル番号の収集が自動化されてしまいました。
ここで記述したplaybookをあなたの職場の本番環境のネットワーク機器に対して実行したらどうなるでしょうか？
誰かが更新していないかもしれないパラメータシートから、なぜ記述が残っているかもわからないような、すでに存在しない機器の情報を時間をかけて探すようなことは二度と起こらないかもしれません。


# Complete

お疲れ様でした。
以上でlab exercise 1.1 は終了です。

---
[ここをクリックすると Ansible Linklight - Networking Workshop へ戻ります](../../README.ja.md)
