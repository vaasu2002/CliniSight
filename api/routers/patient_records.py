from fastapi import APIRouter, HTTPException, status
from typing import List
from ..models import (
    PatientRecordCreate,
    PatientRecordResponse,
    PatientSearchRequest
)
from ingest.services.patient_records import PatientRecordsService

router = APIRouter()

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def add_patient_record(record: PatientRecordCreate):
    """
    Add a new patient record.
    
    This endpoint allows adding patient records that are scoped to a specific patient within a hospital.
    """
    try:
        record_id = PatientRecordsService.add_record(
            hospital_id=record.hospital_id,
            patient_id=record.patient_id,
            content=record.content,
            record_type=record.record_type,
            title=record.title,
            severity=record.severity,
            created_by=record.created_by
        )
        return {"id": record_id, "message": "Patient record added successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add patient record: {str(e)}"
        )

@router.post("/search", response_model=List[PatientRecordResponse])
async def search_patient_records(search_request: PatientSearchRequest):
    """
    Search patient records.
    
    This endpoint allows searching through patient records using semantic search.
    """
    try:
        results = PatientRecordsService.search_records(
            hospital_id=search_request.hospital_id,
            patient_id=search_request.patient_id,
            query=search_request.query,
            record_type=search_request.record_type,
            top_k=search_request.top_k
        )
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search patient records: {str(e)}"
        )

@router.get("/{hospital_id}/{patient_id}", response_model=List[PatientRecordResponse])
async def get_patient_records(
    hospital_id: int,
    patient_id: int,
    record_type: str = None,
    limit: int = 50,
    offset: int = 0
):
    """
    Get patient records for a specific patient.
    
    This endpoint retrieves records for a specific patient with optional filtering by record type.
    """
    try:
        # Use a generic search to get records
        results = PatientRecordsService.search_records(
            hospital_id=hospital_id,
            patient_id=patient_id,
            query="",  # Empty query to get all records
            record_type=record_type,
            top_k=limit
        )
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve patient records: {str(e)}"
        )

@router.get("/{hospital_id}/{patient_id}/{record_id}", response_model=PatientRecordResponse)
async def get_patient_record(hospital_id: int, patient_id: int, record_id: int):
    """
    Get a specific patient record by ID.
    
    This endpoint retrieves a specific patient record by its ID.
    """
    try:
        # For now, we'll use search to get a specific record
        # In a real implementation, you might want to add a get_record method to the service
        results = PatientRecordsService.search_records(
            hospital_id=hospital_id,
            patient_id=patient_id,
            query="",  # Empty query to get all records
            top_k=1000  # Large number to ensure we get the specific record
        )
        
        # Find the specific record
        for record in results:
            if record["id"] == record_id:
                return record
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient record with ID {record_id} not found"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve patient record: {str(e)}"
        ) 