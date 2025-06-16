import pytest
import sys
import os
from pathlib import Path


class TestSetupValidation:
    """Validation tests to ensure the testing infrastructure is properly configured."""

    def test_python_version(self):
        """Ensure Python version is 3.8 or higher."""
        assert sys.version_info >= (3, 8), "Python 3.8 or higher is required"

    def test_project_structure(self):
        """Verify the project structure is correct."""
        project_root = Path(__file__).parent.parent
        
        # Check main directories exist
        assert project_root.exists()
        assert (project_root / "moule").exists()
        assert (project_root / "tests").exists()
        assert (project_root / "tests" / "unit").exists()
        assert (project_root / "tests" / "integration").exists()
        
        # Check __init__.py files exist
        assert (project_root / "moule" / "__init__.py").exists()
        assert (project_root / "tests" / "__init__.py").exists()
        assert (project_root / "tests" / "unit" / "__init__.py").exists()
        assert (project_root / "tests" / "integration" / "__init__.py").exists()

    def test_pyproject_toml_exists(self):
        """Verify pyproject.toml exists and is valid."""
        project_root = Path(__file__).parent.parent
        pyproject_path = project_root / "pyproject.toml"
        
        assert pyproject_path.exists(), "pyproject.toml not found"
        
        # Check it contains required sections
        content = pyproject_path.read_text()
        assert "[tool.poetry]" in content
        assert "[tool.pytest.ini_options]" in content
        assert "[tool.coverage.run]" in content

    def test_fixtures_available(self, temp_dir, mock_config):
        """Test that fixtures from conftest.py are available."""
        assert temp_dir.exists()
        assert isinstance(mock_config, dict)
        assert 'target_url' in mock_config

    @pytest.mark.unit
    def test_unit_marker(self):
        """Test that the unit marker works."""
        assert True

    @pytest.mark.integration
    def test_integration_marker(self):
        """Test that the integration marker works."""
        assert True

    @pytest.mark.slow
    def test_slow_marker(self):
        """Test that the slow marker works."""
        assert True

    def test_imports(self):
        """Verify main module can be imported."""
        try:
            import moule
            assert moule is not None
        except ImportError as e:
            pytest.fail(f"Failed to import moule module: {e}")

    def test_temp_file_fixture(self, temp_file):
        """Test the temp_file fixture works correctly."""
        test_file = temp_file("test.txt", "Hello, World!")
        assert test_file.exists()
        assert test_file.read_text() == "Hello, World!"

    def test_capture_stdout_fixture(self, capture_stdout, capsys):
        """Test stdout capturing fixture."""
        print("Test output")
        # Since pytest captures stdout by default, we need to use capsys
        captured = capsys.readouterr()
        assert "Test output" in captured.out

    def test_mock_requests_fixture(self, mock_requests):
        """Test the mock_requests fixture."""
        import requests
        response = requests.get("http://example.com")
        assert response.status_code == 200
        assert response.text == "Mock response"

    def test_coverage_configured(self):
        """Ensure coverage is properly configured."""
        project_root = Path(__file__).parent.parent
        pyproject_path = project_root / "pyproject.toml"
        content = pyproject_path.read_text()
        
        # Check coverage configuration
        assert "--cov=moule" in content
        assert "--cov-fail-under=15" in content
        assert "--cov-report=html" in content
        assert "--cov-report=xml" in content