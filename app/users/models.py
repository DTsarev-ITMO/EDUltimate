# from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text
from app.database import Base, uniq_str_an, float_def0_an, int_pk

class User(Base):
    id: Mapped[int_pk]
    name: Mapped[uniq_str_an]
    email: Mapped[uniq_str_an]
    password: Mapped[str]
    weight: Mapped[float_def0_an]
    LBS: Mapped[float_def0_an]
    fat_percentage: Mapped[float_def0_an]

    is_user: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_super_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"