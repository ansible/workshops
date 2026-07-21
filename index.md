---
layout: default
title: Ansible Workshops
patternfly: true
---

**Read this in other languages**:
<br>![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English]({{ '/' | relative_url }}),  ![japan](https://github.com/ansible/workshops/raw/devel/images/japan.png)[日本語]({{ '/README.ja' | relative_url }})

<div class="cards-layout">
  <aside class="cards-sidebar">
    <div class="cards-sidebar__header">
      <span>Filter by</span>
      <button id="filter-clear" class="cards-sidebar__clear">Clear filters</button>
    </div>
    <div class="cards-sidebar__section" data-filter-group="domain">
      <h4 class="cards-sidebar__title">Domain</h4>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="gettingstarted"> Getting Started
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="linux"> Linux
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="network"> Network
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="general"> General
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="ai"> AI
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="developer"> Developer
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="cloud"> Cloud
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="windows"> Windows
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="virt"> Virt
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="security"> Security
      </label>
    </div>
    <div class="cards-sidebar__section" data-filter-group="type">
      <h4 class="cards-sidebar__title">Type</h4>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="lab"> Lab
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="workshop"> Workshop
      </label>
    </div>
    <div class="cards-sidebar__section" data-filter-group="time">
      <h4 class="cards-sidebar__title">Time</h4>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="2plushours"> 2+ Hours
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="60to90min"> 60-90 Min
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="under60min"> Under 60 Min
      </label>
    </div>
    <div class="cards-sidebar__section" data-filter-group="tmm">
      <h4 class="cards-sidebar__title">TMM</h4>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="tmm"> TMM
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="nontmm"> Non TMM
      </label>
    </div>
    <div class="cards-sidebar__section" data-filter-group="availability">
      <h4 class="cards-sidebar__title">Availability</h4>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="public"> Public
      </label>
    </div>
  </aside>

  <div class="cards-main">
    <p id="guide-search-count" class="cards-search__count"></p>

    <div class="cards-sections">

      <!-- ========== GETTING_STARTED ========== -->
      <section class="cards-section">
        <h2 class="cards-section__heading">Getting Started</h2>
        <div class="pf-v6-l-gallery pf-m-gutter cards-gallery">

      <a href="./exercises/instruqt/day-in-the-life" class="card-link" data-tags="gettingstarted,workshop,2plushours,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-green">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                2+ Hours
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Day in the Life of an Automater</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Experience a typical day as an automation engineer using Ansible Automation Platform.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">Workshop</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/roadshow01" class="card-link" data-tags="gettingstarted,lab,under60min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">AAP Roadshow #1 - Introspection</h3>
          </div>
          <div class="pf-v6-c-card__body">
            AAP Roadshow module focused on introspection and understanding your automation environment.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/roadshow02" class="card-link" data-tags="gettingstarted,lab,under60min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">AAP Roadshow #2 - Standardization</h3>
          </div>
          <div class="pf-v6-c-card__body">
            AAP Roadshow module focused on standardization and governance of automation.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/roadshow03" class="card-link" data-tags="gettingstarted,lab,under60min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">AAP Roadshow #3 - Operational Efficiency</h3>
          </div>
          <div class="pf-v6-c-card__body">
            AAP Roadshow module focused on operational efficiency and scaling automation.
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
        <h2 class="cards-section__heading">Developer</h2>
        <div class="pf-v6-l-gallery pf-m-gutter cards-gallery">

      <a href="./exercises/instruqt/dev-tools" class="card-link" data-tags="developer,workshop,lab,60to90min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                2-Hour
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Development Tools Workshop</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Create, test, and package Ansible collections using the DevTools suite in a pre-provisioned VS Code environment.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP Zero</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">Workshop</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/dev-tools-extended" class="card-link" data-tags="developer,workshop,lab,2plushours,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-green">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                3-Hour
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Development Tools Workshop (Extended)</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Full DevTools lifecycle using Ansible Workspaces on OpenShift Dev Spaces — create, test, and deploy automation content with the complete ansible-dev-tools suite and VS Code.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">Workshop</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="https://catalog.demo.redhat.com/catalog?search=ansible&item=babylon-catalog-prod%2Fsandboxes-gpte.rhdh-ansible-demo.prod" class="card-link" data-tags="developer,lab,under60min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Plug-ins for Red Hat Developer Hub Demo</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Ansible plug-ins for Red Hat Developer Hub demo environment.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/ansible-builder" class="card-link" data-tags="developer,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Get started with ansible-builder</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Get started with ansible-builder for creating custom execution environments.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884763','_blank')"><span class="pf-v6-c-label__content">Public Lab</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/lightspeed-101" class="card-link" data-tags="developer,lab,60to90min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60-90 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Intro into Ansible Lightspeed with IBM watsonx Code Assistant</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Introduction to Ansible Lightspeed with IBM watsonx Code Assistant for AI-powered content creation.
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

      <a target="_blank" href="./exercises/instruqt/ai-ansible" class="card-link" data-tags="ai,workshop,2plushours,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-green">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                2+ Hours
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Introduction to AI-Driven Ansible Automation: Self-healing</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Introduction to AI-Driven Ansible Automation &amp; AIOps. Build an intelligent, self-healing automation workflow.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">Workshop</span></span>
          </div>
        </div>
      </a>

        </div>
      </section>

<!-- ========== LINUX ========== -->
      <section class="cards-section">
        <h2 class="cards-section__heading">Linux</h2>
        <div class="pf-v6-l-gallery pf-m-gutter cards-gallery">

      <a target="_blank" href="./exercises/instruqt/rhel" class="card-link" data-tags="linux,workshop,2plushours,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-green">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                6-Hour
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible for Red Hat Enterprise Linux</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Full-day RHEL automation workshop. Focused on automating Linux platforms like Red Hat Enterprise Linux.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">Workshop</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="./exercises/instruqt/rhel-90" class="card-link" data-tags="linux,workshop,60to90min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                90-Minute
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible for Red Hat Enterprise Linux (90 min)</h3>
          </div>
          <div class="pf-v6-c-card__body">
            90-minute RHEL automation workshop. Focused on automating Linux platforms like Red Hat Enterprise Linux.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">Workshop</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/ripu" class="card-link" data-tags="linux,lab,2plushours,nontmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-green">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                2+ Hours
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">RHEL In-place Upgrade Automation Workshop</h3>
          </div>
          <div class="pf-v6-c-card__body">
            RHEL In-place Upgrade Automation Workshop. Focused on automation of RHEL in-place upgrades at enterprise scale.
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

      <a target="_blank" href="./exercises/instruqt/windows" class="card-link" data-tags="windows,workshop,60to90min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                90-Minute
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Intro to Windows Automation (90 min)</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Getting Started with Windows Automation. Focused on using Ansible Automation for automating tasks on a Windows host.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">Workshop</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/windows-ad" class="card-link" data-tags="windows,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Intro to Windows Automation - Active Directory</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Windows Automation focused on Active Directory management with Ansible.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884845','_blank')"><span class="pf-v6-c-label__content">Public Lab</span></span>
          </div>
        </div>
      </a>

        </div>
      </section>

<!-- ========== NETWORK ========== -->
      <section class="cards-section">
        <h2 class="cards-section__heading">Network</h2>
        <div class="pf-v6-l-gallery pf-m-gutter cards-gallery">

      <a target="_blank" href="./exercises/instruqt/network-6" class="card-link" data-tags="network,workshop,2plushours,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-green">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                6-Hour
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Network Automation Workshop</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Full-day network automation workshop. Covers network basics and Ansible Automation Platform for network devices.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">Workshop</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="./exercises/instruqt/network" class="card-link" data-tags="network,workshop,60to90min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                90-Minute
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Introduction to Ansible Network Automation Workshop</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Getting Started with Network Automation. Focused on Ansible Automation with respect to routers and switches.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">Workshop</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/eda-netbox" class="card-link" data-tags="network,lab,60to90min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60-90 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Event-Driven Ansible and Netbox as a source of truth</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Event-Driven Ansible with Netbox integration for network automation source of truth.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/network-first-playbook" class="card-link" data-tags="network,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Network Automation: First Playbook</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Write your first network automation playbook with Ansible.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884830','_blank')"><span class="pf-v6-c-label__content">Public Lab</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/network-backup-restore" class="card-link" data-tags="network,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Network Automation: Backup and Restore</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Network configuration backup and restore automation with Ansible.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884831','_blank')"><span class="pf-v6-c-label__content">Public Lab</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/network-resource-modules" class="card-link" data-tags="network,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Network Automation: Resource Modules</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Working with Ansible network resource modules for declarative network management.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884832','_blank')"><span class="pf-v6-c-label__content">Public Lab</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/network-surveys" class="card-link" data-tags="network,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Network Automation: Surveys</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Using Automation Controller surveys for self-service network automation.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884835','_blank')"><span class="pf-v6-c-label__content">Public Lab</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/network-facts" class="card-link" data-tags="network,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Network Automation: Facts</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Gathering and using network device facts with Ansible.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884833','_blank')"><span class="pf-v6-c-label__content">Public Lab</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/network-visibility" class="card-link" data-tags="network,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Network Automation: Infrastructure Visibility</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Network infrastructure visibility and reporting with Ansible.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884834','_blank')"><span class="pf-v6-c-label__content">Public Lab</span></span>
          </div>
        </div>
      </a>

        </div>
      </section>

