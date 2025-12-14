
import os
import sys
from pathlib import Path

# Simulate Lambda Env
os.environ["MODEL_PATH"] = "/tmp/best_model.pt"
os.environ["AWS_LAMBDA_FUNCTION_NAME"] = "test-func"
os.environ["DYNAMODB_TABLE"] = "test-table"

print(f"Current Directory: {os.getcwd()}")
print(f"Python Path: {sys.path}")

try:
    print("\n--- Testing Imports ---")
    from src.api.main import app, PROJECT_ROOT
    print("✅ Successfully imported src.api.main")
    
    print("\n--- Testing Path Logic ---")
    print(f"PROJECT_ROOT: {PROJECT_ROOT}")
    
    # Calculate expected logic
    model_path_relative = os.getenv("MODEL_PATH", "models/best_model.pt")
    model_path_absolute = PROJECT_ROOT / model_path_relative
    
    print(f"Env MODEL_PATH: {model_path_relative}")
    print(f"Calculated Absolute Path: {model_path_absolute}")
    
    if str(model_path_absolute) == "/tmp/best_model.pt":
        print("✅ Path resolution is CORRECT (/tmp/best_model.pt)")
    else:
        print(f"❌ Path resolution is WRONG. Got: {model_path_absolute}")

except ImportError as e:
    print(f"❌ Import Failed: {e}")
    # Check if src exists
    if os.path.exists("src"):
        print("src directory exists.")
        if os.path.exists("src/__init__.py"):
            print("src/__init__.py exists.")
        else:
            print("src/__init__.py MISSING.")
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
