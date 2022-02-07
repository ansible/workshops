# 演習 2: Ansible コレクションの使用

## 目次

- [目的](#objective)
- [ガイド](#guide)
    - [ステップ 1 - Ansible
      コレクションのインストール](#step-1---install-the-ansible-collection)
    - [ステップ 2 - Ansible Playbook の記述](#step-2---write-an-ansible-playbook)
    - [ステップ 3 - Playbook のテスト](#step-3---test-the-playbook)
    - [ステップ 4 - namespace の簡素化](#step-4---simplify-the-namespace)
    - [ステップ 5: 変更をテストする](#step-5-test-the-change)

# 目的

ラボのこの部分では、Playbook で Ansible コレクションを使用する方法を説明します。Ansible
コレクションから特定のモジュールを識別するには、完全修飾コレクション名を使用する必要があります。この名前は、作成者名、コレクション名、およびモジュール名で成り立っています。

    <author>.<collection>.<module>

以下の演習では、Ansible Core Team が作成したコレクションを使用します。作成者の名前は "ansible" です。Ansible
Core Team によって書かれたすべてのモジュールとコレクションの一覧は、[Ansible
Galaxy](https://galaxy.ansible.com/ansible). で確認できます。

ここでは、コレクションとロールを複数維持しています。これらのコレクションの 1 つは "posix"
と呼ばれます。ドキュメントと詳細については、[Ansible Galaxy POSIX
Collection](https://galaxy.ansible.com/ansible/posix) を参照してください。

このコレクションが提供するモジュールの 1
つで、[SELinux](https://www.redhat.com/en/topics/linux/what-is-selinux)
設定を管理できます。そのため、このモジュールの完全修飾コレクション名は `ansible.posix.selinux` になります。

[コレクションの使用](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html))
の詳細は、[Ansible ドキュメント](https://docs.ansible.com/). を参照してください。

# ガイド

## ステップ 1 - Ansible コレクションのインストール

本演習に使用する `ansible.posix.selinux` モジュールは、`ansible.posix`
コレクションの一部になります。モジュールを使用する前に、このコレクションを最初にインストールする必要があります。`ansible-galaxy`
コマンドラインツールを使用し、インストールを自動化できます。[Ansible Galaxy](https://galaxy.ansible.com/)
でロールとコレクションを検索するように事前設定されているので、コレクション名を指定するだけで、あとは処理されます。

    ansible-galaxy collection install ansible.posix

これにより、システムにコレクションがインストールされますが、まだインストールされていない場合に限ります。インストールを強制するには、たとえば、最新バージョンを使用していることを確認するために、強制スイッチ
`-f` を追加できます

    ansible-galaxy collection install -f ansible.posix

これにより、すでに最新の状態であっても最新バージョンが常にダウンロードされ、インストールされます。Ansible コレクションには、他の Ansible
コレクションにも依存関係を持つことができます。これらの依存関係も確実に更新する場合は、`--force-with-deps` スイッチを使用できます。

デフォルトでは、インストールはローカルの `~/.ansible` ディレクトリーに保存されます。これは、`-p
/path/to/collection` スイッチを使用して上書きできます。ただし、`ansible.cfg`
を適宜変更した場合にのみ、`ansible-playbook` がそのディレクトリを使用することに注意してください。

## ステップ 2 - ドキュメント

`ansible-doc`
コマンドは、システムディレクトリーのみでドキュメントの検索を行います。ただし、完全修飾コレクション名を使用して、Ansible
コレクションからインストールしたモジュールを読み取るために引き続きこれを使用できます。

演習の次の部分で使用する `selinux` モジュールのモジュールドキュメントを見てみましょう。

```bash
ansible-doc ansible.posix.selinux
```

> **注記**: 画面の解像度によっては、ドキュメントビューアを終了するために `q` を押す必要がある場合があります。

## ステップ 3 - Ansible Playbook を記述します。

SELinux モジュールを使用して、Enforcing モードに設定されていることを確認します。SELinux は、Linux
システムに追加のセキュリティーをもたらすカーネル機能です。これは、常に有効にし、Enforcing モードに保つことが強く推奨されます。SELinux
を初めて使用する場合は、[What is
SELinux](https://www.redhat.com/en/topics/linux/what-is-selinux)
の記事を参照してください。

SELinux を有効にし、ローカルマシンで Enforcing モードに設定する簡単な Playbook を記述してみましょう。

```yaml
---
- name: set SELinux to enforcing
  hosts: localhost
  become: yes
  tasks:
  - name: set SElinux to enforcing
    ansible.posix.selinux:
      policy: targeted
      state: enforcing
```

後で使用するために Playbook を `enforce-selinux.yml` として保存します。

> **注記**: モジュール名に特に注意してください。通常、`selinux` のような内容が表示されますが、Ansible コレクションで提供されるモジュールを使用しているため、完全修飾モジュール名を指定する必要があります。

## ステップ 4 - Playbook のテスト

Playbook を実行し、結果を確認します。

    ansible-playbook enforce-selinux.yml

以下のような出力が表示されるはずです。

    [警告]: ホストの一覧が空の場合、ローカルホストのみが使用可能です。暗黙的な localhost は 'all' と一致しないことに注意してください。

    PLAY [set SELinux to enforcing] ***********************************************************************************

    TASK [Gathering Facts] ********************************************************************************************
    ok: [localhost]

    TASK [set SElinux to enforcing] ***********************************************************************************
    ok: [localhost]

    PLAY RECAP ********************************************************************************************************
    localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

SELinux が Enforcing に設定されていなかった場合は、ok ではなく "changed" が表示されることがあります。"changed"
と表示され、2 回目を実行すると、今度は "ok" と表示されるはずです。これは、[Ansible
の冪等性](https://docs.ansible.com/ansible/latest/reference_appendices/glossary.html).
のマジックになります。

## ステップ 5 - namespace の簡素化

Playbook で Ansible コレクションから多くのモジュールを使用する場合、<author>.<collection> の接頭辞を付けると邪魔となり、Playbook を読むことが困難になる可能性があります。

`collections` キー単語を使用すると、すべてのタスクで namespace の定義を省略できます。

```yaml
---
- name: set SELinux to enforcing
  hosts: localhost
  become: yes
  collections:
  - ansible.posix
  tasks:
  - name: set SElinux to enforcing
    selinux:
      policy: targeted
      state: enforcing
```

> **注記**: 構文はロールの指定方法と似ていますが、動作が異なります。キーワード `roles` は各ロールで `tasks/main.yml` を実行します。`collections` キーワードは単なるショートカットであるため、タスクでモジュールを使用するたびに作成者と namespace はスキップできます。

## ステップ 6: 変更をテストする

Playbook を再度実行しても、実際には出力に違いは見られないはずです。前述したように、`collections` キーワードは Playbook
を書くことのみを簡素化します。

----
**ナビゲーション**
<br>
[前の演習](../1-create-collections/) - [次の演習](../3-collections-from-roles)

[Click here to return to the Ansible for Red Hat Enterprise Linux
Workshop](../README.md)
