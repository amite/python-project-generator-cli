"""Tests for UI display functions"""
import pytest
from unittest.mock import MagicMock, patch
from src.ui import (
    display_welcome,
    display_project_types,
    display_success,
    display_error,
)


class TestDisplayWelcome:
    """Tests for display_welcome function"""
    
    def test_display_welcome_calls_console(self, mock_console):
        """Test that display_welcome calls console.print"""
        display_welcome()
        # Should call console.print at least once
        assert mock_console.print.called
    
    def test_display_welcome_no_exception(self, mock_console):
        """Test that display_welcome doesn't raise exceptions"""
        display_welcome()
        # If we get here, no exception was raised


class TestDisplayProjectTypes:
    """Tests for display_project_types function"""
    
    def test_display_project_types_calls_console(self, mock_console):
        """Test that display_project_types calls console.print"""
        display_project_types()
        # Should call console.print at least once
        assert mock_console.print.called
    
    def test_display_project_types_no_exception(self, mock_console):
        """Test that display_project_types doesn't raise exceptions"""
        display_project_types()
        # If we get here, no exception was raised
    
    @patch("src.ui.get_template_list")
    def test_display_project_types_uses_template_list(self, mock_get_list, mock_console):
        """Test that display_project_types uses get_template_list"""
        mock_get_list.return_value = [
            {"key": "1", "name": "Test Template", "description": "Test Description"}
        ]
        
        display_project_types()
        
        mock_get_list.assert_called_once()


class TestDisplaySuccess:
    """Tests for display_success function"""
    
    def test_display_success_calls_console(self, mock_console):
        """Test that display_success calls console.print"""
        display_success("test_project", "/tmp/test")
        # Should call console.print at least once
        assert mock_console.print.called
    
    def test_display_success_no_exception(self, mock_console):
        """Test that display_success doesn't raise exceptions"""
        display_success("test_project", "/tmp/test")
        # If we get here, no exception was raised
    
    def test_display_success_with_path_object(self, mock_console):
        """Test that display_success works with Path object"""
        from pathlib import Path
        display_success("test_project", Path("/tmp/test"))
        # Should not raise exception
        assert mock_console.print.called


class TestDisplayError:
    """Tests for display_error function"""
    
    def test_display_error_calls_console(self, mock_console):
        """Test that display_error calls console.print"""
        display_error("Test error message")
        # Should call console.print at least once
        assert mock_console.print.called
    
    def test_display_error_no_exception(self, mock_console):
        """Test that display_error doesn't raise exceptions"""
        display_error("Test error message")
        # If we get here, no exception was raised
    
    def test_display_error_with_different_messages(self, mock_console):
        """Test display_error with different error messages"""
        display_error("Error 1")
        display_error("Error 2")
        display_error("")
        
        # Should call console.print for each error
        assert mock_console.print.call_count >= 3

