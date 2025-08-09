import os
import openai

DB_CONN = os.getenv("DB_CONN", "postgresql://postgres:password@localhost:5432/hospitaldb")
EMBED_DIM = 1536  # OpenAI text-embedding-3-small dimension
EMBEDDING_MODEL = "text-embedding-3-small"

# OpenAI API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")

# Configure OpenAI client
openai.api_key = OPENAI_API_KEY