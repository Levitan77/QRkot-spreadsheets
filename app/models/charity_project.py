from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import MAX_NAME_LENGTH
from app.models.base import Base, CommonCharityMixin


class CharityProject(CommonCharityMixin, Base):
    name: Mapped[str] = mapped_column(
        String(MAX_NAME_LENGTH), unique=True, nullable=False
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
