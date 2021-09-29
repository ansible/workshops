# Exercício - Projects & job templates

**Leia em outras linguagens**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

* [Configurando o repositório Git](#configurando-o-repositório-git)
* [Criando o projeto](#criando-o-projeto)
* [Criando um job template e executando um job](#criando-um-job-template-e-executando-um-job)
* [Laboratório de Desafios: Confira o Resultado](#laboratório-de-desafios-confira-o-resultado)
* [E quanto a alguma prática?](#e-quanto-a-alguma-prática)

O **Project** é uma coleção lógica de Playbooks. Você pode gerenciar seus playbooks colocando-os em um sistema de gerenciamento de código-fonte (SCM) suportado pelo Tower, incluindo Git, Subversion e Mercurial.

Você definitivamente deve manter seus Playbooks sob controle de versão. Neste laboratório, usaremos Playbooks mantidos em um repositório Git.

## Configurando o repositório Git

Para esta demonstração, usaremos playbooks armazenados em um repositório Git:

**https://github.com/ansible/workshop-examples**


Um Playbook para instalar o servidor Apache já foi confirmado no diretório **rhel/apache**, `apache_install.yml`:

```yaml
---
- name: Instalado apache server
  hosts: all

  tasks:
  - name: Ultima versao do apache instalada
    yum:
      name: httpd
      state: latest

  - name: Ultima versão do firewalld instalada
    yum:
      name: firewalld
      state: latest

  - name: Firewalld ativado e em execucao
    service:
      name: firewalld
      enabled: true
      state: started

  - name: Firewalld permite o servico http
    firewalld:
      service: http
      permanent: true
      state: enabled
      immediate: yes

  - name: Apache ativado e em execucao
    service:
      name: httpd
      enabled: true
      state: started
```

> **Dica**
>
> Compare e observe a diferença entre outros Playbooks que você pode ter escrito\! O mais importante é que não há `become`, e` hosts` está definido como `all`.

Para configurar e usar este repositório como um sistema **Source Control Management (SCM)** no Tower, é necessário criar um **Project** que use o repositório.

## Criando o projeto

  - Vá para **RESOURCES → Projects** na visualização do menu lateral, clique no botão ![plus](images / green_plus.png). Preencha o formulário:

  - **NAME:** Exemplos Ansible Workshop

  - **ORGANIZATION:** Default

  - **SCM TYPE:** Git

Agora você precisa do URL para acessar o repositório. Vá para o repositório do Github mencionado acima, escolha o botão verde **Clone or download** à direita, clique em **Use https** e copie o URL HTTPS.

> **Nota**
>
> Se não houver **Use https** para clicar, basta copiar o URL. O importante é que você copie o URL começando com **https**.

Digite o URL na configuração do projeto:

- **SCM URL:** `https://github.com/ansible/workshop-examples.git`

- **SCM UPDATE OPTIONS:** Marque todas as três caixas para sempre obter uma cópia nova do repositório e atualizar o repositório ao iniciar um trabalho.

- Click em **SAVE**

O novo projeto será sincronizado automaticamente após a criação. Mas você também pode fazer isso: Sincronize o projeto novamente com o repositório Git, indo para a visualização **Projects** e clicando na seta circular **Get latest SCM revision** à direita do projeto.

Após iniciar o trabalho de sincronização, vá para a exibição **Jobs**: há um novo trabalho para a atualização do repositório Git.

## Criando um job template e executando um job

Um Job template é uma definição e um conjunto de parâmetros para executar um job. Job templates são úteis para executar o mesmo trabalho várias vezes. Portanto, antes de executar um  **Job** no Tower, você deve criar um **Job Template** que reúne:

- **Inventory**: Em quais hosts o job deve ser executado?

- **Credentials** Quais credenciais são necessárias para efetuar login nos hosts?

- **Project**: Onde está o playbook?

- **What** Playbook é para usar?

Ok, vamos fazer isso: vá para a visualização **Templates**, clique no botão ![plus](images/green_plus.png) e escolha **Job template**.

> **Dica**
>
> Lembre-se que você pode clicar nas lupas para obter uma visão geral das opções a serem selecionadas para preencher os campos.

- **NAME:** Instalar Apache

- **JOB TYPE:** Run

- **INVENTORY:** Inventario Workshop

- **PROJECT:** Exemplos Ansible Workshop

- **PLAYBOOK:** `rhel/apache/apache_install.yml`

- **CREDENTIAL:** Credenciais Workshop

- Precisamos executar as tasks como root, marque **Enable privilege escalation**

- Click em **SAVE**

Você pode iniciar o trabalho clicando diretamente no botão azul **LAUNCH**, ou clicando no foguete na visão geral de Job Template. Depois de iniciar o Job Template, você é automaticamente levado para a visão geral do job, onde pode acompanhar a execução do playbook em tempo real:

![job exection](images/job_overview.png)

Como isso pode levar um tempo, verifique todos os detalhes fornecidos:

- Todos os detalhes do job template, como inventário, projeto, credenciais e playbooks, são mostrados.

- Além disso, a revisão real do playbook é registrada aqui - isso facilita a análise das execuções de tasks posteriormente.

- O tempo de execução com o horário de início e término é registrado, fornecendo uma ideia de quanto tempo realmente durou uma execução do job.

- No lado direito, a saída da execução do Playbook é mostrada. Clique em um nó abaixo de uma task e veja que informações detalhadas são fornecidas para cada task de cada nó.

Após o término do job, vá para a tela principal **Jobs**: Todos os jobs são listados aqui, você deve ver diretamente antes do Playbook executar uma atualização do SCM. Esta é a atualização do Git que configuramos para o **Project** no lançamento\!

## Laboratório de Desafios: Confira o Resultado

É hora de um pequeno desafio:

  - Use um comando ad hoc nos dois hosts para garantir que o Apache esteja instalado e em execução.

Você já passou por todas as etapas necessárias, então tente isso por si mesmo.

> **Dica**
>
> E quanto ao `systemctl status httpd`?

> **ATENÇÃO**
>
> **Solução abaixo**

- Vá para **Inventories** → **Inventario Workshop**

- Em **HOSTS**, selecione os dois hosts e clique em **RUN COMMANDS**

- **MODULE:** command

- **ARGUMENTS:** systemctl status httpd

- **MACHINE CREDENTIALS:** Credenciais Workshop

- Click em **LAUNCH**

## E quanto a alguma prática?

Aqui está uma lista de tasks:

> **ATENÇÃO**
>
> Certifique-se de concluir estas etapas, pois o próximo capítulo depende disso\!

- Crie um novo inventário chamado `Webserver` e coloque apenas `node1` fazendo parte dele.

- Copie o template `Instalar Apache` usando o ícone de cópia na visualização **Templates**.

- Mude o nome para `Instalar o apache ask`

- Altere a configuração **INVENTORY** do projeto para solicitar o inventário no lauch

- **Salve**

- Inicie o template `Instalar Apache Ask`.

- Agora ele solicitará o inventário a ser usado, escolha o inventário do `Webserver` e clique em **LAUNCH**

- Aguarde até o job terminar e verifique se ele é executado apenas no `node1`

> **Dica**
>
> O Job não mudou nada porque o Apache já estava instalado na versão mais recente.

----

[Clique aqui para retornar ao Workshop Ansible for Red Hat Enterprise Linux](../README.pt-br.md#seção-2---exercícios-do-ansible-tower)
