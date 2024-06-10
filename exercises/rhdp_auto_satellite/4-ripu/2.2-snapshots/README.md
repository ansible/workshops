# Workshop Exercise - Let's Talk About Snapshots

## Table of Contents

- [Workshop Exercise - Let's Talk About Snapshots](#workshop-exercise---lets-talk-about-snapshots)
  - [Table of Contents](#table-of-contents)
  - [Objectives](#objectives)
  - [Guide](#guide)
    - [Step 1 - What are Snapshots and What are They Not](#step-1---what-are-snapshots-and-what-are-they-not)
    - [Step 2 - Assessing Different Snapshot Solutions](#step-2---assessing-different-snapshot-solutions)
      - [LVM](#lvm)
      - [VMware](#vmware)
      - [Amazon EBS](#amazon-ebs)
      - [Break Mirror](#break-mirror)
      - [ReaR](#rear)
    - [Step 3 - Snapshot Scope](#step-3---snapshot-scope)
    - [Step 4 - Choosing the Best Snapshot Solution](#step-4---choosing-the-best-snapshot-solution)
  - [Conclusion](#conclusion)

## Objectives

* Understand the difference between backups and snapshots
* Learn about some of the different ways of doing snapshots
* Be prepared for the challenges and barriers you may encounter automating snapshots
* Consider the appropriate snapshot scope for your organization

## Guide

In the previous exercise, we launched the automation to start the RHEL in-place upgrades of our pet application servers. The first step of the upgrade workflow template is to create a snapshot for each RHEL instance being upgraded. If something goes wrong with an upgrade, the snapshot makes it possible to quickly undo the upgrade.

Automating snapshots can be one of the most difficult features of the RHEL in-place upgrade solution approach. In this exercise, we will explore some of the challenges that enterprises face and look at strategies for overcoming them.

Let's start by defining exactly what we mean when we talk about snapshots.

### Step 1 - What are Snapshots and What are They Not

Most organizations with a mature traditional computing environment will have standards and tools implemented for doing backups. Typically, backups will be performed on a periodic schedule. More critical or more dynamic data might be backed up more frequently than mostly static data. There is often a strategy where full backups are performed only occasionally and incremental backups are used to save changed file more often.

The reason for doing backups is to be able to recover data that has been lost for any reason. If data is corrupted because of an operations issue or software defect or accidentally deleted, backups make it easy to turn the clock back and restore the lost data.

But when an entire server is lost, using backups to recover is more difficult because a new operating system must first be installed before anything can be restored from the backup. The data can be spread out across a full backup as well as multiple incremental backups, further increasing the time for a full server recovery. Most organizations only use their backup solution to restore individual files or directories, but they are not as prepared to recover everything on a server. Even if they are, such a recovery will take a long time.

Snapshots are different in that they do not backup and restore individual files. Instead, backups operate at a storage device level, instantly saving the contents of an entire logical volume or virtual disk. Unlike backups, snapshots do not make a copy of the data being backed up, but rather mark a point in time after which a copy of all modified data is copied going forward. For this reason, the underlying technique used for snapshots is often referred to as "copy-on-write" or COW.

While COW snapshots are not a substitute for traditional full and incremental backups, they do offer a number of advantages. The most important advantage is that creating and rolling back snapshots happens almost instantaneously as compared to hours or longer for traditional backup and restore. It is this ability to quickly take an entire server back in time that makes snapshots ideal for reducing the risk of performing RHEL in-place upgrades.

### Step 2 - Assessing Different Snapshot Solutions

There are a number of different types of snapshot solutions you may choose from. Each has their own benefits and drawbacks as summarized in the table below:

| Snapshot type | Works with | Benefits | Drawbacks |
| ------------- | ---------- | -------- | --------- |
| LVM |<ul><li>Bare metal</li><li>On-prem VMs</li><li>Cloud*</li></ul>|<ul><li>No external API access required</li><li>Scope can be just OS or everything</li></ul>|<ul><li>Free space required in volume group</li>Snapshots can run out of space if not sized correctly</li><li>Automation must backup and restore /boot separately</ul>|
| VMware |<ul><li>On-prem VMs (ESX)</li></ul>|<ul><li>Simple and reliable</li><li>Scope includes everything</li></ul>|<ul><li>Doesn't support bare metal, etc.</li><li>Using VMware snapshot for over 3 days is discouraged</li><li>Getting API access can be difficult</li><li>No free space in datastores because of overcommitment</li><li>Everything scope might be too much</li></ul>|
| Amazon EBS |<ul><li>Amazon EC2</li></ul>|<ul><li>Simple and reliable</li><li>Unlimited storage capacity</li><li>Scope can be just OS or everything</li></ul>|<ul><li>Only works on AWS</li></ul>|
| Break Mirror |<ul><li>Bare metal</li></ul>|<ul><li>Alternative to LVM for servers with hardware RAID</li></ul>|<ul><li>Significant development and testing effort required</li><li>RAID and Redfish API standards vary across different vendors and hardware models</li></ul>|
| ReaR |<ul><li>Bare metal</li><li>On-prem VMs</li></ul>|<ul><li>Method of last resort if no snapshot options will work</li></ul>|<ul><li>Not really a snapshot, but does offer boot ISO full recovery capability</li></ul>|

The following sections explain the pros and cons in detail.

#### LVM

The Logical Volume Manager (LVM) is a set of tools included in RHEL that provide a way to create and manage virtual block devices known as logical volumes. LVM logical volumes are typically used as the block devices from which RHEL OS filesystems are mounted. The LVM tools support creating and rolling back logical volume snapshots. Automating these actions from an Ansible playbook is relatively simple.

> **Note**
>
> The snapshot and rollback automation capability implemented for our workshop lab environment creates LVM snapshots managed using Ansible roles from the [`infra.lvm_snapshots`](https://github.com/swapdisk/infra.lvm_snapshots#readme) collection.

Logical volumes are contained in a storage pool known as a volume group. The storage available in a volume group comes from one or more physical volumes, that is, block devices underlying actual disks or disk partitions. Typically, the logical volumes where the RHEL OS is installed will be in a "rootvg" volume group. If best practices are followed, applications and app data will be isolated in their own logicial volumes either in the same volume group or a separate volume group, "appvg" for example.

To create logical volume snapshots, there must be free space in the volume group. That is, the total size of the logical volumes in the volume group must be less than the total size of the volume group. The `vgs` command can be used query volume group free space. For example:

```
# vgs
  VG         #PV #LV #SN Attr   VSize  VFree
  VolGroup00   1   7   0 wz--n- 29.53g 9.53g
```

In the example above, the `VolGroup00` volume group total size is 29.53 GiB and there is 9.53 GiB of free space in the volume group. This should be enough free space to support rolling back a RHEL upgrade.

If there is not enough free space in the volume group, there are a few ways we can make space available:

- Adding another physical volume to the volume group (i.e., `pvcreate` and `vgextend`). For a VM, you would first configure an additional virtual disk.
- Temporarily remove a logical volume you don't need. For example, on bare metal servers, there is often a large /var/crash empty filesystem. Removing this filesystem from `/etc/fstab` and then using `lvremove` to remove the logical volume from which it was mounted will free up space in the volume group.
- Reducing the size of one or more logical volumes. This is tricky because first the filesystem in the logical volume needs to be shrunk. XFS filesystems do not support shrinking. EXT filesystems do support shrinking, but not while the filesystem is mounted. Until recently, this way of freeing up volume group space was considered a last resort to be attempted by only the most skilled Linux admin, but it now possible to safely automate shrinking logical volumes using the [`shrink_lv`](https://github.com/swapdisk/infra.lvm_snapshots/tree/main/roles/shrink_lv#readme) role of the aforementioned `infra.lvm_snapshots` collection.

After a snapshot is created, COW data will start to utilize the free space of the snapshot logical volume as blocks are written to the origin logical volume. Unless the snapshot is create with the same size as the origin, there is a chance that the snapshot could fill up and become invalid. Testing should be performed during the development of the LVM snapshot automation to determine snapshot sizings with enough cushion to prevent this. The `snapshot_autoextend_percent` and `snapshot_autoextend_threshold` settings in lvm.conf can also be used to reduce the risk of snapshots running out of space. The [`lvm_snapshots`](https://github.com/swapdisk/infra.lvm_snapshots/tree/main/roles/lvm_snapshots#readme) role of the `infra.lvm_snapshots` collection supports variables that may be used to automatically configure the autoextend settings.

Unless you have the luxury of creating snapshots with the same size as their origin volumes, LVM snapshot sizing needs to be thoroughly tested and free space usage carefully monitored. However, if that challenge can be met, LVM snapshots offer a reliable snapshot solution without the headache of depending on external infrastructure such as VMware.

#### VMware

A VMware snapshot preserves the state and data of a VM at a specific point in time. Because VMware snapshots operate at the hypervisor level, they are completely independent of the guest OS. This makes them foolproof to anything that can go wrong during a RHEL upgrade. Even if an upgrade fails so badly that the OS can't even be booted up again, reverting the VMware snapshot will still save the day. For these reasons, VMware snapshots appear to be a very compelling snapshot option.

VMware snapshots can be manually created and reverted using the vSphere management UI. To create or revert a VMware snapshot automatically from an Ansible playbook, access permissions to the required vSphere API calls must be authorized for the AAP control node.

In our experience, having this access granted can be extremely challenging. The team that controls the VMware environment in most organizations is deeply invested in the "ClickOps" model of doing everything manually using the vSphere management UI. They may also be hesitant to trust that automation developed outside of their team can be trusted to perform the operations they would do manually to create a VMware snapshot, including checking for sufficient free space in the VMFS data store where the snapshot will be created.

The VMware team may resist supporting snapshots because of limited storage space. While standard VMDK files are fixed in size, COW snapshots will grow over time and require careful monitoring with data stores in VMware environments often running tight on capacity.

Another justification for pushing back on supporting automated snapshots will be the VMware vendor recommendation that snapshots should never be used for more than 72 hours (see KB article [Best practices for using VMware snapshots in the vSphere environment](https://kb.vmware.com/s/article/1025279)). Unfortunately, app teams usually need more than 3 days of soak time before they are comfortable that no impact to their apps has resulted from a RHEL upgrade.

VMware snapshots work great when they can be automated. If you are considering this option, engage early with the team that controls the VMware environment for your organization and be prepared for potential resistance.

#### Amazon EBS

Amazon Elastic Block Store (Amazon EBS) provides the block storage volumes used for the virtual disks attached to AWS EC2 instances. When a snapshot is created for an EBS volume, the COW data is written to Amazon S3 object storage.

While EBS snapshots operate independently from the guest OS running on the EC2 instance, the similarity to VMware snapshots ends there. An EBS snapshot saves the data of the source EBS volume, but does not save the state or memory of the EC2 instance to which the volume is attached. Also unlike with VMware, EBS snapshots can be created for an OS volume only while leaving any separate application volumes as is.

Automating EBS snapshot creation and rollback is fairly straightforward assuming your playbooks can access the required AWS APIs. The tricky bit of the automation is identifying the EC2 instance and attached EBS volume that corresponds to the target host in the Ansible inventory managed by AAP, but this can be solved by setting identifying tags on your EC2 instances.

#### Break Mirror

This method is an alternative to LVM that can be used with bare metal servers where the root disk is on a hardware RAID mirror set. Technically speaking, it is not a snapshot, but it still provides a near instantaneous rollback capability.

Instead of creating a snapshot just before starting the upgrade, the automation reconfigures the RAID controller to break the mirror set of the root disk so then it's just two JBOD disks. One of the JBOD disks is used going forward with the upgrade while the other is left untouched. To perform a rollback, the mirror set is reconstructed from the untouched JBOD.

Most bare metal servers support out-of-band management and those manufactured in the last decade will support APIs based on the [Redfish](https://www.dmtf.org/standards/redfish) standard. These APIs can be used by automation to break and reconstruct the mirror set, but be prepared for a significant development and testing effort because the API implementations are not always the same across different vendors and server models.

#### ReaR

ReaR (Relax and Recover) is a backup and recovery tool that is included with RHEL. ReaR doesn't use snapshots, but it does make it very easy to perform a full backup and restore of your RHEL server. When taking a full backup, ReaR creates a bootable ISO image with the current state of the server. To use a ReaR backup to revert an in-place upgrade, we simply boot the server from the ISO image and then choose the "Automatic Recover" option from the menu.

While ReaR backup and recovery is not instantaneous like rolling back a snapshot, it is remarkably fast compared to recovery tools that require you to perform a fresh OS install and then manually recover at a file level.

Read the article [ReaR: Backup and recover your Linux server with confidence](https://www.redhat.com/sysadmin/rear-backup-and-recover) to learn more.

### Step 3 - Snapshot Scope

The best practice for allocating the local storage of a RHEL servers is to configure volumes that separate the OS from the apps and app data. For example, the OS filesystems would be under a "rootvg" volume group while the apps and app data would be in an "appvg" volume group or at least in their own dedicated logical volumes. This separation helps isolate the storage usage requirements of these two groups so they can be manged based on their individual requirements and are less likely to impact each other. For example, the backup profile for the OS is likely different than for the apps and app data.

This practice helps to enforce a key tenet of the RHEL in-place upgrade approach: that is that the OS upgrade should leave the applications untouched with the expectation that system library forward compatibility and middleware runtime abstraction reduces the risk of the RHEL upgrade impacting app functionality.

With these concepts in mind, let's consider if we want to include the apps and app data in what gets rolled back if we need to revert the RHEL upgrade:

| Snapshot scope | Benefits | Drawbacks |
| -------------- | -------- | --------- |
| OS only |<ul><li>Simplifies storage requirements</li><li>Preserves isolation of OS changes from apps and app data</li><li>Reduces risk of rolling back impacting external apps</li></ul>|<ul><li>Probably not possible with VMware snapshots</li><li>Discipline required to avoid temptation of trying quick app changes to fix impacts</li></ul>|
| OS and apps/data |<ul><li>Reduces risk if trying to fix app impact during maintenance window</li><li>Helpful if app impact could lead to app data corruption</li></ul>|<ul><li>More storage space required</li><li>Rolling back app data could impact external systems</li></ul>|

When snapshots only include the upgraded OS volumes, the best practice of isolating OS changes from app changes is followed. In this case, it is important to resist the temptation to make some heroic app changes in an attempt to avoid rolling back in the face of application impact after a RHEL upgrade. For the sake of safety and soundness, gather the evidence required to help understand what caused any app impact, but then do a rollback. Don't make any app changes that could be difficult to untangle after rolling back the OS.

Unfortunately, a VMware snapshot saves the full state of a VM instance including all virtual disks irrespective of whether they contain OS or app data. This can prove challenging for a couple reasons. First, more storage space will be required for the snapshots and it is more difficult to anticipate how much snapshot growth will result because of app data activity. The other problem is that rolling back app data may result in the app state becoming out of sync with external systems leading to unpredictable issues. When rolling back app data for any reason, be aware of the potential headaches that may result.

### Step 4 - Choosing the Best Snapshot Solution

There are a number of factors you should consider when deciding which method of snapshot/rollback will work best in your environment.

- What is your mix of bare metal servers versus VMware or cloud instances?
- Where can free space most readily be made available?
- Can you get unfettered access to your VMware inventory and vSphere APIs?
- What is the appropriate snapshot scope for your organization?
- Which snapshot solution can you most easily make fully automated?

Consider a belt and suspenders approach, that is, offer support for more than one method. Maybe it makes sense to recommend one method for bare metal and another for VMs.

Whatever your decision, remember that an effective snapshot/rollback capability integrated with your end-to-end automation is the most important feature of any RHEL in-place upgrade solution.

## Conclusion

In this exercise, we learned about the pros and cons of a number of different methods of achieving an automated snapshot/rollback capability. We also considered the risks that can happen because of rolling back app data that isn't isolated from OS changes. With this knowledge, you are ready to make more informed decisions when designing your snapshot/rollback automation approach.

In the next exercise, we'll go back to look at how the RHEL in-place upgrades are progressing on our pet application servers.

---

**Navigation**

[Previous Exercise](../2.1-upgrade/README.md) - [Next Exercise](../2.3-check-upg/README.md)

[Home](../README.md)
