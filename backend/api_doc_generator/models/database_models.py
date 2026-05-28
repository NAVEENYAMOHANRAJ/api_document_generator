"""Database models for storing extraction results and history."""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Integer, DateTime, Text, JSON, Boolean, ForeignKey, Index, create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class ExtractionJob(Base):
    """Store extraction job history and results."""
    __tablename__ = "extraction_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)
    repo_url = Column(String, index=True)
    repo_name = Column(String)
    status = Column(String, default="pending")  # pending, processing, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime, nullable=True)
    total_endpoints = Column(Integer, default=0)
    processed_files = Column(Integer, default=0)
    failed_files = Column(Integer, default=0)
    errors = Column(JSON, default=list)
    job_metadata = Column(JSON, default=dict)


class Endpoint(Base):
    """Store extracted API endpoints."""
    __tablename__ = "endpoints"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, ForeignKey("extraction_jobs.job_id", ondelete="CASCADE"), index=True)
    method = Column(String, index=True)  # GET, POST, PUT, DELETE, etc.
    path = Column(String, index=True)
    description = Column(Text, nullable=True)
    source_file = Column(String)
    function_name = Column(String, nullable=True)
    path_params = Column(JSON, default=list)
    query_params = Column(JSON, default=list)
    request_body = Column(JSON, nullable=True)
    response_model = Column(JSON, nullable=True)
    responses = Column(JSON, default=list)
    tags = Column(JSON, default=list)
    deprecated = Column(Boolean, default=False)
    confidence = Column(Integer, default=85)  # 0-100
    provenance = Column(JSON, nullable=True)  # Store framework, detection_type, line_number, etc.
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_endpoints_job_id_method_path", "job_id", "method", "path"),
    )


class Documentation(Base):
    """Store generated documentation."""
    __tablename__ = "documentation"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, ForeignKey("extraction_jobs.job_id", ondelete="CASCADE"), unique=True, index=True)
    openapi_spec = Column(JSON)
    markdown_doc = Column(Text)
    html_doc = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class Cache(Base):
    """Cache extraction results for quick retrieval."""
    __tablename__ = "cache"

    id = Column(Integer, primary_key=True, index=True)
    cache_key = Column(String, unique=True, index=True)
    data = Column(JSON)
    expires_at = Column(DateTime, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_cache_key_expires_at", "cache_key", "expires_at"),
    )


# Database initialization
import os
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./api_doc_generator.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    
    # Enable foreign key constraint support in SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
else:
    engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

