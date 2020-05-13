# Exercício - Escrevendo seu primeiro Playbook

**Leia em outras linguagens**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

* [Passo 1 - Noções básicas do Playbook](#passo-1---noções-básicas-do-playbook)
* [Passo 2 - Criando uma estrutura de diretórios e um arquivo para o seu Playbook](#passo-2---criando-uma-estrutura-de-diretórios-e-um-arquivo-para-o-seu-playbook)
* [Passo 3 - Rodando o Playbook](#passo-3---rodando-o-playbook)
* [Passo 4 - Amplie seu playbook: Apache Start &amp; Enable](#passo-4---amplie-seu-playbook-apache-start--enable)
* [Passo 5 - Ampliando seu Playbook: Criando um aquivo web.html](#passo-5---ampliando-seu-playbook-criando-um-aquivo-indexhtml)
* [Passo 6 - Pratique: Aplicar a vários hosts](#passo-6---pratique-aplicar-a-vários-hosts)

Embora os comandos Ansible ad hoc sejam úteis para operações simples, eles não são adequados para cenários complexos de gerenciamento ou orquestração de configurações. Para tais casos de uso, os playbooks são o caminho a percorrer.

Playbooks são arquivos que descrevem as configurações ou etapas desejadas para implementar em hosts gerenciados. Os Playbooks podem transformar tarefas administrativas complexas e longas em rotinas facilmente repetíveis, com resultados previsíveis e bem-sucedidos.

Um Playbook é onde você pode pegar alguns desses comandos ad-hoc que você acabou de executar e colocá-los em um conjunto repetitivo de *plays* e *tasks*.

Um Playbook pode ter várias plays e uma play pode ter uma ou várias tasks. Em uma task, um *módulo* é chamado, como os módulos do capítulo anterior. O objetivo de um *play* é mapear um grupo de hosts. O objetivo de uma *task* é implementar módulos nesses hosts.

> **Dica**
>
> Uma boa analogia: quando os módulos Ansible são as ferramentas da sua oficina, o inventário é o material e os Playbooks são as instruções.

## Passo 1 - Noções básicas do Playbook

Playbooks são arquivos de texto escritos no formato YAML e, portanto, precisam:

  - Começar com três traços (`---`)

  - Recuo adequado usando espaços e **não** tabs\!

Existem alguns conceitos importantes:

  - **hosts**: Os hosts gerenciados para executar as tasks.

  - **tasks**: As operações a serem executadas chamando os módulos e passando as opções necessárias.

  - **become**: Escalação de privilégios nos Playbooks, o mesmo que usar `-b` no comando ad hoc.

> **ATENÇÃO**
>
> A ordem do conteúdo em um Playbook é importante, porque o Ansible executa plays e tasks na ordem em que são apresentadas.

Um Playbook deve ser **idempotente**, portanto se um Playbook for executado uma vez para colocar os hosts no estado correto, deve ser seguro executá-lo uma segunda vez e não deverá fazer mais alterações nos hosts.

> **Dica**
>
> A maioria dos módulos Ansible é idempotente, portanto é relativamente fácil garantir que isso seja verdade.

## Passo 2 - Criando uma estrutura de diretórios e um arquivo para o seu Playbook

Chega de teoria, é hora de criar seu primeiro Playbook. Neste laboratório, você cria um Playbook para configurar um servidor web Apache em três etapas:

  - 1ª Etapa: Instalar o pacote httpd

  - 2ª Etapa: Enable/start o serviço httpd

  - 3ª Etapa: Criar um aquivo web.html

Este Playbook garante que o pacote que contém o servidor Apache esteja instalado no `node1`.

Há uma [melhor prática(http://docs.ansible.com/ansible/playbooks_best_practices.html) nas estruturas de diretório recomendadas para playbooks. Nós recomendamos a ler e entender essas práticas ao desenvolver suas habilidades de Ansible ninja. Dito isto, nosso Playbook hoje é muito básico e criar uma estrutura complexa apenas confundirá as coisas.

Em vez disso, vamos criar uma estrutura de diretórios muito simples para nosso playbook e adicionar apenas alguns arquivos a ele.

No host de controle **ansible**, crie um diretório chamado `ansible-files` no seu diretório pessoal e altere os diretórios para ele:

```bash
[student<X>@ansible ~]$ mkdir ansible-files
[student<X>@ansible ~]$ cd ansible-files/
```

Adicione um arquivo chamado `apache.yml` com o seguinte conteúdo. Conforme discutido nos exercícios anteriores, use `vi`/`vim` ou, se você é novo nos editores na linha de comando, consulte a [introdução do editor](../0.0-support-docs/editor_intro.md) novamente.

```yaml
---
- name: Apache server instalado
  hosts: node1
  become: yes
```

Isso mostra uma das forças do Ansible: a sintaxe do Playbook é fácil de ler e entender. Neste manual:

  - Um nome é dado para a Play via `name:`.

  - O host para qual irá executar o Playbook é definido por meio de`hosts:`.

  - Ativamos a escalação de privilégios de usuário com `become:`.

> **Dica**
>
> Obviamente, você precisa usar a escalação de privilégios para instalar um pacote ou executar qualquer outra task que exija permissões de root. Isso é feito no Playbook por `Become: yes'.

Agora que definimos a play, vamos adicionar uma task para fazer algo. Adicionaremos uma task na qual o yum garantirá que o pacote Apache esteja instalado na versão mais recente. Modifique o arquivo para que ele se pareça com a seguinte listagem:

```yaml
---
- name: Apache server instalado
  hosts: node1
  become: yes
  tasks:
  - name: Ultima versao do apache server instalado
    yum:
      name: httpd
      state: latest
```
> **Dica**
>
> Como os playbooks são escritos em YAML, o alinhamento das linhas e das palavras-chave é crucial. Certifique-se de alinhar verticalmente o *t* em `task` com o *b* em` become`. Quando você estiver mais familiarizado com o Ansible, reserve um tempo e estude um pouco a [Sintaxe YAML](http://docs.ansible.com/ansible/YAMLSyntax.html).

Nas linhas adicionadas:

  - Começamos a parte das tasks com a palavra-chave `tasks:`.

  - Uma task é nomeada e o módulo da task é referenciado. Aqui ele usa o módulo `yum`.

  - Parâmetros para o módulo são adicionados:

    - `name:` identifica o nome do pacote.
    - `state:` para definir o estado desejado do pacote.

> **Dica**
>
> Os parâmetros do módulo são individuais para cada módulo. Em caso de dúvida, procure-os novamente com `ansible-doc`.

Salve seu Playbook e saia do Editor.

## Passo 3 - Rodando o Playbook

Playbooks são executados usando o comando `ansible-playbook` no nó de controle. Antes de executar um novo Playbook, é uma boa ideia verificar se há erros de sintaxe:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook --syntax-check apache.yml
```

Agora você deve estar pronto para executar seu Playbook:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook apache.yml
```
A saída não deve relatar nenhum erro, e sim fornecer uma visão geral das tasks executadas e uma recapitulação de reprodução resumindo o que foi feito. Há também uma task chamada "Gathering Facts" listada: esta é uma task interna que é executada automaticamente no início de cada Play. Ele coleta informações sobre os nós gerenciados. Os exercícios posteriores abordarão isso com mais detalhes.

Use o SSH para garantir que o Apache tenha sido instalado no `node1`. O endereço IP necessário é fornecido no inventário.

```bash
[student<X>@ansible ansible-files]$ grep node1 ~/lab_inventory/hosts
node1 ansible_host=11.22.33.44
[student<X>@ansible ansible-files]$ ssh 11.22.33.44
student<X>@11.22.33.44's password:
Last login: Wed May 15 14:03:45 2019 from 44.55.66.77
Managed by Ansible
[student<X>@node1 ~]$ rpm -qi httpd
Name        : httpd
Version     : 2.4.6
[...]
```

Efetue logout do `node1` com o comando `exit` para voltar ao host de controle e verifique o pacote instalado com o comando Ansible ad hoc\!

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m command -a 'rpm -qi httpd'
```

Execute o Playbook pela segunda vez e compare a saída: A saída mudou de "changed" para "ok" e a cor mudou de amarelo para verde. Além disso, o "PLAY RECAP" é diferente agora. Isso facilita a identificação do que o Ansible realmente fez.

## Passo 4 - Amplie seu playbook: Apache Start & Enable

A próxima parte do Playbook garante que o servidor Apache esteja startado e habilitado no `node1`.

No host de controle, como seu usuário student, edite o arquivo `~/ansible-files/apache.yml` para adicionar uma segunda task usando o módulo `service`. O Playbook agora deve ficar assim:

```yaml
---
- name: Apache server instalado
  hosts: node1
  become: yes
  tasks:
  - name: Ultima versao do apache server instalado
    yum:
      name: httpd
      state: latest
  - name: Apache started e enable
    service:
      name: httpd
      enabled: true
      state: started
```

Novamente: o que essas linhas fazem é fácil de entender:

  - uma segunda task é criada e nomeada

  - um módulo é especificado (`service`)

  - parâmetros para o módulo são fornecidos

Assim, com a segunda task, garantimos que o servidor Apache esteja realmente em execução na máquina de destino. Execute seu Playbook estendido:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook apache.yml
```

Observe a saída agora: algumas tasks são mostradas como "ok" em verde e uma é mostrada como "changed" em amarelo.

  - Use um comando Ansible ad hoc novamente para garantir que o Apache tenha sido ativado e iniciado, por exemplo com: `systemctl status httpd`.

  - Execute o Playbook uma segunda vez para se acostumar com a alteração na saída.

## Passo 5 - Ampliando seu Playbook: Criando um aquivo web.html

Verifique se as tasks foram executadas corretamente e o Apache está aceitando conexões: faça uma solicitação HTTP usando o módulo `uri` em um comando ad hoc a partir do nó de controle. Certifique-se de substituir **\<IP\>** pelo IP do nó do inventário.

> **ATENÇÃO**
>
> **Espere muitas linhas vermelhas e um status 403\!**

```bash
[student<X>@ansible ansible-files]$ ansible localhost -m uri -a "url=http://<IP>"
```

Há muitas linhas vermelhas e um erro: Contanto que não haja pelo menos um arquivo `web.html` a ser consumido pelo Apache, ele emitirá um status feio "HTTP Error 403: Forbidden" e o Ansible relatará um erro.

Então, por que não usar o Ansible para implantar um simples arquivo `web.html` ? Crie o arquivo `~/ansible-files/web.html` no nó de controle:

```html
<body>
<h1>O Apache esta funcionando bem</h1>
</body>
```

Você já usou o módulo `copy`  para gravar o texto fornecido na linha de comando em um arquivo. Agora você usará o módulo no seu Playbook para copiar um arquivo:

No nó de controle, com o seu usuário student, edite o arquivo `~/ansible-files/apache.yml` e adicione uma nova task utilizando o módulo`copy`. Agora deve ficar assim:

```yaml
---
- name: Apache server instalado
  hosts: node1
  become: yes
  tasks:
  - name: Ultima versao do apache server instalado
    yum:
      name: httpd
      state: latest
  - name: Apache started e enable
    service:
      name: httpd
      enabled: true
      state: started
  - name: Copiar web.html
    copy:
      src: ~/ansible-files/web.html
      dest: /var/www/html/index.html
```

Você está se acostumando com a sintaxe do Playbook, então o que acontece? A nova task usa o módulo `copy` e define as opções de origem e destino para a operação de cópia como parâmetros.

Execute seu Playbook ampliado:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook apache.yml
```

  - Observe bem a saída.

  - Execute o comando ad hoc usando o módulo "uri" mais acima novamente para testar o Apache: O comando agora deve retornar uma linha verde "status: 200" amigável, entre outras informações.

## Passo 6 - Pratique: Aplicar a vários hosts

Isso foi legal, mas o verdadeiro poder do Ansible é aplicar o mesmo conjunto de tasks de maneira confiável a muitos hosts.

  - Então, que tal mudar o apache.yml Playbook para executar no `node1` **e**` node2` **e** `node3`?

Como você deve se lembrar, o inventário lista todos os nós como membros do grupo `web`:

```ini
[web]
node1 ansible_host=11.22.33.44
node2 ansible_host=22.33.44.55
node3 ansible_host=33.44.55.66
```

> **Dica**
>
> Os endereços IP mostrados aqui são apenas exemplos, seus nós terão diferentes endereços IP.

Altere o Playbook para apontar para o grupo "web":

```yaml
---
- name: Apache server instalado
  hosts: web
  become: yes
  tasks:
  - name: Ultima versao do apache server instalado
    yum:
      name: httpd
      state: latest
  - name: Apache started e enable
    service:
      name: httpd
      enabled: true
      state: started
  - name: Copiar web.html
    copy:
      src: ~/ansible-files/web.html
      dest: /var/www/html/index.html
```

Agora, execute o playbook:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook apache.yml
```

Por fim, verifique se o Apache está em execução nos dois servidores. Primeiro identifique os endereços IP dos nós no seu inventário e depois use cada um no comando ad hoc com o módulo uri, como já fizemos com o `node1` acima. Todas saídas devem estar verde.

----

[Clique aqui para retornar ao Workshop Ansible for Red Hat Enterprise Linux](../README.pt-br.md#seção-1---exercícios-do-ansible-engine)
