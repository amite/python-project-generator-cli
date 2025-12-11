"""Shared constants and configuration values"""

# Common development dependencies used across all templates
DEV_DEPENDENCIES = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.7.0",
    "ruff>=0.0.285",
    "ipykernel>=7.1.0",
]

# Default Python version requirement
PYTHON_VERSION = ">=3.10"

# Build system configuration
BUILD_SYSTEM = {
    "requires": ["hatchling"],
    "build_backend": "hatchling.build"
}

# Common folder structure for all projects
COMMON_FOLDERS = [
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

