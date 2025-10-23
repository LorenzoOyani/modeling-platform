# run.py
"""
Universal entry point for Modeling Platform
Usage:
    python run.py                    # Runs file_upload_ui.py (default)
    python run.py formula            # Runs formula_run_ui.py
    python run.py file_upload        # Runs file_upload_ui.py
"""
import sys
import os
import streamlit.web.cli as stcli

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app.db import init_db

# Map UI names to files
UI_FILES = {
    'file_upload': 'app/ui/file_upload_ui.py',
    'formula': 'app/ui/formula_run_ui.py',
    'default': 'app/ui/file_upload_ui.py'
}

# Initialize database
print("Initializing database...")
init_db()
print("✓ Database ready!")

if __name__ == "__main__":
    # Get UI name from command line argument
    ui_name = sys.argv[1] if len(sys.argv) > 1 else 'default'
    ui_file = UI_FILES.get(ui_name, UI_FILES['default'])

    print(f"Starting {ui_name} UI...")
    sys.argv = ["streamlit", "run", ui_file]
    sys.exit(stcli.main())