import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'app/uploads')

ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS', 'csv,xlsx,xls').split(',')

class FileHandler:
    """Handles file upload and validation"""

    @staticmethod
    def is_allowed_file(filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @staticmethod
    def generate_timestamped_filename(original_filename):
        """Generate filename with timestamp"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name, ext = os.path.splitext(original_filename)
        # Clean the filename (remove special characters)
        clean_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
        return f"{clean_name}_{timestamp}{ext}"

    @staticmethod
    def save_uploaded_file(uploaded_file):
        """
        Save uploaded file to disk

        Args:
            uploaded_file: Streamlit UploadedFile object

        Returns:
            dict: File information (filepath, size, etc.)
        """
        # Ensure upload directory exists
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        # Generate timestamped filename
        new_filename = FileHandler.generate_timestamped_filename(uploaded_file.name)
        filepath = os.path.join(UPLOAD_FOLDER, new_filename)

        # Save file
        with open(filepath, 'wb') as f:
            f.write(uploaded_file.getbuffer())

        # Get file info
        file_size = os.path.getsize(filepath)
        file_type = uploaded_file.name.rsplit('.', 1)[1].lower()

        return {
            'original_filename': uploaded_file.name,
            'saved_filename': new_filename,
            'filepath': filepath,
            'file_size': file_size,
            'file_type': file_type
        }

    @staticmethod
    def get_file_metadata(filepath):
        """
        Extract metadata from file (row count, column count)

        Args:
            filepath: Path to the file

        Returns:
            dict: Metadata (row_count, column_count, columns)
        """
        try:
            file_ext = filepath.rsplit('.', 1)[1].lower()

            if file_ext == 'csv':
                df = pd.read_csv(filepath)
            elif file_ext in ['xlsx', 'xls']:
                df = pd.read_excel(filepath)
            else:
                return None

            return {
                'row_count': len(df),
                'column_count': len(df.columns),
                'columns': list(df.columns)
            }
        except Exception as e:
            print(f"Error reading file metadata: {e}")
            return None

    @staticmethod
    def preview_file(filepath, rows=5):
        """
        Get preview of file data

        Args:
            filepath: Path to the file
            rows: Number of rows to preview

        Returns:
            pandas.DataFrame: Preview data
        """
        try:
            file_ext = filepath.rsplit('.', 1)[1].lower()

            if file_ext == 'csv':
                df = pd.read_csv(filepath, nrows=rows)
            elif file_ext in ['xlsx', 'xls']:
                df = pd.read_excel(filepath, nrows=rows)
            else:
                return None

            return df
        except Exception as e:
            print(f"Error previewing file: {e}")
            return None