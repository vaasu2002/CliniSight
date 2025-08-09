from fastapi import APIRouter, HTTPException, status
from typing import List
from ..models import (
    HospitalGuidelineCreate,
    HospitalGuidelineResponse,
    HospitalGuidelineSearchRequest
)
from ingest.services.hospital_guidelines import HospitalGuidelinesService

router = APIRouter()

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def add_hospital_guideline(guideline: HospitalGuidelineCreate):
    """
    Add a new hospital guideline.
    
    This endpoint allows adding hospital-specific guidelines that are scoped to a particular hospital.
    """
    try:
        guideline_id = HospitalGuidelinesService.add_guideline(
            hospital_id=guideline.hospital_id,
            category=guideline.category,
            title=guideline.title,
            content=guideline.content,
            version=guideline.version,
            effective_date=guideline.effective_date
        )
        return {"id": guideline_id, "message": "Hospital guideline added successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add hospital guideline: {str(e)}"
        )

@router.post("/search", response_model=List[HospitalGuidelineResponse])
async def search_hospital_guidelines(search_request: HospitalGuidelineSearchRequest):
    """
    Search hospital guidelines.
    
    This endpoint allows searching through hospital-specific guidelines using semantic search.
    """
    try:
        results = HospitalGuidelinesService.search_guidelines(
            hospital_id=search_request.hospital_id,
            query=search_request.query,
            category=search_request.category,
            top_k=search_request.top_k
        )
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search hospital guidelines: {str(e)}"
        )

@router.get("/hospital/{hospital_id}", response_model=List[HospitalGuidelineResponse])
async def get_hospital_guidelines(
    hospital_id: int,
    category: str = None,
    top_k: int = 10
):
    """
    Get hospital guidelines for a specific hospital.
    
    This endpoint retrieves guidelines for a specific hospital with optional category filtering.
    """
    try:
        # Use a generic search to get guidelines
        results = HospitalGuidelinesService.search_guidelines(
            hospital_id=hospital_id,
            query="",  # Empty query to get all guidelines
            category=category,
            top_k=top_k
        )
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve hospital guidelines: {str(e)}"
        ) 