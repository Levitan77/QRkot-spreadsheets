from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from app.core.db import Base


class CommonMixin:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CommonCharityMixin(CommonMixin, Base):
    __abstract__ = True
    full_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    invested_amount: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )
    fully_invested: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    create_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    close_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            'full_amount > 0',
            name='check_full_amount_positive',
        ),
        CheckConstraint(
            'full_amount >= invested_amount',
            name='check_full_amount_ge_invested_amount',
        ),
    )

    def __repr__(self):
        return (
            f'{type(self).__name__}(id={self.id}, '
            f'full_amount={self.full_amount}, '
            f'invested_amount={self.invested_amount}, '
            f'fully_invested={self.fully_invested}, '
            f'close_date={self.close_date})'
        )