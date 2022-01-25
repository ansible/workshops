# Configure Routers Role

For the Network Automation Workshop (`workshop_type: network`) this role will configure the network devices (Arista, Cisco, Juniper) so that there is OSPF and BGP connections between them.  This allows the students to see a working configuration as soon as they login to the workbench.

This role will probably not be helpful for outside the workshop as it is very specific to this topology

Example:

```
- name: configure core routers
  hosts: core
  connection: local
  gather_facts: false
  tasks:
    - include_role:
        name: ansible.workshops.configure_routers
      vars:
        type: core
      when:
        - ansible_network_os == "ios" or ansible_network_os == "eos"
```
