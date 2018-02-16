# Ansible AWS training provisioner
**aws_lab_setup** is an automated lab setup for Ansible training on AWS (Amazon Web Services).  There are currently two modes:
 - Ansible Essentials mode (default)
 - Ansible Networking mode

## Ansible Essentials Mode
The default mode provisions four nodes per user:
* One control node from which Ansible will be executed from and where Ansible Tower can be installed (named ansible)
* Three web nodes that coincide with the three nodes in lightbulb's original design
* And one node where `haproxy` is installed (via lightbulb lesson)

## Ansible Networking Mode
This provisions the [Ansible Lightbulb - Networking Workshop](../../workshops/networking).  

This mode builds a four node workshop demonstrating Ansible’s capabilities on network equipment (e.g. Cisco Systems IOS):
* One control node from which Ansible will be executed from and where Ansible Tower can be installed (named `ansible`)
* Two network nodes (`rtr1` and `rtr2`).
* One host node named `host1`

The `ansible` node and `rtr1` are in one VPC.  The `host1` node and `rtr2` are in another VPC.  More details of the setup including a diagram can be found on the [networking workshop page](../../workshops/networking).

To enable networking mode edit the vars file and add:
```
networking: true
```

Use the samples-vars-networking.yml as an example.  [Quick instructions for networking mode can be found here](network_quick_instructions.md).

