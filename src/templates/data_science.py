"""Data Science and ML project template"""
from rich.console import Console
from .base import ProjectTemplate

console = Console()


class DataScienceTemplate(ProjectTemplate):
    """Template for Data Science/ML projects"""
    
    name = "Data Science/ML"
    description = "ML project with scikit-learn, pandas, and model serving API"
    
    def generate(self):
        console.print("[cyan]Creating Data Science project...[/cyan]")
        
        # Create folders
        self.create_folder_structure([
            "src",
            "src/data",
            "src/features",
            "src/models",
            "models",
            "data/raw",
            "data/processed",
        ])
        
        # Dependencies (without extra quotes)
        deps = [
            '"numpy>=1.24.0"',
            '"pandas>=2.0.0"',
            '"scikit-learn>=1.3.0"',
            '"matplotlib>=3.7.0"',
            '"seaborn>=0.12.0"',
            '"jupyter>=1.0.0"',
            '"jupyterlab>=4.0.0"',
            '"fastapi>=0.104.0"',
            '"uvicorn[standard]>=0.24.0"',
            '"joblib>=1.3.0"',
        ]
        self.create_pyproject_toml(deps)
        
        # Create project files
        self._create_data_pipeline()
        self._create_model_training()
        self._create_api_server()
        self.create_src_init()
        
        # Create README
        readme = f'''# {self.project_name}

A Data Science and Machine Learning project with end-to-end pipeline.

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Launch Jupyter Lab:
```bash
uv run jupyter lab
```

## Project Structure

- `src/data/` - Data loading and processing
- `src/features/` - Feature engineering
- `src/models/` - Model training and evaluation
- `models/` - Saved model artifacts
- `notebooks/` - Jupyter notebooks for exploration
- `data/` - Data storage (raw and processed)

## Workflow

1. **Data Ingestion**: Load and explore data in notebooks
2. **Feature Engineering**: Create features using scripts in `src/features/`
3. **Model Training**: Train models using `src/models/train.py`
4. **Deployment**: Serve model via FastAPI

## Model API

Start the model serving API:
```bash
uv run python src/models/serve.py
```

## Testing

```bash
uv run pytest
```
'''
        self.create_readme(readme)
        self.create_gitignore()
        self.create_basic_test()
        
        console.print("[green]✓ Data Science project created successfully![/green]")
    
    def _create_data_pipeline(self):
        content = '''"""Data loading and processing utilities"""
import pandas as pd
from pathlib import Path


def load_data(filepath: str) -> pd.DataFrame:
    """Load data from file"""
    path = Path(filepath)
    
    if path.suffix == '.csv':
        return pd.read_csv(filepath)
    elif path.suffix in ['.xlsx', '.xls']:
        return pd.read_excel(filepath)
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Basic preprocessing"""
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Handle missing values (placeholder)
    df = df.fillna(df.mean(numeric_only=True))
    
    return df
'''
        with open(self.project_path / "src" / "data" / "loader.py", "w") as f:
            f.write(content)
        
        (self.project_path / "src" / "data" / "__init__.py").touch()
        (self.project_path / "src" / "features" / "__init__.py").touch()
        (self.project_path / "src" / "models" / "__init__.py").touch()
    
    def _create_model_training(self):
        content = '''"""Model training script"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
from pathlib import Path


def train_model(X, y, model_path: str = "models/model.joblib"):
    """Train a model and save it"""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    score = model.score(X_test, y_test)
    print(f"Model accuracy: {score:.4f}")
    
    # Save model
    Path(model_path).parent.mkdir(exist_ok=True)
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
    
    return model


if __name__ == "__main__":
    # Example usage
    from sklearn.datasets import make_classification
    X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
    train_model(X, y)
'''
        with open(self.project_path / "src" / "models" / "train.py", "w") as f:
            f.write(content)
    
    def _create_api_server(self):
        content = '''"""Model serving API"""
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from pathlib import Path

app = FastAPI(title="ML Model API")

# Load model (placeholder)
MODEL_PATH = Path(__file__).parent.parent.parent / "models" / "model.joblib"
model = None

@app.on_event("startup")
def load_model():
    global model
    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)
    else:
        print("Model not found. Train a model first.")

class PredictionInput(BaseModel):
    features: list

class PredictionOutput(BaseModel):
    prediction: int
    probability: float

@app.post("/predict", response_model=PredictionOutput)
def predict(input_data: PredictionInput):
    if model is None:
        return {"error": "Model not loaded"}
    
    prediction = model.predict([input_data.features])[0]
    probability = float(max(model.predict_proba([input_data.features])[0]))
    
    return PredictionOutput(prediction=int(prediction), probability=probability)

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        with open(self.project_path / "src" / "models" / "serve.py", "w") as f:
            f.write(content)

