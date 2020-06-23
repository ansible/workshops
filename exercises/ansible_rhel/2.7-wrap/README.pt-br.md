# Exercício - Wrap up

**Leia em outras linguagens**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

* [Desafio final](#desafio-final)
  * [Vamos montar o stage](#vamos-montar-o-stage)
  * [O repositório Git](#o-repositório-git)
  * [Preparando o inventário](#preparando-o-inventário)
  * [Criando o Template](#criando-o-template)
  * [Check os resultados](#check-os-resultados)
  * [Adicionando Survey](#adicionando-survey)
  * [Solução](#solução)
* [Fim](#fim)

# Desafio final

Esse é o desafio final em que tentamos reunir a maior parte do que você aprendeu.

## Vamos montar o stage

Sua equipe de operações e sua equipe de desenvolvimento de aplicações gostam do que vêem no Tower. Para realmente usá-lo em seu ambiente, eles reuniram esses requisitos:

- Todos os servidores web (`node1`, `node2` e `node3`) devem entrar em um grupo

- Como os servidores web podem ser usados para fins de desenvolvimento ou produção, é necessário que haja uma maneira de sinalizá-los como "stage dev" ou "stage prod".

    - Atualmente, o `node1` é usado como de desenvolvimento e o `node2` em produção.

- Obviamente, o conteúdo de "index.html" será diferente entre os estágios dev e prod.

    - Deve haver um título na página informando o ambiente

    - Deve haver um campo de conteúdo

- O escritor de conteúdo `wweb` deve ter acesso a uma pesquisa para alterar o conteúdo dos servidores de desenvolvimento e prod.

## O repositório Git

Todo o código já está no lugar - afinal, este é um laboratório da Tower. Confira o repositório git **Workshop Project** em **https://github.com/ansible/workshop-examples**. Lá você encontrará o Plabook `webcontent.yml`, que chama a role `role_webcontent`.

Comparado à role de instalação anterior do Apache, há uma grande diferença: agora existem duas versões de um playbook `index.html` e uma task de implantar o arquivo de template que possui uma variável como parte do nome do arquivo de origem:

`dev_index.html.j2`

```html
<body>
<h1>Esse eh um servidor web de desenvolvimento, divirta-se!</h1>
{{ dev_content }}
</body>
```

`prod_index.html.j2`

```html
<body>
<h1>Esse eh um servidor web de producao, tenha cuidado!</h1>
{{ prod_content }}
</body>
```

`main.yml`

```yaml
[...]
- name: Deploy index.html from template
  template:
    src: "{{ stage }}_index.html.j2"
    dest: /var/www/html/index.html
  notify: apache-restart
```

## Preparando o inventário

É claro que há mais de uma maneira de conseguir isso, mas aqui está o que você deve fazer:

- Verifique se todos os hosts estão no grupo de inventário `Webserver`.

- Defina uma variável `stage` com o valor `dev` para o inventário `Webserver`:

    - Adicione `stage: dev` ao inventário `Webserver`, colocando-o no campo **VARIABLES** abaixo dos três traços start-yaml.

- Da mesma forma, adicione uma variável `stage: prod`, mas desta vez apenas para `node2` (clicando no nome do host) para que ela substitua a variável de inventário.

> **Dica**
>
> Certifique-se de manter os três traços que marcam o início do YAML\!

## Criando o Template

- Crie um novo **Job Template** chamado `Create Web Content` que:

    - segmenta o inventário do `Webserver`

    - usa o Playbook `rhel/apache/webcontent.yml` do novo projeto **Exemplos Ansible Workshop**

    - Define duas variáveis: `dev_content: default dev content` e `prod_content: default prod content` no **EXTRA VARIABLES FIELD**

    - Usa `Credenciais Workshop` e executa com escalação de privilégios

- Salve e execute o template

## Check os resultados

Desta vez, usamos o poder do Ansible para verificar os resultados: execute curl em cada nó localmente, orquestrado por um comando ad-hoc na linha de comando:

```bash
$ ansible web -m command -a "curl -s http://localhost:80"
 [WARNING]: Consider using the get_url or uri module rather than running 'curl'.  If you need to use command because get_url or uri is insufficient you can add 'warn: false' to this command task or set 'command_warnings=False' in ansible.cfg to get rid of this message.

node2 | CHANGED | rc=0 >>
<body>
<h1>Esse eh um servidor web de producao, tenha cuidado!</h1>
prod wweb
</body>

node1 | CHANGED | rc=0 >>
<body>
<h1>Esse eh um servidor web de desenvolvimento, divirta-se!</h1>
dev wweb
</body>

node3 | CHANGED | rc=0 >>
<body>
<h1>Esse eh um servidor web de desenvolvimento, divirta-se!</h1>
dev wweb
</body>
```

Observe o aviso na primeira linha sobre não usar o `curl` através do módulo `command`, pois existem módulos melhores dentro do Ansible. Voltaremos a isso na próxima parte.

## Adicionando Survey

- Adicione uma survey ao template para permitir alterar as variáveis `dev_content` e `prod_content`

- Adicione permissões ao Team `Web Content` para que o Template **Create Web Content** possa ser executado por `wweb`.

- Execute a survey como usuário `web`

Verifique os resultados. Desde que recebemos um aviso da última vez usando `curl` através do módulo `command`, desta vez usaremos o módulo `uri` dedicado. Como argumentos, ele precisa da URL real e de um sinalizador para exibir o corpo nos resultados.

```bash
$ ansible web -m uri -a "url=http://{{ ansible_host }}/ return_content=yes"
node2 | SUCCESS => {
    "accept_ranges": "bytes",
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "connection": "close",
    "content": "<body>\n<h1>Esse eh um servidor web de producao, tenha cuidado!</h1>\nprod wweb\n</body>\n",
    "content_length": "77",
    "content_type": "text/html; charset=UTF-8",
    "cookies": {},
    "cookies_string": "",
    "date": "Wed, 10 Jul 2019 22:15:45 GMT",
    "elapsed": 0,
    "etag": "\"4d-58d5aef2a5666\"",
    "last_modified": "Wed, 10 Jul 2019 22:09:42 GMT",
    "msg": "OK (77 bytes)",
    "redirected": false,
    "server": "Apache/2.4.6 (Red Hat Enterprise Linux)",
    "status": 200,
    "url": "http://localhost"
}
[...]
```

## Solução

> **ATENÇÃO**
>
> **A solução não está abaixo**

Você já executou todas as etapas de configuração necessárias no laboratório. Se não tiver certeza, basta consultar os respectivos capítulos.

# Fim

Parabéns, você terminou seus laboratórios\! Esperamos que você tenha gostado do seu primeiro encontro com o Ansible Tower, tanto quanto gostamos de criar os laboratórios.

----

[Clique aqui para retornar ao Workshop Ansible for Red Hat Enterprise Linux](../README.pt-br.md#seção-2---exercícios-do-ansible-tower)
