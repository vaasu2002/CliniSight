import psycopg2.sql as sql
from ..config.database import DatabaseManager
from ..config.env import EMBED_DIM
from ..config.logger import logger

"""
[CLASS] DatabaseService
[DESCRIPTION] Handles database schema creation and management.
[METHODS]
    - init_database: Initializes the complete database schema.
    - _create_hospitals_table: Creates the hospitals table.
    - _create_patients_table: Creates the patients table.
    - _create_global_standards_table: Creates the global medical standards table.
    - _create_hospital_guidelines_table: Creates the hospital guidelines table.
    - _create_patient_records_table: Creates the patient records table.
    - _create_audit_log_table: Creates the audit log table.
    - _setup_rls_policies: Sets up the row level security policies.
"""
class DatabaseService:
    
    """
    [METHOD] init_database
    [DESCRIPTION] Initializes the complete database schema.
    [PARAMETERS] None
    [RETURN] None
    """
    @staticmethod
    def init_database():
        logger.info("Initializing database schema...")
        
        with DatabaseManager.get_conn() as conn:
            cur = conn.cursor()
            
            # Enable extensions
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            cur.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
            conn.commit()
            
            # Create tables
            DatabaseService._create_hospitals_table(cur)
            DatabaseService._create_patients_table(cur)
            DatabaseService._create_global_standards_table(cur)
            DatabaseService._create_hospital_guidelines_table(cur)
            DatabaseService._create_patient_records_table(cur)
            DatabaseService._create_audit_log_table(cur)
            
            # Setup RLS
            DatabaseService._setup_rls_policies(cur)
            
            conn.commit()
            cur.close()
            
        logger.info("✅ Database schema initialized successfully")
    
    """
    [METHOD] _create_hospitals_table
    [DESCRIPTION] Creates the hospitals table.
    [PARAMETERS] cur: The database cursor.
    [RETURN] None
    """
    @staticmethod
    def _create_hospitals_table(cur):
        """Create hospitals table."""
        cur.execute("""
        CREATE TABLE IF NOT EXISTS hospitals (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            country TEXT,
            region TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
        );
        """)
    
    """
    [METHOD] _create_patients_table
    [DESCRIPTION] Creates the patients table.
    [PARAMETERS] cur: The database cursor.
    [RETURN] None
    """
    @staticmethod
    def _create_patients_table(cur):
        """Create patients table."""
        cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id SERIAL PRIMARY KEY,
            hospital_id INT NOT NULL REFERENCES hospitals(id) ON DELETE CASCADE,
            patient_uuid UUID NOT NULL DEFAULT uuid_generate_v4(),
            name TEXT,
            date_of_birth DATE,
            gender TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
            UNIQUE(hospital_id, patient_uuid)
        );
        """)
    
    """
    [METHOD] _create_global_standards_table
    [DESCRIPTION] Creates the global medical standards table.
    [PARAMETERS] cur: The database cursor.
    [RETURN] None
    """
    @staticmethod
    def _create_global_standards_table(cur):
        """Create global medical standards table (no RLS)."""
        cur.execute(sql.SQL("""
        CREATE TABLE IF NOT EXISTS global_medical_standards (
            id SERIAL PRIMARY KEY,
            category TEXT NOT NULL,
            subcategory TEXT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            source TEXT,
            version TEXT,
            embedding vector({dim}) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
        );
        """).format(dim=sql.Literal(EMBED_DIM)))
    
    """
    [METHOD] _create_hospital_guidelines_table
    [DESCRIPTION] Creates the hospital guidelines table.
    [PARAMETERS] cur: The database cursor.
    [RETURN] None
    """
    @staticmethod
    def _create_hospital_guidelines_table(cur):
        """Create hospital guidelines table with RLS."""
        cur.execute(sql.SQL("""
        CREATE TABLE IF NOT EXISTS hospital_guidelines (
            id SERIAL PRIMARY KEY,
            hospital_id INT NOT NULL REFERENCES hospitals(id) ON DELETE CASCADE,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            version TEXT DEFAULT '1.0',
            effective_date DATE DEFAULT CURRENT_DATE,
            embedding vector({dim}) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
        );
        """).format(dim=sql.Literal(EMBED_DIM)))
    
    """
    [METHOD] _create_patient_records_table
    [DESCRIPTION] Creates the patient records table.
    [PARAMETERS] cur: The database cursor.
    [RETURN] None
    """
    @staticmethod
    def _create_patient_records_table(cur):
        """Create patient records table with strict RLS."""
        cur.execute(sql.SQL("""
        CREATE TABLE IF NOT EXISTS patient_records (
            id SERIAL PRIMARY KEY,
            hospital_id INT NOT NULL REFERENCES hospitals(id) ON DELETE CASCADE,
            patient_id INT NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
            record_type TEXT NOT NULL DEFAULT 'note',
            title TEXT,
            content TEXT NOT NULL,
            severity TEXT CHECK (severity IN ('low', 'medium', 'high', 'critical')),
            embedding vector({dim}) NOT NULL,
            created_by TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
        );
        """).format(dim=sql.Literal(EMBED_DIM)))
    
    """
    [METHOD] _create_audit_log_table
    [DESCRIPTION] Creates the audit log table.
    [PARAMETERS] cur: The database cursor.
    [RETURN] None
    """
    @staticmethod
    def _create_audit_log_table(cur):
        """Create comprehensive audit log table."""
        cur.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id SERIAL PRIMARY KEY,
            hospital_id INT,
            patient_id INT,
            user_id TEXT,
            user_role TEXT,
            action TEXT NOT NULL,
            table_name TEXT NOT NULL,
            record_id INT,
            details JSONB,
            ip_address INET,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
        );
        """)
    
    """
    [METHOD] _setup_rls_policies
    [DESCRIPTION] Sets up the row level security policies.
    [PARAMETERS] cur: The database cursor.
    [RETURN] None
    """
    @staticmethod
    def _setup_rls_policies(cur):
        """Setup Row Level Security policies."""
        # Enable RLS on protected tables
        cur.execute("ALTER TABLE hospital_guidelines ENABLE ROW LEVEL SECURITY;")
        cur.execute("ALTER TABLE patient_records ENABLE ROW LEVEL SECURITY;")
        
        # Hospital guidelines policy
        cur.execute("""
        DO $$
        BEGIN
          DROP POLICY IF EXISTS hospital_guideline_isolation ON hospital_guidelines;
          CREATE POLICY hospital_guideline_isolation ON hospital_guidelines
            FOR ALL USING (hospital_id = current_setting('app.current_hospital_id')::int);
        END$$;
        """)
        
        # Patient records policy (very strict - requires both contexts)
        cur.execute("""
        DO $$
        BEGIN
          DROP POLICY IF EXISTS patient_record_isolation ON patient_records;
          CREATE POLICY patient_record_isolation ON patient_records
            FOR ALL USING (
              hospital_id = current_setting('app.current_hospital_id')::int
              AND patient_id = current_setting('app.current_patient_id')::int
            );
        END$$;
        """)