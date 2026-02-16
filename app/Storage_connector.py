"""
StorageConnector Module

This module provides functions to interact with a SQLite database for managing storage items.
It includes functionalities to set up the database, create, fetch, delete, and search items,
as well as export the data to a CSV file.
"""
import os
from typing import List
from sqlmodel import Session, create_engine, select, or_, SQLModel
from models import StorageItem, StorageItemType
from logger_config import logger


base_dir = os.path.dirname(__file__)
db_dir = os.path.join(base_dir, "data")
db_path = os.path.join(db_dir, "storage.db")
if not os.path.exists(db_dir):
    os.makedirs(db_dir)
    logger.info(f"Verzeichnis erstellt: {db_dir}")
logger.info(f"Database path: {db_path}")

# SQLAlchemy Engine erstellen
engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})

def setup():
    """Sets up the database by creating the necessary tables if they do not already exist."""
    SQLModel.metadata.create_all(engine)

def fetch_item(item_id: int) -> StorageItem | None:
    """
    Fetch an item from the storage database by its id.
    Args:
        item_id: The id of the item to fetch.
    Returns:
        The item object if found, otherwise None.
    """
    with Session(engine) as session:
        return session.get(StorageItem, item_id)


def delete_item(item_id: int) -> None:
    """
    Deletes an item from the storage database based on the provided item id.
    Args:
        item_id: The id of the item to be deleted from the storage.
    Returns:
        None
    """
    with Session(engine) as session:
        item = session.get(StorageItem, item_id)
        if item:
            session.delete(item)
            session.commit()
            logger.info(f"Item with ID {item_id} deleted.")
        else:
            logger.warning(f"Deletion failed: ID {item_id} not found.")


def create_item(pos: int, obj_type: StorageItemType, name: str, json_data: str) -> None:
    """
    Creates a new item in the storage database with the provided position, type, name, and JSON data.

    Args:
        pos: LED position of the item.
        obj_type: type of the Item
        name: name of item
        json_data: additional json ifno

    Returns:

    """
    info_value = None if json_data in ["{}", ""] else json_data

    new_item = StorageItem(
        position=pos,
        type=obj_type,
        name=name,
        info=info_value
    )

    with Session(engine) as session:
        session.add(new_item)
        session.commit()
        logger.info(f"Item created: {name}")

def search(search_term: str) -> List[StorageItem]:
    """
    Searches the storage database for entries that match the given search term.
    Args:
        search_term: The term to search for in the database. The term will be split
                          into individual words,
                          and each word will be used to search the 'type', 'name', and
                          'info' columns.
    Returns:
        A list of tuples containing the rows from the database that match the search criteria.
              Returns None if there is an SQLite programming error.
    Raises:
        sqlite3.ProgrammingError: If there is an error executing the query.
    """
    with Session(engine) as session:
        statement = select(StorageItem)
        search_words = search_term.split()

        for word in search_words:
            pattern = f"%{word}%"
            statement = statement.where(
                or_(
                    StorageItem.type.like(pattern),
                    StorageItem.name.like(pattern),
                    StorageItem.info.like(pattern)
                )
            )

        results = session.exec(statement).all()
        return list(results)


def update_item(item_id: int, pos: int, obj_type: StorageItemType, name: str, json_data: str) -> None:
    """
    Updates an item in the storage database.
    Args:
        item_id: The id of the item to update.
        pos: The new position of the item.
        obj_type: The new type of the item.
        name: The new name of the item.
        json_data: The new JSON data associated with the item.
    """
    with Session(engine) as session:
        db_item = session.get(StorageItem, item_id)
        if not db_item:
            logger.error(f"Update fehlgeschlagen: Item {item_id} nicht gefunden.")
            return

        db_item.position = pos
        db_item.type = obj_type
        db_item.name = name
        db_item.info = json_data if json_data != "{}" else None

        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        logger.info(f"Item {item_id} erfolgreich aktualisiert.")
