# Workshop Exercise - Debugging and Error Handling

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).


## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
  - [Step 1 - Introduction to Debugging in Ansible](#step-1---introduction-to-debugging-in-ansible)
  - [Step 2 - Utilizing the Debug Module](#step-2---utilizing-the-debug-module)
  - [Step 3 - Error Handling with Blocks](#step-3---error-handling-with-blocks)
  - [Step 4 - Running with Verbose Mode](#step-4---running-with-verbose-mode)
  - [Summary](#summary)

## Objective

Building on the foundational knowledge from previous exercises, this session focuses on debugging and error handling within Ansible. You'll learn techniques to troubleshoot playbooks, manage errors gracefully, and ensure your automation is robust and reliable.

## Guide

### Step 1 - Introduction to Debugging in Ansible

Debugging is a critical skill for identifying and resolving issues within your Ansible playbooks. Ansible provides several mechanisms to help you debug your automation scripts, including the debug module, increased verbosity levels, and error handling strategies.

### Step 2 - Utilizing the Debug Module

The `debug` module is a simple yet powerful tool for printing variable values, which can be instrumental in understanding playbook execution flow.

In this example, add debug tasks to your Apache role in the `tasks/main.yml` to output the value of variables or messages.

#### Implement Debug Tasks:

Insert debug tasks to display the values of variables or custom messages for troubleshooting:

{% raw %}

```yaml
- name: Display Variable Value
  ansible.builtin.debug:
    var: apache_service_name

- name: Display Custom Message
  ansible.builtin.debug:
    msg: "Apache service name is {{ apache_service_name }}"
```

{% endraw %}

### Step 3 - Error Handling with Blocks

Ansible allows grouping tasks using `block` and handling errors with `rescue` sections, similar to try-catch in traditional programming.

In this example, add a block to handle potential errors during the Apache configuration within the `tasks/main.yml` file.

1. Group Tasks and Handle Errors:

Wrap tasks that could potentially fail in a block and define a rescue section to handle errors:

{% raw %}

```yaml
- name: Apache Configuration with Potential Failure Point
  block:
    - name: Copy Apache configuration
      ansible.builtin.copy:
        src: "{{ apache_conf_src }}"
        dest: "/etc/httpd/conf/httpd.conf"
  rescue:
    - name: Handle Missing Configuration
      ansible.builtin.debug:
        msg: "Missing Apache configuration file '{{ apache_conf_src }}'. Using default settings."
```

{% endraw %}

2. Add an `apache_conf_src` variable within `vars/main.yml` of the apache role.

```yaml
apache_conf_src: "files/missing_apache.conf"
```

> NOTE: This file explicitly does not exist so that we can trigger the rescue portion from our `tasks/main.yml`

### Step 4 - Running with Verbose Mode

Ansible's verbose mode (-v, -vv, -vvv, or -vvvv) increases the output detail, providing more insights into playbook execution and potential issues.

#### Execute Playbook in Verbose Mode:

Run your playbook with the `-vv` option to get detailed logs:

```bash
ansible-navigator run deploy_apache.yml -m stdout -vv
```

```
.
.
.


TASK [apache : Display Variable Value] *****************************************
task path: /home/rhel/ansible-files/roles/apache/tasks/main.yml:20
ok: [node1] => {
    "apache_service_name": "httpd"
}
ok: [node2] => {
    "apache_service_name": "httpd"
}
ok: [node3] => {
    "apache_service_name": "httpd"
}

TASK [apache : Display Custom Message] *****************************************
task path: /home/rhel/ansible-files/roles/apache/tasks/main.yml:24
ok: [node1] => {
    "msg": "Apache service name is httpd"
}
ok: [node2] => {
    "msg": "Apache service name is httpd"
}
ok: [node3] => {
    "msg": "Apache service name is httpd"
}

TASK [apache : Copy Apache configuration] **************************************
task path: /home/rhel/ansible-files/roles/apache/tasks/main.yml:30
An exception occurred during task execution. To see the full traceback, use -vvv. The error was: If you are using a module and expect the file to exist on the remote, see the remote_src option
fatal: [node3]: FAILED! => {"changed": false, "msg": "Could not find or access 'files/missing_apache.conf'\nSearched in:\n\t/home/student/lab_inventory/roles/apache/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/missing_apache.conf\n\t/home/student/lab_inventory/files/files/missing_apache.conf\n\t/home/student/lab_inventory/files/missing_apache.conf on the Ansible Controller.\nIf you are using a module and expect the file to exist on the remote, see the remote_src option"}
An exception occurred during task execution. To see the full traceback, use -vvv. The error was: If you are using a module and expect the file to exist on the remote, see the remote_src option
fatal: [node1]: FAILED! => {"changed": false, "msg": "Could not find or access 'files/missing_apache.conf'\nSearched in:\n\t/home/student/lab_inventory/roles/apache/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/missing_apache.conf\n\t/home/student/lab_inventory/files/files/missing_apache.conf\n\t/home/student/lab_inventory/files/missing_apache.conf on the Ansible Controller.\nIf you are using a module and expect the file to exist on the remote, see the remote_src option"}
An exception occurred during task execution. To see the full traceback, use -vvv. The error was: If you are using a module and expect the file to exist on the remote, see the remote_src option
fatal: [node2]: FAILED! => {"changed": false, "msg": "Could not find or access 'files/missing_apache.conf'\nSearched in:\n\t/home/student/lab_inventory/roles/apache/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/missing_apache.conf\n\t/home/student/lab_inventory/files/files/missing_apache.conf\n\t/home/student/lab_inventory/files/missing_apache.conf on the Ansible Controller.\nIf you are using a module and expect the file to exist on the remote, see the remote_src option"}


TASK [apache : Handle Missing Configuration] ***********************************
task path: /home/rhel/ansible-files/roles/apache/tasks/main.yml:39
ok: [node1] => {
    "msg": "Missing Apache configuration file 'files/missing_apache.conf'. Using default settings."
}
ok: [node2] => {
    "msg": "Missing Apache configuration file 'files/missing_apache.conf'. Using default settings."
}
ok: [node3] => {
    "msg": "Missing Apache configuration file 'files/missing_apache.conf'. Using default settings."
}

PLAY RECAP *********************************************************************
node1                      : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0   
node2                      : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0   
node3                      : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0 

```

Notice how the playbook shows there was an error copying the Apache Configuration file but the playbook was able to handle it via the rescue block that was provided. If you notice the final task ‘Handle Missing Configuration’ details that the file was missing and it would use the default settings. 

The final Play Recap shows us that there was a rescued block used via the `rescued=1` per node in the web group.

## Summary

In this exercise, you've explored essential debugging techniques and error handling mechanisms in Ansible. By incorporating debugging tasks, using blocks for error handling, and leveraging verbose mode, you can effectively troubleshoot and enhance the reliability of your Ansible playbooks. These practices are fundamental in developing robust Ansible automation that can gracefully handle unexpected issues and ensure consistent, predictable outcomes.

---
**Navigation**
<br>
[Previous Exercise](../1.7-role) - [Next Exercise](../2.1-intro)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-1---ansible-engine-exercises)
