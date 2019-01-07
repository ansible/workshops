---
name: 🐛 Bug report
about: Create a report to help us quickly resolve your issue
---
<!--- Verify first that your issue is not already reported on GitHub -->
<!--- Also test if the latest release is affected too -->
<!--- Complete *all* sections as described, this form is processed automatically -->

##### SUMMARY
<!--- Explain the problem briefly below -->

##### ISSUE TYPE
<!--- Pick one below and delete the rest -->
 - Bug Report

##### EXTRA VARS FILE
<!--- Paste verbatim output of cat vars.yml (the extra vars file used to provision the workshop)  -->
```paste below

```

e.g. here is an example of an extra vars file we are looking for:
```
$ cat ~/Github/linklight/provisioner/seans_workshop.yml
---
ec2_region: us-east-1
ec2_name_prefix: seantest
student_total: 25
admin_password: ansible
create_login_page: true
```
for more information on the extra vars file please refer to: https://github.com/network-automation/linklight/blob/master/provisioner/README.md

##### ANSIBLE VERSION
<!--- Paste verbatim output from "ansible --version" between quotes -->
```paste below

```

##### CONFIGURATION
<!--- Paste verbatim output from "ansible-config dump --only-changed" between quotes -->
```paste below

```

##### OS / ENVIRONMENT
<!---  Are you running from RHEL, Ubuntu, MacOS?  Provide details here. -->

##### TOWER
<!---  Is this provisioning happening from Tower or Engine? -->
<!---  Please attempt from Engine if Tower does not work and provide details here -->

##### PLAYBOOK SHORT OUTPUT
<!---  Please paste task that is failing -->

```paste below

```

##### PLAYBOOK LONG OUTPUT
<!--- Paste verbatim output from "ansible-playbook provision_lab.yml -e @extra_vars.yml" between quotes -->
```paste below

```
