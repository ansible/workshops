# Exercício do Workshop - Papéis: Tornando seus playbooks reutilizáveis

**Leia isto em outros idiomas**:
<br>![uk](../../../images/uk.png) [Inglês](README.md), ![japan](../../../images/japan.png) [Japonês](README.ja.md), ![brazil](../../../images/brazil.png) [Português do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Francês](README.fr.md), ![Español](../../../images/col.png) [Espanhol](README.es.md).

## Índice

- [Objetivo](#objetivo)
- [Guia](#guia)
  - [Etapa 1 - Fundamentos de Papéis](#etapa-1---fundamentos-de-papéis)
  - [Etapa 2 - Limpando o Ambiente](#etapa-2---limpando-o-ambiente)
  - [Etapa 3 - Construindo o Papel do Apache](#etapa-3---construindo-o-papel-do-apache)
  - [Etapa 4 - Integração do Papel em um Playbook](#etapa-4---integração-do-papel-em-um-playbook)
  - [Etapa 5 - Execução e Validação do Papel](#etapa-5---execução-e-validação-do-papel)
  - [Etapa 6 - Verificando se o Apache está Executando](#etapa-6---verificando-se-o-apache-está-executando)

## Objetivo

Este exercício se baseia nos exercícios anteriores e avança suas habilidades no Ansible ao guiá-lo através da criação de um papel que configura o Apache (httpd). Você usará o conhecimento adquirido para agora integrar variáveis, manipuladores e um modelo para um index.html personalizado. Este papel demonstra como encapsular tarefas, variáveis, modelos e manipuladores em uma estrutura reutilizável para automação eficiente.

## Guia

### Etapa 1 - Fundamentos de Papéis

Papéis no Ansible organizam tarefas de automação relacionadas e recursos, como variáveis, modelos e manipuladores, em um diretório estruturado. Este exercício foca na criação de um papel de configuração do Apache, enfatizando a reutilização e modularidade.

### Etapa 2 - Limpando o Ambiente

Com base em nosso trabalho anterior com a configuração do Apache, vamos criar um playbook do Ansible dedicado a limpar nosso ambiente. Esta etapa prepara o caminho para introduzirmos um novo papel do Apache, fornecendo uma visão clara dos ajustes realizados. Por meio desse processo, ganharemos uma compreensão mais profunda da versatilidade e reutilização oferecidas pelos Papéis do Ansible.

Execute o seguinte playbook do Ansible para limpar o ambiente:

```yaml
---
- name: Cleanup Environment
  hosts: all
  become: true
  vars:
    package_name: httpd
  tasks:
    - name: Remove Apache from web servers
      ansible.builtin.dnf:
        name: "{{ package_name }}"
        state: absent
      when: inventory_hostname in groups['web']

    - name: Remove firewalld
      ansible.builtin.dnf:
        name: firewalld
        state: absent

    - name: Delete created users
      ansible.builtin.user:
        name: "{{ item }}"
        state: absent
        remove: true  # Use 'remove: true’ to delete home directories
      loop:
        - alice
        - bob
        - carol
        - Roger

    - name: Reset MOTD to an empty message
      ansible.builtin.copy:
        dest: /etc/motd
        content: ''
```

### Etapa 3 - Construindo o Papel do Apache

Desenvolveremos um papel chamado `apache` para instalar, configurar e gerenciar o Apache.

1. Gerar Estrutura do Papel:

Crie o papel usando o ansible-galaxy, especificando o diretório de papéis para saída.

```bash
[student@ansible-1 lab_inventory]$ mkdir roles
[student@ansible-1 lab_inventory]$ ansible-galaxy init --offline roles/apache
```

2. Definir Variáveis do Papel:

Preencha `/home/student/lab_inventory/roles/apache/vars/main.yml` com variáveis específicas do Apache:

```yaml
---
# vars file for roles/apache
apache_package_name: httpd
apache_service_name: httpd
```

3. Configurar Tarefas do Papel:

Ajuste `/home/student/lab_inventory/roles/apache/tasks/main.yml` para incluir tarefas para instalação e gerenciamento de serviço do Apache:

```yaml
---
# tasks file for ansible-files/roles/apache
- name: Install Apache web server
  ansible.builtin.package:
    name: "{{ apache_package_name }}"
    state: present

- name: Ensure Apache is running and enabled
  ansible.builtin.service:
    name: "{{ apache_service_name }}"
    state: started
    enabled: true

- name: Install firewalld
  ansible.builtin.dnf:
    name: firewalld
    state: present

- name: Ensure firewalld is running
  ansible.builtin.service:
    name: firewalld
    state: started
    enabled: true

- name: Allow HTTPS traffic on web servers
  ansible.posix.firewalld:
    service: https
    permanent: true
    state: enabled
  when: inventory_hostname in groups['web']
  notify: Reload Firewall
```

4. Implementar Manipuladores:

Em `/home/student/lab_inventory/roles/apache/handlers/main.yml`, crie um manipulador para reiniciar o firewalld se sua configuração mudar:

```yaml
---
# handlers file for ansible-files/roles/apache
- name: Reload Firewall
  ansible.builtin.service:
    name: firewalld
    state: reloaded
```

5. Criar e Implementar Modelo:

Use um modelo Jinja2 para um `index.html` personalizado. Armazene o modelo em `templates/index.html.j2`:

```html
<html>
<head>
<title>Welcome to {{ ansible_hostname }}</title>
</head>
<body>
 <h1>Hello from {{ ansible_hostname }}</h1>
</body>
</html>
```

6. Atualize `tasks/main.yml` para implementar este modelo `index.html`:

```yaml
- name: Deploy custom index.html
  ansible.builtin.template:
    src: index.html.j2
    dest: /var/www/html/index.html
```

### Etapa 4 - Integração do Papel em um Playbook

Incorpore o papel `apache` em um playbook chamado `deploy_apache.yml` dentro de `/home/student/lab_inventory` para aplicá-lo aos seus hosts do grupo 'web' (node1, node2, node3).

```yaml
- name: Setup Apache Web Servers
  hosts: web
  become: true
  roles:
    - apache
```

### Etapa 5 - Execução e Validação do Papel

Execute seu playbook para configurar o Apache nos servidores web designados:

```bash
ansible-navigator run deploy_apache.yml -m stdout
```

#### Saída:

```plaintext
PLAY [Setup Apache Web Servers] ************************************************

TASK [Gathering Facts] *********************************************************
ok: [node2]
ok: [node1]
ok: [node3]

TASK [apache : Install Apache web server] **************************************
changed: [node1]
changed: [node2]
changed: [node3]

TASK [apache : Ensure Apache is running and enabled] ***************************
changed: [node2]
changed: [node1]
changed: [node3]

TASK [apache : Deploy custom index.html] ***************************************
changed: [node1]
changed: [node2]
changed: [node3]

RUNNING HANDLER [apache : Reload Firewall] *************************************
ok: [node2]
ok: [node1]
ok: [node3]

PLAY RECAP *********************************************************************
node1                      : ok=5    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node2                      : ok=5    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node3                      : ok=5    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

### Etapa 6 - Verificando se o Apache está Executando

Após a conclusão do playbook, verifique se o `httpd` está realmente em execução em todos os nós web.

```bash
[rhel@control ~]$ ssh node1 "systemctl status httpd"
● httpd.service - The Apache HTTP Server
   Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2024-01-29 16:49:13 UTC; 3min 46s ago
```

```bash
[rhel@control ~]$ ssh node2 "systemctl status httpd"
● httpd.service - The Apache HTTP Server
   Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2024-01-29 16:49:13 UTC; 3min 58s ago
```

Uma vez verificado que o `httpd` está em execução, verifique se o servidor web Apache está servindo o arquivo `index.html` apropriado:

```bash
[student@ansible-1 lab_inventory]$ curl http://node1
<html>
<head>
<title>Welcome to node1</title>
</head>
<body>
 <h1>Hello from node1</h1>
</body>
</html>
```


---
**Navegação**
<br>
[Exercício anterior](../1.6-templates/README.pt-br.md) - [Próximo exercício](../1.8-troubleshoot/README.pt-br.md)

[Clique aqui para retornar ao workshop de Ansible para Red Hat Enterprise Linux](../README.md#section-1---ansible-engine-exercises)



