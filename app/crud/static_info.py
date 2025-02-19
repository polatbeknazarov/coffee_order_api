from .base import BaseDAO
from core.models import StaticInfo
from core.schemas import StaticInfoBase


class StaticInfoDAO(BaseDAO[StaticInfo, StaticInfoBase]):
    model = StaticInfo
