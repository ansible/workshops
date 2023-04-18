# Automated Satellite Workshop

**Read this in other languages**:
<br>![uk](../../images/uk.png) [English](README.md), ![france](../../images/fr.png) [Français](README.fr.md).
<br>

In this workshop, you will learn how to get the most from Red Hat Satellite in concert with Red Hat Ansible Automation Platform.

## Table of Contents
- [Use Cases](#use-cases)
- [Presentations](#presentations)
- [Time planning](#time-planning)
- [Lab Diagram](#lab-diagram)
- [Workshop Exercises](#Workshop-Exercises)

## Use Cases

This workshop currently focuses on 3 main customer pain points:
- Compliance (OpenSCAP Scanning) and Vulnerability Management
- Patch/Package Management
- CentOS to RHEL conversion
- (WIP) RHEL 7 > 8/9
- Vulnerability Management with Insights

## Presentations

The exercises are self explanatory and guide the participants through the entire lab. All concepts are explained when they are introduced.

There is an optional presentation available to support the workshops and explain Automation, the basics of Ansible and the topics of the exercises in more detail.  Workshop presentation is located at [Automated Satellite Workshop](https://aap2.demoredhat.com/decks/ansible_auto_satellite.pdf).

Also have a look at our Ansible Best Practices Deck:
[Ansible Best Practices](../../decks/ansible_best_practices.pdf)

## Time planning

The time required to do the workshops strongly depends on multiple factors: the number of participants, how familiar those are with Linux in general and how much discussions are done in between.

Having said that, the exercises themselves should take roughly 4 hours. Each lab takes roughly 30-45 minutes. The accompanying presentation itself adds ~1 hour.

## Lab Diagram
![automated Satellite lab diagram](../../images/ansible_smart_mgmt_diagram.png#centreme)

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
* [Exercise 4: Setup Insights](4-setupinsights/README.md)
* [Exercise 5: Explore Insights](5-exploreinsights/README.md)
* [Exercise 6: Remediate Vulnerability](6-remediatevulnerability/README.md)
