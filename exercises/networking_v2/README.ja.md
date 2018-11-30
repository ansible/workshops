# Ansible Linklight - Networking

このコンテンツは、Ansibleのネットワーク機器向け機能(Arista, Cisco, Cumulus, Juniper etc)の効果的なデモやワークショップトレーニング(講師による講義、ハンズあるいはセルフスタディ)の為の多目的ツールキットです。

## Presentation
プレゼンテーション用のスライドが必要ですか？  
こちらを確認ください。:  
[Ansible Networking Linklight Deck](../../decks/ansible-networking_v2.html)

## Ansible Network Automation Exercises

### Section 01 - Using Ansible to gather data from network devices
- [Exercise 1.0 - Anisbleのlab環境を確認してみよう](./exercises/1-0-explore)
- [Exercise 1.1 - Writing your first playbook](./exercises/1-1-first-playbook)
- [Exercise 1.2 - Module documentation, Registering output & tags](./exercises/1-2-playbook-basics)

### Section 02 - Using Ansible to configure, backup and restore
- [Exercise 2.0 - Updating the router configurations using Ansible](./exercises/2-0-config)
- [Exercise 2.1 - Backing up the router configuration](./exercises/2-1-backup/)
- [Exercise 2.2 - Using Ansible to restore the backed up configuration](./exercises/2-2-restore)

### Section 03 - Using Ansible to parse information for reporting
- [Exercise 3.0 - An introduction to templating with Jinja2](./exercises/3-0-templates)
- [Exercise 3.1 - Building dynamic documentation using the command parser](./exercises/3-1-parser/)

## Network Diagram ~この演習のNW構成図~
![Red Hat Ansible Automation](../../images/network_diagram.png)

## 追加情報
 - [Network Automation with Ansible Homepage](https://www.ansible.com/network-automation)
 - [AnsibleのNetwork用Moduleを見てみる](http://docs.ansible.com/ansible/latest/list_of_network_modules.html)
 - [Moduleのメンテナンス と Supportについて見てみる](http://docs.ansible.com/ansible/latest/modules_support.html)
 - [Network Automation GitHub レポジトリを見てみる](https://github.com/network-automation)

---
![Red Hat Ansible Automation](../../images/networkautomation.png)

- [Red Hat® Ansible® Network Automation](https://www.ansible.com/networking): Arista (EOS), Cisco (IOS, IOS XR, NX-OS), Juniper (JunOS), Open vSwitch, VyOS など様々なNWデバイスを自動化しましょう！  
ネットワーク事例を含む様々なAnsibleTowerのユースケースを[こちらから参照](https://www.ansible.com/tower)できます。
