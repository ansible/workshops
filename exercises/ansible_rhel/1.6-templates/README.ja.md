# 演習 - テンプレートを使う

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

* [ステップ 1 -  playbook 内でテンプレートを使用する](#ステップ-1----playbook-内でテンプレートを使用する)
* [ステップ 2 - チャレンジラボ](#step-2---チャレンジラボ)

Ansibleは、管理対象ホストにファイルをコピーする際、固定の内容ではなく変数に値を入力しながらコピーを行う様な事も可能です。例えば対象ホストユニークなホスト名などを含んだファイルのコピーを行うことが可能です。これを実現するのが Jinja2 テンプレートです。 Jinja2 は、Python で最も使用されているテンプレートエンジンの1つです。 (<http://jinja.pocoo.org/>)

## ステップ 1 -  playbook 内でテンプレートを使用する

利用は簡単です。まず、ファイル作成を行うための変数を含んだテンプレートファイルを作成し、テンプレートモジュールを使って対象ホストに転送するだけです。

早速演習を行ってみましょう！  
テンプレートを使って、対象ホストの motd ファイルをホスト固有のデータを含むように変更してみます。  

まず、 `~/ansible-files/` ディレクトリ内に、テンプレートファイル `motd-facts.j2` を作成します。  

<!-- {% raw %} -->
```html+jinja
Welcome to {{ ansible_hostname }}.
{{ ansible_distribution }} {{ ansible_distribution_version}}
deployed on {{ ansible_architecture }} architecture.
```
<!-- {% endraw %} -->

テンプレートファイルには、コピーされる基本テキスト（文頭の Welcome to と文末の architecture ですね♪ ）が含まれています。また、ターゲットマシンのユニークな値に置き換えられる変数がその間に入っています。  

次に、上記テンプレートを利用するための playbook `motd-facts.yml` を以下の通り作成します。場所は、 `~/ansible-files/` ディレクトリ内です。  

```yaml
---
- name: Fill motd file with host data
  hosts: node1
  become: yes
  tasks:
    - template:
        src: motd-facts.j2
        dest: /etc/motd
        owner: root
        group: root
        mode: 0644
```


  - 上記 playbook の意味を考えてみましょう  

  - 作成した playbook `motd-facts.yml` を実行してみましょう  

  - SSHで node1 にログインし、出力されるメッセージを確認してみてください  

  - node1 からログオフします  

Ansibleが変数をシステムから収集したファクト情報で変数を置き換えた上で、ファイルをコピーしていることがわかります。

## ステップ 2 - チャレンジラボ

テンプレートに1行追加して、管理対象ノードの現在のカーネルを表示してください。  

  - 「Ansible ファクト」の章で学んだコマンドを使用して、カーネルバージョンを含むファクトを見つけます。  

> **ヒント**
>
> モジュールは `setup` ですね？ `grep` を使って探してみましょう。

  - 見つかったらその変数を表示するよう、テンプレートファイルに追記しましょう

  - 再度 playbook を実行します

  - 再度 node1 にログインし、表示をチェックしてみてください


> **答えは以下の通り**


  - kernel 情報を有するファクトを見つけます

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup|grep -i kernel
       "ansible_kernel": "3.10.0-693.el7.x86_64",
```

  - `motd-facts.j2` を以下の通り更新します

<!-- {% raw %} -->
```html+jinja
Welcome to {{ ansible_hostname }}.
{{ ansible_distribution }} {{ ansible_distribution_version}}
deployed on {{ ansible_architecture }} architecture
running kernel {{ ansible_kernel }}.
```
<!-- {% endraw %} -->

  - playbook を実行します
  - node1 にログインし、表示をチェックします


うまくいきましたか？

----

[Ansible Engine ワークショップ表紙に戻る](../README.ja.md#section-1---ansible-engineの演習)
