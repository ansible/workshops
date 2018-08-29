# ServiceNow Demo for Linklight

## Table of Contents
  - [Setup](#setup)
  - [Demo 01 - Config Drift](#Demo-01-Config-Drift)

## Setup

  - Setup a free account
    https://developer.servicenow.com/

  - Click **Manage** and create an instance

    ![manage](images/manage.png)

    A URL will be provided like ```https://dev66073.service-now.com/```

  - Login to your WebURL and reset your password.
    ![snow](images/snow.png)

  - Record these three pieces of information that will provide authentication.

    | Field | Input |
    | -------- |:--------------------|
    | username | admin |
    | password | ThisIsAFakePassword |
    | instance | dev66073      |

    **Tip 1** the instance is part the webURL e.g. https://dev66073.service-now.com/ is `dev66073`

    **Tip 2** the password is **not** the same as your password to login to https://developer.servicenow.com/.  To reset it click on **Action** and then **Reset admin password**

    ![reset](images/reset.png)

  - Install pysnow
    https://pysnow.readthedocs.io/en/latest/

    ```$ pip install pysnow```

    **Tip** When using Tower use [this guide](https://docs.ansible.com/ansible-tower/latest/html/upgrade-migration-guide/virtualenv.html).  Tower uses a virtualenv so the install changes slightly:

    ```
    # source /var/lib/awx/venv/ansible/bin/activate
    # umask 0022
    # pip install pysnow
    # deactivate

## Demo 01 - Config Drift

### Objective

Demonstrate automatic ticket creation for configuration drift.  When the configuration for a Cisco CSR router doesn't match desired config, a ServiceNow ticket with relevant information will be created.

### Guide

#### Preface

This demo is built for the Linklight workbench.  To use the demo it is recommended to run the [provisioner](../../provisioner/README.md) for **networking mode**.  By standardizing demos on the Linklight workbench it is easier to test and verify demos are always working.  Feel free re-use any component of this demo but this demo is only supported in this fashion.

#### Step 1

Connect to the Linklight workbench:

```
[user@RHEL ~]$ ssh student1@X.X.X.X
student1@X.X.X.X's password:
```

Move into the `demos/servicenow` directory.

```
[student1@ansible ~]$
[student1@ansible ~]$ cd demos/servicenow
```


#### Step 2

Define the login information (username, password and instance) as defined in the [Setup](#setup).  Fill this information out in `login_info.yml` with your text editor of choice.

```
[student1@ansible ~]$ nano login_info.yml
```

#### Step 3

Run the `config_drift.yml` playbook:

```
[student1@ansible ~]$ ansible-playbook config_drift.yml
```
