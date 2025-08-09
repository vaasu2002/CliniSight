import uuid
from typing import Optional, Dict
from ..config.database import DatabaseManager
from ..config.logger import logger

"""
[CLASS] PatientService
[DESCRIPTION] Service for managing patient operations.
[METHODS]
    - create_patient: Creates a new patient.
    - get_patient: Gets a patient by ID with hospital context.
"""
class PatientService:
    
    """
    [METHOD] create_patient
    [DESCRIPTION] Creates a new patient.
    [PARAMETERS] hospital_id: The ID of the hospital.
    [PARAMETERS] name: The name of the patient.
    [PARAMETERS] date_of_birth: The date of birth of the patient.
    [PARAMETERS] gender: The gender of the patient.
    [PARAMETERS] patient_uuid: The UUID of the patient.
    [RETURN] The ID of the created patient.
    """
    @staticmethod
    def create_patient(hospital_id: int, name: str = None, date_of_birth: str = None, 
                      gender: str = None, patient_uuid: str = None) -> int:
        """Create a new patient."""
        if patient_uuid is None:
            patient_uuid = str(uuid.uuid4())
        
        try:
            result = DatabaseManager.execute_query(
                """INSERT INTO patients (hospital_id, patient_uuid, name, date_of_birth, gender)
                   VALUES (%s, %s, %s, %s, %s) RETURNING id;""",
                (hospital_id, patient_uuid, name, date_of_birth, gender),
                fetch="one"
            )
            patient_id = result[0]
            logger.info(f"Created patient: {name} (ID: {patient_id}, UUID: {patient_uuid})")
            return patient_id
        except Exception as e:
            logger.error(f"Failed to create patient: {e}")
            raise
    
    """
    [METHOD] get_patient
    [DESCRIPTION] Gets a patient by ID with hospital context.
    [PARAMETERS] hospital_id: The ID of the hospital.
    [PARAMETERS] patient_id: The ID of the patient.
    [RETURN] The patient details.
    """
    @staticmethod
    def get_patient(hospital_id: int, patient_id: int) -> Optional[Dict]:
        """Get patient details (with hospital context)."""
        # Note: SecurityContext.set_hospital_context is not implemented yet
        # For now, we'll use a direct query with hospital_id filter
        result = DatabaseManager.execute_query(
            """SELECT id, patient_uuid, name, date_of_birth, gender, created_at 
               FROM patients 
               WHERE id = %s AND hospital_id = %s;""",
            (patient_id, hospital_id),
            fetch="one"
        )
        
        if result:
            return {
                "id": result[0],
                "uuid": str(result[1]),
                "name": result[2],
                "date_of_birth": result[3],
                "gender": result[4],
                "created_at": result[5]
            }
        return None 