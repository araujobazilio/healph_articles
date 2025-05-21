"""Configurações do pytest para os testes do projeto."""
import sys
from pathlib import Path

import pytest

# Adiciona o diretório raiz ao PYTHONPATH para que os testes possam importar os módulos
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configuração para testes que precisam de variáveis de ambiente
@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    """Configura as variáveis de ambiente para os testes."""
    # Configurações padrão para testes
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("STREAMLIT_SERVER_PORT", "8501")

# Fixture para o cliente de teste do Streamlit
@pytest.fixture
def client():
    """Retorna um cliente de teste para a aplicação Streamlit."""
    # Importa aqui para evitar problemas com o pytest
    from streamlit.testing.v1 import AppTest
    
    app = AppTest.from_file("streamlit_app.py")
    return app
