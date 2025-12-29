from typing import Any, Self
from uuid import UUID

from pydantic import BaseModel, model_validator


class AdvertisementStatistics(BaseModel):
    likes: int
    viewCount: int
    contacts: int


class AdvertisementStatisticsResponse(BaseModel):
    ad_statistics: list[AdvertisementStatistics]


class Advertisement(BaseModel):
    name: str
    price: int
    statistics: AdvertisementStatistics


class AdvertisementResponse(Advertisement):
    id: UUID
    createdAt: str # Should be datetime, but API has bug with tz


class AdvertisementListResponse(BaseModel):
    advertisements: list[AdvertisementResponse]


class AdvertisementCreateResponse(BaseModel):
    status: str

    @model_validator(mode="after")
    def validate(self, value: Any) -> Self:
        assert self.status.split("-")[0] == "Сохранили объявление "
        assert is_valid_uuid(self.status.split("-", 1)[1].replace(" ", ""))
        return self

    def get_uuid(self) -> UUID:
        return UUID(self.status.split("-", 1)[1].replace(" ", ""))


def is_valid_uuid(value: str) -> bool:
    try:
        UUID(value)
        return True
    except ValueError:
        return False
