# Exercício de Workshop - Templates

**Leia isto em outros idiomas**:
<br>![uk](../../../images/uk.png) [Inglês](README.md), ![japan](../../../images/japan.png) [Japonês](README.ja.md), ![brazil](../../../images/brazil.png) [Português do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Francês](README.fr.md), ![Español](../../../images/col.png) [Espanhol](README.es.md).

## Índice

- [Objetivo](#objetivo)
- [Guia](#guia)
  - [Passo 1 - Introdução ao Templating Jinja2](#passo-1---introdução-ao-templating-jinja2)
  - [Passo 2 - Criando Seu Primeiro Template](#passo-2---criando-seu-primeiro-template)
  - [Passo 3 - Implementando o Template com um Playbook](#passo-3---implementando-o-template-com-um-playbook)
  - [Passo 4 - Executando o Playbook](#passo-4---executando-o-playbook)

## Objetivo

O Exercício 1.5 introduz o templating Jinja2 dentro do Ansible, um recurso poderoso para gerar arquivos dinâmicos a partir de templates. Você aprenderá como criar templates que incorporam dados específicos do host, permitindo a criação de arquivos de configuração personalizados para cada host gerenciado.

## Guia

### Passo 1 - Introdução ao Templating Jinja2

O Ansible utiliza o Jinja2, uma linguagem de templating amplamente usada para Python, permitindo a geração de conteúdo dinâmico dentro dos arquivos. Essa capacidade é particularmente útil para configurar arquivos que devem variar de host para host.

### Passo 2 - Criando Seu Primeiro Template

Os templates terminam com a extensão `.j2` e misturam conteúdo estático com espaços reservados dinâmicos envolvidos em `{{ }}`.

No exemplo a seguir, vamos criar um template para a Mensagem do Dia (MOTD) que inclui informações dinâmicas do host.

#### Configurando o Diretório de Templates:

Certifique-se de que um diretório de templates exista dentro do seu diretório lab_inventory para organizar seus templates.

```bash
mkdir -p ~/lab_inventory/templates
```

#### Desenvolvendo o Template MOTD:

Crie um arquivo chamado `motd.j2` no diretório de templates com o seguinte conteúdo:

```jinja
Bem-vindo ao {{ ansible_hostname }}.
SO: {{ ansible_distribution }} {{ ansible_distribution_version }}
Arquitetura: {{ ansible_architecture }}
```

Este template exibe dinamicamente o nome do host, a distribuição do sistema operacional, a versão e a arquitetura de cada host gerenciado.

### Passo 3 - Implementando o Template com um Playbook

Utilize o módulo `ansible.builtin.template` em um playbook para distribuir e renderizar o template em seus hosts gerenciados.

Modifique o playbook `system_setup.yml` com o seguinte conteúdo:

```yaml
---
- name: Configuração Básica do Sistema
  hosts: all
  become: true
  tasks:
    - name: Atualizar MOTD a partir do Template Jinja2
      ansible.builtin.template:
        src: templates/motd.j2
        dest: /etc/motd

  handlers:
    - name: Recarregar Firewall
      ansible.builtin.service:
        name: firewalld
        state: reloaded
```

O módulo `ansible.builtin.template` pega o template `motd.j2` e gera um arquivo `/etc/motd` em cada host, preenchendo os espaços reservados do template com os fatos reais do host.

### Passo 4 - Executando o Playbook

Execute o playbook para aplicar seu MOTD personalizado em todos os hosts gerenciados:

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_setup.yml -m stdout
```

```plaintext
PLAY [Configuração Básica do Sistema] *****************************************
.
.
.

TASK [Atualizar MOTD a partir do Template Jinja2] *****************************
changed: [node1]
changed: [node2]
changed: [node3]
changed: [ansible-1]

RECAP ************************************************************************
ansible-1                  : ok=6    changed=1    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
node1                      : ok=8    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node2                      : ok=8    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node3                      : ok=8    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Verifique as alterações fazendo SSH para o nó, e você deverá ver a mensagem do dia:

```plaintext
[rhel@control ~]$ ssh node1

Bem-vindo ao node1.
SO: RedHat 8.7
Arquitetura: x86_64
Registre este sistema no Red Hat Insights: insights-client --register
Crie uma conta ou visualize todos os seus sistemas em https://red.ht/insights-dashboard
Último login: Seg Jan 29 16:30:31 2024 de 10.5.1.29
```

----
**Navegação**
<br>
[Exercício anterior](../1.5-handlers/README.pt-br.md) - [Próximo exercício](../1.7-role/README.pt-br.md)

[Clique aqui para voltar ao workshop de Ansible para Red Hat Enterprise Linux](../README.md)

