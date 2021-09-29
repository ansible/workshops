# Exercício 1.1 - Verifique os pré-requisitos

**Leia em outras linguagens**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

* [Seu ambiente de Laboratório](#seu-ambiente-de-laboratório)
* [Passo 1.1 - Acesse o ambiente](#passo-11---acesse-o-ambiente)
* [Passo 1.2 - Trabalhando nos laboratórios](#passo-12---trabalhando-nos-laboratórios)
* [Passo 1.3 - Troca de Labs](#passo-13---troca-de-labs)

## Seu ambiente de Laboratório

Neste workshop, você irá trabalhar em um ambiente de laboratório pré-configurado. Você terá acesso aos seguintes hosts:

| Role                 | Inventory name |
| ---------------------| ---------------|
| Ansible Control Host | ansible        |
| Managed Host 1       | node1          |
| Managed Host 2       | node2          |
| Managed Host 2       | node3          |

## Passo 1.1 - Acesse o ambiente

Faça Login com seu Ansible Control Host via SSH:

> **ATENÇÃO**
>
> Substitua **11.22.33.44** pelo seu **IP** fornecido a você, e o **X** em student**X** pelo número do aluno fornecido a você.

    ssh studentX@11.22.33.44

> **Dica**
>
> A senha é **instructor provides this**

Torne-se Root:

    [student<X>@ansible ~]$ sudo -i

A maioria dos pré-requisitos já foram feitos pra você:

  - O Ansible já está instalado.

  - Conexão SSH e chaves estão configuradas.

  - `sudo` foi configurado nos hosts para executar comandos que requerem privilégios de root.

Verificando se o Ansible foi instalado corretamente

    [root@ansible ~]# ansible --version
    ansible 2.7.0
    [...]

> **Nota**
>
> O Ansible possui uma configuração simples. Não requer banco de dados ou daemons em execução e pode ser executado facilmente em um notebook. Nos hosts gerenciados, ele não precisa de agente em execução.

Saia do root novamente:

    [root@ansible ~]# exit
    logout

> **Nota**
>
> Em todos os exercícios subsequentes, você deve trabalhar como usuário student\<X\> no nó de controle, a menos que seja explicitamente informado para ser feito de maneira diferente.

## Passo 1.2 - Trabalhando nos laboratórios

Você já deve ter percebido que este laboratório é centralizado em linha de comando…​ :-)

  - Não digite tudo manualmente, use copiar e colar no navegador quando apropriado. Mas pare para pensar e entender.

  - Todos os laboratórios foram preparados com o **Vim**, mas entendemos que nem todo mundo gosta dele. Sinta-se livre para usar editores alternativos. No ambiente de laboratório, fornecemos **Midnight Commander** (basta executar **mc**, as teclas de função podem ser acessadas via Esc-\<n\> ou simplesmente clicadas com o mouse) ou **Nano** (excução **nano**). Aqui está uma breve introdução do [editor](../0.0-support-docs/editor_intro.md).

> **Dica**
>
> No guia do laboratório, os comandos que você deve executar são mostrados com ou sem a saída esperada, o que fizer mais sentido no contexto.

## Passo 1.3 - Troca de Labs

Você descobrirá em breve que muitos capítulos deste guia de laboratório vêm com uma seção "Laboratório de Desafios". Esses laboratórios possuem uma pequena tarefa a ser resolvida usando o que você aprendeu até agora. A solução da tarefa é mostrada sob um sinal de aviso.

----

[Clique aqui para retornar ao Workshop Ansible for Red Hat Enterprise Linux](../README.pt-br.md#seção-1---exercícios-do-ansible-engine)
