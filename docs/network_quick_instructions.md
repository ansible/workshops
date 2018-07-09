# Quick Instructions for Ansible Linklight - Networking

## Clone Network-Automation Linklight

```bash
git clone https://github.com/network-automation/linklight
```

## Move into aws_lab_setup directory

```bash
cd provisioner/
```

## Create Vars File
Create a workshop vars file.  You can literally just do a `cp` from the `provisioner/` directory
```
cp sample-vars-networking.yml my_workshop.yml
```

```yml
---
ec2_region: us-east-1                  # region where the nodes will live
ec2_name_prefix: TESTWORKSHOP          # name prefix for all the VMs
student_total: 2                       # creates student_total of workbenches for the workshop
#OPTIONAL VARIABLES
admin_password: ansible                # password for Ansible control node, defaults to ansible
networking: true                       # Set this if you want the workshop in networking mode
localsecurity: false                   # skips firewalld installation and SE Linux when false
create_login_page: true
towerinstall: true                     # automatically installs Tower to control node
# autolicense: true                    # automatically licenses Tower if license is provided
```

The two most important variables above that probably need modifying are
- `ec2_name_prefix` this name doesn't matter, just name it something you will remember (or use the date)
- `student_total` this is the total amount of students the workshop will create.  

## Run the provision playbook

```bash
ansible-playbook provision_lab.yml -e @my_workshop.yml
```

Now get coffee / beer / something, while it provisions.

## Grab Login information

The login information will be stored in the current working directory (`linklight/provisioner`)

```
cat instructor_inventory.txt
```

## Webpage creation

If you used `create_login_page: true` above you will also get a webpage created for students.

The webpage will be generated as {{ec2_name_prefix}}.rhdemo.io
in the example above this literally means http://my_test_workshop.rhdemo.io

## Lab Teardown
If you used automatically created students the file name will always be `generated_student_list.txt`

Do the tear down like this->

```bash
ansible-playbook teardown_lab.yml -e @my_workshop.yml
```
