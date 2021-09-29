# Workshop Exercise - Check the Prerequisites

**その他の言語はこちらをお読みください。**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## 目次

* [目的](#objective)
* [ガイド](#guide)
* [ラボ環境](#your-lab-environment)
* [Step 1 - ラボ環境へのアクセス](#step-1---access-the-environment)
* [Step 2 - ラボの作業](#step-2---working-the-labs)
* [Step 3 - チャレンジラボ](#step-3---challenge-labs)

## 目的

* ラボトポロジーと環境へのアクセス方法を理解する。
* ワークショップの演習の仕組みを理解する。
* チャレンジラボについて理解する。

## ガイド

### ラボ環境

このラボでは、事前設定されたラボ環境で作業します。ここでは、以下のホストにアクセスできます。

| Role                 | Inventory name |
| ---------------------| ---------------|
| Ansible Control Host | ansible-1      |
| Managed Host 1       | node1          |
| Managed Host 2       | node2          |
| Managed Host 3       | node3          |

### Step 1 - 環境へのアクセス

SSH 経由でコントロールホストにログインします。

> **Warning**
>
> **11.22.33.44** はお使いの環境の **IP** に変更します。student**X** の **X** は、指定の学習者 ID に変更します。

```bash
ssh studentX@11.22.33.44
```

> **ヒント**
>
> パスワードは、インストラクターから渡されます。

次に、root に切り替えます。

```bash
[student<X>@ansible-1 ~]$ sudo -i
```

以下のような前提条件タスクの多くは既に完了しています。

* Ansible ソフトウェアのインストール
* SSH 接続および鍵の設定
* root 権限が必要なコマンドを実行できるように、`sudo` が管理対象ホストで設定されています。

Ansible が正しくインストールされていることを確認します。

```bash
[root@ansible-1 ~]# ansible --version
ansible 2.7.0
[...]
```

> **注意** >
>
> Ansible では、設定管理を容易に保っています。データベースやデーモンを実行する必要はなく、ノートパソコン上で簡単に実行できます。管理対象ホストで、エージェントを実行する必要は必要ありません。

root アカウントから再度ログアウトします。

```bash
[root@ansible-1 ~]# exit
logout
```

> **注意** >
>
> 後続のすべての演習では、明示的に指示されない限り、コントロールノードで stundet\<X\> ユーザーとして作業してください。

### Step 2 - ラボの作業

おわかりの通り、このラボは、コマンドラインを中心に使います。

* すべてを手動入力する必要はありません。ブラウザーからコピーペーストしてください。ただし、特に手を止めて理解を深めるようにしてください。

* すべてのラボは、**Vim** を使用して準備しています。誰もが好むエディターではないことは承知しています。これは自由に変更できます。ラボ環境では
  **Midnight Commander** (**mc** を実行。ファンクションキーは Esc-\<n\> で、マウスクリックでも可能)
  を利用できます。または、**Nano** (**nano** と実行) も利用可能です。これは簡易紹介
  [エディター紹介](../0.0-support-docs/editor_intro.md) です。

> **ヒント** >
>
> このラボガイドでは、その状況で意味がわかりやすいかどうかに関係なく、予期される出力ありなしで、実行するコマンドが表示されます。

### Step 3 - チャレンジラボ

これらのラボガイドの多数の章には、「チャレンジラボ」セクションが用意されています。これらのラボは、これまで学んだ知識で解決するための小さなタスクを行うことを目的としています。タスクの回答は、警告サインの下に表示されます。

---
**ラビゲーション**
<br>
[次の演習](../1.2-adhoc)
<br><br>
[こちらをクリックして、Ansible for Red Hat Enterprise Linux ワークショップに戻ります](../README.md)
