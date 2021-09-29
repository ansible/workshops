# Exercise 3.0 - Jinja2 によるテンプレート処理のご紹介

一般的に言えば、ネットワーク自動化について言及する時、具体的にはネットワーク装置の構成管理にフォーカスされがちです。
このラボでは Ansible を活用して現状確認と動的なドキュメント生成を行う方法についても学習していきます。

これにより同じ情報を使用してレポートやドキュメントを作成することが可能となり、キーボードが好きなネットワークエンジニアのニーズに答えることが出来ます。そしてネットワークエンジニアが作ったネットワークの状態に対するレポートを、マネージャー層が理解する必要がある場合においてもWebページであれば一目瞭然です。

Python で使われている [Jinja2](http://jinja.pocoo.org/docs/2.10/) は、とてもパワフルなテンプレートエンジンです。Ansible では Jinja2 のネイティブ実装を採用しています。Jinja2 を使うことで変数の操作や、論理構造の実装が可能になります。Ansible の `template` モジュールと組み合わせることで、自動化に取り組むエンジニアが動的なレポート生成する場合において強力なツールとなることでしょう。

このラボでは、`template` モジュールを使ってネットワーク装置から収集したデータを Jinja2 テンプレートと一緒に処理する方法を学習していきます。`template` モジュールを使って Markdown ファイルとして出力します。

#### Step 1

まず最初に `router_report.yml` というファイル名の新しい Playbook を作っていきましょう。最初に次の内容を Playbook に記述してください。

{% raw %}
``` yaml
---
- name: GENERATE OS REPORT FROM ROUTERS
  hosts: cisco
  connection: network_cli
  gather_facts: no
```
{% endraw %}


#### Step 2

`ios_facts` モジュールを使って facts を収集するタスクを追加します。これまでのラボで、このモジュールを使用した演習を思い出してください。

{% raw %}
``` yaml
---
- name: GENERATE OS REPORT FROM ROUTERS
  hosts: cisco
  connection: network_cli
  gather_facts: no

  tasks:
    - name: GATHER ROUTER FACTS
      ios_facts:

```
{% endraw %}

> **facts** モジュールは実行時に **ansible_net_version** と **ansible_net_serial_number** の変数を自動的に設定する事を思い出してください。これを検証するには `-v` オプションを付けて verbose モードで Playbook を実行してください。

#### Step 3

ここでは debug モジュールか verbose モードで出力結果を画面で見るのではなく、次のように template モジュールを使って新しいタスクを追加していきます。

{% raw %}
``` yaml
---
- name: GENERATE OS REPORT FROM ROUTERS
  hosts: cisco
  connection: network_cli
  gather_facts: no

  tasks:
    - name: GATHER ROUTER FACTS
      ios_facts:

    - name: ENSURE REPORTS FOLDER
      run_once: true
      file:
        name: reports
        state: directory

    - name: RENDER FACTS AS A REPORT
      template:
        src: os_report.j2
        dest: reports/{{ inventory_hostname }}.md

```
{% endraw %}

ここで少しタスクを詳しく解説していきましょう。`template` モジュールには `os_report.j2` の値を持つ `src` パラメーターがあります。次からのステップでは、このファイルを Jinja2 テンプレート形式で作っていきます。`dest` パラメーターで指定した任意のファイル名でレポートファイルを生成します。


#### Step 4

次のステップでは Jinja2 テンプレートを作っていきましょう。Ansible はカレントの作業ディレクトリの中に `templates` ディレクトリがあるかを自動的に探します。ベストプラクティスとしては `templates` ディレクトリにテンプレートファイルを作成することです。

`vi` や `nano`、もしくはお好みのテキストエディターを使って `templates` の中にある `os_report.j2` を作成してください。ファイルの内容としては次のとおりです。

```shell
[student1@ansible networking-workshop]$ vim templates/os_report.j2
```

{% raw %}
``` python
{{ inventory_hostname.upper() }}
---
{{ ansible_net_serialnum }} : {{ ansible_net_version }}
```
{% endraw %}

このファイルには、今までの演習の Playbook で使用した変数が含まれています。

> 注記: データ型のための Python 組み込みのメソッドは、Jinja2 からネイティブに使用できます。これにより書式設定などの操作が非常に簡単になります。


#### Step 5

では、Playbook を実行してみましょう。

``` shell
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts router_report.yml

PLAY [GENERATE OS REPORT FROM ROUTERS] ******************************************************************************************************************************************************

TASK [GATHER ROUTER FACTS] ******************************************************************************************************************************************************************
ok: [rtr4]
ok: [rtr3]
ok: [rtr2]
ok: [rtr1]

TASK [ENSURE REPORTS FOLDER] ********************************************************************************
changed: [rtr1]

TASK [RENDER FACTS AS A REPORT] *************************************************************************************************************************************************************
changed: [rtr4]
changed: [rtr2]
changed: [rtr3]
changed: [rtr1]

PLAY RECAP **********************************************************************************************************************************************************************************
rtr1                       : ok=2    changed=1    unreachable=0    failed=0   
rtr2                       : ok=2    changed=1    unreachable=0    failed=0   
rtr3                       : ok=2    changed=1    unreachable=0    failed=0   
rtr4                       : ok=2    changed=1    unreachable=0    failed=0   

[student1@ansible networking-workshop]$
```


#### Step 6

Playbook を実行した後、reports ディレクトリに次のファイルが生成されます。

``` shell
[student1@ansible networking-workshop]$ tree reports
reports/
├── rtr1.md
├── rtr2.md
├── rtr3.md
└── rtr4.md

0 directories, 4 files
```

例として、1つレポートの中身を確認してみましょう。

``` shell
[student1@ansible networking-workshop]$ cat reports/rtr4.md


RTR4
---
9TCM27U9TQG : 16.08.01a

[student1@ansible networking-workshop]$
```


#### Step 7

データが取れたことは良いことですが、これらの個々のルーターレポートを1つのレポートに結合する方が良いでしょう。それを行うための新しいタスクを追記していきます。

{% raw %}
``` yaml
---
- name: GENERATE OS REPORT FROM ROUTERS
  hosts: cisco
  connection: network_cli
  gather_facts: no

  tasks:
    - name: GATHER ROUTER FACTS
      ios_facts:

    - name: ENSURE REPORTS FOLDER
      run_once: true
      file:
        name: reports
        state: directory

    - name: RENDER FACTS AS A REPORT
      template:
        src: os_report.j2
        dest: reports/{{ inventory_hostname }}.md

    - name: CONSOLIDATE THE IOS DATA
      assemble:
        src: reports/
        dest: network_os_report.md
      delegate_to: localhost
      run_once: yes

```
{% endraw %}

ここでは `assemble` モジュールを使います。`src` パラメーターで結合するファイルを含むディレクトリを指定し、`dest` パラメーターで生成する先のファイルを指定します。

> 注記: **delegate_to** を使用して、ローカルで実行する必要のあるタスクを指定できます。**run_once** の指示により与えられたタスクが一度だけ実行されることを保証します。

#### Step 8

それでは Playbook を実行してみましょう。

``` shell
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts router_report.yml

PLAY [GENERATE OS REPORT FROM ROUTERS] **********************************************************************

TASK [GATHER ROUTER FACTS] **********************************************************************************
ok: [rtr4]
ok: [rtr3]
ok: [rtr1]
ok: [rtr2]

TASK [ENSURE REPORTS FOLDER] ********************************************************************************
changed: [rtr1]

TASK [RENDER FACTS AS A REPORT] *****************************************************************************
changed: [rtr2]
changed: [rtr1]
changed: [rtr4]
changed: [rtr3]

TASK [CONSOLIDATE THE IOS DATA] *****************************************************************************
changed: [rtr1 -> localhost]

PLAY RECAP **************************************************************************************************
rtr1                       : ok=4    changed=3    unreachable=0    failed=0   
rtr2                       : ok=2    changed=1    unreachable=0    failed=0   
rtr3                       : ok=2    changed=1    unreachable=0    failed=0   
rtr4                       : ok=2    changed=1    unreachable=0    failed=0   

[student1@ansible networking-workshop]$
```

#### Step 9

`network_os_report.md` という新しいファイルが作られました。Playbook が格納されているディレクトリのルートに作られます。中身を確認してみましょう。

``` shell
[student1@ansible networking-workshop]$ cat network_os_report.md

RTR1
---
9YJXS2VD3Q7 : 16.08.01a

RTR2
---
9QHUCH0VZI9 : 16.08.01a

RTR3
---
9ZGJ5B1DL14 : 16.08.01a

RTR4
---
9TCM27U9TQG : 16.08.01a

```

> 注記: Markdown ファイルは HTML のように整形して表示することが可能です

ここでポイントです。3つの小さなタスクによって、あなたが管理するネットワーク上の IOS を搭載するすべての装置からレポートを得ることができました。これは簡単な例ですが、他に何か拡張する際の原則は変わりません。たとえば、デバイスの `show` コマンドの出力に依存する状態レポートやダッシュボードを作成することができます。

この演習で体感頂いたように、Ansibleは、構成管理以外のネットワーク自動化はもちろんのこと、ドキュメントやレポートの生成などに用途を拡張するためのツールと手法も提供します。

# Complete

ラボの Exercise 3.0 が完了しました。

---
[Ansible Linklight - Networking Workshop に戻るにはクリックしてください](../../README.ja.md)
