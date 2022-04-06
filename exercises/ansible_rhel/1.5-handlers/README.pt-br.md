# Exercício - Condicionais, Handlers and Loops

**Leia em outras linguagens**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

* [Passo 1 - Condicionais](#passo-1---condicionais)
* [Passo 2 - Handlers](#passo-2---handlers)
* [Passo 3 - Loops simples](#passo-3---loops-simples)
* [Passo 4 - Loops sobre hashes](#passo-4---loops-sobre-hashes)

## Passo 1 - Condicionais

O Ansible pode usar condicionais para executar tasks ou plays quando determinadas condições forem atendidas.

Para implementar uma condicional, a instrução `when` deve ser usada, seguida pela condição. A condição é expressa usando um dos operadores disponíveis, como por exemplo para comparação:

|      |                                                                        |
| ---- | ---------------------------------------------------------------------- |
| \==  | Compara se dois objetos são iguais.                                    |
| \!=  | Compara se dois objetos não são iguais.                                |
| \>   | Verdadeiro se um objeto for maior que o outro.                         |
| \>=  | Verdadeiro se um objeto for maior ou igual ao outro.                   |
| \<   | Verdadeiro se um objeto for menor que o outro.                         |
| \< = | Verdadeiro se um objeto for menor ou igual ao outro.                   |

Para mais informações, consulte a documentação: <http://jinja.pocoo.org/docs/2.10/templates/>

Como exemplo, você gostaria de instalar um servidor FTP, apenas em hosts que estão no grupo de inventário "ftpserver".

Para fazer isso, edite primeiro o inventário para adicionar outro grupo e coloque o `node2` nele. Certifique-se de que o endereço IP do `node2` seja sempre o mesmo quando o `node2` estiver listado. Edite o inventário `~/lab_inventory/hosts`, ele deve ficar semelhante a:

```ini
[web]
node1 ansible_host=11.22.33.44
node2 ansible_host=22.33.44.55
node3 ansible_host=33.44.55.66

[ftpserver]
node2 ansible_host=22.33.44.55

[control]
ansible ansible_host=44.55.66.77
```

Depois, crie o arquivo `ftpserver.yml` no seu host de controle no diretório `~/ansible-files/`:

```yaml
---
- name: Instalar vsftpd no ftpserver
  hosts: all
  become: yes
  tasks:
    - name: Instalar servidor FTP quando host fizer parte do grupo ftpserver
      yum:
        name: vsftpd
        state: latest
      when: inventory_hostname in groups["ftpserver"]
```

> **Dica**
>
> Agora você já deve saber como executar um playbook do Ansible, por isso começaremos a ser menos detalhados neste guia. Crie o playbook e execute-o. :-)

Execute-o e examine a saída. O resultado esperado: a task é ignorada no node1, node3 e no host ansible (seu host de controle) porque eles não estão no grupo ftpserver no seu arquivo de inventário.

```bash
TASK [Instalar servidor FTP quando host fizer parte do grupo ftpserver] *******************************************
skipping: [ansible]
skipping: [node1]
skipping: [node3]
changed: [node2]
```

## Passo 2 - Handlers

As vezes, quando uma task faz uma alteração no sistema, pode ser necessário executar uma task ou tasks adicionais. Por exemplo, uma alteração no arquivo de configuração de um serviço pode exigir que o serviço seja reiniciado para que a configuração alterada entre em vigor.

Aqui, os handlers entram em cena. Os handlers podem ser vistos como tasks inativas que só são acionadas quando invocadas explicitamente usando a instrução "notify". Leia mais sobre eles na documentação [Ansible Handlers](http://docs.ansible.com/ansible/latest/playbooks_intro.html#handlers-running-operations-on-change).

Como exemplo, vamos escrever um Playbook que:

  - Gerencia o arquivo de configuração do Apache `httpd.conf` em todos os hosts no grupo `web`.

  - Reinicia o Apache quando o arquivo é alterado.

Primeiro, precisamos que o arquivo Ansible seja implantado, vamos pegar node1. Lembre-se de substituir o endereço IP mostrado na lista abaixo pelo endereço IP do seu `node1` individual.

```bash
[student<X>@ansible ansible-files]$ scp 11.22.33.44:/etc/httpd/conf/httpd.conf ~/ansible-files/.
student<X>@11.22.33.44's password:
httpd.conf             
```

Depois, crie o playbook `httpd_conf.yml`. Verifique se você está no diretório `~/ansible-files`.

```yaml
---
- name: Manage httpd.conf
  hosts: web
  become: yes
  tasks:
  - name: Copiar arquivo de configuracao do Apache
    copy:
      src: httpd.conf
      dest: /etc/httpd/conf/
    notify:
        - restart_apache
  handlers:
    - name: restart_apache
      service:
        name: httpd
        state: restarted
```

Então, o que há de novo aqui?

  - A seção "notify" chama o handler somente quando a task de cópia realmente altera o arquivo. Dessa forma, o serviço será reiniciado apenas se necessário - e não sempre que o playbook for executado.

  - A seção "handlers" define uma task que é executada apenas na notificação.

Execute o Playbook. Ainda não alteramos nada no arquivo, portanto, não deve haver linhas 'alteradas' na saída e o manipulador não deveria ter disparado.

  - Agora mude a linha `Listen 80` no httpd.conf para:


```ini
Listen 8080
```

  - Execute o Playbook novamente. Agora a saída do Ansible deve ser muito mais interessante:

      - httpd.conf deve ter sido copiado.

      - O handler deve ter reiniciado o Apache.

O Apache agora deve escutar na porta 8080. Fácil o suficiente para verificar:

```bash
[student1@ansible ansible-files]$ curl http://22.33.44.55
curl: (7) Failed connect to 22.33.44.55:80; Connection refused
[student1@ansible ansible-files]$ curl http://22.33.44.55:8080
<body>
<h1>Esse eh um servidor web de producao, tenha cuidado!</h1>
</body>
```
Sinta-se livre para alterar o arquivo httpd.conf novamente e executar o Playbook.

## Passo 3 - Loops simples

Os loops nos permitem repetir a mesma task. Por exemplo, digamos que você queira criar vários usuários. Usando um loop, você pode fazer isso em uma única task. Os loops também podem iterar mais do que apenas listas básicas. Por exemplo, se você tiver uma lista de usuários com seu grupo de correspondência, o loop também poderá iterar sobre eles. Saiba mais sobre loops na documentação [Ansible Loops](https://docs.ansible.com/ansible/latest/user_guide/playbooks_loops.html).

Para mostrar o recurso de loops, geramos três novos usuários no `node1`. Para isso, crie o arquivo `loop_users.yml` em `~/ansible-files` no seu nó de controle com seu usuário student. Usaremos o módulo `user` para gerar as contas de usuário.

<!-- {% raw %} -->
```yaml
---
- name: Garantir usuarios
  hosts: node1
  become: yes

  tasks:
    - name: Garantir a presenca de tres usuarios
      user:
        name: "{{ item }}"
        state: present
      loop:
         - dev_user
         - qa_user
         - prod_user
```
<!-- {% endraw %} -->

Entenda o playbook e a saída:

<!-- {% raw %} -->
  - Os nomes não são fornecidos diretamente ao módulo do usuário. Em vez disso, existe apenas uma variável chamada `{{ item }}` para o parâmetro `name`.

  - A palavra-chave `loop` lista os nomes de usuário reais. O `{{ item }}` é substituido durante a execução real do Playbook.

  - Durante a execução, a task é listada apenas uma vez, mas há três alterações listadas abaixo dela.
<!-- {% endraw %} -->

## Passo 4 - Loops sobre hashes

Como mencionado, os loops também podem estar sobre listas de hashes. Imagine que os usuários devam ser atribuídos a diferentes grupos adicionais:

```yaml
- username: dev_user
  groups: ftp
- username: qa_user
  groups: ftp
- username: prod_user
  groups: apache
```

O módulo `user` possui o parâmetro opcional `groups` para listar usuários adicionais. Para referenciar itens em um hash, a palavra-chave `{{ item }}` precisa fazer referência à subchave: `{{ item.groups }}` por exemplo.

Vamos reescrever o Playbook para criar os usuários com direitos adicionais:

<!-- {% raw %} -->
```yaml
---
- name: Garantir usuarios
  hosts: node1
  become: yes

  tasks:
    - name: Garantir a presenca de tres usuarios
      user:
        name: "{{ item.username }}"
        state: present
        groups: "{{ item.groups }}"
      loop:
        - { username: 'dev_user', groups: 'ftp' }
        - { username: 'qa_user', groups: 'ftp' }
        - { username: 'prod_user', groups: 'apache' }

```
<!-- {% endraw %} -->

Verifique a saída:

  - Novamente, a task é listada uma vez, mas três alterações são listadas. Cada loop com seu conteúdo é mostrado.

Verifique se o usuário `prod_user` foi realmente criado no `node1`:

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m command -a "id dev_user"
node1 | CHANGED | rc=0 >>
uid=1002(dev_user) gid=1002(dev_user) Gruppen=1002(dev_user),50(ftp)
```

----

[Clique aqui para retornar ao Workshop Ansible for Red Hat Enterprise Linux](../README.pt-br.md#seção-1---exercícios-do-ansible-engine)
