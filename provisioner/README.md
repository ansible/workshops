# Ansible AWS training provisioner
**aws_lab_setup** is an automated lab setup for Ansible training on AWS (Amazon Web Services).  There are currently two modes:
 - Ansible Engine Workshop (default)
 - Ansible Networking Workshop

## Ansible Engine Workshop
This provisions the [Ansible Engine Workshop](../exercises/ansible_engine).

The default mode provisions four nodes per user:
* One control node from which Ansible will be executed from and where Ansible Tower can be installed (named `ansible`)
* Three web nodes that coincide with the three nodes in lightbulb's original design

## Ansible Networking Workshop
This provisions the [Ansible Networking Workshop](../exercises/networking).  

This mode builds a four node workshop demonstrating Ansible’s capabilities on network equipment (e.g. Cisco Systems IOS):
* One control node from which Ansible will be executed from and where Ansible Tower can be installed (named `ansible`)
* Two network nodes (`rtr1` and `rtr2`).
* One host node named `host1`

To enable networking mode edit the vars file and add:

```
networking: true
```

- [Quick instructions for networking mode can be found here](../docs/network_quick_instructions.md).

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

This provisioner  must be run with Ansible Engine v2.6.0 or higher.

**NOTE** For more information on this requirement please read: https://github.com/network-automation/linklight/issues/21

# AWS Setup

The `provision_lab.yml` playbook creates a work bench for each student, configures them for password authentication, and creates an inventory file for each user with their IPs and credentials. An instructor inventory file is also created in the current directory which will let the instructor access the nodes of any student.  This file will be called `instructor_inventory.txt`

## Lab Setup

To provision the workshop onto AWS use the following directions:

### One Time Setup

1. Create an Amazon AWS account.

2. Create an Access Key ID and Secret Access Key.  Save the ID and key for later.

  - New to AWS and not sure what this step means?  [Click here](../docs/aws-directions/AWSHELP.md)

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

7.  When doing a networking or F5 workshop make sure you have subscribed to the right marketplace AMI (Amazon Machine Image)

  - For Networking you will need the Cisco CSR (Cloud Services Router) [Click here](https://aws.amazon.com/marketplace/pp/B00NF48FI2/)
  - For F5 you will need the F5 BIG-IP [Click here](https://aws.amazon.com/marketplace/pp/B079C44MFH/)

### Setup (per workshop)

1. Define the following variables in a file passed in using `-e @extra_vars.yml`

```
---
ec2_region: us-east-1                  # region where the nodes will live
ec2_name_prefix: TESTWORKSHOP          # name prefix for all the VMs
student_total: 2                       # creates student_total of workbenches for the workshop
#OPTIONAL VARIABLES
admin_password: ansible                # password for Ansible control node, defaults to ansible
networking: true                       # Set this if you want the workshop in networking mode
create_login_page: true
towerinstall: true                     # automatically installs Tower to control node
# autolicense: true                    # automatically licenses Tower if license is provided
```

If you want to license it you must copy a license called tower_license.json into this directory.  If you do not have a license already please request one using the [Workshop License Link](https://www.ansible.com/workshop-license).

For a list of AWS availability zones please [refer to the documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html).


For more examples, look at the following:
- [sample-vars.yml](sample-vars.yml) - example for the Ansible Engine Workshop
- [sample-vars.yml](sample-vars-networking.yml) - example for the Ansible Network Workshop
- [sample-vars-auto.yml](sample-vars-auto.yml) - example for Tower installation and licensing

2. Run the playbook:

        ansible-playbook provision_lab.yml -e @extra_vars.yml

What does the AWS provisioner take care of automatically?
- AWS VPC creation (Amazon WebServices Virtual Private Cloud)
- Creation of an SSH key pair (stored at ./WORKSHOPNAME/WORKSHOPNAME-private.pem)
- Creation of a AWS EC2 security group
- Creation of a subnet for the VPC
- Creation of an internet gateway for the VPC
- Creation of route table for VPC (for reachability from internet)

3. Check on the EC2 console and you should see instances being created like:

        TESTWORKSHOP-student1-node1|2|3|ansible

## Accessing student documentation and slides

  * A exercises and instructor slides are already hosted at http://ansible.com/linklight

# AWS Teardown

The `teardown_lab.yml` playbook deletes all the training instances as well as local inventory files.

To destroy all the EC2 instances after training is complete:

1. Run the playbook:

        ansible-playbook teardown_lab.yml -e @extra_vars.yml

# FAQ
For frequently asked questions see the [FAQ](../docs/faq.md)
