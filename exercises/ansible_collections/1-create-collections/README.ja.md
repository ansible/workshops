# 演習 1 - コレクションのインストールと作成

## 目次

- [目的](#objective)
- [ガイド](#guide)
    - [ステップ 1:
      コマンドラインからのコレクションのインストール](#step-1-installing-collections-from-the-command-line)
        - [演習環境の準備](#preparing-the-cgi-environment)
        - [デフォルトのコレクションパスでのインストール](#installing-in-the-default-collections-path)
        - [カスタムコレクションパスでのインストール](#instaling-in-a-custom-collections-path)
        - [コレクションの内容の検証](#inspecting-the-contents-of-the-collection)
    - [ステップ 2:
      コマンドラインからのコレクションの作成](#step-2-creating-collections-from-the-command-line)
        - [Git リポジトリーの初期化](#initializing-the-git-repository)
    - [ステップ 3:
      コレクションへのカスタムモジュールおよびプラグインの追加](#step-3-adding-custom-modules-and-plugins-to-the-collection)
    - [ステップ 4:
      コレクションへのカスタムロールの追加](#step-4-adding-custom-roles-to-the-collection)
    - [ステップ 5:
      コレクションの構築とインストール](#step-5-building-and-installing-collections)
    - [ステップ 6: ローカルでのコレクションのテスト](＃step-6-testing-collections-locally)
        - [テスト Playbook の実行](#running-the-test-playbook)
        - [ローカルコンテナーの実行](#running-the-local-container)
- [重要なこと](#takeaways)

# 目的

この演習により、ユーザーは、コレクションのインストール、作成、カスタマイズの方法について理解できるようになります。以下のトピックについて説明します。

- `ansible-galaxy` ユーティリティーを使用したコマンドラインからの Ansible
コレクションのインストールに関連する手順を紹介します。  - `ansible-galaxy`
ユーティリティーを使用した新しいコレクションの作成に関連する手順を紹介します。  -
新たに作成されたコレクション内でのカスタムロールの作成を紹介します。  - 新しく作成されたコレクションでの新しいカスタムプラグイン (基本的な
Ansible モジュール) の作成を紹介します。

# ガイド

## ステップ 1: コマンドラインからのコレクションのインストール

Ansible コレクションは、Ansible Galaxy および Red Hat Automation Hub
から検索およびインストールできます。インストール後に、コレクションはローカルで使用でき、そのプラグイン、モジュール、およびロールは、複雑な
Ansible ベースのプロジェクトにインポートして実行できます。

### 演習環境の準備

ラボに `dir_name` という名前のディレクトリーを作成し、そのディレクトリーに移動します。このディレクトリーは、演習全体で使用されます。

```bash
mkdir exercise-01
cd exercise-01
```

コレクションには、検索されるデフォルトの検索パスが 2 つあります。

- ユーザースコープパス `/home/<username>/.ansible/collections`

- システムスコープパス `/usr/share/ansible/collections`

> **ヒント**: ユーザーは、
> `ansible.cfg` ファイルの `collections_path` キーを変更するか、または環境変数 `ANSIBLE_COLLECTIONS_PATHS` を必要な
> 検索パスで設定することで、コレクションパスをカスタマイズすることができます。

### デフォルトのコレクションパスでのインストール

まず、ユーザースコープパスにコレクションをインストールする方法を説明します。簡素化するために、コレクション
[newswangerd.collection_demo](https://galaxy.ansible.com/newswangerd/collection_demo)
を使用します。これは、デモ目的で作成された基本的なコレクションです。

これには基本的なロールと非常にシンプルなモジュールが含まれており、モジュールやロールロジックに関与せずに、コレクションがどのように機能するかを理解するための良い例となります。

追加オプションを指定せずに `ansible galaxy collection install` コマンドを使用し、コレクションをインストールします。

```bash
$ ansible-galaxy collection install newswangerd.collection_demo
Process install dependency map
Starting collection install process
Installing 'newswangerd.collection_demo:1.0.10' to '/home/<username>/.ansible/collections/ansible_collections/newswangerd/collection_demo'
```

コレクションがユーザーのホームディレクトリーにインストールされ、Playbook およびロールで使用できるようになりました。

### カスタムコレクションパスでのインストール

`-p` フラグの後にカスタムインストールパスを使用して、現在の作業ディレクトリーにコレクションをインストールします。

```bash
ansible-galaxy collection install -p . newswangerd.collection_demo
```

> **注記**: コレクション検索パスに含まれていないカスタムパスにインストールする場合は、標準の警告メッセージが発行されます:
>
> ```bash
>  [WARNING]: The specified collections path '/home/gbsalinetti/Labs/collections-lab' is not part of the configured Ansible collections paths
> '/home/gbsalinetti/.ansible/collections:/usr/share/ansible/collections'. The installed collection won't be picked up in an Ansible run.
> ```

インストールされたパスは、標準のパターン `ansible_collections/<author>/<collection>` に従います。

`tree` コマンドを実行してコンテンツを検証します。

```bash
$ tree
.
└── ansible_collections
    └── newswangerd
        └── collection_demo
            ├── docs
            │   └── test_guide.md
            ├── FILES.json
            ├── MANIFEST.json
            ├── plugins
            │   └── modules
            │       └── real_facts.py
            ├── README.md
            ├── releases
            │   ├── newswangerd-collection_demo-1.0.0.tar.gz
            │   ├── newswangerd-collection_demo-1.0.1.tar.gz
            │   ├── newswangerd-collection_demo-1.0.2.tar.gz
            │   ├── newswangerd-collection_demo-1.0.3.tar.gz
            │   ├── newswangerd-collection_demo-1.0.4.tar.gz
            │   └── newswangerd-collection_demo-1.0.5.tar.gz
            └── roles
                ├── deltoid
                │   ├── meta
                │   │   └── main.yaml
                │   ├── README.md
                │   └── tasks
                │       └── main.yml
                └── factoid
                    ├── meta
                    │   └── main.yaml
                    ├── README.md
                    └── tasks
                        └── main.yml
```

### コレクションの内容の検証

コレクションには、モジュール、プラグイン、ロール、および Playbook を保持できる標準的な構造があります。

```bash
collection/
├── docs/
├── galaxy.yml
├── plugins/
│   ├── modules/
│   │   └── module1.py
│   ├── inventory/
│   └── .../
├── README.md
├── roles/
│   ├── role1/
│   ├── role2/
│   └── .../
├── playbooks/
│   ├── files/
│   ├── vars/
│   ├── templates/
│   └── tasks/
└── tests/
```

コレクション構造の簡単な説明:

- `plugins` フォルダーは、Playbook およびロールで再利用できるプラグイン、モジュール、および module_utils
  を保持します。
- `roles` フォルダーは、カスタムロールをホストしますが、すべてのコレクション Playbook は `playbooks`
  フォルダーに保存する必要があります。
- `docs` フォルダーは、コレクションのドキュメントや、コレクションおよびそのコンテンツの記述に使用されるメインの `README.md`
  ファイルに使用できます。
- `tests` フォルダーは、コレクション用に記述されたテストを保持します。
- `galaxy.yml` ファイルは、コレクションをインデックス化するために Ansible Galaxy ハブで使用されるすべてのメタデータを含む
  YAML テキストファイルです。また、コレクションの依存関係を一覧表示するためにも使用されます（ある場合）。

`ansible-galaxy collection install` でコレクションをダウンロードすると、さらに 2
つのファイルがインストールされます。

- `MANIFEST.json`: JSON 形式で追加の Galaxy メタデータを保持します。

- `FILES.json`: すべてのファイルの SHA256 チェックサムが含まれる JSON オブジェクト。

## ステップ 2: コマンドラインからのコレクションの作成

ユーザーは独自のコレクションを作成し、それらにロール、Playbook、プラグイン、およびモジュールを設定することができます。ユーザー定義のコレクションのスケルトンは、手動で作成するか、`ansible-galaxy
collection init` コマンドで作成することができます。これにより、後でカスタマイズできる標準スケルトンが作成されます。

以下のコレクションを作成します。

```bash
ansible-galaxy collection init --init-path ansible_collections redhat.workshop_demo_collection
```

`--init-path` フラグは、スケルトンが初期化されるカスタムパスを定義するために使用されます。
コレクション名は常にパターン `<namespace.collection>` に従います。上記の例では、
`redhat` namespace に `workshop_demo_collection` を作成します。

このコマンドは、以下のスケルトンを作成しました。

```bash
$ tree ansible_collections/redhat/workshop_demo_collection/
ansible_collections/redhat/workshop_demo_collection/
├── docs
├── galaxy.yml
├── plugins
│   └── README.md
├── README.md
└── roles
```

スケルトンは実際には最小限です。テンプレートの README ファイルのほかに、Galaxy メタデータを定義するテンプレート `galaxy.yml`
ファイルが作成されます。

### Git リポジトリーの初期化

Galaxy でコレクションを公開する場合は、コレクションで Git リポジトリーを初期化することが推奨されます。

```bash
cd ansible_collections/redhat/workshop_demo_collection && git init .
```

変更すると、`git add` を使用してステージングエリアにファイルが追加され、`git commit` コマンドでコミットされます。

GitHub でコレクションを公開するには、リモートを追加する必要があります。

```bash
git remote add origin https://github.com/<user>/workshop_demo_collection.git
```

`workshop_demo_collection` リポジトリーは GitHub
にすでに存在している必要があります。新しいリポジトリーを作成するには、公式の GitHub
[ドキュメント](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-new-repository).
に従ってください。

## ステップ 3: コレクションへのカスタムモジュールおよびプラグインの追加

コレクションは、さまざまな種類のプラグインおよびモジュールでカスタマイズできます。完全な一覧は、`plugins` フォルダーの `README.md`
ファイルを参照してください。

このワークショップでは、最小限の *Hello World* モジュールを作成し、`plugins/modules`
ディレクトリーにインストールします。

まず、`plugins/modules` ディレクトリーを作成します。

```bash
cd ansible_collections/redhat/workshop_demo_collection
mkdir plugins/modules
```

新しいフォルダーに `demo_hello.py` モジュールを作成します。モジュールコードは、この演習の `solutions/modules`
フォルダーにあります。

```bash
cp <path_to_workshop_repo>/workshops/exercises/ansible_collections/1-create-collections/modules/demo_hello.py plugins/modules/
```

`demo_hello` モジュールは、カスタム定義されたユーザーにさまざまな言語で Hello
と言います。時間をかけてモジュールコードを確認し、その動作を理解してください。

```bash
#!/usr/bin/python


ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: demo_hello
short_description: A module that says hello in many languages
version_added: "2.8"
description:
  - "A module that says hello in many languages."
options:
    name:
        description:
          - Name of the person to salute. If no value is provided the default
            value will be used.
        required: false
        type: str
        default: John Doe
author:
    - Gianni Salinetti (@giannisalinetti)
'''

EXAMPLES = '''
# Pass in a custom name
- name: Say hello to Linus Torwalds
  demo_hello:
    name: "Linus Torwalds"
'''

RETURN = '''
fact:
  description: Hello string
  type: str
  sample: Hello John Doe!
'''

import random
from ansible.module_utils.basic import AnsibleModule


FACTS = [
    "Hello {name}!",
    "Bonjour {name}!",
    "Hola {name}!",
    "Ciao {name}!",
    "Hallo {name}!",
    "Hei {name}!",
]


def run_module():
    module_args = dict(
        name=dict(type='str', default='John Doe'),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result = dict(
        changed=False,
        fact=''
    )

    result['fact'] = random.choice(FACTS).format(
        name=module.params['name']
    )

    if module.check_mode:
        return result

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
```

Ansible モジュールは基本的に、`run_module()` と呼ばれる最小限の関数で作成され、実行される AnsibleModule
クラスの実装になります。ご覧のとおり、モジュールには、プレーンな Python 実行可能ファイルのような `main()`
関数があります。ただし、個別に実行することは意図されていません。

## ステップ 4: コレクションへのカスタムロールの追加

この演習の最後のステップは、カスタムコレクション内のロール作成に重点を置いています。以前のモジュールを使用して、index.html
内でグリーティングを動的に生成し、podman で OCI
イメージ内にビルドする基本的なロールをデプロイします。イメージは最終的にカスタマイズ可能なプライベートレジストリーにプッシュされます。

> **ヒント**: ラボの速度を上げる場合は、演習 `solutions/roles` フォルダーから完了したロールをコピーできます。

`ansible-galaxy init` コマンドを使用して、新しいロールスケルトンを生成します。

```bash
ansible-galaxy init --init-path roles demo_image_builder
```

`roles/demo_image_builder/tasks/main.yml` ファイルに以下のタスクを作成します。

```yaml
---
# tasks file for demo_image_builder
- name: Ensure podman is present in the host
  dnf:
    name: podman
    state: present
  become: true

- name: Generate greeting and store result
  demo_hello:
    name: "{{ friend_name }}"
  register: demo_greeting

- name: Create build directory
  file:
    path: "{{ build_dir_path }}"
    state: directory
    mode: 0755

- name: Copy Dockerfile
  copy:
    src: files/Dockerfile
    dest: "{{ build_dir_path }}"
    mode: 0644

- name: Copy custom index.html
  template:
    src: templates/index.html.j2
    dest: "{{ build_dir_path }}/index.html"
    mode: 0644

- name: Build and Push OCI image
  podman_image:
    name: demo-nginx
    path: "{{ build_dir_path }}"
    build:
      annotation:
        app: nginx
        function: demo
        info: Demo app for Ansible Collections workshop
      format: oci
    push: true
    force: true
    push_args:
      dest: "{{ image_registry }}/{{ registry_username }}"
```

コレクションにインストールされている `demo_hello` モジュールを使用して、greeting 文字列を生成することに注意してください。

> **注記**: コレクションロールが同じコレクション namespace のモジュールを呼び出すと、モジュールは自動的に解決されます。

`roles/demo_image_builder/defaults/main.yml` に以下の変数を作成します。

```yaml
---
# defaults file for demo_image_builder
friend_name: "John Doe"
build_dir_path: "/tmp/demo_nginx_build"
image_registry: "quay.io"
registry_username: ""
```

`roles/demo_image_builder/files/` フォルダーでビルドプロセスで使用される Dockerfile を作成します。

```bash
cat > roles/demo_nginx/files/ << EOF
FROM nginx
COPY index.html /usr/share/nginx/html
EOF
```

`roles/demo_image_builder/templates/` フォルダーで Jinja2 テンプレートとして動作する
index.html.j2 ファイルを作成します。

```bash
cat > roles/demo_image_builder/templates/index.html.j2 << EOF
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title>Ansible Collections Workshop</title>
  <meta name="description" content="Demo Nginx">
  <meta name="author" content="gsalinet@redhat.com">

  <link rel="stylesheet" href="css/styles.css?v=1.0">

</head>

<body>
  <h1>
    {{ demo_greeting.fact }}
  </h1>
</body>
</html>
EOF
```

スケルトンは、完全な構造ファイルとフォルダーを生成します。未使用のものはクリーンアップできます。

```bash
rm -rf roles/demo_image_builder/{handlers,vars,tests}
```

`roles/demo_image_builder/meta/main.yml` ファイルをカスタマイズして、Galaxy
メタデータおよびロールの潜在的な依存関係を定義します。以下の最小限のコンテンツのサンプルを使用します。

```yaml
galaxy_info:
  author: Ansible Automation Platform Hackathon Team
  description: Basic builder role based on podman
  company: Red Hat

  license: Apache-2.0

  min_ansible_version: 2.8


  platforms:
    - name: Fedora
      versions:
      - 31
      - 32
      - 33

  galaxy_tags: ["demo", "podman"]

dependencies: []
```

## ステップ 5: コレクションの構築とインストール

作成タスクが完了したら、コレクションをビルドし、ローカルにインストールしたり、Galaxy にアップロードしたりできる .tar.gz
ファイルを生成できます。

コレクションフォルダーから、以下のコマンドを実行します。

```bash
ansible-galaxy collection build
```

上記のコマンドは、`redhat-workshop_demo_collection-1.0.0.tar.gz` ファイルを作成します。セマンティック
x.y.z バージョンニングに注意してください。

作成後、ファイルを `COLLECTIONS_PATH` にインストールし、ローカルでテストできます。

```bash
ansible-galaxy collection install redhat-workshop_demo_collection-1.0.0.tar.gz
```

デフォルトでは、コレクションは `~/.ansible/collections/ansible_collections`
フォルダーにインストールされます。これで、コレクションをローカルでテストできるようになりました。

## ステップ 6: ローカルでのコレクションのテスト

`exercise-01/collections_test` フォルダーを作成し、ローカルテストを実行します。

```bash
cd ..
mkdir collections_test
```

以下の内容で基本的な `playbook.yml` ファイルを作成します。

```bash
cat > playbook.yml << EOF
---
- hosts: localhost
  remote_user: root
  vars:
    image_registry: quay.io
    registry_username: <YOUR_USERNAME>
    friend_name: Heisenberg
  tasks:
    - import_role:
        name: redhat.workshop_demo_collection.demo_image_builder
EOF
```

`<YOUR_USERNAME>` フィールドを有効な quay.io ユーザー名に置き換えます。
テスト Playbook を実行する前に、レジストリーに対して認証を行うための有効な認証トークンがあることを確認します。以下のコマンドを実行し、`~/.docker/config.json` ファイルに保存されているトークンを生成する有効な認証情報を渡すことで、認証することができます。

```bash
podman login quay.io
```

### テスト Playbook の実行

テスト Playbook を実行します。一部のタスクには権限昇格が必要なため、`-K` オプションを使用して sudo 経由で認証します。

```bash
$ ansible-playbook playbook.yml -K
BECOME password:
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [localhost] **************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ********************************************************************************************************************************************************************************************
ok: [localhost]

TASK [redhat.workshop_demo_collection.demo_image_builder : Ensure podman is present in the host] ******************************************************************************************************************
ok: [localhost]

TASK [redhat.workshop_demo_collection.demo_image_builder : Generate greeting and store result] ********************************************************************************************************************
ok: [localhost]

TASK [redhat.workshop_demo_collection.demo_image_builder : Create build directory] ********************************************************************************************************************************
ok: [localhost]

TASK [redhat.workshop_demo_collection.demo_image_builder : Copy Dockerfile] ***************************************************************************************************************************************
ok: [localhost]

TASK [redhat.workshop_demo_collection.demo_image_builder : Copy custom index.html] ********************************************************************************************************************************
changed: [localhost]

TASK [redhat.workshop_demo_collection.demo_image_builder : Build and Push OCI image] ***************************************************************************************************************************************
changed: [localhost]

PLAY RECAP ********************************************************************************************************************************************************************************************************
localhost                  : ok=7    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

### ローカルコンテナーの実行

podman を使用してビルドされたコンテナーイメージをローカルでテストし、コレクションのモジュールおよびロールの予想される動作を示します。

```bash
podman run -d --rm -d -p 8080:80 localhost/demo-nginx
```

nginx Web サーバーをテストし、ボディーセクションを検査して、h1 セクションで生成された文字列を見つけます。

```bash
$ curl localhost:8080
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title>Ansible Collections Workshop</title>
  <meta name="description" content="Demo Nginx">
  <meta name="author" content="gsalinet@redhat.com">

  <link rel="stylesheet" href="css/styles.css?v=1.0">

</head>

<body>
  <h1>
    Hei Heisenberg!
  </h1>
</body>
</html>
```

# 重要なこと

- コレクションは、Red Hat Automation Hub の Galaxy
からインストールできます。デフォルトのコレクション検索パスまたはカスタムパスを使用できます。

- コレクションは、`ansible-galaxy collection init`
コマンドを使用して作成できます。ユーザーは、ニーズとビジネスロジックに合わせてコレクションコンテンツを開発できます。

- コレクションプラグインは、あらゆる種類の Ansible
プラグインまたはモジュールになります。多くの場合、モジュールはコレクション内で開発され、メインの Ansible
アップストリームから自律的なライフサイクルを作成します。

- コレクションロールは、ローカルコレクションプラグインおよびモジュールを使用できます。

----
**ナビゲーション**
<br>
[次の演習](../2-collections-from-playbook)

[Click here to return to the Ansible for Red Hat Enterprise Linux
Workshop](../README.md)
