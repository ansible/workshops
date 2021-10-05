# Exercício - Introdução ao Tower

**Leia em outras linguagens**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

* [Por que Ansible Tower?](#por-que-ansible-tower)
* [Seu ambiente de laboratório Ansible Tower](#seu-ambiente-de-laboratório-ansible-tower)
* [Dashboard](#dashboard)
* [Conceitos](#conceitos)

## Por que Ansible Tower?

O Ansible Tower é uma interface do usuário baseada na Web que fornece uma solução corporativa para automação de TI.

  - Possui um dashboard amigável.

  - Ele complementa o Ansible Engine, adicionando recursos de automação, gerenciamento visual e monitoramento.

  - Ele fornece controle de acesso do usuário aos administradores.

  - Gerencia graficamente ou sincroniza inventários com uma grande variedade de fontes.

  - Possui uma API RESTful

  - E muito mais...

## Seu ambiente de laboratório Ansible Tower

Neste laboratório, você trabalha em um ambiente de laboratório pré-configurado. Você terá acesso aos seguintes hosts:

| Role                         | Inventory name |
| -----------------------------| ---------------|
| Ansible Control Host & Tower | ansible        |
| Managed Host 1               | node1          |
| Managed Host 2               | node2          |
| Managed Host 2               | node3          |

O Ansible Tower fornecido neste laboratório é configurado individualmente para você. Certifique-se de acessar a máquina certa sempre que trabalhar com ele. O Ansible Tower já foi instalado e licenciado para você, a interface web estará acessível por HTTP/HTTPS.

## Dashboard

Vamos dar uma primeira olhada no Tower: Use a URL que você recebeu, semelhante a `https://student<X>.workshopname.rhdemo.io` (substitua `<X>` pelo número do seu usuário e `workshopname` com o nome do seu workshop atual) e efetue login como `admin`. A senha será fornecida pelo instrutor.

A interface do Tower recebe você com um painel com um gráfico mostrando:

  - atividade recente de trabalho

  - o número de hosts gerenciados

  - quick pointers para listas de hosts com problemas.

A dashboard também exibe dados em tempo real sobre a execução de tasks concluídas nos playbooks.

![Ansible Tower Dashboard](images/dashboard.png)

## Conceitos

Antes de começarmos a usar o Ansible Tower para sua automação, você deve se familiarizar com alguns conceitos e convenções de nomenclatura.

**Projects**

Projetos são coleções lógicas de playbooks no Ansible Tower. Esses Playbooks residem na instância do Ansible Tower ou em um sistema de controle de versão do código-fonte suportado pelo Tower.

**Inventories**

Um inventário é uma coleção de hosts nos quais os trabalhos podem ser iniciados, o mesmo que um arquivo de inventário Ansible. Os inventários são divididos em grupos e esses grupos contêm os hosts reais. Os grupos podem ser preenchidos manualmente, digitando nomes dos hosts no Tower, através de um dos provedores de nuvem suportados pelo Tower ou por meio de scripts de inventário dinâmico.

**Credentials**

As credenciais são utilizadas pelo Tower para autenticação ao iniciar trabalhos em máquinas, sincronizar com fontes de inventário e importar conteúdo do projeto de um sistema de controle de versão. A configuração de credenciais pode ser encontrada nas configurações.

As credenciais do Tower são importadas e armazenadas criptografadas no Tower e não podem ser recuperadas em texto sem formatação na linha de comando por nenhum usuário. Você pode conceder aos usuários e equipes a capacidade de usar essas credenciais, sem expor a credencial ao usuário.

**Templates**

Um job template é uma definição e um conjunto de parâmetros para executar um trabalho Ansible. Os jobs templates são úteis para executar o mesmo job várias vezes. Os jobs templates também incentivam a reutilização do conteúdo do Playbook e a colaboração entre as equipes. Para executar um job, o Tower exige que você primeiro crie um job template.

**Jobs**

Um Job é basicamente uma instância do Tower que lança um Playbook contra um inventário de hosts.

----

[Clique aqui para retornar ao Workshop Ansible for Red Hat Enterprise Linux](../README.pt-br.md#seção-2---exercícios-do-ansible-tower)
