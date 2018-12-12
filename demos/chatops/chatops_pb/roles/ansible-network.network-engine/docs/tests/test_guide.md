# Test Guide

The tests in network-engine are role based where the entry point is `tests/test.yml`.
The tests for `textfsm_parser` and `command_parser` are run against `localhost`.

## How to run tests locally

```
cd tests/
ansible-playbook -i inventory test.yml
```

## Role Structure

```
role_name
├── defaults
│   └── main.yaml
├── meta
│   └── main.yaml
├── output
│   └── platform_name
│       ├── show_interfaces.txt
│       └── show_version.txt
├── parser_templates
│   └── platform_name
│       ├── show_interfaces.yaml
│       └── show_version.yaml
└── tasks
    ├── platform_name.yaml
    └── main.yaml
```

If you add any new Role for test, make sure to include the role in `test.yml`:

```yaml

  roles:
    - command_parser
    - textfsm_parser
    - $role_name
```

## Add new platforms tests to an existing roles

Create directory with the `platform_name` in `output` and `parser_templates` directories
which will contain output and parser files of the platform.

Add corresponding playbook with the `platform_name` in `tasks/$platform_name.yaml`
and add an entry in `tasks/main.yaml`:

```yaml
- name: platform_name command_parser test
  import_tasks: platform_name.yaml
```
