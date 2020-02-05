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

| Key         | Value                                        | Note |
|-------------|----------------------------------------------|------|
| Name        | IIS Basic Job Template                       |      |
| Description | Template for the iis-basic playbook          |      |
| JOB TYPE    | Run                                          |      |
| INVENTORY   | Windows Workshop Inventory                   |      |
| PROJECT     | Ansible Workshop Project                     |      |
| PLAYBOOK    | `iis-basic/install_iis.yml`                  |      |
| CREDENTIAL  | Type: **Machine**. Name: **Student Account** |      |
| LIMIT       | windows                                      |      |
| OPTIONS     | [*] ENABLE FACT CACHE                        |      |

![Create Job Template](images/4-create-job-template.png)

Step 4:
-------

Click SAVE ![Save](images/at_save.png) and then select ADD SURVEY
![Add](images/at_add_survey.png)

Step 5:
-------

Complete the survey form with following values

| Key                    | Value                                                      | Note             |
|------------------------|------------------------------------------------------------|------------------|
| PROMPT                 | Please enter a test message for your new website           |                  |
| DESCRIPTION            | Website test message prompt                                |                  |
| ANSWER VARIABLE NAME   | `iis_test_message`                                         |                  |
| ANSWER TYPE            | Text                                                       |                  |
| MINIMUM/MAXIMUM LENGTH |                                                            | Use the defaults |
| DEFAULT ANSWER         | *Be creative, keep it clean, we’re all professionals here* |                  |

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

Select LAUNCH ![SurveyL](images/4-survey-launch.png)

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

When the job has successfully completed, you should see a URL to your website printed at the bottom of the job output.

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
