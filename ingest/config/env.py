import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
DB_CONN = os.getenv("DB_CONN", "postgresql://postgres:password@localhost:5432/hospitaldb")
EMBED_DIM = 1536  # OpenAI text-embedding-3-small dimension
EMBEDDING_MODEL = "text-embedding-3-small"

