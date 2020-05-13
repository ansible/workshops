# Exercise 1.1 - 要件を確認してみよう

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

* [ラボ環境について](#ラボ環境について)
* [Step 1.1 - 環境へのアクセス](#step-11---環境へのアクセス)
* [Step 1.2 - Working the Labs](#step-12---working-the-labs)
* [Step 1.3 - チャレンジLabs](#step-13---チャレンジlabs)

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
> パスワードは **instructor provides this** です。

rootになるには以下のように実行してください。:

    [student<X>@ansible ~]$ sudo -i

ほとんどの前提条件タスクはすでに行われています。:

  - Ansible はすでにインストールされています。

  - SSH connection と keyはすでに設定済みです。

  - root権限を必要とするコマンドを実行できるように、`sudo` は適切に設定され、権限昇格が可能になっているはずです。

Ansibleが適切にInstallされているかを確認しましょう。

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

## Step 1.2 - Working the Labs

ここからのラボについては、かなりコマンドラインばかりだと思うかもしれません。:-)

  - すべて手で入力するのではなく、必要に応じてブラウザからコピー＆ペーストしてください。しかし、考えたり理解したりするのをやめたりしないでください。

  - すべてのラボは **Vim** を使って準備しましたが、みんながそれを愛しているわけではないことを理解しています。 **Midnight Commander** などを利用することができます。(**mc**を 実行すると実行できます。ファンクションキーはEsc-\<n\>でアクセスするかマウスでクリックすることでアクセスできます。）。または **Nano**（**nano**を実行）なども利用できます。 簡単な[editor intro](../0.0-support-docs/editor_intro.md)も用意してあります。



## Step 1.3 - チャレンジLabs

このラボガイドの様々な章で「チャレンジラボ」セクションがあります。
これらのラボは、これまでに学んだことを使って解決するための様々なタスクを用意しています。
それぞれのラボの解答案は、`Warning`サインより下に記述されています。

----

[Ansible Engine ワークショップ表紙に戻る](../README.ja.md#section-1---ansible-engineの演習)
