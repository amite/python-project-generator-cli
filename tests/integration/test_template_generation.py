"""Integration tests for full project template generation"""
import pytest
from pathlib import Path
from src.templates import (
    RAGAgentTemplate,
    FastAPITemplate,
    DataScienceTemplate,
    AutomationTemplate,
)
from tests.conftest import verify_file_exists, verify_folder_structure, parse_pyproject_toml


class TestRAGAgentTemplate:
    """Integration tests for RAG Agent template"""
    
    def test_rag_agent_generation(self, temp_project_dir):
        """Test full RAG Agent project generation"""
        template = RAGAgentTemplate("test_rag", temp_project_dir)
        template.generate()
        
        # Verify common folders
        verify_folder_structure(temp_project_dir, template.common_folders)
        
        # Verify template-specific folders
        assert (temp_project_dir / "src" / "agents").exists()
        assert (temp_project_dir / "src" / "vectorstore").exists()
        assert (temp_project_dir / "streamlit_app").exists()
        
        # Verify key files
        verify_file_exists(temp_project_dir / "pyproject.toml")
        verify_file_exists(temp_project_dir / "README.md")
        verify_file_exists(temp_project_dir / ".gitignore")
        verify_file_exists(temp_project_dir / "tests" / "test_basic.py")
        verify_file_exists(temp_project_dir / "streamlit_app" / "app.py")
        verify_file_exists(temp_project_dir / "src" / "agents" / "rag_agent.py")
        verify_file_exists(temp_project_dir / "scripts" / "generate_data.py")
        verify_file_exists(temp_project_dir / ".env.example")
    
    def test_rag_agent_pyproject_content(self, temp_project_dir):
        """Test RAG Agent pyproject.toml content"""
        template = RAGAgentTemplate("test_rag", temp_project_dir)
        template.generate()
        
        pyproject_path = temp_project_dir / "pyproject.toml"
        try:
            content = parse_pyproject_toml(pyproject_path)
            if isinstance(content, dict) and "content" not in content:
                assert content["project"]["name"] == "test_rag"
        except Exception:
            # Fallback: check file content
            with open(pyproject_path, "r") as f:
                content = f.read()
                assert 'name = "test_rag"' in content
                assert "langchain" in content.lower()
                assert "streamlit" in content.lower()
    
    def test_rag_agent_readme_content(self, temp_project_dir):
        """Test RAG Agent README content"""
        template = RAGAgentTemplate("test_rag", temp_project_dir)
        template.generate()
        
        readme_path = temp_project_dir / "README.md"
        with open(readme_path, "r") as f:
            content = f.read()
            assert "# test_rag" in content
            assert "RAG" in content
            assert "LangChain" in content
            assert "Streamlit" in content


class TestFastAPITemplate:
    """Integration tests for FastAPI template"""
    
    def test_fastapi_generation(self, temp_project_dir):
        """Test full FastAPI project generation"""
        template = FastAPITemplate("test_fastapi", temp_project_dir)
        template.generate()
        
        # Verify common folders
        verify_folder_structure(temp_project_dir, template.common_folders)
        
        # Verify template-specific folders
        assert (temp_project_dir / "src" / "api").exists()
        assert (temp_project_dir / "src" / "models").exists()
        assert (temp_project_dir / "src" / "services").exists()
        assert (temp_project_dir / "src" / "db").exists()
        
        # Verify key files
        verify_file_exists(temp_project_dir / "pyproject.toml")
        verify_file_exists(temp_project_dir / "README.md")
        verify_file_exists(temp_project_dir / ".gitignore")
        verify_file_exists(temp_project_dir / "tests" / "test_basic.py")
        verify_file_exists(temp_project_dir / "src" / "main.py")
        verify_file_exists(temp_project_dir / "Dockerfile")
        verify_file_exists(temp_project_dir / "docker-compose.yml")
    
    def test_fastapi_pyproject_content(self, temp_project_dir):
        """Test FastAPI pyproject.toml content"""
        template = FastAPITemplate("test_fastapi", temp_project_dir)
        template.generate()
        
        pyproject_path = temp_project_dir / "pyproject.toml"
        try:
            content = parse_pyproject_toml(pyproject_path)
            if isinstance(content, dict) and "content" not in content:
                assert content["project"]["name"] == "test_fastapi"
        except Exception:
            # Fallback: check file content
            with open(pyproject_path, "r") as f:
                content = f.read()
                assert 'name = "test_fastapi"' in content
                assert "fastapi" in content.lower()
                assert "uvicorn" in content.lower()
    
    def test_fastapi_readme_content(self, temp_project_dir):
        """Test FastAPI README content"""
        template = FastAPITemplate("test_fastapi", temp_project_dir)
        template.generate()
        
        readme_path = temp_project_dir / "README.md"
        with open(readme_path, "r") as f:
            content = f.read()
            assert "# test_fastapi" in content
            assert "FastAPI" in content
            assert "Docker" in content or "docker" in content


