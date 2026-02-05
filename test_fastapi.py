from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "✅ FastAPI Test Successful!"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": "2024-01-01"}
