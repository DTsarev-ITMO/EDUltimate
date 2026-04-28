from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, ForeignKey
from app.database import Base, uniq_str_an, float_def0_an
import enum

class User(Base):
    name: Mapped[uniq_str_an]
    email: Mapped[uniq_str_an]
    password: Mapped[str]

    # is_user: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    # is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    # is_super_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)

    # extend_existing = True

    # Односторонняя связь 1:1 с Diet
    diet: Mapped["Diet"] = relationship(back_populates="user", uselist=False)

    # Односторонняя связь 1:1 с UserData
    userData: Mapped["UserData"] = relationship(back_populates="user", uselist=False)

    # Односторонняя связь 1:1 с UserStatus
    userStatus: Mapped["UserStatus"] = relationship(back_populates="user", uselist=False)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"

    def __repr__(self):
        return str(self)

class UserData(Base):
    __tablename__ = "user_data"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    weight: Mapped[float_def0_an]
    fat_percentage: Mapped[float_def0_an]

    # extend_existing = True

    # Связь 1:1 с User
    user: Mapped["User"] = relationship(back_populates="userData", uselist=False)

    # Вычислительные свойства
    @property
    def lean_body_mass(self) -> float:
        return self.weight * (100 - self.fat_percentage) / 100

class UserAdminStatus(enum.Enum):
    USER = "user"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"

class UserStatus(Base):
    __tablename__ = "user_status"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    status: Mapped[UserAdminStatus] = mapped_column(Enum(UserAdminStatus), default=UserAdminStatus.USER)

    # Связь 1:1 с User
    user: Mapped["User"] = relationship(back_populates="userStatus", uselist=False)