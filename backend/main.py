from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, claims
from app.db.base import Base
from app.db.session import engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Unemployment Claims API",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost:3000",  # Local development
    "https://unemployment-claims.vercel.app",  # Vercel deployment
    "https://*.vercel.app",  # Any Vercel preview deployments
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(claims.router, prefix="/api/claims", tags=["claims"])

@app.get("/")
async def root():
    return {"message": "Unemployment Claims API"} 