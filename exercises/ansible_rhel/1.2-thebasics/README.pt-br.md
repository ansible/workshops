# Exercício de Workshop - Os Fundamentos do Ansible

**Leia isso em outros idiomas**:
<br>![uk](../../../images/uk.png) [Inglês](README.md), ![japan](../../../images/japan.png) [日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Português do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Francês](README.fr.md),![Español](../../../images/col.png) [Espanhol](README.es.md).

## Índice de Conteúdos <!-- omitir no toc -->

- [Objetivo](#objetivo)
- [Guia](#guia)
  - [Noções Básicas de Arquivo de Inventário](#noções-básicas-de-arquivo-de-inventário)
  - [Descoberta de Módulos](#descoberta-de-módulos)
  - [Acessando Documentação de Módulos](#acessando-documentação-de-módulos)

## Objetivo

Neste exercício, vamos explorar a mais recente ferramenta de linha de comando do Ansible, o `ansible-navigator`, para aprender a trabalhar com arquivos de inventário e a listar módulos quando precisarmos de ajuda. O objetivo é familiarizar-se com o funcionamento do `ansible-navigator` e como ele pode ser utilizado para enriquecer sua experiência com o Ansible.

## Guia

### Noções Básicas de Arquivo de Inventário

Um arquivo de inventário é um arquivo de texto que especifica os nós que serão gerenciados pela máquina de controle. Os nós a serem gerenciados podem incluir uma lista de nomes de host ou endereços IP desses nós. O arquivo de inventário permite organizar os nós em grupos, declarando um nome de grupo de host entre colchetes ([]).

### Explorando o Inventário

Para usar o comando `ansible-navigator` para gerenciamento de hosts, você precisa fornecer um arquivo de inventário que define uma lista de hosts a serem gerenciados a partir do nó de controle. Neste laboratório, o inventário é fornecido pelo seu instrutor. O arquivo de inventário é um arquivo formatado em `ini` que lista seus hosts, organizados em grupos, fornecendo também algumas variáveis. Um exemplo pode ser visto a seguir:

```bash
[web]
node1 ansible_host=<X.X.X.X>
node2 ansible_host=<Y.Y.Y.Y>
node3 ansible_host=<Z.Z.Z.Z>

[control]
ansible-1 ansible_host=44.55.66.77
```

Para visualizar seu inventário com ansible-navigator, use o comando `ansible-navigator inventory --list -m stdout`. Este comando exibe todos os nós e seus respectivos grupos.

```bash
[student@ansible-1 rhel_workshop]$ cd /home/student
[student@ansible-1 ~]$ ansible-navigator inventory --list -m stdout
{
    "_meta": {
        "hostvars": {
            "ansible-1": {
                "ansible_host": "3.236.186.92"            },
            "node1": {
                "ansible_host": "3.239.234.187"
            },
            "node2": {
                "ansible_host": "75.101.228.151"
            },
            "node3": {
                "ansible_host": "100.27.38.142"
            }
        }
    },
    "all": {
        "children": [
            "control",
            "ungrouped",
            "web"
        ]
    },
    "control": {
        "hosts": [
            "ansible-1"
        ]
    },
    "web": {
        "hosts": [
            "node1",
            "node2",
            "node3"
        ]
    }
}

```

NOTA: `-m` é uma abreviação para `--mode` que permite alternar o modo para saída padrão em vez de usar a interface de usuário baseada em texto (TUI).

Para uma visão menos detalhada, `ansible-navigator inventory --graph -m stdout` oferece uma representação visual dos agrupamentos.

```bash
[student@ansible-1 ~]$ ansible-navigator inventory --graph -m stdout
@all:
  |--@control:
  |  |--ansible-1
  |--@ungrouped:
  |--@web:
  |  |--node1
  |  |--node2
  |  |--node3

```

Podemos ver claramente que os nós: `node1`, `node2`, `node3` fazem parte do grupo `web`, enquanto `ansible-1` faz parte do grupo `control`.

Um arquivo de inventário pode organizar seus hosts em grupos ou definir variáveis. Em nosso exemplo, o inventário atual possui os grupos `web` e `control`. Execute `ansible-navigator` com esses padrões de host e observe a saída:

Usando o comando `ansible-navigator inventory`, você pode executar comandos que fornecem informações apenas para um host ou grupo. Por exemplo, execute os seguintes comandos e observe suas saídas diferentes.

```bash
[student@ansible-1 ~]$ ansible-navigator inventory --graph web -m stdout
[student@ansible-1 ~]$ ansible-navigator inventory --graph control -m stdout
[student@ansible-1 ~]$ ansible-navigator inventory --host node1 -m stdout
```

> **Dica**
>
> O inventário pode conter mais dados. Por exemplo, se você tem hosts que rodam em portas SSH não padrão, você pode colocar o número da porta após o nome do host com dois pontos. Também é possível definir nomes específicos para o Ansible e fazê-los apontar para o IP ou nome do host.

### Descoberta de Módulos

A Plataforma de Automação Ansible vem com vários Ambientes de Execução suportados (EEs). Esses EEs vêm com coleções suportadas agrupadas que contêm conteúdo suportado, incluindo módulos.

> **Dica**
>
> Em `ansible-navigator`, saia pressionando o botão `ESC`.

Para navegar pelos seus módulos disponíveis, primeiro entre no modo interativo:

```bash
$ ansible-navigator
```

![imagem do ansible-navigator](images/interactive-mode.png)

Navegue por uma coleção digitando `:collections`

```bash
:collections
```

![imagem do ansible-navigator](images/interactive-collections.png)

### Acessando Documentação de Módulos

Para explorar os módulos de uma coleção específica, insira o número ao lado do nome da coleção.

Por exemplo, na captura de tela acima, o número `0` corresponde à coleção `amazon.aws`. Para ampliar a visualização da coleção, digite o número `0`.

```bash
0
```

![imagem do ansible-navigator](images/interactive-aws.png)

Acesse diretamente a documentação detalhada de qualquer módulo especificando seu número correspondente. Por exemplo, o módulo `ec2_tag` corresponde ao número `24`.

```bash
:24
```

Rolando para baixo usando as teclas de seta ou page-up e page-down, podemos ver documentação e exemplos.

![imagem do ansible-navigator](images/interactive-ec2-tag.png)

Você pode ir diretamente para um módulo específico simplesmente digitando `:doc namespace.collection.module-name`. Por exemplo, digitar `:doc amazon.aws.ec2_tag` iria direto para a página final mostrada acima.

> **Dica**
>
> Ambientes de execução diferentes podem ter acesso a diferentes coleções e diferentes versões dessas coleções. Ao usar a documentação integrada, você sabe que será precisa para aquela versão específica da coleção.

----

[Clique aqui para retornar ao Workshop Ansible for Red Hat Enterprise Linux](../README.pt-br.md#seção-1---exercícios-do-ansible-engine)
