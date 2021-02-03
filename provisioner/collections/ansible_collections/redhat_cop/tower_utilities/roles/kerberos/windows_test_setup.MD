# Installing and configuring the Active Directory
These instructions have been tested on Windows Server 2016 and 2019

## Rename your computer
1. Navigate to Control Panel, System, Advanced System properties, Computer name, Change
2. Rename the server
3. Restart the server

## Create a new domain
1. Navigate to: Start menu, Control Panel , Administrative Tools , Server Manager.
2. Navigate to Roles, add roles, Domain Services Role, Next, Next, Create a new domain in a new forest, Next
3. Enter in the Domain name
4. Navigate to Next, Select Server 2008 from the dropdown, Next, Yes, Next,
5. Enter a “Directory Services Restore Mode Administrator Password”
6. Click Next, the roles will install and reboot.

## Enable Winrm
1. Follow steps layed out here: https://docs.ansible.com/ansible/latest/user_guide/windows_setup.html#winrm-setup
