# Intro

In this section, you will only be given a summary of the objects you need to create along with some screenshots of a controller that is configured with the completed code. You will also be provided the variables sections from the readme's for each of the required roles to help you complete this task.

## Step 1

If you made it this far, Congratulations! Workflows work much the same as job templates when creating their definition with the addition of the schema to create the nodes and links. It is suggested to link the controller and hub configuration job templates and link them together for this exercise.

Create a file `group_vars/all/workflows.yml` and add the required information to the list `controller_workflows` to configure the UI to look like the screenshot

```yaml
---
controller_workflows:

...
```

Further documentation for those who are interested to learn more see:

- [Workflow Job Template role](https://github.com/redhat-cop/controller_configuration/blob/devel/roles/workflow_job_templates/README.md)

[previous task](task3.md)

You have finished this exercise. [Click here to return to the lab guide](../README.md)
