# 演習 2.5 - ロールベースのアクセス制御

Ansible Tower の優れた機能として、認証情報を Tower 内部で適切に管理する方法を学びました。Ansible Tower のもう1つの利点は、ユーザーとグループの権限管理です。  

## Ansible Tower ユーザー  

Ansible Tower のユーザーには以下の3つのタイプがあります    

- **Normal User** インベントリやプロジェクトなどのオブジェクトに対する読み込み、書き込み権限は、そのユーザーに与えらたロールや権限に限定される    

- **System Auditor** Ansible Tower 環境内のすべてのオブジェクトの読み取り専用権限を有します  

- **System Administrator** Ansible Tower 環境内のすべてのオブジェクトに対して読み取り、書き込みの権限があります  

早速ユーザーを作成しましょう  

- 左のメニュー一覧から **ユーザー**をクリックします  

- 緑色のプラスボタンをクリックします  

- 新しいユーザーに関する情報を入力します  
  
    - **名** Werner  
  
    - **姓** Web  
  
    - **メール** wweb@example.com  
   
    - **ユーザー名** wweb  
  
    - **ユーザータイプ** Normal User  
  
    - **パスワード** ansible  
  
    - Confirm password  

- **保存**をクリック  

## Ansible Tower チーム  

チームは、ユーザー、プロジェクト、資格情報、および権限が関連付けられた組織の下位区分です。チームは、ロールベースのアクセス制御スキームを実装し、組織全体に責任を委任する手段を提供します。たとえば、チームの各ユーザーではなく、チーム全体に権限が付与される場合があります。  

チームを作成します  

- 左のメニューで**チーム**をクリック  

- 緑色のプラスボタンをクリックして、 `Web Content` という名前のチームを作成します  

- **保存**をクリックします  

これでユーザーをチームに登録することができます。  

- チーム `Web Content` 内の **ユーザー** ボタンをクリックします  

- 緑色のプラスボタンをクリックし、wweb ユーザーの横にあるチェックボックスをオンにして、**保存**をクリックします。  

今度は、**パーミッション** ボタンをクリックしてみてください。 "パーミッションが付与されていません"と表示されていると思います。  

権限を付与することにより、プロジェクト、インベントリ、およびその他の Ansible Tower 内のオブジェクトの読み取り、変更、および管理が可能になります。この権限は、Ansible Tower で管理するさまざまなリソースに設定できます。このあたりの柔軟性が Tower のもう一つの大きな特徴です。

## パーミッションの付与

ユーザーまたはチームが Ansible Tower 上で作業する場合、作業に対する適切なアクセス権限を持っている必要があります。新規に作成したユーザー wweb に対し、割り当てられた Web サーバーのコンテンツの変更のみを許可してみましょう。

To allow users or teams to actually do something, you have to set permissions. The user **wweb** should only be allowed to modify content of the assigned webservers.

Add the permission to use the template:

- In the Permissions view of the Team `Web Content` click the green plus button to add permissions.

- A new window opens. You can choose to set permissions for a number of resources.
  
    - Select the resource type **JOB TEMPLATES**
  
    - Choose the `Create index.html` Template by ticking the box next to it.

- The second part of the window opens, here you assign roles to the selected resource.
  
    - Choose **EXECUTE**

- Click **SAVE**

## Test Permissions

Now log out of Tower’s web UI and in again as the **wweb** user.

- Go to the **Templates** view, you should notice for wweb only the `Create
  index.html` template is listed. He is allowed to view and lauch, but not to edit the Template.

- Run the Job Template by clicking the rocket icon. Enter the survey content to your liking and launch the job.

- In the following **Jobs** view have a good look around, note that there where changes to the host (of course…​).

Check the result: execute `curl` again on the control host to pull the content of the webserver on the IP address of `node1`:

```bash
$ curl http://22.33.44.55
```

Just recall what you have just done: You enabled a restricted user to run an Ansible Playbook

  - Without having access to the credentials

  - Without being able to change the Playbook itself

  - But with the ability to change variables you predefined\!

Effectively you provided the power to execute automation to another user without handing out your credentials or giving the user the ability to change the automation code. And yet, at the same time the user can still modify things based on the surveys you created.

This capability is one of the main strengths of Ansible Tower\!

----

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-2---ansible-tower-exercises)
