# Exercicio 1.8 - Labs Bônus

**Read this in other languages**: ![uk](../../../../images/uk.png) [English](README.md),  ![japan](../../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md).

* [Passo 8.1 - Lab Bônus: Comandos Ad Hoc](#passo-81---lab-bônus-comandos-ad-hoc)
* [Passo 8.2 - Lab Bônus: Templates e variáveis](#passo-82---lab-bônus-templates-e-variáveis)
   * [Define as variáveis:](#define-as-variáveis)
   * [Prepare o template:](#prepare-o-template)
   * [Crie o Playbook](#crie-o-playbook)
   * [Execute e teste](#execute-e-teste)

Você já terminou o laboratório. Mas preparamos alguns laboratórios de bônus um pouco mais avançados para você seguir, se quiser. Portanto, se você terminou os laboratórios e ainda tem algum tempo, aqui estão mais alguns laboratórios para você:

## Passo 8.1 - Lab Bônus: Comandos Ad Hoc

Crie um novo usuário "testuser" em `node1` e `node3` usando um comando ad hoc, verifique se ele não foi criado no `node2`!

  - Encontre os parâmetros para o módulo apropriado usando `ansible-doc user` (saia com `q`)

  - Use um comando Ansible ad hoc para criar o usuário com o comentário "Test User"

  - Use o módulo "command" com a chamada adequada para encontrar o ID do usuário

  - Exclua o usuário e verifique se ele foi excluído

> **Dica**
>
> Lembre-se da escalação de privilégios…​

> **ATENÇÃO**
>
> **Solução abaixo\!**

Seus comandos podem ser parecidos com estes:

```bash
[student<X>@ansible ansible-files]$ ansible-doc -l | grep -i user
[student<X>@ansible ansible-files]$ ansible-doc user
[student<X>@ansible ansible-files]$ ansible node1,node3 -m user -a "name=testuser comment='Test User'" -b
[student<X>@ansible ansible-files]$ ansible node1,node3 -m command -a " id testuser" -b
[student<X>@ansible ansible-files]$ ansible node2 -m command -a " id testuser" -b
[student<X>@ansible ansible-files]$ ansible node1,node3 -m user -a "name=testuser state=absent remove=yes" -b
[student<X>@ansible ansible-files]$ ansible web -m command -a " id testuser" -b
```

## Passo 8.2 - Lab Bônus: Templates e variáveis

Você aprendeu o básico sobre templates, variáveis e handlers. Vamos combinar tudo isso.

Em vez de editar e copiar `httpd.conf`, por que você não define uma variável para a porta de escuta e a usa em um template? Aqui está o seu trabalho:

  - Defina uma variável `listen_port` para o grupo `web` com o valor `8080` e outra para `node2` com o valor `80` usando os arquivos adequados.

  - Copie o arquivo `httpd.conf` no template `httpd.conf.j2` que usa a variável `listen_port` em vez do número da porta codificada.

  - Escreva um Playbook que implante o template e reinicie o Apache nas alterações usando um handler.

  - Execute o Playbook e teste o resultado usando `curl`.

> **Dica**
>
> Lembra dos diretórios `group_vars` e `host_vars`? Caso contrário, consulte o capítulo "Variáveis".

> **ATENÇÃO**
>
> **Solução abaixo\!**

### Define as variáveis:

Adicione esta linha a `group_vars/web`:

```ini
listen_port: 8080
```

Adicione esta linha a `host_vars/node2`:

```ini
listen_port: 80
```
### Prepare o template:

  - Copie `httpd.conf` para `httpd.conf.j2`

  - Edite a diretiva "Listen" em `httpd.conf.j2` para deixa-la assim:

<!-- {% raw %} -->
```ini
[...]
Listen {{ listen_port }}
[]...]
```
<!-- {% endraw %} -->

### Crie o Playbook

Crie o playbook chamado `apache_config_tpl.yml`:

```yaml
---
- name: Apache httpd.conf
  hosts: web
  become: yes
  tasks:
  - name: Criar arquivo de configuracao do apache a partir do template
    template:
      src: httpd.conf.j2
      dest: /etc/httpd/conf/httpd.conf
    notify:
        - restart apache
  handlers:
    - name: Reiniciar apache
      service:
        name: httpd
        state: restarted
```

### Execute e teste

Primeiro, execute o próprio Playbook e em seguida, execute curl no `node1` com a porta` 8080` e `node2` na porta` 80`.

```bash
[student1@ansible ansible-files]$ ansible-playbook apache_config_tpl.yml
[...]
[student1@ansible ansible-files]$ curl http://18.195.235.231:8080
<body>
<h1>Esse eh um servidor web de desenvolvimento, divirta-se!</h1>
</body>
[student1@ansible ansible-files]$ curl http://35.156.28.209:80
<body>
<h1>Esse eh um servidor web de producao, tenha cuidado!</h1>
</body>
```

----

[Clique aqui para retornar ao Workshop Ansible for Red Hat Enterprise Linux](../../README.pt-br.md#seção-1---exercícios-do-ansible-engine)
