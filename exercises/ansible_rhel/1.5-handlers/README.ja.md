# ワークショップ演習 - 条件分岐、ハンドラー、ループ

**他の言語で読む**:
<br>![uk](../../../images/uk.png) [英語](README.md), ![japan](../../../images/japan.png) [日本語](README.ja.md), ![brazil](../../../images/brazil.png) [ブラジルのポルトガル語](README.pt-br.md), ![france](../../../images/fr.png) [フランス語](README.fr.md), ![Español](../../../images/col.png) [スペイン語](README.es.md).

# ワークショップ演習 - 条件分岐、ハンドラー、ループの使用

## 目次

- [目的](#目的)
- [ガイド](#ガイド)
  - [ステップ 1 - 条件分岐、ハンドラー、ループの理解](#ステップ-1---条件分岐ハンドラーループの理解)
  - [ステップ 2 - 条件分岐](#ステップ-2---条件分岐)
  - [ステップ 3 - ハンドラー](#ステップ-3---ハンドラー)
  - [ステップ 4 - ループ](#ステップ-4---ループ)

## 目的

演習 1.4 を基に、この演習では Ansible プレイブックでの条件分岐、ハンドラー、ループの応用を紹介します。条件分岐を使ったタスク実行の制御、ハンドラーを使ったサービス応答の管理、ループを使った繰り返しタスクの効率的な処理方法を学びます。

## ガイド

条件分岐、ハンドラー、ループは Ansible の高度な機能であり、自動化プレイブックの制御、効率、柔軟性を向上させます。

### ステップ 1 - 条件分岐、ハンドラー、ループの理解

- **条件分岐**: 特定の条件に基づいてタスクを実行できるようにします。
- **ハンドラー**: `notify` ディレクティブによってトリガーされる特別なタスクで、通常は変更後にサービスを再起動するために使用されます。
- **ループ**: タスクを複数回繰り返し実行するために使用され、タスクが類似しているが異なるアイテムに適用する必要がある場合に特に便利です。

### ステップ 2 - 条件分岐

Ansible の条件分岐は、特定の条件に基づいてタスクが実行されるかどうかを制御します。
インベントリ内の `web` グループに属するホストにのみ Apache HTTP サーバー (`httpd`) をインストールする機能を system_setup.yml プレイブックに追加しましょう。

> 注: 以前の例ではホストを node1 に設定していましたが、現在は all に設定されています。これは、この更新された Ansible プレイブックを実行すると、自動化対象の新しいシステムの更新、新しいシステム上に作成されたユーザー Roger、web グループ内のすべてのホストにインストールされた Apache Web サーバーパッケージ httpd が表示されることを意味します。

```yaml
---
- name: 基本的なシステム設定
  hosts: all
  become: true
  vars:
    user_name: 'Roger'
    package_name: httpd
  tasks:
    - name: セキュリティ関連のパッケージをすべて更新
      ansible.builtin.dnf:
        name: '*'
        state: latest
        security: true
        update_only: true

    - name: 新しいユーザーを作成
      ansible.builtin.user:
        name: "{{ user_name }}"
        state: present
        create_home: true

    - name: Web サーバーに Apache をインストール
      ansible.builtin.dnf:
        name: "{{ package_name }}"
        state: present
      when: inventory_hostname in groups['web']
```

この例では、`inventory_hostname in groups['web']` が条件文です。`inventory_hostname` はプレイブックで Ansible が作業している現在のホストの名前を指します。この条件は、このホストがインベントリファイルで定義された `web` グループの一部であるかどうかを確認します。真の場合、タスクが実行され、そのホストに Apache がインストールされます。

### ステップ 3 - ハンドラー

ハンドラーは、別のタスクによって通知されたときにのみ実行されるべきタスクに使用されます。通常、設定変更後にサービスを再起動するために使用されます。

例えば、すべての Web サーバーでファイアウォールが正しく設定されていることを確認し、その後、新しい設定を適用するためにファイアウォールサービスをリロードしたいとしましょう。希望するファイアウォールルールが適切に設置されていることを確認するタスクによって通知されるファイアウォールサービスをリロードするハンドラーを定義します:

```yaml
---
- name: 基本的なシステム設定
  hosts: all
  become: true
  .
  .
  .
    - name: firewalld をインストール
      ansible.builtin.dnf:
        name: firewalld
        state: present

    - name: firewalld が実行中であることを確認
      ansible.builtin.service:
        name: firewalld
        state: started
        enabled: true

    - name: Web サーバーで HTTPS トラフィックを許可
      ansible.posix.firewalld:
        service: https
        permanent: true
        state: enabled
      when: inventory_hostname in groups['web']
      notify: ファイアウォールをリロード

  handlers:
    - name: ファイアウォールをリロード
      ansible.builtin.service:
        name: firewalld
        state: reloaded
```

「Web サーバーで HTTPS トラフィックを許可」タスクに変更がある場合にのみ、ハンドラー「ファイアウォールをリロード」がトリガーされます。

> 注: 「ファイアウォールをリロード」設定タスクの notify セクション内でハンドラーの名前が使用されていることに注意してください。これにより、Ansible プレイブック内に複数のハンドラーが存在する場合でも、適切なハンドラーが実行されることが保証されます。


```bash
PLAY [基本的なシステム設定] ******************************************************

TASK [事実の収集] *********************************************************
ok: [node1]
ok: [node2]
ok: [ansible-1]
ok: [node3]

TASK [セキュリティ関連のパッケージをすべて更新] ************************************
ok: [node2]
ok: [node1]
ok: [ansible-1]
ok: [node3]

TASK [新しいユーザーを作成] *******************************************************
ok: [node1]
ok: [node2]
ok: [ansible-1]
ok: [node3]

TASK [Web サーバーに Apache をインストール] *******************************************
skipping: [ansible-1]
ok: [node2]
ok: [node1]
ok: [node3]

TASK [firewalld をインストール] *******************************************************
changed: [ansible-1]
changed: [node2]
changed: [node1]
changed: [node3]

TASK [firewalld が実行中であることを確認] *********************************************
changed: [node3]
changed: [ansible-1]
changed: [node2]
changed: [node1]

TASK [Web サーバーで HTTPS トラフィックを許可] **************************************
skipping: [ansible-1]
changed: [node2]
changed: [node1]
changed: [node3]

RUNNING HANDLER [ファイアウォールをリロード] **********************************************
changed: [node2]
changed: [node1]
changed: [node3]

PLAY RECAP *********************************************************************
ansible-1                  : ok=5    changed=2    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
node1                      : ok=8    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node2                      : ok=8    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node3                      : ok=8    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

```

### ステップ 4 - ループ

Ansible のループを使用すると、異なる値を使って複数回タスクを実行できます。この機能は、与えられた例のように複数のユーザーアカウントを作成するタスクなど、特に便利です。演習 1.4 からの元の system_setup.yml プレイブックでは、1人のユーザーを作成するタスクがありました:

```yaml
- name: 新しいユーザーを作成
  ansible.builtin.user:
    name: "{{ user_name }}"
    state: present
    create_home: true
```

これで、ループを使用して複数のユーザーを作成するようにこのタスクを変更しましょう:

```yaml
- name: 新しいユーザーを作成
  ansible.builtin.user:
    name: "{{ item }}"
    state: present
    create_home: true
  loop:
    - alice
    - bob
    - carol
```

変更点は何ですか？

1. ループディレクティブ: ループキーワードは、アイテムのリストを繰り返し処理するために使用されます。この場合、リストには作成したいユーザーの名前が含まれています: alice、bob、および carol。

2. ループを使ったユーザー作成: 1人のユーザーを作成する代わりに、変更されたタスクはループリストの各アイテムを繰り返し処理します。{{ item }} プレースホルダーはリスト内の各ユーザー名に動的に置き換えられるため、ansible.builtin.user モジュールは順番に各ユーザーを作成します。

更新されたプレイブックを実行すると、このタスクはループ内の各ユーザーについて一度に実行されます。入力データが異なる繰り返しタスクを効率的に処理する方法です。

すべてのノードで新しいユーザーを作成するための出力のスニペットです。

```bash
[student@ansible-1 ~lab_inventory]$ ansible-navigator run system_setup.yml -m stdout

PLAY [基本的なシステム設定] ******************************************************

.
.
.

TASK [新しいユーザーを作成] *******************************************************
changed: [node2] => (item=alice)
changed: [ansible-1] => (item=alice)
changed: [node1] => (item=alice)
changed: [node3] => (item=alice)
changed: [node1] => (item=bob)
changed: [ansible-1] => (item=bob)
changed: [node3] => (item=bob)
changed: [node2] => (item=bob)
changed: [node1] => (item=carol)
changed: [node3] => (item=carol)
changed: [ansible-1] => (item=carol)
changed: [node2] => (item=carol)

.
.
.


PLAY RECAP *********************************************************************
ansible-1                  : ok=5    changed=1    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
node1                      : ok=7    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node2                      : ok=7    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node3                      : ok=7    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

---
**ナビゲーション**
<br>
[前の演習](../1.4-variables/README.ja.md) -[次の演習](../1.6-templates/README.ja.md)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-1---ansible-engine-exercises)


