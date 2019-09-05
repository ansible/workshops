# CHATOPS DEMO

The objective of this demo is to familiarize the network engineer with integrating a chat tool like "Slack" as an interface to the managed network devices.

**AUDIENCE**: Network engineers/systems engineers trying to integrate slack into their day-to-day operations to manage end devices

**USE CASE**: The scenario for this demo is as follows :-

    1. Network engineer gets a ticket from her customer requesting to open TCP/UDP/IP traffic from source IP (A) to destination IP (B) on some destination port X.

    2. The first step in the manual process is for the network engineer to crawl through devices in the path between A and B and check whether the traffic is already permitted.

    3. Allow/Disallow the traffic per IT policy

In particular, we will use Ansible and Slack to automate step 2 via this demo.


## General workflow

1. Demo user will enter a custom `/` "slash" command in slack

2. This will prompt the user with a form to enter IP address A/B and port X as described above

3. When the form is submitted, it will kick off an Ansible tower job that will go and parse the access lists on the configured routers

4. A final report is presented back to the demo user


## Pre-requisites

1. The [Linklight Network Workshop V2](https://github.com/network-automation/linklight/blob/master/exercises/networking_v2/README.md) has been provisioned

2. Tower has been licensed [(See setup instructions)](https://github.com/network-automation/linklight/tree/master/provisioner#setup-per-workshop)

3. Already have an account in a slack team with permission to create a channel and add an app.


### STEP 1: Create a slack channel

From the slack chat client or browser side bar, add a new slack channel to start building this demo:

![](./images/create_channel1.png)

![](./images/create_channel2.png)


### STEP 2: Register/Create a new Slack App

1. Navigate to https://api.slack.com/new and click on Build New

![](./images/create_bot1.png)

Give the app a meaningful name and add it to the slack team/workspace you have access to. In the above image, I've created the app called "ansibot" to the "ansiblenetwork" workspace.

2. Slack uses "slash" commands to identify special words to act on. Create a slash command we will be using to invoke our Ansible Tower job

![](./images/create_slashcmd2.png)

3. On clicking create you will be presented with the options
![](./images/create_slashcmd3.png)

Use a meaningful command that makes sense to you. The "Request URL" is the application URI endpoint, to which slack will route the command. For this demo, our app will be configured to listen on port `8888`. So enter the request url with the public IP address or DNS name of your tower instance that was provisioned as per pre-requisite 2. For example: **http://34.207.200.42:8888/acls"** or **http://student11.mydemo.rhdemo.io:8888/acls**

>Note 1: The app has been written to listen on port 8888 so it is important to make sure that this step is configured correctly with the right port.

>Note 2: Note down the name of the **uri** used for the slash command. We will need this later.


### STEP 3: Interactive component

Add an "interactive component". This is the URI invoked (HTTP POST), when the form in slack is submitted.

![](./images/interactive1.png)

![](./images/interactive2.png)

Similar to the previous step, add a url that contains the public IP/DNS name of the tower instance provisioned per the pre-requisites.

>Note 1: The app server is preconfigured to listen on port 8888. Ensure that the URL is constructed with that port number. For example: http://34.207.200.32:8888/interactive or http://student11.mydemo.rhdemo.io:8888/collect-data  
>Note 2: Use a meaningful URI for the interactive component and make sure to note down the name. We will need this later.

### STEP 4: Incoming Webhook
Incoming webhooks allow the tower job to communicate back into the slack channel and post an update/report of the job completion. Create an incoming webhook and note down the full URL.

![](./images/incoming_webhook1.png)

![](./images/incoming_webhooks2.png)

![](./images/incoming_webhooks3.png)



### STEP 5: Create the bot

Next create the bot associated with this app.

![](./images/addbotuser1.png)

![](./images/addbotuser2.png)

### STEP 6: Add the app to the slack channel created in step 1

This step is done from within the slack client/browser

![](./images/add_app1.png)

![](./images/add_app2.png)

After adding the app, ensure that the slash command is now available (it shows up)

![](./images/add_app3.png)

### STEP 7: Slack App and Bot Tokens

Finally, switch back to the app configuration in the browser and collect the App and Bot tokens.

For the App verification token, navigate to the "Basic Information" link

![](./images/token.png)


For the Bot token, navigate to the "OAuth & Permissions" link

![](./images/bot_token.png)


We will need this for our Python app to communicate with the slack app/bot.


### STEP 8: Input variables

1. Over SSH, login to the tower/control node of your pod. Here, switch to the `demo_setup` directory under `demos/chatops`

``` shell
[student2@ansible ~]$ cd ~/demos/chatops/demo_setup/
[student2@ansible demo_setup]$ pwd
/home/student2/demos/chatops/demo_setup
[student2@ansible demo_setup]$
```

2. Edit/Create a file called `input_vars.yaml` and add the information collected in the previous steps into this file:

``` yaml
slash_cmd: acl   #URI used for the slash command
slack_interactive: interactive-component #URI used for interactive component
slack_token: ahSH5n4honXKwBhQpBvVQjgV
slack_bot_token: xoxb-272971091299-490099164215-wMnlZrM3zfsEbksRLJu8g64S
slack_webhook: https://hooks.slack.com/services/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
tower_hostname: 35.173.203.114
tower_username: admin  # Update this if different
tower_password: ansible # Update this if different

```
### STEP 9: Set up the demo

Finally, we will run the `update_demo.yaml` playbook to set up the Python application, install dependencies and start the application as a daemon.

``` shell
[student2@ansible demo_setup]$ ansible-playbook update_demo.yaml -e @input_vars.yaml

PLAY [UPDATE THE USER SPECIFIC CHATOPS INFO] ********************************************************************************************************************************

TASK [Gathering Facts] ******************************************************************************************************************************************************
ok: [localhost]

TASK [UPDATE CUSTOM VARIABLES - SLASH COMMAND] ******************************************************************************************************************************
ok: [localhost]

TASK [UPDATE CUSTOM VARIABLES - INTERACTIVE URI] ****************************************************************************************************************************
ok: [localhost]

TASK [UPDATE CUSTOM VARIABLES - SLACK TOKEN] ********************************************************************************************************************************
ok: [localhost]

TASK [UPDATE CUSTOM VARIABLES - SLACK BOT TOKEN] ****************************************************************************************************************************
ok: [localhost]

TASK [UPDATE CUSTOM VARIABLES - TOWER HOSTNAME] *****************************************************************************************************************************
ok: [localhost]

.
.
.
.
.
<output omitted for brevity>

```
### STEP 10: Testing the demo

At this point, the demo should be all set up to work. Test this by going to the slack channel and using the "slash" command you created.

![](./images/demo1.png )

Enter the following values to test this:

![](./images/demo2.png )

This fires of an Ansible Tower job for you!

![](./images/demo3.png)

>Note: You can verify that the job kicked off by logging into the Ansible Tower website and checking the status of the job


![](./images/demo4.png)

This playbook runs and generates a report that is then sent back to the Slack channel via the incoming webhook:


![](./images/demo5.png)


## Conclusion

Feel free to login to the routers and add additional acls entries and test them via the slack interface.
This demo shows you how flexible Ansible Tower can be for integrating with modern DevOps tools and interaction tools like Slack, allowing network administrators to literally "Chat" with their managed end points.
