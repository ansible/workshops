# Workshop Exercise - Check if Upgrade Undone

## Table of Contents

- [Workshop Exercise - Check if Upgrade Undone](#workshop-exercise---check-if-upgrade-undone)
  - [Table of Contents](#table-of-contents)
  - [Objectives](#objectives)
  - [Guide](#guide)
    - [Step 1 - Our State After Rolling Back](#step-1---our-state-after-rolling-back)
    - [Step 2 - What's Next?](#step-2---whats-next)
  - [Conclusion](#conclusion)

## Objectives

* Validate that all changes and impacts caused by the upgrade are undone after rolling back
* Revisit the topic of snapshot scope
* Consider next steps after rolling back

## Guide

In the previous exercise, we rolled back one of our pet app servers. Now we will take a closer look at where that has left us and consider where do we go from there.

### Step 1 - Our State After Rolling Back

In this step, we will repeat the observations we made on our host after the upgrade with the expectation that everything is back as it was before the upgrade.

- In the previous exercise, we checked that the RHEL version is reverted back. You can verify this at a shell prompt using commands like `cat /etc/redhat-release` and `uname -r` to output the OS release information and kernel version. You can also refresh the RHEL Web Console to confirm the RHEL version shown on the system overview page.

- If you inflicted some damage to the pet app server with the optional [Trash the Instance](../3.1-rm-rf/README.md) exercise, you will now find no evidence of that.

  For example, did you delete everything with the `rm -rf /*` command or remove the standard C library with the `rpm -e --nodeps glibc` command? Your efforts to nuke the OS have been nullified!

  Did you break your pet application by removing the JDK runtime package? If you check now with the `rpm -q temurin-17-jdk` command, you will see the package is installed.

  If you filled up your disk, check now with the `df -h /` command. You will see there is now plenty of free space reported.

- If you installed the Spring Pet Clinic Sample Application from the optional [Deploy a Pet App](../1.6-my-pet-app/README.md) exercise, refresh the web user interface in your browser to verify it is running correctly after rolling back.

  > **Note**
  >
  > Because the external IP addresses of the EC2 instances provisioned for the workshop are dynamically assigned (i.e., using DHCP), it is possible that the web user interface URL may change after a reboot. If that happens, run this command at the shell prompt of the app server to determine the new URL for the application web user interface:
  >
  > ```
  > echo "http://$(curl -s ifconfig.me):8080"
  > ```

  Look for any app data you added or modified after the upgrade and you will find that all those changes are lost. What does this tell us about the snapshot scope implemented by our rollback playbook?

  The business will not be happy about losing their changes, so make sure they are aware of the risk to app data if you choose to do everything scope snapshots.

### Step 2 - What's Next?

No matter what the reason is for rolling back, the next step will be to decide what to do next.

- Maybe you rolled back because there was a failure with the Leapp upgrade itself or some custom automation meant to deal with your standard tools and agents. If so, assess what happened and use the experience to improve your automation to prevent similar issues going forward.

  Developing robust automation is an iterative process. Remember it's good to fail fast! Failed upgrades early in the development of your automation should be expected and will inform you about what needs fixed. Having an automated rollback capability helps accelerate the development of robust playbooks.

- What if you rolled back because application impact was discovered after the upgrade. In this case, it's important for the app team to investigate the cause of the impact. Once the cause is understood, roll back so what was learned can be applied to avoid the issue next time.

  Understanding the cause of application impacts is also an iterative process. App teams must take the time required to fully assess any application issues when upgrading their dev and test servers, rolling back as often as needed. Use the lower environments this way so everyone is fully prepared before moving to production.

- After rolling back, the last pre-upgrade report generated before the upgrade will still be available. If no significant changes are made after rolling back, it is not necessary to generate a fresh pre-upgrade report before trying another upgrade.

## Conclusion

In this exercise, we reviewed the state of our pet app server after rolling back and we considered next steps for some different scenarios.

In the next and final exercise of the workshop, we'll review what we learned and explore some additional things you may want to play with in the workshop lab environment.

---

**Navigation**

[Previous Exercise](../3.2-rollback/README.md) - [Next Exercise](../3.4-conclusion/README.md)

[Home](../README.md)
