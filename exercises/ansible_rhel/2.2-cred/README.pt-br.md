# Exercício do Workshop: Inventários e Credenciais no Controlador de Automação Ansible

**Leia isto em outros idiomas**:
<br>![uk](../../../images/uk.png) [Inglês](README.md), ![japan](../../../images/japan.png) [Japonês](README.ja.md), ![france](../../../images/fr.png) [Francês](README.fr.md), ![Español](../../../images/col.png) [Espanhol](README.es.md).

## Objetivo
Este workshop é projetado para fornecer um entendimento prático de como gerenciar inventários e credenciais dentro do Controlador de Automação Ansible. Você aprenderá como navegar em um inventário pré-carregado, entender sua estrutura e explorar a configuração e uso de credenciais de máquina para acessar hosts gerenciados.

## Índice de Conteúdos
1. [Introdução aos Inventários](#1-introdução-aos-inventários)
2. [Explorando o 'Inventário do Workshop'](#2-explorando-o-inventário-do-workshop)
3. [Entendendo as Credenciais de Máquina](#3-entendendo-as-credenciais-de-máquina)
4. [Tipos Adicionais de Credenciais](#4-tipos-adicionais-de-credenciais)
5. [Conclusão](#5-conclusão)

### 1. Introdução aos Inventários
Inventários no Controlador de Automação Ansible são cruciais para definir e organizar os hosts nos quais seus playbooks serão executados. Eles podem ser estáticos, com uma lista fixa de hosts, ou dinâmicos, puxando listas de hosts de fontes externas.

### 2. Explorando o 'Inventário do Workshop'
O 'Inventário do Workshop' está pré-carregado no seu ambiente de laboratório, representando um inventário estático típico:

- **Acessando o Inventário:** Navegue até `Recursos → Inventários` na interface web e selecione 'Inventário do Workshop'.
- **Visualizando Hosts:** Clique no botão 'Hosts' para revelar as configurações de host pré-carregadas, semelhantes ao que você poderia encontrar em um arquivo de inventário Ansible tradicional, como:



```yaml
[web_servers]
web1 ansible_host=22.33.44.55
web2 ansible_host=33.44.55.66
...
```


### 3. Entendendo as Credenciais de Máquina
As credenciais de máquina são essenciais para estabelecer conexões SSH com seus hosts gerenciados:

- **Acessando Credenciais:** A partir do menu principal, escolha `Recursos → Credenciais` e selecione 'Credencial do Workshop'.
- **Detalhes da Credencial:** A 'Credencial do Workshop' está pré-definida com parâmetros como:
- **Tipo de Credencial:** Máquina, para acesso SSH.
- **Nome de Usuário:** Um usuário pré-definido, por exemplo, `ec2-user`.
- **Chave Privada SSH:** Criptografada, fornecendo acesso seguro aos seus hosts.

### 4. Tipos Adicionais de Credenciais
O Controlador de Automação Ansible suporta vários tipos de credenciais para diferentes cenários de automação:

- **Credenciais de Rede:** Para gerenciamento de dispositivos de rede.
- **Credenciais de Controle de Fonte:** Para acesso à gestão de controle de versão.
- **Credenciais dos Serviços Web da Amazon:** Para integração com a Amazon AWS.

Cada tipo é adaptado a requisitos específicos, melhorando a flexibilidade e segurança da sua automação.

### 5. Conclusão
Este workshop introduz os conceitos fundamentais de inventários e credenciais dentro do Controlador de Automação Ansible. Compreender esses componentes é crucial para gerenciar eficientemente suas tarefas de automação e garantir o acesso seguro à sua infraestrutura.

---
**Navegação**
<br>
[Exercício Anterior](../2.1-intro/README.pt-br.md) - [Próximo Exercício](../2.3-projects/README.pt-br.md)

[Clique aqui para retornar ao Workshop de Ansible para Red Hat Enterprise Linux](../README.md#section-2---ansible-tower-exercises)

