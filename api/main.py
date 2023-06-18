import os
import uvicorn
from dotenv import load_dotenv

from fastapi import FastAPI
from starlette.responses import JSONResponse

# load env variables
# load_dotenv('./.env')

app = FastAPI(title="DAMG 7245")


@app.get("/api/v1/health-check")
async def health_check() -> JSONResponse:
    response = {"msg": "Health is up"}
    return JSONResponse(status_code=200, content=response)


host = os.getenv("FASTAPI_HOST", "localhost")
port = os.getenv("FASTAPI_PORT", 8095)

uvicorn.run(app, host=host, port=int(port))
