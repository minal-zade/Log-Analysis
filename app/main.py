from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Log Analysis REST API (File Based)",
    description="Directly analyzes log files without a database.",
    version="1.0.0"
)

app.include_router(router)
