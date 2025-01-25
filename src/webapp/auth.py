import os

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

username = os.getenv("API_USERNAME")
password = os.getenv("API_PASSWORD")
if not username or not password:
    raise ValueError("API_USERNAME or API_PASSWORD environment variable is not set.")


def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == username and credentials.password == password:
        print("User Validated")
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
