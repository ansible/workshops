# Ansible AWS training provisioner

The `github.com/ansible/workshops` contains an Ansible Playbook `provision_lab.yml`, which is an automated lab setup for Ansible training on AWS (Amazon Web Services).  Set the `workshop_type` variable below to provision the corresponding workshop.

| Workshop | Workshop Type Var   |
|---|---|
| Ansible Red Hat Enterprise Linux Workshop | `workshop_type: rhel`  |
| Ansible Network Automation Workshop | `workshop_type: networking`  |
| Ansible F5 Workshop | `workshop_type: f5`   |
| Ansible Security Automation | `workshop_type: security`   |
| Ansible Windows Automation  | `workshop_type: windows`    |

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

#####OPTIONAL VARIABLES

# turn DNS on for control nodes, and set to type in valid_dns_type
dns_type: aws

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
```

If you want to license it you must copy a license called tower_license.json into this directory.  If you do not have a license already please request one using the [Workshop License Link](https://www.ansible.com/workshop-license).

For more extra_vars examples, look at the following:
- [sample-vars-rhel.yml](sample_workshops/sample-vars-rhel.yml) - example for the Ansible RHEL Workshop
- [sample-vars-windows.yml](sample_workshops/sample-vars-windows.yml) - example for the **Ansible Windows Workshop**
- [sample-vars-networking.yml](sample_workshops/sample-vars-networking.yml) - example for the **Ansible Network Workshop**
- [sample-vars-f5.yml](sample_workshops/sample-vars-f5.yml) - example for **Ansible F5 Workshop**
- [sample-vars-tower-auto.yml](sample_workshops/sample-vars-tower-auto.yml) - example for Tower installation and licensing

2. Run the playbook:

        ansible-playbook provision_lab.yml -e @extra_vars.yml

3. Login to the AWS EC2 console and you will see instances being created.  For example:

        `tesworkshop-student1-ansible`

## Accessing student documentation and slides

  - Exercises and instructor slides are hosted at [http://ansible.github.io/workshops](http://ansible.github.io/workshops)

  - Workbench information is stored in two places after you provision:
    1. in a local directory named after the workshop (e.g. testworkshop/instructor_inventory)

    2. if `create_login_page: true` is enabled in your `extra_vars file,` there will be a website `ec2_name_prefix.workshop_dns_zone` (e.g. `testworkshop.rhdemo.io`)

       - **NOTE:** It is possible to change the DNS domain (right now this is only supported via a AWS Route 53 Hosted Zone) using the parameter `workshop_dns_zone` in your `extra_vars.yml` file.

       - **NOTE:** The playbook does not create the route53 zone and must exist prior to running the playbook.

## DNS

The provisioner currently supports creating DNS records per control node with valid SSL certs using [Lets Encrypt](https://letsencrypt.org/).  Right now DNS is only supported via AWS Route 53, however we are building it in a way that this can be more pluggable and take advantage of other public clouds.

This means that each student workbench will get an individual DNS entry.  For example a DNS name will look like this: `https://student1.testworkshop.rhdemo.io`

  - **NOTE:** The variable `dns_type` defaults to `aws`.  This can also be set to `dns_type: none`.  

  - **NOTE:**  If Lets Encrypt fails, the workshop provisioner will still pass, and alert you of errors in the `summary_information` at the end of the `provision_lab.yml` Ansible Playbook.

# Lab Teardown

The `teardown_lab.yml` playbook deletes all the training instances as well as local inventory files.

To destroy all the EC2 instances after training is complete:

1. Run the playbook:

        ansible-playbook teardown_lab.yml -e @extra_vars.yml

2. Optionally you can enable verbose debug output of the information gathered
   that drives the teardown process by passing the extra optional variable
   `debug_teardown=true`. Example:

        ansible-playbook teardown_lab.yml -e @extra_vars.yml -e debug_teardown=true

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
