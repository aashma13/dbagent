
from pydantic import BaseModel, Field
from typing import  Optional

class StructuredResponseSchema(BaseModel):
    sql_query: str = Field(default='',
        description="Agent-generated sql_query from the sql_db_query step."
    )
    summary: str = Field(
        ...,
        description="A natural language, user-friendly answer of the user query."
    )
