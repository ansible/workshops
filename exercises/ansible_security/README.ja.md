# Ansible ワークショップ - Ansible Security Automation

**これは Ansible Automation Platform 2 のドキュメントです**

3 つのセキュリティーユースケースの自動化を実装することで、Ansible Security Automation を使い始めましょう。3
つのユースケースとは、1) ファイアウォールのオーケストレーション、2) IDS と SIEM (Web サーバー上の疑わしいトラフィックの調査)、3)
脅威ハンティング (ファイアウォール上の異常なアクセス拒否の分析と SQL インジェクションの修復)
になります。このワークショップでは、簡単な紹介の後、基本的なコンセプトを説明し、Ansible Security Automation
を既存のサードパーティーのセキュリティーソリューションと組み合わせて使用する方法を紹介します。

**他の言語でもお読みいただけます**: <br>
[![uk](../../images/uk.png) English](README.md),  [![japan](../../images/japan.png) 日本語](README.ja.md), [![france](../../images/fr.png) Français](README.fr.md).<br>

## ワークショップの平均時間

ワークショップに必要な時間は、参加者の数、参加者がどれだけ Linux
に精通しているか、ワークショップの間にどれだけの議論が行われるかなど、複数の要因に大きく左右されます。

Ansible に関する基本的な経験者の場合

- 概要には約 30 分かかります。最初の演習には約 1 時間かかります。2 番目の演習には約 2 時間かかります。

これらのワークショップのスケジューリングが異なる場合は、Red Hat までご連絡ください。

## ラボダイアグラム

![ansible security lab
diagram](../../images/ansible_security_diagram.png#centreme)

## セクション 1 - Ansible Security Automation の基本について

 - [演習 1.1 - ラボ環境の調査](1.1-explore)
 - [演習 1.2 - 最初の Check Point 用 Playbook の実行](1.2-checkpoint)
 - [演習 1.3 - 最初の Snort Playbook の実行](1.3-snort)
 - [演習 1.4 - 最初の IBM QRadar Playbook の実行](1.4-qradar)

## セクション 2 - Ansible Security Automation のユースケース

 - [演習 2.1 - 調査の強化](2.1-enrich)
 - [演習 2.2 - 脅威ハンティング](2.2-threat)
 - [演習 2.3 - インシデントレスポンス](2.3-incident)

---
![Red Hat Ansible
Automation](../../images/rh-ansible-automation-platform.png)
