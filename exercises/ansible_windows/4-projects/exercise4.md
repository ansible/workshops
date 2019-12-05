A job template is a definition and set of parameters for running an
Ansible job. Job templates are useful to execute the same job many
times.

Syncing your Project
====================

Before you can create a job template with a new playbook, you must first
sync your Project so that Tower knows about it. To do this, click
**Projects** and then click the sync icon next to your project. Once
this is complete, you can create the job template.

![Project Sync](images/4-project-sync.png)

Creating a Job Template
=======================

Step 1:
-------

Select **Templates**

Step 2:
-------

Click the ![Add](images/add.png) icon, and select Job Template

Step 3:
-------

Complete the form using the following values

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p>NAME</p></td>
<td><p>IIS Basic Job Template</p></td>
</tr>
<tr class="even">
<td><p>DESCRIPTION</p></td>
<td><p>Template for the iis-basic-playbook</p></td>
</tr>
<tr class="odd">
<td><p>JOB TYPE</p></td>
<td><p>Run</p></td>
</tr>
<tr class="even">
<td><p>INVENTORY</p></td>
<td><p>Ansible Workshop Inventory</p></td>
</tr>
<tr class="odd">
<td><p>PROJECT</p></td>
<td><p>Ansible Workshop Project</p></td>
</tr>
<tr class="even">
<td><p>PLAYBOOK</p></td>
<td><p>iis-basic/install_iis.yml</p></td>
</tr>
<tr class="odd">
<td><p>CREDENTIAL</p></td>
<td><p>Type: <strong>Machine</strong>. Name: Student Account</p></td>
</tr>
<tr class="even">
<td><p>LIMIT</p></td>
<td><p>Windows</p></td>
</tr>
<tr class="odd">
<td><p>OPTIONS</p></td>
<td><ul>
<li><p>[*] USE FACT CACHE</p></li>
</ul></td>
</tr>
</tbody>
</table>

![Create Job Template](images/4-create-job-template.png)

Step 4:
-------

Click SAVE ![Save](images/at_save.png) and then select ADD SURVEY
![Add](images/at_add_survey.png)

Step 5:
-------

Complete the survey form with following values

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p>PROMPT</p></td>
<td><p>Please enter a test message for your new website</p></td>
</tr>
<tr class="even">
<td><p>DESCRIPTION</p></td>
<td><p>Website test message prompt</p></td>
</tr>
<tr class="odd">
<td><p>ANSWER VARIABLE NAME</p></td>
<td><p>iis_test_message</p></td>
</tr>
<tr class="even">
<td><p>ANSWER TYPE</p></td>
<td><p>Text</p></td>
</tr>
<tr class="odd">
<td><p>MINIMUM/MAXIMUM LENGTH</p></td>
<td><p>Use the defaults</p></td>
</tr>
<tr class="even">
<td><p>DEFAULT ANSWER</p></td>
<td><p><em>Be creative, keep it clean, we’re all professionals here</em></p></td>
</tr>
</tbody>
</table>

![Survey Form](images/4-survey.png)

Step 6:
-------

Select ADD ![Add](images/at_add.png)

Step 7:
-------

Select SAVE ![Add](images/at_save.png)

Step 8:
-------

Back on the main Job Template page, select SAVE
![Add](images/at_save.png) again.

Running a Job Template
======================

Now that you’ve successfully created your Job Template, you are ready to
launch it. Once you do, you will be redirected to a job screen which is
refreshing in real time showing you the status of the job.

Step 1:
-------

Select TEMPLATES

> **Note**
>
> Alternatively, if you haven’t navigated away from the job templates
> creation page, you can scroll down to see all existing job templates

Step 2:
-------

Click the rocketship icon ![Add](images/at_launch_icon.png) for the
**IIS Basic Job Template**

Step 3:
-------

When prompted, enter your desired test message

![Survey Prompt](images/4-survey-prompt.png)

Step 4:
-------

Select **NEXT** and preview the inputs.

Step 5:
-------

Select LAUNCH ![SurveyL](images/at_survey_launch.png)

Step 6:
-------

Sit back, watch the magic happen

One of the first things you will notice is the summary section. This
gives you details about your job such as who launched it, what playbook
it’s running, what the status is, i.e. pending, running, or complete.

![Job Summary](images/4-job-summary-details.png)

Next you will be able to see details on the play and each task in the
playbook.

![Play and Task Output](images/4-job-summary-output.png)

Step 7:
-------

Once your job is successful, navigate to your new website (replace \#
with your student number)

    http://s#-win1.ansibleworkshop.com

If all went well, you should see something like this, but with your own
custom message of course.

![New Website with Personalized Test
Message](images/4-website-output.png)

Extra Credit
============

Now that you have IIS Installed, create a new playbook called
*remove\_iis.yml* to stop and remove IIS.

**Hint:** First stop the `W3Svc` service using the `win_service` module,
then delete the `Web-Server` service using the `win_feature` module.
Optionally, use the `win_file` module to delete the index page.

End Result
==========

At this point in the workshop, you’ve experienced the core functionality
of Ansible Tower. But wait… there’s more! You’ve just begun to explore
the possibilities of Ansible Tower. The next few lessons will help you
move beyond a basic playbook.
