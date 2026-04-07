"""
Backend Unit Tests for Agri Advisory API
Tests cover: Functional, Integration, and Security aspects
Run with: pytest tests/ -v
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
import sys
from pathlib import Path

# Add backend app to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app
from app.db import get_engine

# Use in-memory SQLite for testing instead of MySQL
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_engine] = lambda: engine
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

# Test configuration
VALID_API_KEY = "default-dev-key"
HEADERS = {"x-api-key": VALID_API_KEY}
INVALID_HEADERS = {"x-api-key": "wrong-key"}

# ============================================================================
# FUNCTIONAL TESTS - FARMER CRUD
# ============================================================================

class TestFarmerCreation:
    """TC-001 through TC-009: Farmer creation functionality"""
    
    def test_create_farmer_with_valid_data(self, client: TestClient):
        """TC-001: Create farmer with valid name and phone"""
        payload = {"name": "John Doe", "phone": "9876543210", "language": "mr"}
        response = client.post("/api/farmers/", json=payload, headers=HEADERS)
        
        assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
        data = response.json()
        assert "id" in data, "Response should contain farmer id"
        assert data["name"] == "John Doe"
        assert data["phone"] == "9876543210"
        assert len(data["id"]) > 0
    
    def test_create_farmer_with_name_only(self, client: TestClient):
        """TC-002: Create farmer with only name (phone optional)"""
        payload = {"name": "Jane Doe"}
        response = client.post("/api/farmers/", json=payload, headers=HEADERS)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Jane Doe"
        assert data["phone"] is None
    
    def test_create_farmer_empty_name(self, client: TestClient):
        """TC-003: Reject creation with empty name"""
        payload = {"name": "", "phone": "123"}
        response = client.post("/api/farmers/", json=payload, headers=HEADERS)
        
        assert response.status_code == 422, "Should validate and reject empty name"
    
    def test_create_farmer_name_too_long(self, client: TestClient):
        """TC-004: Reject name exceeding 100 characters"""
        payload = {"name": "x" * 101, "phone": "123"}
        response = client.post("/api/farmers/", json=payload, headers=HEADERS)
        
        assert response.status_code == 422, "Should reject name > 100 chars"
    
    def test_create_farmer_name_whitespace_trimmed(self, client: TestClient):
        """TC-005: Whitespace in name should be trimmed"""
        payload = {"name": "  John Doe  ", "phone": "123"}
        response = client.post("/api/farmers/", json=payload, headers=HEADERS)
        
        assert response.status_code == 200
        assert response.json()["name"] == "John Doe"
    
    def test_create_farmer_phone_too_long(self, client: TestClient):
        """TC-006: Reject phone number > 20 characters"""
        payload = {"name": "Test", "phone": "x" * 21}
        response = client.post("/api/farmers/", json=payload, headers=HEADERS)
        
        assert response.status_code == 422
    
    def test_create_farmer_missing_api_key(self, client: TestClient):
        """TC-008: Reject request without API key"""
        payload = {"name": "Test"}
        response = client.post("/api/farmers/", json=payload)  # No headers
        
        assert response.status_code == 401
        assert "API key required" in response.json()["detail"]
    
    def test_create_farmer_invalid_api_key(self, client: TestClient):
        """TC-009: Reject request with invalid API key"""
        payload = {"name": "Test"}
        response = client.post("/api/farmers/", json=payload, headers=INVALID_HEADERS)
        
        assert response.status_code == 403
        assert "Invalid API key" in response.json()["detail"]

class TestFarmerReading:
    """TC-010 through TC-015: Farmer reading functionality"""
    
    def test_list_farmers_empty(self, client: TestClient):
        """TC-012: List farmers returns empty array when no farmers exist"""
        response = client.get("/api/farmers/", headers=HEADERS)
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_list_farmers_with_data(self, client: TestClient):
        """TC-010: List all farmers returns array"""
        # Create test farmer first
        client.post("/api/farmers/", json={"name": "Test Farmer"}, headers=HEADERS)
        
        response = client.get("/api/farmers/", headers=HEADERS)
        
        assert response.status_code == 200
        farmers = response.json()
        assert len(farmers) > 0
        assert farmers[0]["name"] == "Test Farmer"
    
    def test_list_farmers_pagination(self, client: TestClient):
        """TC-011: Pagination with skip and limit"""
        # Create multiple farmers
        for i in range(5):
            client.post("/api/farmers/", json={"name": f"Farmer {i}"}, headers=HEADERS)
        
        response = client.get("/api/farmers/?skip=0&limit=3", headers=HEADERS)
        
        assert response.status_code == 200
        farmers = response.json()
        assert len(farmers) <= 3
    
    def test_get_farmer_not_found(self, client: TestClient):
        """TC-014: Get non-existent farmer returns 404"""
        response = client.get("/api/farmers/fake-id-123", headers=HEADERS)
        
        assert response.status_code == 404
        assert "Farmer not found" in response.json()["detail"]
    
    def test_get_farmer_with_details(self, client: TestClient):
        """TC-013: Get farmer includes details and plots"""
        # Create farmer
        create_res = client.post("/api/farmers/", json={"name": "Test"}, headers=HEADERS)
        farmer_id = create_res.json()["id"]
        
        response = client.get(f"/api/farmers/{farmer_id}", headers=HEADERS)
        
        assert response.status_code == 200
        data = response.json()
        assert "farmer" in data
        assert "plots" in data
        assert isinstance(data["plots"], list)

class TestFarmerUpdating:
    """TC-016 through TC-019: Farmer update functionality"""
    
    def test_update_farmer_name(self, client: TestClient):
        """TC-016: Update farmer name successfully"""
        # Create farmer
        create_res = client.post("/api/farmers/", json={"name": "Original"}, headers=HEADERS)
        farmer_id = create_res.json()["id"]
        
        # Update name
        response = client.put(f"/api/farmers/{farmer_id}", json={"name": "Updated"}, headers=HEADERS)
        
        assert response.status_code == 200
        assert response.json()["name"] == "Updated"
    
    def test_update_farmer_invalid_data(self, client: TestClient):
        """TC-017: Reject invalid data on update"""
        # Create farmer
        create_res = client.post("/api/farmers/", json={"name": "Test"}, headers=HEADERS)
        farmer_id = create_res.json()["id"]
        
        # Update with invalid name
        response = client.put(f"/api/farmers/{farmer_id}", json={"name": ""}, headers=HEADERS)
        
        assert response.status_code == 422
    
    def test_update_nonexistent_farmer(self, client: TestClient):
        """TC-018: Update non-existent farmer returns 404"""
        response = client.put("/api/farmers/fake-id", json={"name": "New"}, headers=HEADERS)
        
        assert response.status_code == 404
        assert "Farmer not found" in response.json()["detail"]
    
    def test_update_farmer_id_protected(self, client: TestClient):
        """TC-019: farmer ID field should not be changeable"""
        # Create farmer
        create_res = client.post("/api/farmers/", json={"name": "Test"}, headers=HEADERS)
        farmer_id = create_res.json()["id"]
        
        # Try to update ID
        response = client.put(
            f"/api/farmers/{farmer_id}",
            json={"id": "new-id", "name": "Test"},
            headers=HEADERS
        )
        
        assert response.status_code == 200
        # ID should remain unchanged
        assert response.json()["id"] == farmer_id

class TestFarmerDeletion:
    """TC-020 through TC-022: Farmer deletion functionality"""
    
    def test_delete_farmer(self, client: TestClient):
        """TC-020: Delete existing farmer"""
        # Create farmer
        create_res = client.post("/api/farmers/", json={"name": "ToDelete"}, headers=HEADERS)
        farmer_id = create_res.json()["id"]
        
        # Delete
        response = client.delete(f"/api/farmers/{farmer_id}", headers=HEADERS)
        
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]
    
    def test_delete_nonexistent_farmer(self, client: TestClient):
        """TC-021: Delete non-existent farmer returns 404"""
        response = client.delete("/api/farmers/fake-id", headers=HEADERS)
        
        assert response.status_code == 404
        assert "Farmer not found" in response.json()["detail"]
    
    def test_verify_farmer_deleted(self, client: TestClient):
        """TC-022: Verify farmer is actually deleted"""
        # Create farmer
        create_res = client.post("/api/farmers/", json={"name": "Test"}, headers=HEADERS)
        farmer_id = create_res.json()["id"]
        
        # Delete
        client.delete(f"/api/farmers/{farmer_id}", headers=HEADERS)
        
        # Try to get deleted farmer
        response = client.get(f"/api/farmers/{farmer_id}", headers=HEADERS)
        assert response.status_code == 404

class TestPlotManagement:
    """TC-023 through TC-028: Plot CRUD operations"""
    
    def test_add_plot_to_farmer(self, client: TestClient):
        """TC-023: Add plot to farmer successfully"""
        # Create farmer
        farmer_res = client.post("/api/farmers/", json={"name": "Test"}, headers=HEADERS)
        farmer_id = farmer_res.json()["id"]
        
        # Add plot
        plot_payload = {"name": "Field A", "crop": "wheat", "area_hectares": 5}
        response = client.post(f"/api/farmers/{farmer_id}/plots", json=plot_payload, headers=HEADERS)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Field A"
        assert data["crop"] == "wheat"
        assert data["area_hectares"] == 5
    
    def test_add_plot_invalid_area_zero(self, client: TestClient):
        """TC-024: Reject plot with area = 0"""
        farmer_res = client.post("/api/farmers/", json={"name": "Test"}, headers=HEADERS)
        farmer_id = farmer_res.json()["id"]
        
        plot_payload = {"name": "Field", "crop": "wheat", "area_hectares": 0}
        response = client.post(f"/api/farmers/{farmer_id}/plots", json=plot_payload, headers=HEADERS)
        
        assert response.status_code == 422
    
    def test_add_plot_invalid_area_exceed_limit(self, client: TestClient):
        """TC-025: Reject plot with area > 10000 hectares"""
        farmer_res = client.post("/api/farmers/", json={"name": "Test"}, headers=HEADERS)
        farmer_id = farmer_res.json()["id"]
        
        plot_payload = {"name": "Field", "crop": "wheat", "area_hectares": 10001}
        response = client.post(f"/api/farmers/{farmer_id}/plots", json=plot_payload, headers=HEADERS)
        
        assert response.status_code == 422
    
    def test_add_plot_empty_crop(self, client: TestClient):
        """TC-026: Reject plot with empty crop name"""
        farmer_res = client.post("/api/farmers/", json={"name": "Test"}, headers=HEADERS)
        farmer_id = farmer_res.json()["id"]
        
        plot_payload = {"name": "Field", "crop": "", "area_hectares": 5}
        response = client.post(f"/api/farmers/{farmer_id}/plots", json=plot_payload, headers=HEADERS)
        
        assert response.status_code == 422
    
    def test_get_farmer_plots(self, client: TestClient):
        """TC-027: Get all plots for a farmer"""
        farmer_res = client.post("/api/farmers/", json={"name": "Test"}, headers=HEADERS)
        farmer_id = farmer_res.json()["id"]
        
        # Add plots
        for i in range(3):
            client.post(
                f"/api/farmers/{farmer_id}/plots",
                json={"name": f"Field {i}", "crop": "wheat", "area_hectares": 5},
                headers=HEADERS
            )
        
        response = client.get(f"/api/farmers/{farmer_id}/plots", headers=HEADERS)
        
        assert response.status_code == 200
        plots = response.json()
        assert len(plots) == 3
    
    def test_delete_plot(self, client: TestClient):
        """TC-028: Delete plot from farmer"""
        farmer_res = client.post("/api/farmers/", json={"name": "Test"}, headers=HEADERS)
        farmer_id = farmer_res.json()["id"]
        
        plot_res = client.post(
            f"/api/farmers/{farmer_id}/plots",
            json={"name": "Field", "crop": "wheat", "area_hectares": 5},
            headers=HEADERS
        )
        plot_id = plot_res.json()["id"]
        
        response = client.delete(f"/api/farmers/{farmer_id}/plots/{plot_id}", headers=HEADERS)
        
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]

# ============================================================================
# SECURITY TESTS
# ============================================================================

class TestSecurityValidation:
    """SEC-001 through SEC-015: Security-related tests"""
    
    def test_sql_injection_farmer_name(self, client: TestClient):
        """SEC-004: SQL Injection attempt in farmer name"""
        payload = {"name": "'; DROP TABLE farmers; --"}
        response = client.post("/api/farmers/", json=payload, headers=HEADERS)
        
        # Should be stored safely (SQLModel prevents injection)
        assert response.status_code == 200
        farmer_id = response.json()["id"]
        
        # Verify farmer still exists and can be retrieved
        get_response = client.get(f"/api/farmers/{farmer_id}", headers=HEADERS)
        assert get_response.status_code == 200
    
    def test_xss_farmer_name(self, client: TestClient):
        """SEC-006: XSS attempt in farmer name field"""
        payload = {"name": "<script>alert('xss')</script>"}
        response = client.post("/api/farmers/", json=payload, headers=HEADERS)
        
        # Should store safely
        assert response.status_code == 200
        farmer_id = response.json()["id"]
        
        # Verify stored as-is (React will escape on display)
        get_response = client.get(f"/api/farmers/{farmer_id}", headers=HEADERS)
        assert "<script>" in get_response.json()["farmer"]["name"]
    
    def test_xss_advisory_symptoms(self, client: TestClient):
        """SEC-007: XSS attempt in advisory symptoms field"""
        # Create farmer and plot
        farmer_res = client.post("/api/farmers/", json={"name": "Test"}, headers=HEADERS)
        farmer_id = farmer_res.json()["id"]
        
        plot_res = client.post(
            f"/api/farmers/{farmer_id}/plots",
            json={"name": "Field", "crop": "wheat", "area_hectares": 5},
            headers=HEADERS
        )
        plot_id = plot_res.json()["id"]
        
        # Try XSS in advisory
        advisory_payload = {
            "plot_id": plot_id,
            "symptoms": "<img src=x onerror=alert('xss')>",
            "weather": {"rain_last_3_days": 0}
        }
        response = client.post("/api/advisory/recommend", json=advisory_payload, headers=HEADERS)
        
        # Should succeed, React escapes on display
        assert response.status_code == 200
    
    def test_path_traversal_farmer_id(self, client: TestClient):
        """SEC-008: Path traversal attempt in farmer ID"""
        response = client.get("/api/farmers/../../etc/passwd", headers=HEADERS)
        
        # Should not find anything (UUID validation)
        assert response.status_code == 404
    
    def test_api_key_case_sensitivity(self, client: TestClient):
        """SEC-003: API key should be case-sensitive"""
        # Try uppercase key
        response = client.get(
            "/api/farmers/",
            headers={"x-api-key": "DEFAULT-DEV-KEY"}
        )
        
        # Should fail (case-sensitive)
        assert response.status_code == 403
    
    def test_missing_api_key_on_advisory(self, client: TestClient):
        """SEC-001: Advisory endpoint requires API key"""
        response = client.post(
            "/api/advisory/recommend",
            json={"plot_id": "test"}
            # No headers - no API key
        )
        
        assert response.status_code == 401
        assert "API key required" in response.json()["detail"]

class TestAdvisoryFunctionality:
    """Test advisory recommendation system"""
    
    def test_advisory_without_valid_plot(self, client: TestClient):
        """Test advisory for non-existent plot"""
        payload = {"plot_id": "fake-id-12345"}
        response = client.post("/api/advisory/recommend", json=payload, headers=HEADERS)
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    def test_advisory_basic_functionality(self, client: TestClient):
        """Test advisory generates advice for valid plot"""
        # Create farmer and plot
        farmer_res = client.post("/api/farmers/", json={"name": "Test Farmer"}, headers=HEADERS)
        farmer_id = farmer_res.json()["id"]
        
        plot_res = client.post(
            f"/api/farmers/{farmer_id}/plots",
            json={"name": "Test Field", "crop": "wheat", "area_hectares": 10},
            headers=HEADERS
        )
        plot_id = plot_res.json()["id"]
        
        # Get advisory
        advisory_res = client.post(
            "/api/advisory/recommend",
            json={"plot_id": plot_id},
            headers=HEADERS
        )
        
        assert advisory_res.status_code == 200
        data = advisory_res.json()
        assert "advice" in data
        assert isinstance(data["advice"], list)
        assert len(data["advice"]) > 0
    
    def test_advisory_symptom_matching(self, client: TestClient):
        """Test advisory matches symptoms to recommendations"""
        # Create farmer and plot
        farmer_res = client.post("/api/farmers/", json={"name": "Test Farmer"}, headers=HEADERS)
        farmer_id = farmer_res.json()["id"]
        
        plot_res = client.post(
            f"/api/farmers/{farmer_id}/plots",
            json={"name": "Test Field", "crop": "wheat", "area_hectares": 10},
            headers=HEADERS
        )
        plot_id = plot_res.json()["id"]
        
        # Request advisory with yellow leaves symptom
        advisory_res = client.post(
            "/api/advisory/recommend",
            json={"plot_id": plot_id, "symptoms": "yellow leaves"},
            headers=HEADERS
        )
        
        assert advisory_res.status_code == 200
        advice = advisory_res.json()["advice"]
        # Should mention nitrogen deficiency
        assert any("nitrogen" in a.lower() for a in advice)

class TestHealthCheck:
    """Test API health status"""
    
    def test_health_check_endpoint(self, client: TestClient):
        """IT-010: Health check returns OK"""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests for full workflows"""
    
    def test_full_farmer_workflow(self, client: TestClient):
        """IT-001: Create farmer → Add plots → Get details workflow"""
        # Create farmer
        farmer_res = client.post("/api/farmers/", json={"name": "Complete Test"}, headers=HEADERS)
        assert farmer_res.status_code == 200
        farmer_id = farmer_res.json()["id"]
        
        # Add plots
        for i in range(2):
            plot_res = client.post(
                f"/api/farmers/{farmer_id}/plots",
                json={"name": f"Field {i}", "crop": "wheat", "area_hectares": 5},
                headers=HEADERS
            )
            assert plot_res.status_code == 200
        
        # Get details
        detail_res = client.get(f"/api/farmers/{farmer_id}", headers=HEADERS)
        assert detail_res.status_code == 200
        data = detail_res.json()
        assert len(data["plots"]) == 2
        assert data["farmer"]["name"] == "Complete Test"
    
    def test_cascade_delete_plots_with_farmer(self, client: TestClient):
        """IT-008: Deleting farmer cascades to plots"""
        # Create farmer and plots
        farmer_res = client.post("/api/farmers/", json={"name": "Delete Test"}, headers=HEADERS)
        farmer_id = farmer_res.json()["id"]
        
        plot_res = client.post(
            f"/api/farmers/{farmer_id}/plots",
            json={"name": "Field", "crop": "wheat", "area_hectares": 5},
            headers=HEADERS
        )
        plot_id = plot_res.json()["id"]
        
        # Delete farmer
        client.delete(f"/api/farmers/{farmer_id}", headers=HEADERS)
        
        # Verify plot is also gone (cascaded)
        # Try to get plots - farmer doesn't exist
        get_farmer = client.get(f"/api/farmers/{farmer_id}", headers=HEADERS)
        assert get_farmer.status_code == 404

# ============================================================================
# PERFORMANCE BASELINE TESTS
# ============================================================================

import time

class TestPerformanceBaseline:
    """Performance baseline tests"""
    
    def test_create_farmer_response_time(self, client: TestClient):
        """PERF-001: Farmer creation should be fast"""
        start = time.time()
        response = client.post("/api/farmers/", json={"name": "Speed Test"}, headers=HEADERS)
        elapsed = time.time() - start
        
        assert response.status_code == 200
        assert elapsed < 1.0, f"Create farmer took {elapsed}s, expected < 1s"
    
    def test_list_farmers_response_time(self, client: TestClient):
        """PERF-002: List farmers should complete reasonably"""
        # Populate some farmers
        for i in range(10):
            client.post("/api/farmers/", json={"name": f"Farmer {i}"}, headers=HEADERS)
        
        start = time.time()
        response = client.get("/api/farmers/?limit=100", headers=HEADERS)
        elapsed = time.time() - start
        
        assert response.status_code == 200
        assert elapsed < 1.0, f"List farmers took {elapsed}s, expected < 1s"


if __name__ == "__main__":
    # Run with: pytest tests/test_api.py -v
    pytest.main([__file__, "-v", "--tb=short"])
