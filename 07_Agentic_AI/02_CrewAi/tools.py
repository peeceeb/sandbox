from dotenv import load_dotenv
load_dotenv()
import os

serper_api_key = os.getenv("SERPER_API_KEY")
if serper_api_key is not None:
	os.environ['SERPER_API_KEY'] = serper_api_key

from importlib import import_module

SerperDevTool = import_module("crewai_tools").SerperDevTool
search_tool = SerperDevTool()
tools = search_tool

