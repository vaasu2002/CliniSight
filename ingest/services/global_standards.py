from typing import List, Dict
from ..config.database import DatabaseManager
from ..config.logger import logger
from .embedding import EmbeddingService

"""
[CLASS] GlobalStandardsService
[DESCRIPTION] Service for managing global medical standards (accessible by all hospitals).
[METHODS]
    - add_standard: Adds a global medical standard.
    - search_standards: Searches global medical standards.
"""
class GlobalStandardsService:
    
    """
    [METHOD] add_standard
    [DESCRIPTION] Adds a global medical standard.
    [PARAMETERS] category: The category of the standard.
    [PARAMETERS] title: The title of the standard.
    [PARAMETERS] content: The content of the standard.
    [PARAMETERS] subcategory: The subcategory of the standard.
    [PARAMETERS] source: The source of the standard.
    [PARAMETERS] version: The version of the standard.
    [RETURN] The ID of the created standard.
    """
    @staticmethod
    def add_standard(category: str, title: str, content: str, 
                    subcategory: str = None, source: str = None, version: str = "1.0") -> int:
        """Add a global medical standard."""
        try:
            embedding = EmbeddingService.generate_embedding(f"{title} {content}")
            literal = DatabaseManager.vector_to_pg_literal(embedding)
            
            result = DatabaseManager.execute_query(
                """INSERT INTO global_medical_standards 
                   (category, subcategory, title, content, source, version, embedding)
                   VALUES (%s, %s, %s, %s, %s, %s, %s::vector) RETURNING id;""",
                (category, subcategory, title, content, source, version, literal),
                fetch="one"
            )
            standard_id = result[0]
            logger.info(f"Added global standard: {title} (ID: {standard_id})")
            return standard_id
        except Exception as e:
            logger.error(f"Failed to add global standard: {e}")
            raise
    
    """
    [METHOD] search_standards
    [DESCRIPTION] Searches global medical standards.
    [PARAMETERS] query: The search query.
    [PARAMETERS] category: The category to filter by.
    [PARAMETERS] top_k: The number of results to return.
    [RETURN] List of matching standards.
    """
    @staticmethod
    def search_standards(query: str, category: str = None, top_k: int = 5) -> List[Dict]:
        """Search global medical standards."""
        try:
            embedding = EmbeddingService.generate_embedding(query)
            literal = DatabaseManager.vector_to_pg_literal(embedding)
            
            where_clause = ""
            params = [literal, top_k]
            if category:
                where_clause = "WHERE category = %s"
                params.insert(-1, category)
            
            query_sql = f"""
                SELECT id, category, subcategory, title, content, source, version,
                       embedding <-> %s::vector AS distance
                FROM global_medical_standards
                {where_clause}
                ORDER BY embedding <-> %s::vector
                LIMIT %s;
            """
            
            results = DatabaseManager.execute_query(query_sql, tuple(params), fetch="all")
            
            return [{
                "id": r[0],
                "category": r[1],
                "subcategory": r[2],
                "title": r[3],
                "content": r[4],
                "source": r[5],
                "version": r[6],
                "similarity_score": 1 - r[7]  # Convert distance to similarity
            } for r in results]
        except Exception as e:
            logger.error(f"Failed to search global standards: {e}")
            raise 