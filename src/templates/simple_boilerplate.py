"""Simple Py Boilerplate template"""
from rich.console import Console
from .base import ProjectTemplate

console = Console()


class SimpleBoilerplateTemplate(ProjectTemplate):
    """Template for Simple Py Boilerplate - minimal Python project with testing infrastructure"""
    
    name = "Simple Py Boilerplate"
    description = "Minimal Python project with testing infrastructure and main.py"
    
    def generate(self):
        console.print("[cyan]Creating Simple Py Boilerplate project...[/cyan]")
        
        # Create folders (common folders + src)
        self.create_folder_structure(["src"])
        
        # No runtime dependencies - empty list
        deps = []
        self.create_pyproject_toml(deps)
        
        # Create main.py
        self._create_main_py()
        self.create_src_init()
        
        # Create README
        readme = f'''# {self.project_name}

A simple Python project boilerplate with testing infrastructure.

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Run the project:
```bash
uv run python -m src.main
```

## Project Structure

- `src/main.py` - Main entry point
- `tests/` - Test files
- Common project folders for organization

## Testing

Run tests with:
```bash
uv run pytest
```

## Development

This is a minimal boilerplate project. Add your code to `src/main.py` and tests to `tests/`.
'''
        self.create_readme(readme)
        self.create_gitignore()
        self.create_basic_test()
        
        console.print("[green]✓ Simple Py Boilerplate project created successfully![/green]")
    
    def _create_main_py(self):
        """Create src/main.py with simple boilerplate"""
        content = '''"""Main entry point for the project"""


def main():
    """Main function"""
    print("Hello, World!")


if __name__ == "__main__":
    main()
'''
        with open(self.project_path / "src" / "main.py", "w") as f:
            f.write(content)
