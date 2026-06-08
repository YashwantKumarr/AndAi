from fastapi import FastAPI, HTTPException
from typing import List
import airtable_service as db
from models import EmployeeCreate, EmployeeUpdate, EmployeeResponse

# Initialize your FastAPI application
app = FastAPI(title="Airtable CRUD API")

# ==========================================
# 1. CREATE (POST)
# ==========================================
@app.post("/employees/", response_model=EmployeeResponse)
async def create_employee(employee: EmployeeCreate):
    """Adds a brand new employee to the Airtable database."""
    try:
        # Map our Pydantic model exactly to the Airtable column names
        fields = {
            "Name": employee.name,
            "email": employee.email,
            "department": employee.department,
            "salary": employee.salary
        }
        record = db.table.create(fields)
        return db.map_record(record)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==========================================
# 2. READ ALL (GET)
# ==========================================
@app.get("/employees/", response_model=List[EmployeeResponse])
async def get_all_employees():
    """Retrieves every single employee in the database."""
    try:
        records = db.table.all()
        return [db.map_record(r) for r in records]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==========================================
# 3. SEARCH / FILTER (GET with Query Parameter)
# ==========================================
@app.get("/employees/search/", response_model=List[EmployeeResponse])
async def search_employees(department: str):
    """Returns only employees that match a specific department."""
    try:
        # Create the Airtable formula: {department} = 'Engineering'
        search_formula = f"{{department}} = '{department}'"
        records = db.table.all(formula=search_formula)
        return [db.map_record(r) for r in records]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==========================================
# 4. READ ONE (GET with Path Parameter)
# ==========================================
@app.get("/employees/{record_id}", response_model=EmployeeResponse)
async def get_employee(record_id: str):
    """Retrieves exactly one employee using their unique rec... ID."""
    try:
        record = db.table.get(record_id)
        return db.map_record(record)
    except Exception:
        raise HTTPException(status_code=404, detail="Employee not found")

# ==========================================
# 5. UPDATE (PUT)
# ==========================================
@app.put("/employees/{record_id}", response_model=EmployeeResponse)
async def update_employee(record_id: str, employee: EmployeeUpdate):
    """Updates specific fields of an existing employee."""
    try:
        update_fields = {}
        # Only attach fields to the update if the user actually provided them
        if employee.name: update_fields["Name"] = employee.name
        if employee.email: update_fields["email"] = employee.email
        if employee.department: update_fields["department"] = employee.department
        if employee.salary: update_fields["salary"] = employee.salary

        record = db.table.update(record_id, update_fields)
        return db.map_record(record)
    except Exception:
        raise HTTPException(status_code=404, detail="Employee not found or update failed")

# ==========================================
# 6. DELETE (DELETE)
# ==========================================
@app.delete("/employees/{record_id}")
async def delete_employee(record_id: str):
    """Permanently removes an employee from the database."""
    try:
        db.table.delete(record_id)
        return {"status": "success", "message": f"Record {record_id} deleted"}
    except Exception:
        raise HTTPException(status_code=404, detail="Employee not found")