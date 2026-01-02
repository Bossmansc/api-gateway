from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Deployment Schemas ---
class DeploymentBase(BaseModel):
    pass

class DeploymentCreate(DeploymentBase):
    pass # Usually triggered without body or specific commit hash

class Deployment(DeploymentBase):
    id: int
    project_id: int
    status: str
    logs: Optional[str]
    started_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True

# --- Project Schemas ---
class ProjectBase(BaseModel):
    name: str
    github_url: str

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None

class Project(ProjectBase):
    id: int
    status: str
    user_id: int
    created_at: datetime
    deployments: List[Deployment] = []

    class Config:
        from_attributes = True
