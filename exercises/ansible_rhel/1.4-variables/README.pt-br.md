# Exercício - Usando variáveis

**Leia em outras linguagens**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

* [Passo 1 - Criando arquivos de variáveis](#passo-1---criando-arquivos-de-variáveis)
* [Passo 2 - Criando o arquivo index.html](#passo-2---criando-o-arquivo-indexhtml)
* [Passo 3 - Criando o Playbook](#passo-3---criando-o-playbook)
* [Passo 4 - Teste o Resultado](#passo-4---teste-o-resultado)
* [Passo 5 - Ansible Facts](#passo-5---ansible-facts)
* [Passo 6 - Laboratório de desafios: Facts](#passo-6---laboratório-de-desafios-facts)
* [Passo 7 - Usando Facts em Playbooks](#passo-7---usando-facts-em-playbooks)

Os exercícios anteriores mostraram os conceitos básicos do Ansible Engine. Nos próximos exercícios, ensinaremos algumas habilidades mais avançadas que adicionarão flexibilidade e poder aos seus Playbooks.

O Ansible existe para tornar as tarefas simples e repetíveis. Também sabemos que nem todos os sistemas são exatamente iguais e geralmente exigem algumas alterações na maneira como um Playbook do Ansible é executado.

O Ansible suporta variáveis para armazenar valores que podem ser usados nos Playbooks. As variáveis podem ser definidas em vários lugares e têm uma clara precedência. Ansible substitui a variável pelo seu valor quando uma task é executada.

As variáveis são referenciadas nos Playbooks, colocando o nome da variável entre chaves duplas:

<!-- {% raw %} -->
```yaml
Isso é uma variável {{ variable1 }}
```
<!-- {% endraw %} -->

As variáveis e seus valores podem ser definidos em vários locais: no inventário, arquivos adicionais, na linha de comando etc.

A prática recomendada para fornecer variáveis no inventário é defini-las em arquivos localizados em dois diretórios denominados `host_vars` e `group_vars`:

  - Para definir variáveis para um grupo "servers", é criado um arquivo YAML chamado `group_vars/servers` com as definições de variáveis.

  - Para definir variáveis especificamente para um host `node1`, o arquivo `host_vars/node1` com as definições de variáveis é criado.

> **Dica**
>
> Variáveis de host têm precedência sobre variáveis de grupo (mais sobre precedência pode ser encontrada em [docs](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable)).

## Passo 1 - Criando arquivos de variáveis

Para entender e praticar, vamos fazer um laboratório. Seguindo o tema "Vamos construir um servidor Web, ou dois, ou ainda mais...​", você alterará o `index.html` para mostrar o ambiente de desenvolvimento (dev/prod) em que um servidor está implantado.

No host de controle ansible, como usuário `student`, crie os diretórios para conter as definições de variáveis em `~/ansible-files/` :

```bash
[student<X>@ansible ansible-files]$ mkdir host_vars group_vars
```

Agora crie dois arquivos contendo definições de variáveis. Definiremos uma variável chamada `stage` que apontará para diferentes ambientes,`dev` ou `prod`:

  - Crie o arquivo `~/ansible-files/group_vars/web` com este conteúdo:

```yaml
---
stage: dev
```

  - Crie o arquivo `~/ansible-files/host_vars/node2` com este conteúdo:

```yaml
---
stage: prod
```

O que é isso?

  - Para todos os servidores no grupo `web`, a variável `stage` com o valor `dev` é definida. Portanto, como padrão sinalizamos como membros do ambiente de desenvolvimento.

  - Para o servidor `node2`, isso é substituído e o host é sinalizado como um servidor de produção.

## Passo 2 - Criando o arquivo index.html

Agora, crie dois aquivos em `~/ansible-files/`:

Um chamado `prod_index.html` com o seguinte conteúdo:

```html
<body>
<h1>Esse eh um servidor web de producao, tenha cuidado!</h1>
</body>
```

E um chamado `dev_index.html` com o seguinte conteúdo:

```html
<body>
<h1>Esse eh um servidor web de desenvolvimento, divirta-se!</h1>
</body>
```

## Passo 3 - Criando o Playbook

Agora você precisa de um Playbook que copie o arquivo prod ou dev `index.html` - de acordo com a variável "stage".

Crie um novo playbook, chamado `deploy_index_html.yml` no diretório `~/ansible-files/`.

> **Dica**
>
> Observe como a variável "stage" é usada no nome do arquivo a ser copiado.

<!-- {% raw %} -->
```yaml
---
- name: Copia index.html
  hosts: web
  become: yes
  tasks:
  - name: Copia index.html
    copy:
      src: ~/ansible-files/{{ stage }}_index.html
      dest: /var/www/html/index.html
```
<!-- {% endraw %} -->

  - Execute o Playbook:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook deploy_index_html.yml
```

## Passo 4 - Teste o Resultado

O Playbook deve copiar arquivos diferentes como index.html para os hosts, use `curl` para testá-lo. Verifique o inventário novamente se você esqueceu os endereços IP dos seus nós.

```bash
[student<X>@ansible ansible-files]$ grep node ~/lab_inventory/hosts
node1 ansible_host=11.22.33.44
node2 ansible_host=22.33.44.55
node3 ansible_host=33.44.55.66
[student<X>@ansible ansible-files]$ curl http://11.22.33.44
<body>
<h1>Esse eh um servidor web de desenvolvimento, divirta-se!</h1>
</body>
[student1@ansible ansible-files]$ curl http://22.33.44.55
<body>
<h1>Esse eh um servidor web de producao, tenha cuidado!</h1>
</body>
[student1@ansible ansible-files]$ curl http://33.44.55.66
<body>
<h1>Esse eh um servidor web de desenvolvimento, divirta-se!</h1>
</body>
```

> **Dica**
>
> Agora você pensa: "Tem que haver uma maneira mais inteligente de alterar o conteúdo dos arquivos..." e você está absolutamente certo. Este laboratório foi realizado para introduzir variáveis, você está prestes a aprender sobre templates em um dos próximos capítulos.

## Passo 5 - Ansible Facts

Facts são variáveis que são descobertas automaticamente pelo Ansible a partir de um host gerenciado. Lembra da task "Gathering Facts" listada na saída de cada execução do `ansible-playbook`? Nesse momento, os facts são reunidos para cada nó gerenciado. Os fatos também podem ser obtidos pelo módulo `setup`. Eles contêm informações úteis armazenadas em variáveis que os administradores podem reutilizar.

Para ter uma ideia dos facts que o Ansible coleta por padrão, em seu nó de controle enquanto o usuário student executa:

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup
```

Isso pode ser demais, você pode usar filtros para limitar a saída a certos facts, a expressão é curinga no estilo shell:

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup -a 'filter=ansible_eth0'
```
Ou que tal procurar apenas facts relacionados à memória:

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup -a 'filter=ansible_*_mb'
```

## Passo 6 - Laboratório de desafios: Facts

  - Tente encontrar e imprimir a distribuição (Red Hat) de seus hosts gerenciados. Em uma linha, por favor.

> **Dica**
>
> Use grep para procurar o fact, e aplique um filtro para imprimir apenas esse fact.

> **ATENÇÃO**
>
> **Solução abaixo\!**

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup|grep distribution
[student<X>@ansible ansible-files]$ ansible node1 -m setup -a 'filter=ansible_distribution' -o
```

## Passo 7 - Usando Facts em Playbooks

Os facts podem ser usados em um Playbook como variáveis, usando a nomeação apropriada. Crie este Playbook como `facts.yml` no diretório `~/ansible-files/`:

<!-- {% raw %} -->
```yaml    
---
- name: Saida de facts em um playbook
  hosts: all
  tasks:
  - name: Print ansible facts
    debug:
      msg: O endereco IPv4 padrao de {{ ansible_fqdn }} eh {{ ansible_default_ipv4.address }}
```
<!-- {% endraw %} -->

> **Dica**
>
> O módulo "debug" é útil para, por exemplo variáveis ou expressões de depuração.

Execute-o para ver como os facts são impressos:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook facts.yml

PLAY [Saida de facts em um playbook] ******************************************

TASK [Gathering Facts] *********************************************************
ok: [node3]
ok: [node2]
ok: [node1]
ok: [ansible]

TASK [Print ansible facts] ****************************************************
ok: [node1] =>
  msg: O endereco IPv4 padrao de node1 eh 172.16.190.143
ok: [node2] =>
  msg: O endereco IPv4 padrao de node2 eh 172.16.30.170
ok: [node3] =>
  msg: O endereco IPv4 padrao de node3 eh 172.16.140.196
ok: [ansible] =>
  msg: O endereco IPv4 padrao de ansible eh 172.16.2.10

PLAY RECAP *********************************************************************
ansible                    : ok=2    changed=0    unreachable=0    failed=0   
node1                      : ok=2    changed=0    unreachable=0    failed=0   
node2                      : ok=2    changed=0    unreachable=0    failed=0   
node3                      : ok=2    changed=0    unreachable=0    failed=0   
```

----

[Clique aqui para retornar ao Workshop Ansible for Red Hat Enterprise Linux](../README.pt-br.md#seção-1---exercícios-do-ansible-engine)
