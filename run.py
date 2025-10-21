# run.py
import streamlit.web.cli as stcli
import sys

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "app/ui/file_upload_ui.py"]
    sys.exit(stcli.main())
