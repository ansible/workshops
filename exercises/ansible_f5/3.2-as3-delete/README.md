# Exercise 2.0 - Disabling a pool member

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
- [Playbook Output](#playbook-output)
- [Solution](#solution)

# Objective

Demonstrate building a virtual server (exactly like the Section 1 Ansible F5 Exercises) with F5 AS3

  - Learn about AS3 ([Application Services 3 Extension](https://clouddocs.f5.com/products/extensions/f5-appsvcs-extension/3/userguide/about-as3.html)) declarative model.
  - Learn about the [set_fact module](https://docs.ansible.com/ansible/latest/modules/set_fact_module.html)
  - Learn about the [uri module](https://docs.ansible.com/ansible/latest/modules/uri_module.html)


# Guide

## Step 1:

Make sure the F5 BIG-IP has AS3 enabled.  

  1. Login to the F5 BIG-IP through your web browser.  
  2. Click on the iApps button on the lefthand menu.  
  3. Click the `Package Management LX` Link
  4. Make sure that `f5-appsvcs` is installed.  

If this is not working please ask your instructor for help.

![f5 gui](f5-appsvcs.gif)

## Step 2:

Using your text editor of choice create a new file called `as3.yml`:

>`vim` and `nano` are available on the control node, as well as Visual Studio and Atom via RDP

## Step 4:

Enter the following play definition into `as3.yml`:

``` yaml
---
- name: LINKLIGHT AS3
  hosts: lb
  connection: local
  gather_facts: false

  vars:
    pool_members: "{{ groups['webservers'] }}"
```

- The `---` at the top of the file indicates that this is a YAML file.
- The `hosts: lb`,  indicates the play is run only on the lb group.  Technically there only one F5 device but if there were multiple they would be configured simultaneously.
- `connection: local` tells the Playbook to run locally (rather than SSHing to itself)
- `gather_facts: false` disables facts gathering.  We are not using any fact variables for this playbook.

This section from above...
```
  vars:
    pool_members: "{{ groups['webservers'] }}"
```
...sets a variable named `pool_members`, to the webservers group.  There are two webservers on the workbench, `host1` and `host2`.  This means that the `pool_members` variable refers to a list of two webservers.

## Step 5

**Append** the following to the as3.yml Playbook.  

```
  tasks:

  - name: CREATE AS3 JSON BODY
    set_fact:
      as3_app_body: "{{ lookup('template', 'j2/as3_template.j2', split_lines=False) }}"
```

The module [set_fact module](https://docs.ansible.com/ansible/latest/modules/set_fact_module.html) allows a Playbook to create (or override) a variable as a task within a Play.  This can be used to create new facts on the fly dynamically that didn't exist until that point in the Play.  In this case the [template lookup plugin](https://docs.ansible.com/ansible/latest/plugins/lookup/template.html) is being used.  This task
  1. renders the j2/as3_template.j2 jinja template that is provided.
  2. creates a new fact named `as3_app_body` that is just JSON text.


## Step 6

**Append** the following to the as3.yml Playbook.  This task uses the uri module which is used to interact with HTTP and HTTPS web services and supports Digest, Basic and WSSE HTTP authentication mechanisms.  This module is extremely common and very easy to use.  The workshop itself (the Playbooks that provisioned the workbenches) uses the uri module to configure and license Red Hat Ansible Tower.

```
  - name: PUSH AS3
    uri:
      url: "https://{{ ansible_host }}:8443/mgmt/shared/appsvcs/declare"
      method: POST
      body: "{{ lookup('template','j2/tenant_base.j2', split_lines=False) }}"
      status_code: 200
      timeout: 300
      body_format: json
      force_basic_auth: yes
      user: "{{ ansible_user }}"
      password: "{{ ansible_ssh_pass }}"
      validate_certs: no
    delegate_to: localhost
```

Explanation of parameters:
|  parameter | explanation  |
|---|---|
| `- name: PUSH AS3` | human description of Playbook task, prints to terminal window |
|  `uri:` |  this task is calling the [uri module](https://docs.ansible.com/ansible/latest/modules/uri_module.html) |
| `url: "https://{{ ansible_host }}:8443/mgmt/shared/appsvcs/declare"`  | webURL (API) for AS3 |
| `method: POST` | HTTP method of the request, must be uppercase.  Module documentation page has list of all options.  This could also be a `DELETE` vs a `POST` |
| `body: "{{ lookup('template','j2/tenant_base.j2', split_lines=False) }}"` | This sends the combined template (the `tenant_base.j2` which contains `as3_template.j2`) and is passed as the body for the API request. |
| `status_code: 200` | A valid, numeric, [HTTP status code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) that signifies success of the request. Can also be comma separated list of status codes.  200 means OK, which is a standard response for successful HTTP requests |
| `timeout: 300` | The socket level timeout in seconds |

The rest of the parameters are for authentication to the F5 BIG-IP.


## Step 7
Run the playbook - exit back into the command line of the control host and execute the following:

```
[student1@ansible ~]$ ansible-playbook as3.yml
```

# Playbook Output

The output will look as follows.

```yaml
PLAY [Get Status] **************************************************************

TASK [Query BIG-IP for Pool "/Common/http_pool" facts] *************************
ok: [f5]

TASK [Display pool member status] **********************************************
ok: [f5] => {
    "ansible_facts.pool[pool_path].monitor_instance": [
        {
            "enabled_state": 1,
            "instance": {
                "instance_definition": {
                    "address_type": "ATYPE_EXPLICIT_ADDRESS_EXPLICIT_PORT",
                    "ipport": {
                        "address": "18.208.130.134",
                        "port": 80
                    }
                },
                "template_name": "/Common/http"
            },
            "instance_state": "INSTANCE_STATE_UP"
        },
        {
            "enabled_state": 1,
            "instance": {
                "instance_definition": {
                    "address_type": "ATYPE_EXPLICIT_ADDRESS_EXPLICIT_PORT",
                    "ipport": {
                        "address": "34.224.26.74",
                        "port": 80
                    }
                },
                "template_name": "/Common/http"
            },
            "instance_state": "INSTANCE_STATE_UP"
        }
    ]
}

TASK [Get all the members for pool "/Common/http_pool" and store in a variable]
ok: [f5]

TASK [Display pool members ip:port information] ********************************
ok: [f5] => (item={u'port': 80, u'address': u'/Common/host1'}) => {
    "msg": "/Common/host1"
}
ok: [f5] => (item={u'port': 80, u'address': u'/Common/host2'}) => {
    "msg": "/Common/host2"
}

TASK [Force pool member offline] ***********************************************
changed: [f5] => (item={u'port': 80, u'address': u'/Common/host1'})
skipping: [f5] => (item={u'port': 80, u'address': u'/Common/host2'})

PLAY RECAP *********************************************************************
f5                         : ok=5    changed=1    unreachable=0    failed=0
```

# Solution
The solution will be provided by the instructor if you are stuck.  The GUI should show something similar to the following with a black diamond indicating the specified node was forced offline.

![f5bigip-gui](f5bigip-gui.png)

--
You have finished this exercise.  [Click here to return to the lab guide](../README.md)
