# CLI Template Directives

The `network_template` module supports a number of keyword based objectives that
handle how to process the template.  Templates are broken up into a series
of blocks that process lines.  Blocks are logical groups that have a common
set of properties in common.

Blocks can also include other template files and are processed in the same
manner as lines.  See includes below for a description on how to use the
include directive.

The template module works by processing the lines directives in sequential
order.  The module will attempt to template each line in the lines directive
and, if successful, add the line to the final output.  Values used for
variable substitution come from the host facts.  If the line could not
be successfully templated, the line is skipped and a warning message is
displayed that the line could not be templated.

There are additional directives that can be combined to support looping over
lists and hashes as well as applying conditional statements to blocks, lines
and includes.

## `name`

Entries in the template may contain a `name` field.  The `name` field
is used to provide a description of the entry.  It is also used to provide
feedback when processing the template to indicate when an entry is
skipped or fails.

## `lines`

The `lines` directive provides an ordered list of statements to attempt
to template.  Each entry in the `lines` directive will be evaluated for
variable substitution.  If the entry can be successfully templated, then the
output will be added to the final set of entries.  If the entry cannot be
successfully templated, then the entry is ignored (skipped) and a warning
message is provided.  If the entry in the `lines` directive contains
only static text (no variables), then the line will always be processed.

The `lines` directive also supports standard Jinja2 filters as well as any
Ansible specific Jinja2 filters.  For example, lets assume we want to add a
default value if a more specific value was not assigned by a fact.

```yaml
- name: render the system hostname
  lines:
    - "hostname {{ hostname | default(inventory_hostname_short }}"
```

## `block`

A group of `lines` directives can be combined into a `block`
directive.  These `block` directives are used to apply a common set of
values to one or more `lines` or `includes` entries.

For instance, a `block` directive that contains one or more `lines`
entries could be use the same set of `loop` values or have a
common `when` conditional statement applied to them.

## `include`

Sometimes it is advantageous to break up templates into separate files and
combine them.  The `include` directive will instruct the current template
to load another template file and process it.

The `include` directive also supports variable substitution for the
provided file name and can be processed with the `loop` and `when`
directives.

## `when`

The `when` directive allows for conditional statements to be applied to
a set of `lines`, a `block` and/or the `include` directive.  The
`when` statement is evaluated prior to processing the statements and if
the condition is true, the statements will attempt to be templated.  If the
statement is false, the statements are skipped and a message returned.

## `loop`

Depending on the input facts, sometimes it is necessary to iterate over a
set of statements.  The `loop` directive allows the same set of statements
to be processed in such a manner.  The `loop` directive takes, as input,
the name of a fact that is either a list or a hash and iterates over the
statements for each entry.

When the provided fact is a list of items, the value will be assigned to a
variable called `item` and can be referenced by the statements.

When the provided fact is a hash of items, the hash key will be assigned to
the `item.key` variable and the hash value will be assigned to the
`item.value` variable.  Both can then be referenced by the statements.

## `loop_control`

The `loop_control` directive allows the template to configure aspects
related to how loops are process.  This directive provides a set of suboptions
to configure how loops are processed.

### `loop_var`

The `loop_var` directive allows the template to override the default
variable name `item`.  This is useful when handling nested loops such
that both inner and outer loops values can be accessed.

When setting the `loop_var` to some string, the string will replace
`item` as the variable name used to access the values.

For example, lets assume instead of using item, we want to use a different
variable name such as entry:

```yaml
- name: render entries
  lines:
    - "hostname {{ entry.hostname }}"
    - "domain-name {{ entry.domain_name }}"
  loop: "{{ system }}"
  loop_control:
    loop_var: entry
```

## `join`

When building template statements that include optional values for
configuration, the `join` directive can be useful.  The `join`
directive instructs the template to combine the templated lines together
into a single string to insert into the configuration.

For example, lets assume there is a need to add the following statement to
the configuration:

```
ip domain-name ansible.com vrf management
ip domain-name redhat.com
```

To support templating the above lines, the facts might include the domain-name
and the vrf name values.  Here is the example facts:

```yaml
---
system:
  - domain_name: ansible.com
    vrf: management
  - domain_name redhat.com
```

And the template statement would be the following:

```yaml
- name: render domain-name
  lines:
    - "ip domain-name {{ item.domain_name }}"
    - "vrf {{ item.vrf }}"
  loop: "{{ system }}"
  join: yes
```

When this entry is processed, the first iteration will successfully template
both lines and add `ip domain-name ansible.com vrf management` to the
output.

When the second entry is processed, the first line will be successfully
templated but since there is no management key, the second line will return a
null value.  The final line added to the configuration will be ` ip
domain-name redhat.com`.

If the `join` directive had been omitted, then the final set of
configuration statements would be as follows:

```
ip domain-name ansible.com
vrf management
ip domain-name redhat.com
```

## `join_delimiter`

When the `join` delimiter is used, the templated values are combined into a
single string that is added to the final output.  The lines are joined using a
space.  The delimiting character used when processing the `join` can be
modified using `join_delimiter` directive.

Here is an example of using the this directive.  Take the following entry:

```yaml
- name: render domain-name
  lines:
    - "ip domain-name {{ item.domain_name }}"
    - "vrf {{ item.vrf }}"
  loop: "{{ system }}"
  join: yes
  join_delimiter: ,
```

When the preceding statements are processed, the final output would be
(assuming all variables are provided):

```
ip domain-name ansible.com,vrf management
ip domain-name redhat.com
```

## `indent`

The `indent` directive is used to add one or more leading spaces to the
final templated statement.  It can be used to recreated a structured
configuration file.

Take the following template entry as an example:

```yaml
- name: render the interface context
  lines: "interface Ethernet0/1"

- name: render the interface configuration
  lines:
    - "ip address 192.168.10.1/24"
    - "no shutdown"
    - "description this is an example"
  indent: 3

- name: render the interface context
  lines: "!"
```

Then the statements above are processed, the output will look like the
following:

```
interface Ethernet0/1
   ip address 192.168.10.1/24
   no shutdown
   description this is an example
!
```

## `required`

The `required` directive specifies that all of the statements must be
templated otherwise a failure is generated.  Essentially it is a way to
make certain that the variables are defined.

For example, take the following:

```yaml
- name: render router ospf context
  lines:
    - "router ospf {{ process_id }}"
  required: yes
```

When the above is processed, if the variable `process_id` is not present,
then the statement cannot be templated.  Since the `required` directive
is set to true, the statement will cause the template to generate a failure
message.

## `missing_key`

By default, when statements are processed and a variable is undefined, the
module will simply display a warning message to the screen.  In some cases, it
is desired to either suppress warning messages on a missing key or to force the
module to fail on a missing key.

To change the default behaviour, use the `missing_key` directive.  This
directive accepts one of three choices:

* `ignore`
* `warn` (default)
* `fail`

The value of this directive will instruct the template how to handle any
condition where the desired variable is undefined.

