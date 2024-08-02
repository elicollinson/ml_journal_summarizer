import os
import tempfile
from autogen import ConversableAgent
from autogen.coding import DockerCommandLineCodeExecutor
from app.util.scrape_utils import ScrapeUtils
from app.config.config import settings

class ScholarlySummary(self):
    
    def __init__(self):
        self.scrape_utils = ScrapeUtils()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.docs = self.scrape_utils.get_docs()

    
    
    # Create a Docker command line code executor.
    executor = DockerCommandLineCodeExecutor(
        image=settings.EXECUTION_IMAGE,  # Execute code using the given docker image name.
        timeout=int(settings.EXECUTION_TIMEOUT),  # Timeout for each code execution in seconds.
        work_dir=self.temp_dir.name,  # Use the temporary directory to store the code files.
    )

    code_writer_agent = ConversableAgent(
        "code_writer_agent",
        system_message=settings.CODE_WRITER_SYSTEM_MESSAGE,
        llm_config={"config_list": [{"model": settings.MODEL, "api_key": settings.OPENAI_API_KEY}]},
        code_execution_config=False,  # Turn off code execution for this agent.
    )
    
    # Create an agent with code executor configuration that uses docker.
    code_executor_agent_using_docker = ConversableAgent(
        "code_executor_agent_docker",
        llm_config=False,  # Turn off LLM for this agent.
        code_execution_config={"executor": executor},  # Use the docker command line code executor.
        human_input_mode="ALWAYS",  # Always take human input for this agent for safety.
    )

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    chat_result = code_executor_agent_using_docker.initiate_chat(
        code_writer_agent,
        message=f"Today is {today}. Write Python code to plot TSLA's and META's "
        "stock price gains YTD, and save the plot to a file named 'stock_gains.png'.",
    )