<!-- ========== SECURITY ========== -->
      <section class="cards-section">
        <h2 class="cards-section__heading">Security</h2>
        <div class="pf-v6-l-gallery pf-m-gutter cards-gallery">

      <a href="./exercises/instruqt/zero-trust" class="card-link" data-tags="security,workshop,lab,2plushours,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-green">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                2+ Hours
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Implementing Zero Trust with Ansible Automation Platform</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Implementing Zero Trust security architecture with Ansible Automation Platform.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">Workshop</span></span>
          </div>
        </div>
      </a>

      <div class="card-link" data-tags="security,workshop,lab,60to90min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60-90 Min
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
            Foundational security compliance and hardening with Ansible Automation Platform.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">Workshop</span></span>
          </div>
        </div>
      </div>

      <div class="card-link" data-tags="security,workshop,lab,60to90min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60-90 Min
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
            Responsive security with Ansible Automation Platform &mdash; hack and heal exercises.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">Workshop</span></span>
          </div>
        </div>
      </div>

      <div class="card-link" data-tags="security,workshop,lab,60to90min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                60-90 Min
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
            Data sovereignty and compliance with Ansible Automation Platform.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">Workshop</span></span>
          </div>
        </div>
      </div>

        </div>
      </section>

<!-- ========== VIRT ========== -->
      <section class="cards-section">
        <h2 class="cards-section__heading">Virt</h2>
        <div class="pf-v6-l-gallery pf-m-gutter cards-gallery">

      <a target="_blank" href="./exercises/instruqt/day-2-ops" class="card-link" data-tags="virt,workshop,60to90min,nontmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                90-Minute
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Day 2 Ops</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Automation with OpenShift Virtualization. Activities we can perform with OpenShift Virtualization and AAP.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">Non TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">Workshop</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/mig-factory" class="card-link" data-tags="virt,lab,under60min,nontmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">OpenShift Virtualization Migration Factory Demo</h3>
          </div>
          <div class="pf-v6-c-card__body">
            OpenShift Virtualization Migration Factory demonstration environment.
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
        <h2 class="cards-section__heading">Cloud</h2>
        <div class="pf-v6-l-gallery pf-m-gutter cards-gallery">

      <a target="_blank" href="https://catalog.demo.redhat.com/catalog?search=ansible&item=babylon-catalog-prod%2Fazure-gpte.open-environment-azure-aap2.prod" class="card-link" data-tags="cloud,workshop,lab,under60min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Automation Platform on Azure - Open Env</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Ansible Automation Platform on Microsoft Azure open environment.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">Workshop</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="https://catalog.demo.redhat.com/catalog?search=ansible&item=babylon-catalog-prod%2Fsandboxes-gpte.open-environment-aws-aap2.prod" class="card-link" data-tags="cloud,workshop,lab,under60min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Automation Platform on AWS - Open Env</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Ansible Automation Platform on Amazon Web Services open environment.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">Workshop</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/hashicorp-aap" class="card-link" data-tags="cloud,workshop,lab,under60min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">AAP and HashiCorp: Terraform, Vault and AAP</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Ansible Automation Platform and HashiCorp integration with Terraform and Vault.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">Workshop</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="https://catalog.demo.redhat.com/catalog?search=ansible&item=babylon-catalog-prod%2Fgcp-gpte.open-environment-gcp-aap2.prod" class="card-link" data-tags="cloud,lab,under60min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Automation Platform on GCP - Open Env</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Ansible Automation Platform on Google Cloud Platform open environment.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/cloud-azure-visibility" class="card-link" data-tags="cloud,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Hybrid cloud automation: Infrastructure visibility on Microsoft Azure</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Infrastructure visibility and management on Microsoft Azure with Ansible.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884777','_blank')"><span class="pf-v6-c-label__content">Public Lab</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/cloud-operations-aws" class="card-link" data-tags="cloud,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Hybrid cloud automation: Cloud operations on AWS (IaC)</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Cloud operations and Infrastructure as Code on AWS with Ansible.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884774','_blank')"><span class="pf-v6-c-label__content">Public Lab</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/cloud-optimization-aws" class="card-link" data-tags="cloud,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Hybrid cloud automation: Infrastructure optimization on AWS</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Infrastructure optimization and cost management on AWS with Ansible.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884775','_blank')"><span class="pf-v6-c-label__content">Public Lab</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/cloud-visibility-advanced" class="card-link" data-tags="cloud,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Hybrid cloud automation: Infrastructure visibility on Microsoft Azure (Advanced)</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Advanced infrastructure visibility on Microsoft Azure with Ansible.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884773','_blank')"><span class="pf-v6-c-label__content">Public Lab</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/cloud-azure-optimization" class="card-link" data-tags="cloud,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Hybrid cloud automation: Infrastructure optimization (Advanced)</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Advanced infrastructure optimization across hybrid cloud with Ansible.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884829','_blank')"><span class="pf-v6-c-label__content">Public Lab</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/cloud-azure-operations" class="card-link" data-tags="cloud,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Hybrid cloud automation: Cloud operations on Microsoft Azure</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Cloud operations on Microsoft Azure with Ansible Automation Platform.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884828','_blank')"><span class="pf-v6-c-label__content">Public Lab</span></span>
          </div>
        </div>
      </a>

        </div>
      </section>

      <!-- ========== GENERAL ========== -->
      <section class="cards-section">
        <h2 class="cards-section__heading">General</h2>
        <div class="pf-v6-l-gallery pf-m-gutter cards-gallery">

      <a target="_blank" href="./exercises/instruqt/servicenow" class="card-link" data-tags="general,workshop,60to90min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                90-Minute
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Get started with ServiceNow</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Getting Started with ServiceNow Automation. Focused on using Ansible Automation in conjunction with an IT Service Management (ITSM) tool.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">Workshop</span></span>
          
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884768','_blank')"><span class="pf-v6-c-label__content">Public Lab</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="./exercises/instruqt/eda" class="card-link" data-tags="general,workshop,60to90min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-purple">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                90-Minute
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Event-Driven Ansible</h3>
          </div>
          <div class="pf-v6-c-card__body">
            EDA Technical Workshop. Covers EDA fundamentals such as sources, rules, and actions.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">Workshop</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="https://catalog.demo.redhat.com/catalog?item=babylon-catalog-prod/pert.awx-to-aap-25.prod&utm_source=webapp&utm_medium=share-link" class="card-link" data-tags="general,lab,under60min,nontmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Migrate from AWX/Tower to AAP (CNV)</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Migration guide from AWX/Tower to Ansible Automation Platform on CNV.
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
                60-90 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Product Enablement Containerized AAP 2.5</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Product enablement for containerized deployment of Ansible Automation Platform 2.5.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">Non TMM</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="https://catalog.demo.redhat.com/catalog?search=rhel+automation&item=babylon-catalog-prod%2Fenterprise.aap-product-demos-cnv-aap25.prod" class="card-link" data-tags="general,lab,under60min,nontmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Product Demos (AAP 2.5, 2.6, 2.7)</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Sandbox for demoing, development, and experimentation with Ansible Automation Platform.
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
                60-90 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Automated Satellite Workshop</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Automated Satellite Workshop for Red Hat Satellite management with Ansible.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">Non TMM</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/ansible-navigator" class="card-link" data-tags="general,lab,under60min,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Get Started ansible-navigator</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Get started with ansible-navigator for running and developing Ansible content.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884762','_blank')"><span class="pf-v6-c-label__content">Public Lab</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/automation-controller" class="card-link" data-tags="general,lab,2plushours,tmm,public">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-green">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                2+ Hours
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Get Started with Automation Controller</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Get started with the Automation Controller web UI and key concepts.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">TMM</span></span>
          
            <span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-green" style="cursor:pointer" onclick="event.preventDefault();event.stopPropagation();window.open('https://developers.redhat.com/content-gateway/link/3884764','_blank')"><span class="pf-v6-c-label__content">Public Lab</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/adv-controller" class="card-link" data-tags="general,lab,2plushours,nontmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-green">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                2+ Hours
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Advanced Features of Ansible Automation Controller</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Advanced features and capabilities of the Ansible Automation Controller.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">Non TMM</span></span>
          </div>
        </div>
      </a>

      <a target="_blank" href="https://catalog.demo.redhat.com/catalog?search=ansible&item=babylon-catalog-prod%2Fansiblebu.aap2-workshop-casc.prod" class="card-link" data-tags="general,lab,under60min,nontmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Automation Controller Configuration as Code</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Configuration as Code for Automation Controller using the controller configuration collection.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">Non TMM</span></span>
          </div>
        </div>
      </a>

      <a href="./exercises/instruqt/aap-selfservice" class="card-link" data-tags="general,lab,under60min,tmm">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-cyan">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                Under 60 Min
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Introduction to AAP self-service automation</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Introduction to self-service automation with Ansible Automation Platform.
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
        <h2 class="cards-section__heading">Events</h2>
        <div class="pf-v6-l-gallery pf-m-gutter cards-gallery">

      <a target="_blank" href="./exercises/instruqt/ansible-automates" class="card-link" data-tags="events">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-orange">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-users pf-v6-c-label__icon"></i>
                Events
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Automates</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Full-day, one-track conference presenting the best AnsibleFest content to regional audiences around the world.
          </div>
        </div>
      </a>

      <a target="_blank" href="./exercises/instruqt/ansible-automates-events" class="card-link" data-tags="events">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-orange">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-users pf-v6-c-label__icon"></i>
                Events
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Automates Events</h3>
          </div>
          <div class="pf-v6-c-card__body">
            In-person and virtual Ansible Automates event kits with session content repository and marketing assets.
          </div>
        </div>
      </a>

      <a target="_blank" href="./exercises/instruqt/automation-connection" class="card-link" data-tags="events">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-orange">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-users pf-v6-c-label__icon"></i>
                Events
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Automation Connection</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Account-specific 3-hour IT automation event for account expansion and community building within an account.
          </div>
        </div>
      </a>

      <a target="_blank" href="./exercises/instruqt/automation-everywhere" class="card-link" data-tags="events">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-orange">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-users pf-v6-c-label__icon"></i>
                Events
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Automation Everywhere</h3>
          </div>
          <div class="pf-v6-c-card__body">
            3-hour non-technical event for decision makers when an Ansible Automation Platform opportunity has been identified.
          </div>
        </div>
      </a>

      <a target="_blank" href="./exercises/instruqt/automation-roundtable" class="card-link" data-tags="events">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-orange">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-users pf-v6-c-label__icon"></i>
                Events
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Automation Roundtable</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Executive roundtable for peer-to-peer discussions with key IT decision-makers.
          </div>
        </div>
      </a>
        </div>
      </section>

