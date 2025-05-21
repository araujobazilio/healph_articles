#!/usr/bin/env python3
import os
import sys
import streamlit as st
from pathlib import Path

# Configurações para melhorar o desempenho
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTHONUNBUFFERED"] = "1"

# Configurações do Streamlit
st.set_page_config(
    page_title="Gerador de Artigos de Saúde com IA",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/araujobazilio/healph_issues',
        'Report a bug': 'https://github.com/araujobazilio/healph_issues',
        'About': "Gerador de artigos de saúde com IA usando CrewAI e Streamlit"
    }
)

# Adiciona um estilo personalizado
st.markdown("""
    <style>
        .main {
            max-width: 1000px;
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
            border-radius: 20px;
        }
        .stTextInput>div>div>input {
            border-radius: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Verifica se a chave da API está configurada
if "OPENAI_API_KEY" not in os.environ:
    st.warning("⚠️ A chave da API da OpenAI não foi configurada. Por favor, adicione a variável de ambiente OPENAI_API_KEY.")

# Tenta importar e executar o aplicativo principal
try:
    # Adiciona um atraso para garantir que as configurações de ambiente sejam aplicadas
    import time
    time.sleep(1)
    
    # Importa o app principal
    from app import main
    
    # Executa o app
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    st.error("❌ Erro ao importar o módulo principal do aplicativo.")
    st.error(f"Detalhes: {str(e)}")
    st.info("Verifique se todos os módulos necessários estão instalados corretamente.")
    
except Exception as e:
    st.error("❌ Ocorreu um erro inesperado ao executar o aplicativo.")
    st.exception(e)
