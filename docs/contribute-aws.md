# Contribute a new workshop environment for AWS (Amazon Web Services )

There are four components to the AWS `manage_ec2_instances` role:

   - **resources** - this provisions AWS Virtual Private Cloud (VPC), the associated Security Group, the EC2 subnet, route table and SSH key-pair.  The network and security workshop types use two VPCs to create separate networks.  Example for resources can be found in `provisioner/roles/manage_ec2_instances/tasks/resources`.  If you only need a single VPC, you most likely do not have to worry about the resources, and can just copy the default `workshop_type: rhel` setup.

   - **instances** - this provisions the actual Amazon instances (e.g. Red Hat Enterprise Linux 8, Cisco IOS, Microsoft Windows, etc) onto the VPC recreated in the `resources` part of the provisioner.  Examples for each `workshop_type` can be found in `provisioner/roles/manage_ec2_instances/tasks/instances`

   - **ami_find** - this dynamically figures out the correct AMI (Amazon Machine Image) to use depending on which Amazon region you are in (e.g. `us-east-1`).  Examples for each `workshop_type` can be found in `provisioner/roles/manage_ec2_instances/tasks/ami_find`

   - **inventory** - this loads the newly created instances into Ansible Inventory so subsequent Ansible Plays can be executed.  This is so Ansible can now configure the vanilla images by making changes to the newly created instances.  For example we install Ansible for each student, configure their `/etc/hosts`, the `~/.ssh/config` and much more depending the `workshop_type`.  Examples of inventory can be found in `provisioner/roles/manage_ec2_instances/tasks/inventory`
