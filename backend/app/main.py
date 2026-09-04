from fastapi import FastAPI

app = FastAPI(
    title="LocalConnect AI",
    description="AI-powered local services platform",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "LocalConnect AI API is running",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }