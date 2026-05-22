from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, PositiveInt


class DonationBase(BaseModel):
    full_amount: Optional[PositiveInt] = None
    comment: Optional[str] = None


class DonationCreate(DonationBase):
    full_amount: PositiveInt
    model_config = ConfigDict(extra='forbid')


class DonationDB(DonationCreate):
    id: int
    create_date: datetime
    model_config = ConfigDict(from_attributes=True)


class DonationFullInfoDB(DonationDB):
    invested_amount: int = 0
    fully_invested: bool = False
    close_date: Optional[datetime] = None
    user_id: int
    model_config = ConfigDict(from_attributes=True)
