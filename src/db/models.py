from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

class Base(DeclarativeBase): ...

class Crime(Base):
    __tablename__ = "crimes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    city: Mapped[str] = mapped_column(String(80))
    year: Mapped[int] = mapped_column(Integer)
    incidents: Mapped[int] = mapped_column(Integer)
