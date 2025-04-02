import os
import logging
from crewai import Agent, Task, Process, Crew, LLM

# Setup basic configuration for logging
logging.basicConfig(level=logging.DEBUG, filename=os.path.join(os.path.dirname(__file__), 'crewai_log.txt'), 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Set your API key
api_key = os.getenv("GITHUB_API_KEY")
if not api_key:
    raise ValueError("GITHUB_API_KEY environment variable is not set. Please set it before running the application.")

# Define the model
llm = LLM(
    model="gpt-4o",
    base_url="https://models.inference.ai.azure.com",
    api_key=api_key
)

def run_analysis(business_idea):
    # Define agents
    marketer = Agent(
        role="Market Research Analyst",
        goal="Find out how big is the demand for my products and suggest how to reach the widest possible customer base",
        backstory="""You are an expert at understanding the market demand, target audience, and competition. This is crucial for 
        validating whether an idea fulfills a market need and has the potential to attract a wide audience. You are good at coming up
        with ideas on how to appeal to the widest possible audience.""",
        verbose=True,
        allow_delegation=True,
        llm=llm
    )

    technologist = Agent(
        role="Technology Expert",
        goal="Assess the technological feasibility and what technologies the company needs to adopt to succeed",
        backstory="You are a visionary in the realm of technology, with a deep understanding of both current and emerging technological trends.",
        verbose=True,
        allow_delegation=True,
        llm=llm
    )

    business_consultant = Agent(
        role="Business Development Consultant",
        goal="Evaluate and advise on the business model, scalability, and potential revenue streams for long-term sustainability",
        backstory="You are a seasoned professional with expertise in shaping business strategies.",
        verbose=True,
        allow_delegation=True,
        llm=llm
    )

    # Define tasks for each agent
    task1 = Task(
        description=f"Analyze the market demand for {business_idea}",
        expected_output="A detailed report with customer profile and marketing strategies.",
        agent=marketer
    )

    task2 = Task(
        description=f"Analyze how to produce {business_idea}",
        expected_output="A detailed report outlining the required technologies.",
        agent=technologist
    )

    task3 = Task(
        description="Analyze and summarize marketing and technological report",
        expected_output="A comprehensive business plan with goals and a timeline.",
        agent=business_consultant
    )

    # Create the crew with a sequential process
    crew = Crew(
        agents=[marketer, technologist, business_consultant],
        tasks=[task1, task2, task3],
        verbose=True,
        process=Process.sequential
    )

    # Execute the crew and handle the result with logging
    try:
        result = crew.kickoff()
        logging.info(f'Crew execution completed successfully: {result}')
        return result
    except Exception as e:
        logging.error(f'An error occurred during crew execution: {str(e)}')
        raise

if __name__ == '__main__':
    result = run_analysis("plugs for holes in Crocs")
    print("######################")
    print(result)