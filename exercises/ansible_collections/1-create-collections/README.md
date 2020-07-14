# Exercise 1 - Installing and Creating Collections

## Table of Contents
- [Objective](#objective)
- [Guide](#guide)
    - [Step 1: Installing collection from the command line](#step-1-installing-collections-from-the-command-line)
    - [Step 2: Creating collections from the command line](#step-2-creating-collections-from-the-command-line)
    - [Step 2: Creating custom roles](#step-2-creating-custom-roles)
    - [Step 3: Creating custom plugins](#step-3-creating-custom-plugins)
- [Takeaways](#takeaways)

# Objective
This exercise will help users understand how collections are installed, created and customized.
Covered topics:

- Demonstrate the steps involved in the installation of an Ansible Collection from the
command line using the `ansible-galaxy` utility.
- Demonstrate the steps involved in the creation of a new collectoin with the `ansible-galaxy`
utility.
- Demonstrate the creation of a custom role inside the newly created collection.
- Demonstrate the creation of a new custom plugin (basic Ansible module) in the newly created collection.

# Guide

## Installing collections from the command line
Create a directory in your lab named `dir_name` and cd into it. This directory will be used during the
whole exercise.
```
$ mkdir exercise-01
$ cd exercise-01
```

Collection have two default lookup paths that are searched:
- User scoped path `/home/<username>/.ansible/collections`
- System scoped path `/usr/share/ansible/collections`

> **TIP**: Users can customized the collections path by modifying the `collections_path` key in the
> `ansible.cfg` file or by setting the environment variable `ANSIBLE_COLLECTIONS_PATHS` with the desidered
> search path.

### Installing in the default collections path
First, we demonstrate how to install a collection in the user scoped path. 
For the sake of simplicity we are going to use the collection `newswangerd.collection_demo` (https://galaxy.ansible.com/newswangerd/collection_demo),
a basic collection created for demo purposes.   
It contains basic roles and a very simple module and is a good example to understand how a collection works without getting involved in modules or roles logic.
  
Intall the collection using the command `ansible galaxy collection install` with no extra options:
```
$ ansible-galaxy collection install newswangerd.collection_demo
Process install dependency map
Starting collection install process
Installing 'newswangerd.collection_demo:1.0.10' to '/home/<username>/.ansible/collections/ansible_collections/newswangerd/collection_demo'
```

The collection is now installed in the user home directory and can be used in playbooks and roles.

### Instaling in a custom collections path
Install the collection in the current working directory using the `-p` flag followed by the custom installation path.
```
$ ansible-galaxy collection install -p . newswangerd.collection_demo
```

> **NOTE**: When installing on custom paths not included in the collections search path a standard warning message is issued:
>  ```
>  [WARNING]: The specified collections path '/home/gbsalinetti/Labs/collections-lab' is not part of the configured Ansible collections paths
> '/home/gbsalinetti/.ansible/collections:/usr/share/ansible/collections'. The installed collection won't be picked up in an Ansible run.
>  ```

The installed path follows the standard pattern `ansible_collections/<author>/<collection>`. 
Run the `tree` command to inspect the contents:
```
$ tree
.
└── ansible_collections
    └── newswangerd
        └── collection_demo
            ├── docs
            │   └── test_guide.md
            ├── FILES.json
            ├── MANIFEST.json
            ├── plugins
            │   └── modules
            │       └── real_facts.py
            ├── README.md
            ├── releases
            │   ├── newswangerd-collection_demo-1.0.0.tar.gz
            │   ├── newswangerd-collection_demo-1.0.1.tar.gz
            │   ├── newswangerd-collection_demo-1.0.2.tar.gz
            │   ├── newswangerd-collection_demo-1.0.3.tar.gz
            │   ├── newswangerd-collection_demo-1.0.4.tar.gz
            │   └── newswangerd-collection_demo-1.0.5.tar.gz
            └── roles
                ├── deltoid
                │   ├── meta
                │   │   └── main.yaml
                │   ├── README.md
                │   └── tasks
                │       └── main.yml
                └── factoid
                    ├── meta
                    │   └── main.yaml
                    ├── README.md
                    └── tasks
                        └── main.yml

```

### Inspecting the contents of the collection
Collections have a standard structure that can can hold modules, plugins, roles and playbooks. 
```
collection/
├── docs/
├── galaxy.yml
├── plugins/
│   ├── modules/
│   │   └── module1.py
│   ├── inventory/
│   └── .../
├── README.md
├── roles/
│   ├── role1/
│   ├── role2/
│   └── .../
├── playbooks/
│   ├── files/
│   ├── vars/
│   ├── templates/
│   └── tasks/
└── tests/
```

A short description of the collection structure:

- The `plugins` folder holds plugins, modules, and module_utils that can be reused in playbooks and roles.  
- The `roles` folder hosts custom roles, while all collection playbooks must be stored in the `playbooks` folder.  
- The `docs` folder can be used for the collections documentation, as well as the main `README.md` file that is 
  used to describe the collection and its content.
- The `tests` folder holds tests written for the collection.  
- The `galaxy.yml` file is a YAML text file that contains all the metadata used in the Ansible Galaxy hub to index the collection.
  It is also used to list collection dependencies, if there are any.

When a collection is downloaded with the `ansible-galaxy collection install` two more files are installed:
- `MANIFEST.json`, holding additional Galaxy metadata in JSON format.
- `FILES.json`, a JSON object containing all the files SHA256 checksum.

## Creating collections from the command line
Users can create their own collections and populate them with roles, playbook, plugins and modules.
User defined collections skeleton can be created manually or it can be authored with the 
`ansible-galaxy collection init` command. This will create a standard skeleton that can be 
customized lately.

Create the following collection:
```
$ ansible-galaxy collection init --init-path ansible_collections redhat.workshop_demo_collection 
```

The `--init-path` flag is used to define a custom path in which the skeleton will be initialized.  
The collection name always follows the pattern `<namespace.collection>`. The above example creates
the `workshop_demo_collection` in the `redhat` namespace.

The command created the following skeleton:
```
$ tree ansible_collections/redhat/workshop_demo_collection/
ansible_collections/redhat/workshop_demo_collection/
├── docs
├── galaxy.yml
├── plugins
│   └── README.md
├── README.md
└── roles
```

The skeleton is really minimal. Besides the template README files, a template `galaxy.yml` file 
is created to define Galaxy metadata.

### Initializing the Git repository
A good practice is, necessary if we want to publish our collection in Galaxy, is to initialize
a Git repository in the collection. 
```
$ cd ansible_collections/redhat/workshop_demo_collection && git init .
```

When changed, files will be added to the staging area with the `git add` and committed with 
the `git commit` commands.

To publish the collection on GitHub a remote should be added:
```
$ git remote add origin https://github.com/<user>/workshop_demo_collection.git
```

The `workshop_demo_collection` repository must be already present on GitHub. To create a new 
repository follow the official GitHub [documentation](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-new-repository).

## Creating custom roles

## Creating custom plugins

# Takeaways
