from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from dbagent.directories import create_directories_async, clear_local_db_folder
from dbagent.schema.chat_request import ChatRequest
from dbagent.services.chat_service import ChatService
from dbagent.manage_log import get_logger

logger = get_logger(module_name=__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up: Creating necessary directories.")
    await create_directories_async("db-agent")
    yield
    logger.info("Shutting down: Cleaning up directories.")
    await clear_local_db_folder("db-agent")
    logger.info("Cleanup complete.")

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Consider limiting for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(req: ChatRequest):
    service = ChatService(req)
    resp = await service.converse()
    return resp

