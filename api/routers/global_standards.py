from fastapi import APIRouter, HTTPException, status
from typing import List
from ..models import (
    GlobalStandardCreate,
    GlobalStandardResponse,
    SearchRequest
)
from ingest.services.global_standards import GlobalStandardsService

router = APIRouter()

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def add_global_standard(standard: GlobalStandardCreate):
    """
    Add a new global medical standard.
    
    This endpoint allows adding global medical standards that are accessible by all hospitals.
    """
    try:
        standard_id = GlobalStandardsService.add_standard(
            category=standard.category,
            title=standard.title,
            content=standard.content,
            subcategory=standard.subcategory,
            source=standard.source,
            version=standard.version
        )
        return {"id": standard_id, "message": "Global standard added successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add global standard: {str(e)}"
        )

@router.post("/search", response_model=List[GlobalStandardResponse])
async def search_global_standards(search_request: SearchRequest):
    """
    Search global medical standards.
    
    This endpoint allows searching through global medical standards using semantic search.
    """
    try:
        results = GlobalStandardsService.search_standards(
            query=search_request.query,
            category=search_request.category,
            top_k=search_request.top_k
        )
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search global standards: {str(e)}"
        )

@router.get("/", response_model=List[GlobalStandardResponse])
async def get_global_standards(category: str = None, top_k: int = 10):
    """
    Get global medical standards.
    
    This endpoint allows retrieving global medical standards with optional category filtering.
    """
    try:
        # Use a generic search to get standards
        results = GlobalStandardsService.search_standards(
            query="",  # Empty query to get all standards
            category=category,
            top_k=top_k
        )
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve global standards: {str(e)}"
        ) 