from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from parsing.utils.logger import setup_logging

from parsing.api.routes.parse import router as parse_router
from parsing.api.routes.index import router as index_router
from parsing.api.routes.query import router as query_router
from parsing.api.routes.health import router as health_router

# 🔧 Setup logging
setup_logging()
logging.getLogger("httpx").setLevel(logging.WARNING)

app = FastAPI(
    title="LegacyLift AI Engine",
    version="2.0"
)

# 🔥 Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 Register routes
app.include_router(health_router)
app.include_router(parse_router)
app.include_router(index_router)
app.include_router(query_router)