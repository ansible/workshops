============================================
redhat_cop.tower_configuration Release Notes
============================================

.. contents:: Topics


v1.0.2
======

Minor Changes
-------------

- added alias option for survey to survey_spec in workflows.
- updated documentation on surveys for workflows and job templates

v1.0.0
======

Major Changes
-------------

- Updated Roles to use the tower_export model from the awx command line.
- credential_types Updated to use the tower_export model from the awx command line.
- credentials Updated to use the tower_export model from the awx command line.
- inventory Updated to use the tower_export model from the awx command line.
- inventory_sources Updated to use the tower_export model from the awx command line.
- job_templates Updated to use the tower_export model from the awx command line.
- projects Updated to use the tower_export model from the awx command line.
- teams Updated to use the tower_export model from the awx command line.
- users Updated to use the tower_export model from the awx command line.

Minor Changes
-------------

- updated to allow vars in messages for notifications.
- updated tower workflows related role `workflow_job_templates` to include `survey_enabled` defaulting to `false` which is a module default and `omit` the `survey_spec` if not passed.
- updated various roles to include oauth token and tower config file.

Breaking Changes / Porting Guide
--------------------------------

- Removed depreciated options in inventory sources role (source_regions, instance_filters, group_by)
- Renamed notifications role to notification_templates role as in awx.awx:15.0. The variable is not tower_notification_templates.

v0.2.1
======

Minor Changes
-------------

- Changelog release cycle

v0.2.0
======

Minor Changes
-------------

- Added pre-commit hook for local development and automated testing purposes
- Standardised and corrected all READMEs

Bugfixes
--------

- Removed defaulted objects for all roles so that they were not always run if using a conditional against the variable. (see https://github.com/redhat-cop/tower_configuration/issues/68)

v0.1.0
======

Major Changes
-------------

- Groups role - Added groups role to the collection
- Labels role - Added labels role to the collection
- Notifications role - Added many options to notifications role
- Workflow Job Templates role - Added many options to WJT role

Minor Changes
-------------

- GitHub Workflows - Added workflows to run automated linting and integration tests against the codebase
- Hosts role - Added new_name and enabled options to hosts role
- Housekeeping - Added CONTRIBUTING guide and pull request template
- Inventory Sources role - Added notification_templates_started, success, and error options. Also added verbosity and source_regions options.
- Teams role - Added new_name option to teams role
- Test Configs - Added full range of test objects for integration testing

Bugfixes
--------

- Fixed an issue where tower_validate_certs and validate_certs were both used as vars. Now changed to tower_validate_certs
