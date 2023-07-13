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

### Step 2 - Choose your Poison

The `rm -rf /*` command appears frequently in the urban folklore about Unix disasters. The command recursively and forcibly tries to delete every directory and file on a system. When it is run with root privileges, this command will quickly break everything on your pet app server and render it unable to reboot ever again. However, there are much less spectacular ways to mess things up.

Mess up your app server by choosing one of the following suggestions or dream up your own.

#### Delete everything

- As mentioned already, `rm -rf /*` can be fun to try. Expect to see lots of warnings and error messages. Even with root privileges, there will be "permission denied" errors because of read-only objects under pseudo-filesystem like `/proc` and `/sys`. Don't worry, irreparable damage is still being done.

  You might be surprised that you will get back to a shell prompt after this. While all files have been deleted from the disk, already running processes like your shell will continue to be able to access any deleted files to which they still have an open file descriptor. Built-in shell commands may even still work, but most commands will result in a "command not found" error.

  If you want to reboot the instance to prove that it will not come back up, you will not be able to use the `reboot` command, however, the `echo b > /proc/sysrq-trigger` might work.

#### Uninstall glibc

- The command `rpm -e --nodeps glibc` will uninstall the glibc package, removing the standard C library upon which all other libraries depend. The damage done by this command is just as bad as the the previous example, but without all the drama. This package also provides the dynamic linker/loader, so now commands will fail with errors like this:

  ```
  [root@cute-bedbug ~]# reboot
  -bash: /sbin/reboot: /lib64/ld-linux-x86-64.so.2: bad ELF interpreter: No such file or directory
  ```

  If you want to do a `reboot` command, use `echo b > /proc/sysrq-trigger` instead.

#### Break the application

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

#### Wipe the boot record

- The `dd if=/dev/zero of=/sys/block/* count=1` command will clobber the master boot record of your instance. It's rather insidious because you will see that everything continues to function perfectly after running this command, but after you do a `reboot` command, the instance will not come back up again.

#### Fill up your disk

- Try the `while fallocate -l9M $((i++)); do true; done; yes > $((i++))` command. While there are many ways you can consume all the free space in a filesystem, this command gets it done in just a couple seconds. Use a `df -h /` command to verify your root filesystem is at 100%.

#### Set off a fork bomb

- The shell command `:(){ :|:& };:` will trigger a [fork bomb](https://en.wikipedia.org/wiki/Fork_bomb). When this is done with root privileges, system resources will be quickly exhausted resulting in the server entering a "hung" state. Use the fork bomb if you want to demonstrate rolling back a server that has become unresponsive.

## Conclusion

Congratulations, you have trashed one of your app servers. Wasn't that fun?

In the next exercise, you will untrash it by rolling back.

---

**Navigation**

[Previous Exercise](../2.4-check-pet-app/README.md) - [Next Exercise](../3.2-rollback/README.md)

[Home](../README.md)
