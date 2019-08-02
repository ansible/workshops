## Step 5

To understand where the Playbooks are that we imported via the Project, return to the command line of the control node.  Switch to the **awx** user.

```
sudo su - awx
```

You have now switched to the awx user, perform an ls to see what files are in here.

```
-bash-4.2$ ls
beat.db  favicon.ico  job_status  projects  public  uwsgi.stats  venv  wsgi.py
```

There is a **projects** folder here that directly corresponds to the Projects link in Ansible Tower.  Move into the projects directory to see what is available.

```
-bash-4.2$ cd projects/
-bash-4.2$ ls
_10__workshop_project  _10__workshop_project.lock
-bash-4.2$ cd _10__workshop_project
```

The number might not match exactly here, but the **workshop_project** directly corresponds to our WorkShop Project we created in the previous exercise.

Perform an ls -la to look at one files are available in this directory.

```
-bash-4.2$ ls -la
total 44
drwxr-xr-x. 9 awx awx 4096 Jan 22 19:27 .
drwxr-x---. 3 awx awx   69 Jan 22 19:33 ..
-rw-r--r--. 1 awx awx  652 Jan 22 15:45 ansible.cfg
drwxr-xr-x. 4 awx awx   33 Jan 22 18:41 eos
drwxr-xr-x. 8 awx awx  198 Jan 22 19:27 .git
drwxr-xr-x. 2 awx awx   21 Jan 22 15:45 group_vars
drwxr-xr-x. 4 awx awx   33 Jan 22 18:37 ios
drwxr-xr-x. 4 awx awx   33 Jan 22 18:49 junos
-rw-r--r--. 1 awx awx 2535 Jan 22 19:27 network_backup.yml
-rw-r--r--. 1 awx awx  247 Jan 22 15:45 network_banner.yml
-rw-r--r--. 1 awx awx  252 Jan 22 15:45 network_l3_interface.yml
-rw-r--r--. 1 awx awx  250 Jan 22 15:45 network_restore.yml
drwxr-xr-x. 2 awx awx   96 Jan 22 15:45 network_setup
-rw-r--r--. 1 awx awx  543 Jan 22 15:45 network_system.yml
-rw-r--r--. 1 awx awx  609 Jan 22 15:45 network_time.yml
-rw-r--r--. 1 awx awx  272 Jan 22 15:45 network_user.yml
-rw-r--r--. 1 awx awx  297 Jan 22 15:45 README.md
-rw-r--r--. 1 awx awx  712 Jan 22 15:45 sample-vars-auto.yml
drwxr-xr-x. 2 awx awx  103 Jan 22 15:45 templates
```

The Playbooks (shown as .yml files) should directly correspond to the Github repo: https://github.com/network-automation/tower_workshop
