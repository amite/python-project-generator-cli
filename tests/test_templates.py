"""Tests for template base class methods"""
import pytest
from pathlib import Path
from src.templates.base import ProjectTemplate
from tests.conftest import verify_file_exists, verify_folder_structure, parse_pyproject_toml


class TestProjectTemplate:
    """Tests for ProjectTemplate base class"""
    
    def test_init(self, temp_project_dir):
        """Test template initialization"""
        template = ProjectTemplate("test_project", temp_project_dir)
        assert template.project_name == "test_project"
        assert template.project_path == temp_project_dir
        assert len(template.common_folders) > 0
    
    def test_create_folder_structure(self, temp_project_dir):
        """Test folder structure creation"""
        template = ProjectTemplate("test_project", temp_project_dir)
        additional_folders = ["custom_folder", "another/custom"]
        
        template.create_folder_structure(additional_folders)
        
        # Verify common folders
        verify_folder_structure(temp_project_dir, template.common_folders)
        
        # Verify additional folders
        verify_folder_structure(temp_project_dir, additional_folders)
    
    def test_create_folder_structure_no_additional(self, temp_project_dir):
        """Test folder structure creation without additional folders"""
        template = ProjectTemplate("test_project", temp_project_dir)
        template.create_folder_structure()
        
        verify_folder_structure(temp_project_dir, template.common_folders)
    
    def test_create_pyproject_toml(self, temp_project_dir):
        """Test pyproject.toml creation"""
        template = ProjectTemplate("test_project", temp_project_dir)
        dependencies = ['"requests>=2.31.0"', '"click>=8.1.0"']
        
        template.create_pyproject_toml(dependencies)
        
        # Verify file exists
        pyproject_path = temp_project_dir / "pyproject.toml"
        verify_file_exists(pyproject_path)
        
        # Verify content structure
        try:
            content = parse_pyproject_toml(pyproject_path)
            # If parsing worked, verify structure
            if isinstance(content, dict) and "content" not in content:
                assert "project" in content
                assert content["project"]["name"] == "test_project"
        except Exception:
            # Fallback: check file content directly
            with open(pyproject_path, "r") as f:
                content = f.read()
                assert "[project]" in content
                assert 'name = "test_project"' in content
                assert "requests" in content or "click" in content
    
    def test_create_gitignore(self, temp_project_dir):
        """Test .gitignore creation"""
        template = ProjectTemplate("test_project", temp_project_dir)
        template.create_gitignore()
        
        gitignore_path = temp_project_dir / ".gitignore"
        verify_file_exists(gitignore_path)
        
        # Verify content
        with open(gitignore_path, "r") as f:
            content = f.read()
            assert "__pycache__" in content
            assert ".venv" in content
            assert ".pytest_cache" in content
    
    def test_create_readme(self, temp_project_dir):
        """Test README creation"""
        template = ProjectTemplate("test_project", temp_project_dir)
        readme_content = "# Test Project\n\nThis is a test project."
        
        template.create_readme(readme_content)
        
        readme_path = temp_project_dir / "README.md"
        verify_file_exists(readme_path)
        
        # Verify content
        with open(readme_path, "r") as f:
            content = f.read()
            assert content == readme_content
    
    def test_create_basic_test(self, temp_project_dir):
        """Test basic test file creation"""
        template = ProjectTemplate("test_project", temp_project_dir)
        # Create tests directory first
        (temp_project_dir / "tests").mkdir(parents=True, exist_ok=True)
        
        template.create_basic_test()
        
        # Verify test file exists
        test_file = temp_project_dir / "tests" / "test_basic.py"
        verify_file_exists(test_file)
        
        # Verify __init__.py exists
        init_file = temp_project_dir / "tests" / "__init__.py"
        verify_file_exists(init_file)
        
        # Verify test file content
        with open(test_file, "r") as f:
            content = f.read()
            assert "import pytest" in content
            assert "def test_project_structure" in content
            assert "def test_placeholder" in content
    
    def test_create_src_init(self, temp_project_dir):
        """Test src/__init__.py creation"""
        template = ProjectTemplate("test_project", temp_project_dir)
        # Create src directory first
        (temp_project_dir / "src").mkdir(parents=True, exist_ok=True)
        
        template.create_src_init()
        
        init_file = temp_project_dir / "src" / "__init__.py"
        verify_file_exists(init_file)
        
        # Verify content
        with open(init_file, "r") as f:
            content = f.read()
            assert "test_project" in content
    
    def test_create_folder_structure_error_handling(self, temp_project_dir):
        """Test error handling in create_folder_structure"""
        template = ProjectTemplate("test_project", temp_project_dir)
        
        # Create a file with the same name as a folder to cause error
        (temp_project_dir / "notebooks").touch()
        
        # Should raise RuntimeError
        with pytest.raises(RuntimeError, match="Failed to create folder structure"):
            template.create_folder_structure()
    
    def test_create_pyproject_toml_error_handling(self, temp_project_dir):
        """Test error handling in create_pyproject_toml"""
        template = ProjectTemplate("test_project", temp_project_dir)
        
        # Create a directory with the same name to cause error
        (temp_project_dir / "pyproject.toml").mkdir()
        
        # Should raise RuntimeError
        with pytest.raises(RuntimeError, match="Failed to create pyproject.toml"):
            template.create_pyproject_toml(['"requests>=2.31.0"'])
    
    def test_generate_not_implemented(self, temp_project_dir):
        """Test that generate raises NotImplementedError"""
        template = ProjectTemplate("test_project", temp_project_dir)
        
        with pytest.raises(NotImplementedError, match="Subclasses must implement generate"):
            template.generate()

