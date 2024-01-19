# Workshop Exercise - Trash the Instance

## Table of Contents

- [Workshop Exercise - Trash the Instance](#workshop-exercise---trash-the-instance)
  - [Table of Contents](#table-of-contents)
  - [Optional Exercise](#optional-exercise)
  - [Objectives](#objectives)
  - [Guide](#guide)
    - [Step 1 - Select a Pet App Server](#step-1---select-a-pet-app-server)
    - [Step 2 - Choose your Poison](#step-2---choose-your-poison)
      - [Delete everything](#delete-everything)
      - [Uninstall glibc](#uninstall-glibc)
      - [Break the application](#break-the-application)
      - [Wipe the boot record](#wipe-the-boot-record)
      - [Fill up your disk](#fill-up-your-disk)
      - [Set off a fork bomb](#set-off-a-fork-bomb)
  - [Conclusion](#conclusion)

## Optional Exercise

This is an optional exercise. It is not required to successfully complete the workshop, but it will help demonstrate the effectiveness of rolling back a RHEL upgrade. Review the objectives listed in the next section to decide if you want to do this exercise or if you would rather skip ahead to the next exercise:

* [Exercise 3.2 - Run Rollback Job](3.2-rollback/README.md)

## Objectives

* Simulate a failed OS upgrade or application impact
* Demonstrate the scope of rolling back a snapshot

## Guide

Have you ever wanted to try doing `rm -rf /*` on a RHEL host just to see what happens? Or maybe you have accidentally done an equally destructive recursive command and already know the consequences. In this exercise, we are going to intentionally mess up one of our pet app servers to demonstrate how rolling back can save the day.

Let's get started!

### Step 1 - Select a Pet App Server

In the next exercise, we will be rolling back the RHEL upgrade on one of our servers.

- Choose an app server. It can be one of the RHEL7 instances that is now on RHEL8, or one of the RHEL8 instances that was upgraded to RHEL9.

- Follow the steps you used with [Exercise 1.1: Step 2](../1.1-setup/README.md#step-2---open-a-terminal-session) to open a terminal session on the app server you have chosen to roll back.

- At the shell prompt, use the `sudo -i` command to switch to the root user. For example:

  ```
  [ec2-user@cute-bedbug ~]$ sudo -i
  [root@cute-bedbug ~]#
  ```

  Verify you see a root prompt like the example above.

### Step 2 - Break your application

- In [Exercise 1.6: Step 5](../1.6-my-pet-app/README.md#step-5---run-another-pre-upgrade-report), we observed a pre-upgrade finding warning of a potential risk that our `temurin-17-jdk` 3rd-party JDK runtime package might be removed during the upgrade in case it had unresolvable dependencies. Of course, we know this did not happen because our pet app is still working perfectly.

  But what if this package did get removed? Our pet app requires the JDK runtime to function. Without it, our application will be broken. We can simulate this by manually removing the package like this:

  ```
  dnf -y remove temurin-17-jdk
  ```

  Now if you `reboot` the app server, the pet app will not come back up and the following error will be seen at the end of the `~/app.log` file:

  ```
  ...
  which: no javac in (/home/ec2-user/.local/bin:/home/ec2-user/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin)
  Error: JAVA_HOME is not defined correctly.
  We cannot execute
  ```

  This is a realistic example of application impact that can be reversed by rolling back the upgrade.

## Conclusion

Congratulations, you have trashed one of your app servers. Wasn't that fun?

In the next exercise, you will untrash it by rolling back the upgrade.

---

**Navigation**

[Previous Exercise](../2.4-check-pet-app/README.md) - [Next Exercise](../3.2-rollback/README.md)

[Home](../README.md)
