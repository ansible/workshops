# 演習 1.5 - Playbookの実行とレビュー

おめでとうございます! Ansibleのキーコンセプトを使ったPlaybookが出来上がりました。興奮しすぎる前に実際に実行してみましょう。もしPlaybookに問題があった場合は、ここに動くサンプルがあります: [router_configs.yml](router_configs.yml)

## 目次
 - [セクション 1 - routing_configs playbookの実行](#section-1---running-your-routing_configs-playbook)
 - [セクション 2: レビュー](#section-2-review)
 - [セクション 3: テスト!](#section-3-test)

## セクション 1 - routing_configs playbookの実行

### ステップ 1: 正しいディレクトリにいることを確認

```bash
cd ~/networking-workshop
```

### ステップ 2: playbookの実行

```bash
ansible-playbook router_configs.yml
```

## セクション 2: レビュー

うまくいけば、以下とよく似た標準出力が見れるはずです。もしうまくいかなかった時は教えてください。直すのをお手伝いします。

![Figure 1: routing_configs stdout](playbookrun.png)

出力が上と似ていれば、Playbookは無事に実行されました。

それでは、簡単にここまでのおさらいをしましょう。

 - 適用したいサーバーの名前を変数として宣言しました
 - それから、ios_factsモジュールが生成した値をPlaybookの後のタスクで使用できるように登録しました
 - 次に{inventory_hostname}を使って条件のブロックを作りました
 - 条件が合った時、すなわちrtr1の時はスタティックルートとネームサーバの設定を適用しました
 - rtr2の場合はGigabitEthernet1をenable、DHCPアドレスを受け取れるように設定、rtr1と同様のスタティックルートとネームサーバの設定をしました

## セクション 3: テスト!

異なるVPCにあるホストにPingができるはずです。2つのVPCをGREトンネルで繋ぎ、2つのサブネット間でルーティングできるようにスタティックルートを追加しました。

```bash
ping <private IP of host node>
```

ホストノードのIPアドレスは、インベントリーファイル ~/networking-workshop/lab_inventory/student(x).net-ws.hosts に private_ip=172.16.x.x として記載されています。

例:
```bash
[ec2-user@ip-172-17-3-27 networking-workshop]$ ping 172.18.4.188
PING 172.18.4.188 (172.18.4.188) 56(84) bytes of data.
64 bytes from 172.18.4.188: icmp_seq=2 ttl=62 time=2.58 ms
64 bytes from 172.18.4.188: icmp_seq=3 ttl=62 time=3.52 ms
```
**Note** IPアドレスは172.18.4.188とは違うかもしれません!

# 完了
演習1.5が終了しました

# Answer Key
[ここをクリック](https://github.com/network-automation/linklight/blob/master/exercises/networking/1.5-run_routing_configs/router_configs.yml).

 ---
[Ansible Linklight - ネットワークワークショップ に戻る](../README.ja.md)
