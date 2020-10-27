# Exercise 1.1 - 要件を確認してみよう

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## 目次

* [目的](#目的)
* [ガイド](#ガイド)
* [ラボ環境について](#ラボ環境について)
* [Step 1 - 環境へのアクセス](#step-1---環境へのアクセス)
* [Step 1 - Working the Labs](#step-2---working-the-labs)
* [Step 1 - チャレンジLabs](#step-3---チャレンジlabs)

# 目的

- ラボの構成および環境へのアクセス方法を理解する
- ワークショップのエクササイズについて理解する
- チャレンジラボについて理解する

# ガイド

## ラボ環境について

このラボでは、事前設定されたラボ環境で作業します。 以下のホストにアクセスできます。

| Role                 | Inventory name |
| ---------------------| ---------------|
| Ansible Control Host | ansible        |
| Managed Host 1       | node1          |
| Managed Host 2       | node2          |
| Managed Host 2       | node3          |

## Step 1.1 - 環境へのアクセス

SSHでログインできます。:

> **Warning**
>
>  **11.22.33.44** のような文字列を、個々に提供されているStudent情報に記載の **IP** などへ読み替えてください。 **X** は student**X** といった具合です。

    ssh studentX@11.22.33.44

> **Tip**
>
> パスワードは **インストラクターから指示されたパスワード** です。

rootになるには以下のように実行してください。:

    [student<X>@ansible ~]$ sudo -i

ほとんどの前提条件タスクはすでに行われています。:

  - Ansible はすでにインストールされています。

  - SSH connection と keyはすでに設定済みです。

  - root権限を必要とするコマンドを実行できるように、`sudo` は適切に設定され、権限昇格が可能になっているはずです。

Ansibleが適切にインストールされているかを確認しましょう。

    [root@ansible ~]# ansible --version
    ansible 2.7.0
    [...]

> **Note**
>
> Ansibleは構成管理を単純にしてくれます。 Ansibleはデータベースや実行用のデーモンを必要とせず、ラップトップでも簡単に実行できます。 管理対象ホストでは、実行用の常駐エージェントなども不要です。

rootアカウントからログアウトします。

    [root@ansible ~]# exit
    logout

> **Note**
>
> 以降のすべての演習では、明示的な指示がない限り、コントロールノードのstudent\<X\> ユーザーとして作業してください。

## Step 2 - Working the Labs

ここからのラボについては、コマンドライン操作ばっかりだと思うかもしれません。:-)

  - すべて手で入力するのではなく、必要に応じてブラウザからコピー＆ペーストしてください。しかし、考えたり理解したりするのをやめたりしないでください。

  - すべてのラボは **Vim** を使って準備しましたが、みんながそれを愛しているわけではないことを理解しています。 **Midnight Commander** などを利用することができます。(**mc**を 実行すると実行できます。ファンクションキーはEsc-\<n\>でアクセスするかマウスでクリックすることでアクセスできます。）。または **Nano**（**nano**を実行）なども利用できます。 簡単な[editor intro](../0.0-support-docs/editor_intro.md)も用意してあります。

> **ヒント**
>
> あなたが実行するラボガイドのコマンドは、期待される出力の有無にかかわらず、文脈の中でより意味のあるものが何であれ表示されます。

## Step 3 - チャレンジラボ

このラボガイドの様々な章で「チャレンジラボ」セクションがあります。
これらのラボは、これまでに学んだことを使って解決するための様々なタスクを用意しています。
それぞれのラボの解答案は、`Warning`サインより下に記述されています。

----
**ナビゲーション**
<br>
[次のエクササイズ](../1.2-adhoc/README.ja.md)
<br><br>
[Ansible Engine ワークショップ表紙に戻る](../README.ja.md#section-1---ansible-engineの演習)
