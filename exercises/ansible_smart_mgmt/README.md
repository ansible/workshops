# Automated Smart Management Workshop

In this workshop, you will learn how to get the most from Red Hat Smart Management in concert with Red Hat Ansible Automation Platform.

## Table of Contents
- [Use Cases](#use-cases)
- [Lab Diagram](#lab-diagram)
- [Guide](#guide)

## Use Cases
This workshop focuses on 3 main customer pain points:
- Compliance (OpenSCAP Scanning) and Vulnerability Management
- Patch/Package Management
- CentOS to RHEL conversion + upgrade

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



## Guide
Workshop Presentation: [Partner Content Hub](http://redhat-partner.highspot.com)<br>
*You will need a Red Hat Partner Connect account/login to access. Don't have one? Click [here](https://connect.redhat.com/en/support)*

* [Exercise 0: Configuring the Lab Environment](0-setup)
* [Exercise 1: Compliance / Vulnerability Management](1-compliance)
* [Exercise 2: Patch Management / OS](2-patching)
* [Exercise 3: CentOS to RHEL conversion + upgrade](3-convert2rhel)
