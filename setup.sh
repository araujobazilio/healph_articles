#!/bin/bash

# Instala as dependências do sistema necessárias
apt-get update && apt-get install -y gcc python3-dev

# Instala as dependências do Python
pip install -r requirements.txt

# Cria um link simbólico para evitar problemas com o ChromaDB
mkdir -p /app/.chroma
ln -sf /tmp /app/.chroma
