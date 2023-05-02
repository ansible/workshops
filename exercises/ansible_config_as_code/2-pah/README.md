# Intro

In this section you will configure your private automation hub using the code provided that is ***missing some critical values/information*** that you will have to fill in yourself, based on the requirements and looking at readme's for the roles.

## Step 1

Ensure that you have `ansible-navigator` installed on your machine.

```console
sudo dnf install ansible-navigator
```

Further documentation for those who are interested to learn more see:

- [ansible navigator docs](https://ansible-navigator.readthedocs.io/en/latest/installation/#install-ansible-navigator)

## Step 2

Create a file `group_vars/all/ah_repositories.yml` you will need to add `infra.ah_configuration` and `infra.controller_configuration` to the current list of community repositories.

```yaml
---
# Disabled for Workshop use, but can be used for other installations
# ah_repository_certified:
#   token: "{{ cloud_token }}"
#   url: 'https://console.redhat.com/api/automation-hub/'
#   auth_url: 'https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token'
#   wait: true

ah_repository_community:
  requirements:
    - infra.aap_utilities
    - infra.ee_utilities
    - containers.podman
    - awx.awx
  wait: true
...

```

Note: We have ah_repository_certified commented out at this time due to token issues.

Further documentation for those who are interested to learn more see:

- [ah config repository](https://github.com/redhat-cop/ah_configuration/blob/devel/roles/repository/README.md)

## Step 3

{% raw %}

Create a file `group_vars/all/ah_users.yml` make sure this user has `is_superuser` set to `true` and their `password` is set to `"{{ ah_token_password }}"`.

```yaml
---
ah_token_username: "ah_token_user"
ah_users:
  - username: "{{ ah_token_username }}"
    groups:
      - "admin"
    append: true
    state: "present"
...

```

{% endraw %}

Further documentation for those who are interested to learn more see:

- [ah config users](https://github.com/redhat-cop/ah_configuration/blob/devel/roles/user/README.md)

## Step 4

Create a file `group_vars/all/ah_groups.yml` and add `ah_groups` list with one (1) item in it with the `name` of `admin` who's `perms` are `all` and `state` is `present`.
If you need more information follow the documentation link below.

Further documentation for those who are interested to learn more see:

- [ah config groups](https://github.com/redhat-cop/ah_configuration/blob/devel/roles/group/README.md)

## Step 5

Create a playbook `playbooks/hub_config.yml` add in the `repository` role name in the first task and the `user` role name in the last task.

```yaml
---
- name: Configure private automation hub after installation
  hosts: all
  gather_facts: false
  connection: local
  vars_files:
    - "../vault.yml"
  tasks:
    - name: Include repository role
      ansible.builtin.include_role:
        name:

    - name: Include repository sync role
      ansible.builtin.include_role:
        name: infra.ah_configuration.repository_sync

    - name: Include group role
      ansible.builtin.include_role:
        name: infra.ah_configuration.group

    - name: Include user role
      ansible.builtin.include_role:
        name:
...
```

## Step 6

The next step is to run the playbook, for demonstration purposes we are going to show how to get the Execution Environment(EE) that was built in the previous step and run the playbook.

If you wish to skip this step run the playbook this way[^1].

[^1]: `ansible-galaxy collection install infra.ah_configuration` then `ansible-playbook -i inventory.yml -l automationhub playbooks/hub_config.yml`

Login to the automation hub using the podman login command. This will ask for a user:pass. After authenticating pull the config_as_code image.

Use the username: **'admin'** and the password for your account in the workshop.

**Replace rh####** with the correct shortname for the workshop.

```console
podman login --tls-verify=false hub-student#.rh####.example.opentlc.com
podman pull --tls-verify=false hub-student#.rh####.example.opentlc.com/config_as_code:latest
```

Ansible navigator takes the following commands.
The options used are

|CLI Option|Use|
|:---:|:---:|
|`eei`|execution environment to use.|
|`i`|inventory to use.|
|`pa`|pull arguments to use, in this case ignore tls.|
|`m`|which mode to use, defaults to interactive.|

Use these options to run the playbook in the execution environment.

```console
ansible-navigator run playbooks/hub_config.yml --eei hub-student#.rh####.example.opentlc.com/config_as_code -i inventory.yml -l automationhub --pa='--tls-verify=false' -m stdout
```

[previous task](../1-ee/README.md) [next task](../3-controller/README.md)
