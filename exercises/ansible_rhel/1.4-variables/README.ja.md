# ワークショップの演習 - 変数の使用

**他の言語で読む**:
<br>![uk](../../../images/uk.png) [英語](README.md), ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [ブラジルのポルトガル語](README.pt-br.md), ![france](../../../images/fr.png) [フランス語](README.fr.md), ![Español](../../../images/col.png) [スペイン語](README.es.md).

## 目次

- [ワークショップの演習 - 変数の使用](##ワークショップの演習---変数の使用)
  - [目的](#目的)
  - [ガイド](#ガイド)
    - [ステップ 1 - 変数の理解](#ステップ-1---変数の理解)
    - [ステップ 2 - 変数の構文と作成](#ステップ-2---変数の構文と作成)
    - [ステップ 3 - 変更されたプレイブックの実行](#ステップ-3---変更されたプレイブックの実行)
    - [ステップ 4 - チェックプレイブックでの高度な変数の使用](#ステップ-4---チェックプレイブックでの高度な変数の使用)

## 目的
演習 1.3 からのプレイブックを拡張し、Ansible での変数の作成と使用に焦点を当てます。変数を定義し、使用するための構文を学び、動的で適応可能なプレイブックを作成するための不可欠なスキルを習得します。

## ガイド
Ansible の変数は、プレイブックを柔軟で再利用可能にする強力なツールです。値を保存して再利用することができ、プレイブックをより動的で適応可能にします。

### ステップ 1 - 変数の理解
Ansible での変数は、あるデータの名前付き表現です。変数には、文字列や数値のような単純な値や、リストや辞書のような複雑なデータを含めることができます。

### ステップ 2 - 変数の構文と作成
変数の作成と使用には、特定の構文が関与します：

1. 変数の定義：変数は、プレイブックの `vars` セクションや、大規模なプロジェクトのための別々のファイルで定義されます。
2. 変数名の命名：変数名は説明的であるべきで、以下のようなルールに従うべきです：
   * 文字またはアンダースコアで始まること。
   * 文字、数字、アンダースコアのみを含むこと。
3. 変数の使用：タスク内で変数は `"{{ variable_name }}"` というダブルカーリーブレイスを引用符で囲んで参照されます。この構文は、実行時に Ansible に変数の値で置き換えるよう指示します。

`system_setup.yml` プレイブックを更新して、変数を含めて使用します：

```yaml
---
- name: 基本的なシステムセットアップ
  hosts: node1
  become: true
  vars:
    user_name: 'Roger'
  tasks:
    - name: セキュリティ関連のパッケージをすべて更新する
      ansible.builtin.dnf:
        name: '*'
        state: latest
        security: true

    - name: 新しいユーザーを作成する
      ansible.builtin.user:
        name: "{{ user_name }}"
        state: present
        create_home: true
```

"`ansible-navigator`を使用してこのプレイブックを実行してください。

### ステップ 3 - 修正されたプレイブックの実行

更新されたプレイブックを実行します:

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_setup.yml -m stdout
```

```yaml
PLAY [基本システム設定] ******************************************************

TASK [事実の収集] *********************************************************
ok: [node1]

TASK [すべてのセキュリティ関連のパッケージを更新する] ************************************
ok: [node1]

TASK [新しいユーザーを作成] *******************************************************
changed: [node1]

PLAY RECAP *********************************************************************
node1                      : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

更新されたプレイブックで「新しいユーザーを作成」タスクのステータスが変更されたことに注目してください。varsセクションに指定されたユーザー「Roger」が作成されました。

ユーザー作成を確認するには:

ステップ 4 - チェックプレイブック内の高度な変数使用
system_checks.ymlプレイブックを強化して、register変数とwhen条件文を使用し、システム内の「Roger」ユーザーの存在を確認します。

Ansibleのregisterキーワードは、タスクの出力をキャプチャして変数に保存するために使用されます。

`system_checks.yml` プレイブックを更新します:

```yaml
---
- name: システム設定チェック
  hosts: node1
  become: true
  vars:
    user_name: 'Roger'
  tasks:
    - name: ユーザー存在チェック
      ansible.builtin.command:
        cmd: "id {{ user_name }}"
      register: user_check

    - name: ユーザー状態の報告
      ansible.builtin.debug:
        msg: "ユーザー {{ user_name }} は存在します。"
      when: user_check.rc == 0
```

プレイブックの詳細:

* `register: user_check:` これはidコマンドの出力を変数user_checkにキャプチャします。

* `when: user_check.rc == 0:` この行は条件文です。これは、前のタスクの戻り値（user_checkに保存されています）が0であるかどうかをチェックし、成功を示します。この条件が満たされると、デバッグメッセージが表示されます。
この設定は、前のステップの結果に基づいてタスクの流れを制御するために変数を使用する方法の実用的な例を提供します。

チェックプレイブックを実行します:

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_checks.yml -m stdout
```

```bash
PLAY [システム設定チェック] *********************************************

TASK [事実の収集] *********************************************************
ok: [node1]

TASK [ユーザー存在チェック] ****************************************************
changed: [node1]

TASK [ユーザー状態の報告] ******************************************************
ok: [node1] => {
    "msg": "ユーザー Roger は存在します。"
}

PLAY RECAP *********************************************************************
node1                      : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

---
**ナビゲーション**
<br>

[前のエクササイズ](../1.3-playbook/README.ja.md) -[次のエクササイズ](../1.5-handlers/README.ja.md)
<br><br>
[Ansible for Red Hat Enterprise Linux ワークショップに戻る](../README.md)

