# AAP Download Role

This is the Ansible Automation Platform Download Role.  This will download the .tar.gz file for bundled installation of AAP

For example it will download a file: `ansible-automation-platform-setup-bundle-2.0.0-1-early-access.tar.gz`

Downloads are from the website [Download Red Hat Ansible Automation Platform
](https://access.redhat.com/downloads/content/480/ver=Early%20Access%202.0/rhel---8/Early%20Access%202.0/x86_64/product-software)

## Example Usage

Example of using role:

```
- name: download AAP
  vars:
    app_image: "ansible-automation-platform-2.0-early-access-for-rhel-8-x86_64-files"
    offline_token: "your offline token"
  include_role:
    name: ansible.workshops.aap_download
```

- aap_image is optional and defaults to `ansible-automation-platform-2.0-early-access-for-rhel-8-x86_64-files`
- offline_token is required, please Generate an offline token

## Output

This will output a tar.gz file named ```aap.tar.gz``` in your ```playbook_dir```

Literally-> `"{{ playbook_dir }}/aap.tar.gz"`



## Documentation for API

- [Getting started with Red Hat APIs
](https://access.redhat.com/articles/3626371)
- [Red Hat API Tokens
](https://access.redhat.com/management/api)
