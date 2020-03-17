# 演習8 - Windwos のアプリケーション管理  

Windows の管理で結構手間になっているものの一つにアプリケーションの管理があるようです。私も良く面倒くさいという話を聞きます。  
Windows OS が提供するアプリケーションの管理であれば、演習2で行った win_feature モジュールで出来ます。
ただ、Windows の場合、3rdパーティ製のアプリケーションをインストールすることも多いと思います。
これを管理する方法として、[win_pacage](https://docs.ansible.com/ansible/latest/modules/win_package_module.html#win-package-module) モジュールがあるのですが、モジュールの Example を見ていただくと分かる通り、元来 Windows のアプリケーションはそれぞれのベンダーから CD や DVD などのメディアや独自のURLで提供されるケースが多く、Linux の yum コマンドの様に、一括したリポジトリから同一手法でアプリケーションを管理する、ということがなかなか出来ませんでした。このため、パッケージを一括した手法で管理するということがなかなか難しかった面があります。  

しかし、最近、[Chocolatey](https://chocolatey.org/) というリポジトリが登場し、Windows でもLinux同様の一括したアプリケーション管理が可能となってきました。  

凄く便利ですので、演習で確認してみましょう。♬  

### ステップ 1:

以前の演習で「iis_basic」ディレクトリなどを作成した WORKSHOP_PROJECT が存在していると思います。  

![Student Playbooks](images/8-vscode-existing-folders.png)

WORKSHOP_PROJECTセクションにカーソルを合わせ、*New Folder* ボタンをクリックします。`win_chocolatey` と入力します。  

次に、`win_chocolatey` ホルダーを右クリックして、*New File* を選択、`app_manage.yml` と入力します。  
もう一度、`win_chocolatey` ホルダーを右クリックして、*New File* を選択、`app_list.yml` と入力します。  

`app_list.yml` の Playbook 編集用のエディターが右ペインに開いていることを確認し、以下作業を行います。  

![Empty site.yml](images/8-create-win_updates.png)

## Playbook の作成

作成した site.yml を編集し、Playbook にプレイの定義といくつかのタスクを追加します。これは、Windows Update を実行するための非常に基本的な Playbook です。一般的には、更新プロセスを実行するためにはさらに多くのタスク、例えば、サービスチケットの作成、バックアップの作成、または監視の無効化などが必要になる場合があります。そういった今回の演習では含まれていません。もちろん、別途他システムを Ansible と連携、または Ansible から操作することにより、全自動で行うことも可能です。  

<!-- {% raw %} -->
```yaml
---
- hosts: windows
  name: This is my Windows patching playbook
  tasks:
    - name: Install Windows Updates
      win_updates:
        category_names: "{{ categories | default(omit) }}"
        reboot: '{{ reboot_server | default(yes) }}'
```
<!-- {% endraw %} -->

> **ヒント**
>
> **上記の説明**
>
> -   `win_updates:` このモジュールは、Windows 端末の新規パッチの確認またはインストールに使用されます。変数を使用して特定のカテゴリの更新のみをインストールするように指示しています。`reboot`属性は、必要に応じてリモートホストを自動的に再起動し再起動後も更新のインストールを続行します。 また、必要に応じて Survey を使って再起動を停止することも可能です。reboot_server 値が指定されていない場合、再起動属性をyesに設定します。変数が二つありますが、こちらは、Ansible Tower の Survey で入力します。

## 保存とコミット

改良された新しいプレイブックの完成です♪  
早速、変更を保存し、GitLabにコミットしましょう。  

`File` をクリックし、`Save` を選択。編集したファイルを保存します。  

![site.yml](images/7-win_update-playbook.png)

Source Control アイコンをクリックし (1)、変更内容例えば*Adding windows update playbook*を記述し (2)、上部の Commit ボタンをクリックします (3)。  

![Commit site.yml](images/7-win_update-commit.png)

左下の青いバーの矢印をクリックして、gitlabに同期します。  

![Push to Gitlab.yml](images/7-push.png)

コミットが完了するまでに5〜30秒かかります。 青いバーは回転を停止し、問題が0であることを確認します...　

## ジョブテンプレートの作成

Ansible Tower の GUI に戻ってプロジェクトの同期を行います。理由は・・・、もうお分かりですね？  

次に、このプレイブックを実行する新しいジョブテンプレートを作成する必要があります。*テンプレート*に移動して*追加*をクリックし、`ジョブテンプレート`を選択して新しいジョブテンプレートを作成します。

### ステップ 1:

次の値を使用してフォームに入力します。  

| キー                | 値                      | 備考 |
|--------------------|----------------------------|------|
| 名前               | Windows Updates            |      |
| 説明        |                            |      |
| ジョブタイプ           | 実行                        |      |
| インベントリー          | Windows Workshop Inventory |      |
| プロジェクト            | Ansible Workshop Project   |      |
| PLAYBOOK           | `win_updates/site.yml`     |      |
| 認証情報 | Student Account            |      |
| 制限              | windows                    |      |
| オプション            | [*] ファクトキャッシュの有効化にチェック      |      |

![Create Job Template](images/7-win_update-template.ja.jpg)

### ステップ 2:

![Save](images/at_save.ja.jpg) をクリックし、ADD SURVEY ![Add](images/at_add_survey.ja.jpg) をクリックします。
