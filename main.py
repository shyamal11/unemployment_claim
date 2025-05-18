from fastapi import FastAPI
from api.endpoints import router as api_router
import uvicorn

app = FastAPI(title="Unemployment Fraud Detection API")
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 