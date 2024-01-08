from crewai import Agent

from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.search_tools import SearchTools
#from tools.sec_tools import SECTools
from tools.computer_volume_tools import ComputerVolumeTools

from langchain.tools.yahoo_finance_news import YahooFinanceNewsTool

from langchain.llms import Ollama

ollama_solar = Ollama(model="solar")

class PersonalAssistantAgents():
  def personal_assistant(self):
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
        ComputerVolumeTools.get_volume
        # SECTools.search_10q,
        # SECTools.search_10k
      ],
      llm=ollama_solar
    )

  # def research_analyst(self):
  #   return Agent(
  #     role='Staff Research Analyst',
  #     goal="""Being the best at gather, interpret data and amaze
  #     your customer with it""",
  #     backstory="""Known as the BEST research analyst, you're
  #     skilled in sifting through news, company announcements, 
  #     and market sentiments. Now you're working on a super 
  #     important customer""",
  #     verbose=True,
  #     tools=[
  #       BrowserTools.scrape_and_summarize_website,
  #       SearchTools.search_internet,
  #       SearchTools.search_news,
  #       YahooFinanceNewsTool(),
  #       SECTools.search_10q,
  #       SECTools.search_10k
  #     ]
  # )

  # def investment_advisor(self):
  #   return Agent(
  #     role='Private Investment Advisor',
  #     goal="""Impress your customers with full analyses over stocks
  #     and completer investment recommendations""",
  #     backstory="""You're the most experienced investment advisor
  #     and you combine various analytical insights to formulate
  #     strategic investment advice. You are now working for
  #     a super important customer you need to impress.""",
  #     verbose=True,
  #     tools=[
  #       BrowserTools.scrape_and_summarize_website,
  #       SearchTools.search_internet,
  #       SearchTools.search_news,
  #       CalculatorTools.calculate,
  #       YahooFinanceNewsTool()
  #     ]
  #   )