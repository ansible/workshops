# Workshop Exercise - Check if the Upgrades Worked

## Table of Contents

- [Workshop Exercise - Check if the Upgrades Worked](#workshop-exercise---check-if-the-upgrades-worked)
  - [Table of Contents](#table-of-contents)
  - [Objectives](#objectives)
  - [Guide](#guide)
    - [Step 1 - Review the Upgrade Playbook Job Log](#step-1---review-the-upgrade-playbook-job-log)
    - [Step 2 - Verify the Hosts are Upgraded to Next RHEL Version](#step-2---verify-the-hosts-are-upgraded-to-next-rhel-version)
  - [Conclusion](#conclusion)

## Objectives

* Review the upgrade playbook job log
* Verify our pet application servers are running the newer RHEL version

## Guide

In the previous exercises, we review pre-upgrade reports and performed some recommended remediations. If you tried the optional exercises, you also learned about custom pre-upgrade checks and installed a sample pet application. After all of that, you finally launched the Ansible playbook jobs to run the RHEL in-place upgrades on your servers.

It's time to see verify the result of the upgrades and let our application teams assess if their pet apps are still good. We are here in the our RHEL in-place upgrade automation workflow:

![Automation approach workflow diagram with app validation steps highlighted](images/ripu-workflow-hl-validate.svg)

Let's get started!

### Step 1 - Review the Upgrade Playbook Job Log

The first thing we want to do is see if the job running the upgrade playbooks has finished successfully.

- Return to the AAP Web UI tab in your web browser. Navigate to Views > Jobs and then open the "OS / Upgrade" playbook run entry to see the log output from the upgrades.

  > **Note**
  >
  > You will also see an entry for the "AUTO / 02 Upgrade" workflow job. Workflow jobs launch a number of playbook runs. To see the playbook log output, we need to open the playbook run entry, not the workflow job entry.

  For example:

  ![AAP Web UI listing upgrade job entries](images/upgrade_jobs.svg)

- If the playbook run finished without any failed tasks, you should see "Successful" displayed with a green checkmark.

  > **Note**
  >
  > If you see "Running" with spinning arrows, the playbook is still running. Wait for the playbook run to finish before moving on with this exercise.

  Scroll down to the end of the log output to see the "PLAY RECAP" indicating the success or failure status for the playbook run executed on each host. Here is what you should expect to see:

  ![AAP Web UI showing successful upgrade playbook run play recap](images/upgrade_play_recap.svg)

  If there are no failed runs, the RHEL in-place upgrade is done on all of our pet app servers.

### Step 2 - Verify the Hosts are Upgraded to Next RHEL Version

Now let's make sure our pet app servers are actually upgraded to the next RHEL version.

- In [Exercise 1.3: Step 2](../1.3-report/README.md#step-2---navigating-the-rhel-web-console), you used the RHEL Web Console to check the installed RHEL versions on your pet app servers. Let's repeat those steps to see the RHEL versions reported after our upgrades.

  Return to your RHEL Web Console browser tab and use the remote host menu to navigate to the web consoles of each of your pet app servers. The RHEL Web Console system overview page should now show the upgraded versions.

  > **Note**
  >
  > You may need to refresh the browser using Ctrl-R to see the newly reported RHEL version.

  For example, this pet app server that previously had RHEL8 is now reporting RHEL9:

  ![fluent-bee running Red Hat Enterprise Linux 9.2 (Plow)](images/rhel9_upgraded.svg)

  Here is an example one that was previously RHEL7 now running RHEL8:

  ![vocal-hyena running Red Hat Enterprise Linux Server 8.8 (Oopta)](images/rhel8_upgraded.svg)

- You can also check the RHEL and kernel versions from the command line following the steps you used with [Exercise 1.1: Step 2](../1.1-setup/README.md#step-2---open-a-terminal-session).

  At the shell prompt of your pet app servers, use the `cat /etc/redhat-release` and `uname -r` commands. Here's an example showing a pet app server that was upgraded to RHEL9:

  ![command output showing RHEL9 is installed](images/rhel9_commands.svg)

## Conclusion

In this exercise, we observed that the upgrade playbook runs completed successfully. We then used the RHEL Web Console and the command line to verify the new RHEL versions were installed.

If you deployed a sample pet application in the previous optional exercise, continue here to verify the pet application is still functioning as expected after the RHEL upgrades:

- [Exercise 2.4 - How is the Pet App Doing?](../2.4-check-pet-app/README.md)

Otherwise, you may skip ahead to the next section of the workshop where we will demonstrate rolling back the RHEL upgrade, starting with these exercises:

- [Exercise 3.1 - (Optional) Trash the Instance](../3.1-rm-rf/README.md)
- [Exercise 3.2 - Run Rollback Job](../3.2-rollback/README.md)

---

**Navigation**

[Previous Exercise](../2.1-upgrade/README.md) - [Next Exercise](../2.4-check-pet-app/README.md)

[Home](../README.md)
