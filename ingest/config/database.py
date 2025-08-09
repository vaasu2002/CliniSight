import psycopg2
from typing import List
from .logger import logger
from .env import DB_CONN

class DatabaseManager:
    """Manages database connections and utilities."""
    
    @staticmethod
    def get_conn():
        """Get a database connection."""
        try:
            conn = psycopg2.connect(DB_CONN)
            return conn
        except psycopg2.Error as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    @staticmethod
    def vector_to_pg_literal(vec: List[float]) -> str:
        """Convert python list to pgvector literal string."""
        return "[" + ",".join(map(lambda x: repr(float(x)), vec)) + "]"
    
    @staticmethod
    def execute_query(query: str, params: tuple = None, fetch: str = None):
        """Execute a query with proper error handling."""
        with DatabaseManager.get_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute(query, params)
                if fetch == "one":
                    result = cur.fetchone()
                elif fetch == "all":
                    result = cur.fetchall()
                else:
                    result = None
                conn.commit()
                return result
            except psycopg2.Error as e:
                conn.rollback()
                logger.error(f"Query execution failed: {e}")
                raise
            finally:
                cur.close()