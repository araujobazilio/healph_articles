# Sistema de Geração de Artigos de Saúde com CrewAI e Streamlit

Este projeto utiliza o framework CrewAI para criar um sistema de agentes de IA capazes de pesquisar e escrever artigos sobre temas da área da saúde, com uma interface de usuário simples construída com Streamlit.

## 1. Visão Geral

O sistema é composto por dois agentes principais:

* **Agente Pesquisador (Health Research Specialist):** Responsável por conduzir pesquisas aprofundadas na internet sobre o tema de saúde fornecido pelo usuário. Utiliza a ferramenta DuckDuckGoSearchRun para buscar informações em fontes confiáveis.
* **Agente Escritor (Medical Content Creator):** Responsável por analisar os dados da pesquisa e redigir um artigo informativo, bem estruturado e acessível para o público em geral.

As tarefas são executadas sequencialmente: primeiro a pesquisa, depois a escrita do artigo com base nos resultados da pesquisa.

## 2. Pré-requisitos

- Docker e Docker Compose instalados
- Chave de API da OpenAI
- Conta no Streamlit Cloud (para deploy)

## 3. Configuração do Ambiente

### 3.1 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```
OPENAI_API_KEY=sua_chave_aqui
```

### 3.2 Instalação Local com Docker

1. Construa a imagem Docker:
   ```bash
   docker build -t healph-articles .
   ```

2. Execute o contêiner:
   ```bash
   docker run -p 8501:8501 --env-file .env healph-articles
   ```

3. Acesse o aplicativo em: http://localhost:8501

## 4. Deploy no Streamlit Cloud

1. Faça push do código para um repositório no GitHub
2. Acesse o [Streamlit Cloud](https://share.streamlit.io/)
3. Clique em "New app"
4. Selecione o repositório e o branch
5. Defina o "Main file path" como `streamlit_app.py`
6. Adicione a variável de ambiente `OPENAI_API_KEY`
7. Clique em "Deploy!"

## 5. Estrutura do Projeto

```
healph_articles/
├── .streamlit/               # Configurações do Streamlit
│   └── config.toml
├── app.py                    # Código principal da aplicação
├── crewai_config.py          # Configurações personalizadas do CrewAI
├── Dockerfile                # Configuração do Docker
├── entrypoint.sh             # Script de inicialização
├── requirements.txt          # Dependências do Python
└── README.md                 # Documentação
```

## 6. Solução de Problemas

### Erro de SQLite

Se encontrar erros relacionados ao SQLite, tente:

1. Reconstruir a imagem Docker:
   ```bash
   docker-compose build --no-cache
   ```

2. Limpar contêineres antigos:
   ```bash
   docker-compose down -v
   ```

### Erros de Dependências

Se encontrar erros de dependências, tente:

```bash
docker-compose build --no-cache
```

## 7. Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 2. Estrutura de Arquivos

```
/crewai_article_generator/
|-- venv/                    # Ambiente virtual Python
|-- app.py                   # Código principal da aplicação Streamlit e CrewAI
|-- requirements.txt         # Lista de dependências Python
|-- .env.example             # Exemplo de arquivo de variáveis de ambiente
|-- .env                     # Arquivo de variáveis de ambiente (NÃO DEVE SER VERSIONADO)
|-- validation_tests.md      # Documento com casos de teste (para referência)
`-- README.md                # Este arquivo de documentação
```

## 3. Configuração do Ambiente

### 3.1. Requisitos

*   Python 3.10 ou superior
*   Ollama instalado e em execução (se for usar um LLM local como o Llama3). Certifique-se de ter o modelo desejado baixado (ex: `ollama pull llama3`).
*   (Opcional) Chave de API da OpenAI se preferir usar os modelos da OpenAI em vez de um LLM local.

### 3.2. Passos de Configuração

1.  **Clone o repositório (ou extraia os arquivos):**
    Se você recebeu os arquivos em um ZIP, extraia-os para um diretório de sua escolha.

2.  **Crie e ative um ambiente virtual Python:**
    É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto.

    ```bash
    cd caminho/para/crewai_article_generator
    python3 -m venv venv
    source venv/bin/activate  # No Linux/macOS
    # venv\Scripts\activate    # No Windows
    ```

3.  **Instale as dependências:**

    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```
    O `requirements.txt` inclui `crewai`, `streamlit`, `python-dotenv`, `langchain-community` (para ferramentas e LLMs locais como Ollama), e `duckduckgo-search`.

4.  **Configure as Variáveis de Ambiente:**
    Copie o arquivo `.env.example` para `.env`:

    ```bash
    cp .env.example .env
    ```
    Edite o arquivo `.env`:

    *   **Para usar OpenAI (opcional):**
        Descomente e preencha a linha `OPENAI_API_KEY` com sua chave da API OpenAI.
        ```dotenv
        OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        ```
        Se usar OpenAI, você precisará ajustar o código em `app.py` para usar o LLM da OpenAI em vez do Ollama.

    *   **Para usar Ollama (configuração padrão no `app.py` fornecido):**
        Certifique-se de que o Ollama esteja rodando localmente. O `app.py` está configurado para usar o modelo `llama3` via Ollama. Se o seu Ollama estiver em uma URL diferente da padrão (`http://localhost:11434`), você pode (opcionalmente) configurar `OLLAMA_BASE_URL` no `.env` e adaptar o `app.py` para usá-lo, embora o `langchain_community.llms.Ollama` geralmente detecte o servidor local automaticamente.

## 4. Executando a Aplicação

Após configurar o ambiente e as variáveis (se necessário), execute a aplicação Streamlit:

```bash
streamlit run app.py
```

Isso deve abrir a interface do sistema no seu navegador web padrão.

## 5. Como Usar

1.  Abra a aplicação no seu navegador (geralmente `http://localhost:8501`).
2.  Digite o tema de saúde sobre o qual você deseja gerar um artigo no campo de texto "Enter the health topic for the article:".
3.  Clique no botão "Generate Article".
4.  Aguarde enquanto os agentes de IA pesquisam e escrevem o artigo. Isso pode levar alguns minutos, dependendo da complexidade do tema e do desempenho do LLM.
5.  O artigo gerado será exibido na página.

## 6. Considerações

*   **Qualidade do LLM:** A qualidade do artigo gerado depende significativamente do modelo de linguagem (LLM) utilizado. Modelos mais avançados (como GPT-4 via API da OpenAI) tendem a produzir resultados melhores do que modelos menores rodando localmente, mas o Llama3 via Ollama é uma boa alternativa para uso local.
*   **Fontes da Pesquisa:** O agente pesquisador usa o DuckDuckGo. A confiabilidade das fontes pode variar. Para aplicações críticas, seria necessário um controle mais rigoroso das fontes ou o uso de ferramentas de busca especializadas em literatura médica.
*   **Tempo de Geração:** A geração de artigos pode ser demorada, especialmente com LLMs locais.
*   **Simplificação no Fluxo de Dados:** No `app.py` fornecido, a passagem do resultado da pesquisa para a tarefa de escrita foi simplificada. Em uma aplicação mais robusta, você garantiria que o `research_data` fosse explicitamente passado e utilizado pela tarefa de escrita. O exemplo atual passa o `topic` novamente para a tarefa de escrita, assumindo que o contexto da crew permite o acesso implícito aos resultados da tarefa anterior. Para maior clareza e controle, o resultado da `research_task_instance` deveria ser o input da `writing_task_instance`.

Este projeto serve como uma base para a criação de sistemas mais complexos de geração de conteúdo utilizando CrewAI.

