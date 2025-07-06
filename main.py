import uvicorn

if __name__ == "__main__":
    uvicorn.run("dbagent.api:app", port=9000, host="0.0.0.0", reload=True)