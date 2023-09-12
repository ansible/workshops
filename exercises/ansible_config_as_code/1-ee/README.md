# Intro

In this section we will show you step by step how to build an Execution Environment (EE) from code. You will also be publishing this EE to your own private automation hub which you will use in the rest of the tasks.

## Step 1

This lab uses `ansible-core`, `ansible-lint`, and `ansible-builder`, and `podman`. They should be pre-installed on your machine. The versions that are listed are the ones last tested with this workshop.

The following are exepcted to be installed already
ansible-core 2.15.0
ansible-builder 3.0.0
ansible-lint 6.17.0
podman 4.4.1


Further documentation for those who are interested to learn more see:

- [upgrading from ansible to ansible-core](https://access.redhat.com/discussions/6962395)
- [using pip (non supported upstream version)](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

## Step 2

Install our ee_utilities collection and containers.podman using `ansible-galaxy` command. Make sure the versions are correct.

```console
ansible-galaxy collection install infra.ee_utilities:3.1.2 containers.podman:1.10.3 community.general:7.3.0
```

Further documentation for those who are interested to learn more see:

- [installing collections using cli](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html#collections)
- [using collections in AAP](https://docs.ansible.com/ansible-tower/latest/html/userguide/projects.html#collections-support)

## Step 3

### **In the next few steps pay attention to the folder paths and make sure to put the files in the correct folders**

Set the variables to be used in the collections for use. These include hosts, usernames, and other variables that are reused in each role.

Create a file in this folder path `group_vars/all/auth.yml`

{% raw %}

```yaml
---
controller_hostname: "{{ controller_host | default(groups['automationcontroller'][0]) }}"
controller_username: "{{ controller_user | default('admin') }}"
controller_password: "{{ controller_pass }}"
controller_validate_certs: false

ah_host: "{{ ah_hostname | default(groups['automationhub'][0]) }}"
ah_username: "{{ ah_user | default('admin') }}"
ah_password: "{{ ah_pass }}"
ah_path_prefix: 'galaxy'  # this is for private automation hub
ah_validate_certs: false

ee_registry_username: "{{ ah_username }}"
ee_registry_password: "{{ ah_password }}"
ee_registry_dest: "{{ ah_host }}"

ee_base_registry: "{{ ah_host }}"
ee_base_registry_username: "{{ ah_username }}"
ee_base_registry_password: "{{ ah_password }}"
...

```

{% endraw %}

Further documentation for those who are interested to learn more see:

- [more about group_vars](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#organizing-host-and-group-variables)

## Step 4

Create your inventory file `inventory.yml`, **YOU WILL NEED TO FILL THESE IN** copy in the servers replacing lines 77, 81, and 85.

```yaml
---
all:
  children:
    automationcontroller:
      hosts:
        HOST_HERE:

    automationhub:
      hosts:
        HOST_HERE:

    builder:
      hosts:
        VSCODE_HOST:
...

```

NOTE: These are hostnames do not have 'https://' or things will fail

Further documentation for those who are interested to learn more see:

- [more about inventories](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#inventory-basics-formats-hosts-and-groups)
- [how to use this source in AAP](https://docs.ansible.com/ansible-tower/latest/html/userguide/inventories.html#add-source)

## Step 5

Create a vault file `vault.yml` and **YOU WILL NEED TO FILL THESE IN** with the correct passwords for each variable. Currently they are set to the description of what you should be updating them too.

```yaml
---
vault_pass: 'the password to decrypt this vault'
machine_pass: 'password for root user on hub'
controller_pass: 'account pass for controller'
ah_pass: 'hub admin account pass'
controller_api_user_pass: 'this will create and use this password can be generated'
ah_token_password: 'this will create and use this password can be generated'
student_account: 'this is the account under Git Access on your workbench information page, example: student2'
...

```

NOTE: the easiest way to do this is have all passwords be the provided password.


Create a `.password` file **We do not recommend you do this outside of lab environment** put your generated password in this file. Even though we are not committing this file into git because we have it in our ignore list, we do not recommend putting passwords in plain text ever, this is just to simplify/speed up the lab.

```text
Your_Generated_Password_In_.password_File
```

Create an `ansible.cfg` file to point to the .password file.

```ini
[defaults]
vault_password_file=.password
```

Encrypt vault with the password in the .password file

```console
ansible-vault encrypt vault.yml
```

Further documentation for those who are interested to learn more see:

- [ansible vaults](https://docs.ansible.com/ansible/latest/user_guide/vault.html)
- [vault with navigator](https://ansible-navigator.readthedocs.io/en/latest/faq/#how-can-i-use-a-vault-password-with-ansible-navigator)

## Step 6

Create a new playbook called `playbooks/build_ee.yml` and make the hosts use the group builder (which for this lab we are using automation hub, see note) and turn gather_facts on. Then add include role infra.ee_utilities.ee_builder

Note: this we would normally suggest being a small cli only server for deploying config as code and running installer/upgrades for AAP

```yaml
---
- name: Playbook to configure execution environments
  hosts: builder
  gather_facts: true
  vars_files:
    - "../vault.yml"
  tasks:
    - name: Include ee_builder role
      ansible.builtin.include_role:
        name: infra.ee_utilities.ee_builder
...

```

Further documentation for those who are interested to learn more see:

- [include vs import](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/include_role_module.html)
- [ee_builder role](https://github.com/redhat-cop/ee_utilities/tree/main/roles/ee_builder)

## Step 7

Create a file `group_vars/all/ah_ee_list.yml` where we will create a list called `ee_list` that has 4 variables per item which are:

- `name` this is required and will be what the EE image will be called
- `bindep` this is any system packages that would be needed
- `python` these are any python modules that need to be added through pip (excluding ansible)
- `collections` any collections that you would like to be built into your EE image

which the role will loop over and for each item in this list it will create and publish an EE using the provided variables.

{% raw %}

```yaml
---
ee_list:
  - name: "config_as_code"
    dependencies:
      galaxy:
        collections:
          - name: infra.controller_configuration
            version: 2.5.1
          - name: infra.ah_configuration
            version: 2.0.3
          - name: infra.ee_utilities
            version: 3.1.2
          - name: awx.awx
            version: 22.4.0
          - name: containers.podman
            version: 1.10.3
          - name: community.general
            version: 7.3.0

ee_base_image: "{{ ah_host }}/ee-minimal-rhel8:latest"
ee_image_push: true
ee_prune_images: false
ee_create_ansible_config: false
ee_pull_collections_from_hub: false
...
```

{% endraw %}

Further documentation for those who are interested to learn more see:

- [YAML lists and more](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html)
- [builder role documentation](https://github.com/redhat-cop/ee_utilities/blob/main/roles/ee_builder/README.md#build-argument-defaults)

## Step 8

Run the playbook pointing to the recently created inventory file and limit the run to just builder to build your new custom EE and publish it to private automation hub.

```console
ansible-playbook -i inventory.yml -l builder playbooks/build_ee.yml
```

Further documentation for those who are interested to learn more see:

- [more on ansible-playbook](https://docs.ansible.com/ansible/latest/cli/ansible-playbook.html#ansible-playbook)

[previous task](../0-setup/README.md) [next task](../2-pah/README.md)
