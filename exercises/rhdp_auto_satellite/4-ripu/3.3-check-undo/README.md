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

In the previous exercise, we rolled back our three tier application servers. Now we will take a closer look at where that has left us and consider next steps.

### Step 1 - Our State After Rolling Back

In this step, we will repeat the observations we made on our host after the upgrade with the expectation that everything is back as it was before the upgrade.

- In the previous exercise, we checked that the RHEL version is reverted back. You can verify this at a shell prompt using commands like `cat /etc/redhat-release` and `uname -r` to output the OS release information and kernel version. You can also refresh the RHEL Web Console to confirm the RHEL version shown on the system overview page.

- If you inflicted some damage to any of the three tier application servers with the optional [Simulate conversion failure](../3.1-error-condition/README.md) exercise, you will now find no evidence of that. You could switch over to the Ansible Automation Platform UI and run the `CONVERT2RHEL / 99 - Three Tier App smoke test` job template to verify complete application stack functinality. Or check via some of the following:

  For example, did you delete everything with the `rm -rf /*` command or remove the standard C library with the `rpm -e --nodeps glibc` command? Your efforts to nuke the OS have been nullified!

  Did you break your tomcat application server by removing the JDK runtime package? If you check node2 now with the `rpm -qa | grep openjdk` command, you will see the package is installed.

  If you filled up your disk, check now with the `df -h /` command. You will see there is now plenty of free space reported.

  Looking for any app data you added or modified after the upgrade and you will find that all those changes are lost.
  
  ```
  [student@ansible-1 ~]$ ssh node3
  Last login: Thu Jun 27 05:08:29 2024 from ip-192-168-0-85.us-east-2.compute.internal
  [ec2-user@node3 ~]$ sudo su - postgres
  Last login: Fri Jun 21 20:48:59 UTC 2024 on pts/0
  -bash-4.2$ psql
  psql (9.2.24)
  Type "help" for help.

  postgres=# \l
                                  List of databases
    Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges   
  -----------+----------+----------+------------+------------+-----------------------
  db01      | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =Tc/postgres         +
            |          |          |            |            | postgres=CTc/postgres+
            |          |          |            |            | user01=CTc/postgres
  postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
  template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
            |          |          |            |            | postgres=CTc/postgres
  template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
            |          |          |            |            | postgres=CTc/postgres
  (4 rows)

  postgres=# \c db01
  You are now connected to database "db01" as user "postgres".
  db01=# \dt
              List of relations
  Schema |       Name       | Type  | Owner  
  --------+------------------+-------+--------
  public | 14-06-2024-21-53 | table | user01
  public | 14-06-2024-21-59 | table | user01
  public | 14-06-2024-22-02 | table | user01
  public | 15-06-2024-19-54 | table | user01
  public | 15-06-2024-20-16 | table | user01
  public | 17-06-2024-04-39 | table | user01
  public | 21-06-2024-20-52 | table | user01
  public | 21-06-2024-21-41 | table | user01
  public | 27-06-2024-05-08 | table | user01
  (9 rows)

  db01=# \q
  -bash-4.2$ exit
  logout
  [ec2-user@node3 ~]$ exit
  logout
  Shared connection to node3 closed.
  [student@ansible-1 ~]$
  ```
  Earlier in [exercise section 2.4](../2.4-check-three-tier-app/README.md), the `CONVERT2RHEL / 99 - Three Tier App smoke test` job template was launched to verify application stack functionality prior to rolling back the upgrade. The last task in the job output provided the table name to record:

`TASK [Fail if database db01 did not contain table 26-06-2024-17-56]`

  Looking at the table listing above, there is a table `27-06-2024-05-08` which corresponds to application functionality verification after the rollback was completed, however, table `26-06-2024-17-56` is not present. 

  What does this tell us about the snapshot scope implemented by our rollback playbook?

  Business units will not be happy about loss of data, so make sure to raise awareness of the risk to application data when "everything scope" snapshots are employed.

### Step 2 - What's Next?

No matter what the reason is for rolling back, the next step will be to decide what to do next.

- Maybe you rolled back because there was a failure with the Leapp upgrade itself or some custom automation meant to deal with your standard tools and agents. If so, assess what happened and use the experience to improve your automation to prevent similar issues going forward.

  Developing robust automation is an iterative process. Remember it's good to fail fast! Failed upgrades early in the development of your automation should be expected and will inform you about what adjustments need to be implemented along the way. Having an automated rollback capability helps accelerate the development of robust playbooks.

- What if you rolled back because application impact was discovered after the upgrade. In this case, it's important for the app team to investigate the cause of the impact. Once the cause is understood, roll back so what was learned can be applied to avoid the issue for subsequent upgrades.

  Understanding the cause of application impacts is also an iterative process. App teams must take the time required to fully assess any application issues when upgrading their dev and test servers, rolling back as often as needed. Use the lower environments in this manner so full preparations can be made before moving to production.

- After rolling back, the last pre-upgrade report generated before the upgrade will still be available. If no significant changes are made after rolling back, it is not necessary to generate a fresh pre-upgrade report before implementing any new/additional automation and trying another upgrade.

## Conclusion

In this exercise section, we reviewed the state of our three tier application servers after rolling back and we considered next steps for some different scenarios.

In the next and final section of the exercise, we'll review what we learned and explore some additional things you may want to play with in the workshop lab environment.

---

**Navigation**

[Previous Exercise](../3.2-rollback/README.md) - [Next Exercise](../3.4-conclusion/README.md)

[Home](../README.md)
