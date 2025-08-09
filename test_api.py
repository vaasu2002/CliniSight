#!/usr/bin/env python3
"""
CliniSight API Test Script

This script tests the basic functionality of the API endpoints.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    """Test the health endpoint."""
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Health check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_create_hospital():
    """Test creating a hospital."""
    data = {
        "name": "Test Hospital",
        "country": "USA",
        "region": "California"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/hospitals/", json=data)
        print(f"Create hospital: {response.status_code}")
        if response.status_code == 201:
            result = response.json()
            print(f"Hospital created with ID: {result.get('id')}")
            return result.get('id')
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Create hospital failed: {e}")
        return None

def test_create_patient(hospital_id):
    """Test creating a patient."""
    data = {
        "hospital_id": hospital_id,
        "name": "John Doe",
        "date_of_birth": "1980-01-01",
        "gender": "Male"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/patients/", json=data)
        print(f"Create patient: {response.status_code}")
        if response.status_code == 201:
            result = response.json()
            print(f"Patient created with ID: {result.get('id')}")
            return result.get('id')
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Create patient failed: {e}")
        return None

def test_add_global_standard():
    """Test adding a global standard."""
    data = {
        "category": "Cardiology",
        "title": "Hypertension Management",
        "content": "Guidelines for managing hypertension in adults. Regular monitoring of blood pressure is essential.",
        "source": "WHO",
        "version": "2.0"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/global-standards/", json=data)
        print(f"Add global standard: {response.status_code}")
        if response.status_code == 201:
            result = response.json()
            print(f"Global standard created with ID: {result.get('id')}")
            return result.get('id')
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Add global standard failed: {e}")
        return None

def test_search_global_standards():
    """Test searching global standards."""
    data = {
        "query": "hypertension",
        "top_k": 5
    }
    
    try:
        response = requests.post(f"{BASE_URL}/global-standards/search", json=data)
        print(f"Search global standards: {response.status_code}")
        if response.status_code == 200:
            results = response.json()
            print(f"Found {len(results)} results")
            for result in results:
                print(f"- {result.get('title')} (Score: {result.get('similarity_score', 'N/A')})")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Search global standards failed: {e}")
        return False

def test_add_patient_record(hospital_id, patient_id):
    """Test adding a patient record."""
    data = {
        "hospital_id": hospital_id,
        "patient_id": patient_id,
        "content": "Patient presents with chest pain and shortness of breath. Blood pressure elevated at 160/100.",
        "record_type": "consultation",
        "title": "Cardiology Consultation",
        "severity": "high",
        "created_by": "Dr. Smith"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/patient-records/", json=data)
        print(f"Add patient record: {response.status_code}")
        if response.status_code == 201:
            result = response.json()
            print(f"Patient record created with ID: {result.get('id')}")
            return result.get('id')
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Add patient record failed: {e}")
        return None

def test_search_patient_records(hospital_id, patient_id):
    """Test searching patient records."""
    data = {
        "hospital_id": hospital_id,
        "patient_id": patient_id,
        "query": "chest pain",
        "top_k": 5
    }
    
    try:
        response = requests.post(f"{BASE_URL}/patient-records/search", json=data)
        print(f"Search patient records: {response.status_code}")
        if response.status_code == 200:
            results = response.json()
            print(f"Found {len(results)} results")
            for result in results:
                print(f"- {result.get('title')} (Score: {result.get('similarity_score', 'N/A')})")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Search patient records failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Starting CliniSight API Tests")
    print("=" * 50)
    
    # Test health endpoint
    if not test_health():
        print("Health check failed. Make sure the API is running.")
        return
    
    print("\n" + "=" * 50)
    
    # Test hospital creation
    hospital_id = test_create_hospital()
    if not hospital_id:
        print("Hospital creation failed. Stopping tests.")
        return
    
    print("\n" + "=" * 50)
    
    # Test patient creation
    patient_id = test_create_patient(hospital_id)
    if not patient_id:
        print("Patient creation failed. Stopping tests.")
        return
    
    print("\n" + "=" * 50)
    
    # Test global standards
    standard_id = test_add_global_standard()
    if standard_id:
        test_search_global_standards()
    
    print("\n" + "=" * 50)
    
    # Test patient records
    record_id = test_add_patient_record(hospital_id, patient_id)
    if record_id:
        test_search_patient_records(hospital_id, patient_id)
    
    print("\n" + "=" * 50)
    print("All tests completed!")

if __name__ == "__main__":
    main() 