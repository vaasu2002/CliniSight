from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from ..models import HospitalCreate, HospitalResponse
from ingest.services.hospital import HospitalService

router = APIRouter()

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_hospital(hospital: HospitalCreate):
    """
    Create a new hospital.
    
    This endpoint allows creating a new hospital in the system.
    """
    try:
        hospital_id = HospitalService.create_hospital(
            name=hospital.name,
            country=hospital.country,
            region=hospital.region
        )
        return {"id": hospital_id, "message": "Hospital created successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create hospital: {str(e)}"
        )

@router.get("/{hospital_id}", response_model=HospitalResponse)
async def get_hospital(hospital_id: int):
    """
    Get hospital details by ID.
    
    This endpoint retrieves detailed information about a specific hospital.
    """
    try:
        hospital = HospitalService.get_hospital(hospital_id)
        if not hospital:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Hospital with ID {hospital_id} not found"
            )
        return hospital
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve hospital: {str(e)}"
        )

@router.get("/", response_model=List[HospitalResponse])
async def list_hospitals(country: Optional[str] = None, region: Optional[str] = None):
    """
    List hospitals with optional filtering.
    
    This endpoint retrieves a list of hospitals with optional filtering by country and region.
    """
    try:
        # For now, we'll return a simple list. In a real implementation,
        # you might want to add a list_hospitals method to the service
        # This is a placeholder implementation
        return []
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list hospitals: {str(e)}"
        ) 