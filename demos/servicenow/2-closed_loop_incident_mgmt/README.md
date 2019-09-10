# Ansible + ServiceNow - Closed Loop Incident Management

For a short video overview of this demonstration please refer to this YouTube video: [https://youtu.be/TkXRj4w2G2Y](https://youtu.be/TkXRj4w2G2Y)

# Objective

Demonstrate a closed loop incident management scenario.

1. Check devices for compliance.  When a device does not meet compliance requirements, a ServiceNow ticket with relevant information will be created.
2. The ticketing system has business logic to automatically fix bespoke incidents - in this case, a device that is out of compliance should be brought into compliance. ServiceNow will call out to Tower to use automation and fix the incident.
3. The Ansible Tower automation job will bring the device into compliance and then reach out to ServiceNow to resolve and close out the ticket

Thus a BSS (Business Services System) is able to maintain a statement of record while automatically fixing incidents at the same time.


## Table of Contents

- [Step 1 - Connect to workbench](#step-1---connect-to-workbench)
- [Step 2 - Provide ServiceNow credentials](#step-2---provide-servicenow-credentials)
- [Step 3 - Run demo setup playbook](#step-3---run-demo-setup-playbook)

- [Explanation](#explanation)

## Step 1 - Connect to workbench

Connect to the workshop workbench:

```
[user@RHEL ~]$ ssh student1@student1.workshop.rhdemo.io
student1@student1.workshop.rhdemo.io's password:

```

Move into the `demos/servicenow/1-config-drift` directory.

```
[student1@ansible ~]$
[student1@ansible ~]$ cd ~/demos/servicenow/2-closed_loop_incident_mgmt
```


## Step 2 - Provide ServiceNow credentials

Define the login information (username, password and instance) as defined in the [Common Setup](../README.md).  Fill this information out in `login_info.yml` with your text editor of choice.

```
[student1@ansible ~]$ nano login_info.yml
```

## Step 3 - Run demo setup playbook

Run the `demo_setup.yml` playbook as follows. This will create the necessary job templates for the demo in your tower instance:

```
[student1@ansible closed_loop_incident_mgmt]$ ansible-playbook demo_setup.yml
```

After this step, log into your tower instance and verify that the 2 "SNOW" job templates are present:

![relevant job template picture](../images/job_templates.png)

## Step 5

> *Extremely important: Make sure you use FQDNs that have valid SSL certs for the demo to work*

Navigate to the API URI (api/v2/job_templates/) of your tower instance. For example: https://student1.snow-demo.redhatgov.io/api/v2/job_templates/ and identify the API endpoint for the **SNOW-Demo-Compliance-Fix** job template.

For example, it is https://student1.snow-demo.redhatgov.io/api/v2/job_templates/8 in my instance.

Adding a "launch" URI will make this template executable remotely. Record this URL endpoint as we will need it in a further step. For example: https://student1.snow-demo.redhatgov.io/api/v2/job_templates/8/launch



## Step 5
Now, in your servicenow instance, navigate to **System Web Services >> Outbound >> REST Message**

> You can also use the search bar at the top left and search for "rest message"

![](../images/restmsg.png)


  - Click on *New* at the top of the page:
    ![](../images/newrest.png)

  - Give it a name and set the endpoint to the URL we captured in the previous step.
  - Under the *Authentication* tab, chose "Basic" Authentication type.
  - For the Basic auth profile, click on the search bar. This will open yet another window. Click on new and add your Tower instance' login information
  ![](../images/rest_setup1.png)  
  - Click Submit
  - Click again on the REST message you just created and add a new HTTP method
  ![](../images/rest_setup3.png)
  - Give it a name, select **POST** and add the same end-point
  ![](../images/rest_setup4.png)
  - Click on the *HTTP Request* Tab. Under the "HTTP Headers" add a new HTTP header with the name "Content-Type" and value "application/json"
  - At the bottom, in the "Content" area, add the following"
  ```json
  {"extra_vars": {
 "incident_num": "${INC}" } }
 ```
 ![](../images/rest_setup5.png)
 > The extra_vars is how the Service Now API is going to pass the incident number information to the Tower instance
  - Click on the *Auto-generate variable* link
  ![](../images/rest_setup6.png)

  - Click the *Preview Script Usage* link at the bottom and copy the contents.
  ![](../images/rest_setup7.png)

  ```javascript
   try {
 var r = new sn_ws.RESTMessageV2('Tower Job to fix compliance issues', 'Launch compliance fix');
 r.setStringParameterNoEscape('INC', '');

//override authentication profile
//authentication type ='basic'/ 'oauth2'
//r.setAuthentication(authentication type, profile name);

//set a MID server name if one wants to run the message on MID
//r.setMIDServer('MY_MID_SERVER');

//if the message is configured to communicate through ECC queue, either
//by setting a MID server or calling executeAsync, one needs to set skip_sensor
//to true. Otherwise, one may get an intermittent error that the response body is null
//r.setEccParameter('skip_sensor', true);

 var response = r.execute();
 var responseBody = response.getBody();
 var httpStatus = response.getStatusCode();
}
catch(ex) {
 var message = ex.message;
}

```


  - Click submit


## Step 6

 - Navigate to **System Definition >> Business Rules** and click on *New* to add a new business rule
 ![](../images/business_rule1.png)
 > For this demo, the bespoke incident type that should be automatically fixed is router login banner compliance. So the rule is looking for a new *incident* ticket whose description contains banner.
 - Click on the *Advanced* checkbox to enable the *Advanced* Tab
 ![](../images/business_rule2.png)
 > NOTE: Ensure that the Business rule is run **after** the ticket is inserted into the incidents table (see screencap above for all dropdowns and checkboxes)


** If you have used the exact naming conventions in this README, you can copy and paste the following into the *Advanced* tab.**

```javascript
(function executeRule(current, previous /*null when async*/) {

    try {
 var r = new sn_ws.RESTMessageV2('Tower Job to fix compliance issues', 'Launch compliance fix');
 r.setStringParameterNoEscape('INC', current.number);

 var response = r.execute();
 var responseBody = response.getBody();
 var httpStatus = response.getStatusCode();
 current.comments = "Contacting Ansible Tower to fix bespoke incident";
 current.state = '2';
 current.update();
}
catch(ex) {
 var message = ex.message;
}

})(current, previous);
```
 ![](../images/business_rule4.png)

- Click "Submit"


# Running the Demo

Reminder, for a short video overview of this demonstration please refer to this YouTube video: [https://youtu.be/TkXRj4w2G2Y](https://youtu.be/TkXRj4w2G2Y)


## Step 1

Ensure that the router does not have a current banner (required condition for the device to be out of compliance:


```
[student1@ansible]$ ssh rtr1


rtr1#


```

> If there is an existing banner you can use  the `no banner login` command in config mode to remove it


## Step 2
Log into the Tower instance and launch the "SNOW-Demo-Compliance-Check" Template

>Observe the following 2 tasks as that template runs

```
TASK [CREATE AN INCIDENT] ******************************************************
changed: [rtr1 -> localhost]

TASK [VISUAL OUTPUT OF INCIDENT NUMBER] ****************************************
ok: [rtr1] => {
    "snow_var.record.number": "INC0010034"
}

```


## Step 3

Switch over to the ServiceNow instance and see that the ticket number as see in the previous output has been created.

![](../images/incident_1.png)


## Step 4

Switch back to the Ansible Tower Jobs and click on the "SNOW-Demo-Compliance-Fix" Job

>Observe that after sleeping for 180s, the job will fix the issue on the router, resolve and close out the ticket

```
TASK [sleep for 180 seconds and continue with play] ****************************
ok: [rtr1 -> localhost]
TASK [CONFIGURE THE LOGIN BANNER] **********************************************
changed: [rtr1]
TASK [MARK THE TICKET AS RESOLVED] *********************************************
changed: [rtr1]
TASK [MARK THE TICKET AS CLOSED] ***********************************************
changed: [rtr1]

```

## Step 5
Log back into the router and see that you are greeted with the new banner:




```
[student1@ansible servicenow]$ ssh rtr1

DEMO BANNER FOR DEVICE rtr1


rtr1#

```

## Step 6
Finally log back into servicenow to notice the history of the ticket
![](../images/incident_2.png)
