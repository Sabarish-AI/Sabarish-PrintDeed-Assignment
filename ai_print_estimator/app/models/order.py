import uuid
from sqlalchemy import Column, String, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    raw_input = Column(Text, nullable=False)
    input_type = Column(String, nullable=False)
    parsed_specs = Column(JSON, nullable=True)
    status = Column(String, nullable=False)