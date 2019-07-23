# 演習 1.6 - テンプレート

Ansibleは、管理対象ホストにファイルをコピーする際、固定の内容ではなく、ファイル内容を変更した上でコピーする事も可能です。例えば対象ホストユニークなホスト名などを含めてコピーすることも可能です。これを実現するのが Jinja2 テンプレートです。 Jinja2 は、Python で最も使用されているテンプレートエンジンの1つです。 (<http://jinja.pocoo.org/>)

## ステップ 1.6.1 -  playbook 内でテンプレートを使用する

利用は簡単です。まず、ファイル作成を行うためのテンプレートをファイルを作成し、テンプレートモジュールを使って対象ホストに転送するだけです。

早速演習を行ってみましょう！  
テンプレートを使って、対象ホストの motd ファイルをホスト固有のデータを含むように変更してみます。  

まず、 `~/ansible-files/` ディレクトリ内に、テンプレートファイル `motd-facts.j2` を作成します。  

<!-- {% raw %} -->
```html+jinja
Welcome to {{ ansible_hostname }}.
{{ ansible_distribution }} {{ ansible_distribution_version}}
deployed on {{ ansible_architecture }} architecture.
```
<!-- {% endraw %} -->

The template file contains the basic text that will later be copied over. It also contains variables which will be replaced on the target machines individually.

Next we need a playbook to use this template. In the `~/ansible-files/` directory create the Playbook `motd-facts.yml`:

```yaml
---
- name: Fill motd file with host data
  hosts: node1
  become: yes
  tasks:
    - template:
        src: motd-facts.j2
        dest: /etc/motd
        owner: root
        group: root
        mode: 0644
```

You have done this a couple of times by now:

  - Understand what the Playbook does.

  - Execute the Playbook `motd-facts.yml`

  - Login to node1 via SSH and check the motto of the day message.

  - Log out of node1

You should see how Ansible replaces the variables with the facts it discovered from the system.

## Step 6.2 - Challenge Lab

Add a line to the template to list the current kernel of the managed node.

  - Find a fact that contains the kernel version using the commands you learned in the "Ansible Facts" chapter.

> **Tip**
> 
> Do a `grep -i` for kernel

  - Change the template to use the fact you found.

  - Run the Playbook again.

  - Check motd by logging in to node1

> **Warning**
> 
> **Solution below\!**


  - Find the fact:

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup|grep -i kernel
       "ansible_kernel": "3.10.0-693.el7.x86_64",
```

  - Modify the template `motd-facts.j2`:

```bash
Welcome to {{ ansible_hostname }}.
{{ ansible_distribution }} {{ ansible_distribution_version}}
deployed on {{ ansible_architecture }} architecture
running kernel {{ ansible_kernel }}.
```

  - Run the playbook.
  - Verify the new message via SSH login to `node1`.

----

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-1---ansible-engine-exercises)

