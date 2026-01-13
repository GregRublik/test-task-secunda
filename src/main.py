from fastapi import FastAPI, Depends
from api.v1.endpoints.organizations import router
from config import settings
from depends import api_key_auth
import uvicorn

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()

app.include_router(router, prefix="/api/v1", dependencies=[Depends(api_key_auth)])

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)
