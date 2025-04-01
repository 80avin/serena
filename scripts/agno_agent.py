import os
from logging import Logger

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.models.google import Gemini
from agno.playground import Playground, serve_playground_app
from dotenv import load_dotenv
from sensai.util import logging
from sensai.util.helper import mark_used

from serena.agent import SerenaAgent
from serena.agno import SerenaAgnoToolkit

mark_used(Gemini, Claude)

os.chdir(os.path.dirname(os.path.abspath(__file__)))
Logger.root.setLevel(logging.INFO)

load_dotenv()

project_file_path = "../myproject.yml"
serena_agent = SerenaAgent(project_file_path, start_language_server=True)
toolkit = SerenaAgnoToolkit(serena_agent)

# model = Claude(id="claude-3-7-sonnet-20250219")
model = Gemini(id="gemini-2.5-pro-exp-03-25")

agno_agent = Agent(
    name="Serena",
    model=model,
    description="A fully-featured coding assistant",
    tools=[toolkit],  # type: ignore
    show_tool_calls=False,
    markdown=True,
    system_message="",  # Todo
    read_tool_call_history=False,
    telemetry=False,
)

# The app object must be in the module scope so that the server can access it for hot reloading
app = Playground(agents=[agno_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("agno_agent:app", reload=False)
