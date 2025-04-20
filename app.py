from fastapi import FastAPI
from backend.api import router

app = FastAPI(title="Document QA System")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)