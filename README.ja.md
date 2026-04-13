---
layout: default
title: Ansible ワークショップ
patternfly: true
---

**他の言語でもお読みいただけます**:
<br>![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English]({{ '/' | relative_url }})、![japan](https://github.com/ansible/workshops/raw/devel/images/japan.png)[日本語]({{ '/README.ja' | relative_url }})

<div class="cards-layout">
  <aside class="cards-sidebar">
    <div class="cards-sidebar__header">
      <span>フィルター</span>
      <button id="filter-clear" class="cards-sidebar__clear">フィルターをクリア</button>
    </div>
    <div class="cards-sidebar__section">
      <h4 class="cards-sidebar__title">種類</h4>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="90-minute"> 90分
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="4-hour"> 4時間
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="6-hour"> 6時間
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="product-demos"> 製品デモ
      </label>
    </div>
    <div class="cards-sidebar__section">
      <h4 class="cards-sidebar__title">パートナー</h4>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="splunk"> Splunk
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="servicenow"> ServiceNow
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="cisco"> Cisco
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="microsoft"> Microsoft
      </label>
    </div>
  </aside>

  <div class="cards-main">
    <p id="guide-search-count" class="cards-search__count"></p>

    <div class="pf-v6-l-gallery pf-m-gutter cards-gallery" id="main-gallery">

      <!-- 90分ワークショップ -->

      <a target="_blank" href="https://rhpds.github.io/ai-driven-automation-showroom/modules/index.html" class="card-link" data-tags="90-minute,splunk">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                90分
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">AI + Ansible</h3>
          </div>
          <div class="pf-v6-c-card__body">
            AI 駆動型 Ansible 自動化と AIOps の入門。インテリジェントな自己修復型の自動化ワークフローを構築します。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">Splunk</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="https://rhpds.github.io/showroom-virt-aap-day-2/modules/index.html" class="card-link" data-tags="90-minute">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                90分
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Day 2 運用</h3>
          </div>
          <div class="pf-v6-c-card__body">
            OpenShift Virtualization を活用した自動化。AAP と OpenShift Virtualization で実行できる運用タスクを学びます。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="./exercises/instruqt/eda" class="card-link" data-tags="90-minute">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                90分
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">イベント駆動型 Ansible</h3>
          </div>
          <div class="pf-v6-c-card__body">
            EDA テクニカルワークショップ。ソース、ルール、アクションなど EDA の基礎を学びます。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="exercises/instruqt/ansible-cloud-lab" class="card-link" data-tags="90-minute">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                90分
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">クラウド自動化</h3>
          </div>
          <div class="pf-v6-c-card__body">
            クラウド自動化の入門。ハイブリッドクラウド環境のオーケストレーション、運用、ガバナンスを学びます。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="exercises/instruqt/lightspeed" class="card-link" data-tags="90-minute">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                90分
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Lightspeed</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Ansible Lightspeed と開発テクニカルワークショップ。自動化エンジニアやアプリケーション開発者向けの内容です。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="exercises/instruqt/network" class="card-link" data-tags="90-minute,cisco">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                90分
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">ネットワーク自動化</h3>
          </div>
          <div class="pf-v6-c-card__body">
            ネットワーク自動化入門。ルーターやスイッチに対する Ansible 自動化を学びます。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">Cisco</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="./exercises/ansible_rhel_90" class="card-link" data-tags="90-minute">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                90分
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">RHEL 自動化</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Ansible Red Hat Enterprise Linux ワークショップ。RHEL などの Linux プラットフォームの自動化を学びます。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="exercises/instruqt/servicenow" class="card-link" data-tags="90-minute,servicenow">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                90分
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">ServiceNow 自動化</h3>
          </div>
          <div class="pf-v6-c-card__body">
            ServiceNow 自動化入門。IT サービスマネジメント（ITSM）ツールと連携した Ansible 自動化を学びます。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">ServiceNow</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="exercises/instruqt/windows" class="card-link" data-tags="90-minute,microsoft">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                90分
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Windows 自動化</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Windows 自動化入門。Windows ホスト上のタスクを Ansible で自動化する方法を学びます。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">Microsoft</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP</span></span>
          </div>
        </div>
      </a>

      <!-- 4時間ワークショップ -->

      <a target="_blank" href="./exercises/instruqt/eda-4" class="card-link" data-tags="4-hour">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-blue">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                4時間
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">イベント駆動型 Ansible（拡張版）</h3>
          </div>
          <div class="pf-v6-c-card__body">
            EDA テクニカルワークショップ。ソース、ルール、アクションなど EDA の基礎を、より深いハンズオン演習で学びます。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="exercises/instruqt/lightspeed-4" class="card-link" data-tags="4-hour">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-blue">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                4時間
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Lightspeed（拡張版）</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Ansible Lightspeed と開発テクニカルワークショップ。自動化エンジニアやアプリケーション開発者向けの内容です。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="exercises/instruqt/aapcasc-4" class="card-link" data-tags="4-hour">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-blue">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                4時間
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Configuration as Code</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Ansible Automation Platform の構成管理をコードとして実現。CaC の考え方と実践を学びます。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP</span></span>
          </div>
        </div>
      </a>

      <!-- 6時間ワークショップ -->

      <a target="_blank" href="./exercises/ansible_rhel" class="card-link" data-tags="6-hour">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-green">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                6時間
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">RHEL 自動化（終日版）</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Ansible Red Hat Enterprise Linux ワークショップ。RHEL などの Linux プラットフォームの自動化を学びます。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="./exercises/ansible_network" class="card-link" data-tags="6-hour,cisco">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-green">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                6時間
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">ネットワーク自動化（終日版）</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Ansible ネットワーク自動化ワークショップ。Arista、Cisco、Juniper などのルーター・スイッチの自動化を学びます。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">Cisco</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="./exercises/ansible_windows" class="card-link" data-tags="6-hour,microsoft">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-green">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                6時間
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Windows 自動化（終日版）</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Ansible Windows 自動化ワークショップ。Microsoft Windows の自動化を学びます。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">Microsoft</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="./exercises/rhdp_auto_satellite" class="card-link" data-tags="6-hour">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-green">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                6時間
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible + Satellite</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Ansible + Satellite ワークショップ。Red Hat Satellite Server を使ったセキュリティおよびライフサイクル管理の自動化を学びます。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="./exercises/ansible_ripu" class="card-link" data-tags="6-hour">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-green">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                6時間
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">RHEL インプレースアップグレード</h3>
          </div>
          <div class="pf-v6-c-card__body">
            RHEL インプレースアップグレード自動化ワークショップ。エンタープライズ規模での RHEL インプレースアップグレードの自動化を学びます。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP</span></span>
          </div>
        </div>
      </a>

      <!-- 製品デモ -->

      <a target="_blank" href="./exercises/product_demos/" class="card-link" data-tags="product-demos">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-orange">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-play-circle pf-v6-c-label__icon"></i>
                製品デモ
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible 製品デモ</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Ansible Automation Platform のデモ、開発、実験のためのサンドボックス環境です。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP</span></span>
          </div>
        </div>
      </a>

    </div>

    <div class="cards-contributing">
      <h2>その他のリソース</h2>
    </div>

    <div class="cards-resources">
      <h2>セルフペースの演習</h2>
      <p><a href="https://red.ht/ansible-labs">Ansible Automation Platform セルフペースラボ</a> — 事前構成済みの環境で実験・学習できるインタラクティブなシナリオです。プラットフォームが実際の問題解決にどのように役立つかをご自分のペースで体験できます（各15〜30分）。</p>
    </div>

    <div class="cards-resources">
      <h2>YouTube チャンネル</h2>
      <ul>
        <li><a href="https://youtube.com/ansibleautomation">The Ansible Playbook</a> — テクニカルマーケティングエンジニアによる情報発信</li>
        <li><a href="https://www.youtube.com/@RedHatAnsible">Red Hat Ansible</a> — AnsibleFest セッション、製品発表など</li>
      </ul>
    </div>

    <div class="cards-resources">
      <h2>ドキュメントとトレーニング</h2>
      <ul>
        <li><a href="https://docs.ansible.com/ansible/latest/getting_started/index.html">Ansible 入門ガイド</a></li>
        <li><a href="https://docs.ansible.com/ansible/latest/network/getting_started/index.html">Ansible ネットワーク自動化 — 入門ガイド</a></li>
        <li><a href="https://red.ht/aap_training">Red Hat Ansible Automation Platform トレーニングと認定資格</a></li>
        <li><a href="http://red.ht/try_ansible">Ansible Automation Platform のトライアルサブスクリプション</a></li>
        <li><a href="https://forum.ansible.com/">Ansible コミュニティフォーラム</a></li>
      </ul>
    </div>

    <div class="cards-resources">
      <h2>ワークショップドキュメント</h2>
      <ul>
        <li><a href="docs/attendance/attendance.md">ワークショップ参加者向け Web サイト</a></li>
        <li><a href="docs/contribute.md">コントリビューションガイド</a></li>
        <li><a href="provisioner/README.md">AWS Lab Provisioner の使い方</a></li>
        <li><a href="docs/faq.md">よくある質問（FAQ）</a></li>
        <li><a href="docs/release.md">リリースプロセス</a></li>
      </ul>
    </div>
  </div>
</div>

<script>
(function () {
  var headerInput = document.getElementById('header-search');
  var filterClearBtn = document.getElementById('filter-clear');
  var countEl = document.getElementById('guide-search-count');
  var allCards = document.querySelectorAll('.card-link');
  var checkboxes = document.querySelectorAll('.cards-sidebar__checkbox input');

  if (!headerInput) return;

  function getCardText(card) {
    var title = card.querySelector('.pf-v6-c-card__title-text');
    var body = card.querySelector('.pf-v6-c-card__body');
    var labels = card.querySelectorAll('.pf-v6-c-label__content');
    var text = '';
    if (title) text += ' ' + title.textContent;
    if (body) text += ' ' + body.textContent;
    labels.forEach(function (l) { text += ' ' + l.textContent; });
    return text.toLowerCase();
  }

  function getActiveFilters() {
    var active = [];
    checkboxes.forEach(function (cb) {
      if (cb.checked) active.push(cb.value);
    });
    return active;
  }

  function filterCards() {
    var query = headerInput.value.toLowerCase().trim();
    var activeFilters = getActiveFilters();
    filterClearBtn.style.display = (activeFilters.length || query) ? 'inline' : 'none';

    var visible = 0;

    allCards.forEach(function (card) {
      var textMatch = !query || getCardText(card).indexOf(query) !== -1;
      var filterMatch = true;
      if (activeFilters.length) {
        var cardTags = (card.getAttribute('data-tags') || '').split(',').map(function (s) { return s.trim(); });
        filterMatch = activeFilters.some(function (f) { return cardTags.indexOf(f) !== -1; });
      }
      var show = textMatch && filterMatch;
      card.style.display = show ? '' : 'none';
      if (show) visible++;
    });

    if (query || activeFilters.length) {
      countEl.textContent = visible === 0
        ? 'フィルター条件に一致するワークショップはありません。'
        : visible + ' 件のワークショップが見つかりました。';
    } else {
      countEl.textContent = '';
    }
  }

  headerInput.addEventListener('input', filterCards);

  checkboxes.forEach(function (cb) {
    cb.addEventListener('change', filterCards);
  });

  filterClearBtn.addEventListener('click', function () {
    checkboxes.forEach(function (cb) { cb.checked = false; });
    headerInput.value = '';
    filterCards();
  });

  filterClearBtn.style.display = 'none';
})();
</script>
