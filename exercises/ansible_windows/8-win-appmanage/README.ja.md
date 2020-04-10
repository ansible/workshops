# 演習8 - Windwos のアプリケーション管理  

Windows を Ansible で管理するもう一つの大きなモチベーションはアプリケーションの管理の自動化です。  

Windows 上のアプリケーションを Ansible で管理する方法はいくつかあります。例えば、OS が提供するアプリケーションの管理であれば、演習2で行った win_feature モジュールが利用可能です。逆に OS 提供の機能ではなく、3rd パーティ製のアプリケーションの場合、[win_pacage](https://docs.ansible.com/ansible/latest/modules/win_package_module.html#win-package-module) というモジュールがあります。ただ、モジュールの Example を見ていただくと分かる通り、元来 Windows のアプリケーションはそれぞれのベンダーから CD や DVD などのメディアや msi、独自の URL で提供されるケースが多く、Linux の yum コマンドの様に、一括したリポジトリから同一手法でアプリケーションを管理する、ということがなかなか出来ませんでした。このため、パッケージの一括管理がなかなか難しかった面が否めませんでした。  

しかし、最近、[Chocolatey](https://chocolatey.org/) というリポジトリが登場し、Windows でもLinux同様の一括したアプリケーション管理が可能となってきました。[パッケージ](https://chocolatey.org/packages)も Chrome、Firefox、JRE、Putty、Adbe Reader、MS Officeなどなど非常に多彩です。 

凄く便利ですので、演習で確認してみましょう。♬  

### 準備  

Chocolatey 利用には、Windows ホストへ chocolatey ソフトをインストールする必要があります。ここもAnsibleで自動化してみましょう。演習2 を参考に、PowerShell のアドホックコマンド `win_shell` を使って以下を実行してください。  

Ansible Tower で、**「インベントリー」→「Windows Workshop Inventory」→「ホスト」**  

で、**「student1-win1」** にチェックを入れて　**「コマンドの実行」** をクリックします。  

コマンドの実行画面で、以下を入力して`起動` をクリックします。  

**モジュール：**  
　win_shell

**引数**  
　Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

**マシンの認証情報**  
　Student Account

これで、Windows ホスト上で Chocolatey が利用できるようになりました。準備完了です！！  

### ステップ 1:

以前の演習で「iis_basic」ディレクトリなどを作成した WORKSHOP_PROJECT が存在していると思います。  

![Student Playbooks](images/8-vscode-existing-folders.ja.jpg)

WORKSHOP_PROJECTセクションにカーソルを合わせ、*New Folder* ボタンをクリックします。`win_chocolatey` と入力します。  

次に、`win_chocolatey` ホルダーを右クリックして、*New File* を選択、`app_manage.yml` と入力します。  
もう一度、`win_chocolatey` ホルダーを右クリックして、*New File* を選択、`app_list.yml` と入力します。  

以下のようになっていれば OK です。♬  

![Empty site.yml](images/8-create-list-empty.ja.jpg)

## Playbook の作成

今から二つの Playbook を作成します。

**1. app_list.yml:**  
　chocolatey 経由で管理されているアプリケーションの一覧を表示します。  
**2. app_manage.yml:**  
　アプリケーションの追加、削除、更新を行います。  

まず、1から作成してみましょう。  
`app_list.yml` の Playbook 編集用のエディターが右ペインに開いていることを確認し、以下作業を行います。  

<!-- {% raw %} -->
```yaml
---
- hosts: windows
  name: This is my Windows application list playbook

  tasks:
  - name: Gather facts from chocolatey
    win_chocolatey_facts:

  - name: Displays the Packages
    debug:
      var: ansible_chocolatey.packages
```
<!-- {% endraw %} -->

![app_list.yml](images/8-create-list.ja.jpg)

> **ヒント**
>
> `win_chocolatey_facts:` chocolatey で管理するアプリケーションに関する情報を取得するモジュールです。今回は、アプリケーションインストール前後で動作させてみて、インストールされたパッケージの差異を確認します。  


次に、`app_manage.yml` をクリックして、Playbook を以下のように編集してください。    

<!-- {% raw %} -->
```yaml
---
- hosts: windows
  name: his is my Windows application management playbook

  tasks:
  - name: Install Chrome
    win_chocolatey:
      name: googlechrome
      state: present
```
<!-- {% endraw %} -->

![app_manage.yml](images/8-create-mamage.ja.jpg)

> **ヒント**
>
> `win_chocolatey:` chocolatey リポジトリと連携してアプリケーションを追加、削除、更新するモジュールです。今回はほんの一例として Googoe Chrome をインストールしてみました。他にも、`name` に `jre8` を指定すると、Javaのランタイム、そのほか、`putty`、`vscode`などと記述すれば、それぞれのアプリケーションを管理することが可能です。  

## 保存とコミット

chocolatey でアプリケーション一覧を表示させる Playbook 及び、アプリケーションの管理を行う Playbook の完成です♪  
早速、変更を保存し、GitLabにコミットしましょう。やり方は・・・、もうわかりますね？  

## ジョブテンプレートの作成

新しい Playbook を作成しましたので、Ansible Tower の GUI に戻ってプロジェクトの同期を行ってください。  
次に、このプレイブックを実行する新しいジョブテンプレートを作成する必要があります。*テンプレート*に移動して*追加*をクリックし、`ジョブテンプレート`を選択して新しいジョブテンプレートを作成します。

### 1. app_list.yml 用のジョブテンプレート作成  

次の値を使用してフォームに入力します。  

| キー                | 値                      | 備考 |
|--------------------|----------------------------|------|
| 名前               |Windows アプリケーション取得           |      |
| 説明        |                            |      |
| ジョブタイプ           | 実行                        |      |
| インベントリー          | Windows Workshop Inventory |      |
| プロジェクト            | Ansible Workshop Project   |      |
| PLAYBOOK           | `chocolatey/app_list.yml`     |      |
| 認証情報 | Student Account            |      |
| 制限              | windows                    |      |
| オプション            | [*] ファクトキャッシュの有効化にチェック      |      |

![Create Job Template](images/8-win_applist-template.ja.jpg)

保存をクリックします。  

### 2. app_manage.yml 用のジョブテンプレート作成  

同様にして、アプリケーション管理のジョブテンプレートを作成します。  

値は下記参照ください。    

| キー                | 値                      | 備考 |
|--------------------|----------------------------|------|
| 名前               |Windows アプリケーション管理|      |
| 説明        |                            |      |
| ジョブタイプ           | 実行                        |      |
| インベントリー          | Windows Workshop Inventory |      |
| プロジェクト            | Ansible Workshop Project   |      |
| PLAYBOOK           | `chocolatey/app_manage.yml`     |      |
| 認証情報 | Student Account            |      |
| 制限              | windows                    |      |
| オプション            | [*] ファクトキャッシュの有効化にチェック      |      |

![Create Job Template](images/8-win_appmanage-template.ja.jpg)

### Playbook の起動

作成した Playbook を以下の順番に実行してみて、表示内容を確認してみましょう♬  

1. `Windows アプリケーション一覧取得` ジョブテンプレートの起動
2. `Windows アプリケーション管理` ジョブテンプレートの起動
3. `Windows アプリケーション一覧取得` ジョブテンプレートの起動

どうなりましたでしょうか？Chromeは追加でインストールされましたか？  
インストールされると、以下のように表示されると思います。  

![Create Job Template](images/8-chrome-installed.ja.jpg)

今回は演習を簡略化するため変数は使いませんでしたが、アプリケーション管理のところで、state オプションを変数化し、present/absent/latest を選択できるようにしておくと追加、削除、更新が実行時に選択出来て便利かもしれません。また、アプリケーションの一覧をcsv化して、そのファイルを読み込んできて複数のアプリケーションを一気にインストールなどということももちろん可能です。便利ですね。♬  

これでオプションのハンズオンも終了です！お疲れさまでした！！  
