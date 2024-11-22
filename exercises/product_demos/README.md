# Ansible Product Demos

The `Ansible Product Demos` is a Git project that acts as a centralized location for Ansible Product Demos. This project is a collection of use cases implemented with Ansible for use with the Ansible Automation Platform.

This project aims to be an agnostic catalog of automation `Job Templates` that any Red Hat employee, partner, customer or community member can use and contribute to to quickly preload into any Ansible Automation Platform installation.  This differs from workshops that are very perscriptive and opiniated ways to teach Ansible Automation Platform.  This should allow anyone to easily create a job template, and allow any other person to use that very easily.

There are two major components:

- [github.com/ansible/product-demos](https://github.com/ansible/product-demos) - Github Repo open to anyone.  You can "bring your own AAP" and install the repo, which can then install other job templates and workflows to demo use-cases.
- [https://red.ht/apd-sandbox](https://red.ht/apd-sandbox) - This is a demo enviornment (For Red Hat Employees only) that provisions a Red Hat OpenShift cluster with Ansible Automation Platform pre-installed.  This will auto-load the product-demos repository and let you quickly concentrate on demos versus having to build your own AAP environment or home-lab.