---
layout: default
title: Ansible 工作坊
lang: zh-CN
patternfly: true
---

**其他语言版本**：
<br>![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English]({{ '/' | relative_url }})，![japan](https://github.com/ansible/workshops/raw/devel/images/japan.png)[日本語]({{ '/README.ja' | relative_url }})，![cn](https://github.com/ansible/workshops/raw/devel/images/cn.png)[简体中文]({{ '/README.zh' | relative_url }})

<div class="cards-layout">
  <aside class="cards-sidebar">
    <div class="cards-sidebar__header">
      <span>筛选</span>
      <button id="filter-clear" class="cards-sidebar__clear">清除筛选</button>
    </div>
    <div class="cards-sidebar__section" data-filter-group="domain">
      <h4 class="cards-sidebar__title">领域</h4>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="gettingstarted"> 入门
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="linux"> Linux
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="network"> 网络
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="general"> 通用
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="ai"> AI
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="developer"> 开发者
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="cloud"> 云
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="windows"> Windows
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="virt"> 虚拟化
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="security"> 安全
      </label>
    </div>
    <div class="cards-sidebar__section" data-filter-group="type">
      <h4 class="cards-sidebar__title">类型</h4>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="lab"> 实验
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="workshop"> 工作坊
      </label>
    </div>
    <div class="cards-sidebar__section" data-filter-group="time">
      <h4 class="cards-sidebar__title">时长</h4>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="2plushours"> 2 小时以上
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="60to90min"> 60–90 分钟
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="under60min"> 60 分钟以内
      </label>
    </div>
    <div class="cards-sidebar__section" data-filter-group="tmm">
      <h4 class="cards-sidebar__title">TMM</h4>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="tmm"> TMM
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="nontmm"> 非 TMM
      </label>
    </div>
    <div class="cards-sidebar__section" data-filter-group="availability">
      <h4 class="cards-sidebar__title">可用性</h4>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="public"> 公开
      </label>
    </div>
  </aside>

  <div class="cards-main">
    <div class="cards-intro">
      <p><strong>工作坊（Workshops）</strong>是面向课堂或活动交付的综合性讲师引导动手课程。时长通常为 60 分钟至数小时，包含演示文稿、引导式练习，以及从基础到实际应用的结构化学习路径。</p>
      <p><strong>实验（Labs）</strong>是聚焦特定主题或技能的自主动手练习。时间更短（通常不到 60 分钟），可在 Red Hat Demo Platform 上单独启动，无需讲师。</p>
    </div>

    <p id="guide-search-count" class="cards-search__count"></p>

    <div class="cards-sections">

      <!-- ========== GETTING_STARTED ========== -->
      <section class="cards-section">
        <h2 class="cards-section__heading">入门</h2>
        <div class="pf-v6-l-gallery pf-m-gutter cards-gallery">

      <a href="./exercises/day-in-the-life" target="_blank" class="card-link" data-tags="gettingstarted,workshop,2plushours,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-green">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                2 小时以上
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Mission Critical Automation</h3>
          </div>
          <div class="pf-v6-c-card__body">
            体验使用 Ansible Automation Platform 的自动化工程师典型一天。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">工作坊</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/roadshow01" target="_blank" class="card-link" data-tags="gettingstarted,lab,under60min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">AAP Roadshow #1 - Introspection</h3>
          </div>
          <div class="pf-v6-c-card__body">
            AAP Roadshow 模块，聚焦审视并理解你的自动化环境。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/roadshow02" target="_blank" class="card-link" data-tags="gettingstarted,lab,under60min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">AAP Roadshow #2 - Standardization</h3>
          </div>
          <div class="pf-v6-c-card__body">
            AAP Roadshow 模块，聚焦自动化标准化与治理。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/roadshow03" target="_blank" class="card-link" data-tags="gettingstarted,lab,under60min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">AAP Roadshow #3 - Operational Efficiency</h3>
          </div>
          <div class="pf-v6-c-card__body">
            AAP Roadshow 模块，聚焦运营效率与自动化规模化。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          </div>
        </div>
      </a>

        </div>
      </section>

<!-- ========== DEVELOPER ========== -->
      <section class="cards-section">
        <h2 class="cards-section__heading">开发者</h2>
        <div class="pf-v6-l-gallery pf-m-gutter cards-gallery">

      <a href="./exercises/dev-tools" target="_blank" class="card-link" data-tags="developer,workshop,lab,60to90min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                2 小时
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Development Tools Workshop</h3>
          </div>
          <div class="pf-v6-c-card__body">
            在预置的 VS Code 环境中，使用 DevTools 套件创建、测试并打包 Ansible collection。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP Zero</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">工作坊</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/dev-tools-extended" target="_blank" class="card-link" data-tags="developer,workshop,lab,2plushours,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-green">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                3 小时
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Development Tools Workshop (Extended)</h3>
          </div>
          <div class="pf-v6-c-card__body">
            在 OpenShift Dev Spaces 上通过 Ansible Workspaces 完成完整 DevTools 生命周期——使用完整的 ansible-dev-tools 套件与 VS Code 创建、测试并部署自动化内容。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">工作坊</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="https://catalog.demo.redhat.com/catalog?search=ansible&item=babylon-catalog-prod%2Fsandboxes-gpte.rhdh-ansible-demo.prod" class="card-link" data-tags="developer,lab,under60min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Plug-ins for Red Hat Developer Hub Demo</h3>
          </div>
          <div class="pf-v6-c-card__body">
            面向 Red Hat Developer Hub 的 Ansible 插件演示环境。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/ansible-builder" target="_blank" class="card-link" data-tags="developer,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Get started with ansible-builder</h3>
          </div>
          <div class="pf-v6-c-card__body">
            入门 ansible-builder，创建自定义执行环境。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>

            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884763','_blank')"><span class="pf-v6-c-label__content">公开实验</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/lightspeed-101" target="_blank" class="card-link" data-tags="developer,lab,60to90min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60–90 分钟
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Getting started with automation coding assistant</h3>
          </div>
          <div class="pf-v6-c-card__body">
            使用 Ansible VS Code 扩展中的自动化编程助手，根据自然语言描述生成 playbook。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          </div>
        </div>
      </a>

        </div>
      </section>

<!-- ========== AI ========== -->
      <section class="cards-section">
        <h2 class="cards-section__heading">AI</h2>
        <div class="pf-v6-l-gallery pf-m-gutter cards-gallery">

      <a target="_blank" href="./exercises/ai-ansible" class="card-link" data-tags="ai,workshop,2plushours,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-green">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                2 小时以上
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Introduction to AI-Driven Ansible Automation: Self-healing</h3>
          </div>
          <div class="pf-v6-c-card__body">
            AI 驱动的 Ansible 自动化与 AIOps 入门。构建智能、可自愈的自动化工作流。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">工作坊</span></span>
          </div>
        </div>
      </a>

        </div>
      </section>

<!-- ========== LINUX ========== -->
      <section class="cards-section">
        <h2 class="cards-section__heading">Linux</h2>
        <div class="pf-v6-l-gallery pf-m-gutter cards-gallery">

      <a target="_blank" href="./exercises/rhel" class="card-link" data-tags="linux,workshop,2plushours,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-green">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                6 小时
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible for Red Hat Enterprise Linux</h3>
          </div>
          <div class="pf-v6-c-card__body">
            全天 RHEL 自动化工作坊。聚焦 Red Hat Enterprise Linux 等 Linux 平台自动化。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">工作坊</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="./exercises/rhel-90" class="card-link" data-tags="linux,workshop,60to90min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                90 分钟
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible for Red Hat Enterprise Linux (90 min)</h3>
          </div>
          <div class="pf-v6-c-card__body">
            90 分钟 RHEL 自动化工作坊。聚焦 Red Hat Enterprise Linux 等 Linux 平台自动化。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">工作坊</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/ripu" target="_blank" class="card-link" data-tags="linux,lab,2plushours,nontmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-green">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                2 小时以上
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">RHEL In-place Upgrade Automation Workshop</h3>
          </div>
          <div class="pf-v6-c-card__body">
            RHEL 原地升级自动化工作坊。聚焦企业规模的 RHEL 原地升级自动化。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">Non TMM</span></span>
          </div>
        </div>
      </a>

        </div>
      </section>

<!-- ========== WINDOWS ========== -->
      <section class="cards-section">
        <h2 class="cards-section__heading">Windows</h2>
        <div class="pf-v6-l-gallery pf-m-gutter cards-gallery">

      <a target="_blank" href="./exercises/windows" class="card-link" data-tags="windows,workshop,60to90min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                90 分钟
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Intro to Windows Automation (90 min)</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Windows 自动化入门。聚焦使用 Ansible 自动化 Windows 主机上的任务。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">工作坊</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/windows-ad" target="_blank" class="card-link" data-tags="windows,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Intro to Windows Automation - Active Directory</h3>
          </div>
          <div class="pf-v6-c-card__body">
            聚焦使用 Ansible 进行 Active Directory 管理的 Windows 自动化。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>

            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884845','_blank')"><span class="pf-v6-c-label__content">公开实验</span></span>
          </div>
        </div>
      </a>

        </div>
      </section>

<!-- ========== NETWORK ========== -->
      <section class="cards-section">
        <h2 class="cards-section__heading">网络</h2>
        <div class="pf-v6-l-gallery pf-m-gutter cards-gallery">

      <a target="_blank" href="./exercises/network-6" class="card-link" data-tags="network,workshop,2plushours,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-green">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                6 小时
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Network Automation Workshop</h3>
          </div>
          <div class="pf-v6-c-card__body">
            全天网络自动化工作坊。涵盖网络基础以及面向网络设备的 Ansible Automation Platform。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">工作坊</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="./exercises/network" class="card-link" data-tags="network,workshop,60to90min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                90 分钟
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Introduction to Ansible Network Automation Workshop</h3>
          </div>
          <div class="pf-v6-c-card__body">
            网络自动化入门。聚焦针对路由器与交换机的 Ansible 自动化。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">工作坊</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/eda-netbox" target="_blank" class="card-link" data-tags="network,lab,60to90min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60–90 分钟
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Event-Driven Ansible and Netbox as a source of truth</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Event-Driven Ansible 与 NetBox 集成，构建网络自动化单一事实来源。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/network-first-playbook" target="_blank" class="card-link" data-tags="network,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Network Automation: First Playbook</h3>
          </div>
          <div class="pf-v6-c-card__body">
            使用 Ansible 编写你的第一个网络自动化 playbook。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>

            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884830','_blank')"><span class="pf-v6-c-label__content">公开实验</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/network-backup-restore" target="_blank" class="card-link" data-tags="network,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Network Automation: Backup and Restore</h3>
          </div>
          <div class="pf-v6-c-card__body">
            使用 Ansible 实现网络配置备份与恢复自动化。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>

            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884831','_blank')"><span class="pf-v6-c-label__content">公开实验</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/network-resource-modules" target="_blank" class="card-link" data-tags="network,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Network Automation: Resource Modules</h3>
          </div>
          <div class="pf-v6-c-card__body">
            使用 Ansible 网络资源模块实现声明式网络管理。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>

            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884832','_blank')"><span class="pf-v6-c-label__content">公开实验</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/network-surveys" target="_blank" class="card-link" data-tags="network,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Network Automation: Surveys</h3>
          </div>
          <div class="pf-v6-c-card__body">
            使用 Automation Controller surveys 实现自助网络自动化。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>

            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884835','_blank')"><span class="pf-v6-c-label__content">公开实验</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/network-facts" target="_blank" class="card-link" data-tags="network,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Network Automation: Facts</h3>
          </div>
          <div class="pf-v6-c-card__body">
            使用 Ansible 收集并利用网络设备 facts。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>

            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884833','_blank')"><span class="pf-v6-c-label__content">公开实验</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/network-visibility" target="_blank" class="card-link" data-tags="network,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Network Automation: Infrastructure Visibility</h3>
          </div>
          <div class="pf-v6-c-card__body">
            使用 Ansible 实现网络基础设施可见性与报告。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>

            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884834','_blank')"><span class="pf-v6-c-label__content">公开实验</span></span>
          </div>
        </div>
      </a>

        </div>
      </section>

<!-- ========== SECURITY ========== -->
      <section class="cards-section">
        <h2 class="cards-section__heading">安全</h2>
        <div class="pf-v6-l-gallery pf-m-gutter cards-gallery">

      <a href="./exercises/zero-trust" target="_blank" class="card-link" data-tags="security,workshop,lab,2plushours,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-green">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                2 小时以上
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Implementing Zero Trust with Ansible Automation Platform</h3>
          </div>
          <div class="pf-v6-c-card__body">
            使用 Ansible Automation Platform 实施零信任安全架构。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">工作坊</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/defend-contain-comply" target="_blank" class="card-link" data-tags="security,workshop,lab,2plushours,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-green">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                2 小时以上
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Defend, Contain, Comply — Vulnerability Lifecycle Automation with Ansible Automation Platform</h3>
          </div>
          <div class="pf-v6-c-card__body">
            动手实践漏洞管理——使用 Ansible Automation Platform 检测并遏制 CVE、执行策略门控补丁，并验证合规。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">工作坊</span></span>
          </div>
        </div>
      </a>

      <div class="card-link" data-tags="security,workshop,lab,60to90min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60–90 分钟
              </span>
            </span>
            <span class="pf-v6-c-label pf-m-gold pf-m-compact" style="margin-left:8px;">
              <span class="pf-v6-c-label__content">Proposed</span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Compliance &amp; Hardening - Foundational security with AAP</h3>
          </div>
          <div class="pf-v6-c-card__body">
            使用 Ansible Automation Platform 开展基础安全合规与加固。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">工作坊</span></span>
          </div>
        </div>
      </div>

      <div class="card-link" data-tags="security,workshop,lab,60to90min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60–90 分钟
              </span>
            </span>
            <span class="pf-v6-c-label pf-m-gold pf-m-compact" style="margin-left:8px;">
              <span class="pf-v6-c-label__content">Proposed</span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Hack and Heal - Responsive Security with AAP</h3>
          </div>
          <div class="pf-v6-c-card__body">
            使用 Ansible Automation Platform 实现响应式安全——包含攻防与修复练习。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">工作坊</span></span>
          </div>
        </div>
      </div>

      <div class="card-link" data-tags="security,workshop,lab,60to90min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60–90 分钟
              </span>
            </span>
            <span class="pf-v6-c-label pf-m-gold pf-m-compact" style="margin-left:8px;">
              <span class="pf-v6-c-label__content">Proposed</span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Automation Platform and Data Sovereignty</h3>
          </div>
          <div class="pf-v6-c-card__body">
            使用 Ansible Automation Platform 实现数据主权与合规。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">工作坊</span></span>
          </div>
        </div>
      </div>

        </div>
      </section>

<!-- ========== VIRT ========== -->
      <section class="cards-section">
        <h2 class="cards-section__heading">虚拟化</h2>
        <div class="pf-v6-l-gallery pf-m-gutter cards-gallery">

      <a target="_blank" href="./exercises/day-2-ops" class="card-link" data-tags="virt,workshop,60to90min,nontmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                90 分钟
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Day 2 Ops</h3>
          </div>
          <div class="pf-v6-c-card__body">
            使用 OpenShift Virtualization 实现自动化。学习可与 OpenShift Virtualization 和 AAP 一起完成的运维任务。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">Non TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">工作坊</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/mig-factory" target="_blank" class="card-link" data-tags="virt,lab,under60min,nontmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">OpenShift Virtualization Migration Factory Demo</h3>
          </div>
          <div class="pf-v6-c-card__body">
            OpenShift Virtualization Migration Factory 演示环境。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">Non TMM</span></span>
          </div>
        </div>
      </a>

        </div>
      </section>

<!-- ========== CLOUD ========== -->
      <section class="cards-section">
        <h2 class="cards-section__heading">云</h2>
        <div class="pf-v6-l-gallery pf-m-gutter cards-gallery">

      <a target="_blank" href="https://catalog.demo.redhat.com/catalog?search=ansible&item=babylon-catalog-prod%2Fazure-gpte.open-environment-azure-aap2.prod" class="card-link" data-tags="cloud,workshop,lab,under60min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Automation Platform on Azure - Open Env</h3>
          </div>
          <div class="pf-v6-c-card__body">
            在 Microsoft Azure 上的 Ansible Automation Platform 开放实验环境。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">工作坊</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="https://catalog.demo.redhat.com/catalog?search=ansible&item=babylon-catalog-prod%2Fsandboxes-gpte.open-environment-aws-aap2.prod" class="card-link" data-tags="cloud,workshop,lab,under60min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Automation Platform on AWS - Open Env</h3>
          </div>
          <div class="pf-v6-c-card__body">
            在 Amazon Web Services 上的 Ansible Automation Platform 开放实验环境。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">工作坊</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/hashicorp-aap" target="_blank" class="card-link" data-tags="cloud,workshop,lab,under60min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">AAP and HashiCorp: Terraform, Vault and AAP</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Ansible Automation Platform 与 HashiCorp（Terraform、Vault）集成。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">工作坊</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="https://catalog.demo.redhat.com/catalog?search=ansible&item=babylon-catalog-prod%2Fgcp-gpte.open-environment-gcp-aap2.prod" class="card-link" data-tags="cloud,lab,under60min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Automation Platform on GCP - Open Env</h3>
          </div>
          <div class="pf-v6-c-card__body">
            在 Google Cloud Platform 上的 Ansible Automation Platform 开放实验环境。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/cloud-azure-visibility" target="_blank" class="card-link" data-tags="cloud,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Hybrid cloud automation: Infrastructure visibility on Microsoft Azure</h3>
          </div>
          <div class="pf-v6-c-card__body">
            使用 Ansible 在 Microsoft Azure 上进行基础设施可见性与管理。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>

            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884777','_blank')"><span class="pf-v6-c-label__content">公开实验</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/cloud-operations-aws" target="_blank" class="card-link" data-tags="cloud,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Hybrid cloud automation: Cloud operations on AWS (IaC)</h3>
          </div>
          <div class="pf-v6-c-card__body">
            使用 Ansible 在 AWS 上进行云运维与基础设施即代码（IaC）。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>

            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884774','_blank')"><span class="pf-v6-c-label__content">公开实验</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/cloud-optimization-aws" target="_blank" class="card-link" data-tags="cloud,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Hybrid cloud automation: Infrastructure optimization on AWS</h3>
          </div>
          <div class="pf-v6-c-card__body">
            使用 Ansible 在 AWS 上进行基础设施优化与成本管理。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>

            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884775','_blank')"><span class="pf-v6-c-label__content">公开实验</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/cloud-visibility-advanced" target="_blank" class="card-link" data-tags="cloud,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Hybrid cloud automation: Infrastructure visibility on Microsoft Azure (Advanced)</h3>
          </div>
          <div class="pf-v6-c-card__body">
            使用 Ansible 提升 Microsoft Azure 上的高级基础设施可见性。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>

            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884773','_blank')"><span class="pf-v6-c-label__content">公开实验</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/cloud-azure-optimization" target="_blank" class="card-link" data-tags="cloud,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Hybrid cloud automation: Infrastructure optimization (Advanced)</h3>
          </div>
          <div class="pf-v6-c-card__body">
            使用 Ansible 在混合云中进行高级基础设施优化。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>

            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884829','_blank')"><span class="pf-v6-c-label__content">公开实验</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/cloud-azure-operations" target="_blank" class="card-link" data-tags="cloud,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Hybrid cloud automation: Cloud operations on Microsoft Azure</h3>
          </div>
          <div class="pf-v6-c-card__body">
            使用 Ansible Automation Platform 在 Microsoft Azure 上进行云运维。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>

            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884828','_blank')"><span class="pf-v6-c-label__content">公开实验</span></span>
          </div>
        </div>
      </a>

        </div>
      </section>

      <!-- ========== GENERAL ========== -->
      <section class="cards-section">
        <h2 class="cards-section__heading">通用</h2>
        <div class="pf-v6-l-gallery pf-m-gutter cards-gallery">

      <a target="_blank" href="./exercises/servicenow" class="card-link" data-tags="general,workshop,60to90min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                90 分钟
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Get started with ServiceNow</h3>
          </div>
          <div class="pf-v6-c-card__body">
            ServiceNow 自动化入门。聚焦将 Ansible 自动化与 IT 服务管理（ITSM）工具结合使用。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">工作坊</span></span>

            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884768','_blank')"><span class="pf-v6-c-label__content">公开实验</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="./exercises/eda" class="card-link" data-tags="general,workshop,60to90min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                90 分钟
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Event-Driven Ansible</h3>
          </div>
          <div class="pf-v6-c-card__body">
            EDA 技术工作坊。涵盖事件源、规则与操作等 EDA 基础。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">工作坊</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="https://catalog.demo.redhat.com/catalog?item=babylon-catalog-prod/pert.awx-to-aap-25.prod&utm_source=webapp&utm_medium=share-link" class="card-link" data-tags="general,lab,under60min,nontmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Migrate from AWX/Tower to AAP (CNV)</h3>
          </div>
          <div class="pf-v6-c-card__body">
            在 CNV 上将 AWX/Tower 迁移到 Ansible Automation Platform 的指南。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">Non TMM</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="https://catalog.demo.redhat.com/catalog?item=babylon-catalog-prod/pert.containerized-aap-25.prod&utm_source=webapp&utm_medium=share-link" class="card-link" data-tags="general,lab,60to90min,nontmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60–90 分钟
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Product Enablement Containerized AAP 2.5</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Ansible Automation Platform 2.5 容器化部署的产品赋能内容。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">Non TMM</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="./exercises/product_demos/" class="card-link" data-tags="general,lab,under60min,nontmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Product Demos (AAP 2.5, 2.6, 2.7)</h3>
          </div>
          <div class="pf-v6-c-card__body">
            用于演示、开发与实验 Ansible Automation Platform 的沙盒环境。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">Non TMM</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="https://catalog.demo.redhat.com/catalog?search=rhel+automation&item=babylon-catalog-prod%2Fsandboxes-gpte.ans-bu-wksp-auto-satellite.prod" class="card-link" data-tags="general,lab,60to90min,nontmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60–90 分钟
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Automated Satellite Workshop</h3>
          </div>
          <div class="pf-v6-c-card__body">
            使用 Ansible 管理 Red Hat Satellite 的自动化工作坊。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">Non TMM</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/ansible-navigator" target="_blank" class="card-link" data-tags="general,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Get Started ansible-navigator</h3>
          </div>
          <div class="pf-v6-c-card__body">
            入门 ansible-navigator，运行并开发 Ansible 内容。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>

            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884762','_blank')"><span class="pf-v6-c-label__content">公开实验</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/automation-controller" target="_blank" class="card-link" data-tags="general,lab,2plushours,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-green">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                2 小时以上
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Get Started with Automation Controller</h3>
          </div>
          <div class="pf-v6-c-card__body">
            入门 Automation Controller Web UI 与核心概念。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>

            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884764','_blank')"><span class="pf-v6-c-label__content">公开实验</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/adv-controller" target="_blank" class="card-link" data-tags="general,lab,2plushours,nontmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-green">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                2 小时以上
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Advanced Features of Ansible Automation Controller</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Ansible Automation Controller 的高级功能与能力。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">Non TMM</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="./exercises/aapcasc-4" class="card-link" data-tags="general,lab,2plushours,nontmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Automation Controller Configuration as Code</h3>
          </div>
          <div class="pf-v6-c-card__body">
            使用 controller configuration collection，为 Automation Controller 实现配置即代码（CaC）。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">Non TMM</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/aap-selfservice" target="_blank" class="card-link" data-tags="general,lab,under60min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60 分钟以内
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Introduction to AAP self-service automation</h3>
          </div>
          <div class="pf-v6-c-card__body">
            使用 Ansible Automation Platform 入门自助自动化。
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          </div>
        </div>
      </a>

        </div>
      </section>

<!-- ========== EVENTS ========== -->
      <section class="cards-section">
        <h2 class="cards-section__heading">活动</h2>
        <div class="pf-v6-l-gallery pf-m-gutter cards-gallery">

      <a target="_blank" href="./exercises/ansible-automates" class="card-link" data-tags="events">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-orange">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-users pf-v6-c-label__icon"></i>
                活动
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Automates</h3>
          </div>
          <div class="pf-v6-c-card__body">
            全天单轨会议，向全球各地区受众呈现精选 AnsibleFest 内容。
          </div>
        </div>
      </a>

      <a target="_blank" href="./exercises/ansible-automates-events" class="card-link" data-tags="events">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-orange">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-users pf-v6-c-label__icon"></i>
                活动
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Automates Events</h3>
          </div>
          <div class="pf-v6-c-card__body">
            线下与线上 Ansible Automates 活动资料包，含议题内容库与营销素材。
          </div>
        </div>
      </a>

      <a target="_blank" href="./exercises/automation-connection" class="card-link" data-tags="events">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-orange">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-users pf-v6-c-label__icon"></i>
                活动
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Automation Connection</h3>
          </div>
          <div class="pf-v6-c-card__body">
            面向特定客户的 3 小时 IT 自动化活动，用于客户业务拓展与社区建设。
          </div>
        </div>
      </a>

      <a target="_blank" href="./exercises/automation-everywhere" class="card-link" data-tags="events">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-orange">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-users pf-v6-c-label__icon"></i>
                活动
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Automation Everywhere</h3>
          </div>
          <div class="pf-v6-c-card__body">
            面向决策者的 3 小时非技术活动，适用于已识别 Ansible Automation Platform 商机的场景。
          </div>
        </div>
      </a>

      <a target="_blank" href="./exercises/automation-roundtable" class="card-link" data-tags="events">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-orange">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-users pf-v6-c-label__icon"></i>
                活动
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Automation Roundtable</h3>
          </div>
          <div class="pf-v6-c-card__body">
            面向关键 IT 决策者的高管同业圆桌交流。
          </div>
        </div>
      </a>
        </div>
      </section>

<!-- ========== RESOURCES ========== -->
      <section class="cards-section">
        <h2 class="cards-section__heading">资源</h2>
        <div class="pf-v6-l-gallery pf-m-gutter cards-gallery">

      <a target="_blank" href="./exercises/one-stop-shop" class="card-link" data-tags="resources">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-gold">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-book pf-v6-c-label__icon"></i>
                资源
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">ONE-STOP SHOP</h3>
          </div>
          <div class="pf-v6-c-card__body">
            IT 自动化工作坊与活动资源中心——选择最适合你场景的活动或工作坊。
          </div>
        </div>
      </a>

      <a target="_blank" href="./exercises/ansible-workshops" class="card-link" data-tags="resources">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-gold">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-book pf-v6-c-label__icon"></i>
                资源
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Workshops</h3>
          </div>
          <div class="pf-v6-c-card__body">
            全部 Ansible 技术工作坊与活动资料包目录，含时长与目标受众说明。
          </div>
        </div>
      </a>
        </div>
      </section>

    </div>

    <div class="cards-contributing">
      <h2>更多资源</h2>
    </div>

    <div class="cards-resources">
      <h2>自主练习</h2>
      <p><a href="https://red.ht/ansible-labs">Ansible Automation Platform 自主实验</a> — 交互式学习场景，提供预配置环境，便于动手实验、学习并了解平台如何帮助解决实际问题（每个约 15–30 分钟）。</p>
    </div>

    <div class="cards-resources">
      <h2>YouTube 频道</h2>
      <ul>
        <li><a href="https://youtube.com/ansibleautomation">The Ansible Playbook</a> — 与技术营销工程师一起在线学习</li>
        <li><a href="https://www.youtube.com/@RedHatAnsible">Red Hat Ansible</a> — AnsibleFest 议题、产品发布等更多内容</li>
      </ul>
    </div>

    <div class="cards-resources">
      <h2>文档与培训</h2>
      <ul>
        <li><a href="https://docs.ansible.com/ansible/latest/getting_started/index.html">Ansible 入门指南</a></li>
        <li><a href="https://docs.ansible.com/ansible/latest/network/getting_started/index.html">Ansible 网络自动化入门</a></li>
        <li><a href="https://red.ht/aap_training">Red Hat AAP 培训与认证</a></li>
        <li><a href="http://red.ht/try_ansible">获取 AAP 试用订阅</a></li>
        <li><a href="https://forum.ansible.com/">Ansible 社区论坛</a></li>
      </ul>
    </div>

    <div class="cards-resources">
      <h2>工作坊文档</h2>
      <ul>
        <li><a href="docs/attendance/attendance.md">工作坊报名网站</a></li>
        <li><a href="docs/contribute.md">如何贡献</a></li>
        <li><a href="provisioner/README.md">如何使用 AWS 实验环境配置工具</a></li>
        <li><a href="docs/faq.md">常见问题</a></li>
        <li><a href="docs/release.md">发布流程</a></li>
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

  function getFiltersByGroup() {
    var groups = {};
    document.querySelectorAll('.cards-sidebar__section[data-filter-group]').forEach(function (section) {
      var groupName = section.getAttribute('data-filter-group');
      var checked = [];
      section.querySelectorAll('input[type="checkbox"]:checked').forEach(function (cb) {
        checked.push(cb.value);
      });
      if (checked.length) groups[groupName] = checked;
    });
    return groups;
  }

  function filterCards() {
    var query = headerInput.value.toLowerCase().trim();
    var groups = getFiltersByGroup();
    var groupKeys = Object.keys(groups);
    filterClearBtn.style.display = (groupKeys.length || query) ? 'inline' : 'none';

    var visible = 0;

    allCards.forEach(function (card) {
      var textMatch = !query || getCardText(card).indexOf(query) !== -1;
      var filterMatch = true;

      if (groupKeys.length) {
        var cardTags = (card.getAttribute('data-tags') || '').split(',').map(function (s) { return s.trim(); });
        for (var i = 0; i < groupKeys.length; i++) {
          var groupFilters = groups[groupKeys[i]];
          var groupMatch = groupFilters.some(function (f) { return cardTags.indexOf(f) !== -1; });
          if (!groupMatch) { filterMatch = false; break; }
        }
      }

      var show = textMatch && filterMatch;
      card.style.display = show ? '' : 'none';
      if (show) visible++;
    });

    document.querySelectorAll('.cards-section').forEach(function (section) {
      var sectionCards = section.querySelectorAll('.card-link');
      var sectionVisible = false;
      sectionCards.forEach(function (card) {
        if (card.style.display !== 'none') sectionVisible = true;
      });
      section.style.display = sectionVisible ? '' : 'none';
    });

    if (query || groupKeys.length) {
      countEl.textContent = visible === 0
        ? '没有符合筛选条件的工作坊。'
        : visible + ' 个工作坊。';
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
