from pydantic import BaseModel


class StaticInfoBase(BaseModel):
    key: str
    value: str


class StaticInfoRead(StaticInfoBase):
    id: int


class StaticInfoCreate(StaticInfoBase):
    pass


class StaticInfoUpdate(StaticInfoBase):
    pass
