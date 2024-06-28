# Workshop Exercise - Rinse and Repeat

## Table of Contents

- [Workshop Exercise - Rinse and Repeat](#workshop-exercise---rinse-and-repeat)
  - [Table of Contents](#table-of-contents)
  - [Objectives](#objectives)
  - [Guide](#guide)
    - [Step 1 - What You Learned](#step-1---what-you-learned)
    - [Step 2 - Activities for Extra Credit](#step-2---activities-for-extra-credit)
    - [Step 3 - Look at the Code](#step-3---look-at-the-code)
      - [redhat-cop/infra.leapp](#redhat-copinfraleapp)
      - [oamg/leapp-supplements](#oamgleapp-supplements)
      - [redhat-partner-tech/automated-satellite](#redhat-partner-techautomated-satellite)
      - [redhat-cop/infra.lvm_snapshots](#redhat-copinfralvm_snapshots)
  - [Thank You!](#thank-you)

## Objectives

* Review what we have learned in this workshop
* Consider ideas for further exploration
* Look at the code and get involved upstream

## Guide

Congratulations! You have reached the end of the RHEL In-place Upgrade Automation exercises. You are now armed with the knowledge needed to start developing an automation solution to help your organization manage RHEL upgrades at scale.

Let's review what we learned and think about what's next.

### Step 1 - What You Learned

With these exercises, you gained hands-on experience while learning about a prescriptive approach to automating RHEL in-place upgrades.

- You upgraded only a handful of RHEL cloud instances while progressing through the workshop exercises, but with the power of an enterprise deployment of AAP, this approach can be rolled out at scale across a large fleet of RHEL hosts.

- You learned why automated snapshot/rollback is one of the most important capabilities required to successfully deliver RHEL in-place upgrade automation. Snapshots not only eliminate the risk and anxiety experienced by an app team facing a RHEL upgrade, but they also help accelerate the development of robust upgrade automation playbooks.

- You also learned about the custom automation that must be developed to deal with the complex requirements of a large enterprise environment. We demonstrated a few examples of this including using Leapp custom actors for reporting special pre-upgrade checks as well as running Ansible playbooks to handle common remediations and third-party tools and agents.

- But the most important lesson we learned is "You can do this!"

### Step 2 - Activities for Extra Credit

Hopefully, these exercises have opened your eyes to what is possible, but we have just scratched the surface.

- Is it possible to upgrade from RHEL7 to RHEL9? While the Leapp framework doesn't support a "double upgrade" directly, it is possible to take a host that was upgraded from RHEL7 to RHEL8 and then upgrade it from there to RHEL9. You can try this with the three tier application instances in the workshop lab.

  There are a couple things to be aware of if you want to try it. You will first need to run the "LEAPP / 04 Commit" playbook job template. This job will delete the snapshot created for your RHEL7 to RHEL8 upgrade, so be sure you are happy with everything before you do this. While rolling back to RHEL7 will no longer be possible, you will be able to roll back to RHEL8 if needed after upgrading to RHEL9.

  Another consideration with going from RHEL7 to RHEL9 is the increased risk of application impacts. While RHEL system library forward binary compatibility is really solid between each RHEL major version, "N+2" compatibility is not guaranteed. Of course, the only way to know for sure is try it!

- If you skipped over any of the optional exercises, it's not too late to go back and try them now:

- The workshop lab environment is now yours to play with. Dream up your own ideas for additional learning and experimentation. Remember you can upgrade and roll back as often as you like. Rinse and repeat!

### Step 3 - Look at the Code

All of the Ansible roles and playbooks used in this workshop are maintained in upstream repositories that can be found on GitHub. Take some time to review the code and get engaged with the communities supporting these resources.

#### [redhat-cop/infra.leapp](https://github.com/redhat-cop/infra.leapp)

- The `infra.leapp` collection provides the Ansible role that generates the pre-upgrade reports and another that is used to perform the RHEL upgrades. This collection uses the Leapp framework for upgrades from RHEL7 and later, but also supports upgrading from RHEL6 using the older Red Hat Upgrade Tool. The collection is published on Ansible Galaxy [here](https://galaxy.ansible.com/infra/leapp) and also available from Ansible Automation Hub validated content [here](https://console.redhat.com/ansible/automation-hub/repo/validated/infra/leapp/). If you are planning to do RHEL in-place upgrades for your organization, these roles will help you quickly roll out proof-of-concept automation and start upgrading.

#### [oamg/leapp-supplements](https://github.com/oamg/leapp-supplements)

- Leapp Supplements is a repository of example Leapp custom actors. The CheckRebootHygiene actor that was demonstrated in the optional [Custom Pre-upgrade Checks](../1.5-custom-modules/README.md) exercise is maintained here. There is also a Makefile and RPM spec file that can be used to build packages for installing your Leapp custom actors.

#### [redhat-partner-tech/automated-satellite](https://github.com/redhat-partner-tech/automated-satellite)

- This is where you will find all of the AAP job templates and Ansible playbooks included in the workshop, specifically the `aap2-rhdp-prod` and `aap2-rhdp-dev` code branches. You can also explore the infrastructure/configuration as code (IaC/CaC) magic that is used to provision the workshop lab environment.

#### [redhat-cop/infra.lvm_snapshots](https://github.com/redhat-cop/infra.lvm_snapshots)

- Here you will find the upstream project used to build the Ansible collection for managing snapshot sets using LVM. If you are interested in automating LVM snapshots as explained in the [Let's Talk About Snapshots](../2.2-snapshots/README.md#lvm) exercise, review this collection project to get in on the action.

## Thank You!

If you enjoyed this workshop, please take a moment to give it a rating or write a review. If you have any ideas for improvements or new features, don't hesitate to raise an issue [here](https://github.com/redhat-cop/agnosticd/issues/new/choose), reference the workshop name `Ansible Workshop - Automated Satellite Workshop` and tagging/mentioning `@heatmiser` within the issue. All ideas and feedback are welcome!

---

**Navigation**

[Previous Exercise](../3.3-check-undo/README.md)

[Home](../README.md)
