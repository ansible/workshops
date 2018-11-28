# 演習 1.2 - コンフィグのバックアップ

最初のAnsible **playbook** を書いていきます。playbookは演習 1.1 で先程実行した複数の ad-hoc コマンドを、*plays* と *tasks* の複数セットに置き換えたものです。

playbookは1つまたは複数のplayに、1つまたは複数のタスクを持つことができます。*play* の目的はホストのグループをマッピングする事であり、*task* の目的はこれらのホストに対してモジュールを実行する事です。

## 目次
- [環境の調査](#環境の調査)
- [Playbook - backup.yml](#playbook---backupyml)
- [Answer Key](#answer-key)


## 環境の調査
playbook実行の前に、まずは確認してみましょう。
  - ansible.cfg - Ansible設定ファイル
  - inventory - ホストとグループの定義

### ステップ 1: networking_workshop ディレクトリへの移動

```bash
cd ~/networking-workshop
```

### ステップ 2: Ansible設定ファイルを見る

`ansible` コマンドを`--version` を加え実行し、設定内容を確認します:
```bash
[lcage@ip-172-16-74-150 ~]$ ansible --version
ansible 2.4.1.0
  config file = /home/lcage/.ansible.cfg
  configured module search path = [u'/home/lcage/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /usr/bin/ansible
  python version = 2.7.5 (default, Oct 11 2015, 17:47:16) [GCC 4.8.3 20140911 (Red Hat 4.8.3-9)]
```
出力結果に[ansible.cfg ファイル](http://docs.ansible.com/ansible/latest/intro_configuration.html) の保管場所を確認します。`cat` コマンドで ansible.cfg ファイルの設定パラメータを見てみましょう:
```bash
[lcage@ip-172-16-74-150 ~]$ cat ~/.ansible.cfg
[defaults]
connection = smart
timeout = 60
inventory = /home/lcage/networking-workshop/lab_inventory/hosts
host_key_checking = False
private_key_file = ~/.ssh/aws-private.pem
```
2つの最も重要なパラメータは以下です:
 - `inventory`: Ansible が利用するインベントリの保管場所を表しています
 - `private_key_file`: デバイスにログインする際使用する private key の保管場所を表しています

### ステップ 3: インベントリを理解する
[インベントリ](http://docs.ansible.com/ansible/latest/intro_inventory.html) はplaybookの実行対象となるリモートマシンを定義するものです。`cat` コマンドでインベントリファイルを見てみましょう:

```bash
cat ~/networking-workshop/lab_inventory/hosts
```

3つのグループ存在します:
 - `[control]` - 現在sshで入っている `ansible` ノード
 - `[cisco]` - `rtr1` と `rtr2` の2つのルーター。これは`[routers]からの入れ子(children)になっています。`
 - `[hosts]` - `rtr2` に接続している Linuxホスト `host1`

ホストの一つを分析してみましょう:
```bash
rtr1 ansible_host=54.174.116.49 ansible_ssh_user=ec2-user private_ip=172.16.3.183 ansible_network_os=ios
```
 - `rtr1` - Ansible が使用する名前です。名前をDNSに合わせることが必須ではありません。
 - `ansible_host` - Ansible が使用する IPアドレスです。定義されていない場合、デフォルトでDNSを使用します。
 - `ansible_ssh_user` - Ansibleがホストにログインする際のユーザIDです。定義されていない場合、デフォルトでplaybookを実行する際のユーザIDを使用します。
 - `private_ip` - プライベートIPを指定します。デフォルト設定は[ホスト変数](http://docs.ansible.com/ansible/latest/intro_inventory.html#host-variables) となります。変数は playbook より呼び出されるか、または上書きされるかします。
 - `ansible_network_os` - Ansible が接続する際のネットワークOSの種別を指定します。


## Playbook - backup.yml
Cisco IOS 定義バックアップ用のplaybook

**学べること:**
 - ios_facts モジュール
 - register keyword
 - debug モジュール
 - ios_config モジュールの backup パラメータ

 ---

### ステップ 1: Playの定義

では1つ目のplaybook backup.yml を作成しましょう。

```bash
vim backup.yml
```

playの定義から始め、各行が何をしているのかを理解しましょう。

```yml
---
- name: backup router configurations
  hosts: routers
  connection: network_cli
  gather_facts: no
```  

 - `---` YAML開始の定義
 - `hosts:` routers は、playを実行する対象のホスト・グループをInventoryの中で定義しています。
 - `name:` backup router configurations Play は、内容の説明です。
 - `gather_facts: no` setupモジュールで情報を呼び出す必要がないことをAnsibleに伝えます。 setupモジュールはコンピューティングノード(Linux, Windows)をターゲットにする場合に有用ですが、ネットワーク装置をターゲットとする場合はあまり有用ではありません。ターゲットのノードタイプによって、必要な platform_facts モジュールを使いましょう。
 - `connection: network_cli` Ansibleに python モジュールを (Pythonが実行できないターゲットノード) 直接実行するよう伝えます。

###  ステップ 2: Play に Task を追加する

ここまででplayを定義しました。続けてルータのバックアップに必要なtaskを追加しましょう。

この記述の仕方がとても重要です。Playbook内の記述は、すべてここで示されている形式に倣う必要があります。
もしもこのPlaybookの全文を見たい場合は、この演習ページのセクション4を参照してください。

{% raw %}
```bash
  tasks:
    - name: gather ios_facts
      ios_facts:
      register: version

    - debug:
        msg: "{{version}}"

    - name: Backup configuration
      ios_config:
        backup: yes
```
{% endraw %}      

 - `tasks:` 1つまたは複数のtask定義がされることを示す
 - `name:` playbookの実行時に標準出力されるそれぞれのtask名称です。出力されるに完結かつ、適切なtask名を記入してください。

 次のセクションでは IOS関連のFactを集めるため、Ansible ios_facts モジュールを使います。ios_facts モジュールを知りたい場合は[こちらをクリック](http://docs.ansible.com/ansible/latest/ios_facts_module.html)。現在 Fact は有効になっており、次に続く Task で必要に応じて利用することができます。次に debug の行を追加し、何が利用可能かを確認するために、実際に ios_facts モジュールで収集した情報を表示します。

{% raw %}
 ```bash
    - name: gather ios_facts
      ios_facts:
      register: version

    - debug:
        msg: "{{version}}"
```
{% endraw %}

次の3行は Ansible ios_config モジュールを呼び出し、ルータの設定情報を収集してバックアップファイルを生成するため backup: yes パラメータを渡しています。ios_config モジュールのオプション詳細を参照したい場合は [こちらをクリック](http://docs.ansible.com/ansible/latest/modules/ios_config_module.html)

```bash
    - name: Backup configuration
      ios_config:
        backup: yes
```

### ステップ 3: レビュー

playbookを書き終えたら、保存しましょう。`vi` または `vim`にて、`write/quit` を使用(例: Escキー押下後、wq!実行)し、playbookを保存します。

[Yaml](http://yaml.org/) はインデントやスペースの形式が少し特殊かもしれません。スペースやアラインメントをご確認いただくことをお勧めいたします:

{% raw %}
```
---
- name: backup router configurations
  hosts: routers
  connection: network_cli
  gather_facts: no

  tasks:
    - name: gather ios_facts
      ios_facts:
      register: version

    - debug:
        msg: "{‌{version}}"

    - name: Backup configuration
      ios_config:
        backup: yes
```       
{% endraw %}

### ステップ 4: playbook を実行する

**ansible-playbook** コマンドでplaybook を実行します。

```bash
ansible-playbook backup.yml
```
標準出力結果では、以下のような情報が確認できます。
![図 2: backup playbook の 標準出力結果](playbook-output.png)

#### Ansible Tip
 リモートシステムへの実行の前に、playbook のシンタックスチェックを試してみたいですよね?

 もし、playbookが問題なく適切に実行されるか確認したい場合は、以下のように `--syntax-check` を使って見てください。
 ```bash
 ansible-playbook backup.yml --syntax-check
 ```

### ステップ 5: バックアップディレクトリ内のファイル一覧
バックアップディレクトリをリストし、作成されたバックアップファイルを見ることができます。

```bash
ls backup
```

バックアップ設定ファイルの中身を見ることができます:
```bash
less backup/rtr1*
```
or

```bash
less backup/rtr2*
```

 ---
[Click Here to return to the Ansible Linklight - Networking Workshop](../README.ja.md)
