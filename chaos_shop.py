import asyncio
from contextlib import asynccontextmanager
import os
import random
import time

from dotenv import load_dotenv
import faultline
from faultline.integrations.fastapi import FaultlineFastAPIMiddleware
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
app.add_middleware(FaultlineFastAPIMiddleware)


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

@app.get("/crash")
async def unhandled():
    catalog = {"widget": 29.99, "gadget": 49.99}
    item = catalog["flux-capacitor"]  # KeyError: product not found
    return {"item": item}


# Performance testing endpoints

@app.get("/fast")
async def fast():
    """Returns immediately with minimal latency."""
    return {"status": "fast"}


@app.get("/slow")
async def slow():
    """Simulates a slow 2-second asynchronous operation."""
    await asyncio.sleep(2)
    return {"status": "slow", "delay_s": 2}


@app.get("/variable")
async def variable():
    """Simulates variable network or service latency between 50ms and 1.5s."""
    delay = random.uniform(0.05, 1.5)
    await asyncio.sleep(delay)
    return {"status": "variable", "delay_s": round(delay, 3)}


@app.get("/cpu")
async def cpu_bound():
    """CPU-bound task summing squares over 5M numbers to simulate heavy compute."""
    start_time = time.perf_counter()
    total = sum(i * i for i in range(5_000_000))
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    return {"status": "cpu_bound", "elapsed_ms": round(elapsed_ms, 2), "result": total}


@app.get("/items/{item_id}")
async def get_item(item_id: int):
    """Tests route-template grouping (/items/{item_id}) with short variable delay."""
    delay = random.uniform(0.01, 0.2)
    await asyncio.sleep(delay)
    return {"item_id": item_id, "delay_s": round(delay, 3)}


@app.get("/flaky")
async def flaky():
    """Simulates an unreliable endpoint (sleeps 0.1-0.5s, fails ~30% of the time with 500)."""
    delay = random.uniform(0.1, 0.5)
    await asyncio.sleep(delay)
    if random.random() < 0.30:
        raise HTTPException(status_code=500, detail="Flaky service failure")
    return {"status": "ok", "delay_s": round(delay, 3)}
