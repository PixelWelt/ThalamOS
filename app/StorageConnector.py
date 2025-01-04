import csv
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'data/storage.db')
mydb = sqlite3.connect(db_path, check_same_thread=False)
cursor = mydb.cursor()


def setup():
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
    cursor.execute("SELECT * FROM storage;")
    with open("out.csv", "w", newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description])  # Spaltenüberschriften
        csv_writer.writerows(cursor.fetchall())  # Alle Zeilen schreiben
        csv_file.close()


def fetchItem(itemID):
    cursor.execute("select * From storage WHERE id=?;", (itemID,))
    return cursor.fetchone()


def deleteItem(itemID):
    cursor.execute("DELETE FROM storage WHERE ID=?;", (itemID,))
    mydb.commit()


def CreateItem(pos, typ, name, jsonData):
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
        print("SQLite-Fehler:", str(e))
        return None
