# Workshop Exercise - Perform Recommended Remediation

## Table of Contents

- [Workshop Exercise - Perform Recommended Remediation](#workshop-exercise---perform-recommended-remediation)
  - [Table of Contents](#table-of-contents)
  - [Objectives](#objectives)
  - [Guide](#guide)
    - [Step 1 - Explore Options for Resolving Inhibitors](#step-1---explore-options-for-resolving-inhibitors)
    - [Step 2 - Managing the Leapp Answer File](#step-2---managing-the-leapp-answer-file)
    - [Step 3 - Resolving Inhibitors Using a Remediation Playbook](#step-3---resolving-inhibitors-using-a-remediation-playbook)
  - [Conclusion](#conclusion)

## Objectives

* Consider different options for resolving inhibitor risk findings
* Learn how to use the `leapp_answerfile` variable of the `analysis` role
* Use a remediation playbook to proactively prepare for pre-upgrade

## Guide

### Step 1 - Explore Options for Resolving Inhibitors

In the previous exercise, we reviewed the Leapp pre-upgrade reports that were generated for our RHEL7 and RHEL8 pet application servers. With the RHEL8 hosts, there were no inhibitor risk findings reported, so those are good to go and ready to try upgrading. However, there were a couple inhibitors reported for the RHEL7 hosts. We must take action to resolve them before those hosts can be upgraded.

We are now here in our automation approach workflow:

![Automation approach workflow diagram with apply recommended remediations step highlighted](images/ripu-workflow-hl-remediate.svg)

- Let's start by dissecting one of our inhibitor findings:

  ![Details view of missing required answers in the answer file](images/missing_answers_dissected.svg)

  <sub>![1.](images/circle_1.svg)</sub> Each finding has a unique title.

  <sub>![2.](images/circle_2.svg)</sub> A risk factor is assigned to each finding, but as we discussed in the previous exercise, this may be more nuanced than can be indicated by a simple High, Medium, Low or Info rating.

  <sub>![3.](images/circle_3.svg)</sub> The summary provides a detailed explanation of the risk and solution recommendation.

  <sub>![4.](images/circle_4.svg)</sub> Under remediation, we are given a fairly prescriptive recommendation.

  <sub>![5.](images/circle_5.svg)</sub> Sometimes, the remediation also includes an exact command like this one.

- When a remediation command is given such as with the example above, there are a number of options we can choose from for how to execute the command. Obviously, we could go with the quick and dirty method of getting to a root shell prompt on the host to cut and paste the command or manually edit the answerfile. Of course, going that way is prone to human error and doesn't scale well. Another option would be to use the "Run Remediation" button shown above the command. Using this option, the RHEL Web Console executes the command for us. While doing this is less prone to human error, it still doesn't scale well as it's only going to run on this single host.

- In the next steps, we'll look at how we can use the scale of Ansible Automation Platform (AAP) to perform remediations in bulk across a large RHEL estate.

### Step 2 - Managing the Leapp Answer File

The Leapp framework uses an answer file as a means of accepting user input choices. This is explained in greater detail in the [Asking user questions](https://leapp.readthedocs.io/en/latest/dialogs.html) section of the Leapp developer documentation. The inhibitor finding we dissected in the previous step is looking for us to make a decision or, more specifically, asking us to acknowledge we are aware that Leapp will disable the pam_pkcs11 PAM module during the RHEL upgrade.

- In [Exercise 1.2 - Run Pre-upgrade Jobs](../1.2-preupg/README.md), we launched a playbook that runs the pre-upgrade report using the `analysis` role from the `infra.leapp` Ansible collection. Look at the [documentation for this role](https://github.com/redhat-cop/infra.leapp/blob/main/roles/analysis/README.md). Do you see where it supports a `leapp_answerfile` input variable. We can set the variable to automatically populate the Leapp answer file.

- Let's try running the pre-upgrade job again with this variable defined. Launch the "AUTO / 01 Analysis" job template the same as you did under [Exercise 1.2, Step 2](../1.2-preupg/README.md#step-2---use-aap-to-launch-an-analysis-playbook-job), except this time, we will add this setting when we get to the Variables prompt:

  ```json
    "leapp_answerfile": "[remove_pam_pkcs11_module_check]\nconfirm = True\n",
  ```
  For example:

  ![Setting the `leapp_answerfile` input variable](images/analysis_leapp_answerfile.svg)

  After making the variable setting as shown above, click the "Next" button. This will lead to the job template survey prompt. Previously, we used the "ALL_rhel" option to run the pre-upgrade on all our pet servers. However, our `leapp_answerfile` setting is specific to our RHEL7 hosts, so choose the "rhel7" option this time:

  ![Choose "rhel7" at the survey prompt](images/analysis_survey_rhel7_only.svg)

  Click the "Next" button to proceed to the preview prompt. If you are satisfied with the job preview, use the "Launch" button to start the job.

- As before, the AAP Web UI will navigate automatically to the job output page after you start the job. The job will take a few minutes to finish and then you should see the "PLAY RECAP" at the end of the job output.

- Now go back to your RHEL Web Console browser tab and navigate to the pre-upgrade report of one of the RHEL7 hosts.

  > **Note**
  >
  > You may need to refresh the browser using Ctrl-R to see the newly generated report.

  You should see that the "Missing required answers in the answer file" inhibitor finding is no longer being reported.

  For example:

  ![Pre-upgrade report of RHEL7 host without answer file inhibitor](images/rhel7_answer_fixed.svg)

  But we still have the "Possible problems with remote login using root account" inhibitor which we need to fix. Let's look at that next.

### Step 3 - Resolving Inhibitors Using a Remediation Playbook

In the previous step, we were able to resolve an inhibitor finding by simply setting the `leapp_answerfile` input variable supported by the `infra.leapp` Ansible collection `analysis` role. While that's a convenient way to resolve an answerfile inhibitor, our next inhibitor can't be resolved that way.

- Here is our other inhibitor finding:

  ![Details view of missing required answers in the answer file](../1.3-report/images/root_account_inhibitor.svg)

  Like the previous inhibitor finding, this one also provides a detailed summary and a a fairly prescriptive recommended remediation. However, it does not recommend an exact remediation command. Instead, the remediation recommends making edits to the `/etc/ssh/sshd_config` file.

- Of course, we're not going to just login to a root shell and `vi` the configuration file, are we? Right, let's make a playbook to automate the required remediations. Here's a task that should do the trick:

  ```yaml
  - name: Configure sshd
    ansible.builtin.lineinfile:
      path: "/etc/ssh/sshd_config"
      regex: "^(#)?{{ item.key }}"
      line: "{{ item.key }} {{ item.value }}"
      state: present
    loop:
      - {key: "PermitRootLogin", value: "prohibit-password"}
      - {key: "PasswordAuthentication", value: "no"}
    notify:
      - Restart sshd
  ```

  While we're at it, let's also add a task to take care of the answer file inhibitor using the `leapp answer` command. For example:

  ```yaml
  - name: Remove pam_pkcs11 module
    ansible.builtin.shell: |
      set -o pipefail
      leapp answer --section remove_pam_pkcs11_module_check.confirm=True
    args:
      executable: /bin/bash
  ```

- You will find the tasks above in the playbook [`remediate_rhel7.yml`](https://github.com/redhat-partner-tech/leapp-project/blob/main/remediate_rhel7.yml#L21-L38). There are a few more remediation task examples in this playbook as well. The "OS / Remediate" job template is already set up to execute this playbook, so let's use it to remediate our RHEL7 hosts.

- Return to your AAP Web UI browser tab. Navigate to Resources > Templates on the AAP Web UI and open the "OS / Remediate" job template. Click the "Launch" button to get started.

- This will bring you to the job template survey prompt. Again, choose the "rhel7" option at the "Select inventory group" prompt because our remediation playbook is specific to the pre-upgrade findings of our RHEL7 hosts. Then click the "Next" button. If you are satisfied with the job preview, use the "Launch" button to submit the job. This playbook includes only a small number of tasks and should run pretty quickly.

- When the "OS / Remediate" job is finished, launch the "AUTO / 01 Analysis" job template one more time again taking care to choose the "rhel7" option at the "Select inventory group" prompt. When the job completes, go back to the RHEL Web Console of your RHEL7 host and refresh the report. You should now see there are no inhibitors:

  ![Pre-upgrade report of RHEL7 host with no more inhibitors](images/rhel7_no_inhibitors.svg)

  With no inhibitors indicated on our RHEL7 and RHEL8 pet servers, we are ready to try the RHEL upgrade.

## Conclusion

In this exercise, we looked at the different ways we can resolve inhibitor risk findings. We learned how to use the `leapp_answerfile` variable of the `analysis` role to manage the Leapp answer file. Finally, we used an example remediation playbook to demonstrate how we could address pre-upgrade inhibitor findings at scale across our RHEL estate.

Now we are ready to try upgrading our RHEL pet app servers, but before we get to that, there are two more optional exercises in this section of the workshop:

- [Exercise 1.5 - Custom Pre-upgrade Checks](../1.5-custom-modules/README.md)
- [Exercise 1.6 - Deploy a Pet Application](../1.6-my-pet-app/README.md)

These exercises are not required to successfully complete the workshop, but we recommend doing them if time allows. If you can't wait and want skip ahead to upgrading your RHEL hosts, strap in for this exciting exercise:

- [Exercise 2.1 - Run the RHEL Upgrade Jobs](../2.1-upgrade/README.md)

---

**Navigation**

[Previous Exercise](../1.3-report/README.md) - [Next Exercise](../1.5-custom-modules/README.md)

[Home](../README.md)
