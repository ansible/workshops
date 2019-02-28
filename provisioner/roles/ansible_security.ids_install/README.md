ids_install
===========

# This content is currently under development and should not be considered production ready

A role to install many different Intrusion Detection Systems, these are defined
as "providers" to the Role.

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

`ids_install_pkgs` - List of packages to install on the system, by default this
is left empty and the defaults will be selected for each provider.

## snort

For the Snort provider you will need to set the `ids_install_provider` variable
as such:

    vars:
      ids_install_provider: snort

From there, all our `ids_install_provider_*` variables will be namespaced to the
specific provider.

> Note that the `ids_install_snort_version` and `ids_install_snort_daq_version`
> will change upstream sometimes and care should be taken that you are aligned
> with the correct version.
>
>   https://www.snort.org/

### snort variables

* `ids_install_provider` - Default value: `"snort"`
* `ids_install_normalize_logs` - Default value: `true`
* `ids_install_snort_interface` - Default value: `eth0`
* `ids_install_snort_pkgs` - List of packages to install - Default value:
  `['https://s3.amazonaws.com/linklight.securityautomation/daq-2.0.6-1.el7.x86_64.rpm', 'https://s3.amazonaws.com/linklight.securityautomation/snort-2.9.13-1.centos7.x86_64.rpm', 'libdnet', 'pulledpork']`
* `ids_install_snort_rules` - URI to snort rules - Default value:
  `https://s3.amazonaws.com/linklight.securityautomation/community-rules.tar.gz`
* `ids_install_snort_registeredrule_ver` - Snort registered rules version - Default value: `"29130"`
* `ids_install_snort_promiscuous_interface` - Default value: `False`
* `ids_install_snort_logdir` - Default value: `"/var/log/snort"`
* `ids_install_snort_logfile` - Default value: `"snort.log"`
* `ids_install_snort_config_path` - Default value: `"/etc/snort/snort.conf"`

When `ids_install_normalize_logs` is set, the role will also install
[barnyard2](https://github.com/firnsy/barnyard2) in service of normalizing the
snort logs.


Dependencies
------------

* `geerlingguy.repo-epel`


Example Playbook
----------------

    - name: configure snort
      hosts: idshosts
      vars:
          ids_install_provider: "snort"
          ids_install_normalize_logs: True
      tasks:
        - name: import ids_install role
          import_role:
            name: "ids_install"

License
-------

BSD

Author Information
------------------

[Ansible Security Automation Team](https://github.com/ansible-security)
