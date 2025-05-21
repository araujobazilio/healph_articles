#!/usr/bin/env python3
import streamlit as st
import os
from dotenv import load_dotenv # Importa load_dotenv

# Importa a configuração personalizada antes de importar o CrewAI
import crewai_config  # noqa: F401

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI # Importa ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from crewai.tools import BaseTool # Adicionado import
from pydantic import Field # Adicionado import
import io # Adicionado para manipulação de bytes
from xhtml2pdf import pisa # Adicionado para PDF
from markdown import markdown # Adicionado para converter Markdown para HTML

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Define a classe da ferramenta de busca para compatibilidade com CrewAI
class DuckDuckGoSearchTool(BaseTool):
    name: str = "Pesquisa na Web (DuckDuckGo)"
    description: str = "Útil para realizar pesquisas na web e obter informações atuais sobre diversos tópicos. Use para encontrar literatura, notícias e dados relevantes."
    search_tool: DuckDuckGoSearchRun = Field(default_factory=DuckDuckGoSearchRun)

    def _run(self, query: str) -> str:
        """Executa a pesquisa na web e retorna os resultados."""
        try:
            return self.search_tool.run(query)
        except Exception as e:
            return f"Erro ao realizar a pesquisa: {str(e)}"


# Inicializa o LLM da OpenAI
openai_llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7, api_key=os.getenv("OPENAI_API_KEY"))

# Define os Agentes
class HealthArticleAgents:
    def research_agent(self):
        return Agent(
            role='Pesquisador Especialista em Saúde',
            goal='Conduzir pesquisa aprofundada sobre tópicos de saúde especificados utilizando fontes confiáveis da internet.',
            backstory='Um especialista em IA para navegar e extrair informações relevantes de periódicos médicos, bancos de dados de saúde e sites de saúde conceituados. Habilidoso em identificar fontes críveis e sintetizar informações diversas em uma visão geral coerente.',
            tools=[DuckDuckGoSearchTool()],
            llm=openai_llm, # Usa openai_llm
            verbose=True,
            allow_delegation=False
        )

    def writing_agent(self):
        return Agent(
            role='Redator Científico Especializado em Saúde para Profissionais',
            goal='Elaborar artigos técnicos e formais, ricos em detalhes (incluindo dosagens e informações medicamentosas quando aplicável e disponível na pesquisa) e com uma seção de referências bibliográficas, destinados a médicos e enfermeiros.',
            backstory='Um especialista em IA com vasta experiência na redação de literatura médica, publicações científicas e diretrizes clínicas. Seu foco é a precisão, clareza e conformidade com padrões acadêmicos, incluindo a citação adequada de fontes.',
            tools=[],
            llm=openai_llm, # Usa openai_llm
            verbose=True,
            allow_delegation=False
        )

    def review_agent(self):
        return Agent(
            role='Revisor Médico Especialista em Medicina de Emergência',
            goal='Garantir a precisão técnica, relevância clínica e adequação do conteúdo de artigos de saúde para profissionais de medicina de emergência, com foco crítico na pertinência da farmacologia citada.',
            backstory=('Um médico emergencista experiente e pesquisador, com um olhar crítico para a literatura médica. '
                       'Sua especialidade é validar a aplicabilidade prática das informações, assegurando que intervenções e '
                       'especialmente tratamentos farmacológicos sejam contextualmente apropriados para o cenário de emergência discutido.'),
            tools=[], # Geralmente não necessita de ferramentas externas para revisão de texto
            llm=openai_llm,
            verbose=True,
            allow_delegation=False
        )

# Define as Tarefas
class HealthArticleTasks:
    def research_task(self, agent, topic):
        return Task(
            description=f'''Conduza uma pesquisa aprofundada e técnica sobre "{topic}", direcionada a profissionais de saúde.
        O foco é obter informações detalhadas e baseadas em evidências de fontes primárias e secundárias confiáveis (ex: estudos clínicos, revisões sistemáticas, diretrizes de sociedades médicas, bancos de dados de medicamentos conceituados).
        A pesquisa deve buscar ativamente por:
        1.  Dados sobre medicamentos relevantes ao tópico: nomes (genérico/comercial), dosagens usuais para diferentes cenários clínicos, vias de administração, mecanismos de ação, indicações aprovadas, contraindicações importantes, efeitos adversos significativos e interações medicamentosas clinicamente relevantes.
        2.  Informações epidemiológicas, fisiopatológicas, diagnósticas e terapêuticas atuais e relevantes.
        3.  Detalhes das fontes para a seção de referências: autores, ano de publicação, título do artigo/estudo e nome do periódico ou site da organização/banco de dados.
        Priorize fontes como PubMed, Cochrane Library, UpToDate (se acessível conceitualmente), FDA, EMA, e sites de sociedades médicas renomadas.''',
            expected_output='''Um relatório de pesquisa detalhado e estruturado contendo:
        1.  Síntese das informações chave sobre o tópico.
        2.  Dados específicos sobre medicamentos (nomes, dosagens, indicações, etc.), se aplicável ao tema.
        3.  Uma lista clara das fontes consultadas, incluindo autor(es), ano, título e nome do periódico/site, para ser usada na seção de referências bibliográficas do artigo final.
        4.  Links diretos para as fontes mais relevantes, se possível.''',
            agent=agent
        )

    def writing_task(self, agent, research_data):
        return Task(
            description=f'''Com base nos resultados da pesquisa detalhada sobre "{research_data}", elabore um artigo técnico e formal destinado a profissionais de saúde (médicos, enfermeiros).
        O artigo DEVE OBRIGATORIAMENTE:
        1.  Ser escrito em linguagem formal e precisa, utilizando terminologia médica adequada.
        2.  Apresentar as informações de forma clara e bem estruturada.
        3.  Se os dados da pesquisa permitirem, incluir detalhes específicos como:
            - Nomes de medicamentos (genéricos e, se relevante, comerciais).
            - Dosagens usuais, vias de administração.
            - Mecanismos de ação, indicações principais, contraindicações importantes.
            - Efeitos adversos comuns e/ou graves, e interações medicamentosas clinicamente relevantes.
        4.  Interpretar e discutir os achados da pesquisa.
        5.  Finalizar com uma seção EXCLUSIVAMENTE intitulada "Referências Bibliográficas". Nesta seção, liste as principais fontes de informação (artigos, estudos, diretrizes) que foram a base da pesquisa. Formato sugerido: Autor(es) (Ano). Título do estudo/artigo. Nome do Periódico/Site. O Pesquisador Especialista em Saúde foi instruído a fornecer esses detalhes.
        O objetivo é criar um material de alto valor para atualização e prática clínica. Evite simplificações excessivas.''',
            expected_output='Um artigo técnico detalhado e formal sobre o tema, estruturado para profissionais de saúde, incluindo informações sobre medicamentos (dosagens, etc., se aplicável e encontrado na pesquisa) e finalizado com uma seção de "Referências Bibliográficas" listando as fontes primárias da pesquisa.',
            agent=agent
        )

    def review_task(self, agent, article_draft, topic_context):
        return Task(
            description=f'''Revise criticamente o rascunho do artigo fornecido abaixo. 
O tema central do artigo é: "{topic_context}".

Rascunho do Artigo:
---
{article_draft}
---
Seu foco principal é a relevância e precisão no contexto da medicina de emergência para o tema "{topic_context}".
Especificamente:
1.  AVALIAÇÃO FARMACOLÓGICA CRÍTICA: Os medicamentos mencionados e suas dosagens são ESTRITAMENTE relevantes e apropriados para o tema principal do artigo ("{topic_context}") no cenário de atendimento pré-hospitalar ou de emergência?
    -   Se um medicamento não é diretamente aplicável ou é tangencial, REMOVA-O ou justifique sucintamente sua menção se for para um diagnóstico diferencial crucial.
    -   Se o tema central ("{topic_context}") NÃO envolve primariamente farmacologia (ex: manejo de via aérea em trauma, imobilização), evite introduzir discussões farmacológicas desnecessárias. A ausência de menção a medicamentos pode ser a conduta correta.
2.  PRECISÃO TÉCNICA: As informações médicas, incluindo fisiopatologia, diagnóstico e manejo, estão corretas e atualizadas para o tema "{topic_context}"?
3.  PÚBLICO-ALVO: O artigo está adequado em tom, profundidade e linguagem para médicos e enfermeiros de emergência, considerando o tema "{topic_context}"?
4.  CLAREZA E COESÃO: O artigo é bem estruturado, claro e coeso?
5.  REFERÊNCIAS: A seção "Referências Bibliográficas" está presente e parece adequada (sem necessidade de validar cada fonte, mas sim a presença da seção)?
Realize as correções e melhorias necessárias diretamente no texto para produzir a versão final do artigo.''',
            expected_output='O artigo final revisado, otimizado para precisão, relevância em medicina de emergência e adequação farmacológica para o tema "{topic_context}". Se nenhuma alteração significativa for necessária, retorne o rascunho original com uma breve nota de aprovação.',
            agent=agent,
            context = [] # Contexto será preenchido com a saída da tarefa de escrita
        )

