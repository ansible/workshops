## Playbook 2 - host-routes.yml
A playbook for configuring static routes on Linux hosts.

What you will learn:
 - lineinfile module
 - handlers

 ---

### Step 1: Defining the Play

Let’s create our 2nd playbook and name it `host-routes.yml`

```bash
vim host-routes.yml
```

For our 2nd playbook we need to add a routes from VPC-1 (172.16.0.0/16) to VPC-2 (172.17.0.0/16) and vice versa.  For this exercise we will also illustrate handlers.

We need two routes:
 - From the `ansible` control node to `rtr1` for the `172.17.0.0/16` subnet
 - From the `host1` node to `rtr2` for the 172.16.0.0/16 subnet

For this playbook we will be running only on the `ansible` and `host1` nodes.  Start off the playbook like the backup.yml but make sure to remove `connection:local`.  Lets call this playbook `host-routes.yml` since we are adding static routes on the two hosts.
```yml
---
- name: add route on ansible
  hosts: ansible
  gather_facts: no
  become: yes
```

The `ansible` host is running Red Hat Enterprise Linux Server.  To add a static route we just need to add a line using the [Ansible lineinfile module](http://docs.ansible.com/ansible/latest/lineinfile_module.html) with the subnet and destination under `/etc/sysconfig/network-scripts/route-eth0`.  The ```create: yes``` will create the file if its not already created.  We will also use `notify: "restart network"` to run a handler if this file changes.

### Step 2: Adding tasks
{% raw %}
```yml
  tasks:
    - name: add route to 172.17.0.0/16 subnet on ansible node
      lineinfile:
        path: /etc/sysconfig/network-scripts/route-eth0
        line: "172.17.0.0/16 via {{hostvars['rtr1']['private_ip']}}"
        create: yes
      notify: "restart network"
```
{% endraw %}
Next we need to create a handler to restart networking if routes are changed.  The name matters and must match what we are notifying in the task displayed above.  In this case it has to be `restart network` but is user defined and as long as it matches the handler will be run.

### Step 3: Adding a handler

```yml
  handlers:
    - name: restart network
      systemd:
        state: restarted
        name: network
```

### Step 4: Repeat for host1

Now we need to repeat for `host1`:

{% raw %}
```yml
- name: add route on host1
  hosts: host1
  gather_facts: no
  become: yes

  tasks:
    - name: add route to 172.16.0.0/16 subnet on host1 node
      lineinfile:
        path: /etc/sysconfig/network-scripts/route-eth0
        line: "172.16.0.0/16 via {{hostvars['rtr2']['private_ip']}}"
        create: yes
      notify: "restart network"

  handlers:
    - name: restart network
      systemd:
        state: restarted
        name: network
```
{% endraw %}

### Step 5: Run the playbook

Now run the playbook:
```bash
ansible-playbook host-routes.yml
```

# Complete
You have completed lab exercise 1.2

# Answer Key
- For backup.yml [click here](https://github.com/network-automation/linklight/blob/master/exercises/networking/1.2-backup/backup.yml).
- For host-routes.yml [click here](https://github.com/network-automation/linklight/blob/master/exercises/networking/1.2-backup/host-routes.yml)
