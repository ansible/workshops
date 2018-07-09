## Playbook 2 - host-routes.yml
Linuxホスト上にスタティックルートを定義したplaybook

学べること:
 - lineinfile モジュール
 - ハンドラ

 ---

### ステップ 1: Play を定義する

`host-routes.yml` という名の2つ目のplaybookを作成しましょう。

```bash
vim host-routes.yml
```

2つ目のplaybookに、VPC-1 (172.16.0.0/16) から VPC-2 (172.17.0.0/16) までのルートと、その逆のルートをそれぞれ追加する必要があります。この演習のハンドラについて説明します。

2つの経路が必要です:
 - `ansible` コントロールノード から `rtr1`まで、サブネット `172.17.0.0/16`
 - `host1` ノードから `rtr2`まで、サブネット `172.16.0.0/16`

この playbook は、`ansible` と `host1` のノード上でのみ実行します。`connection:local`が削除されているか確かめてから backup.yml のplaybookから実行してください。また、2つのホストにスタティックルートを追加してから、`host-routes.yml` のplaybookを実行してください。

```yml
---
- name: add route on ansible
  hosts: ansible
  gather_facts: no
  become: yes
```
`ansible`ホストはRed Hat Enterprise Linux Serverが起動しています。スタティックルートを追加するため、[Ansible lineinfile モジュール](http://docs.ansible.com/ansible/latest/lineinfile_module.html) を使用して`/etc/sysconfig/network-scripts/route-eth0`にサブネットと宛先IPを行追加する必要があります。```create: yes``` でファイルが存在しない場合は作成します。また、`notify: "restart network"` でファイルが変更された場合にハンドラが実行されます。

### ステップ 2: task の追加
{% raw %}
```yml
  tasks:
    - name: add route to 172.17.0.0/16 subnet on ansible node
      lineinfile:
        path: /etc/sysconfig/network-scripts/route-eth0
        line: "172.17.0.0/16 via {{hostvars['rtr1']['private_ip']}}"
        create: yes
      notify: "restart network"
```
{% endraw %}
ルートが変更された場合にネットワークを再起動するためのハンドラを作成しておく必要があります。The name matters and must match what we are notifying in the task displayed above.
このケースにおいては、`restart network` が実行されるべきですが、ユーザが定義し、かつハンドラ実行条件にマッチした場合に限ります。

### ステップ 3: ハンドラを追加

```yml
  handlers:
    - name: restart network
      systemd:
        state: restarted
        name: network
```

### ステップ 4: host1 にも実施


`host1` にも同様に実施する必要があります:

{% raw %}
```yml
- name: add route on host1
  hosts: host1
  gather_facts: no
  become: yes

  tasks:
    - name: add route to 172.16.0.0/16 subnet on host1 node
      lineinfile:
        path: /etc/sysconfig/network-scripts/route-eth0
        line: "172.16.0.0/16 via {{hostvars['rtr2']['private_ip']}}"
        create: yes
      notify: "restart network"

  handlers:
    - name: restart network
      systemd:
        state: restarted
        name: network
```
{% endraw %}

### ステップ 5: playbook を実行

playbookを実行します:
```bash
ansible-playbook host-routes.yml
```

# 完了
これで演習 1.2 は終了です。

# 正解
- backup.ymlは、[こちらをclick](https://github.com/network-automation/linklight/blob/master/exercises/networking/1.2-backup/backup.yml).
- host-routes.ymlは、[こちらをclick](https://github.com/network-automation/linklight/blob/master/exercises/networking/1.2-backup/host-routes.yml)
