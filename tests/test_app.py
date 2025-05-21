"""Testes para o módulo principal da aplicação."""
import pytest
from unittest.mock import patch, MagicMock

# Teste da função principal
def test_main_flow(client):
    """Testa o fluxo principal da aplicação."""
    # Configura o mock para o CrewAI
    with patch('app.Crew') as mock_crew:
        # Configura o mock para o resultado da execução do Crew
        mock_crew_instance = MagicMock()
        mock_crew.return_value = mock_crew_instance
        mock_crew_instance.kickoff.return_value = "Artigo de teste gerado com sucesso!"
        
        # Executa o teste
        client.run()
        
        # Verifica se o título está correto
        assert "Healph Articles" in client.get_elements("h1")[0].value
        
        # Verifica se o botão está presente
        assert len(client.button) == 1
        
        # Simula o clique no botão
        client.button[0].click().run()
        
        # Verifica se o Crew foi chamado corretamente
        mock_crew.assert_called_once()
        mock_crew_instance.kickoff.assert_called_once()

# Teste de tratamento de erros
def test_error_handling(client):
    """Testa o tratamento de erros na aplicação."""
    with patch('app.Crew') as mock_crew:
        # Configura o mock para levantar uma exceção
        mock_crew_instance = MagicMock()
        mock_crew.return_value = mock_crew_instance
        mock_crew_instance.kickoff.side_effect = Exception("Erro ao gerar artigo")
        
        # Executa o teste
        client.run()
        client.button[0].click().run()
        
        # Verifica se a mensagem de erro foi exibida
        assert "Erro ao gerar o artigo" in client.get_elements("div")[-1].value
