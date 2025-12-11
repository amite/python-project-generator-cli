# Python Project Generator CLI

A beautiful and functional command-line tool for scaffolding Python projects with best practices and standardized structure.

## Features

- 🎨 **Pretty CLI Interface** - Built with Rich for beautiful terminal output
- 🚀 **4 Project Templates** - RAG agents, FastAPI APIs, Data Science/ML, and Task Automation
- 📦 **UV Package Manager** - Modern, fast Python package management
- 🧪 **Test Suite Included** - Every generated project comes with pytest tests
- 📚 **Comprehensive Documentation** - Generated READMEs for each project
- 🏗️ **Standardized Structure** - Consistent folder organization across all projects
- 🔧 **Modular & Extensible** - Easy to add new project templates

## Installation

### Option 1: Global Installation (Recommended)

Install the CLI globally using `pipx` (recommended for CLI tools):

```bash
# Install pipx if you don't have it
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Install the generator globally
pipx install -e .
```

After installation, you can run `gen` from anywhere:

```bash
gen
```

### Option 2: Local Development

For local development or if you prefer not to install globally:

1. Clone or download this repository
2. Install dependencies using uv:

```bash
uv sync
```

## Usage

### If Installed Globally

Simply run:

```bash
gen
```

### If Using Locally

Run the generator:

```bash
uv run python src/main.py
```

Or make it executable:

```bash
chmod +x src/main.py
./src/main.py
```

Follow the interactive prompts to:
1. Select a project type
2. Enter a project name
3. Choose the project location
4. Generate your project!

## Project Templates

### 1. RAG Agent (LangChain + Streamlit)

Perfect for building Retrieval-Augmented Generation applications.

**Includes:**
- LangChain for agent orchestration
- Streamlit web interface with chat UI
- Qdrant vector database integration
- Ollama for local LLM inference
- Data generation scripts
- Environment configuration

**Use cases:** Chatbots, document Q&A systems, knowledge bases

### 2. FastAPI Web API

Production-ready REST API with modern Python stack.

**Includes:**
- FastAPI framework
- SQLAlchemy ORM setup
- Authentication scaffolding
- Docker & docker-compose configuration
- Database migrations with Alembic
- CORS middleware

**Use cases:** Microservices, REST APIs, backend services

### 3. Data Science & Machine Learning

End-to-end ML project structure with model serving.

**Includes:**
- NumPy, pandas, scikit-learn
- Jupyter Lab integration
- Model training pipeline
- FastAPI model serving endpoint
- Data preprocessing utilities
- Visualization tools (matplotlib, seaborn)

**Use cases:** ML experiments, data analysis, model deployment

### 4. Task Automation & Scripting

CLI-based automation framework for repetitive tasks.

**Includes:**
- Click CLI framework
- Task scheduling capabilities
- Example tasks (file organization, web scraping)
- Logging system
- Modular task structure

**Use cases:** DevOps automation, data processing, workflow automation

## Project Structure

Every generated project includes:

```
project_name/
├── notebooks/           # Jupyter notebooks
├── artifacts/
│   ├── wip/            # Work in progress tasks
│   └── completed/      # Completed tasks
├── reports/            # Analysis reports
├── research/           # Learning materials and best practices
├── quality/            # Quality test tracking
├── scripts/            # Utility scripts
├── data/               # Data storage
├── tests/              # Test suite
├── pyproject.toml      # UV dependencies
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```

## Development

### Running Tests

The project includes a comprehensive test suite with 67+ tests covering unit tests, integration tests, and CLI interaction tests.

#### Run All Tests

```bash
uv run pytest
```

#### Run Tests with Verbose Output

```bash
uv run pytest -v
```

#### Run Specific Test Files

```bash
# Run CLI tests only
uv run pytest tests/test_cli.py

# Run template tests only
uv run pytest tests/test_templates.py

# Run integration tests only
uv run pytest tests/integration/

# Run UI tests only
uv run pytest tests/test_ui.py
```

#### Run Specific Test Classes or Functions

```bash
# Run a specific test class
uv run pytest tests/test_cli.py::TestValidateProjectName

# Run a specific test function
uv run pytest tests/test_cli.py::TestValidateProjectName::test_valid_project_names
```

#### Run Tests with Different Output Formats

```bash
# Show test coverage
uv run pytest --cov=src --cov-report=term-missing

# Generate HTML coverage report
uv run pytest --cov=src --cov-report=html
# Then open htmlcov/index.html in your browser

# Show short traceback format
uv run pytest --tb=short

# Show no output except failures
uv run pytest -q
```

#### Run Tests Matching a Pattern

```bash
# Run tests matching a keyword
uv run pytest -k "template"

# Run tests matching multiple keywords
uv run pytest -k "template and not integration"
```

#### Run Tests in Parallel (faster)

```bash
# Install pytest-xdist first: uv add --dev pytest-xdist
uv run pytest -n auto
```

#### Test Structure

The test suite is organized as follows:

```
tests/
├── __init__.py
├── conftest.py              # Pytest fixtures and utilities
├── test_cli.py              # CLI function tests
├── test_templates.py         # Template base class tests
├── test_template_registry.py # Template registry tests
├── test_ui.py                # UI display function tests
└── integration/
    ├── __init__.py
    └── test_template_generation.py  # Full project generation tests
```

#### Test Coverage

The test suite covers:
- **CLI Functions**: Validation, user input, path handling, overwrite confirmation
- **Template Base Class**: Folder creation, file generation, error handling
- **Template Registry**: Template discovery and retrieval
- **UI Functions**: Display functions and console output
- **Integration Tests**: Full project generation for all template types

### Running with Coverage

Generate a coverage report to see which parts of the code are tested:

```bash
# Terminal report with missing lines
uv run pytest --cov=src --cov-report=term-missing

# HTML report (opens in browser)
uv run pytest --cov=src --cov-report=html
open htmlcov/index.html  # or on Linux: xdg-open htmlcov/index.html

# XML report (for CI/CD)
uv run pytest --cov=src --cov-report=xml
```

### Code Formatting

```bash
# Format code with black
uv run black src tests

# Check code style with ruff
uv run ruff check src tests

# Auto-fix ruff issues
uv run ruff check --fix src tests
```

## Extending with New Templates

To add a new project template:

1. Create a new class inheriting from `ProjectTemplate`:

```python
class MyTemplate(ProjectTemplate):
    def generate(self):
        # Your generation logic here
        self.create_folder_structure(["custom", "folders"])
        self.create_pyproject_toml(["dependency1", "dependency2"])
        # Create custom files
        self.create_readme(readme_content)
        self.create_gitignore()
        self.create_basic_test()
```

2. Add it to the `templates` dictionary in `main()`:

```python
templates = {
    "1": RAGAgentTemplate,
    "2": FastAPITemplate,
    "3": DataScienceTemplate,
    "4": AutomationTemplate,
    "5": MyTemplate,  # Add your template
}
```

3. Update the display table in `display_project_types()`

## Requirements

- Python 3.10+
- uv package manager
- Rich library for terminal formatting

## Contributing

Contributions are welcome! Feel free to:
- Add new project templates
- Improve existing templates
- Fix bugs
- Enhance documentation

## License

MIT License - feel free to use this for any purpose.

## Acknowledgments

Built with:
- [UV](https://github.com/astral-sh/uv) - Fast Python package manager
- [Rich](https://github.com/Textualize/rich) - Beautiful terminal formatting
- [Click](https://click.palletsprojects.com/) - CLI framework (used in generated projects)

---

**Happy Coding! 🚀**