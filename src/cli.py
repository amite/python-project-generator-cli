"""CLI interface and user interaction logic"""
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from .ui import display_welcome, display_project_types, display_success, display_error
from .templates import get_template_class, TEMPLATE_REGISTRY

console = Console()


def validate_project_name(project_name: str) -> bool:
    """Validate project name contains only valid characters"""
    return project_name.replace("_", "").replace("-", "").isalnum()


def get_project_type() -> str:
    """Prompt user to select project type"""
    valid_choices = list(TEMPLATE_REGISTRY.keys())
    return Prompt.ask(
        "[cyan]Select project type[/cyan]",
        choices=valid_choices,
        default="1"
    )


def get_project_name() -> str:
    """Prompt user for project name"""
    return Prompt.ask(
        "[cyan]Enter project name[/cyan]",
        default="my_project"
    )


def get_project_path(project_name: str) -> Path:
    """Prompt user for project path"""
    default_path = Path.cwd() / project_name
    path_input = Prompt.ask(
        "[cyan]Enter project path[/cyan]",
        default=str(default_path)
    )
    return Path(path_input)


def confirm_overwrite(project_path: Path) -> bool:
    """Ask user to confirm overwriting existing directory"""
    return Confirm.ask(
        f"[yellow]Directory {project_path} already exists. Overwrite?[/yellow]",
        default=False
    )


def run_cli():
    """Main CLI function"""
    # Display welcome screen
    display_welcome()
    console.print()
    display_project_types()
    console.print()
    
    # Get project type
    project_type = get_project_type()
    
    # Get project name
    project_name = get_project_name()
    
    # Validate project name
    if not validate_project_name(project_name):
        display_error("Error: Project name should contain only letters, numbers, hyphens, and underscores")
        return
    
    # Get project path
    project_path = get_project_path(project_name)
    
    # Check if directory exists
    if project_path.exists():
        if not confirm_overwrite(project_path):
            console.print("[yellow]Operation cancelled[/yellow]")
            return
    
    # Create project directory
    project_path.mkdir(parents=True, exist_ok=True)
    
    # Generate project based on type
    try:
        template_class = get_template_class(project_type)
        template = template_class(project_name, project_path)
        template.generate()
        
        # Display success message
        display_success(project_name, project_path)
        
    except Exception as e:
        display_error(f"Error creating project: {e}")
        import traceback
        console.print(traceback.format_exc())

