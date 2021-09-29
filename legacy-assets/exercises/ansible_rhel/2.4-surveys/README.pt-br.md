# Exercise - Surveys

**Leia em outras linguagens**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

* [Criando o projeto](#criando-o-projeto)
* [Criando um template com uma Survey](#criando-um-template-com-uma-survey)
   * [Crie o Template](#crie-o-template)
   * [Adicionando o Survey](#adicionando-o-survey)
* [Iniciando o template](#iniciando-o-template)
* [Vamos praticar!](#vamos-praticar)

Você deve ter notado o botão **ADD SURVEY** na visualização de configuração **Template**. Uma survey é uma maneira de criar um formulário simples para solicitar parâmetros que são usados como variáveis quando um **template** é iniciado como um **job**.

Você instalou o Apache em todos os hosts no job que você acabou de executar. Agora vamos estender isso:

- Use uma role apropriada que possua um template Jinja2 para implantar um arquivo `index.html`.

- Crie um job **template** com uma survey para coletar os valores para o template `index.html`.

- Inicie o job **template**

Além disso, a role também garantirá que a configuração do Apache esteja configurada corretamente - caso seja confundida durante os outros exercícios.

> **Dica**
>
> O recurso de survey fornece apenas uma consulta simples para dados - ele não suporta princípios de four-eye, consultas baseadas em dados dinâmicos ou menus aninhados.

## Criando o projeto

O Playbook e a role com o template Jinja já existem no repositório do Github **https://github.com/ansible/workshop-examples** no diretório `rhel/apache`**`.

Vá para a interface do Github e dê uma olhada no conteúdo: o playbook `apache_role_install.yml` apenas faz referência à role. A role pode ser encontrada no subdiretório `papers/role_apache`. Dentro da role, observe as duas variáveis no arquivo de templates `templates/index.html.j2` marcadas por `{{…}}`\. Além disso, verifique as tarefas em `tasks/main.yml` que implementam o arquivo a partir do template. O que este Playbook está fazendo? Ele cria um arquivo (**dest**) nos hosts gerenciados a partir do modelo (**src**).

A role também implementa uma configuração estática para o Apache. Isso é para garantir que todas as alterações feitas nos capítulos anteriores sejam substituídas e que seus exemplos funcionem corretamente.

## Criando um template com uma Survey

Agora você irá criar um novo template que inclui uma survey.

### Crie o Template

- Vá para **Template**, clique no botão ![Plus] (images/green_plus.png) e escolha **Job Template**

- **NAME:** Crie index.html

- Configure o template para:

    - Use o **Project** e o **Playbook**

    - Para executar no `node1`

    - Para executar no modo privilegiado

Tente você mesmo.

> **ATENÇÃO**
>
> **Solução abaixo\!**

- **NAME:** Crie index.html

- **JOB TYPE:** Run

- **INVENTORY:** Workshop Inventory

- **Project:** Exemplo Ansible Workshop

- **PLAYBOOK:** `rhel/apache/apache_role_install.yml`

- **CREDENTIAL:** Credenciais Workshop

- **OPTIONS:** Enable Privilege Escalation

- Click em **SAVE**

> **ATENÇÃO**
>
> **Não execute o template ainda!**

### Adicionando o Survey

- No template, clique no botão **ADD SURVEY**

- Em **ADD SURVEY PROMPT**, preencha:

    - **PROMPT:** First Line

    - **ANSWER VARIABLE NAME:** `first_line`

    - **ANSWER TYPE:** Text

- Click em **+ADD**

- Da mesma maneira, adicione um segundo **Survey Prompt**

    - **PROMPT:** Second Line

    - **ANSWER VARIABLE NAME:** `second_line`

    - **ANSWER TYPE:** Text

- Click em **+ADD**

- Click em **SAVE** para o Survey

- Click em **SAVE** para o Template

## Iniciando o template

Agora inicie o **Create index.html** job template.

Antes do lançamento real, a pesquisa solicitará **First Line** e **Second Line**. Preencha e clique em **Next**. A próxima janela mostra os valores, se tudo estiver bom, execute o Job clicando em **Launch**.

> **Dica**
>
> Observe como as duas linhas de survey são mostradas à esquerda do Job view como **Extra Variables**.

Após a conclusão do job, verifique a página inicial do Apache. No console SSH no host de controle, execute `curl` no endereço IP do seu `node1`:

```bash
$ curl http://22.33.44.55
<body>
<h1>O Apache esta funcionando bem</h1>
<h1>This is survey field "First Line": line one</h1>
<h1>This is survey field "Second Line": line two</h1>
</body>
```
Observe como as duas variáveis foram usadas pelo playbook para criar o conteúdo do arquivo `index.html`.

## Vamos praticar!

Aqui está uma lista de tasks:

> **ATENÇÃO**
>
> **Certifique-se de concluir estas etapas, pois o próximo capítulo depende disso\!**

- No inventário `Webserver` adicione os outros nós, `node2` e `node3`.

- Execute o template **Create index.html** novamente.

- Verifique os resultados nos outros dois nós usando `curl` nos respectivos endereços IP.

----

[Clique aqui para retornar ao Workshop Ansible for Red Hat Enterprise Linux](../README.pt-br.md#seção-2---exercícios-do-ansible-tower)
