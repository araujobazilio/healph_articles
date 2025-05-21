# Guia de Contribuição

Obrigado por considerar contribuir para o projeto Healph Articles! Aqui estão algumas diretrizes para ajudar você a começar.

## Como Contribuir

1. **Reportando Problemas**
   - Verifique se o problema já não foi reportado
   - Forneça um título claro e descritivo
   - Inclua etapas para reproduzir o problema
   - Descreva o comportamento esperado e o comportamento real
   - Inclua capturas de tela, se aplicável

2. **Enviando Pull Requests**
   - Crie um branch para sua feature/correção: `git checkout -b feature/nova-feature`
   - Faça commit das suas alterações: `git commit -m 'Adiciona nova feature'`
   - Envie para o branch: `git push origin feature/nova-feature`
   - Abra um Pull Request

## Padrões de Código

- Siga o estilo de código PEP 8
- Escreva testes para novas funcionalidades
- Documente novas funcionalidades
- Mantenha o código limpo e organizado

## Ambiente de Desenvolvimento

1. Clone o repositório:
   ```bash
   git clone https://github.com/araujobazilio/healph_articles.git
   cd healph_articles
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # .\venv\Scripts\activate  # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. Crie um arquivo `.env` baseado no `.env.example`

5. Execute os testes:
   ```bash
   python -m pytest
   ```

## Código de Conduta

Este projeto segue o [Código de Conduta do Contribuidor](CODE_OF_CONDUCT.md). Ao participar, espera-se que você siga este código.

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a Licença MIT.
