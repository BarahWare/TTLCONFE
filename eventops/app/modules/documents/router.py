from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.documents.schemas import DocumentCreate, DocumentResponse, DocumentUpdate
from app.modules.documents.service import DocumentService
from app.shared.exceptions import NotFound

router = APIRouter(tags=["documents"])


@router.get("/api/v1/teams/{team_id}/documents", response_model=list[DocumentResponse])
async def list_documents(team_id: int, db: AsyncSession = Depends(get_db)):
    service = DocumentService(db)
    return await service.get_by_team(team_id)


@router.post("/api/v1/teams/{team_id}/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
    team_id: int,
    body: DocumentCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = DocumentService(db)
    return await service.create(team_id, user.org_id, user.id, body.model_dump())


@router.get("/api/v1/documents/{doc_id}", response_model=DocumentResponse)
async def get_document(doc_id: int, db: AsyncSession = Depends(get_db)):
    service = DocumentService(db)
    try:
        return await service.get_by_id(doc_id)
    except NotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@router.patch("/api/v1/documents/{doc_id}", response_model=DocumentResponse)
async def update_document(doc_id: int, body: DocumentUpdate, db: AsyncSession = Depends(get_db)):
    service = DocumentService(db)
    try:
        return await service.update(doc_id, body.model_dump(exclude_none=True))
    except NotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@router.delete("/api/v1/documents/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(doc_id: int, db: AsyncSession = Depends(get_db)):
    service = DocumentService(db)
    try:
        await service.delete(doc_id)
    except NotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@router.get("/api/v1/events/{event_id}/documents/search", response_model=list[DocumentResponse])
async def search_documents(
    event_id: int,
    q: str | None = None,
    tag: str | None = None,
    category: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    service = DocumentService(db)
    return await service.search(event_id, q=q, tag=tag, category=category)
