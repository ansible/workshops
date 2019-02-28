ids_config
==========

# This content is currently under development and should not be considered production ready

A role to provide configuration for many different Intrusion Detection Systems,
these are defined as "providers" to the Role.

Current supported list of providers:
* snort

Requirements
------------

Red Hat Enterprise Linux 7.x, or derived Linux distribution such as CentOS 7,
Scientific Linux 7, etc

Role Variables
--------------

Role variables that get put into use are IDS provider specific, they are listed
below.

## snort

For the Snort provider you will need to set the `ids_provider` variable as such:

    vars:
      ids_provider: snort

From there, all our `ids_config_*` variables will be namespaced to the
specific provider.

### snort variables

* `ids_config_snort_version`
* `ids_config_snort_rules_files`
* `ids_config_snort_home_net`
* `ids_config_snort_external_net`
* `ids_config_snort_dns_servers`
* `ids_config_snort_smtp_servers`
* `ids_config_snort_http_servers`
* `ids_config_snort_sql_servers`
* `ids_config_snort_telnet_servers`
* `ids_config_snort_ssh_servers`
* `ids_config_snort_ftp_servers`
* `ids_config_snort_sip_servers`
* `ids_config_snort_http_ports`
* `ids_config_snort_shellcode_ports`
* `ids_config_snort_oracle_ports`
* `ids_config_snort_ssh_ports`
* `ids_config_snort_ftp_ports`
* `ids_config_snort_sip_ports`
* `ids_config_snort_file_data_ports`
* `ids_config_snort_gtp_ports`
* `ids_config_snort_rule_path`
* `ids_config_snort_white_list_path`
* `ids_config_snort_black_list_path`
* `ids_config_snort_checksum_mode`
* `ids_config_snort_alert_syslog`

Dependencies
------------

* FIXME - need a namespace for ASA content first, then probably `ids_isntall`
  as dep

Example Playbook
----------------

- name: configure snort
  hosts: idshosts
  vars:
    ids_provider: "snort"
  tasks:
    - name: import ids_config role
      import_role:
        name: "ids_config"

License
-------

BSD

Author Information
------------------

[Ansible Security Automation Team](https://github.com/ansible-security)
