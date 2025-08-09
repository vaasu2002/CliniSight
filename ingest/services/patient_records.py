from typing import List, Dict
from ..config.database import DatabaseManager
from ..config.logger import logger
from .embedding import EmbeddingService

"""
[CLASS] PatientRecordsService
[DESCRIPTION] Service for managing patient records with strict access control.
[METHODS]
    - add_record: Adds a patient record.
    - search_records: Searches patient records (patient-scoped).
"""
class PatientRecordsService:
    
    """
    [METHOD] add_record
    [DESCRIPTION] Adds a patient record.
    [PARAMETERS] hospital_id: The ID of the hospital.
    [PARAMETERS] patient_id: The ID of the patient.
    [PARAMETERS] content: The content of the record.
    [PARAMETERS] record_type: The type of the record.
    [PARAMETERS] title: The title of the record.
    [PARAMETERS] severity: The severity of the record.
    [PARAMETERS] created_by: The user who created the record.
    [RETURN] The ID of the created record.
    """
    @staticmethod
    def add_record(hospital_id: int, patient_id: int, content: str, 
                  record_type: str = "note", title: str = None, 
                  severity: str = "medium", created_by: str = None) -> int:
        """Add a patient record."""
        try:
            embedding = EmbeddingService.generate_embedding(f"{title or ''} {content}")
            literal = DatabaseManager.vector_to_pg_literal(embedding)
            
            # Note: SecurityContext.set_hospital_context and SecurityContext.set_patient_context are not implemented yet
            # For now, we'll use a direct query with hospital_id and patient_id filters
            result = DatabaseManager.execute_query(
                """INSERT INTO patient_records 
                   (hospital_id, patient_id, record_type, title, content, severity, embedding, created_by)
                   VALUES (%s, %s, %s, %s, %s, %s, %s::vector, %s) RETURNING id;""",
                (hospital_id, patient_id, record_type, title, content, severity, literal, created_by),
                fetch="one"
            )
            record_id = result[0]
            logger.info(f"Added patient record (ID: {record_id}) for patient {patient_id}")
            return record_id
        except Exception as e:
            logger.error(f"Failed to add patient record: {e}")
            raise
    
    """
    [METHOD] search_records
    [DESCRIPTION] Searches patient records (patient-scoped).
    [PARAMETERS] hospital_id: The ID of the hospital.
    [PARAMETERS] patient_id: The ID of the patient.
    [PARAMETERS] query: The search query.
    [PARAMETERS] record_type: The type of record to filter by.
    [PARAMETERS] top_k: The number of results to return.
    [RETURN] List of matching records.
    """
    @staticmethod
    def search_records(hospital_id: int, patient_id: int, query: str, 
                      record_type: str = None, top_k: int = 5) -> List[Dict]:
        """Search patient records (patient-scoped)."""
        try:
            embedding = EmbeddingService.generate_embedding(query)
            literal = DatabaseManager.vector_to_pg_literal(embedding)
            
            where_clause = ""
            params = [literal, top_k]
            if record_type:
                where_clause = "AND record_type = %s"
                params.insert(-1, record_type)
            
            query_sql = f"""
                SELECT id, record_type, title, content, severity, created_by, created_at,
                       embedding <-> %s::vector AS distance
                FROM patient_records
                WHERE hospital_id = %s AND patient_id = %s {where_clause}
                ORDER BY embedding <-> %s::vector
                LIMIT %s;
            """
            
            # Add hospital_id and patient_id to params
            params.insert(0, hospital_id)
            params.insert(1, patient_id)
            
            results = DatabaseManager.execute_query(query_sql, tuple(params), fetch="all")
            
            return [{
                "id": r[0],
                "record_type": r[1],
                "title": r[2],
                "content": r[3],
                "severity": r[4],
                "created_by": r[5],
                "created_at": r[6],
                "similarity_score": 1 - r[7]
            } for r in results]
        except Exception as e:
            logger.error(f"Failed to search patient records: {e}")
            raise 