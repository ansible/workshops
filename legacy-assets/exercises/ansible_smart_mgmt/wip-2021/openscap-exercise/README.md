# Integrated Management Workshop: Configuring and performing an OpenSCAP Scan

In this part of the workshop, we will learn how to configure and perform an OpenSCAP scan using playbooks in Ansible Tower with Satellite. When running multiple Red Hat Enterprise Linux systems, it's important to keep all of these systems compliant with a meaningful security policy and perform security scans remotely from a single location. OpenSCAP is an open source project that is used by government agencies, corporations, as well as e-commerce and provides tools for automated vulnerability checking.

## Environment

-   Red Hat Satellite v6.8

-   3 x Red Hat Enterprise Linux clients v7.9

## Pre-requisites (completed in previous exercises in the workshop, values to be changed)

-   Organization to be used = Default Organization

-   Location to be used = Default Location

-   A content view = RHEL7

-   Lifecycle environments = Dev, QA, Prod

-   SSH access to RHEL clients (node1, node2, node3) which has been registered to Satellite

## Exercise

#### 1\. Logging into Satellite

-   Use a web browser on your computer to access the Satellite GUI via the link found in the Environment above. And use the following username and password to login: admin / ansible123

![](https://lh3.googleusercontent.com/61RJI80QPal7BWRRjw8AGQA_okIXvBTGG6Vfo0ECdVjSFO4PPkvAMKHpVccroazXRtV_uvfC20x38j0i49BZErswpsDXTcDrxFw94cp1KlLYdjNDCC3Sxb8UwYcrOZNCWR7rqcmD)

-   Once you're in Satellite you would be able to see a dashboard

![](https://lh5.googleusercontent.com/0oL1NhGOFVJQIcnol7xSneJgzAIAX5HKPkV_hHjan5iM9L7qVliUMct53MsKTy4rkJU0Yu8HBmd7yV9VLafJqDJFZKTLHPo73wNMD64dNuvP6xS04C6KAHKr2KIJ1bF67m62cjdA)

#### 2\. Creating a new compliance policy

-   Now we will start configuring a compliance policy to be able to scan our RHEL nodes.

-   Hover over "Hosts" from the menu on the left side of the screen, and then click on "Policies"

![](https://lh4.googleusercontent.com/cVLJMoZs3YrWJayGeOd3-1lhpyC_Lu-xXxX0RD1ZLl6uzoA_M_dXktuknpvA5TgPPNrcCJqyYwnEVMEMlQno3_8q7dnN-5f6ATT2q-UfiPRe3wGYKnMDx2BjNgnB-7-tvcIzo9F2)

-   Click on the "New Policy" button, and fill out the details as followed in step 3. 

![](https://lh5.googleusercontent.com/2qOPrqw4iC02hxEM6dfG5fj_TOsR5s-AAPCmEIXRDJo7kcfLlATH-bH36htyDB4UHWVTA-43jpwQfv21QdZx6oW41KohQYz4K8bpg1z_70-J6RkSknnMSiD486UjVziqD0SdnSxU)

#### 3\. Configuring a new compliance policy (values to be changed)

-   Now we will start configuring our Satellite server to be able to manage a compliance policy

-   Select "Manual" from the deployment options and click "Next"

![](https://lh3.googleusercontent.com/j9IPZGS-LJPKAZJj4k6wZbbx15cAkOtvqT_UBDj2iAzhi5_Mkkq6aGZClS8gSq__DxVEMsPik-pQVDEK7l2JqWJNYZJXGr2yNdETyeNaSydhU8A205f9cha97QQYNLzlPRjW9-Ka)

-   Create the policy name "PCI-Compliance" and provide any description you like. Then click "Next"

![](https://lh4.googleusercontent.com/sbJOKhFNODc7YodnOaFwZjeOx16eofpbEW0PxDTv76R4aoWKHHtP-BrpKXE7khOnSKKxdKWxQRbWK7TIIoYaW6otQJjxHIO-Rd770NsBLVZiHZdhrpy8MhqaiJRoNQOv0bV1oFo4)

-   Select the "Red Hat rhel7 default content" and "PCI-DSS v3.2.1 Control Baseline for Red Hat Enterprise Linux 7". There is no tailoring file. Then click "Next"![](https://lh6.googleusercontent.com/m4VK9on3A5ZASMOB1sG8Hx76L3-fCy4Pn_mYsSmYT-QZYGbK_bYubLLpYRHzP5DoLGi_XTd7bAXTZZ2xdg5ss0OT-oRWguI7nECaUJtD-8k6i6sxLfTFn6SSLwYsaV8ePRMq5v--)

-   It is necessary to set a schedule when creating a new compliance policy. You can select "Weekly" and "Monday" for lab purposes. Then click "Next"

![](https://lh6.googleusercontent.com/rvXj6ousHaUVEs4XBXe-wON8U3LqnSFN8xrTYtQLEWQ1_YmbPDy3Ytw3Muogeb5tYFkG4rxr5s2MlGlJgjSh4gIc53Ovx0o_VEWHrU7YRH_OM6XyLKZmJLR9m8dOucga_HcFaf5_)

-   Steps 5, 6, and 7 as part of the New Compliance Policy can use default values. Click "Next" through "Locations", "Organizations", and "Hostgroups"

![](https://lh6.googleusercontent.com/Y2DSZltuMov4zXtop_IYzfWZXRRmyk2Ogvnv-Sz22QGaKWm4QD7LcVtjkVP3inDSFIlLUiaRC267gnBrABF0sNJCx-lXN-19Ufu4le-HdUzWz36fxAI4nizD3bi5piEwEoJN3JXF)

#### 4\. Logging into the Ansible Automation Platform

-   Use a web browser on your computer to access the Ansible GUI via the link found in the Environment above

![](https://lh5.googleusercontent.com/UH3-l8kGnC1UM20Op4_d0HZZ7upq84dechLxShPZZ4Ki-4P-bu8ej8sfUZIO-lxBXwdAx7MaIehy9I0NQt-w_DhzJdHBJnOfwRcYaY6Z2UUXsTY_eekbmDgvfq-2SLEIgqEvF7SG)

-   Once you're in Ansible Tower, you'll be able to see a dashboard.

![](https://lh5.googleusercontent.com/yW3YHJtQU1UkU6iJW6gn0i5BYKGPPYAayj3uZ-Qqcqd1yQQqICaHsQbkVYU1bgJhNEK0iUuX4r-cqP-CY8LtTkjT6III2jgw9isInpaJX6GM2pzhwomqTFw0xd6UcxQYMYFJtcpr)

#### 4\. Configuring an Ansible Tower template to run an OpenSCAP scan and launch the scan. (values to be changed)

-   Click "Templates" from the left sidebar. 

![](https://lh3.googleusercontent.com/YEBQn4MdNVakLfpdVL2rArmfB-G8wd2esjHQJzMLhni9KWDWx_1vyRtby0uy9Kc46oRdX57mnDXACRs3GT96qNSJk4M5AsJOXqfJdTduMS7Ug7vO2dpcA4yTVV1PbH5vWBczMekf)

-   Then select ![](https://lh6.googleusercontent.com/sN5ZK1Ryj9X3y6ynlJlYMn9MN7h4rnSmmPgkkPNxgrUbB268TlOs9PjqgKe6SbGlEM1xuTvdGcFUg7CmUplRab-W6mD-apjgX7hnvzhgzZaoar25Oia4kghBEPcxYCHxRq4SBwDp) on the far right side of the screen and click "Job Template". Fill out the details as follows.

-   Name: "OpenSCAP_Configure "

-   Job Type: "Run"

-   Inventory: "Workshop Inventory"

-   Playbook: "configure_openscap.yml"

-   Project: "Automated_Smart_Management" 

-   Credentials: "Satellite_Credential", "Workshop Credential"

-   Extra Variables:

-   HOSTS: web

-   Policy_scan: 

-   PCI_Compliance

![](https://lh6.googleusercontent.com/B_rNKlbNdXn35bcf5KFW_Igt8VSQs3EM1PJryo-T-9eugHt3LBs3TVB5BN5LCDxP2zlQbracBL1z0exSSEt49gYxqFPU1U8OJP1WNxj7hgQS-w03iQg4KZzJ85VwQiXxGAbF3dgH)

Leave the rest of the fields blank or as they are, and click "Save".

-   Launch the job by clicking: ![](https://lh4.googleusercontent.com/-q-chMPmF9atKHlW8-yHvUIN1auckybzcS8T2eyIfkG4vkyKisav_Vk0j3VUzve5yICD3jr4SomqCa8erHRMBfTzhQTr2MTC47roIypd18aadDBlRgApzZi_e8A7M65RePeHo7kN)

![](https://lh4.googleusercontent.com/HRMQ7FhoQazxxarlbwAJgLQS4MoXCjy_mnCMhSugXw0WkXDzh2B582ulwFzIP_PW5pr3Y_jAqpO8T47nsLjGIm9UUBZ_jsdxcqzqiKGT0Oi6x01sc0PF2IjpzhPxdOct1cLUl5Xq)

#### 5\. Navigate back to Satellite to examine the Asset Reporting File (ARF). 

-   Hover over "Hosts" from the menu on the left side of the screen, and then click on "Reports".

![](https://lh4.googleusercontent.com/JZnAxnuQhawkHkBdF1YfOLrXfQ7WV6pRLkpvFwKz9Vrx1Frd3cHZcrLRe7s41qefgY7515rb580oLW5PbrWFm90uip1pNpb1_DhbrWMRfSs9N-9WCCTDc8obztT9uKnMg_MNOqe2)

-   Click on the ![](https://lh5.googleusercontent.com/5xFQMKyfWZ3kWEJpqFymvptsqV7KHkxFQGTQcTJWW5YDALMCnGm2PTIkzXKT9_qJ8keIDJl2yKtlYHSmxCnzuOVFHa7MPC-02ksTREuF2jis47m3ARKa2OWMNsdmt6wxUa4VPcuD) for 'node1.example.com' to evaluate

-   You can sort by "Pass", "Fail", "Fixed", or any number of qualifiers as well as group rules by "Severity"

![](https://lh3.googleusercontent.com/hu_26q9h1QEMEAs6_57yiqDngir1xM5lolQWOSsDkOOzuiCpSUKtYDDk3TLc2zMozmLNWcmmDXMVuIulAvsolKZa_t6Siu62mqLabFdgO19Mr-V6rw6E14n7qYUxmmwt2PpaiapP)

-   Selecting a rule presents further information regarding rationale as well as a description of the rule that includes references and identifiers.

-   If you scroll the page you will notice multiple remediation steps including an 'Ansible' snippet. This presents tasks you can compile within a playbook to automation remediation across affected machines.

![](https://lh3.googleusercontent.com/_H6GjCsPq1pntFiW1lSRJQBq5dOyeGBJhk66RxNn6KO4SqeYJfmEeTgr2-rbpJlIEt5-ueQcfA41Ivae-wIErXreIsy9vkYnVB-i9K_FzA9mz_MWrjFpMdDyMcZurjaSNf-t516p)

#### 7\. Scaling an OpenSCAP scan. (values to be changed)

-   In Satellite, hover over "Hosts" from the menu on the left side of the screen, and then click on "Policies".

![](https://lh4.googleusercontent.com/cVLJMoZs3YrWJayGeOd3-1lhpyC_Lu-xXxX0RD1ZLl6uzoA_M_dXktuknpvA5TgPPNrcCJqyYwnEVMEMlQno3_8q7dnN-5f6ATT2q-UfiPRe3wGYKnMDx2BjNgnB-7-tvcIzo9F2)

-   Select "Manual" from the deployment options and click "Next"

![](https://lh3.googleusercontent.com/j9IPZGS-LJPKAZJj4k6wZbbx15cAkOtvqT_UBDj2iAzhi5_Mkkq6aGZClS8gSq__DxVEMsPik-pQVDEK7l2JqWJNYZJXGr2yNdETyeNaSydhU8A205f9cha97QQYNLzlPRjW9-Ka)

-   Create the policy name "PCI-Compliance" and provide any description you like. Then click "Next"

![](https://lh4.googleusercontent.com/dTnvNbOssJCLU4h2wp1OkN6fOTlVORkANhgW6dmt2gxcegGsXdYlhNbXGVMlc6VDzu8OMzXgXR0oHbs_UWAoBhijgVvsPUEu3_GDkLWaCdLudhJHrlB4Kyv_CGFCEUS362ZqzQak)

-   Select the "Red Hat rhel7 default content" and "DISA STIG for Red Hat Enterprise Linux 7". There is no tailoring file. Then click "Next"

![](https://lh4.googleusercontent.com/WSMWISWqV4d5Lm-rOHEZDmsoRaijc642iIhi7l23Tpe5XCJMEk__7xP0o3pj7lDbP0NJssxNI7a0FMbj21r8FPwqjkQ0W58lmyvprQXu3xgoCNiuii6VGwkt1BH_Hb7psI5XBE5c)

-   It is necessary to set a schedule when creating a new compliance policy. You can select "Weekly" and "Monday" for lab purposes. Then click "Next"

![](https://lh6.googleusercontent.com/rvXj6ousHaUVEs4XBXe-wON8U3LqnSFN8xrTYtQLEWQ1_YmbPDy3Ytw3Muogeb5tYFkG4rxr5s2MlGlJgjSh4gIc53Ovx0o_VEWHrU7YRH_OM6XyLKZmJLR9m8dOucga_HcFaf5_)

-   Steps 5, 6, and 7 as part of the New Compliance Policy can use default values. Click "Next" through "Locations", "Organizations", and "Hostgroups"

![](https://lh6.googleusercontent.com/Y2DSZltuMov4zXtop_IYzfWZXRRmyk2Ogvnv-Sz22QGaKWm4QD7LcVtjkVP3inDSFIlLUiaRC267gnBrABF0sNJCx-lXN-19Ufu4le-HdUzWz36fxAI4nizD3bi5piEwEoJN3JXF)

-   Click "Templates" from the left sidebar. 

![](https://lh3.googleusercontent.com/YEBQn4MdNVakLfpdVL2rArmfB-G8wd2esjHQJzMLhni9KWDWx_1vyRtby0uy9Kc46oRdX57mnDXACRs3GT96qNSJk4M5AsJOXqfJdTduMS7Ug7vO2dpcA4yTVV1PbH5vWBczMekf)

-   Then select ![](https://lh6.googleusercontent.com/sN5ZK1Ryj9X3y6ynlJlYMn9MN7h4rnSmmPgkkPNxgrUbB268TlOs9PjqgKe6SbGlEM1xuTvdGcFUg7CmUplRab-W6mD-apjgX7hnvzhgzZaoar25Oia4kghBEPcxYCHxRq4SBwDp) on the far right side of the screen and click "Job Template". Fill out the details as follows.

-   Name: "OpenSCAP_Configure "

-   Job Type: "Run"

-   Inventory: "Workshop Inventory"

-   Playbook: "configure_openscap.yml"

-   Project: "Automated_Smart_Management" 

-   Credentials: "Satellite_Credential", "Workshop Credential"

-   Extra Variables:

-   HOSTS: web

-   Policy_scan: 

-   PCI-Compliance

-   STIG-Compliance

![](https://lh5.googleusercontent.com/OhrtdmXwa7y3bQoaAgb2JRhj2LI1ZAsRPpi-VP-EAXYncMYvRFlHMJm4PSprCUfwKGOZcwgBEUC8P4D177epWSsPALU5LMb6Yc-t8BnPj7uIz-NdC7qWPG0Xtq7Pg__OTlkpN27b)

Leave the rest of the fields blank or as they are, and click "Save".

-   Launch the job by clicking: ![](https://lh4.googleusercontent.com/-q-chMPmF9atKHlW8-yHvUIN1auckybzcS8T2eyIfkG4vkyKisav_Vk0j3VUzve5yICD3jr4SomqCa8erHRMBfTzhQTr2MTC47roIypd18aadDBlRgApzZi_e8A7M65RePeHo7kN)

![](https://lh6.googleusercontent.com/2DXuz9ZjyFFEZixvCiSnh8EzcM9xpiY1fIgWyI-8i5VR8cuCFzM8fEaVB7Pij0Nd91EBtQjDpeT1YwD8dGJcfJvzOmFfQc9kvqqjNHzMEuWCljQMT0nO6USaBEjJoHQYWdbSGjao)

#### 8\. Navigate back to Satellite to examine the Asset Reporting File (ARF). 

-   Hover over "Hosts" from the menu on the left side of the screen, and then click on "Reports".

![](https://lh4.googleusercontent.com/JZnAxnuQhawkHkBdF1YfOLrXfQ7WV6pRLkpvFwKz9Vrx1Frd3cHZcrLRe7s41qefgY7515rb580oLW5PbrWFm90uip1pNpb1_DhbrWMRfSs9N-9WCCTDc8obztT9uKnMg_MNOqe2)

-   Notice that we've now easily scaled to six scans, 2 scans of each node for PCI-Compliance and for STIG-Compliance. 

![](https://lh3.googleusercontent.com/BoUp9jxDCNaqpWabW1hdEZJazSA5T79Oh1jt7hzCaLtm374oH8EZfrloculCO3ekg2ncdqKMAzAGqdXo7bwNsmMPaxElddYXZx7vmbS3s-J3bGKqCClh7wPjDq0oVC3zL8Xq1wIc)

-   Each report can be reviewed independent of other node scans and remediations for rule findings can be completed according to the requirements of your own internal policies.

  __ _       _     _     _
 / _(_)_ __ (_)___| |__ | |
| |_| | '_ \| / __| '_ \| |
|  _| | | | | \__ \ | | |_|
|_| |_|_| |_|_|___/_| |_(_)
