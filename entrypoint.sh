#!/bin/bash

# Configura o ambiente para o CrewAI
export CHROMA_DB_PATH="/tmp/chroma"
export CHROMA_DB_IMPL="duckdb+parquet"
export CHROMA_CACHE_DIR="/tmp/chroma_cache"
export CHROMA_SERVER_HOST="0.0.0.0"
export CHROMA_SERVER_HTTP_PORT="8000"

# Configurações adicionais para evitar warnings
export TOKENIZERS_PARALLELISM="false"
export TF_CPP_MIN_LOG_LEVEL="2"

# Cria diretórios necessários
mkdir -p /tmp/chroma
mkdir -p /tmp/chroma_cache

# Instala as dependências
pip install -r requirements.txt

# Executa o aplicativo Streamlit
exec streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0
