# Configuration as Code for Ansible Automation Platform 2 Technical Workshop

> **IMPORTANT TO NOTE**
>
> This is the 4 hour workshop.
>


Welcome to our interactive lab on using Configuration as code to configure the Ansible Automation Platrom.

Configuration as Code (CasC) is a software development practice that treats infrastructure configurations as code. This approach allows you to version control, track changes, and automate the deployment of your infrastructure configurations. With CasC, your configuration files or scripts serve as the single source of truth for your infrastructure setup. Any changes should be made through this mechanism, avoiding direct changes in the Ansible Automation Platform (AAP) UI.
Benefits of CasC
By adopting a Configuration as Code approach, you can enjoy numerous benefits, including:

* Version Control : Track changes and collaborate with team members.
* Consistency : Ensure consistent configurations across different environments.
* Repeatability : Repeat the same configuration setup multiple times.
* Automated Deployment : Automate deployment to different environments.
* Auditing and Compliance : Track who made changes, when, and what was changed.

== Lab structure

In this lab, we will demonstrate how to use Configuration as Code to configure various aspects of the Ansible Automation Platform (AAP). This includes:

* First, We will setup the basics for configuring the Automation Platform.

* Next we will Create some credentials, inventories, and job templates and everything that is needed to create them.

* Next we will configure the Hub to load in more content.

* We will then build an execution environment to be used on the platform.

* Finally for extra credit, a workflow can be created from scratch.

By following this lab, you will learn how to use CasC to maintain a consistent and repeatable infrastructure configuration across different environments. This approach will help prevent drift in configuration, require approval before implementation, and ensure that both development and production deployments are well-maintained.

Automation controller before, a recomended place to start is this instruct lab, if you have not done so before:
[Introduction to automation controller](https://developers.redhat.com/content-gateway/link/3884764)

# Agenda

Recommended agenda for when there is an instructor teaching.

<table>
<tbody>
<tr>
<td><b>Part 1</b>: Creating the Basics for configuring the Automation Platform</td>
<td>⏱️ 40 minutes</td>
</tr>
<tr>
<td><b>Part 2</b>: Creating credentials, inventories, and job templates and everything that is needed to create them.</td>
<td>⏱️ 40 minutes</td>
</tr>
<tr>
<td><b>Part 3</b>: Configuring the Automation hub to load more content</td>
<td>⏱️ 30 minutes</td>
</tr>
<tr>
<td><b>Part 4</b>: Build an execution environment to be used on the platform.</td>
<td>⏱️ 40 minutes</td>
</tr>
<tr>
<td><b>Part 4</b>: Creating an Automation controller Workflow in code</td>
<td>⏱️ 90 minutes</td>
</tr>
</tbody>
</table>

**Total Time**: 4 hours (249 minutes)

## Lab Index

<table>
<thead>
<tr>
<th>Lab Title</th>
<th>Description</th>
<th>Link</th>
</tr>
</thead>
<tbody>
<tr>
<td>Config as code Introduction to AAP</td>
<td>Learn about the fundamentals of using Configuration of Code to maintain the Ansible Automation Platform. This is a Red Hat or Partner Only Lab, and requires access to demo.redhat.com, please reach out to your account representative to coordinate access to the Lab</td>
<td><a target="_new" href="https://catalog.demo.redhat.com/catalog?item=babylon-catalog-prod/summit-2025.lb2193-config-as-code-aap.prod&utm_source=webapp&utm_medium=share-link">🚀 Launch Lab</a></td>
</tr>
</tbody>
</table>

# Going Further

Additional material for Configuration as Code for Ansible Automation Platform 2

<table>
<thead>
<tr>
<th>Title</th>
<th>Type</th>
<th>Link</th>
</tr>
</thead>
<tbody>
<tr>
<td>Demystifying Ansible Automation Platform</td>
<td>Book</td>
<td><a target="_new" href="https://www.packtpub.com/product/demystifying-ansible-automation-platform/9781803244884">📖 Demystifying Ansible Automation Platform - Book from Packt</a></td>
</tr>
<tr>
<td>Infra Collections in Ansible Galaxy</td>
<td>Collections</td>
<td><a targete="_new" href="https://galaxy.ansible.com/ui/namespaces/infra/">📒 Download collections used in this lab and get links to their repos</a></td>
</tr>
</tbody>
</table>

# Ansible Workshop

This is an official Ansible Workshop

This workshop is maintained by the [Infra Config as Code Volunteers](https://forum.ansible.com/tag/infra-config-as-code)
Please open an [issues on Github](https://github.com/ansible/instruqt/issues/new?title=New+eda+workshop+issue&body=)


![ansible workshop logo](https://github.com/ansible/workshops/blob/devel/images/Ansible-Workshop-Logo.png?raw=true)