# Table Of Contents
- [Requirements](#requirements)
- [AWS Setup](#aws-setup)
  - [Email Options](#email-options)
  - [Lab Setup](#lab-setup)
    - [One Time Setup](#one-time-setup)
    - [Setup (per workshop)](#setup-per-workshop)
  - [Accessing student documentation and slides](#Accessing-student-documentation-and-slides)
- [AWS Teardown](#aws-teardown)

# Requirements

This provisioner  must be run with Ansible Engine v2.4.2 or higher.


# AWS Setup
The `provision_lab.yml` playbook creates instances, configures them for password authentication, creates an inventory file for each user with their IPs and credentials. An instructor inventory file is also created in the current directory which will let the instructor access the nodes of any student by simply targeting the username as a host group. The lab is created in `us-east-1` by default.  Currently only works with `us-east-1`, `us-west-1`, `eu-west-1`, `ap-southeast-1`, `ap-southeast-2`, `ap-south-1` and `ap-northeast-1`.


## Email Options
This provisioner by default will send email to participants/students containing information about their lab environment including IPs and credentials. This configuration requires that each participant register for the workshop using their full name and email address.   Alternatively, you can use generic accounts for workshops.  This method offers the advantage of enabling the facilitator to handle "walk-ins" and is a simpler method overall in terms of collecting participant information.

Steps included in this guide will be tagged with __(email)__ to denote it as a step required if you want to use email and __(no email)__ for steps you should follow if you chose not to use email   

**WARNING** Emails are sent _every_ time the playbook is run. To prevent emails from being sent on subsequent runs of the playbook, add `email: no` to `extra_vars.yml`.

## Lab Setup
To provision the workshop onto AWS use the following directions:

### One Time Setup

1. Create an Amazon AWS account.

2. Create an Access Key ID and Secret Access Key.  Save the ID and key for later.

  - New to AWS and not sure what this step means?  [Click here](aws-directions/AWSHELP.md)

3. Install `boto` and `boto3`.

        pip install boto boto3

4. Create an [Access Key ID and Secret Access Key](http://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) (you should be using IAM and [not your AWS account directly](http://docs.aws.amazon.com/general/latest/gr/managing-aws-access-keys.html)).  Save the ID and key for later.

5. Install the `passlib` library

        pip install passlib

6. Clone the lightbulb repo:

If you haven't done so already make sure you have the repo cloned to the machine executing the playbook

        git clone https://github.com/ansible/lightbulb.git
        cd lightbulb/tools/aws_lab_setup

#### Step 7-8 are optional
These steps are only needed if you are using the email feature

7. __(email)__ Create a free [Sendgrid](http://sendgrid.com) account if you don't have one. Optionally, create an API key to use with this the playbook.

8. __(email)__ Install the `sendgrid` python library:

    **Note:** The `sendgrid` module does not work with `sendgrid >= 3`. Please install the latest `2.x` version.

        pip install sendgrid==2.2.1

### Setup (per workshop)

1. Define the following variables in a file passed in using `-e @extra_vars.yml`

```yml
ec2_key_name: username                # SSH key in AWS to put in all the instances
ec2_region: us-east-1                 # region where the nodes will live
ec2_az: us-east-1a                    # availability zone
ec2_name_prefix: TRAINING-LAB         # name prefix for all the VMs
admin_password: ansible
## Optional Variables
email: no                             # Set this if you wish to disable email
localsecurity: false                   # skips firewalld installation and SE Linux when turned to false
```

For an example, look at [sample-vars.yml](sample-vars.yml) for a list of all the knobs you can control.  You can use pre-existing AWS VPCs you already created.

2. Create a `users.yml` by copying `sample-users.yml` and adding all your students:

For a users example, look at [sample-users.yml](sample-users.yml)
    **email**
```yml
users:
  - name: Bod Barker
    username: bbarker
    email: bbarker@acme.com

  - name: Jane Smith
    username: jsmith
    email: jsmith@acme.com
```

**no email**
```yml
users:
  - name: Student01
    username: student01
    email: instructor@acme.com

  - name: Student02
    username: student02
    email: instructor@acme.com
```
- **no email** NOTE:  If using generic users, you can generate the corresponding
`users.yml` file from the command line by creating a 'STUDENTS' variable
containing the number of "environments" you want, and then populating the file.
For example:

```bash
STUDENTS=30;
echo "users:" > users.yml &&
for NUM in $(seq -f "%02g" 1 $STUDENTS); do
  echo "  - name: Student${NUM}" >> users.yml
  echo "    username: student${NUM}" >> users.yml
  echo "    email: instructor@acme.com" >> users.yml
  echo >> users.yml
done
```

The [script is attached for your convenience](make_users.sh)

3. Run the playbook:

        ansible-playbook provision_lab.yml -e @extra_vars.yml -e @users.yml

What does the provisioner take care of automatically?
- AWS VPC creation (Amazon WebServices Virtual Private Cloud)
- Creation of an SSH key pair (stored at ./ansible.pem)
  - This private key is installed automatically
- Creation of a AWS EC2 security group
- Creation of a subnet for the VPC
- Creation of an internet gateway for the VPC
- Creation of route table for VPC (for reachability from internet)

4. Check on the EC2 console and you should see instances being created like:

        TRAINING-LAB-<student_username>-node1|2|3|haproxy|tower|control

**email** If successful all your students will be emailed the details of their hosts including addresses and credentials, and an `instructor_inventory.txt` file will be created listing all the student machines.

**no email** If you disabled email in your `extra_vars.yml` file, you will need to upload the instructor's inventory to a public URL which you will hand out to participants.  
1. Use [github gist](https://gist.github.com/) to upload `lightbulb/tools/aws_lab_setup/instructors_inventory`.
2. Use http://goo.gl to shorten the URL to make it more consumable

## Accessing student documentation and slides

  * A student guide and instructor slides are already hosted at http://ansible-workshop.redhatgov.io . (NOTE:  This guide is evolving and newer workshops can be previewed at http://ansible.redhatgov.io . This new version is currently being integrated with the Lightbulb project)
  * Here you will find student instructions broken down into exercises as well as the presentation decks under the __Additional Resources__ drop down.
  * During the workshop, it is recommended that you have a second device or printed copy of the student guide.  Previous workshops have demonstrated that unless you've memorized all of it, you'll likely need to refer to the guide, but your laptop will be projecting the slide decks.  Some students will fall behind and you'll need to refer back to other exercises/slides without having to change the projection for the entire class.

# AWS Teardown

The `teardown_lab.yml` playbook deletes all the training instances as well as local inventory files.

To destroy all the EC2 instances after training is complete:

1. Run the playbook:

        ansible-playbook teardown_lab.yml -e @extra_vars.yml -e @users.yml
