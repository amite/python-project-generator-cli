"""UI display functions for the CLI"""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from .templates import get_template_list

console = Console()


def display_welcome():
    """Display welcome message"""
    console.print(Panel.fit(
        "[bold cyan]Python Project Generator[/bold cyan]\n"
        "[dim]Generate well-structured Python projects with best practices[/dim]",
        border_style="cyan"
    ))


def display_project_types():
    """Display available project types"""
    table = Table(title="Available Project Types", box=box.ROUNDED)
    table.add_column("Type", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    
    templates = get_template_list()
    for template in templates:
        table.add_row(
            f"{template['key']}. {template['name']}",
            template['description']
        )
    
    console.print(table)


def display_success(project_name: str, project_path):
    """Display success message after project creation"""
    console.print()
    console.print(Panel.fit(
        f"[bold green]✓ Project created successfully![/bold green]\n\n"
        f"[cyan]Location:[/cyan] {project_path}\n"
        f"[cyan]Next steps:[/cyan]\n"
        f"  1. cd {project_name}\n"
        f"  2. uv sync\n"
        f"  3. Read the README.md for more information",
        border_style="green",
        title="Success"
    ))


def display_error(message: str):
    """Display an error message"""
    console.print(f"[red]{message}[/red]")

