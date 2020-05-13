# Exercicio - Templates

**Leia em outras linguagens**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

* [Passo 1 - Usando Templates em Playbooks](#passo-1---usando-templates-em-playbooks)
* [Passo 2 - Laboratório de Desafios](#passo-2---laboratório-de-desafios)

O Ansible usa o template Jinja2 para modificar arquivos antes de serem distribuídos para hosts gerenciados. O Jinja2 é um dos mecanismos de template mais usados para o Python (<http://jinja.pocoo.org/>).

## Passo 1 - Usando Templates em Playbooks

Quando um template é criado, ele pode ser implantado nos hosts gerenciados usando o módulo `template`, que suporta a transferência de um arquivo local do nó de controle para os hosts gerenciados.

Como exemplo de uso de templates, você irá alterar o arquivo motd para conter dados específicos do host.


No diretório `~/ansible-files/` crie o arquivo de template `motd-facts.j2`:

<!-- {% raw %} -->
```html+jinja
Bem vindo ao {{ ansible_hostname }}.
{{ ansible_distribution }} {{ ansible_distribution_version}}
implementado na arquitetura {{ ansible_architecture }}.
```
<!-- {% endraw %} -->

O arquivo de template contém o texto básico que mais tarde será copiado. Ele também contém variáveis que serão substituídas nas máquinas de destino individualmente.

Em seguida, precisamos de um Playbook para usar este modelo. No diretório `~/ansible-files/` crie o Playbook `motd-facts.yml`:

```yaml
---
- name: Preencher arquivo motd com dados do host
  hosts: node1
  become: yes
  tasks:
    - template:
        src: motd-facts.j2
        dest: /etc/motd
        owner: root
        group: root
        mode: 0644
```

Você já fez isso algumas vezes até agora:

  - Entender o que o Playbook faz.

  - Executar o Playbook `motd-facts.yml`.

  - Efetue login no node1 via SSH e verifique a mensagem do conteúdo do dia.

  - Efetue Logout no node1.

Você deve ter visto como o Ansible substitui as variáveis pelos dados descobertos no sistema.

## Passo 2 - Laboratório de Desafios

Adicione uma linha ao template para listar o kernel atual do nó gerenciado.

 - Encontre um fact que contenha a versão do kernel usando os comandos que você aprendeu no capítulo "Ansible Facts".

> **Dica**
>
> Use `grep -i` para o kernel

  - Mude o template para usar o fact que você encontrou.

  - Execute o Playbook novamente.

  - Verifique o motd efetuando login no node1

> **ATENÇÃO**
>
> **Solução abaixo\!**


  - Procure o fact:

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup|grep -i kernel
       "ansible_kernel": "3.10.0-693.el7.x86_64",
```

  - Modifique o template `motd-facts.j2`:

<!-- {% raw %} -->
```html+jinja
Bem vindo ao {{ ansible_hostname }}.
{{ ansible_distribution }} {{ ansible_distribution_version}}
implementado na arquitetura {{ ansible_architecture }}
executando o kernel {{ ansible_kernel }}.
```
<!-- {% endraw %} -->

  - Execute o playbook.
  - Verifique a nova mensagem via login SSH no `node1`.
----

[Clique aqui para retornar ao Workshop Ansible for Red Hat Enterprise Linux](../README.pt-br.md#seção-1---exercícios-do-ansible-engine)
