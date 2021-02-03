# Redhat Communities of Practice Tower Utilities Collection

![Ansible Lint](https://github.com/redhat-cop/tower_utilities/workflows/Ansible%20Lint/badge.svg)
![Galaxy Release](https://github.com/redhat-cop/tower_utilities/workflows/galaxy-release/badge.svg)
<!-- Further CI badges go here as above -->

This ansible collection includes a number of roles which can be useful for installing and managing AWX or Ansible Tower. Using this collection, you'll be able to automate following tasks:

* prepare and install Tower (on a normal OS, or on OpenShift)
* configure the OS to support Kerberos (if you plan to manage Windows hosts using AD credentials)
* backup and restore Ansible Tower
* install a minimal Git repo over SSH, for demonstration and learning purposes

## Included content

Click the `Content` button to see the list of content included in this collection.

## Installing this collection

You can install the redhat_cop tower_utilities collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install redhat_cop.tower_utilities

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: redhat_cop.tower_utilities
    # If you need a specific version of the collection, you can specify like this:
    # version: ...
```
## Using this collection

### See Also:

* [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Release and Upgrade Notes

## Roadmap

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [Tower Utilities collection repository](https://github.com/redhat-cop/tower_utilities).
More information about contributing can be found in our [Contribution Guidelines.](https://github.com/redhat-cop/tower_utilities/blob/devel/.github/CONTRIBUTING.md)

## Licensing

GNU General Public License v3.0 or later.

See [LICENCE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
