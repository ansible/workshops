# 演習 2.6 - ワークフロー

# Ansible Tower ワークフロー

Ansible Tower の主要な新機能としてバージョン 3.1 からワークフローが導入されました。ワークフローの基本的な考え方は、複数のジョブテンプレートをリンクし実行できることです。各ジョブテンプレートの実行は、例えば以下の様な実行条件を付与することができます。  

  - ジョブテンプレート A が成功すると、ジョブテンプレート B が自動的に実行されます  

  - ただし、失敗した場合は、ジョブテンプレート C が実行されます  

また、ワークフローはジョブテンプレートに限定されず、プロジェクトまたはインベントリの更新を含めることもできます  

これにより、Tower の新しいアプリケーションが可能になります。異なるジョブテンプレートを相互に構築できます。たとえば、ネットワーキングチームは、独自のコンテンツを備えたプレイブックを独自のGitリポジトリに作成し、独自のインベントリをターゲットにしますが、運用チームには独自のリポジトリ、プレイブック、およびインベントリがあります。

このラボでは、ワークフローの設定方法を学びます。

## ラボシナリオ  

組織には以下の2つの部門があります。  

  - 自分の Git リポジトリで Playbook を開発しているWeb運用チーム

  - Git リポジトリで Tomcat 用の JSP Web アプリケーションを開発するチーム

新しい Tomcat サーバーをデプロイする必要がある場合、以下の 2 つのことを行う必要があります  

  - Tomcat をインストールし、ファイアウォールを開いて、Tomcatサービスを開始する必要があります  

  - 最新の Web アプリケーションを展開する必要があります  

Playbook、JSP ファイルなど、必要なものはすべて Git リポジトリーに存在します。それを利用してラボを行います。  

> **メモ**
>
> シナリオでは、2 つの異なる Git リポジトリの利用を想定していますが、このラボでは同じリポジトリの2つの異なるブランチにアクセスしています  

## プロジェクトの設定

先のラボで実施した通り、まずはプロジェクトに Git リポジトリを登録する必要があります。必要な情報は以下です。ご自身で設定してみてください。  

> **注意**
> 
> このラボは admin アカウントで実施ます。 **wweb** ユーザーでログインしている場合は、ログアウトして **admin** でログインしなおしてください！**  

- web オペレーションのためのプロジェクトを作成します  

  - 名前は **Webops Git Repo** にしましょう  

  - SCM アクセス先は **https://github.com/ansible/workshop-examples.git** です  

  - **SCM BRANCH/TAG/COMMIT** は **webops** とします  

- アプリケーション開発者向けのプロジェクトを作成します。  

  - 名前は **Webdev Git Repo** にしましょう  

  - SCM アクセス先は **https://github.com/ansible/workshop-examples.git** です

  - **SCM BRANCH/TAG/COMMIT** は **webdev**
 
 
> **回答は以下の通り**

- Web 運用者用のプロジェクトを作成します。プロジェクトは、緑色のプラスボタンをクリックし、以下の値を入力します。  
  
    - **名前** Webops Git Repo  
  
    - **組織** Default  
  
    - **SCM タイプ** Git  
  
    - **SCM URL:** https://github.com/ansible/workshop-examples.git  

    - **SCM BRANCH/TAG/COMMIT** webops  
  
    - **SCM 更新オプション** 全てにチェックします  

- **保存**をクリックします    

- Create the project for the application developers. In the **Projects** view click the green plus button and fill in:
  
    - **名前** Webdev Git Repo
  
    - **組織** Default
  
    - **SCM タイプ** Git
  
    - **SCM URL** https://github.com/ansible/workshop-examples.git
  
    - **SCM BRANCH/TAG/COMMIT** webdev

    - **SCM 更新オプション** 全てにチェックします 

- **保存**をクリックします  

## ジョブテンプレートの作成

最終目標はワークフローの作成ですが、まず、通常のジョブテンプレートを作成する必要があります。

  - **テンプレート** を選択し、色のプラスボタンをクリックして、**Job Template**を選択します
    
      - **名前** Tomcat Deploy
    
      - **ジョブタイプ** 実行
    
      - **インベントリー** Workshop Inventory
    
      - **プロジェクト** Webops Git Repo
    
      - **PLAYBOOK** `rhel/webops/tomcat.yml`
    
      - **認証情報** Workshop Credentials  
    
      - **オプション** 権限昇格の有効化にチェックを入れます  

  - **保存**をクリック

  - 上記の内容をアプリチームに対して繰り返します。**テンプレート** を選択し、色のプラスボタンをクリックして、**ジョブテンプレート**を選択します  
    
      - **名前** Web App Deploy
    
      - **ジョブタイプ** 実行
    
      - **インベントリー** Workshop Inventory
    
      - **プロジェクト** Webdev Git Repo
    
      - **PLAYBOOK:** `rhel/webdev/create_jsp.yml`
    
      - **認証情報** Workshop Credentials  
    
      - **オプション** 権限昇格の有効化にチェックを入れます  

  - **保存**をクリック

> **ヒント**  
> 
> Playbook の中身をご覧になりたい方は、 Github URL を確認して、適切なブランチに切り替えてご覧ください。  

## ワークフローの設定

And now you finally set up the workflow. Workflows are configured in the **Templates** view, you might have noticed you can choose between **Job Template** and **Workflow Template** when adding a template so this is finally making sense.

  - Go to the **Templates** view and click the the green plus button. This time choose **Workflow Template**
    
      - **NAME:** Deploy Webapp Server
    
      - **ORGANIZATION:** Default

  - Click **SAVE**

  - Now the **WORKFLOW VISUALIZER** button becomes active, click it to start the graphical editor.

  - Click on the **START** button, a new node opens. To the right you can assign an action to the node, you can choose between **JOBS**, **PROJECT SYNC** and **INVENTORY SYNC**.

  - In this lab we’ll link Jobs together, so select the **Tomcat Deploy** job and click **SELECT**.

  - The node gets annotated with the name of the job. Hover the mouse pointer over the node, you’ll see a red **x** and a green **+** signs appear.

> **Tip**
> 
> Using the red "x" allows you to remove the node, the green plus lets you add the next node.

  - Click the green **+** sign

  - Choose **Web App Deploy** as the next Job (you might have to switch to the next page)

  - Leave **Type** set to **On Success**

> **Tip**
> 
> The type allows for more complex workflows. You could lay out different execution paths for successful and for failed Playbook runs.

  - Click **SELECT**

  - Click **SAVE** in the **WORKFLOW VISUALIZER** view

  - Click **SAVE** in the **Workflow Template** view

## And Action

Your workflow is ready to go, launch it.

  - Click the blue **LAUNCH** button directly or go to the the **Templates** view and launch the **Deploy Webapp Server** workflow by clicking the rocket icon.

![jobs view of workflow](images/job_workflow.png)

Note how the workflow run is shown in the job view. In contrast to a normal job template job execution this time there is no playbook output on the right, but a visual representation of the different workflow steps. If you want to look at the actual playbooks behind that, click **DETAILS** in each step. If you want to get back from a details view to the corresponding workflow, click the ![w-button](images/w_button.png) in the **JOB TEMPLATE** line in the **DETAILS** part on the left side of the job overview.

After the job was finished, check if everything worked fine: log into `node1`, `node2` or `node3` from your control host and run:

```bash
$ curl http://localhost:8080/coolapp/
```

> **Tip**
> 
> You might have to wait a couple of minutes until Tomcat answers requests.

----

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-2---ansible-tower-exercises)
