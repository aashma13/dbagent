import logging
from dbagent.schema.chat_request import ChatRequest
from dbagent.services.agent_initializer import initialize
from dbagent.manage_log import get_logger

logger = get_logger(module_name=__name__)

class ChatService:
    def __init__(self, payload: ChatRequest):
        self.payload = payload
        logger.debug(f"Initializing agent executor for session_id: {payload.session_id}")
        self.agent_executor = initialize()
        
    def get_config(self):
        config = {
            "recursion_limit": 20,
            "configurable": {
                "thread_id": self.payload.session_id,
            }
        }
        return config

    async def converse(self):
        """
        Yields formatted strings including model output, SQL tool usage, and results.
        """
        output = None
        try:
            logger.info(f"Starting conversation for session_id: {self.payload.session_id}")
            config = self.get_config()
            for step in self.agent_executor.stream(
                {
                    "messages": [{"role": "user", "content": self.payload.user_query}]
                },
                stream_mode="values", config=config
            ):
                step["messages"][-1].pretty_print()
            
            output = step.get('structured_response')
            logger.info(f"Conversation completed for session_id: {self.payload.session_id}")
            logger.info(f"{output=}")
            return output
        except Exception as e:
            logger.exception(f"Error during conversation for session_id: {self.payload.session_id}")
            raise
