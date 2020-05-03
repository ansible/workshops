# Ansible Linklight - F5 Networking Workshop

![f5workshop](../../images/ansiblef5-transparent.png)

これはインストラクターの講義、ハンズオン、自習などの様々な形式でワークショップトレーニングを提供することで、F5 BIG-IP を Ansible で自動化する機能を効果的に実証する多目的のコンテンツとなります。

**Read this in other languages**: ![uk](../../images/uk.png) [English](README.md),  ![japan](../../images/japan.png) [日本語](README.ja.md).

## Presentation
プレゼンテーション資料はこちらです:
[Ansible F5 Workshop Deck](../../decks/ansible_f5.pdf)

## Diagram
![f5 diagram](../../images/f5topology.png)

BIG-IP へのログイン情報:
- username: admin
- password: **講師から指示されます** (default is admin)

## Section 1 - Ansible x F5 基礎演習

 - [演習 1.0 - 演習環境の確認](1.0-explore/README.ja.md)
 - [演習 1.1 - Ansible による F5 BIG-IP の情報収集](1.1-get-facts/README.ja.md)
 - [演習 1.2 - F5 BIG-IP へのノード追加](1.2-add-node/README.ja.md)
 - [演習 1.3 - プールの追加](1.3-add-pool/README.ja.md)
 - [演習 1.4 - メンバーをプールへ追加](1.4-add-pool-members/README.ja.md)
 - [演習 1.5 - Virtual Server の追加](1.5-add-virtual-server/README.ja.md)
 - [演習 1.6 - iRule の追加と virtual server へのアタッチ](1.6-add-irules/README.ja.md)
 - [演習 1.7 - コンフィグの保存](1.7-save-running-config/README.ja.md)

## Section 2 - Ansible F5 運用/応用演習

 - [演習 2.0 - プールメンバーの無効化](2.0-disable-pool-member/README.ja.md)
 - [演習 2.1 - コンフィグの削除](2.1-delete-configuration/README.ja.md)
 - [演習 2.2 - エラーハンドリング](2.2-error-handling/README.ja.md)

## Section 3 - Ansible F5 AS3 演習

 - [演習 3.0 - AS3 の紹介](3.0-as3-intro/README.ja.md)
 - [演習 3.1 - AS3 による変更運用](3.1-as3-change/README.ja.md)
 - [演習 3.2 - Web アプリケーションの削除](3.2-as3-delete/README.ja.md)

## Section 4 - Ansible F5 Ansible Tower 演習

 - [演習 4.0 - Red Hat Ansible Tower環境の確認](4.0-explore-tower/README.ja.md)
 - [演習 4.1 - Ansible Tower ジョブテンプレートの作成](4.1-tower-job-template/README.ja.md)
 - [演習 4.2 - ワークフローの作成](4.2-tower-workflow/README.ja.md)
 - [演習 4.3 - ノードメンテナンスワークフローの作成](4.3-tower-workflow2/README.ja.md)

### 演習に関連した議論や質問を投稿するには以下のリンクを使用してください:
  - **https://devcentral.f5.com/questions/f5-ansible-automation-discussion-63579**

---
![Red Hat Ansible Automation](../../images/rh-ansible-automation-platform.png)
