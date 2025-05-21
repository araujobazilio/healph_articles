FROM python:3.10-slim

WORKDIR /app

# Instala as dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos necessários
COPY requirements.txt .
COPY setup.py .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .

# Copia o restante dos arquivos
COPY . .

# Torna o script de entrada executável
RUN chmod +x /app/entrypoint.sh

# Expõe a porta 8501 (porta padrão do Streamlit)
EXPOSE 8501

# Define o comando de entrada
ENTRYPOINT ["/app/entrypoint.sh"]
