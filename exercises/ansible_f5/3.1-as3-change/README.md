# Exercise 3.1 - Operational Change with AS3

**Read this in other languages**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
- [Playbook Output](#playbook-output)
- [Solution](#solution)

# Objective

Demonstrate changing an existing Web Application AS3 template.  There is a problem with the existing template, the serviceMain is showing red.  What is wrong?  
![serviceMain-offline.png](serviceMain-offline.png)


# Guide

## Step 1:

Figure out what is wrong.  Login to the F5 with your web browser to see what was configured.

  1. Click on `ServiceMain` to see why its down.
  2. Look at the `Availability` field in the table.

![pool-nodes-down.png](pool-nodes-down.png)

  3. Click on the `Pools` under `Local Traffic`
  4. Click on `app_pool`
  5. Click on the `Members` button

![443](443.png)

The port **443** is incorrect.  The two RHEL web servers are only running on port 80.  This is why they are showing down.

## Step 2:

Using your text editor of choice open the existing jinja template `as3_template.j2`:

>`vim` and `nano` are available on the control node, as well as Visual Studio and Atom via RDP

## Step 3:

Find where the port **443** is and modify it to port **80**.

The line looks as follows->
{% raw %}
``` json
                "servicePort": 443,
```
{% endraw %}

change it to->

{% raw %}
``` json
                "servicePort": 80,
```
{% endraw %}

## Step 4
Run the playbook - exit back into the command line of the control host and execute the following:

```
[student1@ansible ~]$ ansible-playbook as3.yml
```

# Playbook Output

The output will look as follows.

{% raw %}
```yaml
[student1@ansible ~]$ ansible-playbook as3.yml

PLAY [Linklight AS3] ***********************************************************

TASK [Create AS3 JSON Body] ****************************************************
ok: [f5]

TASK [Push AS3] ****************************************************************
ok: [f5 -> localhost]

PLAY RECAP *********************************************************************
f5                         : ok=2    changed=0    unreachable=0    failed=0
```
{% endraw %}

# Solution

The fixed Jinja template is provided here for an Answer key.  Click here: [as3_template.j2](https://github.com/network-automation/linklight/blob/master/exercises/ansible_f5/3.1-as3-change/j2/as3_template.j2).

# Verifying the Solution

Login to the F5 with your web browser to see what was configured.  Grab the IP information for the F5 load balancer from the lab_inventory/hosts file, and type it in like so: https://X.X.X.X:8443/

![f5 gui as3](as3-fix.gif)

1. Click on the Local Traffic on the lefthand menu
2. Click on Virtual Servers.
3. On the top right, click on the drop down menu titled `Partition` and select WorkshopExample
4. The Virtual Server `serviceMain` will be displayed.
5. This time it will be Green (`Available (Enabled) - The virtual server is available`)
6. Verify under `Pools` for `app_pool` that both web servers are set to port **80** for their `service_port`

----

You have finished this exercise.  [Click here to return to the lab guide](../README.md)
