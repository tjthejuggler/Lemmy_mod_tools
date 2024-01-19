from crewai import Task
from textwrap import dedent

class PersonalAssistantTasks():
  def respond(self, agent, input):
    return Task(description=dedent(f"""
        Receive input from your professor and determine if it is
        a question that only needs a response or if it is a command
        that requires you to perform an action with one of your tools.
        
        {self.__tip_section()}
  
        Here is your professors input: {input}
      """),
      agent=agent
    )
  
  def goodbye(self, agent):
    return Task(description=dedent(f"""
        Say goodbye to your professor and end the conversation in a very strange way.        
        {self.__tip_section()}
      """),
      agent=agent
    )
    
  # def financial_analysis(self, agent): 
  #   return Task(description=dedent(f"""
  #       Conduct a thorough analysis of the stock's financial
  #       health and market performance. 
  #       This includes examining key financial metrics such as
  #       P/E ratio, EPS growth, revenue trends, and 
  #       debt-to-equity ratio. 
  #       Also, analyze the stock's performance in comparison 
  #       to its industry peers and overall market trends.

  #       Your final report MUST expand on the summary provided
  #       but now including a clear assessment of the stock's
  #       financial standing, its strengths and weaknesses, 
  #       and how it fares against its competitors in the current
  #       market scenario.{self.__tip_section()}

  #       Make sure to use the most recent data possible.
  #     """),
  #     agent=agent
  #   )

  # def filings_analysis(self, agent):
  #   return Task(description=dedent(f"""
  #       Analyze the latest 10-Q and 10-K filings from EDGAR for
  #       the stock in question. 
  #       Focus on key sections like Management's Discussion and
  #       Analysis, financial statements, insider trading activity, 
  #       and any disclosed risks.
  #       Extract relevant data and insights that could influence
  #       the stock's future performance.

  #       Your final answer must be an expanded report that now
  #       also highlights significant findings from these filings,
  #       including any red flags or positive indicators for
  #       your customer.
  #       {self.__tip_section()}        
  #     """),
  #     agent=agent
  #   )

  # def recommend(self, agent):
  #   return Task(description=dedent(f"""
  #       Review and synthesize the analyses provided by the
  #       Financial Analyst and the Research Analyst.
  #       Combine these insights to form a comprehensive
  #       investment recommendation. 
        
  #       You MUST Consider all aspects, including financial
  #       health, market sentiment, and qualitative data from
  #       EDGAR filings.

  #       Make sure to include a section that shows insider 
  #       trading activity, and upcoming events like earnings.

  #       Your final answer MUST be a recommendation for your
  #       customer. It should be a full super detailed report, providing a 
  #       clear investment stance and strategy with supporting evidence.
  #       Make it pretty and well formatted for your customer.
  #       {self.__tip_section()}
  #     """),
  #     agent=agent
  #   )

  def __tip_section(self):
    return "If you do your BEST WORK, I'll give you a $10,000 commission!"
