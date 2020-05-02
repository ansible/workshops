# Red Hat Ansible Automation Platform Workshops

The Red Hat Ansible Automation Workshops project is intended for effectively demonstrating Ansible's capabilities through instructor-led workshops or self-paced exercises.

# Website

 - [http://ansible.github.io/workshops](http://ansible.github.io/workshops) - Check out the optional website which is rendered automatically from markdown files using [Github Pages](https://pages.github.com/).  If you are already on the website please ignore this section.


# Instructor-led Workshops

| Workshop   | Presentation Deck  | Exercises  | Workshop Type Var   |
|---|---|---|---|
| **Ansible Red Hat Enterprise Linux Workshop** <br> focused on automating Linux platforms like Red Hat Enterprise Linux  | [Deck](./decks/ansible_rhel.pdf) | [Exercises](./exercises/ansible_rhel)  | `workshop_type: rhel`  |
| **Ansible Network Automation Workshop** <br> focused on router and switch platforms like Arista, Cisco, Juniper   | [Deck](./decks/ansible_network.pdf) | [Exercises](./exercises/ansible_network)  | `workshop_type: network`  |
| **Ansible F5 Workshop** <br> focused on automation of F5 BIG-IP  | [Deck](./decks/ansible_f5.pdf) | [Exercises](./exercises/ansible_f5)   | `workshop_type: f5` |
| **Ansible Security Automation** <br> focused on automation of security tools like Check Point Firewall, IBM QRadar and the IDS Snort  | [Deck](./decks/ansible_security.pdf) | [Exercises](./exercises/ansible_security)   | `workshop_type: security` |
| **Ansible Windows Automation Workshop** <br> focused on automation of Microsoft Windows  | [Deck](./decks/ansible_windows.pdf) | [Exercises](./exercises/ansible_windows)   | `workshop_type: windows` |

## Lab Provisioner
 - [AWS Lab Provisioner](provisioner) - playbook that spins up instances on AWS for students to perform the exercises provided above.

# Self Paced Exercises

 - [Vagrant Demo](vagrant-demo) - Self-paced network automation exercises that can be run on your personal laptop

# Demos

 - [Demos](demos) - These demos are intended for effectively demonstrating Ansible capabilities with prescriptive guides on the Ansible Automation Workshop infrastructure.

# Documentation

 - [How to contribute](docs/contribute.md)
 - [How to use the AWS Lab Provisioner](provisioner/README.md)
 - [FAQ](docs/faq.md)
 - [Release Process](docs/release.md)

---
![Red Hat Ansible Automation](images/rh-ansible-automation-platform.png)
