#!/usr/bin/env python3
import os
import sys
import streamlit as st

# Configura o ambiente para evitar problemas com o ChromaDB
os.environ["CHROMA_DB_PATH"] = "/tmp/chroma"
os.environ["CHROMA_DB_IMPL"] = "duckdb+parquet"
os.environ["CHROMA_CACHE_DIR"] = "/tmp/chroma_cache"
os.environ["CHROMA_SERVER_HOST"] = "0.0.0.0"
os.environ["CHROMA_SERVER_HTTP_PORT"] = "8000"

# Configurações para evitar warnings desnecessários
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# Configurações adicionais do Streamlit
st.set_page_config(
    page_title="Gerador de Artigos de Saúde com IA",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tenta importar o app original
try:
    from app import main
    
    # Executa o app
    if __name__ == "__main__":
        main()
        
except Exception as e:
    st.error("Ocorreu um erro ao carregar o aplicativo.")
    st.exception(e)
