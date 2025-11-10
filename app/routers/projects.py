from __future__ import annotations

from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.projects import models, schemas


router = APIRouter(prefix="/projects", tags=["projects"])


def _serialize_project(project: models.Project) -> schemas.ProjectRead:
    return schemas.ProjectRead(
        id=project.id,
        title=project.title,
        short_description=project.short_description,
        full_description=project.full_description,
        images=[image.url for image in project.images],
        created_at=project.created_at,
        updated_at=project.updated_at,
    )


@router.post("/", response_model=schemas.ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    project_in: schemas.ProjectCreate,
    session: Session = Depends(get_session),
):
    project = models.Project(
        title=project_in.title,
        short_description=project_in.short_description,
        full_description=project_in.full_description,
    )

    for url in project_in.images:
        project.images.append(models.ProjectImage(url=url))

    session.add(project)
    session.commit()
    session.refresh(project)

    return _serialize_project(project)


@router.get("/", response_model=List[schemas.ProjectRead])
def list_projects(session: Session = Depends(get_session)):
    projects = session.execute(select(models.Project)).scalars().unique().all()
    return [_serialize_project(project) for project in projects]


@router.get("/{project_id}", response_model=schemas.ProjectRead)
def get_project(project_id: int, session: Session = Depends(get_session)):
    project = session.get(models.Project, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Проект с ID {project_id} не найден",
        )
    return _serialize_project(project)


@router.put("/{project_id}", response_model=schemas.ProjectRead)
def update_project(
    project_id: int,
    project_update: schemas.ProjectUpdate,
    session: Session = Depends(get_session),
):
    project = session.get(models.Project, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Проект с ID {project_id} не найден",
        )

    project.title = project_update.title
    project.short_description = project_update.short_description
    project.full_description = project_update.full_description

    if project_update.images is not None:
        project.images.clear()
        for url in project_update.images:
            project.images.append(models.ProjectImage(url=url))

    project.updated_at = datetime.utcnow()

    session.commit()
    session.refresh(project)

    return _serialize_project(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, session: Session = Depends(get_session)):
    project = session.get(models.Project, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Проект с ID {project_id} не найден",
        )

    session.delete(project)
    session.commit()

