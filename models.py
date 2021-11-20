from enum import unique
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

db = SQLAlchemy()


class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.Text())
