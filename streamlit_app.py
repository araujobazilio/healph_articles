#!/usr/bin/env python3
import os
import sys
import streamlit as st

# Configura o ambiente para evitar o uso do ChromaDB
os.environ["CHROMA_DB_PATH"] = "/tmp/chroma"
os.environ["CHROMA_DB_IMPL"] = "duckdb+parquet"

# Importa o app original
from app import *

if __name__ == "__main__":
    # Configurações adicionais do Streamlit
    st.set_page_config(
        page_title="Gerador de Artigos de Saúde com IA",
        page_icon="📝",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Executa o app
    main()
