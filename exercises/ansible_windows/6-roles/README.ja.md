# 演習 6 - Ansible roles
このワークショップ全体で行ったように、1つの Playbook として記述することは可能ですが、Ansible を使っていると、有用な Playbook を他から再利用したいと考えるようになります。  

Ansible Roles はこの手段を提供します。Roles を作成すると、Playbook をパーツが分解され、それらのパーツがディレクトリ構造に配置されます。これは Playbook 管理のベストプラクティスと考えられており、Ansible を使っていく上で多くの時間を節約できます。  

この演習では、作成した Playbook を Role に作り変えます。  

まず、iis-basic-playbookがどのように複数の Role に分解されるかを見てみましょう…  

## Role のためのディレクトリーの作成

## ステップ 1:

Visual Studio Codeで、エクスプローラーと以前に `iis_advanced` を作成したWORKSHOP_PROJECT *セクションに移動します。  

![iis\_advanced](images/6-vscode-existing-folders.png)

**iis_advanced** フォルダーを選択します。  

**iis_advanced**を右クリックして*New Folder*を選択、**roles** という名前のホルダーを作成します。   

**roles**を右クリックし、その下に `iis_simple`という新しいフォルダーを作成します。　　

## ステップ 2:  

*iis\_simple* の下にさらに以下の新しいホルダーを作成します:

- defaults

- vars

- handlers

- tasks

- templates

## Step 3:  

template ホルダーを除く各ホルダーに、`main.yml`という名前のファイルを作成します。これは基本的な Roles のホルダー構造であり、main.ymlはロールが各セクションで使用するデフォルトのファイルになります。

完成した構造は次のようになります。  

![Role Structure](images/6-create-role.png)

# Playbook の Role 化

このセクションでは、`vars：`、`tasks：`、`template：`、`handlers：`など、Playbook の主要部分を分解し Role 化します。  

## ステップ 1:

元の `site.yml` のバックアップを作成した後、新しく `site.yml`を作成します。  

`iis_advanced` ホルダーで、`site.yml`を右クリックし、`rename`を選択、`site.yml.backup`に変更します。  

同じホルダーに`site.yml` を新たに作成します。  

## ステップ 2:

site.ymlを編集して、iis_simple という名の Role を呼び出すようにします。以下のようになります。  

```yaml
    ---
- hosts: windows
  name: This is my role-based playbook
  
  roles:
    - iis_simple
```

![New site.yml](images/6-new-site.png)

## ステップ 3:

デフォルト変数をロールに追加します。 `roles \ iis_simple \ defaults \ main.yml`を次のように編集します：

```yaml
    ---
# defaults file for iis_simple
iis_sites:
  - name: 'Ansible Playbook Test'
    port: '8080'
    path: 'C:\sites\playbooktest'
  - name: 'Ansible Playbook Test 2'
    port: '8081'
    path: 'C:\sites\playbooktest2'
```

## ステップ 4:

`roles \ iis_simple \ vars \ main.yml`のロールにいくつかのロール固有の変数を追加します。  

```yaml
---
# vars file for iis_simple
iis_test_message: "Hello World!  My test IIS Server"
```

