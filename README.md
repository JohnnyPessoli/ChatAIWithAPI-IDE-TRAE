﻿# ChatAIWithAPI-IDE-TRAE

Um aplicativo web para análise de comportamento de clientes utilizando IA, com conexão flexível a diferentes bancos de dados.

## Introdução

Este projeto foi desenvolvido com o auxílio da IDE TRAE (Trae AI Responsive Environment), uma inovadora interface de desenvolvimento que integra capacidades avançadas de inteligência artificial ao processo de codificação. A TRAE IDE é uma ferramenta que potencializa a produtividade dos desenvolvedores através de:

- **Assistência em tempo real**: Oferece sugestões de código contextualmente relevantes enquanto você programa
- **Geração de código inteligente**: Capaz de criar componentes completos a partir de descrições em linguagem natural
- **Resolução de problemas**: Ajuda a identificar e corrigir bugs rapidamente
- **Documentação automática**: Gera documentação clara e abrangente para o código
- **Adaptabilidade**: Aprende com seu estilo de codificação para oferecer sugestões cada vez mais personalizadas

A utilização da TRAE IDE neste projeto permitiu um desenvolvimento mais ágil e eficiente, com foco na qualidade do código e na implementação de boas práticas. A ferramenta foi particularmente útil na criação da arquitetura do sistema, na implementação da conexão com diferentes bancos de dados e no desenvolvimento do motor de IA para análise de dados.

## Visão Geral

Este projeto implementa uma interface web que permite aos usuários fazer consultas em linguagem natural sobre o comportamento de seus clientes. A aplicação se conecta ao banco de dados do usuário, analisa os dados e fornece insights valiosos sobre padrões de compra, clientes mais valiosos e probabilidades de compras futuras.

## Tecnologias Utilizadas

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Banco de Dados**: Suporte para SQLite, PostgreSQL e MySQL
- **Análise de Dados**: Pandas, NumPy
- **ORM**: SQLAlchemy
```
## Estrutura do Projeto
TesteIA/
├── config/                  # Configurações do banco de dados
├── src/                     # Código-fonte
│   ├── templates/           # Templates HTML
│   │   ├── index.html       # Página principal
│   │   └── database_config.html  # Página de configuração do banco
│   ├── main.py              # Ponto de entrada da aplicação
│   ├── database.py          # Classe para gerenciamento do banco de dados
│   └── ai_engine.py         # Motor de IA para análise de dados
└── README.md                # Este arquivo
```

## Passo a Passo da Construção

### 1. Configuração do Ambiente

O projeto foi iniciado configurando um ambiente Flask para servir a aplicação web:

- Criação da estrutura básica de diretórios
- Instalação das dependências necessárias (Flask, Pandas, SQLAlchemy)
- Configuração do servidor Flask em `main.py`

### 2. Desenvolvimento do Backend

#### Conexão com Banco de Dados

Foi implementada uma classe `Database` em `database.py` que:

- Suporta múltiplos tipos de banco de dados (SQLite, PostgreSQL, MySQL)
- Fornece métodos para testar conexões
- Implementa funções para executar consultas SQL
- Oferece métodos para explorar a estrutura do banco de dados

#### Motor de IA

Foi desenvolvido um motor de IA em `ai_engine.py` que:

- Processa consultas em linguagem natural
- Analisa dados de clientes para identificar padrões
- Calcula probabilidades de compras futuras
- Identifica clientes mais valiosos
- Gera recomendações baseadas nos dados

### 3. Desenvolvimento do Frontend

#### Interface Principal

A interface principal (`index.html`) foi desenvolvida com:

- Campo para entrada de consultas em linguagem natural
- Sugestões de consultas pré-definidas
- Área para exibição de resultados
- Design responsivo usando Bootstrap 5

#### Configuração do Banco de Dados

Foi criada uma interface de configuração (`database_config.html`) que:

- Permite ao usuário selecionar o tipo de banco de dados
- Solicita as credenciais necessárias para conexão
- Testa a conexão antes de salvar
- Adapta os campos exibidos com base no tipo de banco selecionado

### 4. Integração e Fluxo de Dados

O fluxo de dados na aplicação segue estas etapas:

1. O usuário configura a conexão com seu banco de dados
2. A aplicação valida e estabelece a conexão
3. O usuário faz uma consulta em linguagem natural
4. O motor de IA processa a consulta
5. A aplicação executa as análises necessárias no banco de dados
6. Os resultados são formatados e apresentados ao usuário

## Como Executar

1. Clone este repositório
2. Instale as dependências:
``pip install flask pandas sqlalchemy``
3. Execute a aplicação:
``python src/main.py``
4. Acesse a aplicação em seu navegador: http://127.0.0.1:5000/

## Configuração do Banco de Dados

Na primeira execução, você será redirecionado para a página de configuração do banco de dados, onde deverá fornecer:

- **Para SQLite**: Caminho completo do arquivo do banco de dados
- **Para PostgreSQL/MySQL**: Host, porta, nome do banco, usuário e senha

## Exemplos de Consultas

- "Quais clientes têm maior probabilidade de fazer uma nova compra nos próximos 30 dias?"
- "Quais são os clientes mais valiosos com base no valor total gasto?"
- "Quais produtos estão mais propensos a serem comprados nos próximos meses?"
- "Quais canais de aquisição estão gerando os clientes mais fiéis e lucrativos?"

## Próximos Passos

- Implementação de autenticação de usuários
- Adição de visualizações gráficas para os resultados
- Suporte para mais tipos de banco de dados
- Melhorias no algoritmo de processamento de linguagem natural

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT.
