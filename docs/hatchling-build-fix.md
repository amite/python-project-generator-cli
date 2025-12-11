# Hatchling Build System: Bug Fix Documentation

## What is Hatchling?

**Hatchling** is a modern, extensible Python build backend used for building Python packages. It's part of the [Hatch project](https://hatch.pypa.io/) and serves as an alternative to older build tools like `setuptools`.

### Key Features:
- **Modern build system**: Designed for PEP 517/518 compliance
- **Simple configuration**: Uses `pyproject.toml` for all build settings
- **Flexible**: Supports various project layouts (flat, src-layout, etc.)
- **Fast**: Optimized for performance
- **Extensible**: Plugin system for custom build behaviors

### How It Works:
When you specify `build-backend = "hatchling.build"` in your `pyproject.toml`, tools like `uv`, `pip`, and `build` use hatchling to:
1. **Discover packages**: Automatically find Python packages/modules to include
2. **Build wheels**: Create distributable `.whl` files
3. **Build source distributions**: Create `.tar.gz` source archives
4. **Handle metadata**: Extract and package project metadata

## The Bug

### Error Message:
```
ValueError: Unable to determine which files to ship inside the wheel using the following heuristics: 
https://hatch.pypa.io/latest/plugins/builder/wheel/#default-file-selection

The most likely cause of this is that there is no directory that matches the name of your project (python_project_generator).

At least one file selection option must be defined in the `tool.hatch.build.targets.wheel` table
```

### Root Cause:
The project structure had:
- Project name: `python-project-generator` (with hyphens)
- Code location: `src/main.py` (single file, not a package directory)
- Missing configuration: No `tool.hatch.build.targets.wheel` section in `pyproject.toml`
- Missing package marker: No `src/__init__.py` file

Hatchling's default heuristics look for:
1. A directory matching the project name (converting hyphens to underscores): `python_project_generator/`
2. Or explicit configuration telling it which packages/files to include

Since neither existed, hatchling couldn't determine what to package.

### Why It Failed:
- **No matching directory**: Hatchling expected `python_project_generator/` but found `src/main.py`
- **No explicit configuration**: The `tool.hatch.build.targets.wheel` table was missing
- **Not a package**: `src/` wasn't a Python package (no `__init__.py`)

## The Fix

### Solution Overview:
We needed to explicitly tell hatchling:
1. Which directory contains the packages to include
2. Make `src/` a proper Python package
3. Update the entry point to match the new package structure

### Changes Made:

#### 1. Added Hatchling Build Configuration
**File**: `pyproject.toml`

```toml
[tool.hatch.build.targets.wheel]
packages = ["src"]
```

**What it does**: Explicitly tells hatchling to include the `src` directory as a package in the wheel.

#### 2. Created Package Marker
**File**: `src/__init__.py` (new file)

```python
"""Python Project Generator package."""
```

**What it does**: Makes `src/` a proper Python package, allowing imports like `from src.main import main`.

#### 3. Updated Entry Point
**File**: `pyproject.toml`

**Before**:
```toml
[project.scripts]
pygenerate = "main:main"
```

**After**:
```toml
[project.scripts]
pygenerate = "src.main:main"
```

**What it does**: Updates the CLI entry point to match the new package structure (`src.main` instead of just `main`).

## Verification

After applying the fix:
1. ✅ `uv sync` completes successfully
2. ✅ Package builds without errors
3. ✅ CLI command `pygenerate` works correctly

## Key Takeaways

1. **Hatchling needs explicit configuration** when your project structure doesn't match its default heuristics
2. **Package structure matters**: Directories need `__init__.py` to be recognized as packages
3. **Entry points must match package structure**: If code is in `src/main.py`, the entry point should be `src.main:main`
4. **The `tool.hatch.build.targets.wheel` table** is essential for non-standard project layouts

## Alternative Solutions

Other ways to fix this (not used, but valid):

1. **Rename directory**: Move `src/main.py` → `python_project_generator/main.py`
   - Pros: Matches default heuristics
   - Cons: Requires restructuring the project

2. **Use `only-include`**: Specify exact files to include
   ```toml
   [tool.hatch.build.targets.wheel]
   only-include = ["src/main.py"]
   ```
   - Pros: More explicit
   - Cons: Less flexible, requires updating when adding files

3. **Use `force-include`**: Force include specific paths
   ```toml
   [tool.hatch.build.targets.wheel]
   force-include = ["src/"]
   ```
   - Pros: Simple
   - Cons: May include unwanted files

## References

- [Hatchling Documentation](https://hatch.pypa.io/latest/plugins/builder/wheel/)
- [PEP 517 - Build System Interface](https://peps.python.org/pep-0517/)
- [PEP 518 - Specifying Build Dependencies](https://peps.python.org/pep-0518/)

