# ワークショップ演習 - 前提条件の確認

**他の言語で読む**:
<br>![uk](../../../images/uk.png) [英語](README.md), ![japan](../../../images/japan.png) [日本語](README.ja.md), ![brazil](../../../images/brazil.png) [ブラジルのポルトガル語](README.pt-br.md), ![france](../../../images/fr.png) [フランス語](README.fr.md), ![Español](../../../images/col.png) [スペイン語](README.es.md).

## 目次

- [ワークショップ演習 - 前提条件の確認](#ワークショップ演習---前提条件の確認)
  - [目次](#目次)
  - [目的](#目的)
  - [ガイド](#ガイド)
    - [あなたのラボ環境](#あなたのラボ環境)
    - [ステップ 1 - 環境へのアクセス](#ステップ-1---環境へのアクセス)
    - [ステップ 2 - ターミナルの使用](#ステップ-2---ターミナルの使用)
    - [ステップ 3 - 実行環境の検討](#ステップ-3---実行環境の検討)
    - [ステップ 4 - ansible-navigatorの設定の検討](#ステップ-4---ansible-navigatorの設定の検討)
    - [ステップ 5 - チャレンジラボ](#ステップ-5---チャレンジラボ)

## 目的

* ラボトポロジーを理解する：ラボ環境とアクセス方法に慣れる。
* ワークショップの演習をマスターする：ワークショップのタスクをナビゲートし、実行するスキルを習得する。
* チャレンジラボを受け入れる：実践的なチャレンジシナリオで知識を適用する方法を学ぶ。

## ガイド

このワークショップの初期段階は、Ansibleオートメーションプラットフォームのコマンドラインユーティリティに焦点を当てています。例えば:

- [ansible-navigator](https://github.com/ansible/ansible-navigator) - Ansibleコンテンツを実行および開発するためのテキストベースのユーザーインターフェイス（TUI）。
- [ansible-core](https://docs.ansible.com/core.html) - `ansible`、`ansible-playbook`、`ansible-doc`などのCLIツールを含む、Ansibleオートメーションプラットフォームを支えるフレームワーク、言語、機能を提供するベース実行可能ファイル。
- [実行環境](https://docs.ansible.com/automation-controller/latest/html/userguide/execution_environments.html) - Red Hatがサポートするコレクションを含む、事前に構築されたコンテナイメージ。
- [ansible-builder](https://github.com/ansible/ansible-builder) - 実行環境の構築プロセスを自動化します。このワークショップでは主な焦点ではありません。

新しいAnsibleオートメーションプラットフォームコンポーネントの詳細については、このランディングページをブックマークしてください [https://red.ht/AAP-20](https://red.ht/AAP-20)

### あなたのラボ環境

以下のホストを含む事前設定された環境で作業します:

| 役割                    | インベントリ名   |
| ----------------------- | --------------- |
| Ansibleコントロールホスト | ansible-1       |
| 管理ホスト1             | node1           |
| 管理ホスト2             | node2           |
| 管理ホスト3             | node3           |

### ステップ 1 - 環境へのアクセス

このワークショップでは、統合ファイルブラウザ、構文強調表示エディタ、ブラウザ内ターミナルを備えたVisual Studio Codeの使用をお勧めします。直接SSHアクセスも利用可能です。ワークベンチ環境へのアクセスに関するこのYouTubeチュートリアルをチェックしてください。

注意: 追加の明確化が必要な場合は、短いYouTubeビデオが提供されています：
[Ansible Workshops - ワークベンチ環境へのアクセス](https://youtu.be/Y_Gx4ZBfcuk)

1. ワークショップの起動ページからVisual Studio Codeに接続します。

  ![起動ページ](images/launch_page.png)

2. 提供されたパスワードを入力してログインします。

  ![VS Codeのログイン](images/vscode_login.png)

### ステップ 2 - ターミナルの使用

1. Visual Studio Codeでターミナルを開きます:

  ![新しいターミナルの画像](images/vscode-new-terminal.png)

2. Ansibleコントロールノードのターミナルで`rhel-workshop`ディレクトリに移動します。

```bash
[student@ansible-1 ~]$ cd ~/rhel-workshop/
[student@ansible-1 rhel-workshop]$ pwd
/home/student/rhel-workshop
```

* `~`: ホームディレクトリ`/home/student`のショートカット
* `cd`: ディレクトリを変更するコマンド
* `pwd`: 現在の作業ディレクトリの完全なパスを表示します。

### ステップ 3 - 実行環境の検討

1. `ansible-navigator images`を実行して、設定された実行環境を表示します。
2. 対応する番号を使用してEEを調査します。例えば、`ee-supported-rhel8`を開くために2を押します。

```bash
$ ansible-navigator images
```

![ansible-navigatorの画像](images/navigator-images.png)

> 注意: あなたが見る出力は上記の出力と異なる場合があります

![eeメインメニュー](images/navigator-ee-menu.png)

`2`を選択すると`Ansibleバージョンとコレクション`が表示され、その特定のEEにインストールされているすべてのAnsibleコレクションと`ansible-core`のバージョンが表示されます：

![ee情報](images/navigator-ee-collections.png)

### ステップ 4 - ansible-navigatorの設定の検討

1. Visual Studio Codeまたは`cat`コマンドを使用して`~/.ansible-navigator.yml`の内容を表示します。

```bash
$ cat ~/.ansible-navigator.yml
---
ansible-navigator:
  ansible:
    inventory:
      entries:
      - /home/student/lab_inventory/hosts

  execution-environment:
    image: registry.redhat.io/ansible-automation-platform-20-early-access/ee-supported-rhel8:2.0.0
    enabled: true
    container-engine: podman
    pull:
      policy: missing
    volume-mounts:
    - src: "/etc/ansible/"
      dest: "/etc/ansible/"
```

2. `ansible-navigator.yml`ファイル内の以下のパラメーターに注意してください：

* `inventories`: 使用されているansibleインベントリの場所を示します
* `execution-environment`: デフォルトの実行環境が設定されている場所

設定可能なすべてのノブの完全なリストについては、[ドキュメント](https://ansible.readthedocs.io/projects/navigator/settings/)をチェックしてください。

### ステップ 5 - チャレンジラボ

各章にはチャレンジラボが付属しています。これらのタスクは、学んだ概念の理解と適用をテストします。解決策は警告サインの下に提供されています。

---
**ナビゲーション**

<br>

{% if page.url contains 'ansible_rhel_90' %}
[Next Exercise](../2-thebasics)
{% else %}
[Next Exercise](../1.2-thebasics)
{% endif %}
<br><br>
[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md)
