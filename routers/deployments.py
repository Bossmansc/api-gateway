from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
import models, schemas
from dependencies import get_current_user

router = APIRouter(prefix="", tags=["Deployments"]) # Prefix handled in routes for nested structure

@router.post("/projects/{project_id}/deploy", response_model=schemas.Deployment)
def trigger_deployment(
    project_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Verify project ownership
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    # Create deployment
    new_deployment = models.Deployment(
        project_id=project_id,
        status="building",
        logs="Initializing deployment environment..."
    )
    db.add(new_deployment)
    db.commit()
    db.refresh(new_deployment)
    return new_deployment

@router.get("/deployments/{deployment_id}", response_model=schemas.Deployment)
def get_deployment_status(
    deployment_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Join with Project to verify ownership
    deployment = db.query(models.Deployment).join(models.Project).filter(
        models.Deployment.id == deployment_id,
        models.Project.user_id == current_user.id
    ).first()
    
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    return deployment

@router.get("/deployments/{deployment_id}/logs")
def get_deployment_logs(
    deployment_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    deployment = db.query(models.Deployment).join(models.Project).filter(
        models.Deployment.id == deployment_id,
        models.Project.user_id == current_user.id
    ).first()
    
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
        
    return {"logs": deployment.logs}

@router.post("/deployments/{deployment_id}/cancel", response_model=schemas.Deployment)
def cancel_deployment(
    deployment_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    deployment = db.query(models.Deployment).join(models.Project).filter(
        models.Deployment.id == deployment_id,
        models.Project.user_id == current_user.id
    ).first()
    
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    
    if deployment.status in ["live", "failed", "cancelled"]:
        raise HTTPException(status_code=400, detail="Deployment cannot be cancelled")
        
    deployment.status = "cancelled"
    deployment.logs += "\n[SYSTEM] Deployment cancelled by user."
    deployment.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(deployment)
    return deployment
