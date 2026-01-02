from typing import List, Optional
from datetime import datetime
from sqlalchemy import String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from database import Base

# Using SQLAlchemy 2.0 Mapped syntax for type safety and better registry handling

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    projects: Mapped[List["Project"]] = relationship(back_populates="owner", cascade="all, delete-orphan")

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    github_url: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="active")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    owner: Mapped["User"] = relationship(back_populates="projects")
    deployments: Mapped[List["Deployment"]] = mapped_column(insert_default=[]) # Initialization safety
    deployments: Mapped[List["Deployment"]] = relationship(back_populates="project", cascade="all, delete-orphan")

class Deployment(Base):
    __tablename__ = "deployments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    status: Mapped[str] = mapped_column(String, default="pending")
    logs: Mapped[str] = mapped_column(Text, default="")
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    project: Mapped["Project"] = relationship(back_populates="deployments")
    
