"""Pytest fixtures and test utilities"""
import tempfile
from pathlib import Path
from typing import Generator
import pytest
from unittest.mock import MagicMock
from rich.console import Console
from rich.prompt import Prompt, Confirm


@pytest.fixture
def temp_project_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing project generation"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_console(monkeypatch):
    """Mock Rich Console for testing UI functions"""
    mock = MagicMock(spec=Console)
    monkeypatch.setattr("src.ui.console", mock)
    return mock


@pytest.fixture
def mock_prompt(monkeypatch):
    """Mock Rich Prompt for CLI interaction tests"""
    mock = MagicMock(spec=Prompt.ask)
    monkeypatch.setattr("src.cli.Prompt.ask", mock)
    return mock


@pytest.fixture
def mock_confirm(monkeypatch):
    """Mock Rich Confirm for CLI interaction tests"""
    mock = MagicMock(spec=Confirm.ask)
    monkeypatch.setattr("src.cli.Confirm.ask", mock)
    return mock


@pytest.fixture
def mock_display_functions(monkeypatch):
    """Mock all display functions to avoid console output during tests"""
    mock_welcome = MagicMock()
    mock_project_types = MagicMock()
    mock_success = MagicMock()
    mock_error = MagicMock()
    
    monkeypatch.setattr("src.cli.display_welcome", mock_welcome)
    monkeypatch.setattr("src.cli.display_project_types", mock_project_types)
    monkeypatch.setattr("src.cli.display_success", mock_success)
    monkeypatch.setattr("src.cli.display_error", mock_error)
    
    return {
        "welcome": mock_welcome,
        "project_types": mock_project_types,
        "success": mock_success,
        "error": mock_error,
    }


def verify_file_exists(file_path: Path, should_exist: bool = True) -> None:
    """Helper to verify file existence"""
    assert file_path.exists() == should_exist, f"File {file_path} existence mismatch"


def verify_folder_structure(base_path: Path, expected_folders: list[str]) -> None:
    """Helper to verify folder structure was created correctly"""
    for folder in expected_folders:
        folder_path = base_path / folder
        assert folder_path.exists(), f"Expected folder {folder} does not exist"
        assert folder_path.is_dir(), f"{folder} exists but is not a directory"
        # Check for .gitkeep file (only if folder doesn't have subfolders in the list)
        # If a parent folder has subfolders, the .gitkeep will be in the subfolders, not the parent
        has_subfolders_in_list = any(
            f.startswith(folder + "/") and f != folder
            for f in expected_folders
        )
        # Also check if the folder actually has subdirectories (even if not in the list)
        has_actual_subdirs = any(
            (folder_path / item).is_dir()
            for item in folder_path.iterdir()
            if item.name != ".gitkeep"
        )
        if not has_subfolders_in_list and not has_actual_subdirs:
            gitkeep = folder_path / ".gitkeep"
            assert gitkeep.exists(), f".gitkeep file missing in {folder}"


def parse_pyproject_toml(file_path: Path) -> dict:
    """Helper to parse and validate pyproject.toml structure"""
    if not file_path.exists():
        raise FileNotFoundError(f"pyproject.toml not found at {file_path}")
    
    # Try tomllib (Python 3.11+), fall back to text-based validation
    try:
        import tomllib
        with open(file_path, "rb") as f:
            return tomllib.load(f)
    except ImportError:
        # Fallback: just read as text for basic validation
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Basic validation - check for key sections
            assert "[project]" in content, "Missing [project] section"
            assert "[build-system]" in content, "Missing [build-system] section"
            return {"content": content}

