# Automated Smart Management Workshop

In this workshop, you will learn how to get the most from Red Hat Smart Management in concert with Red Hat Ansible Automation Platform.

## Table of Contents
- [Use Cases](#use-cases)
- [Presentations](#presentations)
- [Time planning](#time-planning)
- [Lab Diagram](#lab-diagram)
- [Workshop Exercises](#Workshop-Exercises)

## Use Cases

This workshop focuses on 3 main customer pain points:
- Compliance (OpenSCAP Scanning) and Vulnerability Management
- Patch/Package Management
- CentOS to RHEL conversion
- (WIP) RHEL 7 > 8/9

## Presentations

The exercises are self explanatory and guide the participants through the entire lab. All concepts are explained when they are introduced.

There is an optional presentation available to support the workshops and explain Automation, the basics of Ansible and the topics of the exercises in more detail.  Workshop presentation is WIP and will be added soon.

Also have a look at our Ansible Best Practices Deck:
[Ansible Best Practices](../../decks/ansible_best_practices.pdf)

## Time planning

The time required to do the workshops strongly depends on multiple factors: the number of participants, how familiar those are with Linux in general and how much discussions are done in between.

Having said that, the exercises themselves should take roughly 4 hours. Each lab takes roughly 30-45 minutes. The accompanying presentation itself adds ~1 hour.

## Presentations

The exercises are self explanatory and guide the participants through the entire lab. All concepts are explained when they are introduced.

There is an optional presentation available to support the workshops and explain Automation, the basics of Ansible and the topics of the exercises in more detail.  Workshop presentation is WIP and will be added soon.

Also have a look at our Ansible Best Practices Deck:
[Ansible Best Practices](../../decks/ansible_best_practices.pdf)

## Time planning

The time required to do the workshops strongly depends on multiple factors: the number of participants, how familiar those are with Linux in general and how much discussions are done in between.

Having said that, the exercises themselves should take roughly 4-5 hours. The first section is slightly longer than the second one. The accompanying presentation itself adds ~1 hour.



## Lab Diagram
![automated smart management lab diagram](../../images/ansible_smart_mgmt_diagram.png#centreme)

### Environment

| Role                    | Inventory name |
| ------------------------| ---------------|
| Automation controller   | ansible-1      |
| Satellite Server        | satellite      |
| Managed Host 1 - RHEL   | node1          |
| Managed Host 2 - RHEL   | node2          |
| Managed Host 3 - RHEL   | node3          |
| Managed Host 4 - CentOS | node4          |
| Managed Host 5 - CentOS | node5          |
| Managed Host 6 - CentOS | node6          |



## Workshop Exercises

* [Exercise 0: Configuring the Lab Environment](0-setup/README.md)
* [Exercise 1: Compliance / Vulnerability Management](1-compliance/README.md)
* [Exercise 2: Patch Management / OS](2-patching/README.md)
* [Exercise 3: CentOS to RHEL conversion](3-convert2rhel/README.md)
