import uuid
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from .. import db

class Tower(db.Model):
    __tablename__ = "towers"

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

    # Foreign key reference to Owner
    owner_id = db.Column(UUID(as_uuid=True), db.ForeignKey('owners.id', ondelete='CASCADE'), nullable=False)

    # Relationship to Owner
    owner = db.relationship('Owner', back_populates='towers')

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
