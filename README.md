# Ansible Lightbulb

The Ansible Lightbulb project is an effort to provide a content toolkit and educational reference for effectively communicating and teaching Ansible topics.

Lightbulb began life as the content that supported Ansible's training program before it joined the Red Hat family focused solely on Linux server automation.

This content is now taking on a new life as a multi-purpose toolkit for effectively demonstrating Ansible's capabilities or providing informal workshop training in various forms -- instructor-led, hands-on or self-paced.

Over time Lightbulb will be expanded to include advanced and developer topics in addition to expanding beyond linux server automation and into Windows and network automation.

To support these objectives, the project provides a lab provisioner tool for creating an environment to present and work with Lightbulb content.

### What's Provided

The Ansible Lightbulb project has been designed to be used as a toolkit and best practices reference for Ansible presentations ranging from demos thru self-paced learning thru hands-on workshops. Here you will find:

* Workshops
* Presentation Decks
* Lab Provisioner

#### Examples

The content in `examples/` is the heart of what Lightbulb has to offer. They are complete Ansible playbooks that demonstrate the most fundamental features and most common use patterns.

These examples are an excellent educational reference for communicating how Ansible works in a clear, focused and consistent manner using recommended best practices.

This content is a great source for canned demos or something you can walk-thru to illustrate automating with Ansible to a group. Some of the examples  serve as the solutions to the workshops.

#### Workshops

The content of `workshops/` are a collection of Markdown documents and applicable resources for providing hands-on assignments for learning how to automate with Ansible.

Instructor notes on the execution and solution to all workshops can be found in `facilitator/solutions/`.

#### Presentation Decks

The content of `decks/` are collection of presentation decks using the [reveal.js framework](http://lab.hakim.se/reveal-js/) for delivering instructor-led or hands-on instruction.

#### Lab Provisioner

Lightbulb provides a lab provisioner utility for creating a personal lab environment for each student. Currently only Amazon Web Services (AWS) is supported in us-east-1 and us-west-1 with the foundation to support other regions in place.

### Requirements

True to its philosophy and The Ansible Way, Lightbulb has been developed so that using Lightbulb is as simple and low-overhead as possible. Requirements depend on the format and delivery of the Lightbulb content.

* Modern HTML5 Standard Compliant Web Browser
* A recent stable version of Python 2.7 and the latest stable version of the boto libraries.
* The latest stable versions of Ansible.
* A SSH client such as PuTTY or Mac OSX Terminal.
* An AWS account or local Vagrant setup.

#### Assumed Knowledge

For hands-on or self-paced training, students should have working knowledge of using SSH and command line shell (BASH). The ability to SSH from their personal laptop to a lab environment hosted in a public cloud can also be required based on the format and presentation of the context.

For demos and instructor-led exercises, conceptual understanding of linux system admin, DevOps and distributed application architecture is all that is required.

### Reference

* [Ansible Documentation](http://docs.ansible.com)
* [Ansible Best Practices: The Essentials](https://www.ansible.com/blog/ansible-best-practices-essentials)

### License

Red Hat, the Shadowman logo, Ansible, and Ansible Tower are trademarks or registered trademarks of Red Hat, Inc. or its subsidiaries in the United States and other countries.

All other parts of Ansible Lightbulb are made available under the terms of the [MIT License](LICENSE).
