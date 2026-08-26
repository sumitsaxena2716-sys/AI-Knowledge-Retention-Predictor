from fastapi import FastAPI

app = FastAPI(
    title="AI Knowledge Retention Predictor",
    description="Backend API for AI-powered knowledge retention analysis and adaptive quiz generation.",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    print("AI Knowledge Retention Predictor API started.")


@app.get("/")
def root():
    return {
        "message": "AI Knowledge Retention Predictor API is running"
    }