# Função para converter Markdown para PDF
def convert_markdown_to_pdf(markdown_content):
    # Converte markdown para HTML
    html_content = markdown(markdown_content)
    
    # Adiciona um estilo básico para melhor formatação do PDF
    html_with_style = f"""
    <html>
    <head>
        <style>
            body {{ font-family: sans-serif; line-height: 1.6; }}
            h1, h2, h3, h4, h5, h6 {{ font-weight: bold; margin-top: 1.5em; margin-bottom: 0.5em; }}
            h1 {{ font-size: 1.8em; }}
            h2 {{ font-size: 1.5em; }}
            h3 {{ font-size: 1.3em; }}
            p {{ margin-bottom: 1em; }}
            ul, ol {{ margin-bottom: 1em; padding-left: 1.5em; }}
            li {{ margin-bottom: 0.3em; }}
            code {{ font-family: monospace; background-color: #f0f0f0; padding: 2px 4px; border-radius: 3px; }}
            pre {{ background-color: #f0f0f0; padding: 1em; border-radius: 3px; overflow-x: auto; }}
            blockquote {{ border-left: 3px solid #ccc; padding-left: 1em; margin-left: 0; font-style: italic; color: #555; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 1em; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    result = io.BytesIO() # Cria um buffer de bytes para o PDF
    
    # Cria o PDF
    pdf = pisa.CreatePDF(
            io.StringIO(html_with_style),  # Usa o HTML com estilo
            dest=result
    )
    
    if not pdf.err:
        return result.getvalue() # Retorna os bytes do PDF
    else:
        st.error(f"Erro ao gerar PDF: {pdf.err}")
        return None

def main():
    # Interface Streamlit
    st.title("Gerador de Artigos de Saúde com IA")

    topic = st.text_input("Digite o tema de saúde para o artigo:")

    if st.button("Gerar Artigo"):
        if topic:
            with st.spinner("Gerando artigo... Isso pode levar alguns minutos."):
                # Inicializa agentes e tarefas
                agents = HealthArticleAgents()
                tasks = HealthArticleTasks()

                researcher = agents.research_agent()
                writer = agents.writing_agent()
                reviewer = agents.review_agent()

                # Cria tarefas com o tema inserido
                research_task_instance = tasks.research_task(researcher, topic)
                
                # Configura a tarefa de escrita
                writing_task_instance = tasks.writing_task(
                    agent=writer, 
                    research_data=topic
                )
                writing_task_instance.context = [research_task_instance]

                # Configura a tarefa de revisão
                review_task_instance = tasks.review_task(
                    agent=reviewer, 
                    article_draft="",
                    topic_context=topic
                )
                review_task_instance.context = [writing_task_instance]

                # Cria e executa a equipe com os três agentes
                crew = Crew(
                    agents=[researcher, writer, reviewer],
                    tasks=[research_task_instance, writing_task_instance, review_task_instance],
                    process=Process.sequential,
                    verbose=True
                )
                
                try:
                    crew_output = crew.kickoff()
                    article_text = ""
                    if crew_output and hasattr(crew_output, 'raw') and crew_output.raw:
                        article_text = str(crew_output.raw)
                    elif isinstance(crew_output, str):
                        article_text = crew_output
                    else:
                        st.error("Não foi possível extrair o texto do resultado da equipe.")
                        return

                    st.subheader("Artigo Gerado:")
                    if article_text:
                        st.markdown(article_text)
                        
                        # Adiciona botão de download para PDF
                        pdf_bytes = convert_markdown_to_pdf(article_text)
                        if pdf_bytes:
                            st.download_button(
                                label="Baixar Artigo em PDF",
                                data=pdf_bytes,
                                file_name=f"{topic.replace(' ', '_')}_artigo.pdf",
                                mime="application/pdf"
                            )
                except Exception as e:
                    st.error(f"Ocorreu um erro: {e}")
        else:
            st.error("Por favor, insira um tema para gerar o artigo.")

# Ponto de entrada principal
if __name__ == "__main__":
    main()

