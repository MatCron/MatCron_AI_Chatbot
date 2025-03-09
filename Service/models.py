from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
import uuid
from .database import Base

class User(Base):
    __tablename__ = "Users"

    Id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    OrgId = Column(String(36), ForeignKey("Organisations.Id"), nullable=False)
    FirstName = Column(String(50), nullable=False)
    LastName = Column(String(50), nullable=False)
    Password = Column(Text, nullable=False)
    Email = Column(String(100), nullable=True, unique=True)
    EmailVerified = Column(Boolean, nullable=False, default=False)
    UserRole = Column(Integer, nullable=True)
    ProfilePicture = Column(Text, nullable=True)
    Token = Column(Text, nullable=True)
    Status = Column(Integer, nullable=False, default=1)
