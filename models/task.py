from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Task(Base):
    __tablename__ = "tasks"

    # 🆔 Unique task
    id = Column(Integer, primary_key=True, index=True)

    # 🔗 Link to Project (must match projects.id)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    # 🧾 Details
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # 👤 Assignment
    assigned_to = Column(String(100), nullable=True)

    # 📅 Due date
    due_date = Column(Date, nullable=True)

    # ✅ Completion flag
    completed = Column(Boolean, default=False)

    # 🚫 Soft delete
    is_deleted = Column(Integer, default=0)

    # 🔁 Opposite of Project.tasks
    project = relationship("Project", back_populates="tasks", lazy="joined")