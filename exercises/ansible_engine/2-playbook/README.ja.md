# Exercise 2 - 初めてのplaybook作成


この演習では *playbook* を作成してみましょう。
playbookは 先程実行した複数の ad-hoc コマンドで利用した情報を、*plays* と *tasks* のセットにし、ファイルへ置き換えたものです。

playbookは1つまたは複数のplayに、1つまたは複数のタスクを持つことができます。

 - *play* の目的はホストのグループをマッピングする事です。その他にも変数の定義やPlaybook全体の挙動に関する設定を行います。
 - *task* の目的はこれらのホストに対してモジュールを実行する事です。

この演習のplaybookでは、1つのplayに2つのtaskを書いていきたいと思います。


## Section 1: ディレクトリとplaybookファイルの作成

Ansibleには、playbookディレクトリ構成の[ベスト・プラクティス](http://docs.ansible.com/ansible/playbooks_best_practices.html)があります。本演習を終えてAnsibleのスキルを更に高めたい方はこちらを読んでください。やや複雑な箇所もありますので、はじめての方はまず本演習を終えて基礎的な利用方法を理解してください。

今回は、とてもシンプルなplaybookディレクトリ構成と、そこに複数ファイルを追加する簡易な形で進めます。


*ステップ 1:* 以下のように *apache_basic* をホームディレクトリとして作成し、作成したディレクトリに移動します。

```bash
mkdir ~/apache_basic
cd ~/apache_basic
```

*ステップ 2:* `vi` または `vim` で `install_apache.yml` ファイルを作成編集します。


## Section 2: Play の定義

現在編集中の  `install_apache.yml` に、Playを定義し、各行の内容を理解しましょう。


```yml
---
- hosts: web
  name: Install the apache web service
  become: yes
```

- `---` YAML開始を定義
- `hosts: web` はこのPlaybookを実行する対象のグループを指定しています。グループ名はInvenotryファイルで定義されています。
- `name: Install the apache web service` Playに名称を設定しています。任意の名称設定が可能です。名称を付けず、スキップすることもできます。
- `become: yes` リモートホストでroot権限を使い実行するためのオプションを指定しています。デフォルトはsudoですが、su、pbrun、[その他](http://docs.ansible.com/ansible/become.html) もサポートしています。


## Section 3: Play内のTask追加

ここまででplayを定義しました。
続けて実行する複数のtaskを追加しましょう。
このあとに記述する`task` の *t* と、先ほどのplayで記載した`become` の *b* が、インデントで同じ位置に来るように調整してください。
この記述の仕方がとても重要です。

Playbook内の記述は、すべてここで示されている形式に倣う必要があります。
この演習で作成するPlaybookの全文を確認したい場合は、この演習ページの最下部を参照してください。


```yml
  tasks:
    - name: install apache
      yum:
        name: httpd
        state: present
     
    - name: start httpd
      service:
        name: httpd
        state: started
```

- `tasks:` 1つまたは複数のtask定義がされることを示す
- `- name:` playbookの実行時に標準出力されるそれぞれのtask名称です。簡潔かつ適切なtask名を記入します。


```yml
    yum:
      name: httpd
      state: present
```


- これらの3行は httpd をインストールするため Ansible の *yum* モジュールを呼び出しています。
yum モジュールの全オプションを確認するには[こちらをクリック](http://docs.ansible.com/ansible/yum_module.html)


```yml
    service:
      name: httpd
      state: started
```

- 次の複数行は、httpd サービスを開始するため、*service*  モジュールを呼び出しています。このモジュールはリモートホストのサービスを制御する際使うのに適してます。
service モジュールの全オプションを確認するには[こちらをクリック](http://docs.ansible.com/ansible/service_module.html)


## Section 4: playbookの保存

playbookを書き終えたら、保存しましょう。

`vi` または `vim`にて、`write/quit` を使用(例: Escキー押下後、wq!実行)し、playbookを保存します。

これにより、playbook `install_apache.yml` が完成です。自動化準備OKとなります。

---
**NOTE**
Ansible (実際にはYAML) はインデントやスペースの形式が少し特殊かもしれません。後ほど余計な混乱を来さぬよう [YAML シンタックス](http://docs.ansible.com/ansible/YAMLSyntax.html) を、その際に完成したplaybookを傍らに置きながらご覧いただき、スペースやアラインメントをご確認いただくことをお勧めいたします。


---

```yml
---
- hosts: web
  name: Install the apache web service
  become: yes

  tasks:
    - name: install apache
      yum:
        name: httpd
        state: present

    - name: start httpd
      service:
        name: httpd
        state: started
```
---


## Section 5: playbookの実行

作成したPlaybookを実行しましょう。Playbookの実行には`ansible-playbook`コマンドを利用します。実行する前に`--syntax-check`オプションで構文をチェックしてみましょう。もしエラーが出る場合はYAMLの定義にミスがあります。インデントの位置などを確認してください。

```bash
ansible-playbook install_apache.yml --syntax-check
```

ではいよいよ実行です。

```
ansible-playbook install_apache.yml
```

正常に終了したら、ブラウザで2台のサーバーへアクセスしてください。もしエラーが出る場合には、スペルミスなどが考えられるますので確認・修正して再度`ansible-playbook`コマンドを実行してください。


## Section 6: 設定を削除するplaybookの作成と実行

先程作成した`install_apache.yml`をコピーして`uninstall_apache.yml`を作成して実行してください。ここでは詳細な手順は解説しませんが以下にヒントを記載します。

- yumモジュールでパッケージを削除するには `state: absent` とする。
- serviceモジュールでサービスを停止するには `state: stopped` とする。
- 実行する順番に気をつけてください。

```
ansible-playbook uninstall_apache.yml
```

[Click Here to return to the Ansible Linklight - Ansible Engine Workshop](../README.ja.md)
