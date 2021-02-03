# redhat_cop.tower_utilities.kerberos
## Description
An Ansible role to setup authentication to a windows domain server with kerberos.

## Requirements
This role installs all required packages in order to facilitate authentication.

## Variables

|Name|Required|Default Value|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`krb_realms`|yes|N/A|List of Dictionaries|Used for storing the realm(domain) name and its domain controllers.  A single domain controller can be specified if that is the only available option, but more than one is preferable. See example usage below.|
|`krb_default_realm`|no|undefined|string|If a default realm(domain) is required to be specified this can be set.  Otherwise it remains unset in the krb5.conf.|
|`krb_dns_lookup_realm`|yes|"false"|string|Whether or not to lookup DNS via realm.|
|`krb_dns_lookup_kdc`|no|"true"|string|Indicate whether DNS SRV records should be used to locate the KDCs and other servers for a realm.|
|`krb_ticket_lifetime`|yes|"24h"|string|Sets the default lifetime for initial ticket requests.|
|`krb_renew_lifetime`|yes|"7d"|string|Kerberos renewable ticket lifetime.|
|`krb_forwardable`|yes|"true"|string|Forwardable kerberos tickets.|
|`krb_rdns`|yes|"false"|string|Whether or not to use rdns.|

### Example use of krb_realms
Note that the first listed item in each listed realm's dc_fqdns list will be set as the realm's admin_server.
```yaml
krb_realms:
  - name: "MYDOMAIN.COM"
    dc_fqdns:
      - "foo1.bar.mydomain.com"
      - "foo2.bar.mydomain.com"
  - name: "YOURDOMAIN.COM"
    dc_fqdns:
      - "ad1.yourdomain.com"
      - "ad2.yourdomain.com"
```

## Dependencies

There are no dependencies requred for this role

The dependencies for Linux, are all installed by this role.

For Windows 2k12 and 2k16 the powershell script in files needs to be run in through a privledged Powershell.

For Windows 2k8 the folllowing is required for some ansible modules to work:
Server 2008 R2 Service pack 1
Powershell v4. via Windows Management Framework 4.0 build 6.1
To check what version of powershell is installed, run the following in powershell:
$PSVersionTable.PSVersion

A technet guide on upgrading to 4 is here:
https://social.technet.microsoft.com/wiki/contents/articles/20623.step-by-step-upgrading-the-powershell-version-4-on-2008-r2.aspx

## Tags
If you would like to skip the check of EPEL and python-pip installation, you can skip the tag `prerequisites` with `--skip-tags prerequisites` option at run-time.

## HTTP/HTTPS Proxy Settings
If you require a proxy server to reach external repositories located on the internet, ensure that you have set them either on the server running the playbook, or in the playbook including the role.

## Example Playbook
```yaml
---
- hosts: towers
# If you need proxy settings to install packages from the internet:
# The following 3 lines are optional
  environment:
    http_proxy: "yourproxyurl:andport"
    https_proxy: "yourproxyurl:andport"
  roles:
    - role: redhat_cop.tower_utilities.kerberos
      krb_default_realm: MYDOMAIN.COM
      krb_realms:
        - name: "MYDOMAIN.COM"
          dc_fqdns:
            - "foo1.bar.mydomain.com"
            - "foo2.bar.mydomain.com"
        - name: "YOURDOMAIN.COM"
          dc_fqdns:
            - "ad1.yourdomain.com"
            - "ad2.yourdomain.com"
```

## License
[MIT](LICENSE)

## Author
[Andrew J. Huffman](https://github.com/ahuffman)
