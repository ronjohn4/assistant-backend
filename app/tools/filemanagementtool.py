import os
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_openai import ChatOpenAI


def init_file_management_tools():
    # 1. Setup a safe working directory
    working_dir = "./assistant_working_dir"
    os.makedirs(working_dir, exist_ok=True)

    # 2. Initialize the file management tools
    toolkit = FileManagementToolkit(
        root_dir=working_dir,
        selected_tools=["write_file", "read_file", "list_directory"]
    )
    tools = toolkit.get_tools()
    return tools
