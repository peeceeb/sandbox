from crewai import Task  # type: ignore[import-not-found]
from tools import search_tool
from agents import news_researcher,news_writer


# Research Task
research_task = Task(
    description=(
        """Identify the big trend in {topic}
            Focus on identifying pros and cons and the overall narrative
            Your final report should clearly articulate the key points
            its market opportunities, and potential risk.
        """),

    expected_output="""A comprehensive 3 paragraphs long report on the latest AI trend in {topic}""",
    tools=[search_tool],
    agent=news_researcher,
)
    

# Writing task with language model configuration
write_task=Task(
    description=(
        """Compose an insightful article on {topic}
            Focus on the latest trends and how its impacting the industry.
            The article should be easy to understand, engaging, and positive.

        """),
    expected_output=(
        """A 4 paragraphs article on {topic} advancement formatted as markdown"""
        ),
    agent=news_writer,
)

