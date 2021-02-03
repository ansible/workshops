# Redhat Communties of Practice Tower Configuration Collection

![Ansible Lint](https://github.com/redhat-cop/tower_configuration/workflows/Ansible%20Lint/badge.svg)
![Galaxy Release](https://github.com/redhat-cop/tower_configuration/workflows/galaxy-release/badge.svg)
<!-- Further CI badges go here as above -->

This Ansible collection allows for easy interaction with an AWX or Ansible Tower server via Ansible roles using the AWX/Tower collection modules.

## Included content

Click the `Content` button to see the list of content included in this collection.

## Installing this collection

You can install the redhat_cop tower_configuration collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install redhat_cop.tower_configuration

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: redhat_cop.tower_configuration
    # If you need a specific version of the collection, you can specify like this:
    # version: ...
```

## Using this collection
Define following vars here, or in `tower_configs/tower_auth.yml`
`tower_hostname: ansible-tower-web-svc-test-project.example.com`

You can also specify authentication by a combination of either:

 - `tower_hostname`, `tower_username`, `tower_password`
 - `tower_hostname`, `tower_oauthtoken`

The OAuth2 token is the preferred method. You can obtain the token through the prefered `tower_token` module, or through the
AWX CLI [login](https://docs.ansible.com/ansible-tower/latest/html/towercli/reference.html#awx-login)
command.

These can be specified via (from highest to lowest precedence):

 - direct role variables as mentioned above
 - environment variables (most useful when running against localhost)
 - a config file path specified by the `tower_config_file` parameter
 - a config file at `~/.tower_cli.cfg`
 - a config file at `/etc/tower/tower_cli.cfg`

Config file syntax looks like this:

```
[general]
host = https://localhost:8043
verify_ssl = true
oauth_token = LEdCpKVKc4znzffcpQL5vLG8oyeku6
```

Tower token module would be invoked with this code:
```yaml
    - name: Create a new token using tower username/password
      awx.awx.tower_token:
        description: 'Creating token to test tower jobs'
        scope: "write"
        state: present
        tower_host: "{{ tower_hostname }}"
        tower_username: "{{ tower_username }}"
        tower_password: "{{ tower_password }}"

```

### Tower Export
The awx command line can export json that is compatable with this collection.
More details can be found [here](playbooks/tower_configs_export_model/README.md)

### See Also:

* [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Release and Upgrade Notes
For details on changes between versions, please see [the changelog for this collection](CHANGELOG.rst).

## Roadmap
Adding the ability to use direct output from the awx export command in the roles along with the current data model.

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [Tower Configuration collection repository](https://github.com/redhat-cop/tower_configuration).
More information about contributing can be found in our [Contribution Guidelines.](https://github.com/redhat-cop/tower_configuration/blob/devel/.github/CONTRIBUTING.md)

## Licensing

GNU General Public License v3.0 or later.

See [LICENCE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
