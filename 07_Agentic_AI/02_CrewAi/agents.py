from dotenv import load_dotenv
from crewai import Agent, LLM
import os

load_dotenv()
llm = LLM(
    model="gemini/gemini-2.5-flash",
    temperature=0.5,
    api_key=os.getenv("GOOGLE_API_KEY"),
)



# Creating a senior researcher agent with memory and verbose mode

researcher= Agent(
    role="Senior Researcher",
    goal="Uncover ground breaking technologies in {topic}",
    verbose=True,
    memory=True,
    backstory=(""" Driven by curiosity, you are at the forefront of innovation, eagerness to explore and share knowledge that could change the world"""),
    llm=llm,
    allow_delegation=True
)

news_researcher= Agent(
    role="Research Writer",
    goal="Demonstrate ability to research in corrresponding news {topic}",
    verbose=True,
    memory=True,
    backstory=(""" Driven by curiosity, you are at the forefront of innovation, eagerness to explore and share knowledge that could change the world"""),
    llm=llm,
    allow_delegation=True
)

news_writer= Agent(
    role="Tech Writer",
    goal="Narrate compelling tech stories about {topic}",
    verbose=True,
    memory=True,
    backstory=(""" Driven by curiosity, you are at the forefront of innovation, eagerness to explore and share knowledge that could change the world"""),
    llm=llm,
    allow_delegation=True
)

