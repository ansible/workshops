==============================
Ansible Network network-engine
==============================

.. _Ansible Network network-engine_v2.6.9:

v2.6.9
======

.. _Ansible Network network-engine_v2.6.9_Bugfixes:

Bugfixes
--------

- Fix templating repeat_for `network-engine#190 <https://github.com/ansible-network/network-engine/pull/190>`_.

- Add missing boilerplate for net_facts module `network-engine#194 <https://github.com/ansible-network/network-engine/pull/194>`_.


.. _Ansible Network network-engine_v2.6.8:

v2.6.8
======

.. _Ansible Network network-engine_v2.6.8_New Modules:

New Modules
-----------

- Add ``net_facts`` module.


.. _Ansible Network network-engine_v2.6.8_Bugfixes:

Bugfixes
--------

- There was a release problem with our v2.6.7 release which required us to release v2.6.8.


.. _Ansible Network network-engine_v2.6.6:

v2.6.6
======

.. _Ansible Network network-engine_v2.6.6_Minor Changes:

Minor Changes
-------------

- Capability to filter AnsibleModule kwargs `network-engine#149 <https://github.com/ansible-network/network-engine/pull/149>`_.


.. _Ansible Network network-engine_v2.6.6_Removed Features (previously deprecated):

Removed Features (previously deprecated)
----------------------------------------

- Remove deprecated module ``cli_get``


.. _Ansible Network network-engine_v2.6.5:

v2.6.5
======

.. _Ansible Network network-engine_v2.6.5_Bugfixes:

Bugfixes
--------

- Remove GenericLinux from supported platforms `network-engine#145 <https://github.com/ansible-network/network-engine/pull/145>`_.


.. _Ansible Network network-engine_v2.6.4:

v2.6.4
======

.. _Ansible Network network-engine_v2.6.4_Removed Features (previously deprecated):

Removed Features (previously deprecated)
----------------------------------------

- Remove deprecated module ``text_parser``.

- Remove deprecated module ``textfsm``.


.. _Ansible Network network-engine_v2.6.4_Bugfixes:

Bugfixes
--------

- Fix repeat_for in json_template `network-engine#139 <https://github.com/ansible-network/network-engine/pull/139>`_.


.. _Ansible Network network-engine_v2.6.4_Documentation Updates:

Documentation Updates
---------------------

- Removes unnecessary details from README `network-engine#126 <https://github.com/ansible-network/network-engine/pull/126>`_.


.. _Ansible Network network-engine_v2.6.3:

v2.6.3
======

.. _Ansible Network network-engine_v2.6.3_Minor Changes:

Minor Changes
-------------

- Makes parser directive extend templatable `network-engine#132 <https://github.com/ansible-network/network-engine/pull/132>`_.


.. _Ansible Network network-engine_v2.6.3_Bugfixes:

Bugfixes
--------

- Task to fail if ansible_min_version isn't met `network-engine#130 <https://github.com/ansible-network/network-engine/pull/130>`_.


.. _Ansible Network network-engine_v2.6.2:

v2.6.2
======

.. _Ansible Network network-engine_v2.6.2_New Lookup Plugins:

New Lookup Plugins
------------------

- NEW ``config_template`` lookup plugin

- NEW ``yang_json2xml`` lookup plugin


.. _Ansible Network network-engine_v2.6.2_New Filter Plugins:

New Filter Plugins
------------------

- NEW ``to_lines`` filter plugin


.. _Ansible Network network-engine_v2.6.2_New Modules:

New Modules
-----------

- NEW ``validate_role_spec`` handle validating facts required by the role


.. _Ansible Network network-engine_v2.6.2_Bugfixes:

Bugfixes
--------

- Fix role path test dependency `network-engine#121 <https://github.com/ansible-network/network-engine/pull/121>`_.


.. _Ansible Network network-engine_v2.6.1:

v2.6.1
======

.. _Ansible Network network-engine_v2.6.1_Documentation Updates:

Documentation Updates
---------------------

- The argument to end a block of text when searching with match_greedy was missing `network-engine#116 <https://github.com/ansible-network/network-engine/pull/116>`_.


.. _Ansible Network network-engine_v2.6.0:

v2.6.0
======

.. _Ansible Network network-engine_v2.6.0_Major Changes:

Major Changes
-------------

- Initial release of 2.6.0 ``network-engine`` Ansible role that is supported with Ansible 2.6.0


.. _Ansible Network network-engine_v2.5.4:

v2.5.4
======

.. _Ansible Network network-engine_v2.5.4_Minor Changes:

Minor Changes
-------------

- Add parsers to search path `network-engine#89 <https://github.com/ansible-network/network-engine/pull/89>`_.

- Fix export_as templating vars `network-engine#104 <https://github.com/ansible-network/network-engine/pull/104>`_.


.. _Ansible Network network-engine_v2.5.4_Bugfixes:

