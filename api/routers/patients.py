from fastapi import APIRouter, HTTPException, status
from typing import List
from ..models import PatientCreate, PatientResponse
from ingest.services.patient import PatientService

router = APIRouter()

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_patient(patient: PatientCreate):
    """
    Create a new patient.
    
    This endpoint allows creating a new patient in a specific hospital.
    """
    try:
        patient_id = PatientService.create_patient(
            hospital_id=patient.hospital_id,
            name=patient.name,
            date_of_birth=patient.date_of_birth,
            gender=patient.gender,
            patient_uuid=patient.patient_uuid
        )
        return {"id": patient_id, "message": "Patient created successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create patient: {str(e)}"
        )

@router.get("/{hospital_id}/{patient_id}", response_model=PatientResponse)
async def get_patient(hospital_id: int, patient_id: int):
    """
    Get patient details by ID.
    
    This endpoint retrieves detailed information about a specific patient within a hospital context.
    """
    try:
        patient = PatientService.get_patient(hospital_id, patient_id)
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Patient with ID {patient_id} not found in hospital {hospital_id}"
            )
        return patient
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve patient: {str(e)}"
        )

@router.get("/hospital/{hospital_id}", response_model=List[PatientResponse])
async def list_hospital_patients(hospital_id: int, limit: int = 50, offset: int = 0):
    """
    List patients for a specific hospital.
    
    This endpoint retrieves a list of patients for a specific hospital with pagination.
    """
    try:
        # For now, we'll return a simple list. In a real implementation,
        # you might want to add a list_patients method to the service
        # This is a placeholder implementation
        return []
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list patients: {str(e)}"
        ) 