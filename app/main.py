from fastapi import FastAPI
from .database import init_db
from .routers import points, polygons  # Corrected import

app = FastAPI()

app.include_router(points.router)
app.include_router(polygons.router)

@app.on_event("startup")
async def startup_event():  # Make startup_event async
    init_db() # Call init_db as awaitable