from contextlib import asynccontextmanager
import os

from dotenv import load_dotenv
import faultline
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    faultline.init(
        dsn=os.getenv("FAULTLINE_DSN"),
        environment="development"
    )
    yield
    faultline.close(timeout=2.0)


app = FastAPI(lifespan=lifespan)


@app.get('/', response_class=FileResponse)
async def index():
    return FileResponse("index.html")


@app.get('/caught')
async def divide():
    a = 10
    b = 0
    try: 
        return {"result": a / b}
    except ZeroDivisionError as exc:
        faultline.capture_exception(exc)
        raise HTTPException(status_code=500, detail="cannot divide by zero")