from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from app.core.constants import (MAX_NAME_LENGTH, MIN_DESCRIPTION_LENGTH,
                                MIN_NAME_LENGTH)


class CharityProjectBase(BaseModel):
    name: str = Field(
        ...,
        min_length=MIN_NAME_LENGTH,
        max_length=MAX_NAME_LENGTH,
    )
    description: str = Field(
        ...,
        min_length=MIN_DESCRIPTION_LENGTH,
    )
    full_amount: PositiveInt


class CharityProjectCreate(CharityProjectBase):
    model_config = ConfigDict(extra="forbid")


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(
        None,
        min_length=MIN_NAME_LENGTH,
        max_length=MAX_NAME_LENGTH,
    )
    description: Optional[str] = Field(
        None,
        min_length=MIN_DESCRIPTION_LENGTH,
    )
    full_amount: Optional[PositiveInt] = Field(
        None,
        gt=0)
    model_config = ConfigDict(extra="forbid")


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = Field(None)
    model_config = ConfigDict(from_attributes=True)