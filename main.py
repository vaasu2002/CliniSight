from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import (
    global_standards,
    hospital,
    hospital_guidelines,
    patient_records,
    patients
)

app = FastAPI(
    title="CliniSight API",
    description="A comprehensive medical records and guidelines management system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(global_standards.router, prefix="/api/v1/global-standards", tags=["Global Standards"])
app.include_router(hospital.router, prefix="/api/v1/hospitals", tags=["Hospitals"])
app.include_router(hospital_guidelines.router, prefix="/api/v1/hospital-guidelines", tags=["Hospital Guidelines"])
app.include_router(patient_records.router, prefix="/api/v1/patient-records", tags=["Patient Records"])
app.include_router(patients.router, prefix="/api/v1/patients", tags=["Patients"])

@app.get("/")
async def root():
    return {"message": "Welcome to CliniSight API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 