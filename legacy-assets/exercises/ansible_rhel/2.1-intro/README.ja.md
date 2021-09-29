# ワークショップ演習 - Ansible Tower の概要

**その他の言語はこちらをお読みください。**
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## 目次

* [目的](#objective)
* [ガイド](#guide)
* [Ansible Tower を使う理由](#why-ansible-tower)
* [使用する Ansible Tower ラボ環境](#your-ansible-tower-lab-environment)
* [ダッシュボード](#dashboard)
* [コンセプト]（＃concepts）

## 目的

この演習では、Red Hat Ansible Automation Platform によって提供される機能の実行を含む、AnsibleTower
の概要を説明します。次のような AnsibleTower の基本を対象とします。

* ジョブテンプレート
* プロジェクト
* インベントリー
* 認証情報
* ワークフロー

## ガイド

### Ansible Tower を使う理由

Ansible Tower は、IT 自動化のためのエンタープライズソリューションを提供する Web ベースの UI です。

* これには、ユーザーフレンドリーなダッシュボードがあります
* 自動化、視覚的管理、監視機能を追加して Ansible を補佐
* 管理者にユーザーアクセス制御を提供
* インベントリーをグラフィカルに監視し、さまざまなリソースと同期
* RESTfulAPI が利用可
* その他いろいろ...

### Ansible Tower ラボ環境

このラボでは、事前設定されたラボ環境で作業します。ここでは、以下のホストにアクセスできます。

| Role                         | Inventory name |
| -----------------------------| ---------------|
| Ansible Control Host & Tower | ansible-1      |
| Managed Host 1               | node1          |
| Managed Host 2               | node2          |
| Managed Host 2               | node3          |

このラボの Ansible Tower
は、個別にセットアップされています。作業を行うマシンへの適切なアクセス権があることを確認してください。Ansible Tower
は、すでにインストールされてライセンス付与が行われています。Web UI は、HTTP/HTTPS でアクセスできます。

### ダッシュボード

タワーを最初に見てみましょう。指定の URL にブラウザでアクセスします。この URL は `https://student<X>.workshopname.rhdemo.io` のようなもので、`<X>` は、学習者番号に置き換え、`workshopname` は、現在のワークショップ名に置き換えます。次に `admin` としてログインします。このパスワードは、インストラクターから渡されます。

Ansible TowerのWeb UI では、次を示すグラフのあるダッシュボードが表示されます。

* 最近のジョブのアクティビティー
* 管理対象ホストの数
* 問題のあるホストのリストへのクイックポインター。

このダッシュボードには、Playbook で完了したタスクの実行に関するリアルタイムデータも表示されます。

![Ansible Tower ダッシュボード](images/dashboard.png)

### コンセプト

自動化に Ansible Tower を使用する方法を詳しく説明する前に、いくつかの概念と命名規則について理解しておく必要があります。

#### プロジェクト

プロジェクトは、Ansible Tower にある Ansible Playbook の論理的なコレクションです。これらの Playbook
は、Ansible インスタンス、または Tower でサポートされているソースコードバージョン管理システムにあります。

#### インベントリー

インベントリーは、ジョブを起動できるホストのコレクションです (Ansible
インベントリーファイルと同様)。インベントリーはグループに分類され、それらのグループには実際のホストが含まれます。グループは、ホスト名を Tower
に入力して手動で取得することも、Ansible Tower
のサポートされるクラウドプロバイダーや動的インベントリースクリプトから取得することもできます。

#### 認証情報

認証情報は、ジョブをマシンに対して起動したり、インベントリーソースと同期したり、プロジェクトのコンテンツをバージョン管理システムからインポートしたりする際の認証に使用されます。認証情報は、設定で見つかります。

Tower の認証情報は、Tower
にインポートおよび暗号化されて保存されます。コマンドラインにおいてプレーンテキストで取得することはできません。実際に認証情報をユーザーに公開することなく、これらの認証情報を使用する機能をユーザーとチームに付与できます。

#### テンプレート

ジョブテンプレートは、Ansible
ジョブを実行するための定義であり、パラメーターセットでもあります。ジョブテンプレートは同じジョブを何度も実行する場合に便利です。また、ジョブテンプレートは
Ansible playbook コンテンツの再利用およびチーム間のコラボレーションを促進します。ジョブを実行するには、Tower
ではジョブテンプレートを先に作成する必要があります。

#### ジョブ

ジョブは、Ansible Playbook をホストのインベントリーに対して起動する Tower のインスタンスです。

---
**ナビゲーション**
<br>
[前の演習](../1.7-role) - [次の演習](../2.2-cred)

[クリックして Ansible for Red Hat Enterprise Linux Workshop
に戻ります](../README.md#section-2---ansible-tower-exercises)
