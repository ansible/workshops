# 演習 2.1 - Tower の紹介（インストール）

## Ansible Tower の価値

Ansible Towerは、IT自動化のためのエンタープライズソリューションを提供するWebベースのUIです。

  - ユーザーフレンドリーなダッシュボード形式

  - Ansibleを補完し、自動化、ビジュアル管理、および監視機能を追加します

  - 管理者にユーザーアクセス制御を提供します

  - 仮想化、クラウドなど様々な情報ソース内のグラフィカルなインベントリの管理と同期

  - RESTful API への対応

  - などなど...

## Ansible Tower ラボ環境

この実習ラボでは、事前設定された実習ラボ環境で作業します。以下のホストにアクセスできます。  

| Role                         | Inventory name |
| -----------------------------| ---------------|
| Ansible Control Host & Tower | ansible        |
| Managed Host 1               | node1          |
| Managed Host 2               | node2          |
| Managed Host 2               | node3          |

Ansible Towerはすでにインストールされ、ライセンスが付与されています。WebUIにはHTTP / HTTPS経由でアクセスできます。  

※講師の意向により Ansible Tower がインストールされていない場合もあります。その際は講師より指示がありますので、Ansible Tower のインストールから実施ください。  

## Ansible Tower インストール

Ansible Tower のインストールが未実施の場合、以下の手順で Tower のインストールを実施ください。既にインストールされている場合はこの手順はスキップしてください。  

> **Warning**
> 
> **11.22.33.44** は自分自身の Ansible Control Host のIPアドレスに置き換えてください。  

Ansible Control Host に ssh でログインします。  

    ssh studentX@11.22.33.44

Ansible Control Host に Tower をインストールします。  

    [student<X>@ansible ~]$ cd /tmp
    [student<X>@ansible ~]$ curl -O https://releases.ansible.com/ansible-tower/setup/ansible-tower-setup-latest.tar.gz
    [student<X>@ansible ~]$ tar xvzf ansible-tower-setup-<xxxxx>.tar.gz
    [student<X>@ansible ~]$ cd ansible-tower-setup-<xxxxx>
    [student<X>@ansible ~]$ vi inventory
  
※ファイルの中でブランクになっている、3つのパスワードを以下の通り設定し、ファイルを保存します。  
  
 admin_password='ansibleWS'  
 pg_password='ansibleWS'  
 rabbitmq_password='ansibleWS'  

インストール開始！！  
  
    [student<X>@ansible ~]$ sudo ./setup.sh

ライセンスファイルの適応  

1.Ansible Tower サーバーにブラウザでアクセスし"参照"をクリックします。  
　https://<Ansigle Control Host>/  
　IDとパスワードは、インストール時に指定した admin / ansibleWS です。  
2. 参照をクリックし、ライセンスファイルを指定します。  
　※ライセンスファイルに関しては講師より指示があります。    
<img src="/image/LicenseFile.jpg" alt="attach:cat" title="attach:cat" width="700">
3.使用許諾にチェックを入れて"送信"を押下します。  

     

## ダッシュボード

When logged in to Ansible Tower using the web UI, the administrator can view a graph that shows

  - recent job activity

  - the number of managed hosts

  - quick pointers to lists of hosts with problems.

The dashboard also displays real time data about the execution of tasks completed in playbooks.

![Ansible Tower License](images/LisenceFile.jpg)

## Concepts

To start using Ansible Tower, you should get familiar with some concepts and naming conventions.

**Projects**

Projects are logical collections of Ansible playbooks in Ansible Tower. These playbooks either reside on the Ansible Tower instance, or in a source code version control system supported by Tower.

**Inventories**

An Inventory is a collection of hosts against which jobs may be launched, the same as an Ansible inventory file. Inventories are divided into groups and these groups contain the actual hosts. Groups may be populated manually, by entering host names into Tower, from one of Ansible Tower’s supported cloud providers or through dynamic inventory scripts.

**Credentials**

Credentials are utilized by Tower for authentication when launching Jobs against machines, synchronizing with inventory sources, and importing project content from a version control system. Credential configuration can be found in the Settings.

Tower credentials are imported and stored encrypted in Tower, and are not retrievable in plain text on the command line by any user. You can grant users and teams the ability to use these credentials, without actually exposing the credential to the user.

**Templates**

A job template is a definition and set of parameters for running an Ansible job. Job templates are useful to execute the same job many times. Job templates also encourage the reuse of Ansible playbook content and collaboration between teams. To execute a job, Tower requires that you first create a job template.

**Jobs**

A job is basically an instance of Tower launching an Ansible playbook against an inventory of hosts.

----

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-2---ansible-tower-exercises)

