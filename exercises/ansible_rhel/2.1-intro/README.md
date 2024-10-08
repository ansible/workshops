# Workshop Exercise - Introduction to Ansible Automation Platform

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table of Contents

* [What is Ansible Automation Platform (AAP)?](#what-is-ansible-automation-platform-aap)
* [Why Use Ansible Automation Platform?](#why-use-ansible-automation-platform)
* [Ansible Automation Controller](#ansible-automation-controller)
* [Event-Driven Ansible](#event-driven-ansible)
* [Automation Hub](#automation-hub)
* [What’s New in Ansible Automation Platform?](#whats-new-in-ansible-automation-platform)
* [Conclusion](#conclusion)

---

## What is Ansible Automation Platform (AAP)?

Ansible Automation Platform (AAP) is a comprehensive automation solution that provides a scalable framework for automating tasks across IT environments. It integrates various components, including automation controller, Event-Driven Ansible and automation hub offering users a unified platform for managing, executing, and orchestrating automation workflows.

AAP simplifies the complexity of IT automation by providing the tools necessary to accelerate the automation process, whether you're just getting started or scaling automation across teams and environments.

## Why Use Ansible Automation Platform?

1. **Scalable Automation**: Automate tasks of any complexity across on-premise, cloud, or hybrid environments. AAP enables teams to manage their automation consistently and efficiently at scale.
   
2. **Unified Experience**: AAP brings together automation controller, Event-Driven Ansible, and automation hub under one platform providing users with a cohesive, integrated experience for developing and managing automation.

3. **Increased Productivity**: With tools for automation content creation, testing, and deployment, AAP helps users across different skill levels work more efficiently. From automation architects to operators, it empowers users to implement automation faster and with fewer errors.

4. **Enhanced Security and Governance**: AAP supports role-based access control (RBAC), ensuring that only authorized users can create and execute automation. This security layer is crucial for maintaining compliance and governance across IT operations.

## Ansible Automation Controller

The **automation controller** is a key component of Ansible Automation Platform. It offers a web-based interface that provides a centralized point to manage, monitor, and control automation. 

### Key Features of Automation Controller:
- **User-Friendly Dashboard**: The controller’s dashboard offers a real-time view of recent job activity, managed hosts and hands-on quick starts to get you started as quickly as possible with Ansible Automation Platform.
- **Visual Workflow Management**: Easily create and modify automation workflows using the visualizer to visualize complex workflow streams.
- **RESTful API**: The platform includes an extensive REST API, which makes integration with other tools and platforms seamless.
- **Inventory and Credential Management**: Automation controller manages inventories and credentials securely, ensuring that only authorized users have access to sensitive data while simplifying configuration.

### Core Concepts:
- **Projects**: Logical collections of Ansible assets such as collections, roles and playbooks stored in a version control system.
- **Inventories**: Collections of hosts against which automation tasks are run. Inventories can be manually defined or dynamically synchronized.
- **Credentials**: Securely stored credentials for authentication when executing jobs against systems or integrating with third-party tools.
- **Job Templates**: Defined sets of parameters that allow for the consistent execution of automation jobs from an Ansible playbook.

## Event-Driven Ansible

**Event-Driven Ansible** is designed to bring intelligent automation into IT operations by responding to real-time events. By connecting to various event sources, Event-Driven Ansible can trigger automation workflows based on specific conditions, improving the efficiency of IT operations and ensuring faster response times.

### Key Features of Event-Driven Ansible:
- **Event-Driven Automation**: Automatically triggers Ansible Rulebooks based on real-time events.
- **Rulebooks**: Use Ansible Rulebooks to define conditional "if-this-then-that" logic, specifying the actions to take when certain events occur.
- **Integration with External Tools**: Event-Driven Ansible can be integrated with external monitoring and event sources like Prometheus, OpenShift, and cloud services to respond to system alerts or other events.
- **Customizable Event Sources**: Event-Driven Ansible supports a wide range of event sources and allows organizations to define custom event plugins.

### Core Concepts:
- **Event Sources**: The origin of the events that trigger automation, such as alerts, system logs, or user inputs.
- **Ansible Rulebooks**: Define conditions and actions to determine when and how to respond to specific events.
- **Actions**: Predefined responses, such as running playbooks or workflows that are executed when event conditions are met.

## Automation Hub

**Automation Hub** serves as the central repository for managing and
distributing Ansible content. It provides access to certified, validated and community-contributed Ansible collections allowing organizations to leverage automation solutions and share automation content across teams.

### Key Features of Automation Hub:
- **Content Management**: automation hub allows users to access and manage certified, validated and community-contributed content collections, including playbooks, roles, and modules, in one central location.
- **Certified Content**: Provides access to certified Ansible content supported by Red Hat, ensuring that organizations use secure, tested automation.
- **Validated Content**: Provides a set of collections containing pre-built YAML content (such as playbooks or roles) to address the most common automation use cases.
- **Private Automation Hub**: Organizations can create their own private automation hub to store and distribute custom automation content internally, offering control and security over automation assets.
- **Collection Repository Management**: Allows fine-grained control over who can access specific content, ensuring that only the right teams have access to the right resources.

### Core Concepts:
- **Collections**: Bundles of Ansible content (playbooks, roles, modules) that can be shared and reused across automation projects.
- **Certified Content**: Verified, secure content from Red Hat and partners, ensuring trust and reliability in automation implementations.
- **Private Automation Hub**: A self-hosted version of automation hub, where organizations can curate, store, and manage their own collections of automation content.

## What’s New in Ansible Automation Platform?

Ansible Automation Platform continually evolves to include new features and enhancements. Some of the latest advancements include:

1. **Unified User Interface**: A streamlined experience that integrates automation controller, Event-Driven Ansible, and automation hub, allowing users to access all tools through a single interface.
   
2. **Containerized Platform Installation**: AAP now supports containerized installation, making deployment easier for environments that require minimal overhead while maintaining the platform's full functionality.

3. **Enhanced Ansible Development Tools**: AAP includes a suite of tools that help developers and operators efficiently create, test, and deploy playbooks, improving productivity and standardization across the organization.

4. **AI-Assisted Automation**: With the integration of Red Hat Ansible Lightspeed, the platform offers generative AI capabilities to help users build automation playbooks more intuitively, even without deep coding expertise.

5. **Ansible Quick Starts**: Interactive, step-by-step guides within the UI help users quickly learn how to navigate and execute key functions within AAP.

## Conclusion

Ansible Automation Platform is designed to provide enterprises with the flexibility, security, and power they need to automate their IT infrastructure. Whether you are an automation beginner or looking to scale automation across complex environments, AAP offers a unified and robust solution to meet those needs.

For more information on Ansible Automation Platform and its latest features, explore the official [Red Hat Ansible Automation Platform website](https://www.redhat.com/en/technologies/automation/ansible).

---
**Navigation**
<br>
[Previous Exercise](../1.7-role) - [Next Exercise](../2.2-cred)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-2---ansible-tower-exercises)
