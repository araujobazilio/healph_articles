from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from crewai.utilities.embedding_configurator import EmbeddingConfigurator

# Configuração personalizada para embeddings
def get_embedding_config():
    # Usando embeddings do HuggingFace que funcionam sem GPU
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        model_kwargs={"device": "cpu"}
    )
    
    # Configura o FAISS como backend para armazenamento de vetores
    return {
        "embeddings": embeddings,
        "vectorstore": FAISS
    }

# Sobrescreve a configuração padrão do CrewAI
EmbeddingConfigurator.get_embedding_config = staticmethod(get_embedding_config)
