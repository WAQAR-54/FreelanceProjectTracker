from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Project(Base):
    __tablename__ = "projects"

    # 🆔 Unique project
    id = Column(Integer, primary_key=True, index=True)

    # 🧾 Core fields
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # 🔗 Link to Client (must match clients.id)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    # 📅 Timeline
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    # 📊 Status
    status = Column(String(50), default="planned")

    # 💰 Budget
    budget = Column(Integer, nullable=True)

    # 🚫 Soft delete
    is_deleted = Column(Integer, default=0)

    # 🔁 Relationships
    # IMPORTANT: yahan back_populates="projects" diya hai,
    # jiska opposite Client model me `projects` MUST exist (we added above)
    client = relationship("Client", back_populates="projects", lazy="joined")

    # Tasks ke liye opposite side Task.project me back_populates="project" diya hoga,
    # to yahan `tasks` zaroori hai:
    tasks = relationship("Task", back_populates="project", lazy="selectin", cascade="all, delete-orphan")