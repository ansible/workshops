# CLI Parser Directives

The `command_parser` module is a module that can be used to parse the results of
text strings into Ansible facts.  The primary motivation for developing the
`command_parser` module is to convert structured ASCII text output (such as
the stdout returned from network devices) into JSON data structures suitable to be
used as host facts.

The parser template file format is loosely based on the Ansible playbook directives
language.  It uses the Ansible directive language to ease the transition from
writing playbooks to writing parser templates.  However, parser templates developed using this
module are not written directly into the playbook, but are a separate file
called from playbooks.  This is done for a variety of reasons but most notably
to keep separation between the parsing logic and playbook execution.

The `command_parser` works based on a set of directives that perform actions
on structured data with the end result being a valid JSON structure that can be
returned to the Ansible facts system.

## Parser language

The parser template format uses YAML formatting, providing an ordered list of directives
to be performed on the content (provided by the module argument).  The overall
general structure of a directive is as follows:

```yaml
- name: some description name of the task to be performed
  directive:
    argument: value
      argument_option: value
    argument: value
  directive_option: value
  directive_option: value
```

The `command_parser` currently supports the following top-level directives:

* `pattern_match`
* `pattern_group`
* `json_template`
* `export_facts`

In addition to the directives, the following common directive options are
currently supported:

* `name`
* `block`
* `loop`
* `loop_control`

  * `loop_var`

* `when`
* `register`
* `export`
* `export_as`
* `extend`

Any of the directive options are accepted but in some cases, the option may
provide no operation.  For instance, when using the `export_facts`
directive, the options `register`, `export` and `export_as` are all
ignored.  The module should provide warnings when an option is ignored.

The following sections provide more details about how to use the parser
directives to parse text into JSON structure.

## Directive Options

This section provides details on the various options that are available to be
configured on any directive.

### `name`

All entries in the parser template many contain a `name` directive.  The
`name` directive can be used to provide an arbitrary description as to the
purpose of the parser items.  The use of `name` is optional for all
directives.

The default value for `name` is `null`.

### `register`

Use the `register` option to register the results of a directive operation
temporarily into the variable name you specify 
so you can retrieve it later in your parser template. You use `register` in 
a parser template just as you would in an Ansible playbook.

Variables created with `register` alone are not available outside of the parser context.
Any values registered are only available within the scope of the parser activities. 
If you want to provide values back to the playbook, you must also define the [export](#export) option.

Typically you will use `register` alone for parsing each individual part of the
command output, then amalgamate them into a single variable at the end of the parser template,
register that variable and set `export: yes` on it.

The default value for `register` is `null`.

<a id="export"></a>

### `export`

Use the `export` option to export any value back to the calling task as an
Ansible fact.  The `export` option accepts a boolean value that defines if
the registered fact should be exported to the calling task in the playbook (or
role) scope.  To export the value, simply set `export` to True.

Note this option requires the `register` value to be set in some cases and will
produce a warning message if the `register` option is not provided.

The default value for `export` is `False`.

### `export_as`

Use the `export_as` option to export a value back to the calling task as an
Ansible fact in a specific format. The `export_as` option defines the structure of the exported data.
Accepted values for `export_as`:

* `dict`
* `hash`
* `object`
* `list`
* `elements` that defines the structure

**Note** this option requires the `register` value to be set and `export: True`.
Variables can also be used with `export_as`.
How to use variable with `export_as` is as follows:

Variable should be defined in vars or defaults or in playbook.
```yaml
  vars:
    export_type: "list"
```

Parser file needs to have the variable set to `export_as`.
```
export_as: "{{ export_type }}"
```

### `extend`

Use the `extend` option to extend a current fact hierarchy with the new
registered fact.  This will case the facts to be merged and returned as a
single tree.  If the fact doesn't previously exist, this will create the entire
structure.

The default value for `extend` is `null`.

### loop

Use the `loop` option to loop over a directive in order to process values.
With the `loop` option, the parser will iterate over the directive and
provide each of the values provided by the loop content to the directive for
processing.

Access to the individual items is the same as it would be for Ansible
playbooks.  When iterating over a list of items, you can access the individual
item using the `{{ item }}` variable.  When looping over a hash, you can
access `{{ item.key }}` and `{{ item.value }}`.

### `loop_control`

Use the `loop_control` option to specify the name of the variable to be
used for the loop instead of default loop variable `item`.
When looping over a hash, you can access `{{ foo.key }}` and `{{ foo.value }}` where `foo`
is `loop_var`.
The general structure of `loop_control` is as follows:

```yaml
- name: User defined variable
  pattern_match:
    regex: "^(\\S+)"
    content: "{{ foo }}"
  loop: "{{ context }}"
  loop_control:
    loop_var: foo

```

### `when`

Use the `when` option to place a condition on the directive to
decided if it is executed or not.  The `when` option operates the same as
it would in an Ansible playbook.

For example, if you only want to perform the match statement
when the value of `ansible_network_os` is set to `ios`, you can apply
the `when` conditional like this:

```yaml
- name: conditionally matched var
  pattern_match:
    regex: "hostname (.+)"
  when: ansible_network_os == 'ios'
```

## Directives

The directives perform actions on the content using regular expressions to
extract various values.  Each directive provides some additional arguments that
can be used to perform its operation.

### `pattern_match`

Use the `pattern_match` directive to extract one or more values from
the structured ASCII text based on regular expressions.

The following arguments are supported for this directive:

* `regex`
* `content`
* `match_all`
* `match_greedy`
* `match_until` : Sets a ending boundary for `match_greedy`.

The `regex` argument templates the value given to it so variables and filters can be used.
Example :
```yaml
- name: Use a variable and a filter
  pattern_match:
    regex: "{{ inventory_hostname | lower }} (.+)"
```

### `pattern_group`

Use the `pattern_group` directive to group multiple
`pattern_match` results together.

The following arguments are supported for this directive:

* `json_template`
* `set_vars`
* `export_facts`

### `json_template`

Use the `json_template` directive to create a JSON data structure based on a
template.  This directive will allow you to template out a multi-level JSON
blob.

The following arguments are supported for this directive:

* `template`

### `set_vars`

Use the `set_vars` directive to set variables to the values like key / value pairs
and return a dictionary.

### `export_facts`

Use the `export_facts` directive to take an arbitrary set of key / value pairs
and expose (return) them back to the playbook global namespace.  Any key /
value pairs that are provided in this directive become available on the host.
