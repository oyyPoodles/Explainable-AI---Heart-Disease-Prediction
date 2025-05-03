from fastapi import APIRouter
from backend.api.predict import router as predict_router
from backend.api.explain import router as explain_router

# Create the main router
router = APIRouter()

# Include the prediction and explanation routers
router.include_router(predict_router, prefix="/predict", tags=["Predictions"])
router.include_router(explain_router, prefix="/explain", tags=["Explanations"])

@router.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {
        "status": "healthy",
        "service": "Heart XAI Chatbot API",
        "version": "1.0.0"
    }