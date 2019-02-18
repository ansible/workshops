# Exercise 4 - apache-basic-playbookを実行する

おめでとうございます!
ここまでで、全てではないにしてもAnsibleの主要なコンセプトのほとんどを含んだPlaybookを書き終えることができました。
まずは実際に実行できるかを確認してみましょう。

では、始めます。

## Section 1 - apache-basic-playbookを実行する

### Step 1:

適切なディレクトリに居ることを確認します。

```bash
cd ~/apache-basic-playbook
```


### Step 2:

playbookを実行します。


```bash
ansible-playbook site.yml
```

## Section 2: この演習の最後に

問題なく実行された場合、以下のような内容が標準出力として表示されます。
エラーが表示される場合は、問題箇所を特定するのでお知らせください。

![apache-basic-playbookの標準出力](stdout_2.png)

台数などがサンプルと異なる場合がありますが気にしないでください。

---

[Click Here to return to the Ansible Linklight - Ansible Engine Workshop](../README.ja.md)
