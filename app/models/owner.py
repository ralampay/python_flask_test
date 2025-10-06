import uuid
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from .. import db

class Owner(db.Model):
    __tablename__ = "owners"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(255),
        nullable=False,
        unique=True
    )

    # Relationship to Tower
    towers = db.relationship('Tower', back_populates='owner', cascade='all, delete-orphan')

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
