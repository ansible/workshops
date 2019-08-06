# 演習 2.2 - インベントリー、認証情報、アドホックコマンド

## インベントリの作成

まず必要なのは、管理対象ホストの一覧です。これは Ansible Engine のインベントリファイルに相当します。インベントリーにはダイナミックインベントリーなど、高度なものもありますが、まずは基本的なところから始めてみましょう。  

  - ブラウザで **https://<Ansigle Control Host & Tower>/** に接続しログインします。  
  　ユーザーは `admin` パスワードはインストール時に指定した `ansibleWS` です。  

インベントリの作成:  

  - 左側のWeb UIメニューで、**インベントリー** をクリックし、右端の ![plus](images/green_plus.png) ボタンをクリック。表示されるプルダウンの中から、インベントリーを選択します。  

  - **名前:** Workshop Inventory  

  - **組織:** Default  

  - **保存** をクリック  

ブラウザ下部に、利用可能なインベントリーが表示されていますので確認してみましょう。 Ansible Tower にあらかじめ作成されている **Demo Inventory** と、今作成した **Workshop Inventory** の2つが存在していることが分かります。ブラウザ上部に戻って、 **Workshop Inventory** の中にある **ホスト** ボタンをクリックすると、まだホストを 1 台も登録していないのでリストが空であることが分かります。  

早速ホストを追加してみましょう。まず、登録するためのホスト一覧を取得する必要があります。このラボ環境では、Tower がインストールされている ansible Control Hot & Tower 上のインベントリーファイルに利用可能なホスト一覧が記述されていますのでそちらを確認してみます。  

Tower サーバーに SSH でログインします。  

> **注意**
> 
> student<X> の <X> の部分は、各自与えられた Student 番号を入力ください。また、11.22.33.44の部分は、各自与えられた、ansible Control Hot & Tower の IP アドレスを入力ください。  

```bash
ssh student<X>@11.22.33.44
```

インベントリーファイルの場所は、Tower ホスト上の、 `~/lab_inventory/hosts` です。 cat で確認してみましょう。

```bash
$ cat ~/lab_inventory/hosts 
[all:vars]
ansible_user=student<X>
ansible_ssh_pass=ansible
ansible_port=22

[web]
node1 ansible_host=22.33.44.55
node2 ansible_host=33.44.55.66
node3 ansible_host=44.55.66.77

[control]
ansible ansible_host=11.22.33.44
```
> **注意**
> 
> 表示される IP アドレスは各自固有のものになっていますので、上記とは異なります。  

node1、node2 などのホストの名前と IP addresses を控えておいてください。これらの情報を以下の手順で Tower のインベントリーに登録していきます。  

  - Tower のインベントリービューで **Workshop Inventory** をクリックします  

  -  **HOSTS** をクリックします  

  -  ![plus](images/green_plus.png) ボタンをクリックします  

  - **ホスト名** `node1`  

  - **変数** 3つのハイフン `---` の下（2行目）に、 `ansible_host: 22.33.44.55` を入力します。 IP アドレス、`22.33.44.55` については、先ほど `node1` について確認した IP アドレスに置き換えてください。記述方法についても注意してください。コロン **:** と IP アドレスの間にはスペースが必要です。また、インベントリーファイルで利用するような **=** で記述してはいけません。  

  -  **保存** をクリックします  

  -  **ホスト** に戻って `node2` と `node3` を上記と同様の手順で追加します。  
  
これで Tower で管理する 3 台のホストに対するインベントリーファイルの作成が完了です♬  

## マシンの認証情報

Ansible Tower は、ホストやクラウド等の認証情報をユーザーに開示せずに利用可能にするという優れた機能を持っています。 Tower がインベントリー登録したリモートホスト上でジョブを実行できるようにするには、リモートホストの認証情報を設定する必要があります。

> **メモ**
> 
> これは Tower が持っている重要な機能の一つ **認証情報の分離の機能です**\! 認証情報はホストやインベントリーの設定とは別で強固に管理することが可能です。

Tower の重要な機能なので、まずはコマンドラインでラボ環境について確認してみましょう。  

