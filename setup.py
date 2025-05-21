from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Dependências principais
install_requires = [
    "streamlit>=1.31.0",
    "python-dotenv>=1.0.0",
    "crewai>=0.11.1",
    "langchain-community>=0.0.14",
    "langchain-openai>=0.0.5",
    "markdown>=3.4.0",
    "markdown-it-py>=2.2.0",
    "mdurl>=0.1.0",
    "tiktoken>=0.5.0",
    "openai>=1.3.0",
    "numpy>=1.24.0",
    "pydantic>=2.0.0",
    "xhtml2pdf>=0.2.12",
    "reportlab>=4.0.0",
    "requests>=2.31.0",
    "duckduckgo-search>=3.8.6"
]

# Configuração para evitar instalação de dependências opcionais
def exclude_deps():
    import os
    import sys
    
    # Código para evitar a instalação do ChromaDB
    os.environ["SKIP_CHROMADB_INSTALL"] = "1"
    
    # Se estiver no Streamlit Cloud, evite dependências pesadas
    if os.environ.get("STREAMLIT_SERVER_RUNNING") == "true":
        return ["chromadb", "faiss-cpu", "sentence-transformers"]
    return []

setup(
    name="healph_articles",
    version="0.1.0",
    author="Rafael Araújo",
    author_email="seu.email@exemplo.com",
    description="Gerador de Artigos de Saúde com IA usando CrewAI e Streamlit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/araujobazilio/healph_articles",
    packages=find_packages(),
    install_requires=install_requires,
    python_requires=">=3.10",
    exclude_deps=exclude_deps(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
    keywords="ai health medical article generation crewai streamlit",
    project_urls={
        "Bug Reports": "https://github.com/araujobazilio/healph_articles/issues",
        "Source": "https://github.com/araujobazilio/healph_articles",
    },
    include_package_data=True
)
