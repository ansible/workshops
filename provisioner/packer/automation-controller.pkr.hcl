variable "ansible_vars_file" {
    type    = string
    default = null
}

local "extra_args" {
    expression = var.ansible_vars_file != null ? ["-e", "@extra_vars.yml", "-e", var.ansible_vars_file] : ["-e", "@extra_vars.yml"]
}

data "amazon-ami" "automation_controller" {
  filters = {
    virtualization-type = "hvm"
    name                = "RHEL-8*HVM-*Hourly*"
    root-device-type    = "ebs"
    "architecture": "x86_64"
  }
  owners      = ["309956199498"]
  most_recent = true
  region      = "us-east-1"
}

source "amazon-ebs" "automation_controller_source" {
  ami_name             = "automation_controller {{timestamp}}"
  instance_type        = "m4.xlarge"
  region               = "us-east-1"
  associate_public_ip_address = "true"
  source_ami           = data.amazon-ami.automation_controller.id
  ssh_username         = "ec2-user"
  ssh_interface        = "public_ip"
  communicator         = "ssh"
  iam_instance_profile = "seanpacker"
  ami_regions = ["us-east-1"]
  launch_block_device_mappings {
    device_name = "/dev/sda1"
    volume_size = "40"
    volume_type = "gp3"
    delete_on_termination = "true"
    iops = "3000"
    throughput = "125"
  }
  run_tags = {
    "Name" = "packer-build"
    "owner" = "seanc"
  }
}



build {
    sources = ["sources.amazon-ebs.automation_controller_source"]

    provisioner "ansible" {
      command = "ansible-playbook"
      playbook_file = "pre_build_controller.yml"
      user = "ec2-user"
      inventory_file_template = "controller ansible_host={{ .Host }} ansible_user={{ .User }} ansible_port={{ .Port }}\n"
      extra_arguments = local.extra_args
      use_proxy = false
    }
}
