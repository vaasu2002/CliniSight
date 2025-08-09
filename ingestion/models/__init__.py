"""
    [PACKAGE] Ingestion Models

    This package contains all the data models and decision logic for the intelligent
    search and caching system.
"""

from .base_models import (
    CriticalityLevel,
    QueryType,
    PatientContext,
    QueryContext,
    CachedResult,
    SearchDecision
)

__all__ = [
    # Base models
    "CriticalityLevel",
    "QueryType", 
    "PatientContext",
    "QueryContext",
    "CachedResult",
    "SearchDecision",
] 