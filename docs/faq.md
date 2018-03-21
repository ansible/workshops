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

Solution:
```
pip install boto boto3
```


## Problem: Unable to locate credentials

```
An exception occurred during task execution. To see the full traceback, use -vvv. The error was: NoCredentialsError: Unable to locate credentials
fatal: [localhost]: FAILED! => {"attempts": 1, "changed": false, "msg": "Failed to describe VPCs: Unable to locate credentials"}
```

Solution:
Set your Access Key ID and Secret Access Key under ~/.aws/credentials

```
[root@centos ~]# cat ~/.aws/credentials
[default]
aws_access_key_id = ABCDEFGHIJKLMNOP
aws_secret_access_key = ABCDEFGHIJKLMNOP/ABCDEFGHIJKLMNOP
```

## Problem: Not authorized for image

```
An exception occurred during task execution. To see the full traceback, use -vvv. The error was: ClientError: An error occurred (AuthFailure) when calling the DescribeImageAttribute operation: Not authorized for image:ami-26ebbc5c
```

Solution:
Install latest dev of Ansible (will lock down specific version after 2.5 launches)

```
pip install git+https://github.com/ansible/ansible.git@devel
```

Refer to direction for Ansible Installation: http://docs.ansible.com/ansible/latest/intro_installation.html

## Problem: TASK [connectivity_test : Wait 400 seconds, but only start checking after 30 seconds] ****************************************************

## Problem: no action detected in task

```
fatal: [localhost]: FAILED! => {"reason": "no action detected in task. This often indicates a misspelled module name, or incorrect module path.\n\nThe error appears to have been in '/home/ec2-user/linklight/provisioner/roles/manage_ec2_instances/tasks/provision.yml': line 264, column 3, but may\nbe elsewhere in the file depending on the exact syntax problem.\n\nThe offending line appears to be:\n\n\n- name: find ami for ansible control node\n  ^ here\n\n\nThe error appears to have been in '/home/ec2-user/linklight/provisioner/roles/manage_ec2_instances/tasks/provision.yml': line 264, column 3, but may\nbe elsewhere in the file depending on the exact syntax problem.\n\nThe offending line appears to be:\n\n\n- name: find ami for ansible control node\n  ^ here\n\nexception type: <class 'ansible.errors.AnsibleParserError'>\nexception: no action detected in task. This often indicates a misspelled module name, or incorrect module path.\n\nThe error appears to have been in '/home/ec2-user/linklight/provisioner/roles/manage_ec2_instances/tasks/provision.yml': line 264, column 3, but may\nbe elsewhere in the file depending on the exact syntax problem.\n\nThe offending line appears to be:\n\n\n- name: find ami for ansible control node\n  ^ here\n"}
```

Solution:
Upgrade Ansible, try latest:

```
pip install git+https://github.com/ansible/ansible.git@devel
```
