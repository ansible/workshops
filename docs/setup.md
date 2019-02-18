# One Time Setup

1. Create an Amazon AWS account.

2. Create an Access Key ID and Secret Access Key.  Save the ID and key for later.

  - New to AWS and not sure what this step means?  [Click here](aws-directions/AWSHELP.md)

3. Install `boto` and `boto3`as well as `netaddr`

        pip install boto boto3 netaddr

  **Are you using Tower?**  [Tower Instructions](#tower-instructions)

4. Set your Access Key ID and Secret Access Key from Step 2 under ~/.aws/credentials

```
[root@centos ~]# cat ~/.aws/credentials
[default]
aws_access_key_id = ABCDEFGHIJKLMNOP
aws_secret_access_key = ABCDEFGHIJKLMNOP/ABCDEFGHIJKLMNOP
```

5. Install the `passlib` library and `netaddr`

        pip install passlib netaddr

6. Clone the linklight repo:

If you haven't done so already make sure you have the repo cloned to the machine executing the playbook

        git clone https://github.com/network-automation/linklight.git
        cd linklight/provisioner

7.  When doing a networking or F5 workshop make sure you have subscribed to the right marketplace AMI (Amazon Machine Image)

  - For Networking you will need the Cisco CSR (Cloud Services Router) [Click here](https://aws.amazon.com/marketplace/pp/B00NF48FI2/)
  - For F5 you will need the F5 BIG-IP [Click here](https://aws.amazon.com/marketplace/pp/B079C44MFH/)

# Tower Instructions
Are you using Red Hat Ansible Tower?  Make sure to use umask for the installation of boto3 on the control node.
https://docs.ansible.com/ansible-tower/latest/html/upgrade-migration-guide/virtualenv.html

```
[user@centos ~]$ sudo -i
[root@centos ~]# source /var/lib/awx/venv/ansible/bin/activate
[root@centos ~]# umask 0022
[root@centos ~]# pip install --upgrade boto3
[root@centos ~]# deactivate
```

# More info on what is happening

The `provision_lab.yml` playbook creates a work bench for each student, configures them for password authentication, and creates an inventory file for each user with their IPs and credentials. An instructor inventory file is also created in the current directory which will let the instructor access the nodes of any student.  This file will be called `instructor_inventory.txt`

What does the AWS provisioner take care of automatically?
- AWS VPC creation (Amazon WebServices Virtual Private Cloud)
- Creation of an SSH key pair (stored at ./WORKSHOPNAME/WORKSHOPNAME-private.pem)
- Creation of a AWS EC2 security group
- Creation of a subnet for the VPC
- Creation of an internet gateway for the VPC
- Creation of route table for VPC (for reachability from internet)

# Webpage creation

If you used `create_login_page: true` above you will also get a webpage created for students.

The webpage will be generated as {{ec2_name_prefix}}.rhdemo.io
in the example above this literally means http://testworkshop.rhdemo.io

It is possible to change the route53 DNS as well using the parameter `workshop_dns_zone` in your `extra_vars.yml` file.

This playbook does not create the route53 zone and must exist prior to running the playbook.

# Remote Desktop

If you used `xrdp: true` you will the ability to remote desktop to the control node.

The provisioner has the ability to install [xrdp](http://www.xrdp.org/) with [xfce](https://xfce.org/) for graphical interface. The xrdp application is a an open source remote desktop protocol(rdp) server. Xfce is a lightweight desktop environment for UNIX-like operating systems. It aims to be fast and low on system resources, while still being visually appealing and user friendly.
