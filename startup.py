import os
import logging
from crewai import Agent, Task, Process, Crew
from langchain.chat_models import ChatOpenAI

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO)

# Set your OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

# Define the OpenAI model using the correct model name
llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=api_key)


marketer = Agent(
    role="Market Research Analyst",
    goal="Find out how big is the demand for my products and suggest how to reach the widest possible customer base",
    backstory="""You are an expert at understanding the market demand, target audience, and competition. This is crucial for 
		validating whether an idea fulfills a market need and has the potential to attract a wide audience. You are good at coming up
		with ideas on how to appeal to widest possible audience.
		""",
    verbose=True,  # enable more detailed or extensive output
    allow_delegation=True,  # enable collaboration between agent
    llm=llm # to load gemini
)

technologist = Agent(
    role="Technology Expert",
    goal="Assess the technological feasibility and what technologies the company needs to adopt to succeed",
    backstory=(
        "You are a visionary in the realm of technology, with a deep understanding of both current and "
        "emerging technological trends. Your expertise lies in knowing the technology and foreseeing how "
        "it can be leveraged to solve real-world problems and drive business innovation."
    ),
    verbose=True,
    allow_delegation=True,
    llm=llm  # Assigning the language model to the agent
)

business_consultant = Agent(
    role="Business Development Consultant",
    goal="Evaluate and advise on the business model, scalability, and potential revenue streams for long-term sustainability",
    backstory=(
        "You are a seasoned professional with expertise in shaping business strategies. Your insight is "
        "essential for turning innovative ideas into viable business models."
    ),
    verbose=True,
    allow_delegation=True,
    llm=llm  # Assigning the language model to the agent
)

# Define tasks for each agent
task1 = Task(
    description="Analyze the market demand for plugs for holes in Crocs...",
    expected_output="A detailed report with customer profile and marketing strategies.",
    agent=marketer
)

task2 = Task(
    description="Analyze how to produce plugs for Crocs...",
    expected_output="A detailed report outlining the required technologies.",
    agent=technologist
)

task3 = Task(
    description="Analyze and summarize marketing and technological report...",
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
except Exception as e:
    logging.error(f'An error occurred during crew execution: {str(e)}')

# Print the result for inspection
print("######################")
print(result)
