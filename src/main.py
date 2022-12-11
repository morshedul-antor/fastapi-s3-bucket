from fastapi import FastAPI
import uvicorn

import api.v1.routes
from db import settings

app = FastAPI()

@app.get("/")
async def root():
       return {"message": "CRUD Application FastAPI"}


app.include_router(api.v1.routes.api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.2", port=8000, reload=True, log_level="info")