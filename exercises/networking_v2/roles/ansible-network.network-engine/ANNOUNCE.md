Ansible Network: Network Engine Release
----------------------------------------

The Ansible Network team is pleased to announce that the initial release of the Network Engine Ansible role is now available in Ansible Galaxy!

What is an Ansible Role?
----------------------------------
An Ansible Role is a collection of related tasks, methods, plugins, and modules in a standard format. You can use Roles in tasks or playbooks.

What does the Network Engine Role do?
----------------------------------
The Network Engine Role provides the fundamental building blocks for a data-model-driven approach to automated network management. Network Engine:

 - extracts data about your network devices
 - returns the data as Ansible facts in a JSON data structure, ready to be added to your inventory host facts and/or consumed by Ansible tasks and templates
 - works on any network platform

With the Network Engine role, and other Roles built around it, you can normalize your Ansible facts across your entire network.

How do I get it?
----------------------------------
Via Ansible Galaxy using the following Linux command:

`ansible-galaxy install ansible-network.network-engine`

How do I use it?
----------------------------------
See the [User Guide](https://github.com/ansible-network/network-engine/blob/devel/docs/user_guide/README.md) for details and examples.