> **ヒント**
>
> **変数を違う場所に置く？？**
>
> はい！ Ansible では、変数はいろんな場所に置く事が出来ます。ほんの一例をあげると:  
>
> - vars ホルダー
>
> - defaults ホルダー
>
> - group\_vars ホルダー
>
> - Playbook の `vars:` の中
>
> - コマンド実行の際の`--extra_vars` オプション
>
>上記変数の定義は、場所によって優先順位が決まっています。最初からあまりいろんなところに置く必要はありませんが、こちらを一度確認しておくと良いと思います。[variable precedence](http://docs.ansible.com/ansible/latest/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable)。この演習では、Role の default を使用していくつかの変数を定義していますが、これらは優先順位が低いため、他の場所で記述されると置き換わります。逆に言うと、順応性がある変数とも言えます。この default より優先順位が高いのが vars で、一部をこちらで定義してみました。  

## ステップ 5:

次に、ハンドラーを Role 化してみましょう。編集するファイルは、`roles\iis_simple\handlers\main.yml` です。

```yaml
---
# handlers file for iis_simple
- name: restart iis service
  win_service:
    name: W3Svc
    state: restarted
    start_mode: auto
```

## ステップ 6:

Add tasks to your role in `roles\iis_simple\tasks\main.yml`.

<!-- {% raw %} -->
```yaml
    ---
    # tasks file for iis_simple

    - name: Install IIS
      win_feature:
        name: Web-Server
        state: present

    - name: Create site directory structure
      win_file:
        path: "{{ item.path }}"
        state: directory
      with_items: "{{ iis_sites }}"

    - name: Create IIS site
      win_iis_website:
        name: "{{ item.name }}"
        state: started
        port: "{{ item.port }}"
        physical_path: "{{ item.path }}"
      with_items: "{{ iis_sites }}"
      notify: restart iis service

    - name: Open port for site on the firewall
      win_firewall_rule:
        name: "iisport{{ item.port }}"
        enable: yes
        state: present
        localport: "{{ item.port }}"
        action: Allow
        direction: In
        protocol: Tcp
      with_items: "{{ iis_sites }}"

    - name: Template simple web site to iis_site_path as index.html
      win_template:
        src: 'index.html.j2'
        dest: '{{ item.path }}\index.html'
      with_items: "{{ iis_sites }}"

    - name: Show website addresses
      debug:
        msg: "{{ item }}"
      loop:
        - http://{{ ansible_host }}:8080
        - http://{{ ansible_host }}:8081
```
<!-- {% endraw %} -->

Step 7:
-------

Add your index.html template.

Right-click `roles\iis_simple\templates` and create a new file called
`index.html.j2` with the following content:

<!-- {% raw %} -->
```html
    <html>
    <body>

      <p align=center><img src='http://docs.ansible.com/images/logo.png' align=center>
      <h1 align=center>{{ ansible_hostname }} --- {{ iis_test_message }}

    </body>
    </html>
```
<!-- {% endraw %} -->

Now, remember we still have a *templates* folder at the base level of
this playbook, so we will delete that now. Right click it and Select
*Delete*.

Step 8: Commit
--------------

Click File → Save All to ensure all your files are saved.

Click the Source Code icon as shown below (1).

Type in a commit message like `Adding iis_simple role` (2) and click the
check box above (3).

![Commit iis\_simple\_role](images/6-commit.png)

Click the `synchronize changes` button on the blue bar at the bottom
left. This should again return with no problems.

Section 3: Running your new playbook
====================================

Now that you’ve successfully separated your original playbook into a
role, let’s run it and see how it works. We don’t need to create a new
template, as we are re-using the one from Exercise 5. When we run the
template again, it will automatically refresh from git and launch our
new role.

Step 1:
-------

Before we can modify our Job Template, you must first go resync your
Project again. So do that now.

Step 2:
-------

Select TEMPLATES

> **Note**
>
> Alternatively, if you haven’t navigated away from the job templates
> creation page, you can scroll down to see all existing job templates

Step 3:
-------

Click the rocketship icon ![Add](images/at_launch_icon.png) for the
**IIS Advanced** Job Template.

Step 4:
-------

When prompted, enter your desired test message

If successful, your standard output should look similar to the figure
below. Note that most of the tasks return OK because we’ve previously
configured the servers and services are already running.

![Job output](images/6-job-output.png)


When the job has successfully completed, you should see two URLs to your websites printed at the bottom of the job output. Verify they are still working.

Section 5: Review
=================

You should now have a completed playbook, `site.yml` with a single role
called `iis_simple`. The advantage of structuring your playbook into
roles is that you can now add reusability to your playbooks as well as
simplifying changes to variables, tasks, templates, etc.

[Ansible Galaxy](https://galaxy.ansible.com) is a good repository of
roles for use or reference.