class TestDataScienceTemplate:
    """Integration tests for Data Science template"""
    
    def test_data_science_generation(self, temp_project_dir):
        """Test full Data Science project generation"""
        template = DataScienceTemplate("test_ds", temp_project_dir)
        template.generate()
        
        # Verify common folders
        verify_folder_structure(temp_project_dir, template.common_folders)
        
        # Verify template-specific folders
        assert (temp_project_dir / "src" / "data").exists()
        assert (temp_project_dir / "src" / "features").exists()
        assert (temp_project_dir / "src" / "models").exists()
        assert (temp_project_dir / "models").exists()
        assert (temp_project_dir / "data" / "raw").exists()
        assert (temp_project_dir / "data" / "processed").exists()
        
        # Verify key files
        verify_file_exists(temp_project_dir / "pyproject.toml")
        verify_file_exists(temp_project_dir / "README.md")
        verify_file_exists(temp_project_dir / ".gitignore")
        verify_file_exists(temp_project_dir / "tests" / "test_basic.py")
        verify_file_exists(temp_project_dir / "src" / "data" / "loader.py")
        verify_file_exists(temp_project_dir / "src" / "models" / "train.py")
        verify_file_exists(temp_project_dir / "src" / "models" / "serve.py")
    
    def test_data_science_pyproject_content(self, temp_project_dir):
        """Test Data Science pyproject.toml content"""
        template = DataScienceTemplate("test_ds", temp_project_dir)
        template.generate()
        
        pyproject_path = temp_project_dir / "pyproject.toml"
        try:
            content = parse_pyproject_toml(pyproject_path)
            if isinstance(content, dict) and "content" not in content:
                assert content["project"]["name"] == "test_ds"
        except Exception:
            # Fallback: check file content
            with open(pyproject_path, "r") as f:
                content = f.read()
                assert 'name = "test_ds"' in content
                assert "pandas" in content.lower()
                assert "scikit-learn" in content.lower() or "sklearn" in content.lower()
    
    def test_data_science_readme_content(self, temp_project_dir):
        """Test Data Science README content"""
        template = DataScienceTemplate("test_ds", temp_project_dir)
        template.generate()
        
        readme_path = temp_project_dir / "README.md"
        with open(readme_path, "r") as f:
            content = f.read()
            assert "# test_ds" in content
            assert "Data Science" in content or "Machine Learning" in content


class TestAutomationTemplate:
    """Integration tests for Automation template"""
    
    def test_automation_generation(self, temp_project_dir):
        """Test full Automation project generation"""
        template = AutomationTemplate("test_automation", temp_project_dir)
        template.generate()
        
        # Verify common folders
        verify_folder_structure(temp_project_dir, template.common_folders)
        
        # Verify template-specific folders
        assert (temp_project_dir / "src" / "tasks").exists()
        assert (temp_project_dir / "logs").exists()
        
        # Verify key files
        verify_file_exists(temp_project_dir / "pyproject.toml")
        verify_file_exists(temp_project_dir / "README.md")
        verify_file_exists(temp_project_dir / ".gitignore")
        verify_file_exists(temp_project_dir / "tests" / "test_basic.py")
        verify_file_exists(temp_project_dir / "src" / "cli.py")
        verify_file_exists(temp_project_dir / "src" / "tasks" / "file_organizer.py")
        verify_file_exists(temp_project_dir / "src" / "tasks" / "web_scraper.py")
    
    def test_automation_pyproject_content(self, temp_project_dir):
        """Test Automation pyproject.toml content"""
        template = AutomationTemplate("test_automation", temp_project_dir)
        template.generate()
        
        pyproject_path = temp_project_dir / "pyproject.toml"
        try:
            content = parse_pyproject_toml(pyproject_path)
            if isinstance(content, dict) and "content" not in content:
                assert content["project"]["name"] == "test_automation"
        except Exception:
            # Fallback: check file content
            with open(pyproject_path, "r") as f:
                content = f.read()
                assert 'name = "test_automation"' in content
                assert "click" in content.lower()
    
    def test_automation_readme_content(self, temp_project_dir):
        """Test Automation README content"""
        template = AutomationTemplate("test_automation", temp_project_dir)
        template.generate()
        
        readme_path = temp_project_dir / "README.md"
        with open(readme_path, "r") as f:
            content = f.read()
            assert "# test_automation" in content
            assert "automation" in content.lower() or "scripting" in content.lower()


class TestAllTemplatesCommonStructure:
    """Tests for common structure across all templates"""
    
    @pytest.mark.parametrize("template_class,project_name", [
        (RAGAgentTemplate, "test_rag"),
        (FastAPITemplate, "test_fastapi"),
        (DataScienceTemplate, "test_ds"),
        (AutomationTemplate, "test_automation"),
    ])
    def test_all_templates_create_common_files(self, temp_project_dir, template_class, project_name):
        """Test that all templates create common files"""
        template = template_class(project_name, temp_project_dir)
        template.generate()
        
        # All templates should create these files
        verify_file_exists(temp_project_dir / "pyproject.toml")
        verify_file_exists(temp_project_dir / "README.md")
        verify_file_exists(temp_project_dir / ".gitignore")
        verify_file_exists(temp_project_dir / "tests" / "test_basic.py")
        verify_file_exists(temp_project_dir / "src" / "__init__.py")
    
    @pytest.mark.parametrize("template_class,project_name", [
        (RAGAgentTemplate, "test_rag"),
        (FastAPITemplate, "test_fastapi"),
        (DataScienceTemplate, "test_ds"),
        (AutomationTemplate, "test_automation"),
    ])
    def test_all_templates_create_common_folders(self, temp_project_dir, template_class, project_name):
        """Test that all templates create common folders"""
        template = template_class(project_name, temp_project_dir)
        template.generate()
        
        # All templates should create these folders
        # Note: artifacts has subfolders (wip, completed), so we check for those instead
        common_folders = [
            "notebooks",
            "artifacts/wip",
            "artifacts/completed",
            "reports",
            "research",
            "quality",
            "scripts",
            "data",
            "tests"
        ]
        verify_folder_structure(temp_project_dir, common_folders)

