# Ansible ワークショップ - Smart Management Automation

**これは Ansible Automation Platform 2 のドキュメントです**

このワークショップでは、Red Hat Smart Management サブスクリプションと Ansible Automation Platform
の最適な使用方法について説明します。

## 目次

# 目次
- [Ansible ワークショップ - Smart Management
  Automation](#ansible-workshop---smart-management-automation)
  - [目次](#table-of-contents)
- [目次](#table-of-contents-1)
  - [ラボダイアグラム](#lab-diagram)
  - [ラボの設定](#lab-setup)
    - [目的](#objective)
    - [ガイド](#guide)
      - [ラボ環境](#your-lab-environment)
      - [**ステップ 1 - Ansible Tower の設定**](#step-1---setup-ansible-tower)
      - [**ステップ 2 - プロジェクトの作成**](#step-2---create-a-project)
      - [**ステップ 3 - ジョブテンプレートの作成**](#step-3---create-job-template)
  - [設定管理](#config-management)
  - [セキュリティーおよびコンプライアンス](#security-and-compliance)


## ラボダイアグラム
## ラボの設定

### 目的
- アクティベーションキーとライフサイクル環境の設定 - Satellite Server へのサーバーの登録

### ガイド
#### ラボ環境

このラボでは、事前設定されたラボ環境で作業します。ここでは、以下のホストにアクセスできます。

| Role                 | Inventory name |
| ---------------------| ---------------|
| Automation Platform  | ansible-1      |
| Satellite Server     | satellite      |
| Managed Host 1       | node1          |
| Managed Host 2       | node2          |
| Managed Host 3       | node3          |

#### **ステップ 1 - Ansible Tower の設定**

Automation Platform にログインします。

ブラウザーを開き、アテンダンスページにある Ansible Tower UI のリンクに移動します。アテンダンスページで、ユーザー名 `admin`
とパスワードを入力してログインします。

#### **ステップ 2 - プロジェクトの作成**

Automation Platform ホームページの左側にあるナビゲーションセクションから、**Project** を選択します。右上隅の緑色の
**Create** ボタンをクリックします。

ソース git リポジトリーとして
`https://github.com/willtome/automated-smart-management.git`
を使用して、プロジェクトを作成します。**Update on Launch** のチェックボックスをオンにします。

#### **ステップ 3 - ジョブテンプレートの作成**

## 設定管理
## Security and Compliance
