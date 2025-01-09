from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def healthcheck():
    """Check if the API is running."""
    return {"status": "healthy"}
