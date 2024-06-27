# Workshop Exercise - Rinse and Repeat

## Table of Contents

- [Workshop Exercise - Rinse and Repeat](#workshop-exercise---rinse-and-repeat)
  - [Table of Contents](#table-of-contents)
  - [Objectives](#objectives)
  - [Guide](#guide)
    - [Step 1 - What You Learned](#step-1---what-you-learned)
    - [Step 2 - Activities for Extra Credit](#step-2---activities-for-extra-credit)
    - [Step 3 - Look at the Code](#step-3---look-at-the-code)
      - [redhat-cop/infra.convert2rhel](#redhat-copinfraconvert2rhel)
      - [redhat-partner-tech/leapp-project](#redhat-partner-techleapp-project)
      - [swapdisk/snapshot](#swapdisksnapshot)
  - [Thank You!](#thank-you)

## Objectives

* Review what we have learned in this workshop
* Consider ideas for further exploration
* Look at the code and get involved upstream

## Guide

Congratulations! You have reached the end of the CentOS to RHEL Conversion Automation exercises. You are now armed with the knowledge needed to start developing an automation solution to help your organization manage CentOS conversions at scale.

Let's review what we learned and think about what's next.

### Step 1 - What You Learned

With these exercises, you gained hands-on experience while learning about a prescriptive approach to automating CentOS to RHEL conversions.

- You converted a handful of CentOS cloud instances while progressing through the workshop exercises, but with the power of an enterprise deployment of AAP, this approach can be rolled out at scale across a large fleet of CentOS hosts.

- You learned why automated snapshot/rollback is one of the most important capabilities required to successfully deliver CentOS to RHEL conversion automation. Snapshots/backups not only eliminate the risk and anxiety experienced by an app team facing a CentOS conversion, but they also help accelerate the development of robust conversion automation playbooks.

- But the most important lesson we learned is "You can do this!"

### Step 2 - Activities for Extra Credit

Hopefully, these exercises have opened your eyes to what is possible, but we have just scratched the surface.

- Is it possible to convert/upgrade from CentOS7 directly to RHEL8 or RHEL9? While the Convert2RHEL and Leapp frameworks do not support a "conversion plus upgrades" directly, it is possible to take a host that was converted from CentOS7 to RHEL7 and then upgrade from there to RHEL8 and, if desired, upgrade onwards to RHEL 9. You can follow this path in this workshop via the next exercise in this workshop series, **Automated Satellite Workshop: RHEL In-place Upgrade Automation exercise**

  There are a couple things to be aware of if you want to continue through to the RHEL In Place Upgrade content. If you stepped through the conversion rollback exercise, you will have to perform the conversion again and once verified as successful, you will need to run the "CONVERT2RHEL / 04 Commit" playbook job template. This job will delete the snapshot created for your CentOS7 to RHEL7 conversion, so be sure you are happy with everything before you do this. While rolling back to CentOS7 will no longer be possible, you will be able to roll back to RHEL7 if needed after upgrading to RHEL8.

  Another consideration with going from CentOS7 to RHEL9 is the increased risk of application impacts. While RHEL system library forward binary compatibility is solid between each RHEL major version, "N+2" compatibility is not guaranteed. Of course, the only way to know for sure is to try it!

- If you skipped over any of the optional exercises, it is not too late to go back and try them now.

- The workshop lab environment is now yours to play with. Dream up your own ideas for additional learning and experimentation. Remember you can upgrade and roll back as often as you like. Rinse and repeat!

### Step 3 - Look at the Code

All of the Ansible roles and playbooks used in this workshop are maintained in upstream repositories that can be found on GitHub. Take some time to review the code and get engaged with the communities supporting these resources.

#### [redhat-cop/infra.convert2rhel](https://github.com/redhat-cop/infra.convert2rhel)

- The `infra.convert2rhel` Ansible collection provides the Ansible role that generates the pre-conversion analysis reports and another that is used to perform conversions for EL rebuild OS's. This collection serves as a framework around the Convert2RHEL utility for conversions from CentOS7, Oracle Linux 7 and more. The collection is published on Ansible Galaxy [here](https://galaxy.ansible.com/ui/repo/published/infra/convert2rhel/) and also available from Ansible Automation Hub validated content [here - Red Hat account required](https://console.redhat.com/ansible/automation-hub/repo/validated/infra/convert2rhel/). If you are planning to do EL conversions for your organization, these Ansible collections will help you quickly roll out proof-of-concept automation and start upgrading.

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
