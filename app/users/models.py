# from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from app.database import Base, uniq_str_an, float_def0_an

class User(Base):
    username: Mapped[uniq_str_an]
    email: Mapped[uniq_str_an]
    password: Mapped[str]
    weight: Mapped[float_def0_an]
    LBS: Mapped[float_def0_an]
    fat_percentage: Mapped[float_def0_an]
    # ration_id: Mapped[int | None] = mapped_column(ForeignKey('profiles.id'))

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.username})"

    def __repr__(self):
        return str(self)