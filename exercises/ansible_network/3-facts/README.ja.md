# 演習 3: Ansible ファクト

**他の言語でもお読みいただけます**: ![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English](README.md)、![japan](https://github.com/ansible/workshops/raw/devel/images/japan.png) [日本語](README.ja.md), ![Español](https://github.com/ansible/workshops/raw/devel/images/es.png) [Español](README.es.md)


## 目次

* [目的](#objective)
* [ガイド](#guide)
   * [ステップ 1 - ドキュメントの使用](#step-1---using-documentation)
   * [ステップ 2 - プレイの作成](#step-2---creating-the-play)
   * [ステップ 3 - ファクトタスクの作成](#step-3---create-the-facts-task)
   * [ステップ 4 - Playbook の実行](#step-4---executing-the-playbook)
   * [ステップ 5 - デバッグモジュールの使用](#step-5---using-debug-module)
   * [ステップ 6 - stdout の使用](#step-6---using-stdout)
* [重要なこと](#takeaways)
* [ソリューション](#solution)
* [完了](#complete)

## 目的

ネットワークインフラストラクチャでの Ansible ファクトのデモンストレーション使用。

Ansible ファクトは、リモートネットワーク要素との会話から得られた情報です。Ansible ファクトは構造化データ (JSON)
で返されるため、操作や変更が簡単になります。たとえば、ネットワークエンジニアは、Ansible
ファクトを使用して監査レポートを非常に迅速に作成し、それらをマークダウンまたは HTML ファイルにテンプレート化できます。

この演習では、以下について説明します。

* Ansible Playbook のゼロからの作成。
* ドキュメントへの `ansible-navigator :doc` の使用
* [cisco.ios.facts
  モジュール](https://docs.ansible.com/ansible/latest/collections/cisco/ios/ios_facts_module.html)
  の使用。
* [デバッグモジュール](https://docs.ansible.com/ansible/latest/modules/debug_module.html)
  の使用。

## ガイド

### ステップ 1 - ドキュメントの使用

端末で `ansible-navigator` インタラクティブモードに入ります

```bash
$ ansible-navigator
```

`ansible-navigator` のスクリーンショット: ![ansible-navigator interactive
mode](images/ansible-navigator-interactive.png)

上記のスクリーンショットでは、モジュールまたはプラグインドキュメントの行を確認できます。
 
```
`:doc <plugin>`                 Review documentation for a module or plugin
 ```

`:doc debug` と入力して `debug` モジュールを検証しましょう。

```bash
:doc debug
```

`ansible-navigator :doc debug` のスクリーンショット: ![ansible-navigator interactive
mode doc](images/ansible-navigator-doc.png)

`debug`
モジュールのドキュメントが対話式ターミナルセッションに表示されました。これは、[docs.ansible.com](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/debug_module.html).
で表示されるまったく同じドキュメントの YAML 表現です。例は、モジュールのドキュメントから Ansible Playbook
に直接カットアンドペーストできます。

ビルドされていないモジュールを参照する場合、以下の 3 つの重要なフィールドがあります。

```
namespace.collection.module
```
例:
```
cisco.ios.facts
```

用語の説明: 
- **namespace** (例: **cisco**) - namespaceは複数のコレクションをグループ化します。**cisco** namespace には、**ios**、**nxos**、**iosxr**を含む複数のコレクションが含まれます。 
- **collection** (例: **ios**) - collectionは、Playbook、ロール、モジュール、プラグインを含む Ansible コンテンツのディストリビューション形式です。**ios**コレクションは、Cisco IOS/IOS-XE の全モジュールが含まれます。 
- **module** (例: facts) - モジュールは、Playbook タスクで使用できるコードの分散ユニットです。たとえば、**facts**モジュールは、指定されたそのシステムに関する構造化データを返します。

**Esc** キーを押してメインメニューに戻ります。`cisco.ios.facts` モジュールで `:doc` コマンドを繰り返します。

```bash
:doc cisco.ios.facts
```

Playbook で facts モジュールを使用します。

### ステップ 2 - プレイの作成

Ansible Playbook は [**YAML** ファイル](https://yaml.org/) です。YAML
は構造化されたエンコーディング形式であり、人間が非常に読みやすくなっています (サブセットとは異なり、JSON 形式) 。

Visual Studio コードで新規ファイルを作成します: ![vscode new
file](images/vscode_new_file.png)

分かりやすくするために、Playbook に `facts.yml` という名前を付けます: ![vscode save
file](images/vscode_save_as.png)


次のプレイ定義を `facts.yml` に入力します。

```yaml
---
- name: gather information from routers
  hosts: cisco
  gather_facts: no
```

各行の説明は次のとおりです。

* 最初の行の `---` は、これが YAML ファイルであることを示しています。
* `- name:` キーワードは、この Ansible Playbookのオプションの説明です。
* `hosts:` キーワードは、インベントリーファイルで定義されたグループ `cisco` に対するこのプレイブックを意味します。
* `gather_facts: no` は必要ありません。これは、Ansible 2.8 以前では、これは Linux
  ホストでのみ機能し、ネットワークインフラストラクチャーでは機能しないためです。特定のモジュールを使用して、ネットワーク機器の事実を収集します。

### ステップ 3 - ファクトタスクの作成

次に、最初の `task` を追加します。このタスクでは、`cisco.ios.facts` モジュールを使用して、グループ `cisco`
内の各デバイスに関するファクトを収集します。

```yaml
---
- name: gather information from routers
  hosts: cisco
  gather_facts: no

  tasks:
    - name: gather router facts
      cisco.ios.facts:
```

> 注記:
>
> プレイはタスクのリストです。モジュールは、そのタスクを実行する、事前に記述されたコードです。

Playbook を保存します。

### ステップ 4 - Playbook の実行

`ansible-navigator` を実行して Ansible Playbook を実行します。

```sh
$ ansible-navigator run facts.yml
```

これにより、Playbook が対話する間に対話セッションが開きます。

facts.yml のスクリーンショット: ![ansible-navigator run
facts.yml](images/ansible-navigator-facts.png)

Playbook の出力をズームするには、**0** を押して、ホスト中心ビューを表示します。ホストは 1 つしかないため、オプションは 1
つのみです。

ズームインのスクリーンショット: ![ansible-navigator zoom
hosts](images/ansible-navigator-hosts.png)

**rtr1** の詳細出力を表示するには、**0** をあと 1 回押してモジュールの戻り値をズームします。

モジュールデータへのズームインのスクリーンショット: ![ansible-navigator zoom
module](images/ansible-navigator-module.png)

スクロールダウンして、Cisco ネットワークデバイスから収集したファクトを表示できます。

### ステップ 5 - デバッグモジュールの使用

ルーターの OS バージョンとシリアル番号を表示する 2 つの追加タスクを記述します。

<!-- {% raw %} -->

``` yaml
---
- name: gather information from routers
  hosts: cisco
  gather_facts: no

  tasks:
    - name: gather router facts
      cisco.ios.facts:

    - name: display version
      debug:
        msg: "The IOS version is: {{ ansible_net_version }}"

    - name: display serial number
      debug:
        msg: "The serial number is:{{ ansible_net_serialnum }}"
```

<!-- {% endraw %} -->

### ステップ 6 - stdout の使用

次に、`ansible-navigator` と `--mode stdout` を使用して Playbook を再実行します

完全なコマンドは `ansible-navigator run facts.yml --mode stdout` です

stdout を使用した ansible-navigator のスクリーンショット: ![ansible-navigator stdout
screenshot](images/ansible-navigator-facts-stdout.png)


20 行未満の "code"
を使用すると、バージョンとシリアル番号の収集が自動化されます。これを本番ネットワークに対して実行していたと想像してみてください。古くなっていない実用的なデータが手元にあります。

## 重要なこと

* `ansible-navigator :doc`
  コマンドを使用すると、インターネットに接続していなくてもドキュメントにアクセスできます。このドキュメントは、コントロールノードの Ansible
  のバージョンとも一致します。
* [cisco.ios.facts モジュール](https://docs.ansible.com/ansible/latest/collections/cisco/ios/ios_config_module.html)
  は、Cisco IOS に固有の構造化データを収集します。各ネットワークプラットフォームに関連するモジュールがあります。たとえば、Juniper
  Junos には junos_facts があり、AristaEOS には eos_facts があります。
* [デバッグモジュール](https://docs.ansible.com/ansible/latest/modules/debug_module.html)
  を使用すると、Ansible Playbook でターミナルウィンドウに値を出力できます。

## ソリューション

完成した Ansible Playbook は、回答キーとしてここに提供されています: [facts.yml](facts.yml)。

## 完了

ラボ演習 3 を完了しました

---
[前の演習](../2-first-playbook/README.ja.md) |
[次の演習](../4-resource-module/README.ja.md)

[Ansible Network Automation ワークショップに戻る](../README.ja.md)
