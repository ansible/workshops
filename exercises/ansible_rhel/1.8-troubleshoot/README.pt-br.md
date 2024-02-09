# Exercício do Workshop - Depuração e Tratamento de Erros

**Leia isso em outros idiomas**:
<br>![uk](../../../images/uk.png) [Inglês](README.md), ![japan](../../../images/japan.png) [Japonês](README.ja.md), ![brazil](../../../images/brazil.png) [Português do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Francês](README.fr.md), ![Español](../../../images/col.png) [Espanhol](README.es.md).

## Índice

- [Objetivo](#objetivo)
- [Guia](#guia)
  - [Etapa 1 - Introdução à Depuração no Ansible](#etapa-1---introdução-à-depuração-no-ansible)
  - [Etapa 2 - Utilizando o Módulo de Depuração](#etapa-2---utilizando-o-módulo-de-depuração)
  - [Etapa 3 - Tratamento de Erros com Blocos](#etapa-3---tratamento-de-erros-com-blocos)
  - [Etapa 4 - Executando em Modo Verbose](#etapa-4---executando-em-modo-verbose)
  - [Resumo](#resumo)

## Objetivo

Baseando-se no conhecimento fundamental dos exercícios anteriores, esta sessão foca na depuração e tratamento de erros dentro do Ansible. Você aprenderá técnicas para solucionar problemas em playbooks, gerenciar erros de forma elegante e garantir que sua automação seja robusta e confiável.

## Guia

### Etapa 1 - Introdução à Depuração no Ansible

A depuração é uma habilidade crucial para identificar e resolver problemas dentro dos seus playbooks do Ansible. O Ansible oferece vários mecanismos para ajudá-lo a depurar seus scripts de automação, incluindo o módulo de depuração, níveis de verbosidade aumentados e estratégias de tratamento de erros.

### Etapa 2 - Utilizando o Módulo de Depuração

O módulo `debug` é uma ferramenta simples, porém poderosa, para imprimir os valores das variáveis, o que pode ser fundamental para entender o fluxo de execução do playbook.

Neste exemplo, adicione tarefas de depuração ao seu papel do Apache no `tasks/main.yml` para exibir o valor das variáveis ou mensagens.

#### Implementar Tarefas de Depuração:

Insira tarefas de depuração para exibir os valores das variáveis ou mensagens personalizadas para solução de problemas:

```yaml
- name: Display Variable Value
  ansible.builtin.debug:
    var: apache_service_name

- name: Display Custom Message
  ansible.builtin.debug:
    msg: "O nome do serviço Apache é {{ apache_service_name }}"
```

### Etapa 3 - Tratamento de Erros com Blocos

O Ansible permite agrupar tarefas usando `block` e tratar erros com seções `rescue`, semelhante ao try-catch na programação tradicional.

Neste exemplo, adicione um bloco para tratar erros potenciais durante a configuração do Apache no arquivo `tasks/main.yml`.

1. Agrupar Tarefas e Tratar Erros:

Envolver as tarefas que podem falhar potencialmente em um bloco e definir uma seção de resgate para tratar os erros:

```yaml
- name: Configuração do Apache com Ponto de Falha Potencial
  block:
    - name: Copiar configuração do Apache
      ansible.builtin.copy:
        src: "{{ apache_conf_src }}"
        dest: "/etc/httpd/conf/httpd.conf"
  rescue:
    - name: Tratar Configuração Ausente
      ansible.builtin.debug:
        msg: "Arquivo de configuração do Apache '{{ apache_conf_src }}' ausente. Usando configurações padrão."
```

2. Adicione uma variável `apache_conf_src` dentro de `vars/main.yml` do papel apache.

```yaml
apache_conf_src: "files/missing_apache.conf"
```

> NOTA: Este arquivo explicitamente não existe para que possamos acionar a parte do resgate em nosso `tasks/main.yml`

### Etapa 4 - Executando em Modo Verbose

O modo verbose do Ansible (-v, -vv, -vvv ou -vvvv) aumenta o detalhe da saída, fornecendo mais insights sobre a execução do playbook e possíveis problemas.

#### Executar o Playbook em Modo Verbose:

Execute seu playbook com a opção `-vv` para obter logs detalhados:

```bash
ansible-navigator run deploy_apache.yml -m stdout -vv
```

```
.
.
.

TASK [apache : Display Variable Value] *****************************************
task path: /home/rhel/ansible-files/roles/apache/tasks/main.yml:20
ok: [node1] => {
    "apache_service_name": "httpd"
}
ok: [node2] => {
    "apache_service_name": "httpd"
}
ok: [node3] => {
    "apache_service_name": "httpd"
}

TASK [apache : Display Custom Message] *****************************************
task path: /home/rhel/ansible-files/roles/apache/tasks/main.yml:24
ok: [node1] => {
    "msg": "O nome do serviço Apache é httpd"
}
ok: [node2] => {
    "msg": "O nome do serviço Apache é httpd"
}
ok: [node3] => {
    "msg": "O nome do serviço Apache é httpd"
}

TASK [apache : Copy Apache configuration] **************************************
task path: /home/rhel/ansible-files/roles/apache/tasks/main.yml:30
Ocorreu uma exceção durante a execução da tarefa. Para ver o rastreamento completo, use -vvv. O erro foi: Se você está usando um módulo e espera que o arquivo exista no remoto, veja a opção remote_src
fatal: [node3]: FAILED! => {"changed": false, "msg": "Não foi possível encontrar ou acessar 'files/missing_apache.conf'\nProcurado em:\n\t/home/student/lab_inventory/roles/apache/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/missing_apache.conf\n\t/home/student/lab_inventory/files/files/missing_apache.conf\n\t/home/student/lab_inventory/files/missing_apache.conf no Controlador Ansible.\nSe você está usando um módulo e espera que o arquivo exista no remoto, veja a opção remote_src"}
fatal: [node1]: FAILED! => {"changed": false, "msg": "Não foi possível encontrar ou acessar 'files/missing_apache.conf'\nProcurado em:\n\t/home/student/lab_inventory/roles/apache/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/missing_apache.conf\n\t/home/student/lab_inventory/files/files/missing_apache.conf\n\t/home/student/lab_inventory/files/missing_apache.conf no Controlador Ansible.\nSe você está usando um módulo e espera que o arquivo exista no remoto, veja a opção remote_src"}
fatal: [node2]: FAILED! => {"changed": false, "msg": "Não foi possível encontrar ou acessar 'files/missing_apache.conf'\nProcurado em:\n\t/home/student/lab_inventory/roles/apache/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/missing_apache.conf\n\t/home/student/lab_inventory/files/files/missing_apache.conf\n\t/home/student/lab_inventory/files/missing_apache.conf no Controlador Ansible.\nSe você está usando um módulo e espera que o arquivo exista no remoto, veja a opção remote_src"}


TASK [apache : Tratar Configuração Ausente] ***********************************
task path: /home/rhel/ansible-files/roles/apache/tasks/main.yml:39
ok: [node1] => {
    "msg": "Arquivo de configuração do Apache 'files/missing_apache.conf' ausente. Usando configurações padrão."
}
ok: [node2] => {
    "msg": "Arquivo de configuração do Apache 'files/missing_apache.conf' ausente. Usando configurações padrão."
}
ok: [node3] => {
    "msg": "Arquivo de configuração do Apache 'files/missing_apache.conf' ausente. Usando configurações padrão."
}

PLAY RECAP *********************************************************************
node1                      : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0
node2                      : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0
node3                      : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0

```

Observe como o playbook mostra que houve um erro ao copiar o arquivo de configuração do Apache, mas o playbook conseguiu tratá-lo por meio do bloco de resgate fornecido. Se você observar a tarefa final 'Tratar Configuração Ausente', ela detalha que o arquivo estava ausente e seria usada a configuração padrão.

O Resumo Final da Execução nos mostra que foi usado um bloco resgatado por meio de `rescued=1` por nó no grupo web.

## Resumo

Neste exercício, você explorou técnicas essenciais de depuração e mecanismos de tratamento de erros no Ansible. Incorporando tarefas de depuração, usando blocos para tratamento de erros e aproveitando o modo verbose, você pode efetivamente solucionar problemas e aprimorar a confiabilidade de seus playbooks do Ansible. Essas práticas são fundamentais no desenvolvimento de automação robusta com Ansible que pode tratar problemas inesperados de forma elegante e garantir resultados consistentes e previsíveis.

---
**Navegação**
<br>
[Exercício Anterior](../1.7-role/README.pt-br.md) - [Próximo Exercício](../2.1-intro/README.pt-br.md)

[Clique aqui para retornar ao Workshop de Ansible para Red Hat Enterprise Linux](../README.md#section-1---ansible-engine-exercises)

