# Exercício de Workshop - Verificar os Pré-requisitos

**Leia isso em outros idiomas**:
<br>![uk](../../../images/uk.png) [Inglês](README.md), ![japan](../../../images/japan.png) [日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Português do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Francês](README.fr.md),![Español](../../../images/col.png) [Espanhol](README.es.md).

## Índice

- [Exercício de Workshop - Verificar os Pré-requisitos](#exercício-de-workshop---verificar-os-pré-requisitos)
  - [Índice](#índice)
  - [Objetivo](#objetivo)
  - [Guia](#guia)
    - [Seu Ambiente de Laboratório](#seu-ambiente-de-laboratório)
    - [Etapa 1 - Acessar o Ambiente](#etapa-1---acessar-o-ambiente)
    - [Etapa 2 - Usando o Terminal](#etapa-2---usando-o-terminal)
    - [Etapa 3 - Examinando Ambientes de Execução](#etapa-3---examinando-ambientes-de-execução)
    - [Etapa 4 - Examinando a configuração do ansible-navigator](#etapa-4---examinando-a-configuração-do-ansible-navigator)
    - [Etapa 5 - Labs de Desafio](#etapa-5---labs-de-desafio)

## Objetivo

* Compreender a Topologia do Laboratório: Familiarize-se com o ambiente de laboratório e métodos de acesso.
* Dominar os Exercícios do Workshop: Obtenha proficiência na navegação e execução das tarefas do workshop.
* Abraçar os Labs de Desafio: Aprenda a aplicar seu conhecimento em cenários práticos de desafio.

## Guia

A fase inicial deste workshop se concentra nas utilidades de linha de comando da Plataforma de Automação Ansible, como:


- [ansible-navigator](https://github.com/ansible/ansible-navigator) - uma Interface de Usuário Baseada em Texto (TUI) para executar e desenvolver conteúdo Ansible.
- [ansible-core](https://docs.ansible.com/core.html) - o executável base que fornece a estrutura, linguagem e funções que sustentam a Plataforma de Automação Ansible, incluindo ferramentas CLI como `ansible`, `ansible-playbook` e `ansible-doc`.
- [Ambientes de Execução](https://docs.ansible.com/automation-controller/latest/html/userguide/execution_environments.html) - Imagens de contêiner pré-construídas com coleções suportadas pela Red Hat.
- [ansible-builder](https://github.com/ansible/ansible-builder) - automatiza o processo de construção de Ambientes de Execução. Não é um foco principal neste workshop.

Se você precisar de mais informações sobre os novos componentes da Plataforma de Automação Ansible, marque esta página inicial [https://red.ht/AAP-20](https://red.ht/AAP-20)

### Seu Ambiente de Laboratório

Você trabalhará em um ambiente pré-configurado com os seguintes hosts:

| Função               | Nome no Inventário |
| ---------------------| -------------------|
| Host de Controle Ansible | ansible-1         |
| Host Gerenciado 1    | node1              |
| Host Gerenciado 2    | node2              |
| Host Gerenciado 3    | node3              |

### Etapa 1 - Acessar o Ambiente

Recomendamos o uso do Visual Studio Code para este workshop por seu navegador de arquivos integrado, editor com destaque de sintaxe e terminal dentro do navegador. O acesso direto via SSH também está disponível. Confira este tutorial do YouTube sobre como acessar seu ambiente de trabalho.

NOTA: Um vídeo curto do YouTube é fornecido caso você precise de clareza adicional:
[Workshops Ansible - Acessando seu ambiente de trabalho](https://youtu.be/Y_Gx4ZBfcuk)

1. Conecte-se ao Visual Studio Code através da página de lançamento do Workshop.

  ![página de lançamento](images/launch_page.png)

2. Insira a senha fornecida para fazer login.

  ![login no vs code](images/vscode_login.png)

### Etapa 2 - Usando o Terminal

1. Abra um terminal no Visual Studio Code:

  ![imagem de um novo terminal](images/vscode-new-terminal.png)

2. Navegue até o diretório `rhel-workshop` no terminal do nó de controle Ansible.

```bash
[student@ansible-1 ~]$ cd ~/rhel-workshop/
[student@ansible-1 rhel-workshop]$ pwd
/home/student/rhel-workshop
```

* `~`: atalho para o diretório home `/home/student`
* `cd`: comando para mudar de diretórios
* `pwd`: imprime o caminho completo do diretório de trabalho atual.

### Etapa 3 - Examinando Ambientes de Execução

1. Execute `ansible-navigator images` para visualizar Ambientes de Execução configurados.
2. Use o número correspondente para investigar um EE, por exemplo, pressionando 2 para abrir `ee-supported-rhel8`

```bash
$ ansible-navigator images
```

![imagens do ansible-navigator](images/navigator-images.png)

> Nota: A saída que você vê pode diferir da saída acima

![menu principal do ee](images/navigator-ee-menu.png)

Selecionar `2` para `Versão do Ansible e coleções` nos mostrará todas as Coleções Ansible instaladas nesse EE específico, e a versão do `ansible-core`:

![informações do ee](images/navigator-ee-collections.png)

### Etapa 4 - Examinando a configuração do ansible-navigator

1. Visualize o conteúdo do `~/.ansible-navigator.yml` usando o Visual Studio Code ou o comando `cat`.

```bash
$ cat ~/.ansible-navigator.yml
---
ansible-navigator:
  ansible:
    inventory:
      entries:
      - /home/student/lab_inventory/hosts

  execution-environment:
    image: registry.redhat.io/ansible-automation-platform-20-early-access/ee-supported-rhel8:2.0.0
    enabled: true
    container-engine: podman
    pull:
      policy: missing
    volume-mounts:
    - src: "/etc/ansible/"
      dest: "/etc/ansible/"
```

2. Observe os seguintes parâmetros dentro do arquivo `ansible-navigator.yml`:

* `inventories`: mostra a localização do inventário ansible sendo usado
* `execution-environment`: onde o ambiente de execução padrão é definido

Para uma lista completa de todos os ajustes configuráveis, consulte a [documentação](https://ansible.readthedocs.io/projects/navigator/settings/)

### Etapa 5 - Labs de Desafio

Cada capítulo vem com um Lab de Desafio. Essas tarefas testam seu entendimento e aplicação dos conceitos aprendidos. As soluções são fornecidas sob um sinal de advertência para referência.


----

[Clique aqui para retornar ao Workshop Ansible for Red Hat Enterprise Linux](../README.pt-br.md)
