from typing import List, Dict
from ..config.database import DatabaseManager
from ..config.logger import logger
from .embedding import EmbeddingService

"""
[CLASS] HospitalGuidelinesService
[DESCRIPTION] Service for managing hospital-specific guidelines.
[METHODS]
    - add_guideline: Adds a hospital guideline.
    - search_guidelines: Searches hospital guidelines (hospital-scoped).
"""
class HospitalGuidelinesService:
    
    """
    [METHOD] add_guideline
    [DESCRIPTION] Adds a hospital guideline.
    [PARAMETERS] hospital_id: The ID of the hospital.
    [PARAMETERS] category: The category of the guideline.
    [PARAMETERS] title: The title of the guideline.
    [PARAMETERS] content: The content of the guideline.
    [PARAMETERS] version: The version of the guideline.
    [PARAMETERS] effective_date: The effective date of the guideline.
    [RETURN] The ID of the created guideline.
    """
    @staticmethod
    def add_guideline(hospital_id: int, category: str, title: str, content: str,
                     version: str = "1.0", effective_date: str = None) -> int:
        """Add a hospital guideline."""
        try:
            embedding = EmbeddingService.generate_embedding(f"{title} {content}")
            literal = DatabaseManager.vector_to_pg_literal(embedding)
            
            # Note: SecurityContext.set_hospital_context is not implemented yet
            # For now, we'll use a direct query with hospital_id filter
            result = DatabaseManager.execute_query(
                """INSERT INTO hospital_guidelines 
                   (hospital_id, category, title, content, version, effective_date, embedding)
                   VALUES (%s, %s, %s, %s, %s, %s, %s::vector) RETURNING id;""",
                (hospital_id, category, title, content, version, effective_date, literal),
                fetch="one"
            )
            guideline_id = result[0]
            logger.info(f"Added hospital guideline: {title} (ID: {guideline_id})")
            return guideline_id
        except Exception as e:
            logger.error(f"Failed to add hospital guideline: {e}")
            raise
    
    """
    [METHOD] search_guidelines
    [DESCRIPTION] Searches hospital guidelines (hospital-scoped).
    [PARAMETERS] hospital_id: The ID of the hospital.
    [PARAMETERS] query: The search query.
    [PARAMETERS] category: The category to filter by.
    [PARAMETERS] top_k: The number of results to return.
    [RETURN] List of matching guidelines.
    """
    @staticmethod
    def search_guidelines(hospital_id: int, query: str, category: str = None, 
                         top_k: int = 5) -> List[Dict]:
        """Search hospital guidelines (hospital-scoped)."""
        try:
            embedding = EmbeddingService.generate_embedding(query)
            literal = DatabaseManager.vector_to_pg_literal(embedding)
            
            where_clause = ""
            params = [literal, top_k]
            if category:
                where_clause = "AND category = %s"
                params.insert(-1, category)
            
            query_sql = f"""
                SELECT id, category, title, content, version, effective_date,
                       embedding <-> %s::vector AS distance
                FROM hospital_guidelines
                WHERE hospital_id = %s {where_clause}
                ORDER BY embedding <-> %s::vector
                LIMIT %s;
            """
            
            # Add hospital_id to params
            params.insert(0, hospital_id)
            
            results = DatabaseManager.execute_query(query_sql, tuple(params), fetch="all")
            
            return [{
                "id": r[0],
                "category": r[1],
                "title": r[2],
                "content": r[3],
                "version": r[4],
                "effective_date": r[5],
                "similarity_score": 1 - r[6]
            } for r in results]
        except Exception as e:
            logger.error(f"Failed to search hospital guidelines: {e}")
            raise 