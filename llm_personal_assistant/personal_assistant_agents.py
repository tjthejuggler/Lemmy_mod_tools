# from crewai import Agent
# from tools.browser_tools import BrowserTools
# from tools.calculator_tools import CalculatorTools
# from tools.search_tools import SearchTools
# # from tools.sec_tools import SECTools
# from tools.computer_volume_tools import ComputerVolumeTools
# from langchain.tools.yahoo_finance_news import YahooFinanceNewsTool
# from langchain.agents import AgentType, initialize_agent, load_tools
# from langchain.llms import Ollama

# ollama_solar = Ollama(model="solar")

# class PersonalAssistantAgents():
#     def personal_assistant(self):
#         return Agent(
#             role='The Best Personal Assistant',
#             goal="""Do exactly what your employer asks you to do,""",
#             backstory="""The most seasoned personal assistant with 
#             lots of expertise in responding to queries and performing
#             actions that is working for a super important employer.""",
#             verbose=True,
#             tools=[
#                 BrowserTools.scrape_and_summarize_website,
#                 SearchTools.search_internet,
#                 CalculatorTools.calculate,
#                 ComputerVolumeTools.set_volume,
#                 ComputerVolumeTools.get_volume,
#                 YahooFinanceNewsTool(),
#                 # SECTools.search_10q,
#                 # SECTools.search_10k
#             ],
#             llm=ollama_solar
#         )



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
from langchain.llms import Ollama
from langchain_community.utilities import ArxivAPIWrapper

arxiv = ArxivAPIWrapper()

# Create tool to be used by agent
arxiv_tool = Tool(
  name="Arxiv Search",
  func=arxiv.run,
  description="useful for when you need to find an Arxiv paper",
)

# Initialize your Ollama model
ollama_solar = Ollama(model="solar")

class PersonalAssistantAgents():
    def personal_assistant(self):
        # Add the Arxiv tool to the list of tools
        return Agent(
            role='The Best Personal Assistant',
            goal="""Do exactly what your employer asks you to do,""",
            backstory="""The most seasoned personal assistant with 
            lots of expertise in responding to queries and performing
            actions that is working for a super important employer.""",
            verbose=True,
            tools=[
                BrowserTools.scrape_and_summarize_website,
                SearchTools.search_internet,
                CalculatorTools.calculate,
                ComputerVolumeTools.set_volume,
                ComputerVolumeTools.get_volume,
                YahooFinanceNewsTool(),
                arxiv_tool,  # Added Arxiv tool here
                # SECTools.search_10q,
                # SECTools.search_10k
            ],
            llm=ollama_solar
        )
