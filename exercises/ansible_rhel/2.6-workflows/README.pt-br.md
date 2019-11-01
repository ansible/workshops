# Exercício 2.6 - Workflows

**Leia em outras linguagens**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

# Ansible Tower Workflows

Os workflows foram introduzidos como um novo recurso importante no Ansible Tower 3.1. A ideia básica de um workflow é vincular vários job templates. Eles podem ou não compartilhar inventário, Playbooks ou mesmo permissões. Os links podem ser condicionais:

  - se o job template A for bem-sucedido, o job template B será automaticamente executado posteriormente

  - mas em caso de falha, o job template C será executado.
  
E os workflows não se limitam aos job templates, mas também podem incluir atualizações de projeto ou inventário.

Isso permite novas aplicações para o Tower: diferentes job templates podem ser criados entre si. Por exemplo. a equipe de rede cria playbooks com seu próprio conteúdo, em seu próprio repositório Git e até direciona seu próprio inventário, enquanto a equipe de operações também possui seus próprios repositórios, playbooks e inventário.

Neste laboratório, você aprenderá como configurar um workflow.

## Cenário de laboratório

Você tem dois departamentos em sua organização:

  - A equipe de operações que está desenvolvendo Playbooks em seu próprio repositório Git.
  
  - A equipe de aplicações, que desenvolve aplicativos web em JSP para o Tomcat em seu repositório Git.

Quando há um novo servidor Tomcat para implantar, duas coisas precisam acontecer:

  - O Tomcat precisa estar instalado, o firewall precisa ser aberto e o start no Tomcat.
  
  - A versão mais recente do aplicação web precisa ser implantada.

Para tornar as coisas um pouco mais fáceis para você, tudo o que é necessário já existe nos repositórios do Git: Playbooks, arquivos JSP etc. Você só precisa colá-los.

> **Nota**
>
> Neste exemplo, assumimos dois repositórios Git diferentes, mas, na realidade, acessaremos duas branches diferentes do mesmo repositório.

## Configurando o projeto

Primeiro, você precisa configurar o repositório Git como Projetos. Você já fez isso antes, tente fazer isso sozinho. Instruções detalhadas podem ser encontradas abaixo.

> **ATENÇÃO**
> 
> **Se você ainda estiver logado como usuário **wweb**, efetue logout e faça login como usuário **admin** novamente.**

- Crie o projeto para operações:

  - Deve ser nomeado **Webops Git Repo**

  - O URL para acessar o repositório é **https://github.com/ansible/workshop-examples.git**

  - O **SCM BRANCH/TAG/COMMIT** é **webops**

- Crie o projeto para os desenvolvedores:

  - Deve ser nomeado como **Webdev Git Repo**

  - The URL to access the repo is **https://github.com/ansible/workshop-examples.git**

  - The **SCM BRANCH/TAG/COMMIT** is **webdev**

> **Warning**
> 
> **Solution Below**

- Create the project for web operations. In the **Projects** view click the green plus button and fill in:
  
    - **NAME:** Webops Git Repo
  
    - **ORGANIZATION:** Default
  
    - **SCM TYPE:** Git
  
    - **SCM URL:** https://github.com/ansible/workshop-examples.git

    - **SCM BRANCH/TAG/COMMIT:** webops
  
    - **SCM UPDATE OPTIONS:** Tick all three boxes.

- Click **SAVE**

- Create the project for the application developers. In the **Projects** view click the green plus button and fill in:
  
    - **NAME:** Webdev Git Repo
  
    - **ORGANIZATION:** Default
  
    - **SCM TYPE:** Git
  
    - **SCM URL:** https://github.com/ansible/workshop-examples.git
  
    - **SCM BRANCH/TAG/COMMIT:** webdev

    - **SCM UPDATE OPTIONS:** Tick all three boxes.

- Click **SAVE**

## Set up Job Templates

Now you have to create Job Templates like you would for "normal" Jobs.

  - Go to the **Templates** view, click the green plus button and choose **Job Template**:
    
      - **NAME:** Tomcat Deploy
    
      - **JOB TYPE:** Run
    
      - **INVENTORY:** Workshop Inventory
    
      - **PROJECT:** Webops Git Repo
    
      - **PLAYBOOK:** `rhel/webops/tomcat.yml`
    
      - **CREDENTIAL:** Workshop Credentials
    
      - **OPTIONS:** Enable privilege escalation

  - Click **SAVE**

  - Go to the **Templates** view, click the green plus button and choose **Job Template**:
    
      - **NAME:** Web App Deploy
    
      - **JOB TYPE:** Run
    
      - **INVENTORY:** Workshop Inventory
    
      - **PROJECT:** Webdev Git Repo
    
      - **PLAYBOOK:** `rhel/webdev/create_jsp.yml`
    
      - **CREDENTIALS:** Workshop Credentials
    
      - **OPTIONS:** Enable privilege escalation

  - Click **SAVE**

> **Tip**
> 
> If you want to know what the Playbooks look like, check out the Github URL and switch to the appropriate branches.

## Set up the Workflow

And now you finally set up the workflow. Workflows are configured in the **Templates** view, you might have noticed you can choose between **Job Template** and **Workflow Template** when adding a template so this is finally making sense.

  - Go to the **Templates** view and click the the green plus button. This time choose **Workflow Template**
    
      - **NAME:** Deploy Webapp Server
    
      - **ORGANIZATION:** Default

  - Click **SAVE**

  - Now the **WORKFLOW VISUALIZER** button becomes active, click it to start the graphical editor.

  - Click on the **START** button, a new node opens. To the right you can assign an action to the node, you can choose between **JOBS**, **PROJECT SYNC** and **INVENTORY SYNC**.

  - In this lab we’ll link Jobs together, so select the **Tomcat Deploy** job and click **SELECT**.

  - The node gets annotated with the name of the job. Hover the mouse pointer over the node, you’ll see a red **x** and a green **+** signs appear.

> **Tip**
> 
> Using the red "x" allows you to remove the node, the green plus lets you add the next node.

  - Click the green **+** sign

  - Choose **Web App Deploy** as the next Job (you might have to switch to the next page)

  - Leave **Type** set to **On Success**

> **Tip**
> 
> The type allows for more complex workflows. You could lay out different execution paths for successful and for failed Playbook runs.

  - Click **SELECT**

  - Click **SAVE** in the **WORKFLOW VISUALIZER** view

  - Click **SAVE** in the **Workflow Template** view

## And Action

Your workflow is ready to go, launch it.

  - Click the blue **LAUNCH** button directly or go to the the **Templates** view and launch the **Deploy Webapp Server** workflow by clicking the rocket icon.

![jobs view of workflow](images/job_workflow.png)

Note how the workflow run is shown in the job view. In contrast to a normal job template job execution this time there is no playbook output on the right, but a visual representation of the different workflow steps. If you want to look at the actual playbooks behind that, click **DETAILS** in each step. If you want to get back from a details view to the corresponding workflow, click the ![w-button](images/w_button.png) in the **JOB TEMPLATE** line in the **DETAILS** part on the left side of the job overview.

After the job was finished, check if everything worked fine: log into `node1`, `node2` or `node3` from your control host and run:

```bash
$ curl http://localhost:8080/coolapp/
```

> **Tip**
> 
> You might have to wait a couple of minutes until Tomcat answers requests.

----

[Clique aqui para retornar ao Workshop Ansible for Red Hat Enterprise Linux](../README.pt-br.md#seção-2---exercícios-do-ansible-tower)
