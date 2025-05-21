#!/bin/bash

# Configura a chave da API da OpenAI
export OPENAI_API_KEY="$OPENAI_API_KEY"

# Instala as dependências
pip install -r requirements.txt

# Inicia o aplicativo Streamlit
exec streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0
