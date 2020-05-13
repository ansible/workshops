# Exercício - Executando comandos ad-hoc

**Leia em outras linguagens**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

Em nosso primeiro exercício, executaremos alguns comandos ad-hoc para ajudá-lo a entender como o Ansible funciona. Os comandos ad-hoc permitem executar tarefas em nós remotos sem precisar escrever um manual. Eles são muito úteis quando você simplesmente precisa fazer uma ou duas coisas de maneira rápida e frequente para muitos nós remotos.

## Table of Contents

* [Passo 1 - Trabalhe com seu inventário](#passo-1---trabalhe-com-seu-inventário)
* [Passo 2 - Arquivos de configuração Ansible](#passo-2---arquivos-de-configuração-ansible)
* [Passo 3 - Pingando um host](#passo-3---pingando-um-host)
* [Passo 4 - Como listar módulos e obter ajuda](#passo-4---como-listar-módulos-e-obter-ajuda)
* [Passo 5 - Use o módulo de command:](#passo-5---use-o-módulo-de-command)
* [Passo 6 - O módulo de cópia e permissões](#passo-6---o-módulo-de-cópia-e-permissões)
* [Laboratório de Desafios: Módulos](#laboratório-de-desafios-módulos)


## Passo 1 - Trabalhe com seu inventário

Para usar o comando ansible para gerenciamento de host, é necessário fornecer um arquivo de inventário que defina uma lista de hosts a serem gerenciados a partir do nó de controle. Neste laboratório, o inventário é fornecido pelo seu instrutor. O inventário é um arquivo listando seus hosts, classificando em grupos, além de fornecer algumas variáveis. É parecido com isso:

```bash
[all:vars]
ansible_user=student1
ansible_ssh_pass=PASSWORD
ansible_port=22

[web]
node1 ansible_host=<X.X.X.X>
node2 ansible_host=<Y.Y.Y.Y>
node3 ansible_host=<Z.Z.Z.Z>

[control]
ansible ansible_host=44.55.66.77
```

O Ansible já está configurado para usar o inventário específico para o seu ambiente. Mostraremos na próxima etapa como isso é feito. Por enquanto, executaremos alguns comandos simples para trabalhar com o inventário.

Para referenciar hosts de inventário, você fornece um padrão de host ao comando ansible. O Ansible possui a opção `--list-hosts` que pode ser útil para esclarecer quais hosts gerenciados são referenciados pelo padrão de host em um comando ansible.

O padrão de host mais básico é o nome de um único host gerenciado listado no arquivo de inventário. Isso especifica que o host será o único no arquivo de inventário que será acionado pelo comando ansible. Execute:

```bash
[student<X@>ansible ~]$ ansible node1 --list-hosts
  hosts (1):
    node1
```

Um arquivo de inventário pode conter muitas outras informações, como organizar seus hosts em grupos ou definir variáveis. No nosso exemplo, o inventário atual possui os grupos `web` e `control`. Execute o Ansible com esses padrões de host e observe a saída:

```bash
[student<X@>ansible ~]$ ansible web  --list-hosts
[student<X@>ansible ~]$ ansible web,ansible --list-hosts
[student<X@>ansible ~]$ ansible 'node*' --list-hosts
[student<X@>ansible ~]$ ansible all --list-hosts
```

Como você pode ver, não há problema em colocar sistemas em mais de um grupo. Por exemplo, um servidor pode ser um servidor web e um servidor de banco de dados. Observe que no Ansible os grupos não são necessariamente hierárquicos.

> **Dica**
>
> O inventário pode conter mais dados. Por exemplo, se você possui hosts que executam em portas SSH não padrão, pode colocar o número da porta após o nome do host com dois pontos. Ou pode definir nomes específicos para o Ansible e fazer com que aponte para o IP ou nome de host "real".

## Passo 2 - Arquivos de configuração Ansible

O comportamento do Ansible pode ser personalizado modificando as configurações no arquivo de configuração do Ansible. O Ansible selecionará seu arquivo de configuração em um dos vários locais possíveis no nó de controle, consulte a [documentação](https://docs.ansible.com/ansible/latest/reference_appendices/config.html).

> **Dica**
>
> A prática recomendada é criar um arquivo `ansible.cfg` no diretório a partir do qual você executa os comandos Ansible. Esse diretório também contém todos os arquivos usados pelo seu projeto Ansible, como o inventário e os playbooks. Outra prática recomendada é criar um arquivo `.ansible.cfg` no seu diretório pessoal.

No ambiente de laboratório fornecido a você, um arquivo `.ansible.cfg` já foi criado e preenchido com os detalhes necessários no diretório inicial do seu usuário `student<X>` no nó de controle:

```bash
[student<X>@ansible ~]$ ls -la .ansible.cfg
-rw-r--r--. 1 student<X> student<X> 231 14. Mai 17:17 .ansible.cfg
```

Saída do conteúdo do arquivo:

```bash
[student<X>@ansible ~]$ cat .ansible.cfg
[defaults]
stdout_callback = yaml
connection = smart
timeout = 60
deprecation_warnings = False
host_key_checking = False
retry_files_enabled = False
inventory = /home/student<X>/lab_inventory/hosts
```

Existem vários sinalizadores de configuração fornecidos. A maioria deles não é interessante aqui, mas lembre-se da última linha: lá é fornecida a localização do inventário. Essa é a maneira que o Ansible sabe nos comandos anteriores a que máquinas se conectar.

Saída de conteúdo do seu inventário dedicado:

```bash
[student<X>@ansible ~]$ cat /home/student<X>/lab_inventory/hosts
[all:vars]
ansible_user=student<X>
ansible_ssh_pass=ansible
ansible_port=22

[web]
node1 ansible_host=11.22.33.44
node2 ansible_host=22.33.44.55
node3 ansible_host=33.44.55.66

[control]
ansible ansible_host=44.55.66.77
```

> **Dica**
>
> Observe que cada aluno tem um ambiente de laboratório individual. Os endereços IP mostrados acima são apenas um exemplo e os endereços IP de seus ambientes individuais são diferentes. Como nos outros casos, substitua **\<X\>** pelo número real do aluno.

## Passo 3 - Pingando um host

> **ATENÇÃO**
>
> **Não se esqueça de executar os comandos no diretório inicial do usuário do aluno, `/home/student<X>`. É aí que o seu arquivo `.ansible.cfg` está localizado, sem ele o Ansible não saberá qual inventário usar.**

Vamos começar com algo realmente básico - executando ping em um host. Para fazer isso, usamos o módulo `ping`. O módulo `ping` garante que nossos hosts de destino sejam responsivos. Basicamente, ele se conecta ao host gerenciado, executa um pequeno script e coleta os resultados. Isso garante que o host gerenciado esteja acessível e que o Ansible possa executar comandos corretamente nele.

> **Dica**
>
> Pense em um módulo como uma ferramenta projetada para realizar uma tarefa específica.

O Ansible precisa saber que deve usar o módulo `ping` : A opção `-m` define qual módulo usar. As opções podem ser passadas para o módulo especificado usando a opção `-a`.

```bash
[student<X>@ansible ~]$ ansible web -m ping
node2 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
[...]
```

Como você vê cada nó relata a execução bem-sucedida e o resultado real - "pong".

## Passo 4 - Como listar módulos e obter ajuda

O Ansible vem com muitos módulos por padrão. Para listar todos os módulos, execute:

```bash
[student<X>@ansible ~]$ ansible-doc -l
```

> **Dica**
>
> No `ansible-doc`, pressione o botão `q`. Use as setas `up`/`down` para rolar pelo conteúdo.

Para encontrar um módulo, tente por exemplo:

```bash
[student<X>@ansible ~]$ ansible-doc -l | grep -i user
```

Obtenha ajuda para um módulo específico, incluindo exemplos de uso:

```bash
[student<X>@ansible ~]$ ansible-doc user
```

> **Dica**
>
> As opções obrigatórias são marcadas com "=" em `ansible-doc`.

## Passo 5 - Use o módulo de command:

Agora vamos ver como podemos executar um bom e velho comando Linux e formatar a saída usando o módulo `command`. Ele simplesmente executa o comando especificado em um host gerenciado:

```bash
[student<X>@ansible ~]$ ansible node1 -m command -a "id"
node1 | CHANGED | rc=0 >>
uid=1001(student1) gid=1001(student1) Gruppen=1001(student1) Kontext=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
```
Nesse caso, o módulo é chamado de `command` e a opção passada com `-a` é o comando real a ser executado. Tente executar este comando ad hoc em todos os hosts gerenciados usando o padrão de host `all`.

Outro exemplo: Veja rapidamente as versões do kernel que seus hosts estão executando:

```bash
[student<X>@ansible ~]$ ansible all -m command -a 'uname -r'
```

Às vezes, é desejável ter a saída para um host em uma linha:

```bash
[student<X>@ansible ~]$ ansible all -m command -a 'uname -r' -o
```

> **Dica**
>
> Como muitos comandos do Linux, o `ansible` permite opções longas e curtas. Por exemplo, `ansible web --module-name ping` é o mesmo que executar `ansible web -m ping`. Usaremos as opções resumidas ao longo deste workshop.

## Passo 6 - O módulo de cópia e permissões

Usando o módulo `copy`, execute um comando ad hoc no `node1` para alterar o conteúdo do arquivo `/etc/motd`. **Neste caso o conteúdo é entregue ao módulo através de uma opção**.

Execute o seguinte, mas **espere um erro**:

```bash
[student<X>@ansible ~]$ ansible node1 -m copy -a 'content="Managed by Ansible\n" dest=/etc/motd'
```
Como mencionado, isso produz um **erro**:

```bash
    node1 | FAILED! => {
        "changed": false,
        "checksum": "a314620457effe3a1db7e02eacd2b3fe8a8badca",
        "failed": true,
        "msg": "Destination /etc not writable"
    }
```

A saída do comando ad hoc está alertando **FAILED** em vermelho para você. Por quê? Porque o usuário **student\<X\>** não tem permissão para gravar o arquivo motd.

Este é um caso de escalonamento de privilégios e a razão pela qual o `sudo` precisa ser configurado corretamente. Precisamos instruir o Ansible a usar o `sudo` para executar o comando como root usando o parâmetro `-b` (pense em "Become").

> **Dica**
>
> O Ansible se conectará às máquinas usando seu nome de usuário atual (aluno\<X\> neste caso), assim como o SSH faria. Para substituir o nome de usuário remoto, você pode usar o parâmetro `-u`.

Para nós, não há problema em se conectar como `student<X>` porque o `sudo` está configurado. Mude o comando para usar o parâmetro `-b` e execute novamente:

```bash
[student<X>@ansible ~]$ ansible node1 -m copy -a 'content="Managed by Ansible\n" dest=/etc/motd' -b
```

Desta vez, o comando é um sucesso:

```bash
node1 | CHANGED => {
    "changed": true,
    "checksum": "4458b979ede3c332f8f2128385df4ba305e58c27",
    "dest": "/etc/motd",
    "gid": 0,
    "group": "root",
    "md5sum": "65a4290ee5559756ad04e558b0e0c4e3",
    "mode": "0644",
    "owner": "root",
    "secontext": "system_u:object_r:etc_t:s0",
    "size": 19,
    "src": "/home/student1/.ansible/tmp/ansible-tmp-1557857641.21-120920996103312/source",
    "state": "file",
    "uid": 0
```

Use Ansible com o módulo genérico `command` para verificar o conteúdo do arquivo motd:

```bash
[student<X>@ansible ~]$ ansible node1 -m command -a 'cat /etc/motd'
node1 | CHANGED | rc=0 >>
Managed by Ansible
```

Execute o comando `ansible node1 -m copy…​` de cima novamente. Nota:

   - A cor de saída diferente (configuração de terminal adequada fornecida).
   - A mudança de `"changed": true,` para `"changed": false,`.
   - A primeira linha diz `SUCCESS` em vez de`CHANGED`.

> **Dica**
>
> Isso facilita muito a identificação de alterações e o que o Ansible realmente fez.

## Laboratório de Desafios: Módulos

  - Usando o `ansible-doc`

       - Encontre um módulo que use o Yum para gerenciar pacotes de software.

       - Procure os exemplos de ajuda do módulo para saber como instalar um pacote na versão mais recente.

       - Execute um comando Ansible ad hoc para instalar o pacote "squid" na versão mais recente no `node1`.

> **Dica**
>
> Use o comando ad hoc copy de cima como modelo e altere o módulo e as opções.

> **ATENÇÃO**
>
> **Solução abaixo\!**

```bash
[student<X>@ansible ~]$ ansible-doc -l | grep -i yum
[student<X>@ansible ~]$ ansible-doc yum
[student<X>@ansible ~]$ ansible node1 -m yum -a 'name=squid state=latest' -b
```

----

[Clique aqui para retornar ao Workshop Ansible for Red Hat Enterprise Linux](../README.pt-br.md#seção-1---exercícios-do-ansible-engine)
