"""Tests for template registry functions"""
import pytest
from src.templates import (
    TEMPLATE_REGISTRY,
    get_template_list,
    get_template_class,
    RAGAgentTemplate,
    FastAPITemplate,
    DataScienceTemplate,
    AutomationTemplate,
)


class TestTemplateRegistry:
    """Tests for template registry"""
    
    def test_registry_contains_all_templates(self):
        """Test that registry contains all expected templates"""
        assert "1" in TEMPLATE_REGISTRY
        assert "2" in TEMPLATE_REGISTRY
        assert "3" in TEMPLATE_REGISTRY
        assert "4" in TEMPLATE_REGISTRY
    
    def test_registry_template_classes(self):
        """Test that registry contains correct template classes"""
        assert TEMPLATE_REGISTRY["1"] == RAGAgentTemplate
        assert TEMPLATE_REGISTRY["2"] == FastAPITemplate
        assert TEMPLATE_REGISTRY["3"] == DataScienceTemplate
        assert TEMPLATE_REGISTRY["4"] == AutomationTemplate


class TestGetTemplateList:
    """Tests for get_template_list function"""
    
    def test_get_template_list_returns_list(self):
        """Test that get_template_list returns a list"""
        result = get_template_list()
        assert isinstance(result, list)
        assert len(result) > 0
    
    def test_get_template_list_structure(self):
        """Test that template list has correct structure"""
        result = get_template_list()
        
        for template in result:
            assert "key" in template
            assert "name" in template
            assert "description" in template
            assert isinstance(template["key"], str)
            assert isinstance(template["name"], str)
            assert isinstance(template["description"], str)
    
    def test_get_template_list_contains_all_templates(self):
        """Test that template list contains all registered templates"""
        result = get_template_list()
        keys = [t["key"] for t in result]
        
        assert "1" in keys
        assert "2" in keys
        assert "3" in keys
        assert "4" in keys
    
    def test_get_template_list_metadata(self):
        """Test that template list contains correct metadata"""
        result = get_template_list()
        
        # Find RAG template
        rag_template = next(t for t in result if t["key"] == "1")
        assert rag_template["name"] == "RAG Agent"
        assert "LangChain" in rag_template["description"]
        
        # Find FastAPI template
        fastapi_template = next(t for t in result if t["key"] == "2")
        assert fastapi_template["name"] == "FastAPI Web API"
        assert "REST API" in fastapi_template["description"]


class TestGetTemplateClass:
    """Tests for get_template_class function"""
    
    def test_get_template_class_valid_keys(self):
        """Test getting template class with valid keys"""
        assert get_template_class("1") == RAGAgentTemplate
        assert get_template_class("2") == FastAPITemplate
        assert get_template_class("3") == DataScienceTemplate
        assert get_template_class("4") == AutomationTemplate
    
    def test_get_template_class_invalid_key(self):
        """Test getting template class with invalid key raises ValueError"""
        with pytest.raises(ValueError, match="Unknown template"):
            get_template_class("999")
    
    def test_get_template_class_empty_key(self):
        """Test getting template class with empty key raises ValueError"""
        with pytest.raises(ValueError, match="Unknown template"):
            get_template_class("")
    
    def test_get_template_class_nonexistent_key(self):
        """Test getting template class with nonexistent key"""
        with pytest.raises(ValueError, match="Unknown template"):
            get_template_class("invalid")

