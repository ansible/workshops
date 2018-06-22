# Lab 4 - Using Ansible to generate dynamic reports

Generally speaking, when one talks about network automation the focus is specifically around configuration management of devices. In this lab you will learn how to use Ansible as a tool to generate living, dynamic documentation. 

This allows the ability to generate reports and documents, using the same information and can cater to the needs of a hands-on-keyboard network engineer to a manager who needs to understand the state of the network with a glance of a web-page!


[Jinja2](http://jinja.pocoo.org/docs/2.10/) is a powerful templating engine for Python. There is native integration of Jinja2 with Ansible. Jinja2 allows for manipulating variables and implementing logical constructs. In combination with the Ansible `template` module, the automation engineer has a powerful tool at their disposal to generate live or dynamic reports.


[Lab: Understanding the template module](./Lab4_template_module.md)


Most CLI based network devices support `show` commands. The output of the commands are "pretty" formatted, in the sense that they are very human readable. However, in the context of automation, where the objective is for a machine(code) to interpret this output, it needs to be transformed into "structured" data. In other words data-types that the code/machine can interpret and navigate. Examples would be lists, dictionaries, arrays and so on.

The Ansible [network-engine](https://github.com/ansible-network/network-engine) is a [role](https://docs.ansible.com/ansible/2.5/user_guide/playbooks_reuse_roles.html) that supports 2 such "translators" - `command_parser` and `textfsm_parser`. These are modules built into the `network-engine` role that takes a raw text input (pretty formatted) and converts it into structured data. You will work with each of these to generate dynamic reports in the following sections:

[Lab: Command parser: show interfaces report](./Lab4_command_parser.md)
**Demo only: TextFSM parser: IP route report**
