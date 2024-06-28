# Workshop Exercise - Simulate upgrade failure

## Table of Contents

- [Workshop Exercise - Simulate upgrade failure](#workshop-exercise---simulate-upgrade-failure)
  - [Table of Contents](#table-of-contents)
  - [Optional Exercise](#optional-exercise)
  - [Objectives](#objectives)
  - [Guide](#guide)
    - [Step 1 - Select a Three Tier Application Server](#step-1---select-a-three-tier-application-server)
    - [Step 2 - Break your application](#step-2---break-your-application)
  - [Conclusion](#conclusion)

## Optional Exercise

This is an optional exercise. It is not required to successfully complete the workshop, but it will help demonstrate the effectiveness of rolling back a RHEL upgrade. Review the objectives listed in the next section to decide if you want to do this exercise or if you would rather skip ahead to the next exercise:

* [Exercise 3.2 - Run Rollback Job](3.2-rollback/README.md)

## Objectives

* Simulate a failed OS upgrade or application impact
* Demonstrate the scope of rolling back a snapshot

## Guide

Have you ever wanted to try doing `rm -rf /*` on a RHEL host just to see what happens? Or maybe you have accidentally done an equally destructive recursive command and already know the consequences. In this exercise, we are going to intentionally break one of the servers from our three tier application stack to demonstrate how rolling back can save the day.

Let's get started!

### Step 1 - Select a Three Tier Application Server

In the next exercise, we will be rolling back the RHEL upgrade on our three tier application stack.

- Choose one of the systems from the three tier application stack "stack01": node1, node2, or node3.

- Follow the steps you used with [Exercise 1.1: Step 2](../1.1-setup/README.md#step-2---open-a-terminal-session) to open a terminal session on the app server you have chosen to break. In this example, we are going to break the tomcat application tier server, node2.

- At the shell prompt, ssh to node2 and use the `sudo -i` command to switch to the root user. For example:

  ```
  [student@ansible-1 ~]$ ssh node2
  Last login: Wed Jun 26 20:23:52 2024 from 192.168.0.85
  [ec2-user@node2 ~]$ sudo -i
  Last login: Wed Jun 26 20:24:06 UTC 2024 on pts/0
  [root@node2 ~]#
  ```

  Verify you see a root prompt like the example above.

### Step 2 - Break your application

- When utilizing a 3rd-party JDK runtime package, a pre-upgrade finding warning of a potential risk may occur in some cases. The issue is that in the event that unresolvable dependencies are present, some 3rd-party JDK runtime packages might be removed during the upgrade. Of course, this did not happen in our case, as the three tier application stack utilizes OpenJDK packages provided by Red Hat and our application stack is functioning correctly.

  But what if we were using a 3rd-party JDK and the package was removed? Our three tier application stack utilizes a tomcat application and tomcat requires a JDK runtime to function. Without it, the tomcat application will be broken. We can simulate this by manually removing the package like this:

  ```
  rpm -e --nodeps java-1.8.0-openjdk java-1.8.0-openjdk-headless
  ```

  Now if you `reboot` node2, the three tier application stack will no longer function correctly, as the tomcat application will not be able to start and the following error will be seen when checking the tomcat service status on node2:

  ```
  [root@node2 ~]# reboot
  Shared connection to node2 closed.
  [student@ansible-1 ~]$ ssh node2
  Web console: https://node2.example.com:9090/ or https://192.168.0.216:9090/

  Last login: Wed Jun 26 20:42:49 2024 from 192.168.0.85
  [ec2-user@node2 ~]$ sudo -i
  [root@node2 ~]# systemctl status tomcat
  ● tomcat.service - Apache Tomcat Web Application Container
    Loaded: loaded (/usr/lib/systemd/system/tomcat.service; enabled; vendor preset: disabled)
    Active: failed (Result: exit-code) since Wed 2024-06-26 21:35:06 UTC; 6min ago
    Process: 1286 ExecStart=/usr/libexec/tomcat/server start (code=exited, status=127)
  Main PID: 1286 (code=exited, status=127)

  Jun 26 21:35:06 node2.example.com server[1286]: /usr/libexec/tomcat/server: Failed to set JAVACMD
  Jun 26 21:35:06 node2.example.com server[1286]: Java virtual machine used:
  Jun 26 21:35:06 node2.example.com server[1286]: classpath used: /usr/share/tomcat/bin/bootstrap.jar:/usr/share/tomcat/bin/tomcat-juli.jar:
  Jun 26 21:35:06 node2.example.com server[1286]: main class used: org.apache.catalina.startup.Bootstrap
  Jun 26 21:35:06 node2.example.com server[1286]: flags used: -Djavax.sql.DataSource.Factory=org.apache.commons.dbcp.BasicDataSourceFactory
  Jun 26 21:35:06 node2.example.com server[1286]: options used: -Dcatalina.base=/usr/share/tomcat -Dcatalina.home=/usr/share/tomcat -Djava.endorsed.dirs= -Dj>
  Jun 26 21:35:06 node2.example.com server[1286]: arguments used: start
  Jun 26 21:35:06 node2.example.com server[1286]: /usr/libexec/tomcat/functions: line 24: exec: : not found
  Jun 26 21:35:06 node2.example.com systemd[1]: tomcat.service: Main process exited, code=exited, status=127/n/a
  Jun 26 21:35:06 node2.example.com systemd[1]: tomcat.service: Failed with result 'exit-code'.
  lines 1-16/16 (END)
  ```

  This is a realistic example of an application impact during upgrades that can be reversed by rolling back the upgrade.

## Conclusion

Congratulations, you have broken the application stack. Wasn't that fun?

In the next exercise, you will correct the issue by rolling back the upgrade.

---

**Navigation**

[Previous Exercise](../2.4-check-pet-app/README.md) - [Next Exercise](../3.2-rollback/README.md)

[Home](../README.md)
