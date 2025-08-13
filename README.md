# CliniSight API

A comprehensive FastAPI application for managing medical records, hospital guidelines, and global medical standards.

## Features

- **Global Medical Standards**: Manage and search global medical standards accessible by all hospitals
- **Hospital Management**: Create and manage hospitals
- **Hospital Guidelines**: Hospital-specific guidelines with semantic search
- **Patient Management**: Create and manage patients within hospitals
- **Patient Records**: Comprehensive patient record management with semantic search
- **Semantic Search**: AI-powered search across all medical content using embeddings

## System Architecture

The CliniSight system follows a multi-agent architecture with specialized components for data ingestion, processing, and intelligent analysis:

```mermaid
flowchart TB
  subgraph Ingest
    subgraph MCP_Fetchers
      A1[PubMed MCP]
      A2[ClinicalTrials.gov MCP]
      A3[Arxiv MCP]
    end
    A4[Institutional Guidelines]
    A5[Electronic health records]
    A6[S3 Object Storage – Medical Images & Large Files]
    A7[Freshness Cache – Last Fetch Timestamps]
  end

  subgraph Indexing
    B1[Preprocessor & Normalizer]
    B2[Embedding Service – Text & Image]
    B3[Postgres + pgvector]
    note1[Hospital data: Imaging, Test Reports, Doctor notes, Radiologist notes]
    note2[Global data: Clinial Trials, Research paper, Guideline]
  end

  subgraph API
    C1[Retrieval API – Postgres pgvector Search + S3 Links]
    C2[Query Builder]
    C3[Orchestrator – LangChain / LlamaIndex Style]
  end

  subgraph Agents
    D1[Guideline Specialist]
    D2[Research Analyst]
    D3[Patient Context Advocate]
    D4[Risk & Outcome Checker]
    D5[Devil's Advocate]
    D6[Moderator]
  end

  subgraph UI
    E1[Patient Dashboard]
    E2[Debate Transcript]
    E3[Alert Feed]
    E4[Evidence Map]
  end

  %% Freshness logic
  A7 -->|Check freshness| A1
  A7 -->|Check freshness| A2
  A7 -->|Check freshness| A3

  %% MCP to indexing
  A1 --> B1
  A2 --> B1
  A3 --> B1
  A4 --> B1
  A5 --> B1
  A6 --> B1

  %% Indexing Flow
  B1 --> B2 --> B3
  A6 --> B3

  %% Retrieval path from Indexing to Agents
  B3 --> C1 --> C3
  C3 --> D1
  C3 --> D2
  C3 --> D3
  C3 --> D4
  C3 --> D5

  %% Agents feedback loop
  D1 --> C3
  D2 --> C3
  D3 --> C3
  D4 --> C3
  D5 --> C3

  %% Moderator to UI
  C3 --> D6
  D6 --> E2
  D6 --> E4
  D6 --> E3

  %% Dashboard connection
  E1 --> D3
```

### Architecture Components

**Ingest Layer**: Handles data collection from multiple sources including PubMed, ClinicalTrials.gov, ArXiv, institutional guidelines, and electronic health records. Features intelligent freshness caching to optimize data retrieval.

**Indexing Layer**: Processes and normalizes incoming data, generates embeddings for both text and images, and stores everything in a PostgreSQL database with pgvector for similarity search.

**API Layer**: Provides retrieval services with vector search capabilities, query building, and orchestration similar to LangChain/LlamaIndex patterns.

**Agents Layer**: Multi-agent system with specialized roles:
- **Guideline Specialist**: Focuses on medical guidelines and protocols
- **Research Analyst**: Analyzes research papers and clinical trials
- **Patient Context Advocate**: Ensures patient-specific considerations
- **Risk & Outcome Checker**: Evaluates potential risks and outcomes
- **Devil's Advocate**: Provides contrarian viewpoints for balanced analysis
- **Moderator**: Orchestrates agent interactions and synthesizes results

**UI Layer**: User interfaces including patient dashboards, debate transcripts, alert feeds, and evidence mapping.

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
