import streamlit as st
import asyncio
import logging
from dbagent.directories import create_directories_async, clear_local_db_folder
from dbagent.schema.chat_request import ChatRequest
from dbagent.services.chat_service import ChatService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="DB Agent Chat",
    layout="centered"
)

def run_async(coro):
    """Helper to run async functions in Streamlit"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

def initialize_app():
    """Initialize the application"""
    if 'initialized' not in st.session_state:
        with st.spinner("Initializing..."):
            try:
                run_async(create_directories_async("db-agent"))
                st.session_state.initialized = True
                logger.info("App initialized successfully")
            except Exception as e:
                st.error(f"Initialization failed: {e}")
                st.session_state.initialized = False

def main():
    st.title("DB Agent Chat")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    initialize_app()
    
    if not st.session_state.get('initialized', False):
        st.error("Failed to initialize. Please refresh the page.")
        return
    
    # Sidebar
    with st.sidebar:
        st.header("Controls")
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("Cleanup"):
            try:
                run_async(clear_local_db_folder("db-agent"))
                st.success("Cleanup complete!")
            except Exception as e:
                st.error(f"Cleanup failed: {e}")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                try:
                    chat_request = ChatRequest(user_query=prompt)
                    
                    response = run_async(ChatService(chat_request).converse())
                    st.write(response.summary)
                    st.session_state.messages.append({"role": "assistant", "content": response.summary})
                    
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main()