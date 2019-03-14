# What this role does
   A typical automation use case is to validate whether access-lists are open
   between a given source and destination IP tuple. This demo uses a role to
   solve this. 
   - [X] Checks for subnets
   - [X] Checks for "any"
   - [X] Checks for "tcp" and "udp" being subsets of IP 

# How to use

``` yaml
---
- name: TEST THE IOS ROLE
  hosts: all
  connection: network_cli
  gather_facts: no

  tasks:

    - include_role:
        name: ios_check_acls
      vars:
        protocol: 'udp'
        action: 'deny'
        src_network: '10.1.1.2'
        src_mask: '255.255.255.255'
        dst_network: '172.17.33.128'
        dst_mask: '255.255.255.128'
        dst_port: '2222'

```

`ansible-playbook -i inventory check_access.yaml`


# To do:

  - [ ] Check for variables
  - [ ] Add role dependencies
  - [ ] Ensure module dependency (netaddr) is installed
  - [ ] Add code to validate source port and range of ports
  - [ ] Handle devices that do not have acls configured on them (fail gracefully)
