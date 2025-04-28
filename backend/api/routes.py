from fastapi import APIRouter, HTTPException
from api.predict import router as predict_router
from api.explain import router as explain_router

router = APIRouter()

router.include_router(predict_router, prefix="/predict", tags=["predictions"])
router.include_router(explain_router, prefix="/explain", tags=["explanations"])

@router.get("/health")
async def health_check():
    return {"status": "healthy"}