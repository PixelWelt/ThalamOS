import csv
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'data/storage.db')
mydb = sqlite3.connect(db_path, check_same_thread=False)
cursor = mydb.cursor()


def setup():
    """
    Sets up the database by creating the 'storage' table and a trigger for automatic 
    updating of the 'modification_time' column.
    The 'storage' table contains the following columns:
    - id: INTEGER, primary key, autoincrement
    - position: INTEGER
    - type: TEXT
    - name: TEXT
    - info: TEXT
    - modification_time: TIMESTAMP, defaults to the current timestamp
    The trigger 'update_modification_time' ensures that the 'modification_time' column 
    is automatically updated to the current timestamp whenever a row in the 'storage' 
    table is updated.
    Commits the changes to the database and prints a confirmation message.
    """
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS storage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        position INTEGER,
        type TEXT,
        name TEXT,
        info TEXT,
        modification_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Trigger für automatische Aktualisierung von modification_time beim Update
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS update_modification_time
    AFTER UPDATE ON storage
    FOR EACH ROW
    BEGIN
        UPDATE storage
        SET modification_time = CURRENT_TIMESTAMP
        WHERE id = OLD.id;
    END;
    """)
    mydb.commit()
    print("Database is ready for service")


def fetchCSV():
    """
    Fetches all data from the 'storage' table in the database and writes it to a CSV file named 'out.csv'.
    The function executes a SQL query to select all rows from the 'storage' table, writes the column headers
    and all rows to the CSV file, and saves the file with UTF-8 encoding.
    Raises:
        Any exceptions raised by the database cursor execution or file operations.
    """

    cursor.execute("SELECT * FROM storage;")
    with open("out.csv", "w", newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description])  # Spaltenüberschriften
        csv_writer.writerows(cursor.fetchall())  # Alle Zeilen schreiben
        csv_file.close()


def fetchItem(itemID):
    """
    Fetch an item from the storage database by its id.
    Args:
        itemID (int): The id of the item to fetch.
    Returns:
        tuple: A tuple containing the item's data if found, otherwise None.
    """

    cursor.execute("select * From storage WHERE id=?;", (itemID,))
    return cursor.fetchone()


def deleteItem(itemID):
    """
    Deletes an item from the storage database based on the provided item id.
    Args:
        itemID (int): The id of the item to be deleted from the storage.
    Returns:
        None
    """

    cursor.execute("DELETE FROM storage WHERE ID=?;", (itemID,))
    mydb.commit()


def CreateItem(pos, typ, name, jsonData):
    """
    Creates an item in the storage database.
    Args:
        pos (int): The position of the item.
        typ (str): The type of the item.
        name (str): The name of the item.
        jsonData (str): The JSON data associated with the item. If empty JSON object ("{}"), no additional info is stored.
    Returns:
        None
    """

    print("Creating item..")
    if jsonData == "{}":
        query = "INSERT INTO storage (position, type, name) VALUES (?, ?, ?);"
        params = (pos, typ, name)
    else:
        query = "INSERT INTO storage (position, type, name, info) VALUES (?, ?, ?, ?);"
        params = (pos, typ, name, jsonData)
    print(query)
    cursor.execute(query, params)
    mydb.commit()


def search(searchTerm):
    """
    Searches the storage database for entries that match the given search term.
    Args:
        searchTerm (str): The term to search for in the database. The term will be split into individual words,
                          and each word will be used to search the 'type', 'name', and 'info' columns.
    Returns:
        list: A list of tuples containing the rows from the database that match the search criteria.
              Returns None if there is an SQLite programming error.
    Raises:
        sqlite3.ProgrammingError: If there is an error executing the query.
    """
    try:
        # Split searchTerm into einzelne Wörter
        search_terms = searchTerm.split()

        # Bedingung mit Platzhaltern ? erstellen
        conditions = " AND ".join(
            ["(type LIKE ? OR name LIKE ? OR info LIKE ?)" for _ in search_terms]
        )
        query = f"""
        SELECT *
        FROM storage
        WHERE {conditions};
        """

        # Parameter für die Platzhalter erstellen
        parameters = tuple(
            f"%{term}%" for term in search_terms for _ in range(3)
        )

        # Debugging: Query und Parameter ausgeben
        print("Query:", query)
        print("Parameter:", parameters)

        # Query ausführen
        cursor.execute(query, parameters)
        results = cursor.fetchall()

        return results

    except sqlite3.ProgrammingError as e:
        print("SQLite-Error:", str(e))
        return None
