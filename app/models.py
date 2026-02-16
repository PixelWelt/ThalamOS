"""
Models Module

This module defines the database models using SQLModel and Pydantic.
It includes the StorageItem model and the StorageItemType enumeration.
"""
from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel

class StorageItemType(str, Enum):
    """Enumeration for different types of storage items."""
    SENSOR = "SENSOR"
    SCREW = "SCREW"
    DISPLAY = "DISPLAY"
    NAIL = "NAIL"
    CABLE = "CABLE"
    MISCELLANEOUS = "MISCELLANEOUS"

class StorageItem(SQLModel, table=True):
    """Data model representing an item in the storage database."""
    __tablename__ = "storage"
    id: Optional[int] = Field(default=None, primary_key=True)
    position: int
    type: StorageItemType
    name: str
    info: Optional[str] = None
    modification_time: datetime = Field(default_factory=datetime.now)


