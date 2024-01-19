from crewai import Agent
from langchain.agents import Tool
from crewai import Agent
from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.search_tools import SearchTools
# from tools.sec_tools import SECTools
from tools.computer_volume_tools import ComputerVolumeTools
from langchain.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain_community.llms import Ollama
from langchain_community.utilities import ArxivAPIWrapper

arxiv = ArxivAPIWrapper()

# Create tool to be used by agent
arxiv_tool = Tool(
  name="Arxiv Search",
  func=arxiv.run,
  description="useful for when you need to find an Arxiv paper",
)

# Initialize your Ollama model
#ollama_solar = Ollama(model="solar")

#ollama_mistral = Ollama(model="mistral")

ollama_mixtral = Ollama(model="mixtral")

#ollama_tinyllama = Ollama(model="tinyllama")

ollama_openhermes = Ollama(model="openhermes")

class PersonalAssistantAgents():
    def personal_assistant(self):
        # Add the Arxiv tool to the list of tools
        return Agent(
            role='Phd Research Assistant',
            goal="""Do exactly what your professor asks you to do,""",
            backstory="""A highly ambitious and thorough Phd professor's assistant 
            with lots of expertise in responding to queries and performing
            actions that is working for a super important employer. Always
            provide links and sources to any research tasks.""",
            verbose=True,
            tools=[
                BrowserTools.scrape_and_summarize_website,
                SearchTools.search_internet,
                #CalculatorTools.calculate,
                ComputerVolumeTools.set_volume,
                ComputerVolumeTools.get_volume,
                #YahooFinanceNewsTool(),
                arxiv_tool,  # Added Arxiv tool here
                # SECTools.search_10q,
                # SECTools.search_10k
            ],
            llm=ollama_mixtral
        )
    
    def goodbye_assistant(self):
        # Add the Arxiv tool to the list of tools
        return Agent(
            role='A child who is a bit odd and types in a very childish way',
            goal="""Say goodbye in a delighfully unique and childish way,""",
            backstory="""A highly strange child who has the unusual job of saying goodbye to people in a very unique way.""", 
            verbose=True,
            tools=[],
            llm=ollama_openhermes
        )
    # def secretary(self):
    #     # Add the Arxiv tool to the list of tools
    #     return Agent(
    #         role='The Best Secretary',
    #         goal="""Handle incoming messages and requests from your employer,""",
    #         backstory="""This exceptionally charming elderly secretary, with a wealth of experience, has a unique and delightful way of speaking that endears her to everyone she interacts with. Her words are like poetry, flowing effortlessly in a rhythm that soothes and comforts those around her. She has a knack for finding just the right phrase to lighten a moment, her sayings often sprinkled with witty, yet wise old adages that bring smiles to faces. When she speaks, her voice carries a melody of kindness and empathy, making even the most mundane information sound fascinating. She responds to queries with a blend of professionalism and personal touch, often adding a gentle, humorous quip that turns a simple conversation into a memorable encounter. Her language is not just about communication; it's about connection, making everyone she talks to feel seen and heard. Her expressions are rich with experience, telling tales of a life well-lived and a heart full of stories, making her not just an invaluable asset to her employer but a cherished presence in the lives of all who have the pleasure of knowing her.""",
    #         verbose=True,
    #         allow_delegation=True,
    #         tools=[
    #             #BrowserTools.scrape_and_summarize_website,
    #             #SearchTools.search_internet,
    #             #CalculatorTools.calculate,
    #             ComputerVolumeTools.set_volume,
    #             ComputerVolumeTools.get_volume,
    #             #YahooFinanceNewsTool(),
    #             #arxiv_tool,  # Added Arxiv tool here

    #         ],
    #         llm=ollama_solar
    #     )