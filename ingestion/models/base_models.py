from enum import Enum
from typing import List
from datetime import datetime
from pydantic import BaseModel

"""
    [ENUM] Represents the criticality level of a query

    A query can be one of the following criticality levels:
    - EMERGENCY: Cache first + parallel live search
        eg- Check for drug interactions in ER patient
    - CRITICAL_SAFETY: Always live search
        eg- Check for recent recalls on breast cancer drug
    - TREATMENT_PLANNING: Prefer cached, live if stale
        eg- Check for standard chemotherapy protocol for lung cancer
    - BACKGROUND_RESEARCH: Cached acceptable
        eg- Check for historical survival rates for pancreatic cancer
"""
class CriticalityLevel(str, Enum):
    EMERGENCY = "emergency"           
    CRITICAL_SAFETY = "critical_safety"     
    TREATMENT_PLANNING = "treatment"  
    BACKGROUND_RESEARCH = "background"

"""
    [ENUM] Represents the type of query

    A query can be one of the following types:
    - DRUG_INTERACTIONS: Always live for safety
        eg- Check for drug interactions in a patient
    - CLINICAL_TRIALS: Live if >24h old, enrollment status changes daily.
        eg- Check for recent clinical trials for breast cancer
    - GUIDELINES: Cached if <30d old
        NCCN updates monthly, ASCO updates quarterly
        eg- Check for standard chemotherapy protocol for lung cancer
    - LITERATURE: Cached if <7d old
        eg- Check for recent literature on breast cancer treatment
    - DRUG_LABELS: Cached if <90d old
        eg- Check for recent drug labels for breast cancer
    - RARE_CONDITIONS: Always live
        eg- Check for rare conditions in breast cancer
"""
class QueryType(str, Enum):
    CLINICAL_TRIALS = "clinical_trials"  
    DRUG_INTERACTIONS = "drug_interactions"  
    DRUG_LABELS = "drug_labels" 
    GUIDELINES = "guidelines"             
    LITERATURE = "literature"              
    RARE_CONDITIONS = "rare_conditions"   

"""
    [MODEL] Represents the context of a patient

    Attributes:
        case_type (str): The type of case the patient has
        cancer_type (str): The type of cancer the patient has
        has_rare_condition (bool): Whether the patient has a rare condition
        medications (List[str]): The medications the patient is taking
        previous_treatments (List[str]): The previous treatments the patient has received
        current_treatments (List[str]): The current treatments the patient is receiving
        current_symptoms (List[str]): The current symptoms the patient is experiencing
"""
class PatientContext(BaseModel):
    case_type: str  # "emergency", "routine", "research"
    cancer_type: str
    has_rare_condition: bool
    medications: List[str]
    previous_treatments: List[str]
    current_symptoms: List[str]

"""
    [MODEL] Represents the context of a query

    Attributes:
        text (str): The text of the query
        query_type (QueryType): The type of query
        criticality (CriticalityLevel): The criticality level of the query
        patient_context (PatientContext): The context of the patient
        keywords (List[str]): The keywords in the query
        mentions_recent (bool): Whether the query mentions recent events
"""
class QueryContext(BaseModel):
    text: str
    query_type: QueryType
    criticality: CriticalityLevel
    patient_context: PatientContext
    keywords: List[str]
    mentions_recent: bool 
    
"""
    [MODEL] Represents the result of a cached query

    Attributes:
        content (str): The content of the cached result
        last_updated (datetime): The date and time the cached result was last updated
        source (str): The source of the cached result
        confidence_score (float): The confidence score of the cached result
        data_type (str): The type of data in the cached result
        relevance_score (float): The relevance score of the cached result
"""
class CachedResult(BaseModel):
    content: str
    last_updated: datetime
    source: str
    confidence_score: float
    data_type: str
    relevance_score: float

"""
    [MODEL] Represents the decision made by the smart decision engine

    Attributes:
        strategy (str): The strategy to use for the search
        reasoning (List[str]): The reasoning for the search decision
        confidence (float): The confidence in the search decision
        estimated_time (float): The estimated time to complete the search
        cost_estimate (float): The estimated cost of the search
        fallback_strategy (str): The fallback strategy to use if the search fails
"""
class SearchDecision(BaseModel):
    strategy: str  # "cache", "live", "hybrid", "parallel"
    reasoning: List[str]
    confidence: float
    estimated_time: float
    cost_estimate: float
    fallback_strategy: str 