Bugfixes
--------

- Fix cli task parser undefined issue when only command is used `network-engine#103 <https://github.com/ansible-network/network-engine/pull/103>`_.

- Fix an issue with using the extend directive with a loop `network-engine#105 <https://github.com/ansible-network/network-engine/pull/105>`_.

- Fixes bug when loading a dir of parsers `network-engine#113 <https://github.com/ansible-network/network-engine/pull/113>`_.


.. _Ansible Network network-engine_v2.5.3:

v2.5.3
======

.. _Ansible Network network-engine_v2.5.3_Minor Changes:

Minor Changes
-------------

- Templating the regex sent to the parser to allow us to use ansible variables in the regex string `network-engine#97 <https://github.com/ansible-network/network-engine/pull/97>`_.


.. _Ansible Network network-engine_v2.5.3_Removed Features (previously deprecated):

Removed Features (previously deprecated)
----------------------------------------

- Move yang2spec lookup to feature branch, till the right location for this plugin is identified `network-engine#100 <https://github.com/ansible-network/network-engine/pull/100>`_.


.. _Ansible Network network-engine_v2.5.2:

v2.5.2
======

.. _Ansible Network network-engine_v2.5.2_Minor Changes:

Minor Changes
-------------

- Add new directives extend `network-engine#91 <https://github.com/ansible-network/network-engine/pull/91>`_.

- Adds conditional support to nested template objects `network-engine#55 <https://github.com/ansible-network/network-engine/pull/55>`_.


.. _Ansible Network network-engine_v2.5.2_New Lookup Plugins:

New Lookup Plugins
------------------

- New lookup plugin ``json_template``

- New lookup plugin ``network_template``

- New lookup plugin ``yang2spec``

- New lookup plugin ``netcfg_diff``


.. _Ansible Network network-engine_v2.5.2_New Filter Plugins:

New Filter Plugins
------------------

- New filter plugin ``interface_range``

- New filter plugin ``interface_split``

- New filter plugin ``vlan_compress``

- New filter plugin ``vlan_expand``


.. _Ansible Network network-engine_v2.5.2_New Tasks:

New Tasks
---------

- New task ``cli``


.. _Ansible Network network-engine_v2.5.2_Bugfixes:

Bugfixes
--------

- Fix AnsibleFilterError, deprecations, and unused imports `network-engine#82 <https://github.com/ansible-network/network-engine/pull/82>`_.


.. _Ansible Network network-engine_v2.5.1:

v2.5.1
======

.. _Ansible Network network-engine_v2.5.1_Deprecated Features:

Deprecated Features
-------------------

- Module ``text_parser`` renamed to ``command_parser``; original name deprecated; legacy use supported; will be removed in 2.6.0.

- Module ``textfsm`` renamed to ``textfsm_parser``; original name deprecated; legacy use supported; will be removed in 2.6.0.


.. _Ansible Network network-engine_v2.5.1_New Modules:

New Modules
-----------

- New module ``command_parser`` (renamed from ``text_parser``)

- New module ``textfsm_parser`` (renamed from ``textfsm``)


.. _Ansible Network network-engine_v2.5.1_Bugfixes:

Bugfixes
--------

- Fix ``command_parser`` Absolute path with tilde in src should work `network-engine#58 <https://github.com/ansible-network/network-engine/pull/58>`_

- Fix content mush only accepts string type `network-engine#72 <https://github.com/ansible-network/network-engine/pull/72>`_

- Fix StringIO to work with Python3 in addition to Python2 `network-engine#53 <https://github.com/ansible-network/network-engine/pull/53>`_


.. _Ansible Network network-engine_v2.5.1_Documentation Updates:

Documentation Updates
---------------------

- User Guide `docs/user_guide <https://github.com/ansible-network/network-engine/tree/devel/docs/user_guide>`_.


.. _Ansible Network network-engine_v2.5.0:

v2.5.0
======

.. _Ansible Network network-engine_v2.5.0_Major Changes:

Major Changes
-------------

- Initial release of the ``network-engine`` Ansible role.

- This role provides the foundation for building network roles by providing modules and plugins that are common to all Ansible Network roles. All of the artifacts in this role can be used independent of the platform that is being managed.


.. _Ansible Network network-engine_v2.5.0_New Modules:

New Modules
-----------

- NEW ``text_parser`` Parses ASCII text into JSON facts using text_parser engine and YAML-formatted input. Provides a rules-based text parser that is closely modeled after the Ansible playbook language. This parser will iterate over the rules and parse the output of structured ASCII text into a JSON data structure that can be added to the inventory host facts.

- NEW ``textfsm`` Parses ASCII text into JSON facts using textfsm engine and Google TextFSM-formatted input. Provides textfsm rules-based templates to parse data from text. The template acting as parser will iterate of the rules and parse the output of structured ASCII text into a JSON data structure that can be added to the inventory host facts.

