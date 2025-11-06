from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric  # ← SQLAlchemy column/data types import
from sqlalchemy.orm import relationship                                   # ← (Optional) agar aap relationship use karna chahein
from database import Base                                                  # ← Aapka declarative Base (database.py se)

class Invoice(Base):                                                       # ← SQLAlchemy model class jo ek table represent karti hai
    __tablename__ = "invoices"                                            # ← DB me table ka naam

    id = Column(Integer, primary_key=True, index=True)                    # ← Primary key (auto-increment), fast lookups ke liye index
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)  # ← Kis project ka invoice hai (FK to projects.id), required

    amount = Column(Numeric(12, 2), nullable=False)                       # ← Invoice amount (12 digits total, 2 decimals), required
    issued_date = Column(Date, nullable=False)                            # ← Invoice banne ki tareekh, required
    due_date = Column(Date, nullable=True)                                # ← Payment due date, optional

    paid_status = Column(String(20), default="unpaid")                    # ← Status: e.g., "paid" / "unpaid" / "overdue" etc.; default "unpaid"
    is_deleted = Column(Integer, default=0)                               # ← Soft delete flag: 0 = active, 1 = deleted

    # NOTE:
    # Agar aap Project model me `invoices = relationship("Invoice", ...)` add karna chahte hain
    # to yahan `back_populates="invoices"` use kar sakte hain. Filhal hum back_populates skip kar rahe
    # hain taa-ke Project model me changes ki dependency na bane.
    # project = relationship("Project", lazy="joined")                    # ← Optional: linked project eager load
