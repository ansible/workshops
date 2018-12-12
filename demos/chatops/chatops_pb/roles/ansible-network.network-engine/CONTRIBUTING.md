# Developer Guide

This role is developed and maintained by the Ansible Network Working Group.
Contributions to this role are welcomed.  This document will provide individuals
with information about how to contribute to the further development of this
role.

## Contributing

There are many ways you can contribute to this role.  Adding new artifacts such
as modules and plugins, testing and/or reviewing and updating documentation.

### Adding support for a new platform

To add support for a new platform to this role, there are a couple of things
that need to be done.

1) Create the module for the platform specific implementation in Ansible.  The
module can be contributed directly to Ansible core, distributed through Ansible
Galaxy or added to this role.

2) (Optional) If adding the module code directly to this role, add the module
to `library/`

3) (Optional) If the new platform module is distributed through another Galaxy
role, please update [README](README.md) Dependencies section to include the
name of the Galaxy role that includes the module.

4) Once the module has been created, the add a new task in `tasks/` for the
specific platform to be supported.  Use any of the existing platform
implementations as a guide.

5) (Optional) If a configuration parameter is not supported, then the
implementation in tasks should detect that and provide a warning message.

6) Update the `meta/main.yaml` file to add the newly provided platform to
the `platforms` meta data.

### Adding platform specific arguments

Sometimes there is a need to add platform specific arguments to a role for use
by a platform specific module.  This can be accomplished by adding the adding
the arguments under a platform specific key.

Note: It is the responsibility of the task writer to handle the implementation
of the platform specific arguments.

Here is an example that implements a platform specific argument:

```yaml
tasks:
  - name: configure network device resource
    include_role:
      name: net_system
    vars:
      resource:
        foo: bar
      ios:
        foo: baz
```

### Adding documentation for a platform specific implementation

While not required, there are times when providing implementation nodes are
advantageous to instructing the playbook writer how to implement platform
specific arguments.  In order to provide platform specific documentation,
create a file in the docs directory using GitHub Markdown.  The file name
should be the platform name.

For instance, let's assume we want to create implementation nodes for a
fictitious platform call `foo`.  Create a new file `docs/foo.md` and
then add a link to [README](README.md) pointing to `docs/foo.md` in the `PLATFORM
NOTES` section.

# Note

The release cadence for the network-engine role is two weeks and it will be
released on every second Tuesday at 12:00 PM (GMT) from the date of prior release.
For the PR to be available in the upcoming release it should be in a mergeable state
that is CI is passing and all review comments fixed at least two days prior to scheduled date
of release.

## Bug Reporting

If you have found a bug in the with the current role please open a [GitHub
issue](../../issues)

## Contact

* [#ansible-network IRC channel](https://webchat.freenode.net/?channels=ansible-network) on Freenode.net

