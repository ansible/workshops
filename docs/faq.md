# FAQ for the Provisioner
Frequently Asked Questions... or rather common problems that people have hit.

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
