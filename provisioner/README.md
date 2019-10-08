# Ansible AWS training provisioner

The `github.com/ansible/workshops` contains a provisioner `provision_lab.yml`, which is an automated lab setup for Ansible training on AWS (Amazon Web Services).  Set the `workshop_type` variable below to provision the corresponding workshop.

| Workshop   | Deck  | Exercises  | Workshop Type Var   |
|---|---|---|---|
| Ansible Red Hat Enterprise Linux Workshop  | [Deck](https://ansible.github.io/workshops/decks/ansible_rhel.pdf)  | [Exercises](../exercises/ansible_rhel) | `workshop_type: rhel`  |
| Ansible Network Automation Workshop  | [Deck](https://ansible.github.io/workshops/decks/ansible_network.pdf) | [Exercises](../exercises/ansible_network)  | `workshop_type: networking`  |
| Ansible F5 Workshop | [Deck](https://ansible.github.io/workshops/decks/ansible_f5.pdf) | [Exercises](../exercises/ansible_f5)   | `workshop_type: f5`   |

# Table Of Contents
- [Requirements](#requirements)
- [Lab Setup](#lab-setup)
  - [One Time Setup](#one-time-setup)
  - [Setup (per workshop)](#setup-per-workshop)
  - [Accessing student documentation and slides](#Accessing-student-documentation-and-slides)
- [Lab Teardown](#aws-teardown)
- [FAQ](../docs/faq.md)
- [More info on what is happening](#more-info-on-what-is-happening)
- [Remote Desktop](#remote-desktop)
- [Getting Help](#getting-help)

# Requirements
- This provisioner must be run with Ansible Engine v2.8.0 or higher.
- AWS Account (follow directions on one time setup below)

# Lab Setup

## One Time Setup
[For One Time Setup - click here](../docs/setup.md)

## Setup (per workshop)

1. Define the following variables in a file passed in using `-e @extra_vars.yml`

```
---
# region where the nodes will live
ec2_region: us-east-1
# name prefix for all the VMs
ec2_name_prefix: TESTWORKSHOP
# creates student_total of workbenches for the workshop
student_total: 2
# Set the right workshop type, like networking, rhel or f5 (see above)
workshop_type: rhel
#OPTIONAL VARIABLES
# password for Ansible control node, defaults to ansible
admin_password: ansible
# creates AWS S3 website for ec2_name_prefix.workshop_dns_zone
create_login_page: true                
# Sets the Route53 DNS zone to use for the S3 website
workshop_dns_zone: rhdemo.io           
# automatically installs Tower to control node
towerinstall: true                     
# automatically licenses Tower if license is provided
autolicense: true
# install xrdp with xfce for graphical interface
#xrdp: true
```

If you want to license it you must copy a license called tower_license.json into this directory.  If you do not have a license already please request one using the [Workshop License Link](https://www.ansible.com/workshop-license).

For more extra_vars examples, look at the following:
- [sample-vars-rhel.yml](sample_workshops/sample-vars-rhel.yml) - example for the Ansible RHEL Workshop
- [sample-vars-networking.yml](sample_workshops/sample-vars-networking.yml) - example for the **Ansible Network Workshop**
- [sample-vars-f5.yml](sample_workshops/sample-vars-f5.yml) - example for **Ansible F5 Workshop**
- [sample-vars-tower-auto.yml](sample_workshops/sample-vars-tower-auto.yml) - example for Tower installation and licensing

2. Run the playbook:

        ansible-playbook provision_lab.yml -e @extra_vars.yml

3. Login to the EC2 console and you should see instances being created like:

        `TESTWORKSHOP-student1-ansible`

## Accessing student documentation and slides

  - Exercises and instructor slides are hosted at http://ansible.github.io/workshops
  - Workbench information is stored in two places after you provision:
    - in a local directory named after the workshop (e.g. TESTWORKSHOP/instructor_inventory)
    - if `create_login_page: true` is enabled in your `extra_vars file,` there will be a website ec2_name_prefix.workshop_dns_zone (e.g. TESTWORKSHOP.rhdemo.io)
    - It is possible to change the route53 DNS as well using the parameter `workshop_dns_zone` in your `extra_vars.yml` file.
    - The playbook does not create the route53 zone and must exist prior to running the playbook.

# Lab Teardown

The `teardown_lab.yml` playbook deletes all the training instances as well as local inventory files.

To destroy all the EC2 instances after training is complete:

1. Run the playbook:

        ansible-playbook teardown_lab.yml -e @extra_vars.yml

# FAQ

For frequently asked questions see the [FAQ](../docs/faq.md)

# More info on what is happening

The `provision_lab.yml` playbook creates a work bench for each student, configures them for password authentication, and creates an inventory file for each user with their IPs and credentials. An instructor inventory file is also created in the current directory which will let the instructor access the nodes of any student.  This file will be called `instructor_inventory.txt`

What does the AWS provisioner take care of automatically?
- AWS VPC creation (Amazon WebServices Virtual Private Cloud)
- Creation of an SSH key pair (stored at ./WORKSHOPNAME/WORKSHOPNAME-private.pem)
- Creation of a AWS EC2 security group
- Creation of a subnet for the VPC
- Creation of an internet gateway for the VPC
- Creation of route table for VPC (for reachability from internet)

# Remote Desktop

If you used `xrdp: true` you will the ability to remote desktop to the control node.

The provisioner has the ability to install [xrdp](http://www.xrdp.org/) with [xfce](https://xfce.org/) for graphical interface. The xrdp application is a an open source remote desktop protocol(rdp) server. Xfce is a lightweight desktop environment for UNIX-like operating systems. It aims to be fast and low on system resources, while still being visually appealing and user friendly.

# Getting Help

Please file issues on Github.  Please fill out all required information.  Your issue will be closed if there if you skip required information in the Github issues template.
