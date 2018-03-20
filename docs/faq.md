# FAQ
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
