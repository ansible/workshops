**他の言語で読む**:  
<br>![uk](../../../images/uk.png) [English](README.md), ![japan](../../../images/japan.png) [日本語](README.ja.md), ![france](../../../images/fr.png) [Français](README.fr.md)  
<br>

---

# セクション 1 – Playbook の作成

`win_updates` モジュールは、Windows Update の確認またはインストールを行います。組み込みの Windows Update サービスを使用するため、WSUS や Microsoft Update サーバーなどのバックエンドが必要です。  
サーバーの Windows Update 設定が「自動ダウンロードのみ」に設定されている場合、このモジュールを使用して `search` で更新を事前取得できます。  
また、特定の更新だけを許可（ホワイトリスト）または禁止（ブラックリスト）することも可能です。例：特定のセキュリティ更新のみをインストール。

ここでは、前の演習と同じ流れで新しい Playbook を作成します。

---

## ステップ 1 – Playbook ファイルを作成

Visual Studio Code で：

1. **Explorer** ビューで、以前に `iis_basic` を作成した *student#* セクションを探します。  
2. **WORKSHOP_PROJECT** フォルダにカーソルを合わせ、**New Folder** ボタンをクリック。`win_updates` と入力し Enter。  
3. `win_updates` フォルダを右クリックし、**New File** を選択。`site.yml` と入力し Enter。  

空のエディタペインが開き、Playbook を作成できます。

![Empty site.yml](images/7-create-win_updates.png)

---

# セクション 2 – Playbook の記述

`site.yml` を編集して以下を追加します。

~~~yaml
---
- hosts: windows
  name: これは Windows パッチ適用 Playbook です
  tasks:
    - name: Windows Update をインストール
      win_updates:
        category_names: "{{ categories | default(omit) }}"
        reboot: "{{ reboot_server | default(true) }}"
~~~

> **注意**  
> - `win_updates`: 更新の確認またはインストールを行います。  
> - `category_names`: 変数を使用して、特定カテゴリのみの更新に制限します。  
> - `reboot`: `true` の場合、必要に応じて自動的に再起動し、処理を続行します。Survey 変数で制御可能。

---

# セクション 3 – 保存とコミット

1. VS Code で **File → Save All** をクリック。  

![site.yml](images/7-win_update-playbook.png)

2. **Source Control** アイコン (1) をクリックし、コミットメッセージ（例：*Windows update Playbook を追加*）を入力 (2)、上のチェックボックスをクリック (3)。  

![Commit site.yml](images/7-win_update-commit.png)

3. 左下の青いバーの矢印をクリックして GitLab にプッシュ。

![Push to Gitlab.yml](images/7-push.png)

---

# セクション 4 – ジョブテンプレートの作成

**automation controller** で：

1. **Projects** に移動し、新しい Playbook が表示されるようにプロジェクトを再同期。  
2. **Templates** に移動。  
3. **Create template** をクリックし、**Create job template** を選択。  

フォームを以下の値で入力：

| 項目                  | 値                              |
|-----------------------|---------------------------------|
| **Name**              | Windows Updates                 |
| **Description**       | (任意)                          |
| **Job Type**          | Run                             |
| **Inventory**         | Windows Workshop Inventory      |
| **Project**           | Ansible Workshop Project        |
| **Playbook**          | `win_updates/site.yml`          |
| **Execution Environment** | Default execution environment |
| **Credentials**       | Student Account                 |
| **Limit**             | windows                         |
| **Options**           | Enable fact storage             |

![Create Job Template](images/7-win_update-template.png)

**Create job template** をクリック。

---

## サーベイの追加

1. **Windows Updates** ジョブテンプレートページで、**Survey** タブを開き、**Create survey question** をクリック。  
2. 1つ目の質問を入力：

| 項目                  | 値                                                                                                               |
|-----------------------|------------------------------------------------------------------------------------------------------------------|
| **Question**          | Which categories to install?                                                                                     |
| **Description**       | (Optional)                                                                                                       |
| **Answer Variable Name** | categories                                                                                                     |
| **Answer Type**       | Multiple Choice (multiple select)                                                                                |
| **Multiple Choice Options** | Application<br>Connectors<br>CriticalUpdates<br>DefinitionUpdates<br>DeveloperKits<br>FeaturePacks Guidance<br>SecurityUpdates<br>ServicePacks<br>Tools<br>UpdateRollups<br>Updates |
| **Default option**    | CriticalUpdates<br>SecurityUpdates                                                                               |
| **Options**           | Required                                                                                                         |

![Category Survey Form](images/7-category-survey.png)

**Create survey question** をクリック。

3. 2つ目の質問を入力：

| 項目                  | 値                                     |
|-----------------------|----------------------------------------|
| **Question**          | Reboot after install?                  |
| **Description**       | (Optional)                             |
| **Answer Variable Name** | reboot_server                        |
| **Answer Type**       | Multiple Choice (single select)        |
| **Multiple Choice Options** | Yes<br>No                        |
| **Default option**    | Yes                                    |
| **Options**           | Required                               |

![Reboot Survey Form](images/7-reboot-survey.png)

4. **Create survey question** をクリック。  
5. ジョブテンプレートページで **Survey Enabled** をオン。

---

# セクション 5 – Playbook の実行

1. automation controller の **Templates** に移動。  
2. **Windows Updates** ジョブテンプレートを見つけ、**Launch** ボタン（ロケットアイコン）をクリック。  
3. プロンプトで：  
   - 更新カテゴリを選択。  
   - *Reboot after install?* に **Yes** を選択。  
   - **Next** をクリックし、**Launch** をクリック。  

ジョブの出力ページに移動し、リアルタイムで進行状況を確認できます。

---

[Ansible for Windows Workshop に戻る](../README.md)

