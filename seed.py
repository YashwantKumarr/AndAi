import json
import requests
import time

# The URL of your local FastAPI server
API_URL = "http://127.0.0.1:8000/employees/"

def seed_database():
    print("Loading test data...")
    with open("test_data.json", "r") as file:
        employees = json.load(file)
    
    print(f"Found {len(employees)} employees. Starting upload...")
    
    success_count = 0
    for emp in employees:
        # Send the POST request to your FastAPI server
        response = requests.post(API_URL, json=emp)
        
        if response.status_code == 200:
            print(f"✅ Successfully added: {emp['name']}")
            success_count += 1
        else:
            print(f"❌ Failed to add {emp['name']}: {response.text}")
            
        # Pause for half a second so Airtable doesn't block us for spamming
        time.sleep(0.5)
        
    print(f"\nSeeding complete! Added {success_count}/{len(employees)} records.")

if __name__ == "__main__":
    seed_database()