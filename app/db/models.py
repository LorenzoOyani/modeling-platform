from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class UploadFile(Base):
    __tablename__ = 'uploaded files'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, nullable=False)
    filePath = Column(String, nullable=False, unique=True)
    upload_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    file_type = Column(String, nullable=False)

    def __repr__(self):
        return f"<UploadedFile(id={self.id}, filename='{self.filename}', file_type='{self.file_type}')>"

    # def to_dict(self):
    #     """convert to dictionary"""
    #
    #     return {
    #         'id': self.id,
    #         'filename': self.filename,
    #         'filePath': self.filePath,
    #         'fileType': self.file_type,
    #         'upload_time': self.upload_time,
    #
    #     }


