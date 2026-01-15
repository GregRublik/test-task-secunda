from fastapi import FastAPI, Depends
from api.v1.endpoints.organizations import router
from config import settings
import uvicorn

app = FastAPI()

app.include_router(router, prefix="/api/v1", )

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)
