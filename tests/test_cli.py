"""Tests for CLI functions"""
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from src.cli import (
    validate_project_name,
    get_project_type,
    get_project_name,
    get_project_path,
    confirm_overwrite,
    run_cli,
)


class TestValidateProjectName:
    """Tests for validate_project_name function"""
    
    def test_valid_project_names(self):
        """Test valid project names"""
        assert validate_project_name("my_project") is True
        assert validate_project_name("my-project") is True
        assert validate_project_name("project123") is True
        assert validate_project_name("Project_Name_123") is True
        assert validate_project_name("a") is True
    
    def test_invalid_project_names(self):
        """Test invalid project names"""
        assert validate_project_name("my project") is False  # space
        assert validate_project_name("my.project") is False  # dot
        assert validate_project_name("my@project") is False  # special char
        assert validate_project_name("") is False  # empty
        assert validate_project_name("project!") is False  # exclamation


class TestGetProjectType:
    """Tests for get_project_type function"""
    
    def test_get_project_type_valid(self, mock_prompt):
        """Test getting project type with valid input"""
        mock_prompt.return_value = "1"
        result = get_project_type()
        assert result == "1"
        mock_prompt.assert_called_once()
    
    def test_get_project_type_different_choice(self, mock_prompt):
        """Test getting different project type"""
        mock_prompt.return_value = "3"
        result = get_project_type()
        assert result == "3"


class TestGetProjectName:
    """Tests for get_project_name function"""
    
    def test_get_project_name_default(self, mock_prompt):
        """Test getting project name with default"""
        mock_prompt.return_value = "my_project"
        result = get_project_name()
        assert result == "my_project"
        mock_prompt.assert_called_once()
    
    def test_get_project_name_custom(self, mock_prompt):
        """Test getting custom project name"""
        mock_prompt.return_value = "custom_name"
        result = get_project_name()
        assert result == "custom_name"


class TestGetProjectPath:
    """Tests for get_project_path function"""
    
    def test_get_project_path_default(self, mock_prompt, monkeypatch):
        """Test getting project path with default"""
        import os
        cwd = Path.cwd()
        expected_default = str(cwd / "test_project")
        
        mock_prompt.return_value = expected_default
        result = get_project_path("test_project")
        
        assert result == Path(expected_default)
        mock_prompt.assert_called_once()
    
    def test_get_project_path_custom(self, mock_prompt):
        """Test getting custom project path"""
        custom_path = "/tmp/custom/path"
        mock_prompt.return_value = custom_path
        result = get_project_path("test_project")
        assert result == Path(custom_path)


class TestConfirmOverwrite:
    """Tests for confirm_overwrite function"""
    
    def test_confirm_overwrite_true(self, mock_confirm):
        """Test overwrite confirmation returns True"""
        mock_confirm.return_value = True
        result = confirm_overwrite(Path("/tmp/test"))
        assert result is True
        mock_confirm.assert_called_once()
    
    def test_confirm_overwrite_false(self, mock_confirm):
        """Test overwrite confirmation returns False"""
        mock_confirm.return_value = False
        result = confirm_overwrite(Path("/tmp/test"))
        assert result is False


class TestRunCLI:
    """Tests for run_cli function"""
    
    def test_run_cli_success(self, temp_project_dir, mock_prompt, mock_confirm, mock_display_functions, monkeypatch):
        """Test successful CLI run - verifies CLI flow works correctly"""
        # Mock console.print in cli module to capture any error output
        mock_console_print = MagicMock()
        monkeypatch.setattr("src.cli.console.print", mock_console_print)
        
        # Use a subdirectory within temp_project_dir so it doesn't exist yet
        project_path = temp_project_dir / "test_project"
        
        # Setup mocks
        mock_prompt.side_effect = ["1", "test_project", str(project_path)]
        mock_confirm.return_value = False  # No overwrite needed (directory won't exist)
        
        # Run CLI
        run_cli()
        
        # Verify display functions were called
        mock_display_functions["welcome"].assert_called_once()
        mock_display_functions["project_types"].assert_called_once()
        
        # Check if error was displayed - if so, the CLI flow had an issue
        if mock_display_functions["error"].call_count > 0:
            # Get the error message
            error_call = mock_display_functions["error"].call_args[0][0]
            # Check console.print calls for traceback info
            console_calls = [str(call) for call in mock_console_print.call_args_list]
            pytest.fail(f"Error during CLI run: {error_call}. Console output: {console_calls}")
        
        # Verify project was created
        assert (project_path / "pyproject.toml").exists(), "Project was not created"
        assert (project_path / "README.md").exists(), "README was not created"
    
    def test_run_cli_invalid_project_name(self, mock_prompt, mock_display_functions, monkeypatch):
        """Test CLI with invalid project name"""
        mock_console_print = MagicMock()
        monkeypatch.setattr("src.cli.console.print", mock_console_print)
        
        mock_prompt.side_effect = ["1", "invalid project name"]
        
        run_cli()
        
        # Should display error and not create project
        mock_display_functions["error"].assert_called_once()
        mock_display_functions["success"].assert_not_called()
    
    def test_run_cli_overwrite_confirmed(self, temp_project_dir, mock_prompt, mock_confirm, mock_display_functions, monkeypatch):
        """Test CLI with overwrite confirmation"""
        mock_console_print = MagicMock()
        monkeypatch.setattr("src.cli.console.print", mock_console_print)
        
        # Create existing directory
        (temp_project_dir / "existing_file.txt").touch()
        
        mock_prompt.side_effect = ["1", "test_project", str(temp_project_dir)]
        mock_confirm.return_value = True  # Confirm overwrite
        
        run_cli()
        
        # Should proceed with overwrite
        mock_display_functions["success"].assert_called_once()
    
    def test_run_cli_overwrite_cancelled(self, temp_project_dir, mock_prompt, mock_confirm, mock_display_functions, monkeypatch):
        """Test CLI with overwrite cancelled"""
        mock_console_print = MagicMock()
        monkeypatch.setattr("src.cli.console.print", mock_console_print)
        
        # Create existing directory
        (temp_project_dir / "existing_file.txt").touch()
        
        mock_prompt.side_effect = ["1", "test_project", str(temp_project_dir)]
        mock_confirm.return_value = False  # Cancel overwrite
        
        run_cli()
        
        # Should not create project
        mock_display_functions["success"].assert_not_called()
    
    def test_run_cli_template_error(self, temp_project_dir, mock_prompt, mock_confirm, mock_display_functions, monkeypatch):
        """Test CLI with template generation error"""
        mock_console_print = MagicMock()
        monkeypatch.setattr("src.cli.console.print", mock_console_print)
        
        mock_prompt.side_effect = ["999", "test_project", str(temp_project_dir)]  # Invalid template
        
        run_cli()
        
        # Should display error
        mock_display_functions["error"].assert_called_once()

