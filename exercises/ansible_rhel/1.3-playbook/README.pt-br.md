# Exercício do Workshop - Escrevendo Seu Primeiro Playbook

**Leia isso em outros idiomas**:
<br>![uk](../../../images/uk.png) [Inglês](README.md), ![japan](../../../images/japan.png) [日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Português do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Francês](README.fr.md), ![Español](../../../images/col.png) [Espanhol](README.es.md).

## Índice de Conteúdos

- [Exercício do Workshop - Escrevendo Seu Primeiro Playbook](#exercício-do-workshop---escrevendo-seu-primeiro-playbook)
  - [Objetivo](#objetivo)
  - [Guia](#guia)
    - [Etapa 1 - Básicos do Playbook](#etapa-1---básicos-do-playbook)
    - [Etapa 2 - Criando Seu Playbook](#etapa-2---criando-seu-playbook)
    - [Etapa 3 - Executando o Playbook](#etapa-3---executando-o-playbook)
    - [Etapa 4 - Verificando o Playbook](#etapa-4---verificando-o-playbook)

## Objetivo

Neste exercício, você usará o Ansible para realizar tarefas básicas de configuração do sistema em um servidor Red Hat Enterprise Linux. Você se familiarizará com módulos fundamentais do Ansible como `dnf` e `user`, e aprenderá a criar e executar playbooks.

## Guia

Os playbooks no Ansible são basicamente scripts escritos em formato YAML. Eles são usados para definir as tarefas e configurações que o Ansible aplicará aos seus servidores.

### Etapa 1 - Básicos do Playbook
Primeiro, crie um arquivo de texto em formato YAML para o seu playbook. Lembre-se de:
- Começar com três traços (`---`).
- Usar espaços, não tabs, para indentação.

Conceitos Principais:
- `hosts`: Especifica os servidores ou dispositivos alvo para o seu playbook ser executado.
- `tasks`: As ações que o Ansible realizará.
- `become`: Permite a escalada de privilégios (executar tarefas com privilégios elevados).

> NOTA: Um playbook do Ansible é projetado para ser idempotente, o que significa que se você executá-lo várias vezes nos mesmos hosts, ele garante o estado desejado sem fazer mudanças redundantes.

### Etapa 2 - Criando Seu Playbook
Antes de criar seu primeiro playbook, certifique-se de estar no diretório correto mudando para `~/lab_inventory`:

```bash
cd ~/lab_inventory
```

Agora, crie um playbook chamado `system_setup.yml` para realizar a configuração básica do sistema:
- Atualize todos os pacotes relacionados à segurança.
- Crie um novo usuário chamado ‘myuser’.

A estrutura básica é a seguinte:

```yaml
---
- name: Basic System Setup
  hosts: node1
  become: true
  tasks:
    - name: Update all security-related packages
      ansible.builtin.dnf:
        name: '*'
        state: latest
        security: true

    - name: Create a new user
      ansible.builtin.user:
        name: myuser
        state: present
        create_home: true
```

> NOTA: A atualização dos pacotes pode levar alguns minutos antes de o playbook do Ansible ser concluído.

* Sobre o módulo `dnf`: Este módulo é usado para gerenciamento de pacotes com DNF (YUM Dandificado) no RHEL e outros sistemas baseados em Fedora.

* Sobre o módulo `user`: Este módulo é usado para gerenciar contas de usuário.

### Etapa 3 - Executando o Playbook

Execute seu playbook usando o comando `ansible-navigator`:

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_setup.yml -m stdout
```

Revise a saída para garantir que cada tarefa seja concluída com sucesso.

### Etapa 4 - Verificando o Playbook
Agora, vamos criar um segundo playbook para verificações pós-configuração, chamado `system_checks.yml`:

```yaml
---
- name: System Configuration Checks
  hosts: node1
  become: true
  tasks:
    - name: Check user existence
      ansible.builtin.command:
        cmd: id myuser
      register: user_check

    - name: Report user status
      ansible.builtin.debug:
        msg: "Usuário 'myuser' existe."
      when: user_check.rc == 0
```

Execute o playbook de verificações:

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_checks.yml -m stdout
```

Revise a saída para garantir que a criação do usuário foi bem-sucedida.

---
**Navegação**
{% if page.url contains 'ansible_rhel_90' %}
[Exercício Anterior](../2-thebasics) - [Próximo Exercício](../4-variables)
{% else %}
[Exercício Anterior](../1.2-thebasics) - [Próximo Exercício](../1.4-variables)
{% endif %}
<br><br>

<br>

[Clique aqui para retornar ao Workshop de Ansible para Red Hat Enterprise Linux](../README.md)""

