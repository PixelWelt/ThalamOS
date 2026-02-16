from datetime import datetime
from typing import Optional
from sqlmodel import Field
from sqlmodel import SQLModel
from enum import Enum

class StorageItemType(str, Enum):
    SENSOR = "SENSOR"
    SCREW = "SCREW"
    DISPLAY = "DISPLAY"
    NAIL = "NAIL"
    CABLE = "CABLE"
    MISCELLANEOUS = "MISCELLANEOUS"

class StorageItem(SQLModel, table=True):
    __tablename__ = "storage"
    id: Optional[int] = Field(default=None, primary_key=True)
    position: int
    type: StorageItemType
    name: str
    info: Optional[str] = None
    modification_time: datetime = Field(default_factory=datetime.now)


