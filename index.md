---
layout: default
title: Ansible Workshops
patternfly: true
---

**Read this in other languages**:
<br>![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English](README.md),  ![japan](https://github.com/ansible/workshops/raw/devel/images/japan.png)[日本語](README.ja.md)

<div class="cards-layout">
  <aside class="cards-sidebar">
    <div class="cards-sidebar__header">
      <span>Filter by</span>
      <button id="filter-clear" class="cards-sidebar__clear">Clear filters</button>
    </div>
    <div class="cards-sidebar__section">
      <h4 class="cards-sidebar__title">Type</h4>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="90-minute"> 90-Minute
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="4-hour"> 4-Hour
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="6-hour"> 6-Hour
      </label>
      <label class="cards-sidebar__checkbox">
        <input type="checkbox" value="product-demos"> Product Demos
      </label>
    </div>
    <div class="cards-sidebar__section">
      <h4 class="cards-sidebar__title">Partner</h4>
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

      <!-- 90-Minute Workshops -->

      <a target="_blank" href="https://rhpds.github.io/ai-driven-automation-showroom/modules/index.html" class="card-link" data-tags="90-minute,splunk">
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
            <h3 class="pf-v6-c-card__title-text">AI + Ansible</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Introduction to AI-Driven Ansible Automation & AIOps. Build an intelligent, self-healing automation workflow.
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
                90-Minute
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Cloud Automation</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Introduction to cloud automation. Focused on how to orchestrate, operationalize and govern your hybrid cloud environments.
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
                90-Minute
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Lightspeed</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Ansible Lightspeed and Development Technical Workshop. Focused on the Ansible automation engineer or application developer.
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
                90-Minute
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Network Automation</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Getting Started with Network Automation. Focused on Ansible Automation with respect to routers and switches.
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
                90-Minute
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">RHEL Automation</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Ansible Red Hat Enterprise Linux Workshop. Focused on automating Linux platforms like Red Hat Enterprise Linux.
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
                90-Minute
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">ServiceNow Automation</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Getting Started with ServiceNow Automation. Focused on using Ansible Automation in conjunction with an IT Service Management (ITSM) tool.
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
                90-Minute
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Windows Automation</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Getting Started with Windows Automation. Focused on using Ansible Automation for automating tasks on a Windows host.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">Microsoft</span></span>
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP</span></span>
          </div>
        </div>
      </a>

      <!-- 4-Hour Workshops -->

      <a target="_blank" href="./exercises/instruqt/eda-4" class="card-link" data-tags="4-hour">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-blue">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-clock pf-v6-c-label__icon"></i>
                4-Hour
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Event-Driven Ansible (Extended)</h3>
          </div>
          <div class="pf-v6-c-card__body">
            EDA Technical Workshop. Covers EDA fundamentals such as sources, rules, and actions with deeper hands-on exercises.
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
                4-Hour
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Lightspeed (Extended)</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Ansible Lightspeed and Development Technical Workshop. Focused on the Ansible automation engineer or application developer.
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
                4-Hour
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Configuration as Code</h3>
          </div>
          <div class="pf-v6-c-card__body">
            CaC for Ansible Automation Platform. Focused on Configuration as Code for Ansible Automation Platform.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP</span></span>
          </div>
        </div>
      </a>

      <!-- 6-Hour Workshops -->

      <a target="_blank" href="./exercises/ansible_rhel" class="card-link" data-tags="6-hour">
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
            <h3 class="pf-v6-c-card__title-text">RHEL Automation (Full Day)</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Ansible Red Hat Enterprise Linux Workshop. Focused on automating Linux platforms like Red Hat Enterprise Linux.
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
                6-Hour
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Network Automation (Full Day)</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Ansible Network Automation Workshop. Focused on router and switch platforms like Arista, Cisco, Juniper.
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
                6-Hour
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Windows Automation (Full Day)</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Ansible Windows Automation Workshop. Focused on automation of Microsoft Windows.
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
                6-Hour
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible + Satellite</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Ansible + Satellite Workshop. Focused on automation of security and lifecycle management with Red Hat Satellite Server.
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
                6-Hour
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">RHEL In-place Upgrade</h3>
          </div>
          <div class="pf-v6-c-card__body">
            RHEL In-place Upgrade Automation Workshop. Focused on automation of RHEL in-place upgrades at enterprise scale.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP</span></span>
          </div>
        </div>
      </a>

      <!-- Product Demos -->

      <a target="_blank" href="./exercises/product_demos/" class="card-link" data-tags="product-demos">
        <div class="pf-v6-c-card">
          <div class="pf-v6-c-card__header">
            <span class="pf-v6-c-label pf-m-orange">
              <span class="pf-v6-c-label__content">
                <i class="fas fa-play-circle pf-v6-c-label__icon"></i>
                Product Demos
              </span>
            </span>
          </div>
          <div class="pf-v6-c-card__title">
            <h3 class="pf-v6-c-card__title-text">Ansible Product Demos</h3>
          </div>
          <div class="pf-v6-c-card__body">
            Sandbox for demoing, development, and experimentation with Ansible Automation Platform.
          </div>
          <div class="pf-v6-c-card__footer">
            <span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">RHDP</span></span>
          </div>
        </div>
      </a>

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
