# 演習 2.3 - プロジェクトとジョブテンプレート

Tower の **プロジェクト** は、 Git、Subversion、Mercurial、ローカルホルダなど、Playbook の置き場所を定義する仕組みを提供します。 Tower ではサポートとされるソースコード管理（SCM）と連携して Playbook を管理することが可能です。  

Playbook は SCM など、バージョン管理の仕組みの下に置いておくべきです。このラボでは、 Git リポジトリに保存されている Playbook を利用します。  

## Git リポジトリのセットアップ  
このデモでは、既に Git リポジトリに保存されているプレイブックを使用します。  

**https://github.com/ansible/workshop-examples**

このラボで利用する Apache Web Server をインストールするための Playbook は、上記 github サイトの **rhel/apache** に置いてある、`apache_install.yml` です。内容は以下の通りです。  

```yaml
---
- name: Apache server installed
  hosts: all

  tasks:
  - name: latest Apache version installed
    yum:
      name: httpd
      state: latest

  - name: latest firewalld version installed
    yum:
      name: firewalld
      state: latest

  - name: firewalld enabled and running
    service:
      name: firewalld
      enabled: true
      state: started

  - name: firewalld permits http service
    firewalld:
      service: http
      permanent: true
      state: enabled
      immediate: yes

  - name: Apache enabled and running
    service:
      name: httpd
      enabled: true
      state: started
```

> **ヒント**
> 
> Engine の演習で書いた Playbook と比較するとちょっと違っているところがあります。重要なところは、 `become` が無いところと、 `hosts` の設定に `all` を指定しているところです。  

このリポジトリを Tower の **Source Control Management (SCM)** として利用するには **プロジェクト** を作成する必要があります。  

## プロジェクトの作成  

  - 左のメニューから **プロジェクト** を選択し、 ![plus](images/green_plus.png) ボタンをクリック。フォームにいかを記入します。  

  - **名前** Ansible Workshop Examples  

  - **組織** Default  

  - **SCM タイプ** Git  

ここで、リポジトリにアクセスするためのURLが必要です。上記の Github リポジトリに移動し、右側の緑色の **Clone or download** ボタンをクリック。さらに、 **Clone with HTTPS** が選択されていることを確認し、URL をコピーします。  

SCM URL にコピーした URL を貼り付けます。  

- **SCM URL** `https://github.com/ansible/workshop-examples.git`  

- **SCM 更新オプション** 3つのボックスすべてにチェックマークを付けて、常にリポジトリの最新コピーを取得し、ジョブの起動時にリポジトリを更新します。    

- **保存** をクリックします  

新しいプロジェクトは、作成後に自動的に同期されます。ただし、これを手動で行うこともできます。 **Projects** ビューに移動し、プロジェクトの右側にある円形矢印 **最新のSCMリビジョンを取得** アイコンをクリックして、プロジェクトを Git リポジトリと再度同期します。  

## ジョブテンプレートを作成してジョブを実行する  

ジョブテンプレートは、Ansible ジョブを実行するための定義とパラメーターのセットです。ジョブテンプレートは、同じジョブを何度も実行するのに役立ちます。ジョブ手プレートではいくつかのパラメータを指定します。それぞれの意味は下記の通りです。  

- **インベントリ** ジョブを実行するホストを指定します  

- **認証情報** 管理対象ホストにログインするためのアカウント情報です  

- **プロジェクト** Playbook の場所を指定します   

- **Playbook の指定** 実際に使用する Playbook の指定  

早速 **Job Template** を作成してみましょう。♪  
左のメニューから **Templates** を選択し、[plus](images/green_plus.png) ボタンをクリック。選択肢の中から **ジョブテンプレート** を選びます。  

> **ヒント**
> 
> 下記フィールドの多くは、虫眼鏡アイコンをクリックの上オプション選択で設定が可能です。

- **名前** Apache Install

- **ジョブタイプ** 実行

- **インベントリー** Workshop Inventory

- **PROJECT:** Ansible Workshop Examples

- **PLAYBOOK:** `rhel/apache/apache_install.yml`

- **CREDENTIAL:** Workshop Credentials

- We need to run the tasks as root so check **Enable privilege escalation**

- Click **SAVE**

You can start the job by directly clicking the blue **LAUNCH** button, or by clicking on the rocket in the Job Templates overview. After launching the Job Template, you are automatically brought to the job overview where you can follow the playbook execution in real time:

![job exection](images/job_overview.png)

Since this might take some time, have a closer look at all the details provided:

- All details of the job template like inventory, project, credentials and playbook are shown.

- Additionally, the actual revision of the playbook is recorded here - this makes it easier to analyse job runs later on.

- Also the time of execution with start and end time is recorded, giving you an idea of how long a job execution actually was.

- On the right side, the output of the playbook run is shown. Click on a node underneath a task and see that detailed information are provided for each task of each node.

After the Job has finished go to the main **Jobs** view: All jobs are listed here, you should see directly before the Playbook run an SCM update was started. This is the Git update we configured for the **Project** on launch\!

## Challenge Lab: Check the Result

Time for a little challenge:

  - Use an ad hoc command on both hosts to make sure Apache has been installed and is running.

You have already been through all the steps needed, so try this for yourself.

> **Tip**
> 
> What about `systemctl status httpd`?

> **Warning**
> 
> **Solution Below**

- Go to **Inventories** → **Workshop Inventory**

- In the **HOSTS** view select both hosts and click **RUN COMMANDS**

- **MODULE:** command

- **ARGUMENTS:** systemctl status httpd

- **MACHINE CREDENTIALS:** Workshop Credentials

- Click **LAUNCH**

## What About Some Practice?

Here is a list of tasks:

> **Warning**
> 
> Please make sure to finish these steps as the next chapter depends on it\!

- Create a new inventory called `Webserver` and make only `node1` member of it.

- Copy the `Install Apache` template using the copy icon in the **Templates** view

- Change the name to `Install Apache Ask`
  
- Change the **INVENTORY** setting of the Project so it will ask for the inventory on launch

- **SAVE**

- Llaunch the `Install Apache Ask` template.

- It will now ask for the inventory to use, choose the `Webserver` inventory and click **LAUNCH**

- Wait until the Job has finished and make sure it run only on `node1`

> **Tip**
> 
> The Job didn’t change anything because Apache was already installed in the latest version.

----

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-2---ansible-tower-exercises)

