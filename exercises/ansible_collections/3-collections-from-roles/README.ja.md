# 演習 3 - ロールからのコレクションの実行

## 目次

- [目的](#objective)
- [ガイド](#guide)
    - [ステップ 1: コレクション検索について](#step-1-understand-collections-lookup)
    - [ステップ 2: ロールからのコレクションの実行](step-2-running-collections-from-a-role)
- [重要なこと](#takeaways)

# 目的

この演習により、ユーザーは、ロール内からコレクションがどのように使用されるかを理解できるようになります。

以下のトピックについて説明します:

- コレクションの解決ロジックを説明します。

- コレクション完全修飾コレクション名 (FQCN) を使用してロールからコレクションを呼び出す方法を説明します。

# ガイド

## ステップ 1: コレクション検索について

Ansible コレクションは単純な方法を使用してコレクションの namespace を定義します。Playbook が `collections`
キーと 1 つ以上のロールを使用してコレクションを読み込む場合、ロールは Playbook によって設定されたコレクションを継承しません。

これは、この演習のメイントピックにつながります。つまり、ロールには、ロールのメタデータに基づいた独立したコレクションの読み込み方法があります。ロール内のタスクのコレクション検索を制御するために、ユーザーは
2 つのアプローチから選択することができます。

- **アプローチ 1**: ロール内の `meta/main.yml` ファイル内の `collections`
  フィールドでコレクションの一覧を渡します。これにより、ロールによって検索されるコレクションの一覧は、Playbook
  のコレクション一覧よりも優先度が高くなります。Ansible は、ロールを呼び出す Playbook が別の `collections`
  キーワードエントリーで異なるコレクションを定義する場合でも、ロール内で定義されたコレクション一覧を使用します。

  ```yaml
  # myrole/meta/main.yml
  collections:
    - my_namespace.first_collection
    - my_namespace.second_collection
    - other_namespace.other_collection
  ```

- **アプローチ 2**: ロールのタスクから直接コレクション完全修飾コレクション名 (FQCN) を使用します。これにより、コレクションは常に一意の
  FQCN で呼び出され、Playbook の他のルックアップを上書きします。

  ```yaml
  - name: Create an EC2 instance using collection by FQCN
    amazon.aws.ec2:
      key_name: mykey
      instance_type: t2.micro
      image: ami-123456
      wait: yes
      group: webserver
      count: 3
      vpc_subnet_id: subnet-29e63245
      assign_public_ip: yes
  ```

コレクション **内**
で定義されるロールは、独自のコレクションを常に暗黙的に最初に検索します。そのため、モジュール、プラグイン、またはその他のロールにアクセスするために、ロールメタデータで
`collections` キーワードを使用する必要はありません。

## ステップ 2: ロールからのコレクションの実行

演習フォルダーを作成します。

```bash
mkdir exercise-03
cd esercise--3
```

このラボでは、`ansible.posix` コレクションを使用します。これには、システム管理用の一連の POSIX
指向モジュールおよびプラグインが含まれます。

```bash
ansible-galaxy collection install ansible.posix
```

### アプローチ 1: メタデータとして読み込まれたコレクション

> **ヒント**: 演習のステップを実行したり、`solutions/selinux_manage_meta` から完了したロールをコピーしたりできます。

`ansible-galaxy init` コマンドを使用して新しいロールを作成します。

```bash
ansible-galaxy init --init-path roles selinux_manage_meta
```

`roles/selinux_manage_meta/meta/main.yml` ファイルを編集し、列 1
から始まるファイルの最後に以下の行を追加します。

```yaml
# Collections list
collections:
  - ansible.posix
```

`roles/selinux_manage_meta/tasks/main.yml` ファイルを編集し、以下のタスクを追加します。

```yaml
---
# tasks file for selinux_manage_meta
- name: Enable SELinux enforcing mode
  selinux:
    policy: targeted
    state: "{{ selinux_mode }}"

- name: Enable booleans
  seboolean:
    name: "{{ item }}"
    state: true
    persistent: true
  loop: "{{ sebooleans_enable }}"

- name: Disable booleans
  seboolean:
    name: "{{ item }}"
    state: false
    persistent: true
  loop: "{{ sebooleans_disable }}"
```

> **注記:** 簡単なモジュール名を使用しています。Ansible は、メタデータファイルの
> `collections` 一覧からの情報を使用し、使用されるコレクションを見つけます。

`roles/selinux_manage_meta/defaults/main.yml` を編集して、ロール変数のデフォルト値を定義します。

```yaml
---
# defaults file for selinux_manage_meta
selinux_mode: enforcing
sebooleans_enable: []
sebooleans_disable: []
```

ロール内の未使用のフォルダーをクリーンアップします。

```bash
rm -rf roles/selinux_manage_meta/{tests,vars,handlers,files,templates}
```

これで、基本的な Playbook で新しいロールをテストできます。以下の内容で現在のフォルダーに `playbook.yml` ファイルを作成します。

```yaml
---
- hosts: localhost
  become: true
  vars:
    sebooleans_enable:
      - httpd_can_network_connect
      - httpd_mod_auth_pam
    sebooleans_disable:
      - httpd_enable_cgi
  roles:
    - selinux_manage_meta
```

Playbook を実行して結果を確認します。

```bash
$ ansible-playbook playbook.yml
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [localhost] ******************************************************************************************************

TASK [Gathering Facts] ************************************************************************************************
ok: [localhost]

TASK [selinux_manage_meta : Enable SELinux enforcing mode] ************************************************************
ok: [localhost]

TASK [selinux_manage_meta : Enable booleans] **************************************************************************
changed: [localhost] => (item=httpd_can_network_connect)
changed: [localhost] => (item=httpd_mod_auth_pam)

TASK [selinux_manage_meta : Disable booleans] *************************************************************************
changed: [localhost] => (item=httpd_can_network_connect)

PLAY RECAP ************************************************************************************************************
localhost                  : ok=4    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

### アプローチ 2: FQCN で読み込まれるコレクション

2 つ目のアプローチは、コレクションの FQCN
を使用して関連モジュールおよびプラグインを呼び出します。違いをよりよく示すために、内部ロジックを変更せずに、FQCN
アプローチで以前のロールの新しいバージョンを実装します。

> **ヒント**: 演習のステップを実行したり、`solutions/selinux_manage_fqcn` から完了したロールをコピーしたりできます。

`ansible-galaxy init` コマンドを使用して新しいロールを作成します。

```bash
ansible-galaxy init --init-path roles selinux_manage_fqcn
```

`roles/selinux_manage_fqcn/tasks/main.yml` ファイルを編集し、以下のタスクを追加します。

```yaml
---
# tasks file for selinux_manage_fqcn
- name: Enable SELinux enforcing mode
  ansible.posix.selinux:
    policy: targeted
    state: "{{ selinux_mode }}"

- name: Enable booleans
  ansible.posix.seboolean:
    name: "{{ item }}"
    state: true
    persistent: true
  loop: "{{ sebooleans_enable }}"

- name: Disable booleans
  ansible.posix.seboolean:
    name: "{{ item }}"
    state: false
    persistent: true
  loop: "{{ sebooleans_disable }}"
```

> **注記**: ロールタスクでのモジュール FQCN の使用方法に注意してください。Ansible は直接、
> `collections` キーワードが Playbook レベルで定義されている場合でも、
> ロールタスク内からインストールされたコレクションを検索します。

`roles/selinux_manage_fqcn/defaults/main.yml` を編集して、ロール変数のデフォルト値を定義します。

```yaml
---
# defaults file for selinux_manage_fqcn
selinux_mode: enforcing
sebooleans_enable: []
sebooleans_disable: []
```

ロール内の未使用のフォルダーをクリーンアップします。

```bash
rm -rf roles/selinux_manage_meta/{tests,vars,handlers,files,templates}
```

新しいロールを使用するように、以前の `playbook.yml` ファイルを変更します。

```yaml
---
- hosts: localhost
  become: true
  vars:
    sebooleans_enable:
      - httpd_can_network_connect
      - httpd_mod_auth_pam
    sebooleans_disable:
      - httpd_enable_cgi
  roles:
    - selinux_manage_FQCN
```

Playbook を再度実行し、結果を確認します。

```bash
$ ansible-playbook playbook.yml
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [localhost] ******************************************************************************************************

TASK [Gathering Facts] ************************************************************************************************
ok: [localhost]

TASK [selinux_manage_meta : Enable SELinux enforcing mode] ************************************************************
ok: [localhost]

TASK [selinux_manage_meta : Enable booleans] **************************************************************************
changed: [localhost] => (item=httpd_can_network_connect)
ok: [localhost] => (item=httpd_mod_auth_pam)

TASK [selinux_manage_meta : Disable booleans] *************************************************************************
changed: [localhost] => (item=httpd_can_network_connect)

PLAY RECAP ************************************************************************************************************
localhost                  : ok=4    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

これでガイド付きの演習は終了となります。

# 重要なこと

- コレクションは、`meta/main.yml` で定義されている `collections` リストを使用して、ロールから呼び出すことができます。

- コレクションは、ロールタスクから直接 FQCN を使用して、ロールから呼び出すことができます。

----
**ナビゲーション**
<br>
[前の演習](../2-collections-from-playbook/) - [次の演習](../4-collections-from-tower)

[Click here to return to the Ansible for Red Hat Enterprise Linux
Workshop](../README.md)
