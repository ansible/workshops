# FAQ for the Provisioner
Frequently Asked Questions... or rather common problems that people have hit.

### Problem: boto3 missing

```
fatal: [localhost]: FAILED! => {"attempts": 1, "changed": false, "msg": "Python modules \"botocore\" or \"boto3\" are missing, please install both"}
```

OR

```
fatal: [localhost]: FAILED! => {"attempts": 1, "changed": false, "msg": "boto is required for this module"}
```

#### Solution:

```
pip install boto boto3
```


### Problem: Unable to locate credentials

```
An exception occurred during task execution. To see the full traceback, use -vvv. The error was: NoCredentialsError: Unable to locate credentials
fatal: [localhost]: FAILED! => {"attempts": 1, "changed": false, "msg": "Failed to describe VPCs: Unable to locate credentials"}
```

#### Solution:

Set your Access Key ID and Secret Access Key under ~/.aws/credentials

```
[root@centos ~]# cat ~/.aws/credentials
[default]
aws_access_key_id = ABCDEFGHIJKLMNOP
aws_secret_access_key = ABCDEFGHIJKLMNOP/ABCDEFGHIJKLMNOP
```

<aside class="warning">
NOTE: boto3 (the AWS python library) doesn't properly handle AwS environment variables and will generate a fairly opaque parsing error. Stick with the credentials file shown above or something similar. The error is something like:
</aside>
```
caught_exception\nValueError: Invalid header value 'AWS4-HMAC-SHA256 ...
```
