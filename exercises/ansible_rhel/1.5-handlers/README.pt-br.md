# Exercício do Workshop - Condicionais, Manipuladores e Loops

**Leia isto em outros idiomas**:
<br>![uk](../../../images/uk.png) [Inglês](README.md), ![japan](../../../images/japan.png) [Japonês](README.ja.md), ![brazil](../../../images/brazil.png) [Português do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Francês](README.fr.md), ![Español](../../../images/col.png) [Espanhol](README.es.md).

# Exercícios do Workshop - Usando Condicionais, Manipuladores e Loops

## Índice

- [Objetivo](#objetivo)
- [Guia](#guia)
  - [Passo 1 - Entendendo Condicionais, Manipuladores e Loops](#passo-1---entendendo-condicionais-manipuladores-e-loops)
  - [Passo 2 - Condicionais](#passo-2---condicionais)
  - [Passo 3 - Manipuladores](#passo-3---manipuladores)
  - [Passo 4 - Loops](#passo-4---loops)

## Objetivo

Expandindo o Exercício 1.4, este exercício introduz a aplicação de condicionais, manipuladores e loops em playbooks Ansible. Você aprenderá a controlar a execução de tarefas com condicionais, gerenciar respostas de serviços com manipuladores e lidar eficientemente com tarefas repetitivas usando loops.

## Guia

Condicionais, manipuladores e loops são recursos avançados no Ansible que aumentam o controle, a eficiência e a flexibilidade em seus playbooks de automação.

### Passo 1 - Entendendo Condicionais, Manipuladores e Loops

- **Condicionais**: Permitem que tarefas sejam executadas com base em condições específicas.
- **Manipuladores**: Tarefas especiais acionadas por uma diretiva `notify`, normalmente usadas para reiniciar serviços após alterações.
- **Loops**: Usados para repetir uma tarefa várias vezes, particularmente útil quando a tarefa é semelhante, mas precisa ser aplicada a itens diferentes.

### Passo 2 - Condicionais

Condicionais no Ansible controlam se uma tarefa deve ser executada com base em certas condições.
Vamos adicionar ao playbook system_setup.yml a capacidade de instalar o Servidor HTTP Apache (`httpd`) apenas nos hosts que pertencem ao grupo `web` no nosso inventário.

> NOTA: Exemplos anteriores tinham hosts configurados como node1, mas agora está configurado para todos. Isso significa que, ao executar este playbook Ansible atualizado, você notará atualizações para os novos sistemas sendo automatizados, o usuário Roger criado em todos os novos sistemas e o pacote do servidor web Apache httpd instalado em todos os hosts dentro do grupo web.

```yaml
---
- name: Configuração Básica do Sistema
  hosts: all
  become: true
  vars:
    user_name: 'Roger'
    package_name: httpd
  tasks:
    - name: Atualizar todos os pacotes relacionados à segurança
      ansible.builtin.dnf:
        name: '*'
        state: latest
        security: true
        update_only: true

    - name: Criar um novo usuário
      ansible.builtin.user:
        name: "{{ user_name }}"
        state: present
        create_home: true

    - name: Instalar o Apache em servidores web
      ansible.builtin.dnf:
        name: "{{ package_name }}"
        state: present
      when: inventory_hostname in groups['web']
```

Neste exemplo, `inventory_hostname in groups['web']` é a declaração condicional. `inventory_hostname` refere-se ao nome do host atual em que o Ansible está trabalhando no playbook. A condição verifica se este host faz parte do grupo `web` definido no seu arquivo de inventário. Se verdadeiro, a tarefa será executada e o Apache será instalado nesse host.

### Passo 3 - Manipuladores

Manipuladores são usados para tarefas que só devem ser executadas quando notificadas por outra tarefa. Tipicamente, eles são usados para reiniciar serviços após uma mudança de configuração.

Vamos supor que queremos garantir que o firewall esteja configurado corretamente em todos os servidores web e, em seguida, recarregar o serviço de firewall para aplicar quaisquer novas configurações. Vamos definir um manipulador que recarrega o serviço de firewall e é notificado por uma tarefa que garante que as regras de firewall desejadas estejam em vigor:

```yaml
---
- name: Configuração Básica do Sistema
  hosts: all
  become: true
  .
  .
  .
    - name: Instalar firewalld
      ansible.builtin.dnf:
        name: firewalld
        state: present

    - name: Garantir que o firewalld esteja em execução
      ansible.builtin.service:
        name: firewalld
        state: started
        enabled: true

    - name: Permitir tráfego HTTPS em servidores web
      ansible.posix.firewalld:
        service: https
        permanent: true
        state: enabled
      when: inventory_hostname in groups['web']
      notify: Recarregar Firewall

  handlers:
    - name: Recarregar Firewall
      ansible.builtin.service:
        name: firewalld
        state: reloaded

```

O manipulador Recarregar Firewall é acionado apenas se a tarefa "Permitir tráfego HTTPS em servidores web" fizer alguma mudança.

> NOTA: Observe como o nome do manipulador é usado na seção `notify` da tarefa de configuração "Recarregar Firewall". Isso garante que o manipulador correto seja executado, pois pode haver vários manipuladores dentro de um playbook Ansible.


```bash
PLAY [Configuração Básica do Sistema] ******************************************************

TASK [Coletando Fatos] *********************************************************
ok: [node1]
ok: [node2]
ok: [ansible-1]
ok: [node3]

TASK [Atualizar todos os pacotes relacionados à segurança] ************************************
ok: [node2]
ok: [node1]
ok: [ansible-1]
ok: [node3]

TASK [Criar um novo usuário] *******************************************************
ok: [node1]
ok: [node2]
ok: [ansible-1]
ok: [node3]

TASK [Instalar o Apache em servidores web] *******************************************
skipping: [ansible-1]
ok: [node2]
ok: [node1]
ok: [node3]

TASK [Instalar firewalld] *******************************************************
changed: [ansible-1]
changed: [node2]
changed: [node1]
changed: [node3]

TASK [Garantir que o firewalld esteja em execução] *********************************************
changed: [node3]
changed: [ansible-1]
changed: [node2]
changed: [node1]

TASK [Permitir tráfego HTTPS em servidores web] **************************************
skipping: [ansible-1]
changed: [node2]
changed: [node1]
changed: [node3]

MANIPULADOR EM EXECUÇÃO [Recarregar Firewall] **********************************************
changed: [node2]
changed: [node1]
changed: [node3]

RECAPITULAÇÃO DO JOGO *********************************************************************
ansible-1                  : ok=5    changed=2    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
node1                      : ok=8    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node2                      : ok=8    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node3                      : ok=8    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

```

### Passo 4 - Loops

Loops no Ansible permitem que você execute uma tarefa várias vezes com diferentes valores. Este recurso é particularmente útil para tarefas como a criação de várias contas de usuário, como no exemplo dado. No playbook original system_setup.yml do Exercício 1.4, tínhamos uma tarefa para criar um único usuário:

```yaml
- name: Criar um novo usuário
  ansible.builtin.user:
    name: "{{ user_name }}"
    state: present
    create_home: true
```

Agora, vamos modificar essa tarefa para criar vários usuários usando um loop:

```yaml
- name: Criar um novo usuário
  ansible.builtin.user:
    name: "{{ item }}"
    state: present
    create_home: true
  loop:
    - alice
    - bob
    - carol
```

O que mudou?

1. Diretiva Loop: A palavra-chave loop é usada para iterar sobre uma lista de itens. Neste caso, a lista contém os nomes dos usuários que queremos criar: alice, bob e carol.

2. Criação de Usuário com Loop: Em vez de criar um único usuário, a tarefa modificada agora itera sobre cada item na lista do loop. O espaço reservado `{{ item }}` é substituído dinamicamente por cada nome de usuário na lista, de modo que o módulo ansible.builtin.user cria cada usuário por vez.

Quando você executa o playbook atualizado, essa tarefa é executada três vezes, uma para cada usuário especificado no loop. É uma maneira eficiente de lidar com tarefas repetitivas com dados de entrada variáveis.

Trecho da saída para a criação de um novo usuário em todos os nós.

```bash
[student@ansible-1 ~lab_inventory]$ ansible-navigator run system_setup.yml -m stdout

PLAY [Configuração Básica do Sistema] ******************************************************

.
.
.

TASK [Criar um novo usuário] *******************************************************
changed: [node2] => (item=alice)
changed: [ansible-1] => (item=alice)
changed: [node1] => (item=alice)
changed: [node3] => (item=alice)
changed: [node1] => (item=bob)
changed: [ansible-1] => (item=bob)
changed: [node3] => (item=bob)
changed: [node2] => (item=bob)
changed: [node1] => (item=carol)
changed: [node3] => (item=carol)
changed: [ansible-1] => (item=carol)
changed: [node2] => (item=carol)

.
.
.

RECAPITULAÇÃO DO JOGO *********************************************************************
ansible-1 : ok=5 changed=1 unreachable=0 failed=0 skipped=2 rescued=0 ignored=0
node1 : ok=7 changed=1 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0
node2 : ok=7 changed=1 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0
node3 : ok=7 changed=1 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0
```

---
**Navegação**
<br>
[Exercício Anterior](../1.4-variables/README.pt-br.md) - [Próximo Exercício](../1.6-templates/READMW.pt-br.md)

[Clique aqui para retornar ao Workshop de Ansible para Red Hat Enterprise Linux](../README.md#section-1---ansible-engine-exercises)


