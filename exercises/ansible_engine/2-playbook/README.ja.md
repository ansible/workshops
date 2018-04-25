# 演習 2 - 初めてのplaybook作成


まずはAnsibleｍの動きを見ていただく上でも、*playbook* を作成してみたいと思います。 playbookは 先程実行した複数の ad-hoc コマンドを、*plays* と *tasks* の複数セットに置き換えたものです。

playbookは1つまたは複数のplayに、1つまたは複数のタスクを持つことができます。*play* の目的はホストのグループをマッピングする事であり、*task* の目的はこれらのホストに対してモジュールを実行する事です。

初めてのplaybookでは、1つのplayに2つのtaskを書いていきたいと思います。


## セクション 1: ディレクトリとplaybookファイルの作成

推奨するplaybookディレクトリ構成の[ベスト・プラクティス](http://docs.ansible.com/ansible/playbooks_best_practices.html)があります。Ansibleのスキルを得て熟練される場合は、こちらを読み、理解いただくことを強くお勧めします。本日のplaybookはとても基本なものですが、入り組んだ構造から少し複雑に映るかも知れないからです。

今回は、とてもシンプルなplaybookディレクトリ構成と、そこに複数ファイルを追加する簡易な形で進めます。


*ステップ 1:* 以下のように *apache_basic* をホームディレクトリとして作成し、作成したディレクトリに移動します。

```bash
mkdir ~/apache_basic
cd ~/apache_basic
```

*ステップ 2:* `vi` または `vim` で `install_apache.yml` ファイルを作成編集します。


## セクション 2: Play の定義

現在編集中の  `install_apache.yml` に、Playを定義し、各行の内容を理解しましょう。


```yml
---
- hosts: web
  name: Install the apache web service
  become: yes
```

- `---` YAML開始の定義
- `hosts: web` はplayを実行する対象のホスト・グループをInventoryの中で定義しています。
- `name: Install the apache web service` Play内容の説明です。
- `become: yes` リモートホストでroot権限を使い実行。デフォルトはsudoですが、su、pbrun、[その他](http://docs.ansible.com/ansible/become.html) もサポート。


## セクション 3: Play内のTask追加

ここまででplayを定義しました。続けて実行する複数のtaskを追加しましょう。`task` の *t* と、`become` の *b* はインデントの位置を合わせ、垂直に揃えてください。
この記述の仕方がとても重要です。Playbook内の記述は、すべてここで示されている形式に倣う必要があります。
もしもこのPlaybookの全文を見たい場合は、この演習ページの最下部を参照してください。


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
- `- name:` playbookの実行時に標準出力されるそれぞれのtask名称
よって、出力されるに完結かつ、適切なtask名を記入してください。


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


## セクション 4: playbookの保存

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

[Click Here to return to the Ansible Linklight - Ansible Engine Workshop](../README.md)
