"""Task Automation and Scripting template"""
from rich.console import Console
from .base import ProjectTemplate

console = Console()


class AutomationTemplate(ProjectTemplate):
    """Template for Task Automation and Scripting"""
    
    name = "Task Automation"
    description = "Scripting and automation with CLI interface"
    
    def generate(self):
        console.print("[cyan]Creating Automation project...[/cyan]")
        
        # Create folders
        self.create_folder_structure(["src", "src/tasks", "logs"])
        
        # Dependencies (without extra quotes)
        deps = [
            '"click>=8.1.0"',
            '"requests>=2.31.0"',
            '"beautifulsoup4>=4.12.0"',
            '"python-dotenv>=1.0.0"',
            '"schedule>=1.2.0"',
            '"pyyaml>=6.0"',
        ]
        self.create_pyproject_toml(deps)
        
        # Create project files
        self._create_cli_interface()
        self._create_example_tasks()
        self.create_src_init()
        
        # Create README
        readme = f'''# {self.project_name}

A Python automation and scripting project for repetitive tasks.

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Run the CLI:
```bash
uv run python -m src.cli --help
```

## Project Structure

- `src/tasks/` - Individual automation tasks
- `scripts/` - Standalone scripts
- `logs/` - Task execution logs
- `data/` - Input/output data

## Usage

### Run a specific task:
```bash
uv run python -m src.cli run task-name
```

### List available tasks:
```bash
uv run python -m src.cli list
```

### Schedule a task:
```bash
uv run python -m src.cli schedule task-name --interval 3600
```

## Creating New Tasks

Add new tasks in `src/tasks/` by subclassing `Task`.

## Testing

```bash
uv run pytest
```
'''
        self.create_readme(readme)
        self.create_gitignore()
        self.create_basic_test()
        
        console.print("[green]✓ Automation project created successfully![/green]")
    
    def _create_cli_interface(self):
        content = '''#!/usr/bin/env python3
"""Main CLI interface for automation tasks"""
import click
from pathlib import Path
import importlib
import sys

@click.group()
def cli():
    """Task automation CLI"""
    pass

@cli.command()
def list():
    """List all available tasks"""
    tasks_dir = Path(__file__).parent / "tasks"
    click.echo("Available tasks:")
    for task_file in tasks_dir.glob("*.py"):
        if task_file.name != "__init__.py":
            click.echo(f"  - {task_file.stem}")

@cli.command()
@click.argument('task_name')
@click.option('--dry-run', is_flag=True, help='Simulate without executing')
def run(task_name, dry_run):
    """Run a specific task"""
    try:
        module = importlib.import_module(f"src.tasks.{task_name}")
        if hasattr(module, 'run'):
            click.echo(f"Running task: {task_name}")
            if dry_run:
                click.echo("[DRY RUN MODE]")
            module.run(dry_run=dry_run)
            click.echo("✓ Task completed")
        else:
            click.echo(f"Error: Task '{task_name}' has no run() function", err=True)
    except ModuleNotFoundError:
        click.echo(f"Error: Task '{task_name}' not found", err=True)

@cli.command()
@click.argument('task_name')
@click.option('--interval', default=3600, help='Interval in seconds')
def schedule(task_name, interval):
    """Schedule a task to run periodically"""
    click.echo(f"Scheduling '{task_name}' every {interval} seconds")
    # TODO: Implement scheduling logic
    click.echo("Note: Scheduling not yet implemented")

if __name__ == '__main__':
    cli()
'''
        with open(self.project_path / "src" / "cli.py", "w") as f:
            f.write(content)
    
    def _create_example_tasks(self):
        # File organizer task
        organizer_content = '''"""File organization task"""
from pathlib import Path
import shutil


def run(dry_run=False):
    """Organize files by extension"""
    source_dir = Path("data")
    
    if not source_dir.exists():
        print(f"Directory {source_dir} not found")
        return
    
    extensions = {}
    for file in source_dir.glob("*"):
        if file.is_file():
            ext = file.suffix or "no_extension"
            if ext not in extensions:
                extensions[ext] = []
            extensions[ext].append(file)
    
    for ext, files in extensions.items():
        target_dir = source_dir / ext.lstrip(".")
        print(f"Moving {len(files)} {ext} files to {target_dir}")
        
        if not dry_run:
            target_dir.mkdir(exist_ok=True)
            for file in files:
                shutil.move(str(file), str(target_dir / file.name))
'''
        with open(self.project_path / "src" / "tasks" / "file_organizer.py", "w") as f:
            f.write(organizer_content)
        
        # Web scraper task
        scraper_content = '''"""Web scraping task example"""
import requests
from bs4 import BeautifulSoup


def run(dry_run=False):
    """Scrape a website (example)"""
    url = "https://example.com"
    
    print(f"Scraping: {url}")
    
    if dry_run:
        print("[DRY RUN] Would fetch and parse the page")
        return
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title')
        
        print(f"Page title: {title.string if title else 'No title found'}")
    except Exception as e:
        print(f"Error: {e}")
'''
        with open(self.project_path / "src" / "tasks" / "web_scraper.py", "w") as f:
            f.write(scraper_content)
        
        (self.project_path / "src" / "tasks" / "__init__.py").touch()

