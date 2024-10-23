# ワークショップ演習 - ロール: プレイブックを再利用可能にする

**他の言語で読む**:
<br>![uk](../../../images/uk.png) [英語](README.md), ![japan](../../../images/japan.png) [日本語](README.ja.md), ![brazil](../../../images/brazil.png) [ブラジルのポルトガル語](README.pt-br.md), ![france](../../../images/fr.png) [フランス語](README.fr.md), ![Español](../../../images/col.png) [スペイン語](README.es.md).

## 目次

- [目的](#目的)
- [ガイド](#ガイド)
  - [ステップ 1 - ロールの基本](#ステップ-1---ロールの基本)
  - [ステップ 2 - 環境のクリーンアップ](#ステップ-2---環境のクリーンアップ)
  - [ステップ 3 - Apacheロールの構築](#ステップ-3---Apacheロールの構築)
  - [ステップ 4 - プレイブックでのロールの統合](#ステップ-4---プレイブックでのロールの統合)
  - [ステップ 5 - ロールの実行と検証](#ステップ-5---ロールの実行と検証)
  - [ステップ 6 - Apacheが稼働していることを確認](#ステップ-6---Apacheが稼働していることを確認)

## 目的

この演習は、前の演習を基にしており、Apache（httpd）を設定するロールの作成を通じて、Ansibleスキルをさらに進化させます。変数、ハンドラー、カスタムindex.htmlのテンプレートを統合した知識を活用します。このロールは、タスク、変数、テンプレート、ハンドラーを再利用可能な構造にカプセル化し、効率的な自動化を実現する方法を示します。

## ガイド

### ステップ 1 - ロールの基本

Ansibleのロールは、関連する自動化タスクやリソース（変数、テンプレート、ハンドラーなど）を構造化されたディレクトリに整理します。この演習では、再利用性とモジュール性に重点を置いて、Apache設定ロールを作成することに焦点を当てます。

### ステップ 2 - 環境のクリーンアップ

Apache設定に関する以前の作業を踏まえ、環境を整理するためのAnsibleプレイブックを作成しましょう。このステップは、新しいApacheロールを導入するための準備を整え、行われた調整のクリアなビューを提供します。このプロセスを通じて、Ansibleロールによって提供される多様性と再利用性についての理解を深めます。

環境をクリーンアップするために以下のAnsibleプレイブックを実行します：

```yaml
---
- name: Cleanup Environment
  hosts: all
  become: true
  vars:
    package_name: httpd
  tasks:
    - name: Remove Apache from web servers
      ansible.builtin.dnf:
        name: "{{ package_name }}"
        state: absent
      when: inventory_hostname in groups['web']

    - name: Remove firewalld
      ansible.builtin.dnf:
        name: firewalld
        state: absent

    - name: Delete created users
      ansible.builtin.user:
        name: "{{ item }}"
        state: absent
        remove: true  # Use 'remove: true’ to delete home directories
      loop:
        - alice
        - bob
        - carol
        - Roger

    - name: Reset MOTD to an empty message
      ansible.builtin.copy:
        dest: /etc/motd
        content: ''
```

### ステップ 3 - Apacheロールの構築

`apache`という名前のロールを開発して、Apacheをインストール、設定、管理します。

1. ロール構造を生成する：

ansible-galaxyを使用してロールを作成し、出力のためにロールディレクトリを指定します。

```bash
[student@ansible-1 lab_inventory]$ mkdir roles
[student@ansible-1 lab_inventory]$ ansible-galaxy init --offline roles/apache
```

2. ロール変数を定義する：

Apacheに固有の変数で `/home/student/lab_inventory/roles/apache/vars/main.yml` を埋めます：

```yaml
---
# vars file for roles/apache
apache_package_name: httpd
apache_service_name: httpd
```

3. ロールタスクを設定する：

Apacheのインストールとサービス管理のタスクを含むように `/home/student/lab_inventory/roles/apache/tasks/main.yml` を調整します：

```yaml
---
# tasks file for ansible-files/roles/apache
- name: Install Apache web server
  ansible.builtin.package:
    name: "{{ apache_package_name }}"
    state: present

- name: Ensure Apache is running and enabled
  ansible.builtin.service:
    name: "{{ apache_service_name }}"
    state: started
    enabled: true

- name: Install firewalld
  ansible.builtin.dnf:
    name: firewalld
    state: present

- name: Ensure firewalld is running
  ansible.builtin.service:
    name: firewalld
    state: started
    enabled: true

- name: Allow HTTPS traffic on web servers
  ansible.posix.firewalld:
    service: https
    permanent: true
    state: enabled
  when: inventory_hostname in groups['web']
  notify: Reload Firewall
```

4. ハンドラーを実装する：

設定が変更された場合にfirewalldを再起動するハンドラーを `/home/student/lab_inventory/roles/apache/handlers/main.yml` に作成します：

```yaml
---
# handlers file for ansible-files/roles/apache
- name: Reload Firewall
  ansible.builtin.service:
    name: firewalld
    state: reloaded
```

5. テンプレートを作成して展開する：

カスタムの `index.html` のためのJinja2テンプレートを使用します。テンプレートを `templates/index.html.j2` に保存します：

```html
<html>
<head>
<title>Welcome to {{ ansible_hostname }}</title>
</head>
<body>
 <h1>Hello from {{ ansible_hostname }}</h1>
</body>
</html>
```

6. この `index.html` テンプレートを展開するために `tasks/main.yml` を更新します：

```yaml
- name: Deploy custom index.html
  ansible.builtin.template:
    src: index.html.j2
    dest: /var/www/html/index.html
```

### ステップ 4 - プレイブックでのロールの統合

`/home/student/lab_inventory` 内の `deploy_apache.yml` というプレイブックに `apache` ロールを埋め込んで、'web' グループホスト（node1、node2、node3）に適用します。

```yaml
- name: Setup Apache Web Servers
  hosts: web
  become: true
  roles:
    - apache
```

### ステップ 5 - ロールの実行と検証

デザインされたWebサーバーにApacheを設定するためにプレイブックを起動します：

```bash
ansible-navigator run deploy_apache.yml -m stdout
```

#### 出力：

```plaintext
PLAY [Setup Apache Web Servers] ************************************************

TASK [Gathering Facts] *********************************************************
ok: [node2]
ok: [node1]
ok: [node3]

TASK [apache : Install Apache web server] **************************************
changed: [node1]
changed: [node2]
changed: [node3]

TASK [apache : Ensure Apache is running and enabled] ***************************
changed: [node2]
changed: [node1]
changed: [node3]

TASK [apache : Deploy custom index.html] ***************************************
changed: [node1]
changed: [node2]
changed: [node3]

RUNNING HANDLER [apache : Reload Firewall] *************************************
ok: [node2]
ok: [node1]
ok: [node3]

PLAY RECAP *********************************************************************
node1                      : ok=5    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node2                      : ok=5    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node3                      : ok=5    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

### ステップ 6 - Apacheが稼働していることを確認

プレイブックの完了後、すべてのWebノードで `httpd` が実際に稼働していることを確認します。

```bash
[rhel@control ~]$ ssh node1 "systemctl status httpd"
● httpd.service - The Apache HTTP Server
   Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2024-01-29 16:49:13 UTC; 3min 46s ago
```

```bash
[rhel@control ~]$ ssh node2 "systemctl status httpd"
● httpd.service - The Apache HTTP Server
   Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2024-01-29 16:49:13 UTC; 3min 58s ago
```

`httpd` が稼働していることを確認したら、Apache Webサーバーが適切な `index.html` ファイルを提供しているかどうかをチェックします：

```bash
[student@ansible-1 lab_inventory]$ curl http://node1
<html>
<head>
<title>Welcome to node1</title>
</head>
<body>
 <h1>Hello from node1</h1>
</body>
</html>
```


---
**ナビゲーション**
<br>
[前の演習](../1.6-templates/README.ja.md) -[次の演習](../1.8-troubleshoot/README.ja.md)

[Red Hat Enterprise Linux のための Ansible ワークショップに戻る](../README.md#section-1---ansible-engine-exercises)


