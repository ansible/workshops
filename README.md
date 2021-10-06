# Red Hat Ansible Automation Platform Workshops

**Read this in other languages**:
<br>![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English](README.md),  ![japan](https://github.com/ansible/workshops/raw/devel/images/japan.png)[日本語](README.ja.md)

**This is documentation for Ansible Automation Platform 2**

The Red Hat Ansible Automation Workshops project is intended for effectively demonstrating Ansible's capabilities through instructor-led workshops or self-paced exercises.

## Website

- [http://aap2.demoredhat.com](http://aap2.demoredhat.com) - Check out the optional website which is rendered automatically from markdown files using [Github Pages](https://pages.github.com/).  If you are already on the website please ignore this section.

## Instructor-led Workshops

6 hour workshops:
>**Note**
>
>Google Source will only work for Red Hat employees.  PDFs are provided for public consumption.

| Workshop   | Public Deck | Red Hat Internal  | Exercises  | Workshop Type Var   |
|---|---|---|---|---|
| **[Ansible Red Hat Enterprise Linux Workshop](./exercises/ansible_rhel)** <br> focused on automating Linux platforms like Red Hat Enterprise Linux  | [PDF](./decks/ansible_rhel.pdf) | [Google Source](https://docs.google.com/presentation/d/1O2Gj5r_fhjM5Pi5FizrZRInmZ37IlpeKPTP6jSZxEKs/edit?usp=sharing) | [Exercises](./exercises/ansible_rhel)  | `workshop_type: rhel`  |
| **[Ansible Network Automation Workshop](./exercises/ansible_network)** <br> focused on router and switch platforms like Arista, Cisco, Juniper   | [PDF](./decks/ansible_network.pdf) | [Google Source](https://docs.google.com/presentation/d/1PIT-kGAGMVEEK8PsuZCoyzFC5CIzLBwdnftnUsdUNWQ/edit?usp=sharing) | [Exercises](./exercises/ansible_network)  | `workshop_type: network`  |
| **[Ansible F5 Workshop](./exercises/ansible_f5)** <br> focused on automation of F5 BIG-IP  | [PDF](./decks/ansible_f5.pdf) | [Google Source](https://docs.google.com/presentation/d/1eSZHx_tVZ59U-nAYysehEXsSAJgLBr9SrgpjOfLUg84) | [Exercises](./exercises/ansible_f5)   | `workshop_type: f5` |
| **[Ansible Security Automation](./exercises/ansible_security)** <br> focused on automation of security tools like Check Point Firewall, IBM QRadar and the IDS Snort  | [PDF](./decks/ansible_security.pdf) | [Google Source](https://docs.google.com/presentation/d/19gVCBz1BmxC15tDDj-FUlUd_jUUUKay81E8F24cyUjk/edit?usp=sharing) | [Exercises](./exercises/ansible_security)   | `workshop_type: security` |
| **[Ansible Windows Automation Workshop](./exercises/ansible_windows)** <br> focused on automation of Microsoft Windows  | [PDF](./decks/ansible_windows.pdf) | [Google Source](https://docs.google.com/presentation/d/1fGHBNpkvXBfwBC385QswcSOBz0xNzDxEc8ZhbuyIoAE) | [Exercises](./exercises/ansible_windows)   | `workshop_type: windows` |
| \[WIP\] **[Smart Management Automation Workshop](./exercises/ansible_smart_mgmt)** <br> focused on automation of  security and lifecycle management with Red Hat Satellite Server | - | - | [Exercises](./exercises/ansible_smart_mgmt) | `workshop_type: smart_mgmt`

90 minute abbreviated versions:

| Workshop   | Public Deck  | Red Hat Internal | Exercises  | Workshop Type Var   |
|---|---|---|---|---|
| **[Ansible Red Hat Enterprise Linux Workshop](./exercises/ansible_rhel_90)** <br> focused on automating Linux platforms like Red Hat Enterprise Linux  | [PDF](./decks/ansible_rhel_90.pdf) | [Google Source](https://docs.google.com/presentation/d/143JtFwmz469ucKNbB4L5T-PtKfurjpcOmCICzSbwm3Y) | [Exercises](./exercises/ansible_rhel_90)  | `workshop_type: rhel_90`  |

## Self Paced Exercises

- [Ansible Automation Platform Self-Paced Labs
](https://www.redhat.com/en/engage/redhat-ansible-automation-202108061218) - These interactive learning scenarios provide you with a pre-configured Ansible Automation Platform environment to experiment, learn, and see how the platform can help you solve real-world problems. The environment runs entirely in your browser, enabling you to learn more about our technology at your pace and time.

## Product Demos

- [Demos](https://github.com/ansible/product-demos) - These demos are intended for effectively demonstrating Ansible capabilities with prescriptive guides on the Ansible Automation Workshop infrastructure.

## Workshop Documentation

- [Workshop attendance website](docs/attendance/attendance.md)
- [How to contribute](docs/contribute.md)
- [How to use the AWS Lab Provisioner](provisioner/README.md)
- [FAQ](docs/faq.md)
- [Release Process](docs/release.md)

## Additional Content

- [Get a Trial Subscription for Red Hat Ansible Automation Platform](http://red.ht/try_ansible)
- [Ansible Blog - The Inside Playbook](https://www.ansible.com/blog)
- [Ansible YouTube](https://youtube.com/ansibleautomation)
- [Ansible Getting Started Guide](https://docs.ansible.com/ansible/latest/user_guide/index.html#get)
- [Ansible Network Automation - Getting Started](https://docs.ansible.com/ansible/latest/network/getting_started/index.html)
- [Red Hat Training and Certification for Red Hat Ansible Automation Platform](https://red.ht/aap_training)

## Slack Community

- [Join us on Ansible Network Slack](https://join.slack.com/t/ansiblenetwork/shared_invite/zt-3zeqmhhx-zuID9uJqbbpZ2KdVeTwvzw)

## E-Books

- [The Automated Enterprise](https://www.redhat.com/en/engage/automated-enterprise-ebook-20171107?intcmp=7013a000002DXg8AAG)

### E-Books for Ansible Network Automation

  - [Part 1: Modernize Your Network with Red Hat](https://www.ansible.com/resources/ebooks/network-automation-for-everyone?hsLang=en-us)
  - [Part 2: Automate Your Network with Red Hat](https://www.redhat.com/en/engage/network-automation-ebook-s-202104291219)

#### Other languages
  - ![chinese](https://github.com/ansible/workshops/raw/devel/images/cn.png)[借助红帽实现网络自动化](https://www.redhat.com/rhdc/managed-files/ma-network-automation-technical-e-book-f28378-202104-a4-zh.pdf)
  - ![french](https://github.com/ansible/workshops/raw/devel/images/fr.png)[Automatiser votre réseau avec Red Hat](https://www.redhat.com/rhdc/managed-files/ma-network-automation-technical-e-book-f28378-202104-a4-fr.pdf)
  - ![italian](https://github.com/ansible/workshops/raw/devel/images/it.png)[Automatizzare la rete con Red Hat](https://www.redhat.com/rhdc/managed-files/ma-network-automation-technical-e-book-f28378-202104-a4-it.pdf)

### E-Books for Ansible Security Automation

  - [Simplify your security operations center](https://www.redhat.com/en/resources/security-automation-ebook?extIdCarryOver=true&sc_cid=7013a000002gyQ2AAI)

---
![Red Hat Ansible Automation](https://github.com/ansible/workshops/raw/devel/images/rh-ansible-automation-platform.png)
