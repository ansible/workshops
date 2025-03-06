# Workshop Exercise - Using Variables

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table of Contents

- [Workshop Exercise - Using Variables](#workshop-exercise---using-variables)
  - [Table of Contents](#table-of-contents)
  - [Objective](#objective)
  - [Guide](#guide)
    - [Step 1 - Understanding Variables](#step-1---understanding-variables)
    - [Step 2 - Variable Syntax and Creation](#step-2---variable-syntax-and-creation)
    - [Step 3 - Running the Modified Playbook](#step-3---running-the-modified-playbook)
    - [Step 4 - Advanced Variable Usage in Checks Playbook](#step-4---advanced-variable-usage-in-checks-playbook)


## Objective
Extending our playbooks from Exercise 1.3, the focus turns to the creation and usage of variables in Ansible. You'll learn the syntax for defining and using variables, an essential skill for creating dynamic and adaptable playbooks.

## Guide
Variables in Ansible are powerful tools for making your playbooks flexible and reusable. They allow you to store and reuse values, making your playbooks more dynamic and adaptable.

### Step 1 - Understanding Variables
A variable in Ansible is a named representation of some data. Variables can contain simple values like strings and numbers, or more complex data like lists and dictionaries.

### Step 2 - Variable Syntax and Creation
The creation and usage of variables involve a specific syntax:

1. Defining Variables: Variables are defined in the `vars` section of a playbook or in separate files for larger projects.
2. Variable Naming: Variable names should be descriptive and adhere to rules such as:
   * Starting with a letter or underscore.
   * Containing only letters, numbers, and underscores.
3. Using Variables: Variables are referenced in tasks using the double curly braces in quotes {% raw %} `"{{ variable_name }}"` {% endraw %}. This syntax tells Ansible to replace it with the variable's value at runtime.


Update the `system_setup.yml` playbook to include and use a variable:

{% raw %}
```yaml
---
- name: Basic System Setup
  hosts: node1
  become: true
  vars:
    user_name: 'Roger'
  tasks:
    - name: Update all security-related packages
      ansible.builtin.package:
        name: '*'
        state: latest
        security: true

    - name: Create a new user
      ansible.builtin.user:
        name: "{{ user_name }}"
        state: present
        create_home: true
```
{% endraw %}

Run this playbook with `ansible-navigator`.

### Step 3 - Running the Modified Playbook

Execute the updated playbook:

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_setup.yml -m stdout
```

```bash
PLAY [Basic System Setup] ******************************************************

TASK [Gathering Facts] *********************************************************
ok: [node1]

TASK [Update all security-related packages] ************************************
ok: [node1]

TASK [Create a new user] *******************************************************
changed: [node1]

PLAY RECAP *********************************************************************
node1                      : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Notice how the updated playbook shows a status of changed in the Create a new user task. The user, ‘Roger’, specified within the vars section has been created.

Verify the user creation via:

```bash
[student@ansible-1 lab_inventory]$ ssh node1 id Roger
```

### Step 4 - Advanced Variable Usage in Checks Playbook
Enhance the `system_checks.yml` playbook to check for the ‘Roger’ user within the system using the `register` variable and `when` conditional statement.

The register keyword in Ansible is used to capture the output of a task and save it as a variable.


Update the `system_checks.yml` playbook:

{% raw %}

```yaml
---
- name: System Configuration Checks
  hosts: node1
  become: true
  vars:
    user_name: 'Roger'
  tasks:
    - name: Check user existence
      ansible.builtin.command:
        cmd: "id {{ user_name }}"
      register: user_check

    - name: Report user status
      ansible.builtin.debug:
        msg: "User {{ user_name }} exists."
      when: user_check.rc == 0
```
{% endraw %}

Playbook Details:

* `register: user_check:` This captures the output of the id command into the variable user_check.
* `when: user_check.rc == 0:` This line is a conditional statement. It checks if the return code (rc) of the previous task (stored in user_check) is 0, indicating success. The debug message will only be displayed if this condition is met.

This setup provides a practical example of how variables can be used to control the flow of tasks based on the outcomes of previous steps.


Run the checks playbook:

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_checks.yml -m stdout
```

Output:

```bash
PLAY [System Configuration Checks] *********************************************

TASK [Gathering Facts] *********************************************************
ok: [node1]

TASK [Check user existence] ****************************************************
changed: [node1]

TASK [Report user status] ******************************************************
ok: [node1] => {
    "msg": "User Roger exists."
}

PLAY RECAP *********************************************************************
node1                      : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Review the output to confirm the user existence check is correctly using the variable and conditional logic.

---
**Navigation**
<br>

{% if page.url contains 'ansible_rhel_90' %}
[Previous Exercise](../3-playbook) - [Next Exercise](../5-surveys)
{% else %}
[Previous Exercise](../1.3-playbook) - [Next Exercise](../1.5-handlers)
{% endif %}
<br><br>
[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md)
