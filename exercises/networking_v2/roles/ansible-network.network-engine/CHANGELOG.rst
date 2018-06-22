===============================
Ansible Network: network-engine
===============================

.. _Ansible Network: network-engine_v2.5.1:

v2.5.1
======

.. _Ansible Network: network-engine_v2.5.1_Documentation Updates:

Documentation Updates
---------------------

- User Guide `docs/user_guide <https://github.com/ansible-network/network-engine/tree/devel/docs/user_guide>`_.


.. _Ansible Network: network-engine_v2.5.1_Deprecated Features:

Deprecated Features
-------------------

- Module ``text_parser`` renamed to ``command_parser``; original name deprecated; legacy use supported; will be removed in 2.6.0.

- Module ``textfsm`` renamed to ``textfsm_parser``; original name deprecated; legacy use supported; will be removed in 2.6.0.


.. _Ansible Network: network-engine_v2.5.1_New Modules:

New Modules
-----------

- New module ``command_parser`` (renamed from ``text_parser``)

- New module ``textfsm_parser`` (renamed from ``textfsm``)


.. _Ansible Network: network-engine_v2.5.1_Bugfixes:

Bugfixes
--------

- Fix ``command_parser`` Absolute path with tilde in src should work `network-engine#58 <https://github.com/ansible-network/network-engine/pull/58>`_

- Fix content mush only accepts string type `network-engine#72 <https://github.com/ansible-network/network-engine/pull/72>`_

- Fix StringIO to work with Python3 in addition to Python2 `network-engine#53 <https://github.com/ansible-network/network-engine/pull/53>`_


.. _Ansible Network: network-engine_v2.5.0:

v2.5.0
======

.. _Ansible Network: network-engine_v2.5.0_Major Changes:

Major Changes
-------------

- Initial release of the ``network-engine`` Ansible role.

- This role provides the foundation for building network roles by providing modules and plugins that are common to all Ansible Network roles. All of the artifacts in this role can be used independent of the platform that is being managed.


.. _Ansible Network: network-engine_v2.5.0_New Modules:

New Modules
-----------

- NEW ``text_parser`` Parses ASCII text into JSON facts using text_parser engine and YAML-formatted input. Provides a rules-based text parser that is closely modeled after the Ansible playbook language. This parser will iterate over the rules and parse the output of structured ASCII text into a JSON data structure that can be added to the inventory host facts.

- NEW ``textfsm`` Parses ASCII text into JSON facts using textfsm engine and Google TextFSM-formatted input. Provides textfsm rules-based templates to parse data from text. The template acting as parser will iterate of the rules and parse the output of structured ASCII text into a JSON data structure that can be added to the inventory host facts.

