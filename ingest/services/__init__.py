"""
Services package for the ingest module.

This package contains various services for data ingestion and processing.
"""

from .embedding import EmbeddingService
from .hospital import HospitalService
from .patient import PatientService
from .global_standards import GlobalStandardsService
from .hospital_guidelines import HospitalGuidelinesService
from .patient_records import PatientRecordsService

__all__ = [
    'EmbeddingService',
    'HospitalService', 
    'PatientService',
    'GlobalStandardsService',
    'HospitalGuidelinesService',
    'PatientRecordsService'
] 