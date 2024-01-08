#if i get ImportError: cannot import name 'InstanceOf' from 'pydantic'
# pip install --upgrade pydantic

from crewai import Crew
from textwrap import dedent

from personal_assistant_agents import PersonalAssistantAgents
from personal_assistant_tasks import PersonalAssistantTasks

from dotenv import load_dotenv

import sys

load_dotenv()

class FinancialCrew:
  def __init__(self, input):
    self.input = input

  def run(self):
    agents = PersonalAssistantAgents()
    tasks = PersonalAssistantTasks()

    # research_analyst_agent = agents.research_analyst()
    # financial_analyst_agent = agents.financial_analyst()
    # investment_advisor_agent = agents.investment_advisor()
    personal_assistant = agents.personal_assistant()

    respond_task = tasks.respond(personal_assistant, self.input)
    # research_task = tasks.research(research_analyst_agent, self.company)
    # financial_task = tasks.financial_analysis(financial_analyst_agent)
    # filings_task = tasks.filings_analysis(financial_analyst_agent)
    # recommend_task = tasks.recommend(investment_advisor_agent)

    crew = Crew(
      agents=[
        # research_analyst_agent,
        # financial_analyst_agent,
        # investment_advisor_agent
        personal_assistant
      ],
      tasks=[
        # research_task,
        # financial_task,
        # filings_task,
        # recommend_task
        respond_task
      ],
      verbose=True
    )

    result = crew.kickoff()
    return result

if __name__ == "__main__":
    print("## Hi TJ!")
    print('-------------------------------')

    if len(sys.argv) < 2:
        print(dedent("""
            Please provide an input argument when running the program.
            Usage: python main.py <input>
        """))
        sys.exit(1)

    input_arg = sys.argv[1]
  
    financial_crew = FinancialCrew(input_arg)
    result = financial_crew.run()
    print("\n\n########################")
    print("## Here is my response")
    print("########################\n")
    print(result)
