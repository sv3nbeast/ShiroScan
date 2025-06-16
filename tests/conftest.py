import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock
import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def temp_file(temp_dir):
    """Create a temporary file for testing."""
    def _create_temp_file(name="test_file.txt", content=""):
        file_path = temp_dir / name
        file_path.write_text(content)
        return file_path
    return _create_temp_file


@pytest.fixture
def mock_requests(mocker):
    """Mock the requests library."""
    mock = mocker.patch('requests.get')
    mock.return_value.status_code = 200
    mock.return_value.text = "Mock response"
    mock.return_value.content = b"Mock response"
    mock.return_value.headers = {'Content-Type': 'text/html'}
    return mock


@pytest.fixture
def mock_config():
    """Provide a mock configuration for testing."""
    return {
        'target_url': 'http://example.com',
        'timeout': 10,
        'threads': 5,
        'key_file': 'key.log',
        'dns_log': 'test.dnslog.cn',
        'cookie': 'rememberMe=test',
        'mode': 'cbc',
    }


@pytest.fixture
def mock_shiro_response():
    """Mock a typical Shiro response with rememberMe cookie."""
    response = Mock()
    response.status_code = 200
    response.headers = {
        'Set-Cookie': 'rememberMe=deleteMe; Path=/; Max-Age=0; Expires=Thu, 01-Jan-1970 00:00:00 GMT'
    }
    response.text = "<html><body>Test response</body></html>"
    return response


@pytest.fixture
def mock_key_list():
    """Provide a mock list of encryption keys for testing."""
    return [
        "kPH+bIxk5D2deZiIxcaaaA==",
        "4AvVhmFLUs0KTA3Kprsdag==",
        "Z3VucwAAAAAAAAAAAAAAAA==",
        "fCq+/xW488hMTCD+cmJ3aQ==",
        "1QWLxg+NYmxraMoxAXu/Iw=="
    ]


@pytest.fixture
def mock_plugin():
    """Create a mock plugin for testing."""
    plugin = MagicMock()
    plugin.poc.return_value = "Mock payload"
    plugin.__name__ = "MockPlugin"
    return plugin


@pytest.fixture
def sample_base64_payload():
    """Provide a sample base64 encoded payload."""
    return "rO0ABXNyADJvcmcuYXBhY2hlLnNoaXJvLnN1YmplY3QuU2ltcGxlUHJpbmNpcGFsQ29sbGVjdGlvbqh/WCXGowhKAwABTAAPcmVhbG1QcmluY2lwYWxzdAAPTGphdmEvdXRpbC9NYXA7eHBwdwEAeA=="


@pytest.fixture
def mock_subprocess_run(mocker):
    """Mock subprocess.run for testing command execution."""
    mock = mocker.patch('subprocess.run')
    mock.return_value.returncode = 0
    mock.return_value.stdout = "Mock command output"
    mock.return_value.stderr = ""
    return mock


@pytest.fixture
def mock_threading(mocker):
    """Mock threading for testing concurrent operations."""
    mock_pool = mocker.patch('threadpool.ThreadPool')
    mock_pool.return_value.putRequest.return_value = None
    mock_pool.return_value.wait.return_value = None
    return mock_pool


@pytest.fixture(autouse=True)
def reset_environment():
    """Reset environment variables before each test."""
    original_env = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def capture_stdout(monkeypatch):
    """Capture stdout for testing print statements."""
    from io import StringIO
    captured_output = StringIO()
    monkeypatch.setattr('sys.stdout', captured_output)
    return captured_output


@pytest.fixture
def mock_dns_log(mocker):
    """Mock DNS log functionality."""
    mock = mocker.patch('requests.get')
    mock.return_value.json.return_value = {
        'status': 'success',
        'data': ['test.example.com']
    }
    return mock