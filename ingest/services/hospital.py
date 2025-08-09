from typing import Optional, Dict
from ..config.database import DatabaseManager
from ..config.logger import logger

"""
[CLASS] HospitalService
[DESCRIPTION] Service for managing hospital operations.
[METHODS]
    - create_hospital: Creates a new hospital.
    - get_hospital: Gets a hospital by ID.
"""
class HospitalService:
    
    """
    [METHOD] create_hospital
    [DESCRIPTION] Creates a new hospital.
    [PARAMETERS] name: The name of the hospital.
    [RETURN] The ID of the created hospital.
    """
    @staticmethod
    def create_hospital(name: str, country: str = None, region: str = None) -> int:
        """Create a new hospital."""
        try:
            result = DatabaseManager.execute_query(
                """INSERT INTO hospitals (name, country, region) 
                   VALUES (%s, %s, %s) 
                   ON CONFLICT (name) DO UPDATE SET 
                   country = EXCLUDED.country, region = EXCLUDED.region 
                   RETURNING id;""",
                (name, country, region),
                fetch="one"
            )
            hospital_id = result[0]
            logger.info(f"Created/updated hospital: {name} (ID: {hospital_id})")
            return hospital_id
        except Exception as e:
            logger.error(f"Failed to create hospital {name}: {e}")
            raise
    
    """
    [METHOD] get_hospital
    [DESCRIPTION] Gets a hospital by ID.
    [PARAMETERS] hospital_id: The ID of the hospital.
    [RETURN] The hospital details.
    """
    @staticmethod
    def get_hospital(hospital_id: int) -> Optional[Dict]:
        """Get hospital details."""
        result = DatabaseManager.execute_query(
            "SELECT id, name, country, region, created_at FROM hospitals WHERE id = %s;",
            (hospital_id,),
            fetch="one"
        )
        if result:
            return {
                "id": result[0],
                "name": result[1],
                "country": result[2],
                "region": result[3],
                "created_at": result[4]
            }
        return None 