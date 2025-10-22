from app.db import get_db_session, UploadFile
from app.core.file_handler import FileHandler
from typing import List, Optional, Dict
import os


class FileService:
    """Service layer that combines file system operations with database operations"""

    @staticmethod
    def upload_and_save_file(uploaded_file) -> Optional[UploadFile]:
        """
        Complete file upload workflow:
        1. Validate file
        2. Save to disk
        3. Save metadata to database

        Args:
            uploaded_file: Streamlit UploadedFile object

        Returns:
            UploadFile: Database record or None if failed
        """
        # Validate file type
        if not FileHandler.is_allowed_file(uploaded_file.name):
            print(f"File type not allowed: {uploaded_file.name}")
            return None

        # Save file to disk
        file_info = FileHandler.save_uploaded_file(uploaded_file)

        # Save metadata to database
        db = get_db_session()
        try:
            db_file = UploadFile(
                filename=file_info['saved_filename'],
                filePath=file_info['filepath'],
                file_type=file_info['file_type']
            )
            db.add(db_file)
            db.commit()
            db.refresh(db_file)
            return db_file
        except Exception as e:
            print(f"Error saving to database: {e}")
            # Rollback database transaction
            db.rollback()
            # Clean up uploaded file
            FileHandler.delete_file(file_info['filepath'])
            return None
        finally:
            db.close()

    @staticmethod
    def get_all_files() -> List[UploadFile]:
        """Get all uploaded files from database"""
        db = get_db_session()
        try:
            return db.query(UploadFile).all()
        finally:
            db.close()

    @staticmethod
    def get_file_by_id(self, file_id: str) -> Optional[UploadFile]:
        """get specific file by id"""
        db = get_db_session()
        try:
            return db.query(UploadFile).filter(UploadFile.id == file_id).first()

        finally:
            db.close()

    @staticmethod
    def get_file_with_preview(file_id: str, rows: int = 5) -> Optional[Dict]:
        """
        Get file record with preview data

        Returns:
            dict: {
                'file': UploadFile object,
                'preview': DataFrame,
                'metadata': dict
            }
        """
        db_file = FileService.get_file_by_id(file_id)
        if not db_file:
            return None

        preview = FileHandler.preview_file(db_file.filePath, rows)
        metadata = FileHandler.get_file_metadata(db_file.filePath)

        return {
            'file': db_file,
            'preview': preview,
            'metadata': metadata
        }

    @staticmethod
    def delete_file(file_id: str) -> bool:
        """
        Delete file completely:
        1. Remove from database
        2. Delete from disk
        """
        db = get_db_session()
        try:
            file = db.query(UploadFile).filter(UploadFile.id == file_id).first()
            if file:
                # Delete from disk first
                FileHandler.delete_file(file.filePath)

                # Delete from database
                db.delete(file)
                db.commit()
                return True
            return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            db.rollback()
            return False
        finally:
            db.close()

    @staticmethod
    def search_files_by_name(search_term: str) -> List[UploadFile]:
        """Search files by filename"""
        db = get_db_session()
        try:
            return db.query(UploadFile).filter(
                UploadFile.filename.contains(search_term)
            ).all()
        finally:
            db.close()
