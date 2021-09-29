# Exercise 1 - Installing and Creating Collections

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
    - [Step 1: Installing collections from the command line](#step-1-installing-collections-from-the-command-line)
        - [Preparing the exercise environment](#preparing-the-exercise-environment)
        - [Installing in the default collections path](#installing-in-the-default-collections-path)
        - [Instaling in a custom collections path](#instaling-in-a-custom-collections-path)
        - [Inspecting the contents of the collection](#inspecting-the-contents-of-the-collection)
    - [Step 2: Creating collections from the command line](#step-2-creating-collections-from-the-command-line)
        - [Initializing the Git repository](#initializing-the-git-repository)
    - [Step 3: Adding custom modules and plugins to the collection](#step-3-adding-custom-modules-and-plugins-to-the-collection)
    - [Step 4: Adding custom roles to the collection](#step-4-adding-custom-roles-to-the-collection)
    - [Step 5: Building and installing collections](#step-5-building-and-installing-collections)
    - [Step 6: Testing collections locally](#step-6-testing-collections-locally)
        - [Running the test playbook](#running-the-test-playbook)
        - [Running the local container](#running-the-local-container)
- [Takeaways](#takeaways)

# Objective

This exercise will help users understand how collections are installed, created and customized.
Covered topics:

- Demonstrate the steps involved in the installation of an Ansible Collection from the
command line using the `ansible-galaxy` utility.
- Demonstrate the steps involved in the creation of a new collection with the `ansible-galaxy`
utility.
- Demonstrate the creation of a custom role inside the newly created collection.
- Demonstrate the creation of a new custom plugin (basic Ansible module) in the newly created collection.

# Guide

## Step 1: Installing collections from the command line

Ansible Collections can be searched and installed from Ansible Galaxy and Red Hat Automation Hub.
Once installed, a collection can be used locally and its plugins, modules, and roles can be imported
and executed in complex Ansible-based projects.

### Preparing the exercise environment

Create a directory in your lab named `dir_name` and cd into it. This directory will be used during the
whole exercise.

```bash
mkdir exercise-01
cd exercise-01
```

Collection have two default lookup paths that are searched:

- User scoped path `/home/<username>/.ansible/collections`

- System scoped path `/usr/share/ansible/collections`

> **TIP**: Users can customized the collections path by modifying the `collections_path` key in the
> `ansible.cfg` file or by setting the environment variable `ANSIBLE_COLLECTIONS_PATHS` with the desired
> search path.

### Installing in the default collections path

First, we demonstrate how to install a collection in the user scoped path.For the sake of simplicity we are going to use the collection [newswangerd.collection_demo](https://galaxy.ansible.com/newswangerd/collection_demo), a basic collection created for demo purposes.

It contains basic roles and a very simple module and is a good example to understand how a collection works without getting involved in modules or roles logic.

Install the collection using the command `ansible galaxy collection install` with no extra options:

```bash
$ ansible-galaxy collection install newswangerd.collection_demo
Process install dependency map
Starting collection install process
Installing 'newswangerd.collection_demo:1.0.10' to '/home/<username>/.ansible/collections/ansible_collections/newswangerd/collection_demo'
```

The collection is now installed in the user home directory and can be used in playbooks and roles.

### Instaling in a custom collections path

Install the collection in the current working directory using the `-p` flag followed by the custom installation path.

```bash
ansible-galaxy collection install -p . newswangerd.collection_demo
```

> **NOTE**: When installing on custom paths not included in the collections search path a standard warning message is issued:
>
> ```bash
>  [WARNING]: The specified collections path '/home/gbsalinetti/Labs/collections-lab' is not part of the configured Ansible collections paths
> '/home/gbsalinetti/.ansible/collections:/usr/share/ansible/collections'. The installed collection won't be picked up in an Ansible run.
> ```

The installed path follows the standard pattern `ansible_collections/<author>/<collection>`.

Run the `tree` command to inspect the contents:

```bash
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

```bash
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

## Step 2: Creating collections from the command line

Users can create their own collections and populate them with roles, playbook, plugins and modules.
User defined collections skeleton can be created manually or it can be authored with the
`ansible-galaxy collection init` command. This will create a standard skeleton that can be
customized lately.

Create the following collection:

```bash
ansible-galaxy collection init --init-path ansible_collections redhat.workshop_demo_collection
```

The `--init-path` flag is used to define a custom path in which the skeleton will be initialized.
The collection name always follows the pattern `<namespace.collection>`. The above example creates
the `workshop_demo_collection` in the `redhat` namespace.

The command created the following skeleton:

```bash
$ tree ansible_collections/redhat/workshop_demo_collection/
ansible_collections/redhat/workshop_demo_collection/
├── docs
├── galaxy.yml
├── plugins
│   └── README.md
├── README.md
└── roles
```

The skeleton is really minimal. Besides the template README files, a template `galaxy.yml` file is created to define Galaxy metadata.

### Initializing the Git repository

A good practice is, necessary if we want to publish our collection in Galaxy, is to initialize
a Git repository in the collection.

```bash
cd ansible_collections/redhat/workshop_demo_collection && git init .
```

When changed, files will be added to the staging area with the `git add` and committed with
the `git commit` commands.

To publish the collection on GitHub a remote should be added:

```bash
git remote add origin https://github.com/<user>/workshop_demo_collection.git
```

The `workshop_demo_collection` repository must be already present on GitHub. To create a new repository follow the official GitHub [documentation](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-new-repository).

## Step 3: Adding custom modules and plugins to the collection

Collections can be customized with different kinds of plugins and modules. For a complete list please refer to the `README.md` file in the `plugins` folder.

In this workshop we are going to create a minimal *Hello World* module and install it in the `plugins/modules` directory.

First, create the `plugins/modules` directory:

```bash
cd ansible_collections/redhat/workshop_demo_collection
mkdir plugins/modules
```

Create the `demo_hello.py` module in the new folder. The module code is available in the `solutions/modules`
folder of this exercise.

```bash
cp <path_to_workshop_repo>/workshops/exercises/ansible_collections/1-create-collections/modules/demo_hello.py plugins/modules/
```

The `demo_hello` module says Hello in different languages to custom defined users. Take your time to look at the module code and understand its behavior.

```bash
#!/usr/bin/python


ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: demo_hello
short_description: A module that says hello in many languages
version_added: "2.8"
description:
  - "A module that says hello in many languages."
options:
    name:
        description:
          - Name of the person to salute. If no value is provided the default
            value will be used.
        required: false
        type: str
        default: John Doe
author:
    - Gianni Salinetti (@giannisalinetti)
'''

EXAMPLES = '''
# Pass in a custom name
- name: Say hello to Linus Torwalds
  demo_hello:
    name: "Linus Torwalds"
'''

RETURN = '''
fact:
  description: Hello string
  type: str
  sample: Hello John Doe!
'''

import random
from ansible.module_utils.basic import AnsibleModule


FACTS = [
    "Hello {name}!",
    "Bonjour {name}!",
    "Hola {name}!",
    "Ciao {name}!",
    "Hallo {name}!",
    "Hei {name}!",
]


def run_module():
    module_args = dict(
        name=dict(type='str', default='John Doe'),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result = dict(
        changed=False,
        fact=''
    )

    result['fact'] = random.choice(FACTS).format(
        name=module.params['name']
    )

    if module.check_mode:
        return result

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
```

An Ansible module is basically an implementation of the AnsibleModule class created and executed in a minimal function called `run_module()`. As you can see, a module has a `main()` function, like a plain Python executable. Anyway, it is
not meant to be executed independently.

## Step 4: Adding custom roles to the collection

The last step of this exercise will be focused on a role creation inside the custom collection. We will deploy a basic role that uses the previous module to dynamically generates greetings inside an index.html and build it inside an OCI image with podman. The image will be finally pushed into a customizable private registry.

> **TIP**: If you want to speed up the lab you can copy the completed role from the exercise `solutions/roles` folder.

Generate the new role skeleton using the `ansible-galaxy init` command:

```bash
ansible-galaxy init --init-path roles demo_image_builder
```

Create the following tasks in the `roles/demo_image_builder/tasks/main.yml` file:

```yaml
---
# tasks file for demo_image_builder
- name: Ensure podman is present in the host
  dnf:
    name: podman
    state: present
  become: true

- name: Generate greeting and store result
  demo_hello:
    name: "{{ friend_name }}"
  register: demo_greeting

- name: Create build directory
  file:
    path: "{{ build_dir_path }}"
    state: directory
    mode: 0755

- name: Copy Dockerfile
  copy:
    src: files/Dockerfile
    dest: "{{ build_dir_path }}"
    mode: 0644

- name: Copy custom index.html
  template:
    src: templates/index.html.j2
    dest: "{{ build_dir_path }}/index.html"
    mode: 0644

- name: Build and Push OCI image
  podman_image:
    name: demo-nginx
    path: "{{ build_dir_path }}"
    build:
      annotation:
        app: nginx
        function: demo
        info: Demo app for Ansible Collections workshop
      format: oci
    push: true
    force: true
    push_args:
      dest: "{{ image_registry }}/{{ registry_username }}"
```

Notice the usage of the `demo_hello` module, installed in the collection, to generate the greeting string.

> **NOTE**: When a collection role calls a module in the same collection namespace, the module is automatically resolved.

Create the following variables in the `roles/demo_image_builder/defaults/main.yml`:

```yaml
---
# defaults file for demo_image_builder
friend_name: "John Doe"
build_dir_path: "/tmp/demo_nginx_build"
image_registry: "quay.io"
registry_username: ""
```

Create the Dockerfile used in the build process in the `roles/demo_image_builder/files/` folder:

```bash
cat > roles/demo_nginx/files/ << EOF
FROM nginx
COPY index.html /usr/share/nginx/html
EOF
```

Create the index.html.j2 file which acts as a Jinja2 template in `roles/demo_image_builder/templates/` folder:

```bash
cat > roles/demo_image_builder/templates/index.html.j2 << EOF
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title>Ansible Collections Workshop</title>
  <meta name="description" content="Demo Nginx">
  <meta name="author" content="gsalinet@redhat.com">

  <link rel="stylesheet" href="css/styles.css?v=1.0">

</head>

<body>
  <h1>
    {{ demo_greeting.fact }}
  </h1>
</body>
</html>
EOF
```

The skeleton generates a complete structure files and folder. We can clean up the unused ones:

```bash
rm -rf roles/demo_image_builder/{handlers,vars,tests}
```

Customize the `roles/demo_image_builder/meta/main.yml` file to define Galaxy metadata and potential dependencies of the role. Use this sample minimal content:

```yaml
galaxy_info:
  author: Ansible Automation Platform Hackathon Team
  description: Basic builder role based on podman
  company: Red Hat

  license: Apache-2.0

  min_ansible_version: 2.8


  platforms:
    - name: Fedora
      versions:
      - 31
      - 32
      - 33

  galaxy_tags: ["demo", "podman"]

dependencies: []
```

## Step 5: Building and installing collections

Once completed the creation task we can build the collection and generate a .tar.gz file that can be installed locally or uploaded to Galaxy.

From the collection folder run the following command:

```bash
ansible-galaxy collection build
```

The above command will create the file `redhat-workshop_demo_collection-1.0.0.tar.gz`. Notice the semantic x.y.z versioning.

Once created the file can be installed in the `COLLECTIONS_PATH` to be tested locally:

```bash
ansible-galaxy collection install redhat-workshop_demo_collection-1.0.0.tar.gz
```

By default the collection will be installed in the `~/.ansible/collections/ansible_collections` folder. Now the collection can be tested locally.

## Step 6: Testing collections locally

Create the `exercise-01/collections_test` folder to execute the local test:

```bash
cd ..
mkdir collections_test
```

Create a basic `playbook.yml` file with the following contents:

```bash
cat > playbook.yml << EOF
---
- hosts: localhost
  remote_user: root
  vars:
    image_registry: quay.io
    registry_username: <YOUR_USERNAME>
    friend_name: Heisenberg
  tasks:
    - import_role:
        name: redhat.workshop_demo_collection.demo_image_builder
EOF
```

Replace the `<YOUR_USERNAME>` field with a valid quay.io username.
Before running the test playbook, be sure to have a valid auth token to authenticate to the registry. You can authenticate by running the following command and passing valid credentials that will generate a token stored in the `~/.docker/config.json` file:

```bash
podman login quay.io
```

### Running the test playbook

Run the test playbook. Since some tasks require privilege escalation use the `-K` option to authenticate via sudo.

```bash
$ ansible-playbook playbook.yml -K
BECOME password:
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [localhost] **************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ********************************************************************************************************************************************************************************************
ok: [localhost]

TASK [redhat.workshop_demo_collection.demo_image_builder : Ensure podman is present in the host] ******************************************************************************************************************
ok: [localhost]

TASK [redhat.workshop_demo_collection.demo_image_builder : Generate greeting and store result] ********************************************************************************************************************
ok: [localhost]

TASK [redhat.workshop_demo_collection.demo_image_builder : Create build directory] ********************************************************************************************************************************
ok: [localhost]

TASK [redhat.workshop_demo_collection.demo_image_builder : Copy Dockerfile] ***************************************************************************************************************************************
ok: [localhost]

TASK [redhat.workshop_demo_collection.demo_image_builder : Copy custom index.html] ********************************************************************************************************************************
changed: [localhost]

TASK [redhat.workshop_demo_collection.demo_image_builder : Build and Push OCI image] ***************************************************************************************************************************************
changed: [localhost]

PLAY RECAP ********************************************************************************************************************************************************************************************************
localhost                  : ok=7    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

### Running the local container

Locally test the built container image with podman to demonstrate the expected behavior
of the collection's module and role.

```bash
podman run -d --rm -d -p 8080:80 localhost/demo-nginx
```

Test the nginx web server and inspect the body section to find the generated string in the h1 section.

```bash
$ curl localhost:8080
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title>Ansible Collections Workshop</title>
  <meta name="description" content="Demo Nginx">
  <meta name="author" content="gsalinet@redhat.com">

  <link rel="stylesheet" href="css/styles.css?v=1.0">

</head>

<body>
  <h1>
    Hei Heisenberg!
  </h1>
</body>
</html>
```

# Takeaways

- Collections can be installed from Galaxy of from Red Hat Automation Hub. Default collections search paths or custom paths can be used.

- Collections can be created using the `ansible-galaxy collection init` command. Users can develop collections contents accordingly to their needs and business logic.

- Collections plugins can be either any kind of Ansible plugins or modules. Modules are often developed inside collection to create an autonomous lifecycle from the main Ansible upstream.

- Collection roles can use local collections plugins and modules.

----
**Navigation**
<br>
[Next Exercise](../2-collections-from-playbook)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md)
