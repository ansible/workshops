# Exercício - Roles: Tornando seus playbooks reutilizáveis

**Leia em outras linguagens**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

* [Passo 1 - Entendendo a estrutura da Role](#passo-1---entendendo-a-estrutura-da-role)
* [Passo 2 - Criando uma estrutura básica de diretório de roles](#passo-2---criando-uma-estrutura-básica-de-diretório-de-roles)
* [Passo 3 - Criando o arquivo de tasks](#passo-3---criando-o-arquivo-de-tasks)
* [Passo 4 - Criando o handler](#passo-4---criando-o-handler)
* [Passo 5 - Criando o index.html e template de arquivo de configuração do vhost](#passo-5---criando-o-indexhtml-e-template-de-arquivo-de-configuração-do-vhost)
* [Passo 6 - Teste a role](#passo-6---teste-a-role)

Embora seja possível escrever um playbook em um arquivo, como fizemos neste workshop, você poderá reutilizar arquivos e começar a organizar as coisas.

Roles são a maneira como fazemos isso. Quando você cria uma role, desconstrói seu playbook em partes e essas partes ficam em uma estrutura de diretórios. Isso é explicado em mais detalhes nas [melhores práticas](http://docs.ansible.com/ansible/playbooks_best_practices.html) já mencionadas no exercício 3.

## Passo 1 - Entendendo a estrutura da Role

As roles são basicamente a automação criada em torno das diretivas *include* e realmente não contêm muita magia adicional além de algumas melhorias no processamento do caminho de pesquisa para arquivos referenciados.

As roles seguem uma estrutura de diretórios definida; uma role é nomeada pelo diretório de nível superior. Alguns dos subdiretórios contêm arquivos YAML, denominados `main.yml`. Os subdiretórios arquivos e templates podem conter objetos referenciados pelos arquivos YAML.

Um exemplo de estrutura de projeto pode ser assim, o nome da role seria "apache":

```text
apache/
├── defaults
│   └── main.yml
├── files
├── handlers
│   └── main.yml
├── meta
│   └── main.yml
├── README.md
├── tasks
│   └── main.yml
├── templates
├── tests
│   ├── inventory
│   └── test.yml
└── vars
    └── main.yml
```

Os arquivos `main.yml` contêm conteúdo, dependendo da sua localização na estrutura de diretórios mostrada acima. Por exemplo, `vars/main.yml` faz referência a variáveis,`handlers/main.yaml` descreve handlers, e assim por diante. Observe que, ao contrário dos playbooks, os arquivos `main.yml` contêm apenas o conteúdo específico e não informações adicionais, como hosts, `become` ou outras palavras-chave.

> **Dica**
>
> Na verdade, existem dois diretórios para variáveis: `vars` e `default`: as variáveis padrão têm a menor precedência e geralmente contêm valores padrão definidos pelos autores da função e são frequentemente usadas quando pretende que seus valores sejam substituídos. pode ser definido em `vars/main.yml` ou `defaults/main.yml`, mas não nos dois lugares.

O uso de roles em um Playbook é direto:

```yaml
---
- name: Iniciando roles
  hosts: web
  roles:
    - role1
    - role2
```

As tasks, handlers e variáveis dessa role serão incluídas no Playbook, nessa ordem. Qualquer cópia, script, template ou task de inclusão na role pode fazer referência aos arquivos, templates ou tasks relevantes *sem nomes de caminho absolutos ou relativos*. O Ansible procurará por eles nos arquivos, templates ou task da role, respectivamente, com base em seu uso.

## Passo 2 - Criando uma estrutura básica de diretório de roles

Ansible procura por roles em um subdiretório chamado `roles` no diretório do projeto. Isso pode ser substituído na configuração Ansible. Cada role tem seu próprio diretório. Para facilitar a criação de um novo role, a ferramenta `ansible-galaxy` pode ser usada.

> **Dica**
>
> Ansible Galaxy é o seu hub para encontrar, reutilizar e compartilhar o melhor conteúdo Ansible. Por enquanto, vamos usá-lo apenas como um auxiliar para criar a estrutura de diretórios.

Ok, vamos começar a criar uma role. Criaremos uma role que instala e configura o Apache para servir um host virtual. Execute estes comandos no diretório `~/ansible-files`:

```bash
[student<X>@ansible ansible-files]$ mkdir roles
[student<X>@ansible ansible-files]$ ansible-galaxy init --offline roles/apache_vhost
```

Dê uma olhada nos diretórios de role e seu conteúdo:

```bash
[student<X>@ansible ansible-files]$ tree roles
```

## Passo 3 - Criando o arquivo de tasks

O arquivo `main.yml` no subdiretório de taks da role deve fazer o seguinte:

  - Verificar se o httpd está instalado

  - Verificar se o httpd está iniciado e habilitado

  - Colocar o conteúdo HTML na raiz do documento Apache

  - Instalar o template fornecido para configurar o vhost

> **ATENÇÃO**
>
> **O `main.yml` (e outros arquivos possivelmente incluídos pelo main.yml) podem conter apenas tasks, *não* Playbooks completos!**

Mude para o diretório `functions/apache_vhost`. Edite o arquivo `tasks/main.yml`:

```yaml
---
- name: Instalar httpd
  yum:
    name: httpd
    state: latest

- name: Start e enable o servico httpd
  service:
    name: httpd
    state: started
    enabled: true
```

Observe que aqui apenas as tasks foram adicionadas. Os detalhes de um Playbook não estão presentes.

As tasks que foram adicionadas até o momento:

  - Instalar o pacote httpd usando o módulo yum

  - Usar o módulo de serviço para dar start e enable no httpd

Em seguida, adicionamos mais duas tasks para garantir uma estrutura de diretórios vhost e copiar o conteúdo html:

<!-- {% raw %} -->
```yaml
- name: Verificar se o diretoio vhost esta presente
  file:
    path: "/var/www/vhosts/{{ ansible_hostname }}"
    state: directory

- name: Entregar conteúdo html
  copy:
    src: index.html
    dest: "/var/www/vhosts/{{ ansible_hostname }}"
```
<!-- {% endraw %} -->

Note que o diretório vhost é criado/garantido usando o módulo `file`.

A última task que adicionamos usa o módulo de template para criar o arquivo de configuração do vhost a partir de um template j2:

```yaml
- name: Template arquivo vhost
  template:
    src: vhost.conf.j2
    dest: /etc/httpd/conf.d/vhost.conf
    owner: root
    group: root
    mode: 0644
  notify:
    - restart_httpd
```
Observe que ele está usando um handler para reiniciar o httpd após uma atualização de configuração.

O arquivo completo `tasks/main.yml` é:

<!-- {% raw %} -->
```yaml
---
- name: Instalar httpd
  yum:
    name: httpd
    state: latest

- name: Start e enable o servico httpd
  service:
    name: httpd
    state: started
    enabled: true

- name: Verificar se o diretório vhost está presente
  file:
    path: "/var/www/vhosts/{{ ansible_hostname }}"
    state: directory

- name: Entregar conteúdo html
  copy:
    src: index.html
    dest: "/var/www/vhosts/{{ ansible_hostname }}"

- name: Template arquivo vhost
  template:
    src: vhost.conf.j2
    dest: /etc/httpd/conf.d/vhost.conf
    owner: root
    group: root
    mode: 0644
  notify:
    - restart_httpd
```
<!-- {% endraw %} -->


## Passo 4 - Criando o handler

Crie o handler no arquivo `handlers/main.yml` para reiniciar o httpd quando notificado pela task do template:

```yaml
---
# arquivo de handlers para roles/apache_vhost
- name: restart_httpd
  service:
    name: httpd
    state: restarted
```

## Passo 5 - Criando o index.html e template de arquivo de configuração do vhost

Crie o conteúdo HTML que será exibido pelo servidor web.

  - Crie um arquivo index.html no diretório "src" da role, `files` :

```bash
[student<X>@ansible ansible-files]$ echo 'vhost index' > ~/ansible-files/roles/apache_vhost/files/index.html
```

  - Crie o arquivo de template `vhost.conf.j2` no subdiretório `templates` da role.

<!-- {% raw %} -->
```html
# {{ ansible_managed }}

<VirtualHost *:8080>
    ServerAdmin webmaster@{{ ansible_fqdn }}
    ServerName {{ ansible_fqdn }}
    ErrorLog logs/{{ ansible_hostname }}-error.log
    CustomLog logs/{{ ansible_hostname }}-common.log common
    DocumentRoot /var/www/vhosts/{{ ansible_hostname }}/

    <Directory /var/www/vhosts/{{ ansible_hostname }}/>
  Options +Indexes +FollowSymlinks +Includes
  Order allow,deny
  Allow from all
    </Directory>
</VirtualHost>
```
<!-- {% endraw %} -->

## Passo 6 - Teste a role

Você está pronto para testar a role no `node2`. Mas como uma role não pode ser atribuída diretamente a um nó, primeiro crie um Playbook que conecte a role e o host. Crie o arquivo `test_apache_role.yml` no diretório `~/ansible-files`:

```yaml
---
- name: Use apache_vhost role playbook
  hosts: node2
  become: true

  pre_tasks:
    - debug:
        msg: 'Iniciando a configuracao do servidor web.'

  roles:
    - apache_vhost

  post_tasks:
    - debug:
        msg: 'Servidor web foi configurado.'
```

Observe as palavras-chave `pre_tasks` e` post_tasks`. Normalmente, as tasks das roles são executadas antes das tasks de um Playbook. Para controlar a ordem de execução, as `pre_tasks` são executadas antes que quaisquer roles sejam aplicadas. As `post_tasks` são executadas após a conclusão de todas as roles. Aqui, apenas as usamos para destacar melhor quando a role real é executada.

Agora você está pronto para executar seu playbook:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook test_apache_role.yml
```

Execute um comando curl no `node2` para confirmar que a role funcionou:

```bash
[student<X>@ansible ansible-files]$ curl -s http://node2:8080
vhost index
```

Deu tudo certo? Parabéns! Você concluiu com êxito os exercícios do Workshop do Ansible Engine!

----

[Clique aqui para retornar ao Workshop Ansible for Red Hat Enterprise Linux](../README.pt-br.md#seção-1---exercícios-do-ansible-engine)
