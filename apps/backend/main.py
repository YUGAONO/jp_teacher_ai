from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import CORS_ALLOWED_ORIGINS
from routers import auth, health, pdf

app = FastAPI(title="JLPT Example Generator API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(pdf.router)