from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.documents.models import Document
from app.shared.exceptions import NotFound


class DocumentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, team_id: int, event_id: int, user_id: int, data: dict) -> Document:
        doc = Document(team_id=team_id, event_id=event_id, uploaded_by=user_id, **data)
        self.db.add(doc)
        await self.db.commit()
        await self.db.refresh(doc)
        return doc

    async def get_by_team(self, team_id: int) -> list[Document]:
        result = await self.db.execute(
            select(Document).where(Document.team_id == team_id).order_by(Document.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_id(self, doc_id: int) -> Document:
        result = await self.db.execute(select(Document).where(Document.id == doc_id))
        doc = result.scalar_one_or_none()
        if not doc:
            raise NotFound("Document not found")
        return doc

    async def update(self, doc_id: int, data: dict) -> Document:
        doc = await self.get_by_id(doc_id)
        for key, value in data.items():
            if value is not None:
                setattr(doc, key, value)
        doc.version += 1
        await self.db.commit()
        await self.db.refresh(doc)
        return doc

    async def delete(self, doc_id: int):
        doc = await self.get_by_id(doc_id)
        await self.db.delete(doc)
        await self.db.commit()

    async def search(self, event_id: int, q: str | None = None, tag: str | None = None, category: str | None = None) -> list[Document]:
        query = select(Document).where(Document.event_id == event_id)
        if q:
            query = query.where(Document.title.ilike(f"%{q}%"))
        if tag:
            query = query.where(Document.tags.any(tag))
        if category:
            query = query.where(Document.category == category)
        result = await self.db.execute(query.order_by(Document.created_at.desc()))
        return list(result.scalars().all())
