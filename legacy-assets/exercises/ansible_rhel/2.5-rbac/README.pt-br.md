# Exercicio - Controle de acesso baseado em role

**Leia em outras linguagens**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

* [Usuários Ansible Tower](#usuários-ansible-tower)
* [Times no Ansible Tower](#times-no-ansible-tower)
* [Concedendo Permissões](#concedendo-permissões)
* [Permissão de testes](#permissão-de-testes)

Você já aprendeu como o Tower separa credenciais de usuários. Outra vantagem do Ansible Tower é o gerenciamento de direitos de usuários e grupos.

## Usuários Ansible Tower

Existem três tipos de usuários:

- **Usuário normal**: Tem acesso limitado de leitura e gravação ao inventário e aos projetos aos quais esse usuário recebeu as funções e privilégios apropriados.

- **System Auditor**: Os auditores herdam implicitamente o recurso read-only para todos os objetos no Tower.

- **System Administrator**: Possui privilégios de administrador, leitura e gravação em toda a instalação do Tower.

Vamos criar um usuário:

- No menu do Tower em **ACCESS** click em **Users**

- Click no botão verde.

- Preencha os valores para o novo usuário:

    - **FIRST NAME:** Werner

    - **LAST NAME:** Web

    - **EMAIL:** wweb@example.com

    - **USERNAME:** wweb

    - **USER TYPE:** Normal User

    - **PASSWORD:** ansible

    - confirme a senha

- Click em **SAVE**

## Times no Ansible Tower

Uma equipe é uma subdivisão de uma organização com usuários, projetos, credenciais e permissões associadas. As equipes fornecem um meio para implementar esquemas de controle de acesso baseados em role e delegar responsabilidades nas organizações. Por exemplo, as permissões podem ser concedidas a uma equipe inteira, e não a cada usuário da equipe.

Criando o time:

- No menu vai para **ACCESS → Teams**

- Clique no botão verde e crie uma equipe chamada `Web Content`.

- Click em **SAVE**

Agora você pode adicionar um usuário à equipe:

- Mude para a visualização Usuários da equipe `Web Content` clicando no botão **USERS**.

- Clique no botão verde, marque a caixa ao lado do usuário `wweb` e clique em **SAVE**.

Agora clique no botão **PERMISSIONS** na visualização **TEAMS**, você será recebido com "No Permissions Have Been Granted".

As permissões permitem ler, modificar e administrar projetos, inventários e outros elementos do Tower. As permissões podem ser definidas para diferentes recursos.

## Concedendo Permissões

Para permitir que usuários ou equipes realmente façam algo, é necessário definir permissões. O usuário **wweb** deve ter permissão apenas para modificar o conteúdo dos servidores web atribuídos.

Adicione a permissão para usar o template:

- Na visualização Permissions do time `Web Content`, clique no botão verde para adicionar permissões.

- Uma nova janela é aberta. Você pode optar por definir permissões para vários recursos.

    - Selecione o tipo de recurso **JOB TEMPLATE**

    - Escolha o template `Create index.html` marcando a caixa ao lado.

- A segunda parte da janela é aberta, aqui você atribui roles ao recurso selecionado.

    - Escolha **EXECUTE**

- Click em **SAVE**

## Permissão de testes

Agora, saia da interface web do Tower e faça login novamente como usuário da **wweb**.

- Vá para a visualização **Templates**, você deve observar na web apenas que o modelo `Create index.html` está listado. Ele tem permissão para visualizar e lançar, mas não para editar o template.

- Execute o job template clicando no ícone do foguete. Digite o conteúdo da survey e inicie o job.

- Na exibição a seguir **Jobs**, observe que há alterações no host (é claro ...​).

Verifique o resultado: execute `curl` novamente no host de controle para obter o conteúdo do servidor web no endereço IP do` node1`:

```bash
$ curl http://22.33.44.55
```

Lembre-se do que acabou de fazer: você ativou um usuário restrito para executar um Playbook!

  - Sem ter acesso às credenciais

  - Sem poder alterar o próprio Playbook

  - Mas com a capacidade de alterar variáveis, você predefiniu\!

Efetivamente, você forneceu o poder de executar a automação para outro usuário sem distribuir suas credenciais ou dar ao usuário a capacidade de alterar o código de automação. E, ao mesmo tempo, o usuário ainda pode modificar as coisas com base nas surveys que você criou.

Esse recurso é um dos principais pontos fortes da Ansible Tower\!

----

[Clique aqui para retornar ao Workshop Ansible for Red Hat Enterprise Linux](../README.pt-br.md#seção-2---exercícios-do-ansible-tower)
