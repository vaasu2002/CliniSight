# CliniSight API

A comprehensive FastAPI application for managing medical records, hospital guidelines, and global medical standards.

## Features

- **Global Medical Standards**: Manage and search global medical standards accessible by all hospitals
- **Hospital Management**: Create and manage hospitals
- **Hospital Guidelines**: Hospital-specific guidelines with semantic search
- **Patient Management**: Create and manage patients within hospitals
- **Patient Records**: Comprehensive patient record management with semantic search
- **Semantic Search**: AI-powered search across all medical content using embeddings

## Project Structure

```
CliniSight/
├── main.py                          # FastAPI application entry point
├── api/                             # API package
│   ├── __init__.py
│   ├── models.py                    # Pydantic models for request/response schemas
│   └── routers/                     # API route handlers
│       ├── __init__.py
│       ├── global_standards.py      # Global standards endpoints
│       ├── hospital.py              # Hospital management endpoints
│       ├── hospital_guidelines.py   # Hospital guidelines endpoints
│       ├── patients.py              # Patient management endpoints
│       └── patient_records.py       # Patient records endpoints
├── ingest/                          # Core services
│   ├── services/                    # Business logic services
│   │   ├── global_standards.py
│   │   ├── hospital.py
│   │   ├── hospital_guidelines.py
│   │   ├── patient.py
│   │   ├── patient_records.py
│   │   ├── embedding.py
│   │   └── database.py
│   └── config/                      # Configuration files
└── requirements.txt                 # Python dependencies
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (create a `.env` file):
```env
DATABASE_URL=postgresql://username:password@localhost:5432/clinisight
OPENAI_API_KEY=your_openai_api_key
```

3. Run the application:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### Global Medical Standards

- `POST /api/v1/global-standards/` - Add a new global medical standard
- `POST /api/v1/global-standards/search` - Search global standards
- `GET /api/v1/global-standards/` - Get global standards with optional filtering

### Hospitals

- `POST /api/v1/hospitals/` - Create a new hospital
- `GET /api/v1/hospitals/{hospital_id}` - Get hospital details
- `GET /api/v1/hospitals/` - List hospitals with optional filtering

### Hospital Guidelines

- `POST /api/v1/hospital-guidelines/` - Add a new hospital guideline
- `POST /api/v1/hospital-guidelines/search` - Search hospital guidelines
- `GET /api/v1/hospital-guidelines/hospital/{hospital_id}` - Get guidelines for a specific hospital

### Patients

- `POST /api/v1/patients/` - Create a new patient
- `GET /api/v1/patients/{hospital_id}/{patient_id}` - Get patient details
- `GET /api/v1/patients/hospital/{hospital_id}` - List patients for a hospital

### Patient Records

- `POST /api/v1/patient-records/` - Add a new patient record
- `POST /api/v1/patient-records/search` - Search patient records
- `GET /api/v1/patient-records/{hospital_id}/{patient_id}` - Get patient records
- `GET /api/v1/patient-records/{hospital_id}/{patient_id}/{record_id}` - Get specific patient record

## API Documentation

Once the server is running, you can access:

- **Interactive API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## Example Usage

### Creating a Hospital
```bash
curl -X POST "http://localhost:8000/api/v1/hospitals/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "General Hospital",
       "country": "USA",
       "region": "California"
     }'
```

### Adding a Global Standard
```bash
curl -X POST "http://localhost:8000/api/v1/global-standards/" \
     -H "Content-Type: application/json" \
     -d '{
       "category": "Cardiology",
       "title": "Hypertension Management",
       "content": "Guidelines for managing hypertension in adults...",
       "source": "WHO",
       "version": "2.0"
     }'
```

### Creating a Patient
```bash
curl -X POST "http://localhost:8000/api/v1/patients/" \
     -H "Content-Type: application/json" \
     -d '{
       "hospital_id": 1,
       "name": "John Doe",
       "date_of_birth": "1980-01-01",
       "gender": "Male"
     }'
```

### Adding a Patient Record
```bash
curl -X POST "http://localhost:8000/api/v1/patient-records/" \
     -H "Content-Type: application/json" \
     -d '{
       "hospital_id": 1,
       "patient_id": 1,
       "content": "Patient presents with chest pain...",
       "record_type": "consultation",
       "title": "Cardiology Consultation",
       "severity": "high",
       "created_by": "Dr. Smith"
     }'
```

### Searching Patient Records
```bash
curl -X POST "http://localhost:8000/api/v1/patient-records/search" \
     -H "Content-Type: application/json" \
     -d '{
       "hospital_id": 1,
       "patient_id": 1,
       "query": "chest pain",
       "top_k": 5
     }'
```

## Security Considerations

- All endpoints include proper hospital and patient context validation
- Patient records are scoped to specific patients within hospitals
- Hospital guidelines are scoped to specific hospitals
- Global standards are accessible by all hospitals but require proper authentication

## Development

The application uses:
- **FastAPI** for the web framework
- **Pydantic** for data validation and serialization
- **PostgreSQL** with pgvector for vector similarity search
- **OpenAI** for generating embeddings
- **Uvicorn** as the ASGI server

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. 