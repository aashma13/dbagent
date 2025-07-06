import os
import sqlite3
import logging
from datetime import datetime
from functools import lru_cache
from langchain.chat_models import init_chat_model
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import create_react_agent
from dbagent.prompts.template import db_agent_system_message
from dbagent.schema.chat_response import StructuredResponseSchema
from dbagent.configs.settings import settings
from dbagent.manage_log import get_logger

logger = get_logger(module_name=__name__)
    
OPENAI_API_KEY = settings.openai_api_key
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

@lru_cache(maxsize=1)
def initialize():
    logger.info("Initializing agent...")

    try:
        llm = init_chat_model(model=settings.llm_model, model_provider=settings.llm_provider)
        logger.info("Initialized chat model.")

        db = SQLDatabase.from_uri(settings.database_url)
        logger.info("Connected to SQL database.")

        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        tools = toolkit.get_tools()
        logger.info("Loaded tools from SQLDatabaseToolkit.")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_dir = f"db-agent/history/{timestamp}"
        os.makedirs(base_dir, exist_ok=True)
        logger.info(f"Created base directory at {base_dir}.")

        db_path = os.path.join(base_dir, f"agent_checkpoints_{timestamp}.sqlite")
        conn = sqlite3.connect(db_path, check_same_thread=False)
        logger.info(f"SQLite checkpoint DB created at {db_path}.")

        memory = SqliteSaver(conn=conn)

        agent_executor = create_react_agent(
            model=llm,
            tools=tools,
            prompt=db_agent_system_message.format(dialect=settings.db_backend,
                                                  top_k=settings.top_k),
            checkpointer=memory,
            debug=False,
            response_format=StructuredResponseSchema,
        )

        logger.info("Agent executor created successfully.")
        return agent_executor

    except Exception as e:
        logger.exception("Failed to initialize agent.")
        raise