<!-- ========== RESOURCES ========== -->
      <section class="cards-section">
        <h2 class="cards-section__heading">Resources</h2>
        <div class="pf-v6-l-gallery pf-m-gutter cards-gallery">

      <a target="_blank" href="./exercises/instruqt/one-stop-shop" class="card-link" data-tags="resources">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-gold">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-book pf-v6-c-label__icon"></i>
                Resources
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">ONE-STOP SHOP</h3>
          </div>
          <div class="pf-v6-c-card__body">
            IT Automation Workshops and Events hub — select the event or workshop that best fits your scenario.
          </div>
        </div>
      </a>

      <a target="_blank" href="./exercises/instruqt/ansible-workshops" class="card-link" data-tags="resources">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-gold">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-book pf-v6-c-label__icon"></i>
                Resources
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Workshops</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Catalog of all Ansible technical workshops and event kits with duration and target audience guidance.
          </div>
        </div>
      </a>
        </div>
      </section>

    </div>

    <div class="cards-contributing">
      <h2>Additional Resources</h2>
    </div>

    <div class="cards-resources">
      <h2>Self Paced Exercises</h2>
      <p><a href="https://red.ht/ansible-labs">Ansible Automation Platform Self-Paced Labs</a> — Interactive learning scenarios with a pre-configured environment to experiment, learn, and see how the platform can help you solve real-world problems (15-30 minutes each).</p>
    </div>

    <div class="cards-resources">
      <h2>YouTube Channels</h2>
      <ul>
        <li><a href="https://youtube.com/ansibleautomation">The Ansible Playbook</a> — Join the Tech Marketing Engineers online</li>
        <li><a href="https://www.youtube.com/@RedHatAnsible">Red Hat Ansible</a> — Ansiblefest sessions, product announcements and more</li>
      </ul>
    </div>

    <div class="cards-resources">
      <h2>Documentation & Training</h2>
      <ul>
        <li><a href="https://docs.ansible.com/ansible/latest/getting_started/index.html">Ansible Getting Started Guide</a></li>
        <li><a href="https://docs.ansible.com/ansible/latest/network/getting_started/index.html">Ansible Network Automation — Getting Started</a></li>
        <li><a href="https://red.ht/aap_training">Red Hat Training and Certification for AAP</a></li>
        <li><a href="http://red.ht/try_ansible">Get a Trial Subscription for AAP</a></li>
        <li><a href="https://forum.ansible.com/">Ansible Community Forum</a></li>
      </ul>
    </div>

    <div class="cards-resources">
      <h2>Workshop Documentation</h2>
      <ul>
        <li><a href="docs/attendance/attendance.md">Workshop attendance website</a></li>
        <li><a href="docs/contribute.md">How to contribute</a></li>
        <li><a href="provisioner/README.md">How to use the AWS Lab Provisioner</a></li>
        <li><a href="docs/faq.md">FAQ</a></li>
        <li><a href="docs/release.md">Release Process</a></li>
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
        ? 'No workshops match your filters.'
        : visible + ' workshop' + (visible !== 1 ? 's' : '') + ' found.';
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
