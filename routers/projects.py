from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models, schemas
from dependencies import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=List[schemas.Project])
def get_projects(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    projects = db.query(models.Project).filter(models.Project.user_id == current_user.id).offset(skip).limit(limit).all()
    return projects

@router.post("/", response_model=schemas.Project)
def create_project(
    project: schemas.ProjectCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_project = models.Project(**project.model_dump(), user_id=current_user.id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.get("/{project_id}", response_model=schemas.Project)
def get_project(
    project_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id, 
        models.Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=schemas.Project)
def update_project(
    project_id: int,
    project_update: schemas.ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    update_data = project_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)
    
    db.commit()
    db.refresh(project)
    return project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()
    return None
