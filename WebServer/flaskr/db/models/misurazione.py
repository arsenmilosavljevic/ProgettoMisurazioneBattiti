from ..base import *
from sqlalchemy import DateTime 
from datetime import datetime,timezone
from .user import User


class Misurazione(Base):
    __tablename__ = "Misurazione"

    bpmMedi: Mapped[int] = mapped_column(int, nullable=False)
    bpmMax: Mapped[int] = mapped_column(int, nullable=False)
    bpmMin: Mapped[int] = mapped_column(int, nullable=False)
    data: Mapped[datetime] = mapped_column(DateTime, default=lambda:datetime.now(timezone.utc))
    user_id: Mapped[str] = mapped_column(ForeignKey("User.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="misurazioni")

    def __new__(cls, session=None, **kwargs):
        if session and "user_id" in kwargs and "data" in kwargs:
            query = select(cls).where(
                cls.user_id == kwargs["user_id"],
                cls.data == kwargs["data"]
            )
            record = session.execute(query).scalars().first()
            if record:
                return record  
        record = super().__new__(cls)
        record.__init__(**kwargs)
        return record

    @classmethod
    def get_by_user(cls, session, user_id, ordina=True):
        query = select(cls).where(cls.user_id == user_id)
        if ordina:
            query = query.order_by(desc(cls.data))
        return session.execute(query).scalars().all()