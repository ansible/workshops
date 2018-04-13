# Ansible AWS training provisioner
**aws_lab_setup** is an automated lab setup for Ansible training on AWS (Amazon Web Services).  There are currently two modes:
 - Ansible Engine mode (default)
 - Ansible Networking mode

## Ansible Essentials Mode
The default mode provisions four nodes per user:
* One control node from which Ansible will be executed from and where Ansible Tower can be installed (named `ansible`)
* Three web nodes that coincide with the three nodes in lightbulb's original design

## Ansible Networking Mode
This provisions the [Ansible Linklight - Networking Workshop](../exercises/networking).  

This mode builds a four node workshop demonstrating Ansible’s capabilities on network equipment (e.g. Cisco Systems IOS):
* One control node from which Ansible will be executed from and where Ansible Tower can be installed (named `ansible`)
* Two network nodes (`rtr1` and `rtr2`).
* One host node named `host1`

To enable networking mode edit the vars file and add:
```
networking: true
```
### More Info on Networking Mode

- Use the [samples-vars-networking.yml](samples-vars-networking.yml) as an example.  
- [Quick instructions for networking mode can be found here](network_quick_instructions.md).

# Table Of Contents
- [Requirements](#requirements)
- [AWS Setup](#aws-setup)
  - [Lab Setup](#lab-setup)
    - [One Time Setup](#one-time-setup)
    - [Setup (per workshop)](#setup-per-workshop)
  - [Accessing student documentation and slides](#Accessing-student-documentation-and-slides)
- [AWS Teardown](#aws-teardown)
- [FAQ](../docs/faq.md)

# Requirements

This provisioner  must be run with Ansible Engine v2.5.0 or higher.

# AWS Setup
The `provision_lab.yml` playbook creates a work bench for each student, configures them for password authentication, and creates an inventory file for each user with their IPs and credentials. An instructor inventory file is also created in the current directory which will let the instructor access the nodes of any student.  This file will be called `instructor_inventory.txt`

## Lab Setup
To provision the workshop onto AWS use the following directions:

### One Time Setup

1. Create an Amazon AWS account.

2. Create an Access Key ID and Secret Access Key.  Save the ID and key for later.

  - New to AWS and not sure what this step means?  [Click here](aws-directions/AWSHELP.md)

3. Install `boto` and `boto3`.

        pip install boto boto3

4. Set your Access Key ID and Secret Access Key from Step 2 under ~/.aws/credentials

```
[root@centos ~]# cat ~/.aws/credentials
[default]
aws_access_key_id = ABCDEFGHIJKLMNOP
aws_secret_access_key = ABCDEFGHIJKLMNOP/ABCDEFGHIJKLMNOP
```

5. Install the `passlib` library

        pip install passlib

6. Clone the linklight repo:

If you haven't done so already make sure you have the repo cloned to the machine executing the playbook

        git clone https://github.com/network-automation/linklight.git
        cd linklight/provisioner

### Setup (per workshop)

1. Define the following variables in a file passed in using `-e @extra_vars.yml`

```yml
ec2_region: us-east-1                 # region where the nodes will live
ec2_az: us-east-1a                    # availability zone
ec2_name_prefix: TRAININGLAB          # name prefix for all the VMs
admin_password: ansible
## Optional Variables
localsecurity: false                   # skips firewalld installation and SE Linux when false
```

There is also option to install Ansible Tower to the control node, and an option to license it.  If you want to license it you must copy a license called tower_license.json into this directory.

```
autolicense: true
towerinstall: true
```

For an example, look at the following:
- [sample-vars.yml](sample-vars.yml)
- [sample-vars.yml](sample-vars-networking.yml)
- [sample-vars-auto.yml](sample-vars-auto.yml)

2. Run the playbook:

        ansible-playbook provision_lab.yml -e @extra_vars.yml

What does the provisioner take care of automatically?
- AWS VPC creation (Amazon WebServices Virtual Private Cloud)
- Creation of an SSH key pair (stored at ./ansible.pem)
  - This private key is installed automatically
- Creation of a AWS EC2 security group
- Creation of a subnet for the VPC
- Creation of an internet gateway for the VPC
- Creation of route table for VPC (for reachability from internet)

4. Check on the EC2 console and you should see instances being created like:

        TRAININGLAB-student1-node1|2|3|ansible

## Accessing student documentation and slides

  * A exercises and instructor slides are already hosted at http://ansible.com/linklight

# AWS Teardown

The `teardown_lab.yml` playbook deletes all the training instances as well as local inventory files.

To destroy all the EC2 instances after training is complete:

1. Run the playbook:

        ansible-playbook teardown_lab.yml -e @extra_vars.yml -e @users.yml

# FAQ
For frequently asked questions see the [FAQ](../docs/faq.md)
