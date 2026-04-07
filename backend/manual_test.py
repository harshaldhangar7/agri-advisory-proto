#!/usr/bin/env python
"""
Manual Test Script for Agri Advisory API - Direct Backend Testing

This script performs manual API testing against a running backend instance.
It tests all major functionality without requiring pytest.

Usage:
    python manual_test.py http://localhost:8000

Prerequisites:
    - Backend running: python -m uvicorn app.main:app --reload
    - MySQL database initialized
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
API_KEY = "default-dev-key"
BASE_URL = "http://localhost:8000"

# ANSI Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_section(title):
    """Print a section header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{title:^70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")

def print_test(name, passed, message=""):
    """Print test result"""
    status = f"{Colors.GREEN}✓ PASS{Colors.ENDC}" if passed else f"{Colors.RED}✗ FAIL{Colors.ENDC}"
    print(f"{status} | {name}")
    if message:
        print(f"  {Colors.YELLOW}→ {message}{Colors.ENDC}")

def test_health_check():
    """Test 1: Health check endpoint"""
    print_section("1. HEALTH CHECK TEST")
    try:
        response = requests.get(f"{BASE_URL}/health")
        passed = response.status_code == 200 and response.json()["status"] == "ok"
        print_test("Health check endpoint", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("Health check endpoint", False, f"Error: {e}")
        return False

def test_authentication():
    """Test 2: API Key authentication"""
    print_section("2. AUTHENTICATION TESTS")
    tests_passed = []
    
    # Test 1: Missing API key
    try:
        response = requests.get(f"{BASE_URL}/api/farmers/")
        passed = response.status_code == 401
        print_test("Missing API key rejection", passed, f"Status: {response.status_code}")
        tests_passed.append(passed)
    except Exception as e:
        print_test("Missing API key rejection", False, f"Error: {e}")
        tests_passed.append(False)
    
    # Test 2: Invalid API key
    try:
        headers = {"x-api-key": "wrong-key"}
        response = requests.get(f"{BASE_URL}/api/farmers/", headers=headers)
        passed = response.status_code == 403
        print_test("Invalid API key rejection", passed, f"Status: {response.status_code}")
        tests_passed.append(passed)
    except Exception as e:
        print_test("Invalid API key rejection", False, f"Error: {e}")
        tests_passed.append(False)
    
    # Test 3: Valid API key
    try:
        headers = {"x-api-key": API_KEY}
        response = requests.get(f"{BASE_URL}/api/farmers/", headers=headers)
        passed = response.status_code == 200
        print_test("Valid API key acceptance", passed, f"Status: {response.status_code}")
        tests_passed.append(passed)
    except Exception as e:
        print_test("Valid API key acceptance", False, f"Error: {e}")
        tests_passed.append(False)
    
    return all(tests_passed)

def test_farmer_crud():
    """Test 3: Farmer CRUD operations"""
    print_section("3. FARMER CRUD TESTS")
    headers = {"x-api-key": API_KEY}
    tests_passed = []
    farmer_id = None
    
    # Create farmer
    try:
        payload = {
            "name": f"Test Farmer {datetime.now().strftime('%H%M%S')}",
            "phone": "9876543210",
            "language": "mr"
        }
        response = requests.post(f"{BASE_URL}/api/farmers/", json=payload, headers=headers)
        passed = response.status_code == 200
        if passed:
            farmer_id = response.json()["id"]
            print_test("Create farmer", passed, f"Farmer ID: {farmer_id}")
        else:
            print_test("Create farmer", False, f"Status: {response.status_code}, {response.text}")
        tests_passed.append(passed)
    except Exception as e:
        print_test("Create farmer", False, f"Error: {e}")
        tests_passed.append(False)
        return False  # Can't continue without farmer
    
    # List farmers
    try:
        response = requests.get(f"{BASE_URL}/api/farmers/", headers=headers)
        passed = response.status_code == 200 and isinstance(response.json(), list)
        count = len(response.json()) if passed else 0
        print_test("List farmers", passed, f"Found {count} farmers")
        tests_passed.append(passed)
    except Exception as e:
        print_test("List farmers", False, f"Error: {e}")
        tests_passed.append(False)
    
    # Get farmer details
    if farmer_id:
        try:
            response = requests.get(f"{BASE_URL}/api/farmers/{farmer_id}", headers=headers)
            passed = response.status_code == 200
            print_test("Get farmer details", passed, f"Status: {response.status_code}")
            tests_passed.append(passed)
        except Exception as e:
            print_test("Get farmer details", False, f"Error: {e}")
            tests_passed.append(False)
    
    # Update farmer
    if farmer_id:
        try:
            payload = {"name": "Updated Test Farmer"}
            response = requests.put(f"{BASE_URL}/api/farmers/{farmer_id}", json=payload, headers=headers)
            passed = response.status_code == 200
            print_test("Update farmer name", passed, f"Status: {response.status_code}")
            tests_passed.append(passed)
        except Exception as e:
            print_test("Update farmer name", False, f"Error: {e}")
            tests_passed.append(False)
    
    # Delete farmer
    if farmer_id:
        try:
            response = requests.delete(f"{BASE_URL}/api/farmers/{farmer_id}", headers=headers)
            passed = response.status_code == 200
            print_test("Delete farmer", passed, f"Status: {response.status_code}")
            tests_passed.append(passed)
        except Exception as e:
            print_test("Delete farmer", False, f"Error: {e}")
            tests_passed.append(False)
    
    return all(tests_passed)

def test_plot_management():
    """Test 4: Plot operations"""
    print_section("4. PLOT MANAGEMENT TESTS")
    headers = {"x-api-key": API_KEY}
    tests_passed = []
    
    # Create farmer first
    try:
        payload = {
            "name": f"Plot Test Farmer {datetime.now().strftime('%H%M%S')}",
            "phone": "1234567890"
        }
        response = requests.post(f"{BASE_URL}/api/farmers/", json=payload, headers=headers)
        farmer_id = response.json()["id"]
    except Exception as e:
        print_test("Setup: Create test farmer", False, f"Error: {e}")
        return False
    
    # Add plot
    plot_id = None
    try:
        payload = {
            "name": "Test Field",
            "crop": "wheat",
            "area_hectares": 5.5
        }
        response = requests.post(f"{BASE_URL}/api/farmers/{farmer_id}/plots", json=payload, headers=headers)
        passed = response.status_code == 200
        if passed:
            plot_id = response.json()["id"]
            print_test("Add plot to farmer", passed, f"Plot ID: {plot_id}")
        else:
            print_test("Add plot to farmer", False, f"Status: {response.status_code}")
        tests_passed.append(passed)
    except Exception as e:
        print_test("Add plot to farmer", False, f"Error: {e}")
        tests_passed.append(False)
    
    # Get farmer plots
    try:
        response = requests.get(f"{BASE_URL}/api/farmers/{farmer_id}/plots", headers=headers)
        passed = response.status_code == 200 and isinstance(response.json(), list)
        count = len(response.json()) if passed else 0
        print_test("Get farmer plots", passed, f"Found {count} plots")
        tests_passed.append(passed)
    except Exception as e:
        print_test("Get farmer plots", False, f"Error: {e}")
        tests_passed.append(False)
    
    # Delete plot
    if plot_id and farmer_id:
        try:
            response = requests.delete(
                f"{BASE_URL}/api/farmers/{farmer_id}/plots/{plot_id}",
                headers=headers
            )
            passed = response.status_code == 200
            print_test("Delete plot", passed, f"Status: {response.status_code}")
            tests_passed.append(passed)
        except Exception as e:
            print_test("Delete plot", False, f"Error: {e}")
            tests_passed.append(False)
    
    # Cleanup: Delete farmer
    try:
        requests.delete(f"{BASE_URL}/api/farmers/{farmer_id}", headers=headers)
    except:
        pass
    
    return all(tests_passed)

def test_advisory():
    """Test 5: Advisory system"""
    print_section("5. ADVISORY SYSTEM TESTS")
    headers = {"x-api-key": API_KEY}
    tests_passed = []
    
    # Create farmer and plot
    try:
        farmer_payload = {
            "name": f"Advisory Test Farmer {datetime.now().strftime('%H%M%S')}",
            "phone": "1234567890"
        }
        farmer_response = requests.post(f"{BASE_URL}/api/farmers/", json=farmer_payload, headers=headers)
        farmer_id = farmer_response.json()["id"]
        
        plot_payload = {
            "name": "Test Field",
            "crop": "wheat",
            "area_hectares": 5
        }
        plot_response = requests.post(
            f"{BASE_URL}/api/farmers/{farmer_id}/plots",
            json=plot_payload,
            headers=headers
        )
        plot_id = plot_response.json()["id"]
    except Exception as e:
        print_test("Setup: Create test farmer and plot", False, f"Error: {e}")
        return False
    
    # Get advisory without symptoms
    try:
        payload = {
            "plot_id": plot_id,
            "weather": {"rain_last_3_days": 0}
        }
        response = requests.post(f"{BASE_URL}/api/advisory/recommend", json=payload, headers=headers)
        passed = response.status_code == 200 and "advice" in response.json()
        advice_count = len(response.json().get("advice", [])) if passed else 0
        print_test("Get advisory (no symptoms)", passed, f"Generated {advice_count} advice items")
        tests_passed.append(passed)
    except Exception as e:
        print_test("Get advisory (no symptoms)", False, f"Error: {e}")
        tests_passed.append(False)
    
    # Get advisory with symptoms
    try:
        payload = {
            "plot_id": plot_id,
            "symptoms": "yellow leaves on the crop",
            "weather": {"rain_last_3_days": 5}
        }
        response = requests.post(f"{BASE_URL}/api/advisory/recommend", json=payload, headers=headers)
        passed = response.status_code == 200 and "advice" in response.json()
        advice_count = len(response.json().get("advice", [])) if passed else 0
        print_test("Get advisory (with symptoms)", passed, f"Generated {advice_count} advice items")
        tests_passed.append(passed)
    except Exception as e:
        print_test("Get advisory (with symptoms)", False, f"Error: {e}")
        tests_passed.append(False)
    
    # Test advisory with invalid plot
    try:
        payload = {
            "plot_id": "fake-plot-id-123",
            "symptoms": "test"
        }
        response = requests.post(f"{BASE_URL}/api/advisory/recommend", json=payload, headers=headers)
        passed = response.status_code == 404
        print_test("Advisory rejects invalid plot", passed, f"Status: {response.status_code}")
        tests_passed.append(passed)
    except Exception as e:
        print_test("Advisory rejects invalid plot", False, f"Error: {e}")
        tests_passed.append(False)
    
    # Cleanup
    try:
        requests.delete(f"{BASE_URL}/api/farmers/{farmer_id}", headers=headers)
    except:
        pass
    
    return all(tests_passed)

def test_validation():
    """Test 6: Input validation"""
    print_section("6. INPUT VALIDATION TESTS")
    headers = {"x-api-key": API_KEY}
    tests_passed = []
    
    # Test: Empty name rejected
    try:
        payload = {"name": "", "phone": "123"}
        response = requests.post(f"{BASE_URL}/api/farmers/", json=payload, headers=headers)
        passed = response.status_code == 422
        print_test("Reject empty farmer name", passed, f"Status: {response.status_code}")
        tests_passed.append(passed)
    except Exception as e:
        print_test("Reject empty farmer name", False, f"Error: {e}")
        tests_passed.append(False)
    
    # Test: Name too long rejected
    try:
        payload = {"name": "x" * 101, "phone": "123"}
        response = requests.post(f"{BASE_URL}/api/farmers/", json=payload, headers=headers)
        passed = response.status_code == 422
        print_test("Reject overly long name", passed, f"Status: {response.status_code}")
        tests_passed.append(passed)
    except Exception as e:
        print_test("Reject overly long name", False, f"Error: {e}")
        tests_passed.append(False)
    
    #  Test: Whitespace trimming
    try:
        payload = {"name": "  Test Farmer  ", "phone": "123"}
        response = requests.post(f"{BASE_URL}/api/farmers/", json=payload, headers=headers)
        passed = response.status_code == 200 and response.json()["name"] == "Test Farmer"
        print_test("Trim whitespace from names", passed, f"Name trimmed: {passed}")
        if passed:
            # Cleanup
            requests.delete(f"{BASE_URL}/api/farmers/{response.json()['id']}", headers=headers)
        tests_passed.append(passed)
    except Exception as e:
        print_test("Trim whitespace from names", False, f"Error: {e}")
        tests_passed.append(False)
    
    return all(tests_passed)

def main():
    """Run all tests"""
    print(f"""{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║      🧪 AGRI ADVISORY API - MANUAL TEST SUITE                   ║
║                                                                  ║
║      Testing against: {BASE_URL:<44}║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    {Colors.ENDC}""")
    
    # Check backend connectivity
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        print(f"{Colors.GREEN}✓ Backend is accessible{Colors.ENDC}\n")
    except Exception as e:
        print(f"{Colors.RED}✗ Cannot connect to backend at {BASE_URL}{Colors.ENDC}")
        print(f"{Colors.RED}Error: {e}{Colors.ENDC}")
        print(f"\n{Colors.YELLOW}Make sure backend is running:{Colors.ENDC}")
        print(f"  cd backend && python -m uvicorn app.main:app --reload\n")
        return False
    
    # Run test suites
    results = {}
    results["Health Check"] = test_health_check()
    results["Authentication"] = test_authentication()
    results["Farmer CRUD"] = test_farmer_crud()
    results["Plot Management"] = test_plot_management()
    results["Advisory System"] = test_advisory()
    results["Input Validation"] = test_validation()
    
    # Print summary
    print_section("TEST SUMMARY")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = f"{Colors.GREEN}✓ PASS{Colors.ENDC}" if result else f"{Colors.RED}✗ FAIL{Colors.ENDC}"
        print(f"{status} | {name}")
    
    print(f"\n{Colors.BOLD}Results: {Colors.GREEN}{passed} passed{Colors.ENDC}, {Colors.RED}{total - passed} failed{Colors.ENDC}{Colors.ENDC}")
    print(f"Overall: {'🎉 ALL TESTS PASSED' if passed == total else '⚠️  SOME TESTS FAILED'}\n")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
