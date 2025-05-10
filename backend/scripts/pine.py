import pinecone
from dotenv import load_dotenv
import os

load_dotenv()
pc = pinecone.Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("carebuddy-docs")

# Delete all vectors
index.delete(delete_all=True, namespace="medical")