SSH 経由で Tower ホストにログインします。  

  - いつものように、<X> の部分と、Tower ホストのアドレスは各自のものに置き換えてください。  

  - `node1` に SSH 接続し、 `sudo -i` を実行してみます。 SSH 接続の際はパスワード入力が要求されますが、 `sudo -i` に関してはパスワードは要求されません。  

```bash
[student<X>@ansible ~]$ ssh student<X>@22.33.44.55
student<X>@22.33.44.55's password: 
Last login: Thu Jul  4 14:47:04 2019 from 11.22.33.44
[student<X>@node1 ~]$ sudo -i
[root@node1 ~]#
```

これはどういう意味でしょう？  

  - Tower ユーザーである **ansible** は、インベントリーで指定した管理対象ホストにパスワードベースの SSH で接続可能  

  - ユーザー **ansible** は、 `sudo`  による権限昇格で、**root** としてコマンド実行が可能  

## マシン認証情報の作成  

では早速 Tower で認証情報を作成してみましょう。 Tower　左側のメニューから **認証情報** をクリックします。  

Click the ![plus](images/green_plus.png) button to add new credentials  
    
  - **名前** Workshop Credentials  

  - **組織** Default  

  - **認証情報のタイプ** 虫眼鏡をクリックして **マシン** を選択し、**選択**  をクリックします  

  - **ユーザー名** student\<X\> - make sure to replace the **\<X\>** with your actual student number!

  - **PASSWORD:** Enter the password which is provided by the instructor.

  - **PRIVILEGE ESCALATION METHOD:** sudo

  - Click **SAVE**

  - Go back to the **RESOURCES** → **Credentials** → **Workshop Credentials** and note that the password is not visible.

> **Tip**
> 
> Whenever you see a magnifiying glass icon next to an input field, clicking it will open a list to choose from.

You have now setup credentials to use later for your inventory hosts.

## Run Ad Hoc Commands

As you’ve probably done with Ansible before you can run ad hoc commands from Tower as well.

  - In the web UI go to **RESOURCES → Inventories → Workshop Inventory**

  - Click the **HOSTS** button to change into the hosts view and select the three hosts by ticking the boxes to the left of the host entries.

  - Click **RUN COMMANDS**. In the next screen you have to specify the ad hoc command:
    
      - As **MODULE** choose **ping**
    
      - For **MACHINE CREDENTIAL** click the magnifying glass icon and select **Workshop Credentials**.
    
      - Click **LAUNCH**, and watch the output.

The simple **ping** module doesn’t need options. For other modules youneed to supply the command to run as an argument. Try the **command** module to find the userid of the executing user using an ad hoc command.
  
- **MODULE:** command

- **ARGUMENTS:** id

> **Tip**
> 
> After choosing the module to run, Tower will provide a link to the docs page for the module when clicking the question mark next to "Arguments". This is handy, give it a try.

How about trying to get some secret information from the system? Try to print out */etc/shadow*.
    
- **MODULE:** command

- **ARGUMENTS:** cat /etc/shadow

> **Warning**
> 
> **Expect an error\!**

Oops, the last one didn’t went well, all red.

Re-run the last ad hoc command but this time tick the **ENABLE PRIVILEGE ESCALATION** box.

As you see, this time it worked. For tasks that have to run as root you need to escalate the privileges. This is the same as the **become: yes** you’ve probably used often in your Ansible Playbooks.

## Challenge Lab: Ad Hoc Commands

Okay, a small challenge: Run an ad hoc to make sure the package "tmux" is installed on all hosts. If unsure, consult the documentation either via the web UI as shown above or by running `[ansible@tower ~]$ ansible-doc yum` on your Tower control host.

> **Warning**
> 
> **Solution below\!**

  - **MODULE:** yum

  - **ARGUMENTS:** name=tmux

  - Tick **ENABLE PRIVILEGE ESCALATION**

> **Tip**
> 
> The yellow output of the command indicates Ansible has actually done something (here it needed to install the package). If you run the ad hoc command a second time, the output will be green and inform you that the package was already installed. So yellow in Ansible doesn’t mean "be careful"…​ ;-).

----

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-2---ansible-tower-exercises)

