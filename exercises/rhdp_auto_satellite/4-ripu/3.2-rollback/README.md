# Workshop Exercise - Run Rollback Job

## Table of Contents

- [Workshop Exercise - Run Rollback Job](#workshop-exercise---run-rollback-job)
  - [Table of Contents](#table-of-contents)
  - [Objectives](#objectives)
  - [Guide](#guide)
    - [Step 1 - Launch the Rollback Job Template](#step-1---launch-the-rollback-job-template)
    - [Step 2 - Observe the Rollback Job Output](#step-2---observe-the-rollback-job-output)
    - [Step 3 - Check the RHEL Version](#step-3---check-the-rhel-version)
  - [Conclusion](#conclusion)

## Objectives

* Demonstrate using an Ansible playbook for rolling back a RHEL upgrade
* Verify the RHEL major version is reverted back

## Guide

In this exercise, we will demonstrate rolling back the three tier application stack servers, just as we would if the RHEL upgrade had failed or if we had found that the upgrade caused unexpected impacts to the application.

We are now in the rollback phase of our exploration of the RHEL in-place automation workflow:

![Automation approach workflow diagram with rollback playbook highlighted](images/ripu-workflow-hl-rollback.svg)

After rolling back, the three tier application stack will be restored to as it was just before entering the upgrade phase of the workflow.

### Step 1 - Launch the Rollback Job Template

In this step, we will be rolling back the RHEL in-place upgrade for our entire three tier application server stack.

> **Note**
>
> In this case, only one of our nodes has an issue. Depending on overall thoughts on how to best proceed, an argument could be made for just rolling back the tomcat application node, node2, and leave node1 and node3 as they are. However, in this case, we are going to demonstrate the ability to simulataneously roll back an entire application stack of systems at once.

- Return to the AAP Web UI tab in your web browser. Navigate to Resources > Templates and then open the "LEAPP / 03 Rollback" job template. Here is what it looks like:

  ![AAP Web UI showing the rollback job template details view](images/rollback_template.png)

- Click the "Launch" button which will bring up the prompts for submitting the workflow starting with the limit prompt. We want to do a rollback of the entire three tier application stack. To do this, we will not enter any values into the "Limit" prompt.

  ![AAP Web UI showing the rollback job limit prompt](images/rollback_prompts.png)

  Click the "Next" button to proceed.

  ![AAP Web UI showing the rollback job survey prompt](images/rollback_survey.png)

- Next we see the job template survey prompt asking us to select an inventory group. Our systems were upgraded to RHEL8 and we looked in Satellite and verified that the nodes were in fact registered as RHEL8 nodes, configured to consume the RHEL8_Dev content view. So, we should choose "RHEL8_Dev" for our inventory group, yes? Actually, no. We have not _committed_ to keeping the upgraded systems, our system tags that define the current OS and content view have not been updated...so the Ansible inventory still recognizes these systems as members of the "RHEL7_Dev" inventory group. So if we have not initiated the commit automation to accept the converted systems as RHEL8_Dev nodes, we choose the "RHEL7_Dev" option and click the "Next" button.

  ![AAP Web UI showing the rollback job preview prompt](images/rollback_preview.png)

  If everything looks good, use the "Launch" button to start the playbook job.

### Step 2 - Observe the Rollback Job Output

After launching the rollback workflow job, the AAP Web UI will navigate automatically to the workflow output visualizer page.

  ![Rollback workflow job visualizer](images/rollback_workflow_job_visual.png)

- The automated rollback takes only a few minutes to run. You can monitor the log output as the playbook run progresses by clicking directly on the "UTILITY / Snapshot Instance" node in the workflow visualizer.

- When all of the workflow job nodes have completed (green check mark), if you haven't done so already, click on the "UTILITY / Snapshot Instance" node in the workflow visualizer. Once the "UTILITY / Snapshot Instance" job details displays, click on the "Output" tab and scroll to the bottom of the job output. If it finished successfully, you should see "failed=0" status for each node in the job summary, like this example:

  ![Rollback job "PLAY RECAP" as seen at the end of the job output](images/rollback_job_recap.png)

  Notice in the example above, we see the job completed in aproximately four minutes. However, most of that time was spent in the final "Wait for the snapshot to drain" task which holds the job until the snapshot merges finish in the background. The instance was actually rolled back and service ready in just under a minute. Impressive, right?

### Step 3 - Check the RHEL Version

Repeat the steps you followed with [Exercise 2.3: Step 2](../2.3-check-upg/README.md#step-2---verify-the-hosts-are-upgraded-to-next-rhel-version), this time to verify that the RHEL version is reverted back.

- For example, if the three tier host you rolled back had been upgraded from RHEL7 to RHEL8, you should now see it is back to RHEL7:

  ![command output showing the host is back to RHEL7 installed](images/commands_after_rollback.png)

- Additionally, we can check Satellite to verify node status. Switching to the Satellite UI in your brwoser, hover over "Hosts" in the left hand menu and then click on "Content Hosts":

  ![Satellite Content Hosts showing RHEL7](images/rollback_satellite_content_hosts.png)

We can see that the three tier application stack nodes are all reverted to RHEL7 and set to utilize the RHEL7_Dev content view

## Conclusion

In this exercise, we used automation to quickly reverse the RHEL in-place upgrade and restore the three tier application stack servers back to their original state.

In the next exercise, we'll dig deeper to validate that all changes and impacts caused by the upgrade are now undone.

---

**Navigation**

[Previous Exercise](../3.1-rm-rf/README.md) - [Next Exercise](../3.3-check-undo/README.md)

[Home](../README.md)