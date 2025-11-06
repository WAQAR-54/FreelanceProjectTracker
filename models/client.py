from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from database import Base

class Client(Base):
    __tablename__ = "clients"

    # 🆔 Unique client
    id = Column(Integer, primary_key=True, index=True)

    # 👤 Basic info
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True, unique=True)
    phone = Column(String(50), nullable=True)
    company_name = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)

    # 🚫 Soft delete
    is_deleted = Column(Integer, default=0)

    # 🔁 IMPORTANT: Project side se back_populates="client" diya hai,
    # is liye yahan opposite side MUST exist as `projects`
    projects = relationship(
        "Project",
        back_populates="client",
        lazy="selectin",
        cascade="all, delete-orphan"
    )

    # (optional) Agar tasks ko client se direct dekhna ho to yahan relationship define NAHIN karte.
    # Tasks Project se linked rehte hain.
