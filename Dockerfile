FROM python:3.10-slim

WORKDIR /app

# Instala as dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    wget \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instala uma versão mais recente do SQLite
RUN wget https://www.sqlite.org/2024/sqlite-autoconf-3450100.tar.gz \
    && tar -xzf sqlite-autoconf-3450100.tar.gz \
    && cd sqlite-autoconf-3450100 \
    && ./configure --prefix=/usr/local \
    && make \
    && make install \
    && cd .. \
    && rm -rf sqlite-autoconf-3450100 sqlite-autoconf-3450100.tar.gz

# Atualiza o Python para usar a nova versão do SQLite
ENV LD_LIBRARY_PATH="/usr/local/lib:${LD_LIBRARY_PATH}"
ENV PATH="/usr/local/bin:${PATH}"

# Copia os arquivos de requisitos primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos
COPY . .

# Cria diretório para o ChromaDB
RUN mkdir -p /tmp/chroma

# Comando para rodar o Streamlit
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
