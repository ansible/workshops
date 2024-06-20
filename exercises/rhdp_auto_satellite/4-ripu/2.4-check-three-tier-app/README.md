# Workshop Exercise - How is the Pet App Doing?

## Table of Contents

- [Workshop Exercise - How is the Pet App Doing?](#workshop-exercise---how-is-the-pet-app-doing)
  - [Table of Contents](#table-of-contents)
  - [Objectives](#objectives)
  - [Guide](#guide)
    - [Step 1 - Retest our Pet Application](#step-1---retest-our-pet-application)
    - [Step 2 - Add More Records to the Database](#step-2---add-more-records-to-the-database)
  - [Conclusion](#conclusion)

## Objectives

* Confirm our pet app is still functioning as expected after the upgrade
* Add new records to the app database to see what happens when rolling back

## Guide

In [Exercise 1.6](../1.6-my-pet-app/README.md) we installed a sample pet application and tested its functionality. Now that we have upgraded the RHEL version of our app server, let's retest to see if there has been any impact.

### Step 1 - Retest our Pet Application

It's time to repeat the testing you did for [Step 3](../1.6-my-pet-app/README.md#step-3---test-the-pet-application) in the previous exercise.

- You should usually be able to access the application web user interface at the same address you used before. If you still have the app open in one of you browser tabs, try refreshing the page.

  > **Note**
  >
  > Because the external IP addresses of the EC2 instances provisioned for the workshop are dynamically assigned (i.e., using DHCP), it is possible that the web user interface URL may change after a reboot. If that happens, run this command at the shell prompt of the app server to determine the new URL for the application web user interface:
  >
  > ```
  > echo "http://$(curl -s ifconfig.me):8080"
  > ```

- Did you previously use the "Edit Owner" or "Add New Pet" buttons to change any data or add new records? If so, check to see if that data is still there and displayed correctly.

- If you observe any changes in your application behavior or the application isn't working at all, troubleshoot the issue to try to narrow down the root cause. Make note of any issues so you can retest after rolling back the upgrade.

### Step 2 - Add More Records to the Database

In [Exercise 2.2](../2.2-snapshots/README.md), we considered the potential pitfalls of including app data in the scope of our snapshot. Imagine what would happen if your app at first appeared fine after the upgrade, but an issue was later discovered after the app had been returned to production use.

- Add a new record to the database. For example, add a new pet record with the name "Post Upgrade" to make it easy to distinguish. Remember this record to see what happens after we revert the OS upgrade in the next section of the workshop.

- What will be the business impact if data updates are rolled back with the upgrade? That is exactly the problem we will demonstrate next because the pet app servers deployed in this workshop do not have separate volumes to isolate the OS from the app data.

## Conclusion

In this exercise, we observed that the RHEL in-place upgrade left our application untouched and we found that it still works as expected after the upgrade. Then we added some new app data to demonstrate what will happen after rolling back the upgrade.

This concludes the RHEL Upgrade section of the workshop. In the next and final section, we will be rolling back the RHEL upgrade, taking us right back to where we started.

---

**Navigation**

[Previous Exercise](../2.3-check-upg/README.md) - [Next Exercise](../3.1-rm-rf/README.md)

[Home](../README.md)
