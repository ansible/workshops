# Exercício do Workshop - Usando Variáveis

**Leia isto em outros idiomas**:
<br>![uk](../../../images/uk.png) [Inglês](README.md), ![japan](../../../images/japan.png) [日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Português do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Francês](README.fr.md), ![Español](../../../images/col.png) [Espanhol](README.es.md).

## Índice

- [Exercício do Workshop - Usando Variáveis](##workshop-exercise---using-variables)
  - [Objetivo](#objetivo)
  - [Guia](#guia)
    - [Passo 1 - Entendendo Variáveis](#passo-1---entendendo-variáveis)
    - [Passo 2 - Sintaxe e Criação de Variáveis](#passo-2---sintaxe-e-criação-de-variáveis)
    - [Passo 3 - Executando o Playbook Modificado](#passo-3---executando-o-playbook-modificado)
    - [Passo 4 - Uso Avançado de Variáveis no Playbook de Verificações](#passo-4---uso-avançado-de-variáveis-no-playbook-de-verificações)

## Objetivo
Estendendo nossos playbooks do Exercício 1.3, o foco se volta para a criação e uso de variáveis no Ansible. Você aprenderá a sintaxe para definir e usar variáveis, uma habilidade essencial para criar playbooks dinâmicos e adaptáveis.

## Guia
Variáveis no Ansible são ferramentas poderosas para tornar seus playbooks flexíveis e reutilizáveis. Elas permitem armazenar e reutilizar valores, tornando seus playbooks mais dinâmicos e adaptáveis.

### Passo 1 - Entendendo Variáveis
Uma variável no Ansible é uma representação nomeada de algum dado. Variáveis podem conter valores simples como strings e números, ou dados mais complexos como listas e dicionários.

### Passo 2 - Sintaxe e Criação de Variáveis
A criação e uso de variáveis envolvem uma sintaxe específica:

1. Definindo Variáveis: Variáveis são definidas na seção `vars` de um playbook ou em arquivos separados para projetos maiores.
2. Nomeando Variáveis: Os nomes das variáveis devem ser descritivos e aderir a regras como:
   * Começar com uma letra ou sublinhado.
   * Conter apenas letras, números e sublinhados.
3. Usando Variáveis: Variáveis são referenciadas em tarefas usando as chaves duplas em aspas `"{{ nome_da_variável }}"`. Esta sintaxe indica ao Ansible para substituí-la pelo valor da variável em tempo de execução.

Atualize o playbook `system_setup.yml` para incluir e usar uma variável:

```yaml
---
- name: Configuração Básica do Sistema
  hosts: node1
  become: true
  vars:
    user_name: 'Roger'
  tasks:
    - name: Atualizar todos os pacotes relacionados à segurança
      ansible.builtin.dnf:
        name: '*'
        state: latest
        security: true

    - name: Criar um novo usuário
      ansible.builtin.user:
        name: "{{ user_name }}"
        state: present
        create_home: true
```

Execute este playbook com ansible-navigator.

### Passo 3 - Executando o Playbook Modificado
Execute o playbook atualizado:

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_setup.yml -m stdout

PLAY [Configuração Básica do Sistema] ******************************************************

TASK [Coletando Fatos] *********************************************************
ok: [node1]

TASK [Atualizar todos os pacotes relacionados à segurança] ************************************
ok: [node1]

TASK [Criar um novo usuário] *******************************************************
changed: [node1]

PLAY RECAP *********************************************************************
node1                      : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Observe como o playbook atualizado mostra um status de alterado na tarefa Criar um novo usuário. O usuário, 'Roger', especificado na seção vars, foi criado.

Verifique a criação do usuário via:

```bash
[student@ansible-1 lab_inventory]$ ssh node1 id Roger

```

### Passo 4 - Uso Avançado de Variáveis no Playbook de Verificações
Aprimore o playbook `system_checks.yml` para verificar a existência do usuário 'Roger' no sistema usando a variável `register` e a declaração condicional `when`.

A palavra-chave register no Ansible é usada para capturar a saída de uma tarefa e salvá-la como uma variável.

Atualize o playbook `system_checks.yml`:

```yaml
---
- name: Verificações de Configuração do Sistema
  hosts: node1
  become: true
  vars:
    user_name: 'Roger'
  tasks:
    - name: Verificar existência do usuário
      ansible.builtin.command:
        cmd: "id {{ user_name }}"
      register: user_check

    - name: Relatar status do usuário
      ansible.builtin.debug:
        msg: "O usuário {{ user_name }} existe."
      when: user_check.rc == 0
```

Detalhes do Playbook:

* `register: user_check:` Isso captura a saída do comando id na variável user_check.
* `when: user_check.rc == 0:` Esta linha é uma declaração condicional. Ela verifica se o código de retorno (rc) da tarefa anterior (armazenado em user_check) é 0, indicando sucesso. A mensagem de depuração só será exibida se esta condição for atendida.
Esta configuração fornece um exemplo prático de como as variáveis podem ser usadas para controlar o fluxo de tarefas com base nos resultados das etapas anteriores.

Execute o playbook de verificações:

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_checks.yml -m stdout

PLAY [Verificações de Configuração do Sistema] *********************************************

TASK [Coletando Fatos] *********************************************************
ok: [node1]

TASK [Verificar existência do usuário] ****************************************************
changed: [node1]

TASK [Relatar status do usuário] ******************************************************
ok: [node1] => {
    "msg": "O usuário Roger existe."
}

PLAY RECAP *********************************************************************
node1                      : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Revise a saída para confirmar que a verificação da existência do usuário está usando corretamente a variável e a lógica condicional.

---
**Navegação**

[Exercício Anterior](../1.3-playbook/README.pt-br.md) - [Próximo Exercício](../1.5-handlers/README.pt-br.md)

[Clique aqui para retornar ao Workshop de Ansible para Red Hat Enterprise Linux](../README.md)

