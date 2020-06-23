# 演習 - プロジェクトとジョブテンプレート

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

* [目的](#目的)
* [Git リポジトリのセットアップ](#git-リポジトリのセットアップ)
* [プロジェクトの作成](#プロジェクトの作成)
* [ジョブテンプレートを作成してジョブを実行する](#ジョブテンプレートを作成してジョブを実行する)
* [チャレンジラボ: 結果の確認](#チャレンジラボ-結果の確認)
* [次のラボの準備も含め少し作業します](#次のラボの準備も含め少し作業します)

# 目的

Ansible Towerの **Project** は、Ansible Playbookの論理的なコレクションです。PlaybookをGit、Subversion、Mercurialなど、Towerがサポートしているソースコード管理（SCM）システムに配置して管理することができます。

この演習では以下の内容をカバーしています。
- Ansible Tower プロジェクトの理解と使用
- Gitリポジトリに保管されているAnsibleのプレイブックを使う
- Ansible のジョブテンプレートを作成して使用する

Playbook は SCM など、バージョン管理の仕組みの下に置いておくべきです。このラボでは、 Git リポジトリに保存されている Playbook を利用します。  

## Git リポジトリのセットアップ  
このデモでは、既に Git リポジトリに保存されているプレイブックを使用します。  

**https://github.com/ansible/workshop-examples**

このラボで利用する Apache Web Server をインストールするための Playbook は、上記 github サイトの **rhel/apache** に置いてある、`apache_install.yml` です。内容は以下の通りです。  

```yaml
---
- name: Apache server installed
  hosts: all

  tasks:
  - name: latest Apache version installed
    yum:
      name: httpd
      state: latest

  - name: latest firewalld version installed
    yum:
      name: firewalld
      state: latest

  - name: firewalld enabled and running
    service:
      name: firewalld
      enabled: true
      state: started

  - name: firewalld permits http service
    firewalld:
      service: http
      permanent: true
      state: enabled
      immediate: yes

  - name: Apache enabled and running
    service:
      name: httpd
      enabled: true
      state: started
```

> **ヒント**
>
> Engine の演習で書いた Playbook と比較するとちょっと違っているところがあります。重要なところは、 `become` が無いところと、 `hosts` の設定に `all` を指定しているところです。  

このリポジトリを Tower の **Source Control Management (SCM)** として利用するには **プロジェクト** を作成する必要があります。  

## プロジェクトの作成  

  - 左のメニューから **プロジェクト** を選択し、 ![plus](images/green_plus.png) ボタンをクリック。フォームに以下を入力します。  

  <table>
    <tr>
      <th>Parameter</th>
      <th>Value</th>
    </tr>
    <tr>
      <td>名前</td>
      <td>Workshop Project</td>
    </tr>
    <tr>
      <td>組織</td>
      <td>Default</td>
    </tr>
    <tr>
      <td>SCMタイプ</td>
      <td>Git</td>
    </tr>
  </table>

ここで、リポジトリにアクセスするためのURLが必要です。上記の Github リポジトリに移動し、右側の緑色の **Clone or download** ボタンをクリック。さらに、 **Clone with HTTPS** が選択されていることを確認し、URL をコピーします。  

> **Note**
>
> クリックする **httpsを使用** の項目がない場合でも、**SSHを使用** があれば問題ありません。URLをコピーするだけです。重要なのは、**https** で始まるURLをコピーすることです。

SCM URL にコピーした URL を貼り付けます。  

 <table>
   <tr>
     <th>Parameter</th>
     <th>Value</th>
   </tr>
   <tr>
     <td>SCM URL</td>
     <td><code>https://github.com/ansible/workshop-examples.git</code></td>
   </tr>
   <tr>
     <td>SCM 更新オプション</td>
     <td>上から3つのボックスにチェックマークを付けて、常にリポジトリの最新コピーを取得し、ジョブの起動時にリポジトリを更新する設定とします。</td>
   </tr>
 </table>

- **保存** をクリックします  

新しいプロジェクトは、作成後に自動的に同期されます。ただし、これを手動で行うこともできます。 **Projects** ビューに移動し、プロジェクトの右側にある円形矢印 **最新のSCMリビジョンを取得** アイコンをクリックすると、プロジェクトを Git リポジトリと再度同期します。  

## ジョブテンプレートを作成してジョブを実行する  

ジョブテンプレートは、Ansible ジョブを実行するための定義とパラメーターのセットです。ジョブテンプレートは、同じジョブを何度も実行するのに役立ちます。ジョブテンプレートではいくつかのパラメータを指定します。それぞれの意味は下記の通りです。  

- **インベントリー:** ジョブを実行するホストを指定します  

- **認証情報:** 管理対象ホストにログインするためのアカウント情報です  

- **プロジェクト:** Playbook の場所を指定します   

- **Playbook の指定**

早速 **ジョブテンプレート** を作成してみましょう。 

左のメニューから **テンプレート** を選択し、 ![plus](images/green_plus.png) ボタンをクリック。選択肢の中から **ジョブテンプレート** を選びます。    

> **ヒント**
>
> 下記フィールドの多くは、虫眼鏡アイコンをクリックの上オプション選択で設定が可能です。  

<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>名前</td>
    <td>Install Apache</td>
  </tr>
  <tr>
    <td>ジョブタイプ</td>
    <td>実行</td>
  </tr>
  <tr>
    <td>インベントリー</td>
    <td>Workshop Inventory</td>
  </tr>
  <tr>
    <td>プロジェクト</td>
    <td>Workshop Project</td>
  </tr>
  <tr>
    <td>PLAYBOOK</td>
    <td><code>rhel/apache/apache_install.yml</code></td>
  </tr>    
  <tr>
    <td>認証情報</td>
    <td>Workshop Credentials</td>
  </tr>
  <tr>
    <td>制限</td>
    <td>web</td>
  </tr>    
  <tr>
    <td>オプション</td>
    <td>root権限で実行するために **権限昇格の有効化** にチェックを入れます  </td>
  </tr>           
</table>

- **保存** をクリックします  

青い **起動** ボタンを直接クリックするか、テンプレートのビューでロケットアイコンをクリックしてジョブを開始します。ジョブテンプレートを起動すると、自動的にジョブの概要が表示され、Playbook の実行をリアルタイムで追跡できます。  


![job exection](images/job_overview.png)  


完了するまで少し時間がかかりますので、何を行っているか確認してみてください。  

- インベントリ、プロジェクト、認証情報のチェック、Playbook などのジョブテンプレートの詳細が表示されます  

- さらに、Playbook で変更された部分が記録されています  

- また、開始時刻と終了時刻を含む実行時間も記録されるため、ジョブの実行が実際にどれくらいかかったかがわかります  

- 右側に、プレイブック実行の出力が表示されます。タスクの下のノードをクリックして、各ノードの各タスクの詳細情報が提供されていることを確認します  

ジョブが完了したら、左のメニューからジョブをクリックします。すべてのジョブがここに一覧表示されます。Playbook を実行する前に、SCM 更新が開始されるのが分かります。これは、プロジェクト作成時に、 `起動時のリビジョン更新` にチェックを入れましたね？その Git 情報の更新です！  

## チャレンジラボ: 結果の確認  

以下に挑戦してみましょう！

  - アドホックコマンドを使用して、対象ホストに Apache がインストールされ、実行されていることを確認します。

確認する方法は以前のラボで学んでいると思いますので、考えてやってみてください。

> **ヒント**
>
> `systemctl status httpd` を使う！？

> **回答**

- **インベントリー** → **Workshop Inventory**

- **ホスト** をクリックし、対象ホストをチェックにより選択。さらに、 **コマンドの実行** をクリックします。

- 以下を記入します:

<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>モジュール</td>
    <td>command</td>
  </tr>
  <tr>
    <td>引数</td>
    <td>systemctl status httpd</td>
  </tr>
  <tr>
    <td>マシンの認証情報</td>
    <td>Workshop Credentials</td>
  </tr>   
</table>

- **起動** をクリック

----

[Ansible Tower ワークショップ表紙に戻る](../README.ja.md#section-2---ansible-towerの演習)
