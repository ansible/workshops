# Exercício 2.2 - Inventários, Credenciais e comandos ad hoc

**Read this in other languages**: ![uk](../../../../images/uk.png) [English](README.md),  ![japan](../../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md).

* [Criando um inventário](#criando-um-inventário)
* [Credenciais de máquina](#credenciais-de-máquina)
* [Configurar credenciais da máquina](#configurar-credenciais-da-máquina)
* [Executar comandos ad hoc](#executar-comandos-ad-hoc)
* [Laboratório de desafios: Comandos Ad Hoc](#laboratório-de-desafios-comandos-ad-hoc)

## Criando um inventário

Vamos começar: a primeira coisa que precisamos é de um inventário de seus hosts gerenciados. É o equivalente a um arquivo de inventário no Ansible Engine. Há muito mais a aprender, como inventários dinâmicos, mas vamos começar com o básico.

  - Você já deve ter a interface  web aberta, caso contrário: aponte o navegador para o URL fornecido, semelhante a **https://student\<X\>.workshopname.rhdemo.io** (substitua "\<X\>" com o seu número de usuário e" workshopname "com o nome do seu workshop atual) e faça o login como `admin`. A senha será fornecida pelo instrutor.

Criando o inventário:

  - No menu da interface web no lado esquerdo, vá para **RESOURCES** → **Inventories**, clique no botão ![plus](images/green_plus.png) no lado direito e escolha **Inventory**.

  - **NAME:** Inventario Workshop

  - **ORGANIZATION:** Default

  - Click em **SAVE**

Agora haverá dois inventários, o **Inventario Demo** e o **Inventario Workshop**. No **Inventario Workshop**, clique no botão **Hosts**, ele ficará vazio, pois não adicionamos nenhum host lá.

Então, vamos adicionar alguns hosts. Primeiro, precisamos ter a lista de todos os hosts acessíveis a você neste laboratório. Estes podem ser encontrados em um inventário no nó de controle ansible no qual o Tower está instalado.

Faça login no host de controle do Tower via SSH:

> **ATENÇÃO**
>
> Substitua **workshopname** pelo nome do workshop fornecido a você e **X** no student **X** pelo número do usuário fornecido a você.

```bash
ssh student<X>@student<X>.workshopname.rhdemo.io
```

Você pode encontrar as informações de inventário em `~/lab_inventory/hosts`.

```bash
$ cat ~/lab_inventory/hosts
[web]
node1 ansible_host=22.33.44.55
node2 ansible_host=33.44.55.66
node3 ansible_host=44.55.66.77

[control]
ansible ansible_host=11.22.33.44
```
> **ATENÇÃO**
>
> No seu inventário, os endereços IP serão diferentes.

Observe os nomes dos nós e os endereços IP, vamos usá-los para preencher o inventário no Tower agora:

  - Na exibição de inventário do Tower, clique no seu **Inventário Workshop**

  - Clique no botão **HOSTS**

  - À direita, clique no botão ![plus](images/green_plus.png)

  - **HOST NAME:** `node1`

  - **Variables:** Sob os três traços `---`, digite `ansible_host: 22.33.44.55` em uma nova linha. Certifique-se de inserir o seu endereço IP específico para o seu `node1` no inventário pesquisado acima e observe que a definição da variável possui dois pontos **:** e um espaço entre os valores, não um sinal de igual **=** como no arquivo de inventário.

  - Click em **SAVE**

  - Volte para **HOSTS** e repita o processo para adicionar `node2` como um segundo host e `node3` como um terceiro. Certifique-se de que para cada nó insira os endereços IP corretos.

Agora você criou um inventário com três hosts gerenciados.

## Credenciais de máquina

Um dos grandes recursos do Ansible Tower é tornar as credenciais utilizáveis para os usuários sem torná-las visíveis. Para permitir que o Tower execute tasks em hosts remotos, você deve configurar credenciais de conexão.

> **Nota**
>
> Este é um dos recursos mais importantes do Tower: **Separação de credenciais**\! As credenciais são definidas separadamente e não com os hosts ou as configurações de inventário.

Como essa é uma parte importante da sua configuração do Tower, por que não verificar se está funcionando e verificar se as credenciais estão funcionando corretamente?

Para acessar o host do Tower via SSH, faça o seguinte:

  - Entre no seu host de controle do Tower via SSH: `ssh student<X>@student<X>.workshopname.rhdemo.io`
    Substitua **workshopname** pelo nome do workshop fornecido a você e **X** no student**X** pelo número do usuário fornecido a você.

  - Dê SSH no `node1` ou em um dos outros nós e execute o `sudo -i`. Para a conexão SSH, é necessário fornecer uma senha, `sudo -i` funciona sem senha.

```bash
[student<X>@ansible ~]$ ssh student<X>@22.33.44.55
student<X>@22.33.44.55's password:
Last login: Thu Jul  4 14:47:04 2019 from 11.22.33.44
[student<X>@node1 ~]$ sudo -i
[root@node1 ~]#
```

O que isto significa?

  - O usuário do Tower **ansible** pode conectar-se aos hosts gerenciados com senha baseada em SSH

  - O usuário **ansible** pode executar comandos nos hosts gerenciados como **root** com `sudo`

## Configurar credenciais da máquina

Agora vamos configurar as credenciais para acessar nossos hosts gerenciados do Tower. No menu **RESOURCES**, escolha **CREDENTIALS**. Agora:

Clique no botão ![plus](images/green_plus.png) para adicionar novas credenciais

  - **NAME:** Credenciais Workshop

  - **ORGANIZATION:** Default

  - **CREDENTIAL TYPE:** Clique na lupa, escolha **Machine** e clique em ![plus](images/select.png)

  - **CREDENTIAL TYPE:** Machine

  - **USERNAME:** student\<X\> - substitua **\<X\>** pelo número real do usuário!

  - **PASSWORD:** Digite a senha que é fornecida pelo instrutor.

  - **PRIVILEGE ESCALATION METHOD:** sudo

  - Click em **SAVE**

  - Volte para **RESOURCES** → **CREDENTIALS** → **Credenciais Workshop** e observe que a senha não está visível.

> **Dica**
>
> Sempre que você avistar um ícone de lupa ao lado de um campo de entrada, clique nele para abrir uma lista para sua escolha.

Agora você configurou credenciais para usar posteriormente em seus hosts de inventário.

## Executar comandos ad hoc

Provavelmente você já fez com o Ansible Engine, agora também pode executar comandos ad hoc no Tower.

  - Vá para **RESOURCES → Inventories → Inventario Workshop**

  - Clique no botão **HOSTS** para mudar para a exibição de hosts e selecione os três hosts marcando as caixas à esquerda das entradas do host.

  - Clique em **RUN COMMANDS**. Na próxima tela, você deve especificar o comando ad hoc:

      - Em **MODULE**, escolha **ping**

      - Para **MACHINE CREDENTIAL**, clique no ícone da lupa e selecione **Credenciais Workshop**.

      - Clique em **LAUNCH** e observe a saída.

O módulo simples **ping** não precisa de opções. Para outros módulos, você precisa fornecer o comando para executar como argumento. Experimente o módulo **command** para encontrar o ID do usuário em execução usando um comando ad hoc.

- **MODULE:** command

- **ARGUMENTS:** id

> **Dica**
>
> Após escolher o módulo a ser executado, o Tower fornecerá um link para a página de documentos do módulo ao clicar no ponto de interrogação ao lado de "Arguments". Isso é útil, experimente.

Que tal tentar obter algumas informações secretas do sistema? Tente imprimir */etc/shadow*.  

- **MODULE:** command

- **ARGUMENTS:** cat /etc/shadow

> **ATENÇÃO**
>
> **Espere um erro\!**

Opa, o último não correu bem, todo vermelho.

Execute novamente o último comando ad hoc, mas desta vez marque a caixa **ENABLE PRIVILEGE ESCALATION**.

Como você pode ver, desta vez funcionou. Para tasks que precisam ser executadas como root, você precisa escalar os privilégios. É o mesmo que o **become: yes** você provavelmente já usou com frequência em seus Playbooks com Ansible Engine.

## Laboratório de desafios: Comandos Ad Hoc

Agora um pequeno desafio: execute um ad hoc para garantir que o pacote "tmux" esteja instalado em todos os hosts. Se não tiver certeza, consulte a documentação através da interface do web, como mostrado acima, ou executando `[ansible@tower~] $ ansible-doc yum` no host de controle do Tower.

> **ATENÇÃO**
>
> **Solução abaixo\!**

  - **MODULE:** yum

  - **ARGUMENTS:** name=tmux

  - Marque **ENABLE PRIVILEGE ESCALATION**

> **Dica**
>
> A saída amarela do comando indica que o Ansible realmente fez alguma coisa (aqui é necessário instalar o pacote). Se você executar o comando ad hoc pela segunda vez, a saída será verde e informará que o pacote já foi instalado. O amarelo no Ansible não significa "cuidado"…​ ;-).

----

[Clique aqui para retornar ao Workshop Ansible for Red Hat Enterprise Linux](../../README.pt-br.md#seção-2---exercícios-do-ansible-tower)
