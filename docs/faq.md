# FAQ for the Provisioner
Frequently Asked Questions... or rather common problems that people have hit.

## How do I do a release PR?

Read this [guide](release.md)

## Problem: boto3 missing

```
fatal: [localhost]: FAILED! => {"attempts": 1, "changed": false, "msg": "Python modules \"botocore\" or \"boto3\" are missing, please install both"}
```

OR

```
fatal: [localhost]: FAILED! => {"attempts": 1, "changed": false, "msg": "boto is required for this module"}
```

### Solution:

```
pip install boto boto3
```


## Problem: Unable to locate credentials

```
An exception occurred during task execution. To see the full traceback, use -vvv. The error was: NoCredentialsError: Unable to locate credentials
fatal: [localhost]: FAILED! => {"attempts": 1, "changed": false, "msg": "Failed to describe VPCs: Unable to locate credentials"}
```

### Solution:

Set your Access Key ID and Secret Access Key under ~/.aws/credentials

```
[root@centos ~]# cat ~/.aws/credentials
[default]
aws_access_key_id = ABCDEFGHIJKLMNOP
aws_secret_access_key = ABCDEFGHIJKLMNOP/ABCDEFGHIJKLMNOP
```

## Problem: wrong version of Ansible

```
TASK [make sure we are running correct Ansible Version] ********************************
fatal: [localhost]: FAILED! => {
    "assertion": "ansible_version.minor >= 6",
    "changed": false,
    "evaluated_to": false
}
```
### Solution
Install 2.6 or later.  For Tower make sure to use an RPM.  You can download a nightly here: https://releases.ansible.com/ansible/rpm/nightly/devel/epel-7-x86_64/

## Problem: Wrong version of boto3
```
make sure we are running correct boto version
py_cmd.stdout.startswith('1.7')
```

### Solution

Install and/or upgrade boto3
```
pip install boto3 --upgrade
```

Are you using Tower?  Make sure to use umask
https://docs.ansible.com/ansible-tower/latest/html/upgrade-migration-guide/virtualenv.html

```
[user@centos ~]$ sudo -i
[root@centos ~]# source /var/lib/awx/venv/ansible/bin/activate
[root@centos ~]# umask 0022
[root@centos ~]# pip install --upgrade boto3
[root@centos ~]# deactivate
```

## Problem: AWS Signature Failure
```
    "error": {
        "message": "Signature expired: 20180703T083815Z is now earlier than 20180703T152801Z (20180703T154301Z - 15 min.)",
        "code": "SignatureDoesNotMatch",
        "type": "Sender"
```

### Solution

Ensure the time on your Ansile Tower or Ansible Engine Server is correct.

## Problem: Generic Tower Issue

There is some issue that does not happen on the command line, but manifests itself via the Ansible Tower Web GUI.

### Solution

Red Hat Ansible Tower executes Ansible playbooks via the awx user.  SSH to the control node and become the awx user->

```
[user@centos ~]$ sudo su - awx
-bash-4.2$
```

Ansible Tower also takes advantage of a Python virtual environment (referred to as a virtualenv).  To mimic how Red Hat Ansible Tower executes playbooks you also must set the virtualenv

```
-bash-4.2$ source /var/lib/awx/venv/ansible/bin/activate
(ansible) -bash-4.2$
```

Ansible Tower stores job templates under the projects folder in the awx home directory, located at `/var/lib/awx/projects`

```
(ansible) -bash-4.2$ ls /var/lib/awx/projects
```

cd into the relevant project folder and execute the Playbook from the command line to run the playbook exactly how it was run from Ansible Tower.  This will hopefully let you see an error or problem you were not aware of via the Tower GUI.

## Problem: Creating EC2 instances fail with an "OptInRequired" message

```
TASK [manage_ec2_instances : Create EC2 instances for rtr3 node (NETWORKING MODE)] ***
fatal: [localhost]: FAILED! => changed=false
  msg: 'Instance creation failed => OptInRequired: In order to use this AWS Marketplace product you need to accept terms and subscribe. To do so please visit https://aws.amazon.com/marketplace/pp?sku=bw54e0gl17zf0vxq54dttwvow'

```
### Solution:

This is likely if you are using the device (CSR/F5/vMX) for the first time in AWS. You will need to follow the link in the error output and accept the Terms and Conditions in order to proceed. Once you accept, re-run the provisioner.


## Problem: F5 Workshop provisioner fails on mac

```
TASK [f5_setup : Install AS3] *******************************************************************************
fatal: [TESTWORKSHOP-student1-f5]: FAILED! => {"changed": false, "cmd": "rpm -qp --queryformat '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}' <ommited>/workshops/provisioner/roles/f5_setup/files/f5-appsvcs-3.4.0-2.noarch.rpm", "msg": "[Errno 2] No such file or directory", "rc": 2}
```

### Solution:

```
$ brew install rpm
```

## Problem: Windows workshop: MacOS breaking on a fork

```TASK [Gathering Facts] **********************************************
objc[43678]: +[__NSPlaceholderDate initialize] may have been in progress in another thread when fork() was called. We cannot safely call it or ignore it in the fork() child process. Crashing instead. Set a breakpoint on objc_initializeAfterForkError to debug.
```

### Solution:

```
$ export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```
