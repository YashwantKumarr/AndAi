import os
from pyairtable import Api
from dotenv import load_dotenv

# Load secret variables from the .env file
load_dotenv()

PAT = os.getenv("AIRTABLE_PAT")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")

# Initialize the pyairtable API connection
api = Api(PAT)
table = api.table(BASE_ID, TABLE_NAME)

def map_record(record: dict) -> dict:
    """Helper to flatten Airtable's messy JSON into our clean Pydantic format."""
    fields = record.get("fields", {})
    return {
        "id": record.get("id"),
        "name": fields.get("Name", ""),
        "email": fields.get("email", ""),
        "department": fields.get("department", ""),
        "salary": fields.get("salary", 0)
    }