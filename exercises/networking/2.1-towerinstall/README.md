# Exercise 2.1 - Installing Ansible Tower

In this exercise, we are going to get Ansible Tower installed on your control node

## Step 1: ssh into your control node

```bash
ssh <username>@<IP of control node>
```

## Step 2: Change directories to /tmp

```bash
cd /tmp
```

## Step 3: Download the latest Ansible Tower package

```bash
curl -O https://releases.ansible.com/ansible-tower/setup/ansible-tower-setup-latest.tar.gz
```

## Step 4: Untar and unzip the package file

```bash
tar xvfz /tmp/ansible-tower-setup-latest.tar.gz
```

## Step 5: Change directories into the ansible tower package

```bash
cd /tmp/ansible-tower-setup-*
```

## Step 6: Using an editor of your choice, open the inventory file

```bash
vim inventory
```

## Step 7: fill a few variables out in an inventory file: `admin_password`, `rabbitmq_password`, `pg_password`

```yml
[tower]
localhost ansible_connection=local

[database]

[all:vars]
admin_password='ansibleWS'

pg_host=''
pg_port=''

pg_database='awx'
pg_username='awx'
pg_password='ansibleWS'

rabbitmq_port=5672
rabbitmq_vhost=tower
rabbitmq_username=tower
rabbitmq_password='ansibleWS'
rabbitmq_cookie=cookiemonster

# Needs to be true for fqdns and ip addresses
rabbitmq_use_long_name=false
```

## Step 8: run the Ansible Tower setup script

```bash
sudo ./setup.sh
```
Step 8 will take approx. 10-15 minutes to complete. This may be a good time to take a break.

## End Result

At this point, your Ansible Tower installation should be complete. You can access Tower at https://<IP-of-your-control-node>;

You know you were successful if you are able to browse to your Ansible Tower’s url (control node’s IP address) and get something like this

![Figure 1: Ansible Tower Login Screen](tower.png)

 ---
[Click Here to return to the Ansible Linklight - Networking Workshop](../README.md)
