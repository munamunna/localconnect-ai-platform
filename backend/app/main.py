from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware





app = FastAPI(
    title="LocalConnect AI Platform",
    version="0.1.0",
)

from app.api.routes import (
    freelancers,
    health,
    leads,
    agent
)

app.include_router(
    agent.router,
    prefix="/api/agent",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    health.router,
)

app.include_router(
    leads.router,
    prefix="/api/leads",
)

app.include_router(
    freelancers.router,
    prefix="/api/freelancers",
)