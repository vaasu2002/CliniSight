from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Global Standards Models
class GlobalStandardCreate(BaseModel):
    category: str = Field(..., description="Category of the standard")
    title: str = Field(..., description="Title of the standard")
    content: str = Field(..., description="Content of the standard")
    subcategory: Optional[str] = Field(None, description="Subcategory of the standard")
    source: Optional[str] = Field(None, description="Source of the standard")
    version: str = Field("1.0", description="Version of the standard")

class GlobalStandardResponse(BaseModel):
    id: int
    category: str
    subcategory: Optional[str]
    title: str
    content: str
    source: Optional[str]
    version: str
    similarity_score: Optional[float] = None

# Hospital Models
class HospitalCreate(BaseModel):
    name: str = Field(..., description="Name of the hospital")
    country: Optional[str] = Field(None, description="Country of the hospital")
    region: Optional[str] = Field(None, description="Region of the hospital")

class HospitalResponse(BaseModel):
    id: int
    name: str
    country: Optional[str]
    region: Optional[str]
    created_at: datetime

# Hospital Guidelines Models
class HospitalGuidelineCreate(BaseModel):
    hospital_id: int = Field(..., description="ID of the hospital")
    category: str = Field(..., description="Category of the guideline")
    title: str = Field(..., description="Title of the guideline")
    content: str = Field(..., description="Content of the guideline")
    version: str = Field("1.0", description="Version of the guideline")
    effective_date: Optional[str] = Field(None, description="Effective date of the guideline")

class HospitalGuidelineResponse(BaseModel):
    id: int
    category: str
    title: str
    content: str
    version: str
    effective_date: Optional[str]
    similarity_score: Optional[float] = None

# Patient Models
class PatientCreate(BaseModel):
    hospital_id: int = Field(..., description="ID of the hospital")
    name: Optional[str] = Field(None, description="Name of the patient")
    date_of_birth: Optional[str] = Field(None, description="Date of birth of the patient")
    gender: Optional[str] = Field(None, description="Gender of the patient")
    patient_uuid: Optional[str] = Field(None, description="UUID of the patient")

class PatientResponse(BaseModel):
    id: int
    uuid: str
    name: Optional[str]
    date_of_birth: Optional[str]
    gender: Optional[str]
    created_at: datetime

# Patient Records Models
class PatientRecordCreate(BaseModel):
    hospital_id: int = Field(..., description="ID of the hospital")
    patient_id: int = Field(..., description="ID of the patient")
    content: str = Field(..., description="Content of the record")
    record_type: str = Field("note", description="Type of the record")
    title: Optional[str] = Field(None, description="Title of the record")
    severity: str = Field("medium", description="Severity of the record")
    created_by: Optional[str] = Field(None, description="User who created the record")

class PatientRecordResponse(BaseModel):
    id: int
    record_type: str
    title: Optional[str]
    content: str
    severity: str
    created_by: Optional[str]
    created_at: datetime
    similarity_score: Optional[float] = None

# Search Models
class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    category: Optional[str] = Field(None, description="Category filter")
    top_k: int = Field(5, description="Number of results to return")

class PatientSearchRequest(BaseModel):
    hospital_id: int = Field(..., description="ID of the hospital")
    patient_id: int = Field(..., description="ID of the patient")
    query: str = Field(..., description="Search query")
    record_type: Optional[str] = Field(None, description="Record type filter")
    top_k: int = Field(5, description="Number of results to return")

class HospitalGuidelineSearchRequest(BaseModel):
    hospital_id: int = Field(..., description="ID of the hospital")
    query: str = Field(..., description="Search query")
    category: Optional[str] = Field(None, description="Category filter")
    top_k: int = Field(5, description="Number of results to return") 