"""Template registry and exports"""
from typing import Dict, Type
from .base import ProjectTemplate
from .rag_agent import RAGAgentTemplate
from .fastapi import FastAPITemplate
from .data_science import DataScienceTemplate
from .automation import AutomationTemplate
from .simple_boilerplate import SimpleBoilerplateTemplate


# Template registry - automatically populated
TEMPLATE_REGISTRY: Dict[str, Type[ProjectTemplate]] = {
    "1": RAGAgentTemplate,
    "2": FastAPITemplate,
    "3": DataScienceTemplate,
    "4": AutomationTemplate,
    "5": SimpleBoilerplateTemplate,
}


def get_template_list():
    """Get a list of available templates with their metadata"""
    return [
        {"key": key, "name": cls.name, "description": cls.description}
        for key, cls in TEMPLATE_REGISTRY.items()
    ]


def get_template_class(template_key: str) -> Type[ProjectTemplate]:
    """Get a template class by its key"""
    if template_key not in TEMPLATE_REGISTRY:
        raise ValueError(f"Unknown template: {template_key}")
    return TEMPLATE_REGISTRY[template_key]


__all__ = [
    "ProjectTemplate",
    "RAGAgentTemplate",
    "FastAPITemplate",
    "DataScienceTemplate",
    "AutomationTemplate",
    "SimpleBoilerplateTemplate",
    "TEMPLATE_REGISTRY",
    "get_template_list",
    "get_template_class",
]

